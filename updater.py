from utils.config_manager import IgnoreUpdates, Version, UpdateURL, Platform
import os
import requests
import webbrowser
from zipfile import ZipFile
from io import BytesIO
from elevate import elevate
from tkinter import messagebox

DoneUpdateURL = UpdateURL + Version + '/win64.zip' if Platform == 'Windows' else '/lin64.zip'
VersionURL = 'https://raw.githubusercontent.com/karkar47/karkar47/refs/heads/main/other/aydar/version'
ReleaseURL = 'https://github.com/karkar47/Aydar4Win/releases'


def check_for_updates():
    ver_resp = requests.get(VersionURL)
    get_ver = ver_resp.text.strip("\n")

    actual_ver_done = int(get_ver.replace(".", ""))
    ver_done = int(Version.replace(".", ""))

    if actual_ver_done > ver_done:
        try_update()
        return True
    else:
        return False

def try_update():
    dialog_answer = messagebox.askyesno("Обнова прилетела!", "Хотите обновиться?")
    # upd_resp = requests.get(DoneUpdateURL)
    if dialog_answer:
        warning_message = messagebox.askyesno("^_^", 'По нажатию кнопки "Да" вы будете переведены на страницу релизов Aydar.\nЭто сделано так, потому что функция автоматического обновления ещё в разработке.\nСпасибо, что остаетесь с нами!')

    if warning_message and not IgnoreUpdates:
        webbrowser.open_new(ReleaseURL)

        # elevate()

        # command = 'taskkill /f /im aydar.exe' if Platform == 'Windows' else 'pkill -9 aydar'
        # os.system(command)
        # os.mkdir("temp")

        # with ZipFile(BytesIO(upd_resp.content)) as zip_file:
        #     zip_file.extractall('temp/')
        
        # windows_to_update = {'aydar.exe': 'temp/w64/aydar.exe', 'welcome.exe': 'temp/w64/welcome.exe', '_internal': 'temp/w64/_internal'}
        # linux_to_update = {'aydar.exe': 'temp/w64/aydar.exe', 'welcome.exe': 'temp/w64/welcome.exe', '_internal': 'temp/w64/_internal'}
        # to_update = windows_to_update if Platform == 'Windows' else linux_to_update
        # for file in windows_to_update:
        #     if os.path.exists(to_update[file]):
        #         os.replace(file, to_update[file])
                
        # os.rmdir('temp')


if __name__ == '__main__':
    check_for_updates()