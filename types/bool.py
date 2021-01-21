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

from PyQt5.QtWidgets import QCheckBox, QGroupBox
from qgis.core import QgsProject, Qgis
from qgis.gui import QgsCollapsibleGroupBox
from ..setting import Setting
from ..setting_widget import SettingWidget
from ..widgets import CheckBoxBoolWidget, GroupBoxBoolWidget, CheckableBoolWidget


class Bool(Setting):

    def __init__(self, name, scope, default_value, **kwargs):
        Setting.__init__(self, name, scope, default_value,
                         object_type=bool,
                         project_read=lambda plugin, key, def_val: QgsProject.instance().readBoolEntry(plugin, key, def_val)[0],
                         project_write=lambda plugin, key, val: QgsProject.instance().writeEntryBool(plugin, key, val),
                         **kwargs)

    def check(self, value):
        if type(value) != type(True):
            self.info('{}:: Invalid value for setting {}: {}. It must be a boolean.'
                      .format(self.plugin_name, self.name, value),
                      Qgis.Warning)
            return False
        return True

    @staticmethod
    def supported_widgets():
        return {
            QCheckBox: CheckBoxBoolWidget,
            QGroupBox: GroupBoxBoolWidget,
            QgsCollapsibleGroupBox: GroupBoxBoolWidget
        }

    def fallback_widget(self, widget) -> SettingWidget:
        if hasattr(widget, "isCheckable") and widget.isCheckable():
            return CheckableBoolWidget(self, widget)
        return None


