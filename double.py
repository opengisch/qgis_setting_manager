"""
Custom settings for QGIS plugin
Denis Rouzaud
denis.rouzaud@gmail.com
Feb. 2013
"""

from PyQt4.QtCore import QSettings, SIGNAL
from PyQt4.QtGui import QLineEdit, QDoubleSpinBox
from qgis.core import QgsProject

from setting import Setting


class Double(Setting):

    def __init__(self, pluginName, name, scope, defaultValue, options={}):

        setGlobal = lambda(value): QSettings(pluginName, pluginName).setValue(name, value)
        setProject = lambda(value): QgsProject.instance().writeEntryDouble(pluginName, name, value)
        getGlobal = lambda: QSettings(pluginName, pluginName).value(name, defaultValue).toDouble()[0]
        getProject = lambda: QgsProject.instance().readDoubleEntry(pluginName, name, defaultValue)[0]

        Setting.__init__(self, pluginName, name, scope, defaultValue, options,
                         setGlobal, setProject, getGlobal, getProject)
        
    def check(self, value):
        if type(value)!=int and type(value) != float:
            raise NameError("Setting %s must be a double." % self.name)

    def setWidget(self, widget):
        if type(self.widget) == QLineEdit:
            signal = SIGNAL("textChanged(QString)")
            widgetSetMethod = widget.setText
            widgetGetMethod = lambda: widget.text().toDouble()[0]
        elif type(self.widget) == QDoubleSpinBox:
            signal = SIGNAL("valueChanged(double)")
            widgetSetMethod = widget.setValue
            widgetGetMethod = widget.value
        else:
            raise NameError("SettingManager does not handle %s widgets for integers for the moment (setting: %s)" %
                            (type(widget), self.name))
        self.widget = widget
        self.signal = signal
        self.widgetSetMethod = widgetSetMethod
        self.widgetGetMethod = widgetGetMethod


