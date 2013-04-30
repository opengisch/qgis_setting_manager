"""
Custom settings for QGIS plugin
Denis Rouzaud
denis.rouzaud@gmail.com
Feb. 2013
"""

from PyQt4.QtCore import QSettings, SIGNAL
from PyQt4.QtGui import QCheckBox
from qgis.core import QgsProject

from setting import Setting


class Bool(Setting):

    def __init__(self, pluginName, name, scope, defaultValue, options={}):

        setGlobal = lambda(value): QSettings(pluginName, pluginName).setValue(name, value)
        setProject = lambda(value): QgsProject.instance().writeEntryBool(pluginName, name, value)
        getGlobal = lambda: QSettings(pluginName, pluginName).value(name, defaultValue).toBool()
        getProject = lambda: QgsProject.instance().readBoolEntry(pluginName, name, defaultValue)[0]

        Setting.__init__(self, pluginName, name, scope, defaultValue, options,
                         setGlobal, setProject, getGlobal, getProject)

    def check(self, value):
        if type(value) != bool:
            raise NameError("Setting %s must be a boolean." % self.name)

    def setWidget(self, widget):
        if type(widget) == QCheckBox or (hasattr(widget, "isCheckable") and self.widget.isCheckable()):
            self.signal = SIGNAL("clicked()")
            self.widgetSetMethod = widget.setChecked
            self.widgetGetMethod = widget.isChecked
        else:
            raise NameError("SettingManager does not handle %s widgets for integers for the moment (setting: %s)" %
                            (type(widget), self.name))
        self.widget = widget
