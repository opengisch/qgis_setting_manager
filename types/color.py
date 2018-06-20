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
# dialog_title: show in color dialog
# allow_alpha: use or not alpha channel

import warnings

from PyQt5.QtGui import QColor
from qgis.core import QgsProject, Qgis
from qgis.gui import QgsColorButton

from ..setting import Setting
from ..setting_widget import SettingWidget


class Color(Setting):

    def __init__(self, name, scope, default_value, allow_alpha: bool = False, dialog_tilte: str = False, **kwargs):
        Setting.__init__(self, name, scope, default_value, None,
                         QgsProject.instance().readListEntry, QgsProject.instance().writeEntry, **kwargs)
        # compatibility (TODO: remove in next major release)
        if type(allow_alpha) is dict:
            self.allow_alpha = False
            self.dialog_title = None
            warnings.warn('You are using the old API with dictionary based options.'
                          ' Switch to named arguments instead.', DeprecationWarning)
            if 'dialogTitle' in allow_alpha:
                self.dialog_title = allow_alpha['dialogTitle']
            if 'allowAlpha' in allow_alpha:
                self.allow_alpha = allow_alpha['allowAlpha']
        else:
            self.allow_alpha = allow_alpha
            self.dialog_title = dialog_tilte

    def read_out(self, value, scope):
        if type(value) not in (list, tuple) or len(value) not in (3, 4):
            # do not raise error if setting type is not correct, return default value
            return self.default_value
        else:
            r = int(value[0])
            g = int(value[1])
            b = int(value[2])
            a = int(value[3]) if len(value) > 3 and self.allow_alpha else 255
            return QColor(r, g, b, a)

    def write_in(self, value, scope):
        if self.allow_alpha:
            return ["%u" % value.red(), "%u" % value.green(), "%u" % value.blue(), "%u" % value.alpha()]
        else:
            return ["%u" % value.red(), "%u" % value.green(), "%u" % value.blue()]

    def check(self, value: QColor):
        if type(value) != QColor:
            self.info('{}:: Invalid value for setting {}: {}. It must be a QColor.'
                      .format(self.plugin_name, self.name, value),
                      Qgis.Warning)
            return False
        return True

    def config_widget(self, widget):
        if type(widget) == QgsColorButton:
            return QgisColorWidget(self, widget, allow_alpha=self.allow_alpha)
        else:
            return StandardColorWidget(self, widget, allow_alpha=self.allow_alpha, dialog_title=self.dialog_title)


class QgisColorWidget(SettingWidget):
    def __init__(self, setting, widget, allow_alpha: bool = False):
        signal = widget.colorChanged
        SettingWidget.__init__(self, setting, widget, signal)
        self.widget.setAllowOpacity(allow_alpha)

    def set_widget_value(self, value):
        self.widget.setColor(value)

    def widget_value(self):
        return self.widget.color()


class StandardColorWidget(SettingWidget):
    def __init__(self, setting, widget, allow_alpha: bool = False, dialog_title: str = None):
        color_widget = QgsColorButton(widget, dialog_title)
        signal = color_widget.colorChanged

        SettingWidget.__init__(self, setting, color_widget, signal)
        self.widget.setAllowOpacity(allow_alpha)

    def set_widget_value(self, value):
        self.widget.setColor(value)

    def widget_value(self):
        return self.widget.color()
