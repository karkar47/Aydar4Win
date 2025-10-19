from configparser import ConfigParser
import os
import requests
import shutil
from zipfile import ZipFile
from io import BytesIO

profile_file = 'dotfiles/.aydarprofiles'
profile_mgr = ConfigParser()
profile_mgr.optionxform = str

if os.path.exists(profile_file):
    try:
        profile_mgr.read(profile_file, encoding='utf-8')
    except Exception as e:
        print(f"Ошибка при чтении конфига {e}")

profiles = profile_mgr.sections()
number_of_profiles = len([profile for profile in profiles if profile.startswith('apid')])


def create_profile(name, path2image, DownloadURL):
    global number_of_profiles
    profile_id = f'apid{number_of_profiles + 1:03d}'

    profile_mgr.add_section(profile_id)
    profile_mgr.set(profile_id, 'path2image', path2image)
    profile_mgr.set(profile_id, 'name', name)

    with open(profile_file, 'w', encoding='utf-8') as profilefile:
        profile_mgr.write(profilefile)

    os.mkdir(f'profiles/{profile_id}')

    response = requests.get(DownloadURL)
    response.raise_for_status()

    with ZipFile(BytesIO(response.content)) as zip_file:
        zip_file.extractall(f'profiles/{profile_id}')

def delete_profile(profile2remove):
    # elevate()
    if profile_mgr.has_section(profile2remove):
        profile_mgr.remove_section(profile2remove)
        with open(profile_file, 'w', encoding='utf-8') as profilefile:
            profile_mgr.write(profilefile)
        shutil.rmtree(f'profiles/{profile2remove}')
    else:
        print(f"{profile2remove} not found. Nothing to delete")

def parse_profiles():
    result = {}
    for profile in profiles:
        result[profile] = {}
        for key, value in profile_mgr.items(profile):
            result[profile][key] = value
    return result

def start_profile(platform, name, proton_folder):
    if platform == "Windows":
        yaica_path_win = f'profiles\\{name}\\Яйцеоды 2.exe'
        os.startfile(yaica_path_win)
    else:
        if proton_folder != '' and proton_folder != None:
            yaica_cmd_path_lin = f"export STEAM_COMPAT_CLIENT_INSTALL_PATH=~/.local/share/Steam/ && export STEAM_COMPAT_DATA_PATH=~/.local/share/Steam/steamapps/compatdata && ~/.local/share/Steam/steamapps/common/'{proton_folder}'/proton run profiles/'{name}'/'Яйцеоды 2.exe'"
            os.startfile(yaica_cmd_path_lin)
        else:
            print('proton root folder empty')

def open_profile_mods_folder(platform, id):
    
    if platform == "Windows":
        folder2open = f'profiles\\{id}\\mods\\'
        os.startfile(folder2open)
    else:
        folder2open = f'/profile/{id}/mods/'
        os.popen(["xdg-open", folder2open])

def save_chosen_icon(path2image, profile):
    profile_mgr.set(profile, 'path2image', path2image)

    with open(profile_file, 'w', encoding='utf-8') as profilefile:
        profile_mgr.write(profilefile)

def rename_profile(profile, name):
    profile_mgr.set(profile, 'name', name)

    with open(profile_file, 'w', encoding='utf-8') as profilefile:
        profile_mgr.write(profilefile)