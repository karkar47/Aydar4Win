from configparser import ConfigParser
import os

config_file = 'dotfiles/.aydarcfg'
config = ConfigParser()
config.optionxform = str # Позволяет сохранять регистр при сохранении

if os.path.exists(config_file):
    try:
        config.read(config_file, encoding='utf-8')
    except Exception as e:
        print(f"Ошибка при чтении конфига {e}")


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

def main():
    # Написал на скорую руку, не бейте сильно
    folder_path = f'{os.environ["HOME"]}/.local/share/Steam/steamapps/common/'
    folders = os.listdir(folder_path)
    out_folders = []

    for folder in folders:
        if folder.startswith('Proton'):
            out_folders.append(folder)
    folder_number = -1

    print("Выберите Proton:")
    for folder in out_folders:
        folder_number += 1
        print(f'{folder_number}. {folder}')
    user_input = input('(0_0)--> ')
    try:
        int(user_input)
    except ValueError:
        main()
    if int(user_input) <= -1 or int(user_input) > folder_number:
        main()

    config.set('DEFAULT', 'ProtonFolder', out_folders[int(user_input)])

    with open(config_file, 'w', encoding='utf-8') as configfile:
        config.write(configfile)

if __name__ == "__main__":
    main()