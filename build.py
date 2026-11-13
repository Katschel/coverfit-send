import pathlib
import zipfile

root = pathlib.Path(__file__).resolve().parent
src = root / 'plugin' if (root / 'plugin' / '__init__.py').exists() else root
out = root / 'CoverFit_Send.zip'

count = 0
with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as z:
    for f in sorted(src.rglob('*')):
        rel = f.relative_to(src)
        if not f.is_file() or rel.parts[0].startswith('.') or '__pycache__' in rel.parts:
            continue
        if f.name == 'build.py':
            continue
        if f.suffix in ('.py', '.png') or f.name.startswith('plugin-import-name'):
            z.write(f, rel.as_posix())
            count += 1

if count == 0:
    raise SystemExit('No plugin files found in ' + str(src))
print('built', out, 'with', count, 'files')