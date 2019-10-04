#-----------------------------------------------------------
#
# QGIS setting manager is a python module to easily manage read/write
# settings and set/get corresponding widgets.
#
# Copyright    : (C) 2019 Denis Rouzaud
# Email        : denis@opengis.ch
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

from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtWidgets import QListWidget, QButtonGroup, QTableWidget

from ..setting_widget import SettingWidget


class ListStringListWidget(SettingWidget):
    def __init__(self, setting, widget: QListWidget):
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
    def column(self) -> int:
        return self._column

    @column.setter
    def column(self, value: int):
        self._column = value

    @property
    def userdata(self) -> bool:
        return self._userdata

    @userdata.setter
    def userdata(self, value: bool):
        self._userdata = value

    @property
    def invert(self) -> bool:
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
    def __init__(self, setting, widget: QButtonGroup):
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

