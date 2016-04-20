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


from types import *
from scope import Scope

# to print debug info
Debug = False


class SettingManager:
    def __init__(self, plugin_name):
        self.plugin_name = plugin_name
        self.settings = []

    def add_setting(self, setting):
        setting.set_plugin_name(self.plugin_name)
        self.settings.append(setting)

    def setting(self, name):
        for s in self.settings:
            if s.name == name:
                return s
        return None

    def value(self, setting_name):
        setting = self.setting(setting_name)
        if setting is None:
            raise NameError('%s has no setting %s' % (self.plugin_name, setting_name))
        return setting.value()

    def set_value(self, setting_name, value):
        setting = self.setting(setting_name)
        if setting is None:
            raise NameError('%s has no setting %s' % (self.plugin_name, setting_name))
        setting.set_value(value)

    ##########################################
    #                                        #
    ##########################################
    # deprecated
    def addSetting(self, name, setting_type, tscope, default_value, options={}):
        print("qgissettingmanager:: calling addSetting with these chain of argument is deprecated."
              " Consider using add_setting.")
        if self.setting(name) is not None:
            raise NameError("%s already exist in settings." % name)
        if setting_type.lower() not in ("string", "double", "integer", "bool", "color", "stringlist"):
            raise NameError("Wrong type %s" % setting_type)
        if tscope.lower() == "global":
            scope = Scope.Global
        elif tscope.lower() == "project":
            scope = Scope.Project
        else:
            raise NameError("%s is not a valid scope. Must be project or global." % tscope)
        SettingClass = globals()[setting_type[0].upper() + setting_type[1:].lower()]
        setting = SettingClass(name, scope, default_value, options)
        setting.set_plugin_name(self.plugin_name)
        self.settings.append(setting)

    # deprecated
    def setValue(self, setting_name, value):
        print("qgissettingmanager:: calling setValue is deprecated. Consider using set_value.")
        return self.set_value(setting_name, value)






