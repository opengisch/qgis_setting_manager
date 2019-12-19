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

import json

from qgis.core import Qgis

from ..setting import Setting


class Dictionary(Setting):
    def __init__(self, name, scope, default_value, **kwargs):
        Setting.__init__(
            self, name, scope, default_value,
            object_type=dict,
            **kwargs)

    def read_out(self, value, scope):
        # always cast to dict
        if value is None:
            value = {}
        return json.loads(value)

    def write_in(self, value, scope):
        # always cast to list
        if value is None:
            value = {}
        return json.dumps(value)

    def check(self, value):
        if value is not None and type(value) is not dict:
            self.info('{}:: Invalid value for setting {}: {}. It must be a dictionary.'
                      .format(self.plugin_name, self.name, value),
                      Qgis.Warning)
            return False
        return True

    @staticmethod
    def supported_widgets():
        return {}
