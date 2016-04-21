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

from scope import Scope


class Setting(QObject):
    valueChanged = pyqtSignal()

    def __init__(self, name, scope, default_value, object_type, project_read_method, options={}):
        QObject.__init__(self)

        # TODO pyton3 check based on enum
        if scope not in (Scope.Global, Scope.Project):
            raise NameError('Scope of setting {} is not valid: {}'.format(name, scope))
        self.check(default_value)

        # these will determined when set_plugin_name is called
        self.plugin_name = None

        self.name = name
        self.scope = scope
        self.default_value = default_value
        self.widget = None
        self.object_type = object_type
        self.options = options
        self.project_read_method = project_read_method

    def read_out(self, value, scope):
        """
        This method shall be overriden in type subclasses
        to transform the output being read from project/global
        to the desired setting format (such as color for instance)
        """
        return value

    def write_in(self, value, scope):
        """
        This method shall be overriden in type subclasses
        to transform the desired setting format (such as color for instance)
        to the input to project/global settings
        """
        return value

    def check(self, value):
        """
        This method shall be overriden in type subclasses
        to check the validity of the value
        the implementation should raise errors
        """
        return True

    def set_plugin_name(self, plugin_name):
        self.plugin_name = plugin_name

    def global_name(self):
        return 'plugins/{}/{}'.format(self.plugin_name, self.name)

    def set_value(self, value):
        self.check(value)
        value = self.write_in(value, self.scope)
        if self.scope == Scope.Global:
            QSettings().setValue(self.global_name(), value)
        elif self.scope == Scope.Project:
            QgsProject.instance().writeEntry(self.plugin_name, self.name, value)
        self.valueChanged.emit()

    def value(self):
        if self.scope == Scope.Global:
            value = QSettings().value(self.global_name(),
                                      self.write_in(self.default_value, self.scope),
                                      type=self.object_type)
            # TODO python3: remove backward compatibility
            # try to gather old setting value (using old version of QGIS Setting Manager)
            if self.read_out(value, self.scope) == self.default_value:
                value = QSettings(self.plugin_name, self.plugin_name).value(self.name,
                                                                            self.write_in(self.default_value, self.scope),
                                                                            type=self.object_type)
                if self.read_out(value, self.scope) != self.default_value:
                    # rewrite the setting in new system
                    QSettings().setValue(self.global_name(), value)
        elif self.scope == Scope.Project:
            value = self.project_read_method(self.plugin_name, self.name, self.write_in(self.default_value, self.scope))[0]

        return self.read_out(value, self.scope)

    def remove(self):
        if self.scope == Scope.Project:
            QgsProject.instance().removeEntry(self.plugin_name, self.name)
        else:
            QSettings().remove(self.global_name())

    def set_value_on_widget_update_signal(self):
        if self.widget is None:
            return
        eval("self.widget.%s.connect(self.set_value_from_widget)" % self.signal)

    def set_widget_from_value(self):
        if self.widget is None:
            return
        setting_value = self.value()
        self.widgetSetMethod(setting_value)

    def set_value_from_widget(self, dummy=None):
        if self.widget is None:
            return
        widget_value = self.widgetGetMethod()
        self.set_value(widget_value)
