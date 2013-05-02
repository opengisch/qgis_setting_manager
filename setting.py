from PyQt4.QtCore import QObject, pyqtSignal


class Setting(QObject):
    valueChanged = pyqtSignal()

    def __init__(self, pluginName, name, scope, defaultValue, options, setGlobal, setProject, getGlobal, getProject):
        QObject.__init__(self)
        self.pluginName = pluginName
        self.name = name
        self.scope = scope
        self.defaultValue = defaultValue
        self.widget = None
        self.options = options
        self.setGlobal = setGlobal
        self.setProject = setProject
        self.getGlobal = getGlobal
        self.getProject = getProject

        self.check(defaultValue)

    def check(self, value):
        """
        This method shall be overriden in type subclasses
        to check the validity of the value
        """
        return True

    def setValue(self, value):
        self.check(value)
        if self.scope == "global":
            self.setGlobal(value)
        elif self.scope == "project":
            self.setProject(value)
        self.valueChanged.emit()

    def getValue(self):
        if self.scope == "global":
            return self.getGlobal()
        elif self.scope == "project":
            return self.getProject()

    def setValueOnWidgetUpdateSignal(self):
        if self.widget is None:
            return
        QObject.connect(self.widget, self.signal, self.setValueFromWidget)

    def setWidgetFromValue(self):
        if self.widget is None:
            return
        settingValue = self.getValue()
        self.widgetSetMethod(settingValue)

    def setValueFromWidget(self, dummy=None):
        if self.widget is None:
            return
        widgetValue = self.widgetGetMethod()
        self.setValue(widgetValue)