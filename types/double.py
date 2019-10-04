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

from PyQt5.QtWidgets import QLineEdit, QDoubleSpinBox
from qgis.core import QgsProject, Qgis
from qgis.gui import QgsScaleWidget

from ..setting import Setting
from ..widgets import LineEditDoubleWidget, DoubleQgsScaleWidget, DoubleSpinBoxDoubleWidget


class Double(Setting):

    def __init__(self, name, scope, default_value, **kwargs):
        Setting.__init__(self, name, scope, default_value,
                         object_type=float,
                         project_read=lambda plugin, key, def_val: QgsProject.instance().readDoubleEntry(plugin, key, def_val)[0],
                         project_write=lambda plugin, key, val: QgsProject.instance().writeEntryDouble(plugin, key, val),
                         **kwargs)

    def check(self, value):
        if type(value) != int and type(value) != float:
            self.info('{}:: Invalid value for setting {}: {}. It must be a floating number.'
                      .format(self.plugin_name, self.name, value),
                      Qgis.Warning)
            return False
        return True

    @staticmethod
    def supported_widgets():
        return {
            QgsScaleWidget: DoubleQgsScaleWidget,
            QLineEdit: LineEditDoubleWidget,
            QDoubleSpinBox: DoubleSpinBoxDoubleWidget
        }






