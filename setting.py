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

from PyQt4.QtCore import QObject, pyqtSignal, QSettings
from qgis.core import QgsProject

class Setting(QObject):
    valueChanged = pyqtSignal()

    def __init__(self, pluginName, name, scope, defaultValue, options={}, objectType = None):
        QObject.__init__(self)
        self.pluginName = pluginName
        self.name = name
        self.scope = scope
        self.defaultValue = defaultValue
        self.widget = None
        self.objectType = objectType
        self.options = options

        self.projectReadMethod = QgsProject.instance().readEntry

        self.check(defaultValue)

        self.globalName = 'plugins/{}/{}'.format(self.pluginName, self.name)

    def readOut(self, value, scope):
        return value

    def writeIn(self, value, scope):
        return value

    def check(self, value):
        """
        This method shall be overriden in type subclasses
        to check the validity of the value
        """
        return True

    def setValue(self, value):
        if not self.check(value):
            return
        value = self.writeIn(value, self.scope)
        if self.scope == "global":
            QSettings().setValue(self.globalName, value)
        elif self.scope == "project":
            QgsProject.instance().writeEntry(self.pluginName, self.name, value)
        self.valueChanged.emit()

    def getValue(self):
        if self.scope == "global":
            value = QSettings().value(self.globalName, self.defaultValue, type=self.objectType)
            # try to gather old setting value (using old version of Qgis Setting Manager)
            if self.readOut(value, self.scope) == self.defaultValue:
                value = QSettings(self.pluginName, self.pluginName).value(self.name, self.defaultValue, type=self.objectType)
                if self.readOut(value, self.scope) != self.defaultValue:
                    # rewrite the setting in new system
                    QSettings().setValue(self.globalName, value)
        elif self.scope == "project":
            value = self.projectReadMethod(self.pluginName, self.name, self.defaultValue)[0]

        return self.readOut(value, self.scope)

    def setValueOnWidgetUpdateSignal(self):
        if self.widget is None:
            return
        eval("self.widget.%s.connect(self.setValueFromWidget)" % self.signal)

    def setWidgetFromValue(self):
        if self.widget is None:
            return
        settingValue = self.getValue()
        self.widgetSetMethod(settingValue)

    def setValueFromWidget(self, dummy=None):
        if self.widget is None:
            return
        widgetValue = self.widgetGetMethod()
        self.setValue(widgetValue)
