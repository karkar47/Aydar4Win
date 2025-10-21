import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk
from utils.config_manager import UserName, isWelcomeWorked, UserTheme, Platform, DownloadURL, ProtonFolder, UserColor
from utils.profile_manager import parse_profiles, profiles, number_of_profiles, create_profile, delete_profile, start_profile, open_profile_mods_folder, save_chosen_icon, rename_profile
from utils.account_manager import account_login, open_account, check_account_session, is_logined_already, AccountName
import multiprocessing
import threading
import os

# My fellow brothers, I, Billy Herrington, stand here today...

class Aydar(ctk.CTk):
    def __init__(self):
        super().__init__()

        # execfile_ext = '.exe' if Platform == 'Windows' else ''

        if isWelcomeWorked == False:
            try:
                welcome_path = 'welcome.exe' if Platform == 'Windows' else './welcome'
                if os.path.exists(welcome_path):
                    os.system(welcome_path)
                    os._exit(os.EX_OK)
            except:
                print("Welcome not found!")

        try:
            updater_path = 'updater.exe' if Platform == 'Windows' else 'updater'
            updater_command = 'updater.exe' if Platform == 'Windows' else './updater'
            if os.path.exists(updater_path):
                os.system(updater_command)
                print('Updater started!')
        except:
            print("Updater not found!")

        # Настройка окна
        self.title(f"Привет, {UserName}! Чем займёмся сегодня?")
        self.geometry("800x600")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        if Platform == 'Windows':
            self.iconbitmap("media/icons/ico/aydar-200x200-user.ico")
        else:
            img = ImageTk.PhotoImage(Image.open("media/icons/png/aydar-200x200-user.png"))
            self.iconphoto(False, img)


        ctk.set_appearance_mode(UserTheme)
        ctk.set_default_color_theme(UserColor)

        self.profiles = []
        self.selected_profile = None

        self.create_header()
        self.create_sidebar()
        self.create_profile_grid()

        check_account_session()

    def create_header(self):
        # Хедер
        header = ctk.CTkFrame(self, height=40, border_width=0, corner_radius=0) # fg_color='#323232', 
        header.grid(row=0, column=0, sticky="ew")
        header.grid_propagate(False)

        header.grid_columnconfigure(0, weight=1)
        header.grid_columnconfigure(1, weight=1)
        header.grid_columnconfigure(2, weight=1)

        # Иконачке
        self.account_ico = ctk.CTkImage(light_image=Image.open("media/icons/png/aydar-200x200-user.png"), size=(25, 25))
        self.add_profile_ico = ctk.CTkImage(light_image=Image.open("media/icons/png/aydar-200x200-plus.png"), size=(25, 25))
        self.profile_ico = ctk.CTkImage(light_image=Image.open("media/icons/png/aydar-200x200-user.png"), size=(100, 100))
        self.delete_profile_ico = ctk.CTkImage(light_image=Image.open("media/icons/png/aydar-120x120-delete.png"), size=(20, 20))
        self.start_profile_ico = ctk.CTkImage(light_image=Image.open("media/icons/png/aydar-120x120-start.png"), size=(20, 20))
        self.mods_folder_ico = ctk.CTkImage(light_image=Image.open("media/icons/png/aydar-120x120-folder.png"), size=(20, 20))
        self.settings_ico = ctk.CTkImage(light_image=Image.open("media/icons/png/aydar-120x120-settings.png"), size=(20, 20))
        self.reference_ico = '' # справкa

        top_line = ctk.CTkFrame(header, height=0, fg_color='#7a7a7a', border_width=1)
        top_line.grid(row=0, column=0, columnspan=3, sticky='new')
        # После строчки кода чуть выше, ты наверное скажешь "Блин, нифига ты гений, создаешь кадр с размером 0 и задаёшь ему обводку, хотя мог бы сделать кадру размер 1 и всё!"
        # И ты будешь вполне прав, НО! Дело в том, что я уже пытался так сделать. И ЗНАЕШЬ ЧТО???? Customtkinter ПРОСТО НЕ ВЫВОДИТ такой кадр НОРМАЛЬНО, даже если у него размер 1.
        # Поэтому мне приходится делать такой костыль, я не знаю, это баг ctk или я тупой, но так получается.
        # Если ты знаешь в чем дело, пожалуйста сделай пулл реквест с указанием ошибок и пришли мне куда-нибудь(можешь даже в личку), я посмотрю и приму с радостью.

        bottom_line = ctk.CTkFrame(header, height=0, fg_color='#7a7a7a', border_width=1)
        bottom_line.grid(row=1, column=0, columnspan=3, sticky='sew') # слишком запарно, проще иметь одну линию сверху

        # logo_label = ctk.CTkLabel(header, image=logo_img, text="")
        # logo_label.grid(row=0, column=2, sticky="e", pady=5, padx=115)

        def account_command():
            if is_logined_already:
                multiprocessing.Process(target=open_account, daemon=True).start()
            else:
                self.account_window()
        
        self.account_command = account_command
        account_text = AccountName if is_logined_already else "Войти в аккаунт"

        self.account_btn = ctk.CTkButton(header, text=account_text, fg_color='transparent', hover_color=("#a0a0a0", "#474747"), image=self.account_ico, width=90, text_color=('black', 'white'), command=account_command) # hover_color='#474747', 
        self.account_btn.grid(row=0, column=2, sticky="e", pady=3, padx=3)

        add_profile_btn = ctk.CTkButton(header, text="Добавить профиль", fg_color='transparent', hover_color=("#a0a0a0", "#474747"), image=self.add_profile_ico, text_color=('black', 'white'), command=self.add_profile_window)
        add_profile_btn.grid(row=0, column=0, sticky='w', pady=3, padx=3)
    
    def create_sidebar(self):
        # Боковая панель справа
        sidebar = ctk.CTkFrame(self, width=200, border_width=0, corner_radius=0) # fg_color='#323232', 
        sidebar.grid(row=1, column=0, sticky='nes')
        sidebar.grid_propagate(False)

        sidebar.grid_rowconfigure(0, weight=0)
        sidebar.grid_rowconfigure(1, weight=1)

        sidebar.grid_columnconfigure(0, weight=1)

        left_line = ctk.CTkFrame(sidebar, width=0, fg_color='#7a7a7a', border_width=1)
        left_line.grid(row=0, rowspan=3, column=0, sticky='nws')

        preview_frame = ctk.CTkFrame(sidebar, height=150)
        preview_frame.grid(row=0, column=0, pady=4, padx=4, sticky='wen')

        buttons_frame = ctk.CTkFrame(sidebar, fg_color='transparent')
        buttons_frame.grid(row=1, column=0, pady=1, padx=1, sticky='wens')

        self.start_profile_btn = ctk.CTkButton(buttons_frame, text="Запустить профиль", fg_color='transparent', hover_color=("#a0a0a0", "#474747"), image=self.start_profile_ico, height=30, anchor='w', text_color=('black', 'white'), state='disabled', command=lambda: self.on_doubleclick(self.selected_profile.id))
        self.start_profile_btn.grid(sticky='wen', padx=5, pady=3)

        self.open_mods_btn = ctk.CTkButton(buttons_frame, text="Папка с модами", fg_color='transparent', hover_color=("#a0a0a0", "#474747"), image=self.mods_folder_ico, anchor='w', height=30, text_color=('black', 'white'), state='disabled', command=lambda: open_profile_mods_folder(Platform, self.selected_profile.id))
        self.open_mods_btn.grid(sticky='wen', padx=5, pady=3)

        self.set_icon_btn = ctk.CTkButton(buttons_frame, text="Сменить иконку", fg_color='transparent', hover_color=("#a0a0a0", "#474747"), image=self.settings_ico, anchor='w', height=30, text_color=('black', 'white'), state='disabled', command=lambda: self.set_icon_window())
        self.set_icon_btn.grid(sticky='wen', padx=5, pady=3)

        self.rename_profile_btn = ctk.CTkButton(buttons_frame, text="Переименовать", fg_color='transparent', hover_color=("#a0a0a0", "#474747"), image=self.settings_ico, anchor='w', height=30, text_color=('black', 'white'), state='disabled', command=lambda: self.rename_profile_window(self.selected_profile.id))
        self.rename_profile_btn.grid(sticky='wen', padx=5, pady=3)

        self.delete_profile_btn = ctk.CTkButton(buttons_frame, text="Удалить профиль", fg_color='transparent', hover_color=("#a0a0a0", "#474747"), image=self.delete_profile_ico, height=30, anchor='w', text_color=('black', 'white'), state='disabled', command=lambda: self.delete_profile_window_vanila(self.selected_profile.id))
        self.delete_profile_btn.grid(sticky='wen', padx=5, pady=3)

#        self.reset_session_btn = ctk.CTkButton(buttons_frame, text="Сбросить сессию\nна сайте EpicSUS", fg_color='transparent', hover_color=("#a0a0a0", "#474747"), image=self.settings_ico, height=30, anchor='w', text_color='red', command=lambda: self.delete_profile_window_vanila(self.selected_profile.id))
#        self.reset_session_btn.grid(sticky='wen', padx=5, pady=180)

        self.sidebar_buttons = [self.start_profile_btn, self.open_mods_btn, self.delete_profile_btn, self.set_icon_btn, self.rename_profile_btn]



    
    def create_profile_grid(self):
        # Основной контейнер для сетки профилей
        self.profile_container = ctk.CTkFrame(self, fg_color="transparent")
        self.profile_container.grid(row=1, column=0, sticky="nsew", padx=(0, 200))
        
        self.profile_container.grid_columnconfigure(0, weight=1)
        self.profile_container.grid_columnconfigure(1, weight=1)
        self.profile_container.grid_columnconfigure(2, weight=1)
        self.profile_container.grid_columnconfigure(3, weight=1)

        self.load_profiles()
    
    def load_profiles(self):
        parse_profiles_result = parse_profiles()
        for profile in profiles:
            print(profile)
            self.add_profile_to_grid(name=str(parse_profiles_result[profile]['name']), path2image=str(parse_profiles_result[profile]['path2image']), id=str(profile))

    def add_profile_to_grid(self, name, path2image, id):
        # Создаем фрейм профиля
        profile_frame = ctk.CTkFrame(self.profile_container, width=150, height=180, bg_color='transparent', fg_color='transparent')

        profile_frame.bind("<Button-1>", lambda event, n=name: self.on_singleclick(n)) #  lambda n=name:
        profile_frame.bind("<Double-Button-1>", lambda event, id=id: self.on_doubleclick(id)) # lambda n=name: 
        
        # Позиция в сетке
        row = len(self.profiles) // 4
        col = len(self.profiles) % 4
        
        profile_frame.grid(row=row, column=col, padx=10, pady=10)

        if path2image == "default":
            profile_img = self.profile_ico
        else:
            profile_img = ctk.CTkImage(light_image=Image.open(path2image), size=(100, 100))
        
        # Добавляем иконку
        img_label = ctk.CTkLabel(profile_frame, image=profile_img, text="")
        img_label.pack(pady=(10, 5), padx=1)

        img_label.bind("<Button-1>", lambda event, n=name: self.on_singleclick(n))
        img_label.bind("<Double-Button-1>", lambda event, id=id: self.on_doubleclick(id))
        
        # Добавляем имя
        name_label = ctk.CTkLabel(profile_frame, text=name)
        name_label.pack(pady=1)

        profile_frame.name = name # СсылОчко для того, чтобы мы смогли найти имя за пределами функции
        profile_frame.id = id
        profile_frame.image = img_label
        profile_frame.label = name_label
        
        # Сохраняем профиль
        self.profiles.append(profile_frame)
    
    def add_profile_window(self):
        add_profile_window = ctk.CTkToplevel(self)
        add_profile_window.geometry('300x200')
        add_profile_window.title("Добавить профиль")
        add_profile_window.attributes('-topmost', True)
        add_profile_window.resizable(False, False)
        # Костыль
        # add_profile_window.after(200, lambda: add_profile_window.iconbitmap("media/icons/ico/aydar-200x200-plus.ico"))

        if Platform == 'Windows':
            add_profile_window.iconbitmap("media/icons/ico/aydar-200x200-plus.ico")
        else:
            img = ImageTk.PhotoImage(Image.open("media/icons/png/aydar-200x200-plus.png"))
            add_profile_window.iconphoto(False, img)       
        
        # Поля для ввода
        name_label = ctk.CTkLabel(add_profile_window, text="Имя профиля:")
        name_label.pack(pady=5)

        name_entry = ctk.CTkEntry(add_profile_window)
        name_entry.pack(pady=1)

        wait_label = ctk.CTkLabel(add_profile_window, text="Пожалуйста, подождите")

        def on_close_warning():
            messagebox.showwarning('Ахтунг!', 'Пожалуйста, подождите до окончания загрузки профиля. Окно закроется автоматически, когда профиль загрузится.')
        
        # Кнопка сохранения
        def save_profile():
            name = name_entry.get()
            if name:
                self.add_profile_to_grid(name, 'default', f'apid{number_of_profiles + 1:03d}')
                wait_label.pack(pady=3)
                name_entry.configure(state='disabled')
                save_button.configure(state='disabled')
                add_profile_window.protocol('WM_DELETE_WINDOW', on_close_warning)

                create_profile(name, 'default', DownloadURL)
                add_profile_window.destroy()
        
        save_button = ctk.CTkButton(add_profile_window, text="Сохранить", anchor='center', command=lambda: threading.Thread(target=save_profile, daemon=True).start())
        save_button.pack(pady=5)
    
    def set_icon_window(self):
        file_types = [("Иконки", "*.png *.jpg *.jpeg *.gif")]
        filedialog = ctk.filedialog.askopenfile(mode='r', filetypes=file_types)
        if filedialog:
            save_chosen_icon(filedialog.name, self.selected_profile.id)

            image = ctk.CTkImage(light_image=Image.open(f'{filedialog.name}'), size=(100, 100))

            profile_image = self.selected_profile.image
            profile_image.configure(image=image)

    def delete_profile_window_vanila(self, profile):
        dialog_answer = messagebox.askyesno("Удаление профиля", "Вы уверены, что хотите удалить профиль?")
        if dialog_answer:
            self.selected_profile.destroy()
            self.profiles.remove(self.selected_profile)
            self.deactivate_sidebar_buttons()
            
            delete_profile(profile)
            self.selected_profile = None

    def rename_profile_window(self, profile):
        rename_profile_window = ctk.CTkToplevel(self)
        rename_profile_window.geometry('300x200')
        rename_profile_window.title("Переименовать профиль")
        rename_profile_window.attributes('-topmost', True)
        rename_profile_window.resizable(False, False)
        # Костыль
        # rename_profile_window.after(200, lambda: rename_profile_window.iconbitmap("media/icons/ico/aydar-200x200-plus.ico"))

        if Platform == 'Windows':
            rename_profile_window.iconbitmap("media/icons/ico/aydar-200x200-plus.ico")
        else:
            img = ImageTk.PhotoImage(Image.open("media/icons/png/aydar-200x200-plus.png"))
            rename_profile_window.iconphoto(False, img)
        
        # Поля для ввода
        name_label = ctk.CTkLabel(rename_profile_window, text="Новое имя профиля:")
        name_label.pack(pady=5)

        name_entry = ctk.CTkEntry(rename_profile_window)
        name_entry.pack(pady=1)

        wrong_name_label = ctk.CTkLabel(rename_profile_window, text="Пожалуйста, введите новое имя профиля.", text_color='red')

        def save_new_name():
            name = name_entry.get()
            if name:
                profile_label = self.selected_profile.label
                profile_label.configure(text=name)

                rename_profile(profile, name)
                rename_profile_window.destroy()
            else:
                wrong_name_label.pack(pady=3)

        save_button = ctk.CTkButton(rename_profile_window, text="Сохранить", anchor='center', command=lambda: save_new_name())
        save_button.pack(pady=5)


    # def delete_profile_window_custom(self):
    #     delete_profile_window = ctk.CTkToplevel(self)
    #     delete_profile_window.geometry('400x80')
    #     delete_profile_window.title("Удалить профиль")
    #     delete_profile_window.attributes('-topmost', True)
    #     # Костыль
    #     delete_profile_window.after(200, lambda: delete_profile_window.iconbitmap("media/icons/ico/aydar-200x200-plus.ico"))
        
    #     # Поля для ввода
    #     ctk.CTkLabel(delete_profile_window, text="Вы уверены, что хотите удалить профиль?").pack(pady=5)

    #     button_frame = ctk.CTkFrame(delete_profile_window)
    #     button_frame.pack(side="right", padx=20, pady=20)

    #     yes_button = ctk.CTkButton(button_frame, text="Да")
    #     yes_button.pack(side="left", padx=5)

    #     no_button = ctk.CTkButton(button_frame, text="Нет")
    #     no_button.pack(side="left", padx=5)

    def account_window(self):
        account_window = ctk.CTkToplevel(self)
        account_window.geometry('400x300')
        account_window.title("Аккаунт")
        account_window.attributes('-topmost', True)

        # Костыль
        # account_window.after(200, lambda: account_window.iconbitmap("media/icons/ico/aydar-200x200-plus.ico"))

        if Platform == 'Windows':
            account_window.iconbitmap("media/icons/ico/aydar-200x200-plus.ico")
        else:
            img = ImageTk.PhotoImage(Image.open("media/icons/png/aydar-200x200-plus.png"))
            account_window.iconphoto(False, img)

        if is_logined_already:
            pass
        else:
            ctk.CTkLabel(account_window, text="Войти", font=('Yu Gothic UI Light', 32)).pack(pady=10)   

            email_entry = ctk.CTkEntry(account_window, placeholder_text="Введите email")
            email_entry.pack(pady=5)

            pass_entry = ctk.CTkEntry(account_window, placeholder_text="Введите пароль")
            pass_entry.pack(pady=5)

            def prelogin():
                global is_logined_already

                email = email_entry.get()
                password = pass_entry.get()
                login_results = account_login(email, password)
                if login_results:
                    account_window.destroy()

                    self.account_btn.configure(text=login_results)
                    is_logined_already = True
                else:
                    wrong_login_label.pack(pady=5)
            

            login_btn = ctk.CTkButton(account_window, text="Войти", command=prelogin)
            login_btn.pack(pady=20)

            wrong_login_label = ctk.CTkLabel(account_window, text="Неверная почта или пароль", text_color='red')

    def on_singleclick(self, name):
    # Ну это штуко для того, чтобы когда вы кликали на профиль он выбирался и уро уро уро
        if self.selected_profile:
            self.selected_profile.configure(fg_color='transparent')
        
        for profile in self.profiles:
            if hasattr(profile, 'name') and profile.name == name:
                profile.configure(fg_color=("#cfcfcf", "#474747"))
                self.selected_profile = profile

                self.activate_sidebar_buttons()

                break

    def on_doubleclick(self, id):
        start_results = start_profile(Platform, id, ProtonFolder)
        if not start_results:
            messagebox.showerror('Ошибка', 'Проверьте целостность файлов профиля или наличие steam proton.')
    
    def activate_sidebar_buttons(self):
        # if self.start_profile_btn.cget('state') != 'normal':
        for button in self.sidebar_buttons:
            button.configure(state='normal')

    def deactivate_sidebar_buttons(self):
        # if self.start_profile_btn.cget('state') != 'disable':
        for button in self.sidebar_buttons:
            button.configure(state='disabled')


if __name__ == '__main__':
    multiprocessing.freeze_support()
    app = Aydar()
    app.mainloop()
