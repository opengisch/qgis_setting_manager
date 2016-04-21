#-----------------------------------------------------------
#
# QGIS Quick Finder Plugin
# Copyright (C) 2014 Denis Rouzaud, Arnaud Morvan
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
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
#---------------------------------------------------------------------

from PyQt4.QtGui import QColor

from .. import *


pluginName = "test_plugin"


class MySettings(SettingManager):
    def __init__(self):
        SettingManager.__init__(self, pluginName)

        settings_root = {'bool': {'class': Bool, 'default': True, 'options': {}},
                         'color': {'class': Color, 'default': QColor(100, 100, 100, 100), 'options': {'allowAlpha': True}},
                         'double': {'class': Double, 'default': 0.123456789, 'options': {}},
                         'integer': {'class': Integer, 'default': 1, 'options': {}},
                         'string_list': {'class': Stringlist, 'default': ('abc', 'def', 'ghi'), 'options': {}},
                         'string': {'class': String, 'default': 'default_string', 'options': {}}}

        self.settings = {}
        scopes = {'project': Scope.Project, 'global': Scope.Global}
        for s_name, setting_ in settings_root.iteritems():
            for scope_str, scope_val in scopes.iteritems():
                # TODO python 3 use enum
                setting_name = '{}_{}'.format(s_name, scope_str)
                self.settings[setting_name] = setting_
                self.add_setting(setting_['class'](setting_name, scope_val, setting_['default']))



