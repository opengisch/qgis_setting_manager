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

from enum import Enum

from qgis.core import QgsProject, QgsCoordinateReferenceSystem

from ..setting_widget import SettingWidget


class ComboMode(Enum):
    Text = 1
    Data = 2


class LineEditStringWidget(SettingWidget):
    def __init__(self, setting, widget):
        signal = widget.textChanged
        SettingWidget.__init__(self, setting, widget, signal)

    def set_widget_value(self, value):
        self.widget.setText(value)

    def widget_value(self):
        return self.widget.text()


class ButtonGroupStringWidget(SettingWidget):
    def __init__(self, setting, widget):
        signal = widget.buttonClicked
        SettingWidget.__init__(self, setting, widget, signal)

    def set_widget_value(self, value):
        for button in self.widget.buttons():
            if value == button.objectName():
                button.setChecked(True)
                break

    def widget_value(self):
        value = ""
        for button in self.widget.buttons():
            if button.isChecked():
                value = button.objectName()
                break
        return value


class ComboStringWidget(SettingWidget):
    def __init__(self, setting, widget):
        self._mode = ComboMode.Data
        signal = widget.currentIndexChanged
        SettingWidget.__init__(self, setting, widget, signal)

    @property
    def mode(self) -> ComboMode:
        """Defines if setting is found directly in combobox text or rather in the userData."""
        return self._mode

    @mode.setter
    def mode(self, value: ComboMode):
        self._mode = value

    def auto_populate(self):
        for v in self.setting.allowed_values:
            self.widget.addItem(v)
        self.mode = ComboMode.Text
        self.set_widget_from_value()

    def set_widget_value(self, value):
        if self._mode is ComboMode.Text:
            self.widget.setCurrentIndex(self.widget.findText(value))
        else:
            self.widget.setCurrentIndex(self.widget.findData(value))

    def widget_value(self):
        if self._mode is ComboMode.Text:
            return self.widget.currentText()
        else:
            return self.widget.itemData(self.widget.currentIndex()) or ""


class MapLayerComboStringWidget(SettingWidget):
    def __init__(self, setting, widget):
        signal = widget.layerChanged
        SettingWidget.__init__(self, setting, widget, signal)

    def set_widget_value(self, value):
        self.widget.setLayer(QgsProject.instance().mapLayer(value))

    def widget_value(self):
        layer = self.widget.currentLayer()
        if layer is not None:
            return layer.id()
        else:
            return ""


class FieldComboStringWidget(SettingWidget):
    def __init__(self, setting, widget):
        signal = widget.currentIndexChanged
        SettingWidget.__init__(self, setting, widget, signal)

    def set_widget_value(self, value):
        self.widget.setField(value)

    def widget_value(self):
        return self.widget.currentField()


class FileStringWidget(SettingWidget):
    def __init__(self, setting, widget):
        signal = widget.fileChanged
        SettingWidget.__init__(self, setting, widget, signal)

    def set_widget_value(self, value):
        self.widget.setFilePath(value)

    def widget_value(self):
        return self.widget.filePath()


class ProjectionStringWidget(SettingWidget):
    def __init__(self, setting, widget):
        signal = widget.crsChanged
        SettingWidget.__init__(self, setting, widget, signal)

    def set_widget_value(self, value):
        self.widget.setCrs(QgsCoordinateReferenceSystem(value))

    def widget_value(self):
        return self.widget.crs().authid()


class AuthConfigSelectStringWidget(SettingWidget):
    def __init__(self, setting, widget):
        signal = widget.selectedConfigIdChanged
        SettingWidget.__init__(self, setting, widget, signal)

    def set_widget_value(self, value):
        self.widget.setConfigId(value)

    def widget_value(self):
        return self.widget.configId()
