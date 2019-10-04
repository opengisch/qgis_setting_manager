#-----------------------------------------------------------
#
# QGIS Setting Manager
# Copyright (C) 2016 Denis Rouzaud
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

from qgis.PyQt.QtGui import QColor
from qgis.PyQt.QtWidgets import QDoubleSpinBox, QComboBox
from qgis.core import QgsTolerance
from qgis.gui import QgsCollapsibleGroupBox, QgsProjectionSelectionWidget

from .. import Bool, Color, Double, Integer, String, Stringlist, Enum, Dictionary, SettingManager, Scope

pluginName = "qgis_setting_manager_testing"


class MySettings(SettingManager):
    def __init__(self):
        SettingManager.__init__(self, pluginName)
        
        self.bad_values = {}
        self.new_values = {}
        self.init_widget = {}

        bool_collapse_init = lambda widget: widget.setCheckable(True)
        self.add_testing_setting(Bool, 'bool', True, False, init_widget={QgsCollapsibleGroupBox: bool_collapse_init})
        self.add_testing_setting(Color, 'color_alpha', QColor(100, 100, 100, 100), QColor(30, 30, 30, 30), allow_alpha=True)
        self.add_testing_setting(Color, 'color_no_alpha', QColor(100, 100, 100), QColor(30, 30, 30), allow_alpha=False, bad_values=[QColor(30, 30, 30, 30)])
        double_spin_init = lambda widget: widget.setDecimals(5)
        self.add_testing_setting(Double, 'double', 0.12345, 9.87654, init_widget={QDoubleSpinBox: double_spin_init})
        integer_combo_init = lambda widget: widget.addItems(['1', '2', '3'])
        self.add_testing_setting(Integer, 'integer', 1, 2, init_widget={QComboBox: integer_combo_init})
        string_crs_init = lambda widget: widget.addItems(['EPSG:2056', 'EPSG:21781'])
        self.add_testing_setting(String, 'string', 'EPSG:2056', 'EPSG:21781', init_widget={QgsProjectionSelectionWidget: string_crs_init})
        self.add_testing_setting(Stringlist, 'stringlist', ['abc', 'def', 'ghi'], ['qwe', 'rtz', 'uio'])
        self.add_testing_setting(Enum, 'enum', QgsTolerance.Pixels, QgsTolerance.LayerUnits, scopes=[Scope.Global])
        self.add_testing_setting(Dictionary, 'dictionary', {'my_key_1': 1, 'my_key_2': 2}, {'my_key_1': 1, 'my_key_2': 2})

    def add_testing_setting(self, _type, name, default_value, new_value,
                            bad_values: list = [],
                            scopes=(Scope.Project, Scope.Global),
                            init_widget={},
                            **kwargs):
        for _scope in scopes:
            setting_name = '{}_{}'.format(name, _scope)
            self.add_setting(_type(setting_name, _scope, default_value, **kwargs))
            self.new_values[setting_name] = new_value
            self.bad_values[setting_name] = bad_values
            self.init_widget[setting_name] = init_widget
            
 

"""
double:
QDoubleSpinBox:
init_widget:
- setDecimals(5)
QLineEdit:

integer:
QComboBox:
init_widget:
- addItem(str(1))
- addItem(str(2))
- addItem(str(3))

QListWidget:
init_widget:
- addItems(('abc', 'def', 'ghi', 'random', 'qwe', 'rtz', 'uio'))

"""



