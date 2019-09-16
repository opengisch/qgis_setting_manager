#-----------------------------------------------------------
#
# QGIS setting manager is a python module to easily manage read/write
# settings and set/get corresponding widgets.
#
# Copyright    : (C) 2016 Denis Rouzaud
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

from PyQt5.QtCore import pyqtSlot, QObject
from qgis.core import Qgis, QgsMessageLog


class SettingWidget(QObject):

    DEBUG = False

    def __init__(self, setting, widget, signal):
        QObject.__init__(self)

        self.setting = setting
        self.widget = widget
        self.signal = signal
        self.connected = False

    def __repr__(self):
        return 'SettingWidget: {} with value: {}'.format(self.setting.name, self.widget_value())

    def connect_widget_auto_update(self):
        """
        This connects the proper signal of the widget to self.set_value_from_widget
        """
        self.signal.connect(self.set_value_from_widget)
        self.connected = True

    def disconnect_widget_auto_update(self):
        """
        This disconnects the proper signal of the widget from self.set_value_from_widget
        """
        if self.connected:
            self.signal.disconnect(self.set_value_from_widget)
            self.connected = False

    def set_widget_value(self, value):
        """
        To be reimplemented in sub-class
        """
        pass

    def widget_value(self):
        """
        To be reimplemented in sub-class
        """
        return None

    def set_widget_from_value(self):
        if self.DEBUG:
            msg = 'setting {} with value from widget {}'.format(self.setting.name, self.setting.value())
            QgsMessageLog.logMessage('{}:: {}'.format(self.__class__.__name__, msg), 'Setting manager', Qgis.Info)

        reconnect = False
        if self.connected:
            reconnect = True
            self.disconnect_widget_auto_update()
        self.set_widget_value(self.setting.value())
        if reconnect:
            self.connect_widget_auto_update()

    @pyqtSlot()
    def set_value_from_widget(self):
        self.setting.set_value(self.widget_value())
