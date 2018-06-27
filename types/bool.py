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

from PyQt5.QtWidgets import QCheckBox
from qgis.core import QgsProject, Qgis
from qgis.gui import QgsCollapsibleGroupBox
from ..setting import Setting
from ..setting_widget import SettingWidget


class Bool(Setting):

    def __init__(self, name, scope, default_value, **kwargs):
        Setting.__init__(self, name, scope, default_value,
                         object_type=bool,
                         project_read=lambda plugin, key, def_val: QgsProject.instance().readBoolEntry(plugin, key, def_val)[0],
                         project_write=lambda plugin, key, val: QgsProject.instance().writeEntryBool(plugin, key, val),
                         **kwargs)

    def check(self, value: bool):
        if type(value) != bool:
            self.info('{}:: Invalid value for setting {}: {}. It must be a boolean.'
                      .format(self.plugin_name, self.name, value),
                      Qgis.Warning)
            return False
        return True

    def config_widget(self, widget):
        if isinstance(widget, QCheckBox):
            return CheckBoxBoolWidget(self, widget)
        elif isinstance(widget, QgsCollapsibleGroupBox):
            return QgsCollapsibleGroupBoxBoolWidget(self, widget)
        elif hasattr(widget, "isCheckable") and widget.isCheckable():
            return CheckableBoolWidget(self, widget)
        else:
            raise NameError("SettingManager does not handle %s widgets for booleans at the moment (setting: %s)" %
                            (type(widget), self.name))


class CheckBoxBoolWidget(SettingWidget):
    def __init__(self, setting, widget):
        signal = widget.toggled
        SettingWidget.__init__(self, setting, widget, signal)

    def set_widget_value(self, value):
        self.widget.setChecked(value)

    def widget_value(self):
        return self.widget.isChecked()


class QgsCollapsibleGroupBoxBoolWidget(SettingWidget):
    def __init__(self, setting, widget):
        signal = widget.toggled
        SettingWidget.__init__(self, setting, widget, signal)

    def set_widget_value(self, value):
        self.widget.setChecked(value)

    def widget_value(self):
        return self.widget.isChecked()


class CheckableBoolWidget(SettingWidget):
    def __init__(self, setting, widget):
        signal = widget.clicked
        SettingWidget.__init__(self, setting, widget, signal)

    def set_widget_value(self, value):
        self.widget.setChecked(value)

    def widget_value(self):
        return self.widget.isChecked()
