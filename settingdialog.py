from PyQt4.QtGui import QDialog


class SettingDialog():
    def __init__(self, settingManager, setValuesOnDialogAccepted=True, setValueOnWidgetUpdate=False):
        if not isinstance(self, QDialog):
            raise NameError("PluginSettingsDialog should be instantiated as QDialog first.")
        if setValuesOnDialogAccepted:
            self.accepted.connect(self.acceptDialog)

        self._settings = []
        for setting in settingManager.settings:
            if hasattr(self, setting.name):
                setting.setWidget(getattr(self, setting.name))
                if setValueOnWidgetUpdate:
                    setting.setValueOnWidgetUpdateSignal()
                self._settings.append(setting)

    """
    you can override this method in the PluginSettings subclass
    """
    def onBeforeAcceptDialog(self):
        return True

    def acceptDialog(self):
        if self.onBeforeAcceptDialog():
            self.setValuesFromWidgets()

    def showEvent(self, e):
        self.setWidgetsFromValues()

    def setValuesFromWidgets(self):
        for setting in self._settings:
            if setting.widget is not None:
                setting.setValueFromWidget()

    def setWidgetsFromValues(self):
        for setting in self._settings:
            if setting.widget is not None:
                setting.setWidgetFromValue()