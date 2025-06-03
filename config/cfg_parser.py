from configparser import ConfigParser
import os

config_file = '.aydarcfg'
config = ConfigParser()

if os.path.exists(config_file):
    try:
        config.read(config_file, encoding='utf-8')
    except Exception as e:
        print(f"Ошибка при чтении конфига {e}")


theme = config.get('DEFAULT', 'theme', fallback='green')
isWelcomeWorked = config.getboolean('DEFAULT', 'isWelcomeWorked', fallback=True)
isPythonFile = config.getboolean('DEFAULT', 'isPythonFile', fallback=False)
IgnoreUpdates = config.getboolean('DEFAULT', 'IgnoreUpdates', fallback=False)

file_ext = '.exe' if isPythonFile == False else '.py'

def update_config(changes):
    for section, params in changes.items():
        if not config.has_section(section):
            config.add_section(section)
        
        for key, value in params.items():
            config.set(section, key, str(value))
    
    try:
        with open(config_file, 'w', encoding='utf-8') as configfile:
            config.write(configfile)
        return True
    except Exception as e:
        print(f"Ошибка при сохранении конфига: {e}")
        return False
