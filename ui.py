from calibre.gui2 import error_dialog, info_dialog
from calibre.gui2.actions import InterfaceAction
from qt.core import QMenu, QToolButton


class CoverFitSendAction(InterfaceAction):
    name = 'CoverFit Send'
    action_spec = ('CoverFit Send', None,
                   'Email selected books (cover fitted to the screen) to your Kindle', None)
    popup_type = QToolButton.ToolButtonPopupMode.MenuButtonPopup

    def _icon(self):
        from qt.core import QIcon, QPixmap
        try:
            return get_icons('images/icon.png', 'CoverFit Send')  # noqa: F821 (injected by calibre)
        except Exception:
            pass
        try:
            data = self.interface_action_base_plugin.load_resources(['images/icon.png'])['images/icon.png']
            pm = QPixmap()
            pm.loadFromData(data)
            if not pm.isNull():
                return QIcon(pm)
        except Exception:
            pass
        return QIcon.ic('mail.png')  # built-in Calibre icon as a fallback

    def genesis(self):
        from calibre_plugins.coverfit_send.config import prefs
        icon = self._icon()
        self.qaction.setIcon(icon)
        self.menu = QMenu(self.gui)
        self.qaction.setMenu(self.menu)
        self.qaction.triggered.connect(lambda checked=False: self.send())

        self.create_menu_action(self.menu, 'coverfit-send', 'Email to default address',
                                icon=icon, triggered=lambda checked=False: self.send())
        self.send_menu = self.menu.addMenu('Email to...')
        self.menu.aboutToShow.connect(self._fill_send_menu)
        self._fill_send_menu()
        self.toggle = self.create_menu_action(self.menu, 'coverfit-send-toggle', 'Fit cover to screen',
                                              triggered=self.toggle_enabled)
        self.toggle.setCheckable(True)
        self.toggle.setChecked(prefs['enabled'])
        self.menu.addSeparator()
        self.create_menu_action(self.menu, 'coverfit-send-settings', 'Settings...',
                                icon='config.png', triggered=self.show_settings)
        self._add_to_toolbar()

    def _fill_send_menu(self):
        """List the addresses from Calibre's email settings."""
        from calibre_plugins.coverfit_send.sender import get_accounts
        self.send_menu.clear()
        try:
            addrs, default = get_accounts()
        except Exception:
            addrs, default = [], None
        for a in addrs:
            act = self.send_menu.addAction(a + ('  (default)' if a == default else ''))
            act.triggered.connect(lambda checked=False, a=a: self.send(a))

    def _add_to_toolbar(self):
        """Put the button on the main toolbar once, on first run (the user can remove it later)."""
        from calibre.gui2 import gprefs
        from calibre_plugins.coverfit_send.config import prefs
        if prefs['toolbar_added'] == self.name:
            return
        key = 'action-layout-toolbar'
        layout = list(gprefs[key])
        if self.name not in layout:
            layout.append(self.name)
            gprefs[key] = tuple(layout)
        prefs['toolbar_added'] = self.name

    def toggle_enabled(self, *a):
        from calibre_plugins.coverfit_send.config import prefs
        prefs['enabled'] = self.toggle.isChecked()

    def show_settings(self):
        from calibre_plugins.coverfit_send.config import prefs
        self.interface_action_base_plugin.do_user_config(self.gui)
        self.toggle.setChecked(prefs['enabled'])

    def send(self, to=None):
        try:
            self._send(to)
        except Exception:
            import traceback
            error_dialog(self.gui, self.name, 'CoverFit Send hit an error while sending.',
                         det_msg=traceback.format_exc(), show=True)

    def _send(self, to=None):
        from calibre_plugins.coverfit_send.config import get_size, prefs
        from calibre_plugins.coverfit_send.sender import get_accounts

        rows = self.gui.library_view.selectionModel().selectedRows()
        if not rows:
            return error_dialog(self.gui, self.name, 'Select a book first.', show=True)
        try:
            addrs, default = get_accounts()
        except Exception as e:
            return error_dialog(self.gui, self.name, 'Could not read the email settings: %s' % e, show=True)
        if not to:
            to = prefs['to'] if prefs['to'] in addrs else default
        if not to:
            return error_dialog(self.gui, self.name,
                                'No address set up under Preferences > Sharing books by email.', show=True)

        db = self.gui.current_db.new_api
        items, skipped = [], []
        for r in rows:
            book_id = self.gui.library_view.model().id(r)
            title = db.field_for('title', book_id)
            src = db.format_abspath(book_id, 'EPUB')
            if src:
                items.append((title, src, title + '.epub'))
            else:
                skipped.append(title)
        if skipped:
            info_dialog(self.gui, self.name, 'No EPUB for: ' + ', '.join(skipped), show=True)
        if not items:
            return

        import atexit
        import os
        import shutil
        import tempfile
        from calibre.gui2 import Dispatcher
        from calibre.utils.filenames import ascii_filename
        from calibre_plugins.coverfit_send.cover import make_fitted_copy

        w, h = get_size()
        tmp = tempfile.mkdtemp(prefix='coverfit_')
        atexit.register(shutil.rmtree, tmp, True)
        jobs, files, subjects, texts, names = [], [], [], [], []
        for i, (title, src, fname) in enumerate(items):
            path = src
            if prefs['enabled']:
                dst = os.path.join(tmp, '%d.epub' % i)
                try:
                    if make_fitted_copy(src, dst, w, h, prefs['mode']):
                        path = dst
                except Exception:
                    pass  # send the original unchanged
            jobs.append(title)
            files.append(path)
            subjects.append('E-book: ' + title)
            texts.append('Sent from calibre')
            names.append(ascii_filename(fname))

        # Calibre's own email jobs: they show up in the job queue and use the saved mail settings
        from calibre.gui2.email import send_mails
        send_mails(jobs, Dispatcher(self.done), files, [to] * len(files),
                   subjects, texts, names, self.gui.job_manager)
        self.gui.status_bar.show_message('Sending %d book(s) to %s' % (len(items), to), 3000)

    def done(self, job):
        pass  # Calibre's email job reports success/failure itself
