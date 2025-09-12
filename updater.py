from utils.config_parser import IgnoreUpdates, Version, UpdateURL
import os
import requests
from zipfile import ZipFile
from io import BytesIO
from elevate import elevate
from tkinter import messagebox

DoneUpdateURL = UpdateURL + Version + '/w64.zip'
VersionURL = 'https://raw.githubusercontent.com/karkar47/karkar47/refs/heads/main/other/aydar/version'



def check_for_updates():
    ver_resp = requests.get(VersionURL)
    get_ver = ver_resp.text.strip("\n")

    if get_ver > Version:
        try_update()
        return True
    else:
        return False

def try_update():
    dialog_answer = messagebox.askyesno("Обнова прилетела!", "Хотите обновиться?")
    upd_resp = requests.get(DoneUpdateURL) 

    if IgnoreUpdates:
        return
    if dialog_answer:
        elevate()

        os.system('taskkill /f /im aydar.exe')

        os.mkdir("temp")

        with ZipFile(BytesIO(upd_resp.content)) as zip_file:
            zip_file.extractall('temp/')
        
        os.replace('temp/w64/aydar.exe', 'aydar.exe')
        os.replace('temp/w64/welcome.exe', 'welcome.exe')
        os.replace('temp/w64/_internal', '_internal')
        os.rmdir('temp')


if __name__ == '__main__':
    check_for_updates()