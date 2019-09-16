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

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QListWidget, QButtonGroup, QTableWidget
from qgis.core import QgsProject, Qgis, QgsSettings

from ..setting import Setting
from ..setting_widget import SettingWidget


class Stringlist(Setting):
    def __init__(self, name, scope, default_value, **kwargs):
        Setting.__init__(self, name, scope, default_value,
                         object_type=None,
                         qsettings_read=lambda key, def_val: QgsSettings().value(key, def_val),
                         qsettings_write=lambda key, val: QgsSettings().setValue(key, val),
                         project_read=lambda plugin, key, def_val: QgsProject.instance().readListEntry(plugin, key, def_val)[0],
                         **kwargs)

    def read_out(self, value, scope):
        # always cast to list
        if value is not None:
            value = list(value)
        else:
            value = []
        return value

    def write_in(self, value, scope):
        # always cast to list
        if value is not None:
            value = list(value)
        return value

    def check(self, value):
        if value is not None and type(value) not in (list, tuple):
            self.info('{}:: Invalid value for setting {}: {}. It must be a string list.'
                      .format(self.plugin_name, self.name, value),
                      Qgis.Warning)
            return False
        return True

    def config_widget(self, widget):
        if type(widget) == QListWidget:
            return ListStringListWidget(self, widget)
        elif type(widget) == QTableWidget:
            return TableWidgetStringListWidget(self, widget)
        elif type(widget) == QButtonGroup:
            return ButtonGroupStringListWidget(self, widget)
        else:
            raise NameError("SettingManager does not handle %s widgets for integers for the moment (setting: %s)" %
                            (type(widget), self.name))


class ListStringListWidget(SettingWidget):
    def __init__(self, setting, widget):
        signal = widget.itemChanged
        SettingWidget.__init__(self, setting, widget, signal)

    def set_widget_value(self, value):
        for i in range(self.widget.count()):
            item = self.widget.item(i)
            if item.text() in value:
                item.setCheckState(Qt.Checked)
            else:
                item.setCheckState(Qt.Unchecked)

    def widget_value(self):
        value = []
        for i in range(self.widget.count()):
            item = self.widget.item(i)
            if item.checkState() == Qt.Checked:
                value.append(item.text())
        return value


class TableWidgetStringListWidget(SettingWidget):
    def __init__(self, setting, widget: QTableWidget):
        signal = widget.itemChanged
        SettingWidget.__init__(self, setting, widget, signal)
        self._column = 0
        self._userdata = False
        self._invert = False

    @property
    def column(self):
        return self._column

    @column.setter
    def column(self, value: int):
        self._column = value

    @property
    def userdata(self):
        return self._userdata

    @userdata.setter
    def userdata(self, value: bool):
        self._userdata = value

    @property
    def invert(self):
        return self._invert

    @invert.setter
    def invert(self, value: bool):
        self._invert = value

    def set_widget_value(self, value):
        for r in range(self.widget.rowCount()):
            item = self.widget.item(r, self._column)
            data = item.data(Qt.UserRole) if self._userdata else item.text()
            if not self._invert and data in value or \
                   self._invert and data not in value:
                item.setCheckState(Qt.Checked)
            else:
                item.setCheckState(Qt.Unchecked)

    def widget_value(self):
        value = []
        for i in range(self.widget.rowCount()):
            item = self.widget.item(i, self._column)
            if not self._invert and item.checkState() == Qt.Checked or \
                   self._invert and item.checkState() == Qt.Unchecked:
                data = item.data(Qt.UserRole) if self._userdata else item.text()
                value.append(data)
        return value


class ButtonGroupStringListWidget(SettingWidget):
    def __init__(self, setting, widget):
        signal = widget.buttonClicked
        SettingWidget.__init__(self, setting, widget, signal)

    def set_widget_value(self, value):
        for item in self.widget.buttons():
            item.setChecked(item.objectName() in value)

    def widget_value(self):
        value = []
        for item in self.widget.buttons():
            if item.isChecked():
                value.append(item.objectName())
        return value






