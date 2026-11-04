from calibre.utils.config import JSONConfig
from qt.core import QCheckBox, QComboBox, QFormLayout, QLabel, QSpinBox, QWidget

# (brand key, brand title, [(model key, title, width, height), ...]) -- portrait px.
# Models with the same screen are grouped into one entry. Verify for your model;
# use "Other / custom size" if it is not listed.
BRANDS = [
    ('kindle', 'Kindle', [
        ('basic-2022', 'Basic (2022-2026)', 1072, 1448),
        ('pw-2024', 'Paperwhite (2024-2026)', 1264, 1680),
        ('pw-2021', 'Paperwhite (2021, 11th gen)', 1236, 1648),
        ('colorsoft', 'Colorsoft (2024-2026)', 1264, 1680),
        ('scribe-11', 'Scribe 11" (2025-2026)', 1980, 2640),
        ('scribe-10', 'Scribe (2022-2024)', 1860, 2480),
    ]),
    ('kobo', 'Kobo', [
        ('kobo-6', 'Clara 2E / Clara BW / Clara Colour (6")', 1072, 1448),
        ('kobo-7', 'Libra 2 / Libra Colour (7")', 1264, 1680),
        ('kobo-8', 'Sage (8")', 1440, 1920),
        ('kobo-10', 'Elipsa / Elipsa 2E (10.3")', 1404, 1872),
    ]),
    ('tolino', 'Tolino', [
        ('tolino-6', 'Shine 4 / Shine 5 / Shine Color (6")', 1072, 1448),
        ('tolino-6-lo', 'Page 2 (6")', 758, 1024),
        ('tolino-7', 'Vision 5 / Vision 6 / Vision Color (7")', 1264, 1680),
        ('tolino-8', 'Epos 2 / Epos 3 (8")', 1404, 1872),
    ]),
    ('pocketbook', 'PocketBook', [
        ('pocketbook-6', 'Verse / Verse Lite / Basic Lux 3-4 (6")', 758, 1024),
        ('pocketbook-6-hi', 'Verse Pro / Verse Pro Color (6")', 1072, 1448),
        ('pocketbook-7', 'Era / Era Color / Era Lite (7")', 1264, 1680),
        ('pocketbook-78', 'InkPad 4 / Color 2 / Color 3 (7.8")', 1404, 1872),
        ('pocketbook-97', 'InkPad Lite (9.7")', 825, 1200),
        ('pocketbook-10', 'InkPad X Pro / Color Note / InkPad One (10.3")', 1404, 1872),
        ('pocketbook-10-hi', 'InkPad Eo / Eo 2 (10.3")', 1860, 2480),
    ]),
    ('boox', 'Onyx Boox', [
        ('boox-6', 'Go 6 / Poke 5 (6")', 1072, 1448),
        ('boox-6-lo', 'Poke 4 Lite (6")', 758, 1024),
        ('boox-picco', 'Picco (3.97")', 480, 800),
        ('boox-palma', 'Palma / Palma 2 / Palma 3 (6.13")', 824, 1648),
        ('boox-7', 'Page / Go 7 / Go Color 7 / Leaf (7")', 1264, 1680),
        ('boox-78', 'Nova Air / Nova Air 2 / Tab Mini C (7.8")', 1404, 1872),
        ('boox-10', 'Note Air 2 / Air 3 / Note 5 / Tab Ultra (10.3")', 1404, 1872),
        ('boox-10-hi', 'Go 10.3 / Note Air 3 C-6 C / Tab Ultra C (10.3")', 1860, 2480),
        ('boox-85', 'Note Mini C (8.5")', 1536, 2048),
        ('boox-133', 'Max Lumi 2 / Tab X (13.3", 2023)', 1650, 2200),
        ('boox-133-hi', 'Note Max / Tab X C (13.3")', 2400, 3200),
    ]),
]
MODELS = [(k, '%s %s' % (bt, t), w, h) for _, bt, ms in BRANDS for k, t, w, h in ms]  # flat list
CUSTOM = 'custom'
DEFAULT_MODEL = 'basic-2022'

prefs = JSONConfig('plugins/coverfit_send')
prefs.defaults['enabled'] = True
prefs.defaults['model'] = ''             # key from MODELS, or 'custom'; empty = not chosen yet
prefs.defaults['screen'] = ''            # legacy (v0.6): 'WxH'
prefs.defaults['preset'] = ''            # legacy: model label
prefs.defaults['width'] = 1072           # used for 'custom'
prefs.defaults['height'] = 1448
prefs.defaults['mode'] = 'stretch'       # 'stretch' (distorts) or 'crop' (keeps proportions)
prefs.defaults['to'] = ''                # default recipient; empty = Calibre's default email account
prefs.defaults['toolbar_added'] = ''

# models dropped from the list: users who had one selected keep their size as a custom size
_DROPPED = {'basic-2019': (600, 800), 'pw-2015': (1072, 1448), 'pw-2012': (758, 1024),
            'oasis-2017': (1264, 1680), 'oasis-2016': (1072, 1448), 'voyage': (1072, 1448)}
if prefs['model'] in _DROPPED:
    prefs['width'], prefs['height'] = _DROPPED[prefs['model']]
    prefs['model'] = 'custom'

# one-time carry-over of the settings file used under the old plugin name
_old = JSONConfig('plugins/coverfill')
if len(_old) and not len(prefs):
    for _k, _v in _old.items():
        prefs[_k] = _v


def _by_size(w, h):
    return next((m[0] for m in MODELS if (m[2], m[3]) == (w, h)), DEFAULT_MODEL)


def _model_key():
    if prefs['model']:
        return prefs['model']
    if 'x' in prefs['screen'] and prefs['screen'] != CUSTOM:  # v0.6 setting
        try:
            w, h = map(int, prefs['screen'].split('x'))
            return _by_size(w, h)
        except ValueError:
            pass
    return DEFAULT_MODEL


def _brand_of(key):
    return next((b[0] for b in BRANDS if any(m[0] == key for m in b[2])), CUSTOM)


def get_size():
    key = _model_key()
    for k, title, w, h in MODELS:
        if k == key:
            return w, h
    return prefs['width'], prefs['height']


class ConfigWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        from calibre_plugins.coverfit_send.sender import get_accounts
        self.setMinimumWidth(520)
        form = QFormLayout(self)
        form.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)
        form.setVerticalSpacing(10)

        self.enabled = QCheckBox('Fit the cover to the e-reader screen before sending')
        self.enabled.setChecked(prefs['enabled'])
        form.addRow(self.enabled)

        self.to = QComboBox()
        addrs, default = get_accounts()
        for a in addrs:
            self.to.addItem(a + ('  (default)' if a == default else ''), a)
        if addrs:
            cur = prefs['to'] if prefs['to'] in addrs else default
            self.to.setCurrentIndex(max(0, self.to.findData(cur)))
        else:
            self.to.setEnabled(False)
            self.to.addItem('No address set up: see Preferences > Sharing books by email', '')
        form.addRow('Default recipient', self.to)

        key = _model_key()
        self.brand = QComboBox()
        for bk, bt, ms in BRANDS:
            self.brand.addItem(bt, bk)
        self.brand.addItem('Other / custom size', CUSTOM)
        self.brand.setCurrentIndex(max(0, self.brand.findData(_brand_of(key))))
        form.addRow('Brand', self.brand)

        self.model = QComboBox()
        self.model_lbl = QLabel('Model')
        form.addRow(self.model_lbl, self.model)

        self.res = QLabel()
        form.addRow('Screen', self.res)

        self.w = QSpinBox(); self.w.setRange(200, 4000); self.w.setValue(prefs['width']); self.w.setSuffix(' px')
        self.h = QSpinBox(); self.h.setRange(200, 4000); self.h.setValue(prefs['height']); self.h.setSuffix(' px')
        self.custom_rows = [(QLabel('Width'), self.w), (QLabel('Height'), self.h)]
        for lbl, spin in self.custom_rows:
            form.addRow(lbl, spin)

        self.mode = QComboBox()
        self.mode.addItem('Stretch (fills exactly, may distort)', 'stretch')
        self.mode.addItem('Crop (keeps proportions, trims edges)', 'crop')
        self.mode.setCurrentIndex(max(0, self.mode.findData(prefs['mode'])))
        form.addRow('Fit mode', self.mode)

        for text in ('Recipients and mail server are set up in Calibre under Preferences > Sharing books by email.',
                     'Your library stays untouched. Only a temporary copy gets the fitted cover.'):
            note = QLabel(text)
            note.setWordWrap(True)
            note.setStyleSheet('color: gray;')
            form.addRow(note)

        self.brand.currentIndexChanged.connect(lambda *a: self._fill_models())
        self.model.currentIndexChanged.connect(self._update)
        self.w.valueChanged.connect(self._update)
        self.h.valueChanged.connect(self._update)
        self._fill_models(key)  # needs all widgets above, so it runs last

    def _fill_models(self, select=None):
        """Show only the models of the chosen brand."""
        self.model.blockSignals(True)
        self.model.clear()
        models = next((b[2] for b in BRANDS if b[0] == self.brand.currentData()), [])
        for k, title, w, h in models:
            self.model.addItem(title, k)
        self.model.setCurrentIndex(max(0, self.model.findData(select)))
        self.model.blockSignals(False)
        self._update()

    def _update(self, *a):
        custom = self.brand.currentData() == CUSTOM
        self.model_lbl.setVisible(not custom)
        self.model.setVisible(not custom)
        for lbl, spin in self.custom_rows:
            lbl.setVisible(custom)
            spin.setVisible(custom)
        if custom:
            self.res.setText('%d x %d px' % (self.w.value(), self.h.value()))
        else:
            m = next((m for m in MODELS if m[0] == self.model.currentData()), None)
            self.res.setText('%d x %d px' % (m[2], m[3]) if m else '')

    def save_settings(self):
        prefs['enabled'] = self.enabled.isChecked()
        if self.to.currentData():
            prefs['to'] = self.to.currentData()
        prefs['model'] = CUSTOM if self.brand.currentData() == CUSTOM else self.model.currentData()
        prefs['width'] = self.w.value()
        prefs['height'] = self.h.value()
        prefs['mode'] = self.mode.currentData()
