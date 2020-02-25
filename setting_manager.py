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


# to print debug info
Debug = False


class SettingManager:
    def __init__(self, plugin_name, save_under_plugins: bool = True):
        """
        :param plugin_name: the plugin name
        :param save_under_plugins: determines if global settings are grouped under "plugins" or at the top level
        """
        self.plugin_name = plugin_name
        self.save_under_plugins = save_under_plugins
        self.__settings = {}

    def add_setting(self, setting):
        if setting.name in self.__settings:
            raise NameError("{} already exist in settings.".format(setting.name))
        setting.set_plugin_name(self.plugin_name)
        setting.save_under_plugins = self.save_under_plugins
        self.__settings[setting.name] = setting

    def value(self, setting_name):
        if setting_name not in self.__settings:
            raise NameError('%s has no setting %s' % (self.plugin_name, setting_name))
        return self.__settings[setting_name].value()

    def set_value(self, setting_name, value):
        if setting_name not in self.__settings:
            raise NameError('%s has no setting %s' % (self.plugin_name, setting_name))
        self.__settings[setting_name].set_value(value)

    def remove(self, setting_name):
        if setting_name not in self.__settings:
            raise NameError('{} has no setting {}'.format(self.plugin_name, setting_name))
        self.__settings[setting_name].reset_default()
        del self.__settings[setting_name]

    def settings_list(self):
        return list(self.__settings.keys())

    def setting(self, name):
        if name not in self.__settings:
            raise NameError('{} setting does not exist'.format(name))
        return self.__settings[name]
