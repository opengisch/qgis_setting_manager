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


# options:
# combo_mode: can be data or text. It defines if setting is found directly in combobox text or rather in the userData.

import warnings
from enum import Enum

from PyQt5.QtWidgets import QLineEdit, QButtonGroup, QComboBox
from qgis.core import QgsProject, QgsCoordinateReferenceSystem, Qgis
from qgis.gui import QgsMapLayerComboBox, QgsFieldComboBox, QgsFileWidget, QgsProjectionSelectionWidget

from ..setting import Setting, Scope
from ..setting_widget import SettingWidget


class ComboMode(Enum):
    Text = 1
    Data = 2


class String(Setting):
    def __init__(self,
                 name,
                 scope: Scope,
                 default_value,
                 combo_mode: ComboMode=ComboMode.Data,
                 **kwargs):
        """

        :param name:
        :param scope:
        :param default_value:
        :param combo_mode: defines what is used to retrieve the setting in a combo box. Can be Data (default) or Text.
        :param enum: if given, the setting will be associated to the enum as given by the default value.
                     Can be QGIS for a QGIS enum. Enum must have been declared using Qt Q_ENUM macro.
                     Enum mode is available for global settings only.
        :param kwargs:
        """
        assert isinstance(combo_mode, ComboMode)
        self.combo_mode = combo_mode

        Setting.__init__(self, name, scope, default_value, object_type=str, ** kwargs)

    def check(self, value):
        if type(value) != str:
            self.info('{}:: Invalid value for setting {}: {}. It must be a string.'
                      .format(self.plugin_name, self.name, value),
                      Qgis.Warning)
            return False
        return True

    def config_widget(self, widget):
        if type(widget) == QLineEdit:
            return LineEditStringWidget(self, widget)
        elif type(widget) == QButtonGroup:
            return ButtonGroupStringWidget(self, widget)
        elif type(widget) == QComboBox:
            return ComboStringWidget(self, widget, self.combo_mode)
        elif type(widget) == QgsMapLayerComboBox:
            return MapLayerComboStringWidget(self, widget)
        elif type(widget) == QgsFieldComboBox:
            return FieldComboStringWidget(self, widget)
        elif type(widget) == QgsFileWidget:
            return FileStringWidget(self, widget)
        elif type(widget) == QgsProjectionSelectionWidget:
            return ProjectionStringWidget(self, widget)
        else:
            raise NameError("SettingManager does not handle %s widgets for strings at the moment (setting: %s)" %
                (type(widget), self.name))


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
    def __init__(self, setting, widget, mode: ComboMode=ComboMode.Data):
        self.mode = mode
        signal = widget.currentIndexChanged
        SettingWidget.__init__(self, setting, widget, signal)

    def set_widget_value(self, value):
        if self.mode is ComboMode.Text:
            self.widget.setCurrentIndex(self.widget.findText(value))
        else:
            self.widget.setCurrentIndex(self.widget.findData(value))

    def widget_value(self):
        if self.mode is ComboMode.Text:
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

#    def widget_test(self, value):
#        print('cannot test auto update of projection selection at the moment (QGIS 3.0 broken)')
#        return False
