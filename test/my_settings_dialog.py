
from PyQt4.QtGui import QDialog
from qgis.gui import QgsCollapsibleGroupBox
from ..setting_dialog import SettingDialog
from my_settings import MySettings


class MySettingsDialog(QDialog, SettingDialog):
    def __init__(self, setting_name, widget_class, set_values_on_dialog_accepted, set_value_on_widget_update):
        QDialog.__init__(self)

        self.settings = MySettings()
        w = widget_class(self)
        w.setObjectName(setting_name)

        if widget_class == QgsCollapsibleGroupBox:
            w.setCheckable(True)

        SettingDialog.__init__(self, self.settings, set_values_on_dialog_accepted, set_value_on_widget_update)
