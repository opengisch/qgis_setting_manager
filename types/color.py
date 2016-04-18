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
# dialogTitle: show in color dialog
# alpha: use or not alpha channel

from PyQt4.QtCore import QSettings
from PyQt4.QtGui import QColor, QColorDialog
from qgis.core import QgsProject
from qgis.gui import QgsColorButton, QgsColorButtonV2

from ..setting import Setting


class Color(Setting):

    def __init__(self, pluginName, name, scope, defaultValue, options={}):

        setGlobal = lambda(value): QSettings().setValue(pluginName + "/" + name, [value.red(),
                                                                                     value.green(),
                                                                                     value.blue(),
                                                                                     value.alpha()])
        setProject = lambda(value): QgsProject.instance().writeEntry(pluginName, name,
                                                                     ["%u" % value.red(),
                                                                      "%u" % value.green(),
                                                                      "%u" % value.blue(),
                                                                      "%u" % value.alpha()])
        getGlobal = lambda: self.list2color(QSettings().value(pluginName + "/" + name, defaultValue))
        getProject = lambda: self.list2color(QgsProject.instance().readListEntry(pluginName, name, defaultValue))

        if scope == 'global':
            v = QSettings().value(pluginName + "/" + name)
            if v is None:
                QSettings().setValue(pluginName + "/" + name, defaultValue)

        Setting.__init__(self, pluginName, name, scope, defaultValue, options,
                         setGlobal, setProject, getGlobal, getProject)

    def check(self, color):
        if type(color) != QColor:
            raise NameError("Color setting %s must be a QColor." % self.name)

    def setWidget(self, widget):
        if type(widget) in ( QgsColorButton, QgsColorButtonV2 ):
            self.widget = widget
        else:
            txt = self.options.get("dialogTitle", "")
            self.widget = QgsColorButtonV2(widget, txt)
        if type(widget) == QgsColorButton:
            self.widget.setColorDialogOptions(QColorDialog.ShowAlphaChannel)
        else:
            self.widget.setAllowAlpha(self.options.get("allowAlpha", False))
        self.signal = "colorChanged"
        self.widgetSetMethod = self.widget.setColor
        self.widgetGetMethod = self.widget.color

    def list2color(self, color):
        if type(color) != list or len(color) not in (3,4):
            return self.defaultValue
        else:
            r = int(color[0])
            g = int(color[1])
            b = int(color[2])
            a = int(color[3]) if len(color)>3 and self.options.get("allowAlpha", False) else 255
        return QColor(r, g, b, a)
