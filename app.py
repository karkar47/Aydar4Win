import customtkinter as ctk
from PIL import Image

class Aydar(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Настройка окна
        self.title("Сигма. Гойда. Скибиди.")
        self.geometry("800x600")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        ctk.set_appearance_mode("Light")

        self.create_header()
        self.create_sidebar()

    def create_header(self):
        # Хедер
        header = ctk.CTkFrame(self, height=40, border_width=0, corner_radius=0) # fg_color='#323232', 
        header.grid(row=0, column=0, sticky="ew")
        header.grid_propagate(False)

        header.grid_columnconfigure(0, weight=1)
        header.grid_columnconfigure(1, weight=1)
        header.grid_columnconfigure(2, weight=1)

        # Иконачке
        account_ico = ctk.CTkImage(light_image=Image.open("media/icons/png/aydar-200x200-user.png"), size=(25, 25))
        # add_profile_ico = ctk.CTkImage(light_image=Image.open("media/icons/"))
        settings_ico = ''
        reference_ico = ''

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

        accounts_button = ctk.CTkButton(header, text="Аккаунт", fg_color='transparent', hover_color=("#a0a0a0", "#474747"), image=account_ico, width=90, text_color=('black', 'white')) # hover_color='#474747', 
        accounts_button.grid(row=0, column=2, sticky="e", pady=3, padx=3)

        add_profile_button = ctk.CTkButton(header, text="Добавить профиль", fg_color='transparent', hover_color=("#a0a0a0", "#474747"), text_color=('black', 'white'))
        add_profile_button.grid(row=0, column=0, sticky='w', pady=3, padx=3)
    
    def create_sidebar(self):
        # Боковая панель справа
        sidebar = ctk.CTkFrame(self, width=100, border_width=0, corner_radius=0) # fg_color='#323232', 
        sidebar.grid(row=1, column=0, sticky='nes')


if __name__ == '__main__':
    app = Aydar()
    app.mainloop()