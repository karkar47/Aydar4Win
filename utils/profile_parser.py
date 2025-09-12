from configparser import ConfigParser
import os
import requests
from zipfile import ZipFile
from io import BytesIO
from utils.config_parser import DownloadURL

profile_file = 'profiles/.aydarprofiles'
profile = ConfigParser()
profile.optionxform = str # Позволяет сохранять регистр при сохранении конфига

if os.path.exists(profile_file):
    try:
        profile.read(profile_file, encoding='utf-8')
    except Exception as e:
        print(f"Ошибка при чтении профилей {e}")

sections = profile.sections()

def create_profile(section, path2image):
    profile.add_section(section)
    profile.set(section, 'path2image', path2image)

    with open(profile_file, 'w') as profilefile:
        profile.write(profilefile)
    
    os.mkdir(f'profiles/{section}')

    response = requests.get(DownloadURL)
    response.raise_for_status()

    with ZipFile(BytesIO(response.content)) as zip_file:
        zip_file.extractall(f'profiles/{section}')

def delete_profile(section_to_remove):
    if profile.has_section(section_to_remove):
        profile.remove_section(section_to_remove)
        with open(profile_file, 'w') as profilefile:
            profile.write(profilefile)
        print(f"Секция '{section_to_remove}' удалена.")
    else:
        print(f"Секция '{section_to_remove}' не найдена.")

def parse_profiles():
    result = {}
    for section in profile.sections():
        result[section] = {}
        for key, value in profile.items(section):
            result[section][key] = value
            
    return result
