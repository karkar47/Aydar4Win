from configparser import ConfigParser
import os
import platform

config_file = '.aydarcfg'
config = ConfigParser()
config.optionxform = str # Позволяет сохранять регистр при сохранении конфига

if os.path.exists(config_file):
    try:
        config.read(config_file, encoding='utf-8')
    except Exception as e:
        print(f"Ошибка при чтении конфига {e}")

# objects2check = ['profiles/.aydarprofiles', 'media/icons/png/aydar-140x45-white.png']

# for obj in objects2check:
#     print(os.path.exists(obj))

isWelcomeWorked = config.getboolean('DEFAULT', 'isWelcomeWorked', fallback=True)
isPythonFile = config.getboolean('DEFAULT', 'isPythonFile', fallback=False)
IgnoreUpdates = config.getboolean('DEFAULT', 'IgnoreUpdates', fallback=False)
UserTheme = config.get('USERPROFILE', 'UserTheme', fallback='dark')
UserColor = config.get('USERPROFILE', 'UserColor', fallback='green')
UserName = config.get('USERPROFILE', 'UserName', fallback='UnknownEgg')


def update_config(changes: dict):
    # Сохраняет изменения
    if os.path.exists(config_file):
        config.read(config_file, encoding='utf-8')
    
    for section, options in changes.items():
        for key, value in options.items():
            config.set(section, key, str(value))
    
    try:
        with open(config_file, 'w', encoding='utf-8') as f:
            config.write(f)
        return True
    except Exception as e:
        print(f"Ошибка сохранения: {e}")
        return False
