from utils.config_parser import isWelcomeWorked, IgnoreUpdates, file_ext
import os
import requests

if isWelcomeWorked == False:
    try:
        os.system('welcome.py')
    except Exception as e:
        print(f"Ошибка в запуске приветствия: {e}")