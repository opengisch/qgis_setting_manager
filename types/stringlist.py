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

from qgis.PyQt.QtWidgets import QListWidget, QTableWidget, QButtonGroup
from qgis.core import QgsProject, Qgis, QgsSettings

from ..setting import Setting
from ..widgets import ListStringListWidget, TableWidgetStringListWidget, ButtonGroupStringListWidget


class Stringlist(Setting):
    def __init__(self, name, scope, default_value, **kwargs):
        Setting.__init__(self, name, scope, default_value,
                         object_type=None,
                         qsettings_read=lambda key, def_val: QgsSettings().value(key, def_val),
                         qsettings_write=lambda key, val: QgsSettings().setValue(key, val),
                         project_read=lambda plugin, key, def_val: QgsProject.instance().readListEntry(plugin, key, def_val)[0],
                         **kwargs)

    def read_out(self, value, scope):
        # always cast to list
        if value is not None:
            value = list(value)
        else:
            value = []
        return value

    def write_in(self, value, scope):
        # always cast to list
        if value is not None:
            value = list(value)
        return value

    def check(self, value):
        if value is not None and type(value) not in (list, tuple):
            self.info('{}:: Invalid value for setting {}: {}. It must be a string list.'
                      .format(self.plugin_name, self.name, value),
                      Qgis.Warning)
            return False
        return True

    @staticmethod
    def supported_widgets():
        return {
            QListWidget: ListStringListWidget,
            QTableWidget: TableWidgetStringListWidget,
            QButtonGroup: ButtonGroupStringListWidget,
        }







