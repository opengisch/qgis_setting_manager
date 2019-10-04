# -----------------------------------------------------------
#
# QGIS Setting Manager
# Copyright (C) 2016 Denis Rouzaud
#
# -----------------------------------------------------------
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
# ---------------------------------------------------------------------

from qgis.PyQt.QtGui import QColor
from qgis.PyQt.QtWidgets import QDoubleSpinBox, QComboBox, QListWidget, QTableWidgetItem, QTableWidget, QButtonGroup
from qgis.core import QgsTolerance
from qgis.gui import QgsCollapsibleGroupBox, QgsScaleWidget, QgsMapLayerComboBox, QgsFieldComboBox, QgsAuthConfigSelect

from .. import Bool, Color, Double, Integer, String, Stringlist, Enum, Dictionary, SettingManager, Scope

pluginName = "qgis_setting_manager_testing"


class MySettings(SettingManager):
    def __init__(self):
        SettingManager.__init__(self, pluginName)

        self.testing_settings = {}

        # bool
        bool_collapse_init = lambda widget: widget.setCheckable(True)
        self.add_testing_setting(
            Bool, 'bool', True, False, init_widget={QgsCollapsibleGroupBox: bool_collapse_init})

        # color
        self.add_testing_setting(
            Color, 'color_alpha', QColor(100, 100, 100, 100), QColor(30, 30, 30, 30), allow_alpha=True
        )
        self.add_testing_setting(
            Color, 'color_no_alpha', QColor(100, 100, 100), QColor(30, 30, 30),
            allow_alpha=False, bad_values=[QColor(30, 30, 30, 30)]
        )

        # double
        double_spin_init = lambda widget: widget.setDecimals(5)
        self.add_testing_setting(
            Double, 'double', 1.12345, 2.87654,
            init_widget={QDoubleSpinBox: double_spin_init}, skip_widgets=[QgsScaleWidget]
        )
        self.add_testing_setting(Double, 'double_scale', 1000, 2000, only_widgets=[QgsScaleWidget])

        # integer
        integer_combo_init = lambda widget: widget.addItems(['1', '2', '3'])
        self.add_testing_setting(Integer, 'integer', 1, 2, init_widget={QComboBox: integer_combo_init})

        # string
        string_crs_init = lambda widget: (widget.addItem('CH1903+', 'EPSG:2056'), widget.addItem('CH1903', 'EPSG:21781'))
        self.add_testing_setting(
            String, 'string', 'EPSG:2056', 'EPSG:21781', init_widget={QComboBox: string_crs_init},
            skip_widgets=[QgsMapLayerComboBox, QgsFieldComboBox, QgsAuthConfigSelect, QButtonGroup]
        )

        # string list
        stringlist_list_init = lambda widget: widget.addItems(['abc', 'def', 'ghi', 'random', 'qwe', 'rtz', 'uio'])
        self.add_testing_setting(
            Stringlist, 'stringlist', ['abc', 'def', 'ghi'], ['qwe', 'rtz', 'uio'],
            init_widget={QListWidget: stringlist_list_init}, skip_widgets=[QTableWidget, QButtonGroup]
        )
        stringlist_table_init = lambda widget: (
            widget.setRowCount(3),
            widget.setColumnCount(2),
            widget.setItem(0, 0, QTableWidgetItem('first row, first col')),
            widget.setItem(0, 1, QTableWidgetItem('first row, second col')),
            widget.setItem(1, 0, QTableWidgetItem('second row, first col')),
            widget.setItem(1, 1, QTableWidgetItem('second row, second col')),
            widget.setItem(2, 0, QTableWidgetItem('third row, first col')),
            widget.setItem(2, 1, QTableWidgetItem('third row, second col')),
        )
        self.add_testing_setting(
            Stringlist, 'stringlist_table', ['first row, first col', 'second row, first col'], ['third row, first col'],
            init_widget={QTableWidget: stringlist_table_init}, only_widgets=[QTableWidget]
        )

        # enum
        enum_combo_init = lambda widget: (widget.addItem('LayerUnits', QgsTolerance.LayerUnits),
                                          widget.addItem('Pixels', QgsTolerance.Pixels))
        self.add_testing_setting(
            Enum, 'enum', QgsTolerance.Pixels, QgsTolerance.LayerUnits, scopes=[Scope.Global],
            init_widget={QComboBox: enum_combo_init}
        )

        # dictionary
        self.add_testing_setting(
            Dictionary, 'dictionary', {'my_key_1': 1, 'my_key_2': 2}, {'my_key_1': 1, 'my_key_2': 2}
        )

    def add_testing_setting(self, _type, name, default_value, new_value,
                            bad_values: list = [],
                            scopes=(Scope.Project, Scope.Global),
                            init_widget={},
                            skip_widgets=[],
                            only_widgets=[],
                            **kwargs):
        for _scope in scopes:
            setting_name = '{}_{}'.format(name, _scope)
            setting = _type(setting_name, _scope, default_value, **kwargs)
            self.add_setting(setting)
            self.testing_settings[setting_name] = {}
            self.testing_settings[setting_name]['new_value'] = new_value
            self.testing_settings[setting_name]['bad_values'] = bad_values
            self.testing_settings[setting_name]['init_widget'] = init_widget
            if only_widgets:
                self.testing_settings[setting_name]['widgets'] = only_widgets
            else:
                self.testing_settings[setting_name]['widgets'] = [w for w in setting.supported_widgets().keys() if w not in skip_widgets]

