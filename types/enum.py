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
# ---------------------------------------------------------------------

from enum import Enum as PyEnum

from PyQt5.QtWidgets import QComboBox
from qgis.core import Qgis, QgsSettings

from ..setting import Setting, Scope


class EnumType(PyEnum):
    NoEnum = 1
    QGIS = 2
    Python = 3


class Enum(Setting):
    def __init__(self,
                 name,
                 scope: Scope,
                 default_value,
                 enum_type: EnumType = EnumType.NoEnum,
                 **kwargs):
        """

        :param name: the name of the setting
        :param scope: at the moment only Global scope is supported for Enum
        :param default_value: the default value given as enum
        :param enum_type: if not , the setting will be associated to the enum as given by the default value.
                     Can be QGIS for a QGIS enum. Enum must have been declared using Qt Q_ENUM macro.
                     Enum mode is available for global settings only.
        :param kwargs:
        """

        assert scope is Scope.Global

        self.enum_type = enum_type

        if enum_type == EnumType.Python:
            Setting.__init__(self, name, scope, default_value,
                             object_type=int, # for Python enum and global, force conversion to int
                             **kwargs)
        else:
            Setting.__init__(self, name, scope, default_value,
                             object_type=None,
                             qsettings_read=QgsSettings().enumValue,
                             qsettings_write=QgsSettings().setEnumValue,
                             **kwargs)

    def check(self, value):
        if self.enum_type is EnumType.QGIS and not isinstance(value, self.default_value.__class__) or \
                self.enum_type is EnumType.Python and value.__class__ not in (int, self.default_value.__class__):
            message = '{plugin}:: Invalid value for setting {name}: {value} ({vclass}). ' \
                      'It must be a {type}.'.format(
                plugin=self.plugin_name, name=self.name,
                value=value, vclass=value.__class__,
                type=self.default_value.__class__
            )
            raise NameError(message)
            self.info(message, Qgis.Warning)
            return False
        return True

    def read_out(self, value, scope):
        # for Python enum and global, force conversion to int
        if self.enum_type == EnumType.Python and self.scope == Scope.Global:
            return self.default_value.__class__(value)
        else:
            return value

    def write_in(self, value, scope):
        # for Python enum and global, force conversion to int
        if self.enum_type == EnumType.Python and self.scope == Scope.Global:
            return value.value
        else:
            return value

    @staticmethod
    def supported_widgets():
        from ..widgets import ComboEnumWidget
        return {
            QComboBox: ComboEnumWidget
        }


