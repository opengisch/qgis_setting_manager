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

from PyQt5.QtCore import QObject, pyqtSignal, QSettings
from qgis.core import QgsProject, QgsMessageLog, Qgis
from enum import Enum


class Scope(Enum):
    Project = 1
    Global = 2


class Setting(QObject):
    valueChanged = pyqtSignal()

    def __init__(self, name, scope, default_value, object_type, project_read, project_write, options={}):
        QObject.__init__(self)

        if not isinstance(scope, Scope):
            raise NameError('Scope of setting {} is not valid: {}'.format(name, scope))
        if not self.check(default_value):
            raise NameError('Default value of setting {} is not valid: {}'.format(name, default_value))

        # these will determined when set_plugin_name is called
        self.plugin_name = None

        self.name = name
        self.scope = scope
        self.default_value = default_value
        self.object_type = object_type
        self.options = options
        self.project_read = project_read
        self.project_write = project_write

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

    def check(self, value) -> bool:
        """
        This method shall be reimplemented in type subclasses
        to check the validity of the value
        the implementation should raise errors
        """
        return True

    def config_widget(self, widget):
        """
        This method must be reimplemented in subclasses
        """
        return None

    def _check(self, value) -> bool:
        """
        Private checking method: will trigger the sub-classed check and perform global checks
        :param value: the value to be checked
        :return: True if the value is correct
        """
        if not self.check(value):
            return False
        if 'value_list' in self.options:
            if value not in self.options['value_list']:
                self.info('{}:: Invalid value for setting {}: {}. It should be within the list of values: {}.'
                          .format(self.plugin_name, self.name, value, self.options['value_list']),
                          Qgis.Warning)
                return False
        return True

    def set_plugin_name(self, plugin_name):
        self.plugin_name = plugin_name

    def global_name(self):
        return 'plugins/{}/{}'.format(self.plugin_name, self.name)

    def set_value(self, value):
        # checking should be made before write_in
        if not self._check(value):
            return
        value = self.write_in(value, self.scope)
        if self.scope == Scope.Global:
            QSettings().setValue(self.global_name(), value)
        elif self.scope == Scope.Project:
            self.project_write(self.plugin_name, self.name, value)
        self.valueChanged.emit()

    def value(self):
        if self.scope == Scope.Global:
            if self.object_type is not None:
                value = QSettings().value(self.global_name(), self.write_in(self.default_value, self.scope), type=self.object_type)
            else:
                value = QSettings().value(self.global_name(), self.write_in(self.default_value, self.scope))
        elif self.scope == Scope.Project:
            value = self.project_read(self.plugin_name, self.name, self.write_in(self.default_value, self.scope))[0]
        value = self.read_out(value, self.scope)
        # checking should be made after read_out
        if not self._check(value):
            return self.default_value
        else:
            return value

    def reset_default(self):
        if self.scope == Scope.Project:
            QgsProject.instance().removeEntry(self.plugin_name, self.name)
        else:
            QSettings().remove(self.global_name())

    def info(self, msg="", level=Qgis.Info):
        QgsMessageLog.logMessage('{} {}'.format(self.__class__.__name__, msg), 'QgsSettingManager', level)
