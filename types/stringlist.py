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


from PyQt4.QtCore import Qt
from PyQt4.QtGui import QListWidget, QButtonGroup
from qgis.core import QgsProject

from ..setting import Setting


class Stringlist(Setting):

    def __init__(self, name, scope, default_value, options={}):
        Setting.__init__(self, name, scope, default_value, None, QgsProject.instance().readListEntry, QgsProject.instance().writeEntry, options)

    def read_out(self, value, scope):
        # always cast to list
        return list(value)

    def write_in(self, value, scope):
        # always cast to list
        return list(value)

    def check(self, value):
        if type(value) not in (list, tuple):
            raise NameError("Setting %s must be a string list." % self.name)

    def set_widget(self, widget):
        if type(widget) == QListWidget:
            self.widget_signal = "clicked"
            self.widget_set_method = self.setListBoxes
            self.widget_get_method = self.getListBoxes
        elif type(widget) == QButtonGroup:
            self.widget_signal = "buttonClicked"
            self.widget_set_method = self.setGroupBoxes
            self.widget_get_method = self.getGroupBoxes
        else:
            raise NameError("SettingManager does not handle %s widgets for integers for the moment (setting: %s)" %
                            (type(widget), self.name))
        self._widget = widget

    def setListBoxes(self, value):
        if self.widget is None:
            return
        for i in range(self.widget.count()):
            item = self.widget.item(i)
            if item.text() in value:
                item.setCheckState(Qt.Checked)
            else:
                item.setCheckState(Qt.Unchecked)

    def getListBoxes(self):
        if self.widget is None:
            return
        value = []
        for i in range(self.widget.count()):
            item = self.widget.item(i)
            if item.checkState() == Qt.Checked:
                value.append(item.text())
        return value

    def setGroupBoxes(self, value):
        if self.widget is None:
            return
        for item in self.widget.buttons():
            item.setChecked(item.objectName() in value)

    def getGroupBoxes(self):
        if self.widget is None:
            return
        value = []
        for item in self.widget.buttons():
            if item.isChecked():
                value.append(item.objectName())
        return value

