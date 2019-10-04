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


# for combobox, the value corresponds to the index of the combobox

from PyQt5.QtWidgets import QLineEdit, QSpinBox, QSlider, QComboBox
from qgis.core import QgsProject, Qgis

from ..setting import Setting
from ..widgets import LineEditIntegerWidget, SpinBoxIntegerWidget, ComboBoxIntegerWidget


class Integer(Setting):
    def __init__(self, name, scope, default_value, **kwargs):
        Setting.__init__(self, name, scope, default_value,
                         object_type=int,
                         project_read=lambda plugin, key, def_val: QgsProject.instance().readNumEntry(plugin, key, def_val)[0],
                         **kwargs)

    def check(self, value):
        if type(value) != int and type(value) != float:
            self.info('{}:: Invalid value for setting {}: {}. It must be an integer.'
                      .format(self.plugin_name, self.name, value),
                      Qgis.Warning)
            return False
        return True

    @staticmethod
    def supported_widgets():
        return {
            QLineEdit: LineEditIntegerWidget,
            QSpinBox: SpinBoxIntegerWidget,
            QSlider: SpinBoxIntegerWidget,
            QComboBox: ComboBoxIntegerWidget
        }


