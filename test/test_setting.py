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


from qgis.testing import unittest
from qgis.PyQt.QtGui import QColor

import nose2

from .my_settings import MySettings

QColor.__repr__ = lambda color: 'QColor: {} a: {}'.format(color.name(), color.alpha())


class TestSetting(unittest.TestCase):

    def test_settings(self):
        my_settings = MySettings()
        for setting_name in my_settings.settings_list():
            setting = my_settings.setting(setting_name)
            new_value = my_settings.new_values[setting_name]
            bad_values = my_settings.bad_values[setting_name]
            yield self.check_setting, setting_name, setting.default_value, new_value, bad_values

    def check_setting(self, name, default_value, new_value, bad_values):
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

        # bad values
        for bad_value in bad_values:
           self.assertFalse(MySettings().set_value(name, bad_value))


if __name__ == '__main__':
    nose2.main()
