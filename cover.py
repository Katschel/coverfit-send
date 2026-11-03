import io
import posixpath
import zipfile
from urllib.parse import unquote
from xml.etree import ElementTree as ET

from PIL import Image, ImageOps

C = '{urn:oasis:names:tc:opendocument:xmlns:container}'
O = '{http://www.idpf.org/2007/opf}'


def find_cover_path(z):
    """Return the zip path of the cover image, or None."""
    opf = ET.fromstring(z.read('META-INF/container.xml')).find('.//%srootfile' % C).get('full-path')
    pkg = ET.fromstring(z.read(opf))
    items = pkg.findall('.//%sitem' % O)
    cover = next((i for i in items if 'cover-image' in (i.get('properties') or '').split()), None)
    if cover is None:  # EPUB 2: <meta name="cover" content="item-id">
        for m in pkg.findall('.//%smeta' % O):
            if m.get('name') == 'cover':
                cover = next((i for i in items if i.get('id') == m.get('content')), None)
                break
    if cover is None:
        return None
    return posixpath.normpath(posixpath.join(posixpath.dirname(opf), unquote(cover.get('href'))))


def fit_image(data, path, w, h, mode):
    img = Image.open(io.BytesIO(data)).convert('RGB')
    if mode == 'crop':
        img = ImageOps.fit(img, (w, h), Image.LANCZOS)
    else:
        img = img.resize((w, h), Image.LANCZOS)
    out = io.BytesIO()
    if path.lower().endswith('.png'):
        img.save(out, 'PNG')
    else:
        img.save(out, 'JPEG', quality=92)
    return out.getvalue()


def make_fitted_copy(src, dst, w, h, mode):
    """Write a copy of src EPUB to dst with the cover resized. Returns True if a cover was changed."""
    with zipfile.ZipFile(src) as zin:
        cover = find_cover_path(zin)
        if not cover or cover not in zin.namelist():
            return False
        with zipfile.ZipFile(dst, 'w') as zout:
            for info in zin.infolist():  # keeps order, so 'mimetype' stays first
                data = zin.read(info.filename)
                if info.filename == cover:
                    data = fit_image(data, cover, w, h, mode)
                zout.writestr(info, data, compress_type=info.compress_type)
    return True
