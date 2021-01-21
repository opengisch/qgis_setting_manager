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

import abc

from PyQt5.QtCore import QObject, pyqtSignal, QSettings
from qgis.core import QgsProject, QgsMessageLog, Qgis, QgsSettings
from enum import Enum


class Scope(Enum):
    Project = 1
    Global = 2


class Setting():
    def __init__(self, name: str, scope: Scope, default_value,
                 object_type=None,
                 project_read=lambda plugin, key, def_val: QgsProject.instance().readEntry(plugin, key, def_val)[0],
                 project_write=lambda plugin, key, val: QgsProject.instance().writeEntry(plugin, key, val),
                 qsettings_read=lambda key, def_val, object_type: QgsSettings().value(key, def_val, type=object_type),
                 qsettings_write=lambda key, val: QgsSettings().setValue(key, val),
                 allowed_values: list = None):
        """

        :param name:
        :param scope:
        :param default_value:
        :param object_type:
        :param project_read:
        :param project_write:
        :param allowed_values: optional list to limit the allowed values for the setting.
        """

        if not isinstance(scope, Scope):
            raise NameError('Scope of setting {} is not valid: {}'.format(name, scope))

        # these will determined when set_plugin_name is called
        self.plugin_name = None

        self._save_under_plugins = True

        self.name = name
        self.scope = scope
        self.default_value = default_value
        self.object_type = object_type
        self.project_read = project_read
        self.project_write = project_write
        self.qsettings_read = qsettings_read
        self.qsettings_write = qsettings_write
        self.allowed_values = allowed_values

        if not self.check(default_value):
            raise NameError('Default value of setting {} is not valid: {}'.format(name, default_value))

    def read_out(self, value, scope):
        """
        This method shall be reimplemented in type subclasses
        to transform the output being read from project/global
        to the desired setting format (such as color for instance)
        """
        return value

    def write_in(self, value, scope):
        """
        This method shall be reimplemented in type subclasses
        to transform the desired setting format (such as color for instance)
        to the input to project/global settings
        """
        return value

    def check(self, value):
        """
        This method shall be reimplemented in type subclasses
        to check the validity of the value
        the implementation should raise errors
        """
        return True

    @staticmethod
    def supported_widgets() -> dict:
        """
        This method shall be reimplemented in type subclasses
        :return: a dictionary of widget_class => setting_widget_class
        """
        pass

    @staticmethod
    def fallback_widget(widget):
        """
        Optional virtual method to
        :param widget: the input widget
        :return: a SettingWidget implementation
        """
        return None

    def config_widget(self, widget):
        """
        Returns the SettingWidget implementation for a given widget
        :raise NameError if the widget is not supported
        """
        for widget_type, setting_widget_class in self.supported_widgets().items():
            if isinstance(widget, widget_type):
                return setting_widget_class(self, widget)
        raise NameError("SettingManager does not handle {w} widgets for {t} at the moment (setting: {s})".format(
            w=type(widget), t=type(self).__name__, s=self.name)
        )

    def _check(self, value) -> bool:
        """
        Private checking method: will trigger the sub-classed check and perform global checks
        :param value: the value to be checked
        :return: True if the value is correct
        """
        if not self.check(value):
            return False
        if self.allowed_values and value not in self.allowed_values:
            self.info('{}:: Invalid value for setting {}: {}. It should be within the list of values: {}.'
                      .format(self.plugin_name, self.name, value, self.allowed_values),
                      Qgis.Warning)
            return False
        return True

    def set_plugin_name(self, plugin_name):
        self.plugin_name = plugin_name

    @property
    def save_under_plugins(self):
        return self._save_under_plugins

    @save_under_plugins.setter
    def save_under_plugins(self, value: bool):
        self._save_under_plugins = value

    def global_name(self):
        if self.save_under_plugins:
            return 'plugins/{}/{}'.format(self.plugin_name, self.name)
        else:
            return '{}/{}'.format(self.plugin_name, self.name)

    def set_value(self, value) -> bool:
        """
        Sets the value for the setting
        :return: True if the setting was written
        """
        # checking should be made before write_in
        if not self._check(value):
            return False
        value = self.write_in(value, self.scope)
        if self.scope == Scope.Global:
            self.qsettings_write(self.global_name(), value)
        elif self.scope == Scope.Project:
            self.project_write(self.plugin_name, self.name, value)
        return True

    def value(self):
        if self.scope == Scope.Global:
            if self.object_type is not None:
                value = self.qsettings_read(self.global_name(), self.write_in(self.default_value, self.scope), object_type=self.object_type)
            else:
                value = self.qsettings_read(self.global_name(), self.write_in(self.default_value, self.scope))
        elif self.scope is Scope.Project:
            value = self.project_read(self.plugin_name, self.name, self.write_in(self.default_value, self.scope))
        value = self.read_out(value, self.scope)
        # checking should be made after read_out
        if not self._check(value):
            return self.default_value
        else:
            return value

    def reset_default(self):
        if self.scope is Scope.Project:
            QgsProject.instance().removeEntry(self.plugin_name, self.name)
        else:
            QSettings().remove(self.global_name())

    def info(self, msg="", level=Qgis.Info):
        QgsMessageLog.logMessage('{} {}'.format(self.__class__.__name__, msg), 'QgsSettingManager', level)
