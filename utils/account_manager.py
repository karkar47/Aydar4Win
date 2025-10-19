from configparser import ConfigParser
import os
import requests
import webview
import platform as pf
from cryptography.fernet import Fernet

account_file = 'dotfiles/.aydaraccount'
account_mgr = ConfigParser()
account_mgr.optionxform = str # Позволяет сохранять регистр при сохранении

if os.path.exists(account_file):
    try:
        account_mgr.read(account_file, encoding='utf-8')
    except Exception as e:
        print(f"Ошибка при чтении файла аккаунта {e}")

sections = account_mgr.sections()

AccountCookie = account_mgr.get('ACCOUNT', 'AccountCookie', fallback='None')
is_logined_already = account_mgr.getboolean('ACCOUNT', 'is_logined_already', fallback=False)
BlockTrollVideo = account_mgr.getboolean('DEFAULT', 'BlockTrollVideo', fallback=False)
DevMode = account_mgr.getboolean('DEFAULT', 'DevMode', fallback=False)
AccountName = account_mgr.get('ACCOUNT', 'AccountName', fallback='Войти')
AccountPass = account_mgr.get('ACCOUNT', 'AccountPass', fallback='')
AccountEmail = account_mgr.get('ACCOUNT', 'AccountEmail', fallback='')


session = requests.Session()
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Trailer/93.3.3570.29'}
url = "https://epicsusgames.ru/login.php"

platform = pf.system()

def create_key():
    key = Fernet.generate_key()

    folder_path = f'{os.environ['USERPROFILE']}\\.aydar' if platform == "Windows" else f'{os.environ['HOME']}/.aydar'
    key_path = f'{os.environ['USERPROFILE']}\\.aydar\\aydarkey' if platform == "Windows" else f'{os.environ['HOME']}/.aydar/aydarkey'

    if not os.path.exists(key_path):
        os.mkdir(folder_path)
    with open(key_path, "w", encoding='utf-8') as file:
        file.write(key.decode())

def read_key():
    folder_path = f'{os.environ['USERPROFILE']}\\.aydar' if platform == "Windows" else f'{os.environ['HOME']}/.aydar'
    key_path = f'{os.environ['USERPROFILE']}\\.aydar\\aydarkey' if platform == "Windows" else f'{os.environ['HOME']}/.aydar/aydarkey'
    if os.path.exists(key_path):
        with open(key_path, "rb") as file:
            key = file.read()
        return key
    else:
        create_key()
        return False

key = read_key()
cipher = Fernet(key)

def encrypt_data(email, password, cookie):
    encpass = cipher.encrypt(password.encode())
    encemail = cipher.encrypt(email.encode())
    enccookie = cipher.encrypt(cookie.encode())

    account_mgr.set('ACCOUNT', 'AccountPass', encpass.decode())
    account_mgr.set('ACCOUNT', 'AccountEmail', encemail.decode())
    account_mgr.set('ACCOUNT', 'AccountCookie', enccookie.decode())

    with open(account_file, 'w', encoding='utf-8') as accountfile:
        account_mgr.write(accountfile)

def decrypt_data():
    outpass = cipher.decrypt(AccountPass).decode()
    outemail = cipher.decrypt(AccountEmail).decode()
    outcookie = cipher.decrypt(AccountCookie).decode()

    return {"email": outemail, "password": outpass, "cookie": outcookie}

def account_login(email, password):
    data = {"email": email, "password": password, "login": ""}
    response = session.post(url, data=data, headers=headers)

    if "Вход | EpicSUS ID" in response.text:
        return False
    else:
        encrypt_data(email=email, password=password, cookie=f'{session.cookies.get_dict()['PHPSESSID']}')
        account_mgr.set('ACCOUNT', 'is_logined_already', 'True')
        

        # Вычисление имени аккаунта
        start_index = response.text.find('<title>')
        finish_index = response.text.find(' | EpicSUS')

        if start_index != -1 and finish_index != -1:
            ExtractedName = response.text[start_index + len('<title>'):finish_index]
            account_mgr.set('ACCOUNT', 'AccountName', ExtractedName)
        else:
            ExtractedName = False

        with open(account_file, 'w', encoding='utf-8') as accountfile:
            account_mgr.write(accountfile)
        
        return ExtractedName


def open_account():
    data = decrypt_data()

    # Заранее делаем заготовку 
    script = """
    if (localStorage.getItem('reloaded')) {
        if (""" + str(BlockTrollVideo).lower() + """ === true) {
            const troll = document.getElementById('trollVideo');
            if (troll) {
                troll.remove();
            }
        }
    }
    else {
        localStorage.setItem('reloaded', 'true');
        document.cookie = 'PHPSESSID=""" + data['cookie'] + """; path=/';
        // setTimeout(() => window.location.reload(), 10);
        window.location.reload();
    }
    """

    def set_cookies(window):
        window.run_js(script)

    def on_request_sent(request):
        request.headers['sec-ch-ua-platform'] = '"Windows"' # Чтобы уж точно все было без палева
        request.headers['sec-ch-ua'] = '"Chrome";v=136' # Браузер тоже 

    window = webview.create_window('Профиль', 'https://epicsusgames.ru/profile')
    window.events.loaded += set_cookies
    window.events.request_sent += on_request_sent

    webview.start(debug=DevMode, user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Trailer/93.3.3570.29')


def check_account_session():
    if is_logined_already:
        data = decrypt_data()
        cookies = {'PHPSESSID': data['cookie']}
        request = requests.get(url, cookies=cookies)
        if "Вход | EpicSUS" in request.text:
            account_login(email=data['email'], password=data['password'])
