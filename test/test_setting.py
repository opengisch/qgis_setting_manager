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

import qgis
import os
import yaml
from qgis.testing import unittest
from PyQt5.QtGui import QColor

import nose2

from .my_settings import MySettings
from .. import Scope


class TestSetting(unittest.TestCase):
    def test_settings(self):
        cur_dir = os.path.dirname(__file__)
        definition_file = os.path.join(cur_dir, 'setting_config.yaml')
        with open(definition_file, 'r') as f:
            definition = yaml.load(f.read())

        for setting_definition_name, setting_definition in definition['settings'].items():
            for scope in Scope:
                setting_name = '{}_{}_core'.format(setting_definition_name, scope.name)
                default_value = eval(str(setting_definition['default_value']))
                new_value = eval(str(setting_definition['new_value']))
                yield self.check_setting, setting_name, default_value, new_value

    def check_setting(self, name, default_value, new_value):
        # clean just in case
        MySettings().remove(name)

        # default
        self.assertEqual(MySettings().value(name), default_value)

        # set value
        MySettings().set_value(name, new_value)
        self.assertEqual(MySettings().value(name), new_value)

        # remove setting
        MySettings().remove(name)
        self.assertEqual(MySettings().value(name), default_value)

#    def test_value_list(self):
#        MySettings().set_value('value_list_str', 'my_invalid_val')
#        self.assertEqual(MySettings().value('value_list_str'), 'my_val_1')


if __name__ == '__main__':
    nose2.main()
