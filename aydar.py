import customtkinter as ctk
import webview
from PIL import Image
from utils.config_parser import UserName, isWelcomeWorked, UserTheme
from utils.profile_parser import parse_profiles, sections, create_profile, delete_profile
import os

# My fellow brothers, I, Billy Herrington, stand here today...

class Aydar(ctk.CTk):
    def __init__(self):
        super().__init__()

        if isWelcomeWorked == False:
            try:
                os.startfile("welcome.exe")
                os._exit(os.EX_OK)
            except:
                print("Welcome not found!")

        try:
            os.startfile("updater.exe")
        except:
            print("Updater not found!")

        # Настройка окна
        self.title(f"Привет, {UserName}! Чем займёмся сегодня?")
        self.geometry("800x600")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.iconbitmap("media/icons/ico/aydar-200x200-user.ico")

        ctk.set_appearance_mode(UserTheme)

        self.profiles = []
        self.selected_profiles = {}

        self.create_header()
        self.create_sidebar()
        self.create_profile_grid()

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
        self.settings_ico = ''
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

        accounts_button = ctk.CTkButton(header, text="Аккаунт", fg_color='transparent', hover_color=("#a0a0a0", "#474747"), image=self.account_ico, width=90, text_color=('black', 'white')) # hover_color='#474747', 
        accounts_button.grid(row=0, column=2, sticky="e", pady=3, padx=3)

        add_profile_button = ctk.CTkButton(header, text="Добавить профиль", fg_color='transparent', hover_color=("#a0a0a0", "#474747"), image=self.add_profile_ico, text_color=('black', 'white'), command=self.add_profile_window)
        add_profile_button.grid(row=0, column=0, sticky='w', pady=3, padx=3)
    
    def create_sidebar(self):
        # Боковая панель справа
        sidebar = ctk.CTkFrame(self, width=200, border_width=0, corner_radius=0) # fg_color='#323232', 
        sidebar.grid(row=1, column=0, sticky='nes')
        sidebar.grid_propagate(False)

        sidebar.grid_rowconfigure(0, weight=1)
        sidebar.grid_rowconfigure(1, weight=1)
        sidebar.grid_rowconfigure(2, weight=1)

        left_line = ctk.CTkFrame(sidebar, width=0, fg_color='#7a7a7a', border_width=1)
        left_line.grid(row=0, rowspan=3, column=1, sticky='nws')

        # start_profile_btn = ctk.CTkButton(sidebar, width=20, height=30, command=)
        # start_profile_btn.grid(row=1, column=2, sticky='e')
    
    def create_profile_grid(self):
        # Основной контейнер для сетки профилей
        self.profile_container = ctk.CTkFrame(self, fg_color="transparent")
        self.profile_container.grid(row=1, column=0, sticky="nsew", padx=(0, 200))  # Учитываем ширину sidebar
        
        # Настройка сетки (4 колонки)
        for i in range(4):
            self.profile_container.grid_columnconfigure(i, weight=1)
        
        # Начальные профили (можно загрузить из конфига)
        self.load_sample_profiles()
    
    def load_sample_profiles(self):
        parse_profiles_result = parse_profiles()
        for profile in sections:
            self.add_profile_to_grid(profile, path2image=str(parse_profiles_result[profile]['path2image']))

    def add_profile_to_grid(self, name, path2image):
        # Создаем фрейм профиля
        profile_frame = ctk.CTkFrame(self.profile_container, width=150, height=180, bg_color='transparent', fg_color='transparent')

        profile_frame.bind("<Double-Button-1>", self.on_doubleclick)
        
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
        img_label.pack(pady=(10, 5))

        img_label.bind("<Double-Button-1>", lambda event: self.on_doubleclick(name=name))
        
        # Добавляем имя
        name_label = ctk.CTkLabel(profile_frame, text=name)
        name_label.pack()
        
        # Сохраняем профиль
        self.profiles.append(profile_frame)
    
    def add_profile_window(self):
        add_profile_window = ctk.CTkToplevel(self)
        add_profile_window.geometry('400x300')
        add_profile_window.title("Добавить профиль")
        # Костыль
        add_profile_window.after(200, lambda: add_profile_window.iconbitmap("media/icons/ico/aydar-200x200-plus.ico"))
        
        # Поля для ввода
        ctk.CTkLabel(add_profile_window, text="Имя профиля:").pack(pady=5)
        name_entry = ctk.CTkEntry(add_profile_window)
        name_entry.pack(pady=5)
        
        # Кнопка сохранения
        def save_profile():
            name = name_entry.get()
            if name:
                self.add_profile_to_grid(name, 'default')
                create_profile(name, 'default')
                add_profile_window.destroy()
        
        ctk.CTkButton(add_profile_window, text="Сохранить", command=save_profile).pack(pady=20)

    def on_oneclick(self, name):
        pass

    def on_doubleclick(self, name):
        # event.widget.config(bg="lightgreen")
        os.startfile(f'profiles\\{name}\\Яйцеоды 2.exe')


if __name__ == '__main__':
    app = Aydar()
    app.mainloop()