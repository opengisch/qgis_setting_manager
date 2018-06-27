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
# ---------------------------------------------------------------------

from enum import Enum as PyEnum

from PyQt5.QtWidgets import QComboBox
from qgis.core import Qgis, QgsSettings, QgsMessageLog

from ..setting import Setting, Scope
from ..setting_widget import SettingWidget


class EnumMode(PyEnum):
    NoEnum = 1
    QGIS = 2
    Python = 3  # TODO: still to be implemented


class Enum(Setting):
    def __init__(self,
                 name,
                 scope: Scope,
                 default_value,
                 mode: EnumMode = EnumMode.QGIS,
                 **kwargs):
        """

        :param name: the name of the setting
        :param scope: at the moment only Global scope is supported for Enum
        :param default_value: the default value given as enum
        :param mode: if given, the setting will be associated to the enum as given by the default value.
                     Can be QGIS for a QGIS enum. Enum must have been declared using Qt Q_ENUM macro.
                     Enum mode is available for global settings only.
        :param kwargs:
        """

        assert scope is Scope.Global
        assert mode is EnumMode.QGIS

        self.mode = mode

        Setting.__init__(self, name, scope, default_value,
                         object_type=None,
                         qsettings_read=QgsSettings().enumValue,
                         qsettings_write=QgsSettings().setEnumValue,
                         **kwargs)

    def check(self, value):
        if self.mode is EnumMode.QGIS:
            if not isinstance(value, self.default_value.__class__):
                raise NameError('xxxx')
                self.info('{plugin}:: Invalid value for setting {name}: {value} ({vclass}). It must be a {type}.'
                          .format(plugin=self.plugin_name, name=self.name,
                                  value=value, vclass=value.__class__,
                                  type=self.default_value.__class__),
                          Qgis.Warning)
                return False
        return True

    def config_widget(self, widget):
        if type(widget) == QComboBox:
            return ComboEnumWidget(self, widget)
        else:
            raise NameError("SettingManager does not handle %s widgets for strings at the moment (setting: %s)" %
                            (type(widget), self.name))


class ComboEnumWidget(SettingWidget):
    def __init__(self, setting, widget):
        signal = widget.currentIndexChanged
        SettingWidget.__init__(self, setting, widget, signal)

    def set_widget_value(self, value):
        if self.DEBUG:
            msg = 'setting {} value {}'.format(self.setting.name, value)
            QgsMessageLog.logMessage('{}:: {}'.format(self.__class__.__name__, msg), 'Setting manager', Qgis.Info)
        self.widget.setCurrentIndex(self.widget.findData(value))

    def widget_value(self):
        value = self.widget.itemData(self.widget.currentIndex())
        if value is None:
            value = self.setting.default_value
        value = self.setting.default_value.__class__(value)
        return value



