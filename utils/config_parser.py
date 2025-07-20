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


isWelcomeWorked = config.getboolean('DEFAULT', 'isWelcomeWorked', fallback=True)
isPythonFile = config.getboolean('DEFAULT', 'isPythonFile', fallback=False)
IgnoreUpdates = config.getboolean('DEFAULT', 'IgnoreUpdates', fallback=False)
UserTheme = config.get('USERPROFILE', 'UserTheme', fallback='dark')
UserColor = config.get('USERPROFILE', 'UserColor', fallback='green')
UserName = config.get('USERPROFILE', 'UserName', fallback='UnknownEgg')
Platform = platform.uname().system


if isPythonFile == True:
    file_ext = '.py'
elif Platform == 'Windows':
    file_ext = '.exe'
else:
    file_ext = ''


def update_config(changes: dict):
    # Читаем существующий конфиг (если есть)
    if os.path.exists(config_file):
        config.read(config_file, encoding='utf-8')
    
    # Применяем изменения
    for section, options in changes.items():
        for key, value in options.items():
            config.set(section, key, str(value))
    
    # Сохраняем
    try:
        with open(config_file, 'w', encoding='utf-8') as f:
            config.write(f)
        return True
    except Exception as e:
        print(f"Ошибка сохранения: {e}")
        return False
