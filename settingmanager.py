"""
Custom settings for QGIS plugin
Denis Rouzaud
denis.rouzaud@gmail.com
http://3nids.github.io/qgissettingmanager/
"""
from types import *

# to print debug info
Debug = False

# possible types
valueTypes = ("string", "double", "integer", "bool", "color", "stringlist")


class SettingManager():
    def __init__(self, pluginName):
        self.pluginName = pluginName
        self.settings = []

    def addSetting(self, name, settingType, scope, defaultValue, options={}):
        if self.setting(name) is not None:
            raise NameError("%s already exist in settings." % name)
        if settingType.lower() not in valueTypes:
            raise NameError("Wrong type %s" % settingType)
        if scope.lower() not in ("global", "project"):
            raise NameError("%s is not a valid scope. Must be project or global." % scope)
        SettingClass = globals()[settingType[0].upper() + settingType[1:].lower()]
        setting = SettingClass(self.pluginName, name, scope, defaultValue, options)
        self.settings.append(setting)

    def setting(self, name):
        for setting in self.settings:
            if setting.name == name:
                return setting
        return None

    def value(self, settingName):
        setting = self.setting(settingName)
        if setting is None:
            raise NameError('%s has no setting %s' % (self.pluginName, settingName))
        return setting.getValue()

    def setValue(self, settingName, value):
        setting = self.setting(settingName)
        if setting is None:
            raise NameError('%s has no setting %s' % (self.pluginName, settingName))
        setting.setValue(value)






