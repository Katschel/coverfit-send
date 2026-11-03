from calibre.utils.config import JSONConfig
from qt.core import QCheckBox, QComboBox, QFormLayout, QLabel, QSpinBox, QWidget

# (key, title, width, height) -- portrait px. Models with the same screen are merged into one entry.
# Verify for your model.
MODELS = [
    ('basic-2022', 'Kindle Basic (2022-2026)', 1072, 1448),
    ('basic-2019', 'Kindle Basic (2019)', 600, 800),
    ('pw-2024', 'Kindle Paperwhite (2024-2026)', 1264, 1680),
    ('pw-2021', 'Kindle Paperwhite (2021, 11th gen)', 1236, 1648),
    ('pw-2015', 'Kindle Paperwhite (2015-2018)', 1072, 1448),
    ('pw-2012', 'Kindle Paperwhite (2012-2013)', 758, 1024),
    ('colorsoft', 'Kindle Colorsoft (2024-2026)', 1264, 1680),
    ('oasis-2017', 'Kindle Oasis (2017-2019)', 1264, 1680),
    ('oasis-2016', 'Kindle Oasis (2016)', 1072, 1448),
    ('voyage', 'Kindle Voyage (2014)', 1072, 1448),
    ('scribe-11', 'Kindle Scribe 11" (2025-2026)', 1980, 2640),
    ('scribe-10', 'Kindle Scribe (2022-2024)', 1860, 2480),
]
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

        self.enabled = QCheckBox('Fit the cover to the Kindle screen before sending')
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

        self.model = QComboBox()
        for k, title, w, h in MODELS:
            self.model.addItem(title, k)
        self.model.addItem('Other / custom size', CUSTOM)
        self.model.setCurrentIndex(max(0, self.model.findData(_model_key())))
        form.addRow('Kindle model', self.model)

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

        self.model.currentIndexChanged.connect(self._update)
        self.w.valueChanged.connect(self._update)
        self.h.valueChanged.connect(self._update)
        self._update()

    def _update(self, *a):
        key = self.model.currentData()
        custom = key == CUSTOM
        for lbl, spin in self.custom_rows:
            lbl.setVisible(custom)
            spin.setVisible(custom)
        if custom:
            self.res.setText('%d x %d px' % (self.w.value(), self.h.value()))
        else:
            m = next(m for m in MODELS if m[0] == key)
            self.res.setText('%d x %d px' % (m[2], m[3]))

    def save_settings(self):
        prefs['enabled'] = self.enabled.isChecked()
        if self.to.currentData():
            prefs['to'] = self.to.currentData()
        prefs['model'] = self.model.currentData()
        prefs['width'] = self.w.value()
        prefs['height'] = self.h.value()
        prefs['mode'] = self.mode.currentData()
