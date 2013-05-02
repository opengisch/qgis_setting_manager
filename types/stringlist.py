
from PyQt4.QtCore import QSettings, SIGNAL, QStringList, Qt
from PyQt4.QtGui import QListWidget, QButtonGroup, QListWidgetItem
from qgis.core import QgsProject

from ..setting import Setting


class Stringlist(Setting):

    def __init__(self, pluginName, name, scope, defaultValue, options={}):

        setGlobal = lambda(value): QSettings(pluginName, pluginName).setValue(name, value)
        setProject = lambda(value): QgsProject.instance().writeEntry(pluginName, name, value)
        getGlobal = lambda: QSettings(pluginName, pluginName).value(name, defaultValue).toStringList()
        getProject = lambda: QgsProject.instance().readListEntry(pluginName, name, defaultValue)[0]

        Setting.__init__(self, pluginName, name, scope, defaultValue, options,
                         setGlobal, setProject, getGlobal, getProject)

    def check(self, value):
        if type(value) not in (list, tuple, QStringList):
            raise NameError("Setting %s must be a string list." % self.name)

    def setWidget(self, widget):
        if type(widget) == QListWidget:
            self.signal = SIGNAL("clicked()")
            self.widgetSetMethod = self.setListBoxes
            self.widgetGetMethod = self.getListBoxes
        elif type(widget) == QButtonGroup:
            self.signal = SIGNAL("buttonClicked(int)")
            self.widgetSetMethod = self.setGroupBoxes
            self.widgetGetMethod = self.getGroupBoxes
        else:
            raise NameError("SettingManager does not handle %s widgets for integers for the moment (setting: %s)" %
                            (type(widget), self.name))
        self.widget = widget

    def setListBoxes(self, value):
        if self.widget is None:
            return
        for i in range(self.widget.count()):
            item = self.widget.item(i)
            if item.text() in value:
                item.setCheckState(Qt.Checked)
            else:
                item.setCheckState(Qt.Unchecked)

    def getListBoxes(self):
        if self.widget is None:
            return
        value = []
        for i in range(self.widget.count()):
            item = self.widget.item(i)
            if item.checkState() == Qt.Checked:
                value.append(item.text())
        return value

    def setGroupBoxes(self, value):
        if self.widget is None:
            return
        for item in self.widget.buttons():
            item.setChecked(item.objectName() in value)

    def getGroupBoxes(self):
        if self.widget is None:
            return
        value = []
        for item in self.widget.buttons():
            if item.isChecked():
                value.append(item.objectName())
        return value

