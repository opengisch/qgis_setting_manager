"""
Custom settings for QGIS plugin
Denis Rouzaud
denis.rouzaud@gmail.com
Feb. 2013
"""
# for combobox, the value corresponds to the index of the combobox

from PyQt4.QtCore import QSettings, SIGNAL
from PyQt4.QtGui import QLineEdit, QSpinBox, QSlider, QComboBox
from qgis.core import QgsProject

from setting import Setting


class Integer(Setting):

    def __init__(self, pluginName, name, scope, defaultValue, options={}):

        setGlobal = lambda(value): QSettings(pluginName, pluginName).setValue(name, value)
        setProject = lambda(value): QgsProject.instance().writeEntry(pluginName, name, value)
        getGlobal = lambda: QSettings(pluginName, pluginName).value(name, defaultValue).toInt()[0]
        getProject = lambda: QgsProject.instance().readDoubleEntry(pluginName, name, defaultValue)[0]

        Setting.__init__(self, pluginName, name, scope, defaultValue, options,
                         setGlobal, setProject, getGlobal, getProject)

    def check(self, value):
        if type(value) != int and type(value) != float:
            raise NameError("Setting %s must be an integer." % self.name)

    def setWidget(self, widget):
        if type(self.widget) == QLineEdit:
            signal = SIGNAL("textChanged(QString)")
            widgetSetMethod = widget.setText()
            widgetGetMethod = lambda: widget.text().toInt()[0]
        elif type(self.widget) in (QSpinBox, QSlider):
            signal = SIGNAL("valueChanged(int)")
            widgetSetMethod = widget.setValue
            widgetGetMethod = widget.value
        elif type(self.widget) == QComboBox:
            signal = SIGNAL("activated(int)")
            widgetSetMethod = widget.setCurrentIndex
            widgetGetMethod = widget.currentIndex
        else:
            raise NameError("SettingManager does not handle %s widgets for integers for the moment (setting: %s)" %
                            (type(widget), self.name))
        self.widget = widget
        self.signal = signal
        self.widgetSetMethod = widgetSetMethod
        self.widgetGetMethod = widgetGetMethod
