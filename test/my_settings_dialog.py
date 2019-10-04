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

from PyQt5.QtWidgets import QDialog, QDoubleSpinBox, QComboBox, QListWidget, QGridLayout
from qgis.core import QgsTolerance
from qgis.gui import QgsCollapsibleGroupBox
from ..setting_dialog import SettingDialog, UpdateMode
from .my_settings import MySettings


class MySettingsDialog(QDialog, SettingDialog):
    def __init__(self, setting_name, widget_class, mode: UpdateMode=UpdateMode.DialogAccept, init_widget=None):
        """

        :param setting_name:
        :param widget_class:
        :param mode:
        :param init_widget: some initializing code for the widget
        """

        settings = MySettings()

        QDialog.__init__(self, setting_manager=settings, mode=mode)
        SettingDialog.__init__(self, setting_manager=settings, mode=mode)

        #super(QDialog, self).__init__(setting_manager=settings, mode=mode)
        self.DEBUG = True

        self.widget = widget_class(self)
        self.widget.setObjectName(setting_name)

        if init_widget:
            print("runnning init_widget lambda")
            init_widget(self.widget)

        self.settings = settings
        self.init_widgets()
