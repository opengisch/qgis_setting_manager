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

from PyQt5.QtWidgets import QLineEdit, QDoubleSpinBox
from qgis.core import QgsProject, Qgis

from ..setting import Setting
from ..setting_widget import SettingWidget


class Double(Setting):

    def __init__(self, name, scope, default_value, **kwargs):
        Setting.__init__(self, name, scope, default_value, float, QgsProject.instance().readDoubleEntry,
                         QgsProject.instance().writeEntryDouble, kwargs)

    def check(self, value):
        if type(value) != int and type(value) != float:
            self.info('{}:: Invalid value for setting {}: {}. It must be a floating number.'
                      .format(self.plugin_name, self.name, value),
                      Qgis.Warning)
            return False
        return True

    def config_widget(self, widget):
        if type(widget) == QLineEdit:
            return LineEditDoubleWidget(self, widget)
        elif type(widget) == QDoubleSpinBox:
            return DoubleSpinBoxDoubleWidget(self, widget)
        else:
            raise NameError("SettingManager does not handle %s widgets for integers for the moment (setting: %s)" %
                            (type(widget), self.name))


class LineEditDoubleWidget(SettingWidget):
    def __init__(self, setting, widget):
        signal = widget.textChanged
        SettingWidget.__init__(self, setting, widget, signal)

    def set_widget_value(self, value):
        self.widget.setText('{}'.format(value))

    def widget_value(self):
        return float(self.widget.text())


class DoubleSpinBoxDoubleWidget(SettingWidget):
    def __init__(self, setting, widget):
        signal = widget.valueChanged
        SettingWidget.__init__(self, setting, widget, signal)

    def set_widget_value(self, value):
        self.widget.setValue(value)

    def widget_value(self):
        return self.widget.value()



