#-----------------------------------------------------------
#
# QGIS setting manager is a python module to easily manage read/write
# settings and set/get corresponding widgets.
#
# Copyright    : (C) 2013 Denis Rouzaud
# Email        : denis.rouzaud@gmail.com
#
#-----------------------------------------------------------
#
# licensed under the terms of GNU GPL 2
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this progsram; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
#---------------------------------------------------------------------

from PyQt4.QtGui import QDialog, QWidget, QButtonGroup

from setting_manager import Debug


class SettingDialog:
    def __init__(self, setting_manager, set_values_on_dialog_accepted=True, set_value_on_widget_update=False):
        if isinstance(self, QDialog) and set_values_on_dialog_accepted:
            self.accepted.connect(self.accept_dialog)

        self.setting_manager = setting_manager

        self.__settings = []
        for setting_name in setting_manager.settings_list():
            for objectClass in (QWidget, QButtonGroup):
                widget = self.findChild(objectClass, setting_name)
                if widget is not None:
                    if Debug:
                        print "Widget found: {}".format(setting_name)
                    self.setting_manager.set_widget(setting_name, widget)
                    if set_value_on_widget_update:
                        self.setting_manager.set_value_on_widget_update_signal(setting_name)
                    self.__settings.append(setting_name)
                    break

        # in case the widget has no showEvent
        self.set_widgets_from_values()

    def showEvent(self, e):
        self.set_widgets_from_values()

    def before_accept_dialog(self):
        """
        you can override this method in the PluginSettings subclass
        """
        return True

    def widget_list(self):
        """
        returns the list of widgets related to settings
        """
        return self.__settings

    def setting(self, name):
        if name not in self.__settings:
            return None
        return self.setting_manager.setting(name)

    def accept_dialog(self):
        if self.before_accept_dialog():
            self.set_values_from_widgets()

    def set_values_from_widgets(self):
        for setting_name in self.__settings:
            self.setting_manager.set_value_from_widget(setting_name)

    def set_widgets_from_values(self):
        for setting_name in self.__settings:
            self.setting_manager.set_widget_from_value(setting_name)

    # deprecated
    # TODO python 3 remove deprecated method
    def onBeforeAcceptDialog(self):
        return self.before_accept_dialog()