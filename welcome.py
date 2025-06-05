import customtkinter as ctk
from PIL import Image

class WelcomeSetup(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Настройки главного окна
        self.title("Добро пожаловать!")
        self.geometry("800x500")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.create_header()
        
        # Контейнер для слайдов
        self.slides_container = ctk.CTkFrame(self)
        self.slides_container.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
        self.slides_container.grid_columnconfigure(0, weight=1)
        self.slides_container.grid_rowconfigure(0, weight=1)
        
        # Создаем слайды
        self.slides = []
        self.current_slide = 0
        self.create_slides()
        
        # Кнопка "Далее" (в отдельном фрейме)
        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 20))
        self.button_frame.grid_columnconfigure(0, weight=1)
        
        self.next_btn = ctk.CTkButton(self.button_frame, text="Давайте", command=self.next_slide)
        self.next_btn.grid(row=0, column=0, pady=10)
        
        self.show_slide(0)
    
    def create_header(self):
        header = ctk.CTkFrame(self, height=80, corner_radius=0)
        header.grid(row=0, column=0, sticky="ew")
        header.grid_columnconfigure(0, weight=1)

        logo_img = ctk.CTkImage(light_image=Image.open("media/icons/png/aydar-140x45-white.png"), size=(140, 45))
        logo_label = ctk.CTkLabel(header, image=logo_img, text="")
        logo_label.grid(row=0, column=0, sticky="w", padx=20)

    def create_slides(self):
        # Слайд 1
        slide1 = ctk.CTkFrame(self.slides_container)
        slide1.grid_columnconfigure(0, weight=1)
        
        title1 = ctk.CTkLabel(slide1, text=" Добро пожаловать! ", font=('Yu Gothic UI Light', 64, 'italic'))
        title1.grid(row=0, column=0, pady=(40, 20))
        
        text1 = ctk.CTkLabel(slide1, text="Давайте настроим ваш новый Aydar.", font=("Arial", 16))
        text1.grid(row=1, column=0, pady=(0, 40))
        
        self.slides.append(slide1)
        

        # Слайд 2
        slide2 = ctk.CTkFrame(self.slides_container)
        slide2.grid_columnconfigure(0, weight=1)
        
        label2 = ctk.CTkLabel(slide2, text="Как вас зовут?", font=("Yu Gothic UI Light", 48))
        label2.grid(row=0, column=0, sticky="n", pady=5)

        entry2 = ctk.CTkEntry(slide2, placeholder_text="Введите имя")
        entry2.grid(row=0, column=0, pady=150, ipadx=50, ipady=5, sticky='n', padx=20)
        
        logo_user = ctk.CTkImage(light_image=Image.open("media/icons/png/aydar-200x200-user.png"), size=(200, 200))
        logo_user_label = ctk.CTkLabel(slide2, image=logo_user, text="")
        logo_user_label.grid(row=0, column=0, sticky="nw", padx=30, pady=90)

        self.slides.append(slide2)
        

        # Слайд 3
        slide3 = ctk.CTkFrame(self.slides_container)
        slide3.grid_columnconfigure(0, weight=1)
        
        label3 = ctk.CTkLabel(slide3, text="Какая тема вам лучше?", font=("Yu Gothic UI Light", 48))
        label3.grid(row=0, column=0, sticky="n", pady=5)
        
        # entry3 = ctk.CTkEntry(slide3, placeholder_text="Введите что-нибудь")
        # entry3.grid(row=0, column=0, pady=150, ipadx=50, ipady=5, sticky='n', padx=20)
        
        choicethememenu = ctk.CTkOptionMenu(slide3, values=['Тёмная', 'Светлая'])
        choicethememenu.grid(row=0, column=0, pady=150, ipadx=50, ipady=5, sticky='n', padx=20)
        choicethememenu.set('Тёмная')

        self.slides.append(slide3)
    
    def show_slide(self, slide_index):
        # Скрываем все слайды
        for slide in self.slides:
            slide.grid_forget()
        
        # Показываем нужный слайд
        self.slides[slide_index].grid(row=0, column=0, sticky="nsew")
        
        # Обновляем текст кнопки
        btn_texts = ["Давайте", "Далее", "Завершить"]
        self.next_btn.configure(text=btn_texts[slide_index])
    
    def next_slide(self):
        self.current_slide += 1
        
        if self.current_slide >= len(self.slides):
            self.destroy()
            return
        
        self.show_slide(self.current_slide)

if __name__ == "__main__":
    app = WelcomeSetup()
    app.mainloop()
