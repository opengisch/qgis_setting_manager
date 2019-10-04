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

from qgis.PyQt.QtWidgets import QLineEdit, QComboBox, QButtonGroup
from qgis.core import Qgis
from qgis.gui import QgsMapLayerComboBox, QgsFieldComboBox, QgsFileWidget, QgsProjectionSelectionWidget,\
    QgsAuthConfigSelect

from ..setting import Setting, Scope
from ..widgets import LineEditStringWidget, ButtonGroupStringWidget, ComboStringWidget,\
    MapLayerComboStringWidget, FieldComboStringWidget, FileStringWidget, AuthConfigSelectStringWidget, ProjectionStringWidget



class String(Setting):
    def __init__(self,
                 name,
                 scope: Scope,
                 default_value,
                 **kwargs):
        """

        :param name:
        :param scope:
        :param default_value:
        :param combo_mode: defines what is used to retrieve the setting in a combo box. Can be Data (default) or Text.
        :param enum: if given, the setting will be associated to the enum as given by the default value.
                     Can be QGIS for a QGIS enum. Enum must have been declared using Qt Q_ENUM macro.
                     Enum mode is available for global settings only.
        :param kwargs:
        """

        # prevent bad usage (from older version)
        assert 'combo_mode' not in kwargs

        Setting.__init__(self, name, scope, default_value, object_type=str, ** kwargs)

    def check(self, value):
        if value is not None and type(value) != str:
            self.info('{}:: Invalid value for setting {}: {}. It must be a string.'
                      .format(self.plugin_name, self.name, value),
                      Qgis.Warning)
            return False
        return True

    @staticmethod
    def supported_widgets():
        return {
            QgsMapLayerComboBox: MapLayerComboStringWidget,
            QgsFieldComboBox: FieldComboStringWidget,
            QgsFileWidget: FileStringWidget,
            QgsProjectionSelectionWidget: ProjectionStringWidget,
            QgsAuthConfigSelect: AuthConfigSelectStringWidget,
            QLineEdit: LineEditStringWidget,
            QButtonGroup: ButtonGroupStringWidget,
            QComboBox: ComboStringWidget,
        }


