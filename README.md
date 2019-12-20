[![Build Status](https://travis-ci.org/opengisch/qgissettingmanager.svg?branch=master)](https://travis-ci.org/opengisch/qgissettingmanager)

## About

Easily manage the settings in your [QGIS](http://www.qgis.org) plugin.

This module can:

* manage **different types of settings** (bool, string, color, integer, double, stringlist)
* **read and write settings** both in QGIS application or in the QGIS project
* automatically **set widgets** of a dialog according to their **corresponding setting**
* automatically **write settings from their corresponding widgets**

You are looking at the documentation for **QGIS 3**. See the [qgis2](https://github.com/opengisch/qgissettingmanager/tree/qgis2) branch for QGIS 2.
Current version requires QGIS 3.2 minimum (otherwise projection widgets are not supported).


## The main setting class

All your settings shall be saved in a single class, which will subclass SettingManager.

```python
from qgissettingmanager import *

class MySettings(SettingManager):
    def __init__(self):
        SettingManager.__init__(self, my_plugin_name)
        self.add_setting( Bool("my_setting", Scope.Global, True) )
```

You may add as many settings as you want using `add_setting` method:

```python
add_setting( SettingClass( name, scope, default_value, allowed_values: list = None, **options ) )
```

* `SettingClass`: `Bool`, `String`, `Color`, `Integer`, `Double`, `Stringlist` or `Dictionary`
* `name`: the name of the setting
* `scope`: `Scope.Global` or `Scope.Project`
* `default_value`: the default value of the setting (type must correspond)
* `allowed_values`: a list of authorized values. 
If specified, the setting will fall back to `default_value` if an unauthorized value is provided.
* `options`: additional options (see [possible widgets](#possiblewidgets))

### Access the settings

Instantiate your settings class in your current class:

```python
import MySettings
self.settings = MySettings()
```

The settings are easily accessed using the `value` and `setValue` methods:

```python
myVariable = self.settings.value("myVariable")
self.settings.set_value("myVariable", False)
```

### Remove settings

Settings can be removed from registry (local or project wise) using `MySettings().remove('my_setting')`.


## Match settings with widgets of a dialog

### Quick start

You can associate a setting to a defined widget in a dialog (or a dockable window). The first condition is to **name the widget as the setting name**.
Then, your dialog class shall subclass the `SettingDialog` class:

```python
class MyDialog(QDialog, Ui_myDialog, SettingDialog):
    def __init__(self):
        settings = MySettings()
        super.__init__(self, setting_manager=settings)
        self.setupUi(self)
        self.settings = settings
        self.init_widgets()
```

Hence, when the dialog is shown, all widgets which are named according to a  setting will be set to the corresponding value. On dialog acceptance, the settings will be set according to the value read from their widget.

To control which setting has been associated to a widget, you can print `self.widget_list()`.

### Settings' update behavior

You can have a different behavior using `SettingDialog` parameters:

```python
super.__init__(self, setting_manager=settings, mode=UpdateMode.WidgetUpdate)
```

`mode` can take the following values:

* `UpdateMode.NoUpdate`: settings values won't be updated;
* `UpdateMode.DialogAccept`: settings values are set when the dialog is accepted _(default)_;
* `UpdateMode.WidgetUpdate`: settings are set as soon as the widget is modified.

### Check something before updating the settings

You can override the `SettingDialog.before_accept_dialog()` method to check your settings.
Settings will be saved only if the method returns `True`.

### Using showEvent

Be warned that `SettingDialog` implements `showEvent` method. Therefore, if you redefine it in your dialog class, you have to write:

```python
def showEvent(self, e):
    settingDialog.showEvent(self, e)
    # do your own stuff
```


### Possible widgets
<a name="possiblewidgets"/>

The widgets are automatically detected by the manager. If the type of widget is not handled, an error is raised.

To access widget properties, get the widget after the initilization of setting widgets and set them afterwards.
For instance:

```python
class MyDialog(QDialog, Ui_myDialog, SettingDialog):
    def __init__(self):
        settings = MySettings()
        super.__init__(self, setting_manager=settings)
        self.setupUi(self)
        self.settings = settings
        self.init_widgets()

        list_table_widget: TableWidgetStringListWidget = self.setting_widget('my_list')
        list_table_widget.column = 0  # to modify the column to be checked
        list_table_widget.userdata = True  # to use UserData instead of Text
        list_table_widget.invert = True   # to invert the checking 
```


**String**

* `QLineEdit`
* `QComboBox` 
    * `mode`: additional option to define what is used to retrieve the setting. Can be `ComboMode.Text` or [`ComboMode.Data`](http://qt-project.org/doc/qt-5/qcombobox.html#itemData).
    * `auto_populate()`: auto populates the combo box from the possible values (need to be defined). Mode will be set to `ComboMode.Data`.
* `QButtonGroup` (the setting is set as the checked widget text in the button group)
* `QgsMapLayerComboBox` uses layer ID for the setting value
* `QgsFileWidget`
* `QgsAuthConfigSelect`

**Boolean**

* `QCheckBox`
* Any checkable widget (groupbox, etc.)

**Color**

* Native QGIS widgets (QgsColorButton) or any widget (label or pushbutton are recommended). For standard Qt Widgets, QGIS [color button](http://qgis.org/api/classQgsColorButton.html)) will be used. 

Additional options:
* `allow_alpha` (boolean) to allow transparent colors
* `dialog_title` (string) to set the dialog title.

**Integer**

* `QLineEdit`
* `QSpinBox`
* `QSlider`
* `QComboBox` (setting is set as the combo box index)

**Double**

* `QLineEdit`
* `QDoubleSpinBox`
* `QgsScaleWidget`

**String list**

* `QListWidget` (checks items having their _text_ in the list)
* `QButtonGroup` (checks items having their _name_ in the list)
* `QTableWidget` checks items having their _text_ or _data_ in the table. Properties of the widget:
  * `column` specifies which column is used
  * `invert` if True, unchecked items are saved
  * `userdata` if True, use the `userData` instead of the `text
  
** Enums (from QGIS API or as Python Enum) **

* ComboEnumWidget`
  * `auto_populate()`: auto populates the combo box from the possible enum entries (only for Python)

  
**Dictionnary**

* No widgets are offered yet.

**List**

* No widgets are offered yet.
* Works only for global settings


New types of widget are easily added, if one is missing, do not hesitate to [ask](https://github.com/opengisch/qgissettingmanager/issues)!

## Using git submodules

To use this module, you can easily copy the files and put them in your project.
A more elegant way is to use [git submodule](http://git-scm.com/book/en/Git-Tools-Submodules). Hence, you can keep up with latest improvements. In you plugin directory, do

```
git submodule add https://github.com/opengisch/qgissettingmanager.git
```

A folder _qgissettingmanager_ will be added to your plugin directory. 
However, git only references the module, and you can `git pull` in this folder to get the last changes.
