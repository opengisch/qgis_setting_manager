"""
Custom settings for QGIS plugin
Denis Rouzaud
denis.rouzaud@gmail.com
Feb. 2013
"""
# options:
# comboMode: can be data or text. It defines if setting is found directly in combobox text or rather in the userData.

from PyQt4.QtCore import QSettings, SIGNAL, QString
from PyQt4.QtGui import QLineEdit, QButtonGroup, QComboBox
from qgis.core import QgsProject

from ..setting import Setting


class String(Setting):

    def __init__(self, pluginName, name, scope, defaultValue, options={}):

        setGlobal = lambda(value): QSettings(pluginName, pluginName).setValue(name, value)
        setProject = lambda(value): QgsProject.instance().writeEntry(pluginName, name, value)
        getGlobal = lambda: QSettings(pluginName, pluginName).value(name, defaultValue).toString()
        getProject = lambda: QgsProject.instance().readEntry(pluginName, name, defaultValue)[0]

        Setting.__init__(self, pluginName, name, scope, defaultValue, options,
                         setGlobal, setProject, getGlobal, getProject)

    def check(self, value):
        if type(value) != str and type(value) != QString:
            raise NameError("Setting %s must be a string." % self.name)

    def setWidget(self, widget):
        if type(widget) == QLineEdit:
            self.signal = SIGNAL("textChanged(QString)")
            self.widgetSetMethod = widget.setText
            self.widgetGetMethod = widget.text
        elif type(widget) == QButtonGroup:
            self.signal = SIGNAL("buttonClicked(int)")
            self.widgetSetMethod = self.setButtonGroup
            self.widgetGetMethod = self.getButtonGroup
        elif type(widget) == QComboBox:
            self.signal = SIGNAL("activated(int)")
            comboMode = self.options.get("comboMode", "data")
            if comboMode == 'data':
                self.widgetSetMethod = lambda(value): self.widget.setCurrentIndex(widget.findData(value))
                self.widgetGetMethod = lambda: widget.itemData(widget.currentIndex()).toString()
            elif comboMode == 'text':
                self.widgetSetMethod = lambda(value): self.widget.setCurrentIndex(widget.findText(value))
                self.widgetGetMethod = widget.currentText
        else:
            raise NameError("SettingManager does not handle %s widgets for integers for the moment (setting: %s)" %
                            (type(widget), self.name))
        self.widget = widget

    def setButtonGroup(self, value):
        # for checkboxes
        if self.widget is None:
            return
        for button in self.widget.buttons():
            if value == button.objectName():
                button.setChecked(True)
                break

    def getButtonGroup(self):
        if self.widget is None:
            return
        value = ""
        for button in self.widget.buttons():
            if button.isChecked():
                value = button.objectName()
                break
        return value
