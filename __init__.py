from calibre.customize import InterfaceActionBase


class CoverFitSend(InterfaceActionBase):
    name = 'CoverFit Send'
    description = 'Email books to your e-reader with the cover fitted to the screen'
    supported_platforms = ['windows', 'osx', 'linux']
    author = 'Katschel'
    version = (0, 8)
    minimum_calibre_version = (5, 0, 0)
    actual_plugin = 'calibre_plugins.coverfit_send.ui:CoverFitSendAction'

    def is_customizable(self):
        return True

    def config_widget(self):
        from calibre_plugins.coverfit_send.config import ConfigWidget
        return ConfigWidget()

    def save_settings(self, config_widget):
        config_widget.save_settings()
