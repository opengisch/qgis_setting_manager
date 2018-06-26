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

import os
import yaml
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QCheckBox, QLabel, QPushButton, QDoubleSpinBox, QLineEdit, QSpinBox, QSlider, QComboBox, QListWidget
from qgis.gui import QgsCollapsibleGroupBox, QgsColorButton, QgsProjectionSelectionWidget

from .. import *

pluginName = "qgis_setting_manager_testing"


class MySettings(SettingManager):
    def __init__(self):
        SettingManager.__init__(self, pluginName)

        cur_dir = os.path.dirname(__file__)
        definition_file = os.path.join(cur_dir, 'setting_config.yaml')
        with open(definition_file, 'r') as f:
            definition = yaml.load(f.read())

        for setting_definition_name, setting_definition in definition['settings'].items():
            for scope in Scope:
                # Add core setting
                setting_name = '{}_{}_core'.format(setting_definition_name, scope.name)
                options_core = ''
                if 'options' in setting_definition:
                    for option in setting_definition['options']:
                        options_core += ', {}={}'.format(option, setting_definition['options'][option])

                exec('self.add_setting({setting_class}("{setting_name}", {scope}, {default_value}{options}))'
                     .format(setting_class=setting_definition['setting_class'],
                             setting_name=setting_name,
                             scope=scope,
                             default_value=setting_definition['default_value'],
                             options=options_core))

                # Add widgets settings
                for widget_name, widget in setting_definition['widgets'].items():
                    setting_name = '{}_{}_{}'.format(setting_definition_name, scope.name, widget_name)
                    options = options_core
                    if widget and 'options' in widget:
                        for option in widget['options']:
                            options += ', {}={}'.format(option, widget['options'][option])

                    exec('self.add_setting({setting_class}("{setting_name}", {scope}, {default_value}{options}))'
                         .format(setting_class=setting_definition['setting_class'],
                                 setting_name=setting_name,
                                 scope=scope,
                                 default_value=setting_definition['default_value'],
                                 options=options))

        self.add_setting(String('value_list_str', Scope.Global, 'my_val_1', value_list= ('my_val_1', 'my_val_2')))



