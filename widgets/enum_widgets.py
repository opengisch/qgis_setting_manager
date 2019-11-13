#-----------------------------------------------------------
#
# QGIS setting manager is a python module to easily manage read/write
# settings and set/get corresponding widgets.
#
# Copyright    : (C) 2019 Denis Rouzaud
# Email        : denis@opengis.ch
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


from ..setting_widget import SettingWidget
from ..types.enum import EnumType


class ComboEnumWidget(SettingWidget):
    def __init__(self, setting, widget):
        signal = widget.currentIndexChanged
        SettingWidget.__init__(self, setting, widget, signal)

    def set_widget_value(self, value):
        self.widget.setCurrentIndex(self.widget.findData(value))

    def widget_value(self):
        value = self.widget.itemData(self.widget.currentIndex())
        if value is None:
            value = self.setting.default_value
        value = self.setting.default_value.__class__(value)
        return value

    def auto_populate(self):
        assert self.setting.enum_type == EnumType.Python
        self.disconnect_widget_auto_update()
        for e in list(self.setting.default_value.__class__):
            self.widget.addItem(str(e), e)
        self.connect_widget_auto_update()






