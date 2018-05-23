# How to use _utils.config_ and _utils.locale_
## 1. Config
Firstly, import it:
```python
import utils.config as cfg
```
It is good practice to initialize config at the app startup, although if you don't do this, app will try to do it
automatically when you're first getting a property. Config is already initialized in `App.__init__()`
so you don't have to do it:
```python
cfg.init()
```

Example config file looks like this:
```ini
[SOMEGROUP]
message = Hello world
pi = 3.14
isConfigAwesome = yes

[OTHER]
someIntProperty = 2137
```

Config file location is set in `utils/constants.py`:
```python
CONFIG_FILE = 'config.ini'
```
If the file doesn't exist, `utils.config` module will create one with default settings
(see `__create_default_cfg()` in `utils/config.py`)

_**TODO:**_ Move default config creation to a better place

### Getting values
To get config property, simply use `cfg.get(group: str, property: str) -> str`:
```python
my_message = cfg.get('somegroup', 'message')    # returns 'Hello World'
pi_str = cfg.get('somegroup', 'pi')             # returns '3.14'
pi = float(pi_str)                              # we need to convert it to float
bool_str = cfg.get('somegroup', 'isConfigAwesome')  # returns 'yes'
```

We can also get whole `SOMEGROUP`:
```python
some_group = cfg.get('somegroup')
message = some_group['message']

#this is the same:
message = cfg.get('somegroup')['message']

#and this:
message = cfg.get('somegroup', 'message') 
```

We have also built-in type conversions:
```python
# 'yes/no', 'true/false' are automatically converted to bool
some_group = cfg.get('somegroup')
is_awesome = some_group.getboolean('isConfigAwesome' )    # returns True
pi = some_group.getfloat('pi')          # returns 3.14

int_prop = cfg.get('other').getint('someintproperty')   # returns 2137
```

**NOTE**: Property names are _NOT_ case sensitive.

### Setting values
To update config inside code, just get whole group, update its properties and call `cfg.save()`:
```python
some_group = cfg.get('somegroup')                   # get property group
some_group['message'] = "This is my new message"    # update value
cfg.save()                                          # saves updated values to config.ini
```
That's it.

For more info, see official Python `configparser` library [documentation](https://docs.python.org/3/library/configparser.html).

## 2. Locale
To use locale, we need to import `utils.locale`:
```python
import utils.locale as i18n
```

Like in config (see section 1), library can be initialized with `i18n.init()`, but it's already done in App class.

Locale file location is set in `utils/constants.py`:
```python
LOCALE_FILE = 'locale.ini'
```

The file looks like this
```ini
[ENGLISH]
message = Hello World

[POLISH]
message = Witaj Świecie
```


Current language is set in `config.ini` as `locale` property of `GENERAL` section:
```ini
[GENERAL]
locale = english
...
```

### Getting translations
Simply use `i18n.get()`:
```python
my_message = i18n.get('message')    # returns 'Hello World'
```
It throws `KeyError` when message is not defined in current language

### Switching language
```python
i18n.switch_language('polish')
my_message = i18n.get('message')   # returns 'Witaj Świecie'
```
If language is not found, it will throw `NameError`

_Probably to see effects of switching languages, app restart is needed,
because for example menu title is only set at startup but I need to check it_

