"""
Custom settings for QGIS plugin
Denis Rouzaud
denis.rouzaud@gmail.com
Feb. 2013
"""
# options:
# dialogTitle: show in color dialog

from PyQt4.QtCore import QSettings, QStringList, SIGNAL
from PyQt4.QtGui import QColor
from qgis.core import QgsProject
from qgis.gui import QgsColorButton

from setting import Setting


class Color(Setting):

    def __init__(self, pluginName, name, scope, defaultValue, options={}):

        setGlobal = lambda(value): QSettings(pluginName, pluginName).setValue(name, [value.red(),
                                                                                     value.green(),
                                                                                     value.blue()])
        setProject = lambda(value): QgsProject.instance().writeEntry(pluginName, name,
                                                                     QStringList(["%u" % value.red(),
                                                                                  "%u" % value.green(),
                                                                                  "%u" % value.blue()]))
        getGlobal = lambda: self.list2color(QSettings(pluginName, pluginName).value(name, defaultValue).toList())
        getProject = lambda: self.list2color(QgsProject.instance().readListEntry(pluginName, name, defaultValue))

        Setting.__init__(self, pluginName, name, scope, defaultValue, options,
                         setGlobal, setProject, getGlobal, getProject)

    def check(self, color):
        if type(color) != QColor:
            raise NameError("Color setting %s must be a QColor." % self.name)

    def setWidget(self, widget):
        txt = self.options.get("dialogTitle", "")
        self.widget = QgsColorButton(widget, txt)
        self.signal = SIGNAL("colorChanged(color)") # TODO: check if signal is working
        self.widgetSetMethod = self.widget.setColor
        self.widgetGetMethod = self.widget.color

    def list2color(self, color):
        if type(color) != list or len(color) != 3:
            return self.defaultValue
        else:
            r = color[0].toInt()[0]
            g = color[1].toInt()[0]
            b = color[2].toInt()[0]
        return QColor(r, g, b)

