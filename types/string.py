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
# comboMode: can be data or text. It defines if setting is found directly in combobox text or rather in the userData.

from PyQt4.QtGui import QLineEdit, QButtonGroup, QComboBox
from qgis.core import QgsProject, QgsMapLayerRegistry
from qgis.gui import QgsMapLayerComboBox, QgsFieldComboBox

from ..setting import Setting


class String(Setting):

    def __init__(self, name, scope, default_value, options={}):
        Setting.__init__(self, name, scope, default_value, str, QgsProject.instance().readEntry, QgsProject.instance().writeEntry, options)

    def check(self, value):
        if type(value) != str and type(value) != unicode:
            print(type(value))
            raise NameError('{}:: Invalid value for setting {}: {}. It must be a string.'.format(self.plugin_name, self.name, value))

    def set_widget(self, widget):
        if type(widget) == QLineEdit:
            self.widget_signal = "textChanged"
            self.widget_set_method = widget.setText
            self.widget_get_method = widget.text
        elif type(widget) == QButtonGroup:
            self.widget_signal = "buttonClicked"
            self.widget_set_method = self.setButtonGroup
            self.widget_get_method = self.getButtonGroup
        elif type(widget) == QComboBox:
            self.widget_signal = "activated"
            combo_mode = self.options.get("comboMode", "data")
            if combo_mode == 'data':
                self.widget_set_method = lambda(value): self.widget.setCurrentIndex(widget.findData(value))
                self.widget_get_method = lambda: widget.itemData(widget.currentIndex()) or ""
            elif combo_mode == 'text':
                self.widget_set_method = lambda(value): self.widget.setCurrentIndex(widget.findText(value))
                self.widget_get_method = widget.currentText
        elif type(widget) in QgsMapLayerComboBox:
            self.widget_signal = "layerChanged"
            self.widget_set_method = lambda(value): self.widget.setLayer(QgsMapLayerRegistry.instance().mapLayer(value))
            self.widget_get_method = lambda: widget.currentLayer().id()
        else:
            raise NameError("SettingManager does not handle %s widgets for strings at the moment (setting: %s)" %
                            (type(widget), self.name))
        self._widget = widget

    def setButtonGroup(self, value):
        # for checkboxes
        if self.widget is None:
            return
        for button in self.widget.buttons():
            if value == button.objectName():
                button.setChecked(True)
                break

    def getButtonGroup(self):
        if self.widget is None:
            return
        value = ""
        for button in self.widget.buttons():
            if button.isChecked():
                value = button.objectName()
                break
        return value
