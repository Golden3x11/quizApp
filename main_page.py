from tkinter import *
from customtkinter import *
from tkinter.messagebox import *
import app
import login_page
import quiz_page
import rankingpage


class App(CTk):
    def __init__(self):
        super().__init__()
        set_appearance_mode('light')
        set_default_color_theme('dark-blue')

        self.title('Quiz App')
        app.POSITION_W = int(self.winfo_screenwidth() / 2 - app.WIDTH / 2)
        app.POSITION_H = int(self.winfo_screenheight() / 2 - app.HEIGHT / 2)
        self.geometry("{}x{}+{}+{}".format(app.WIDTH, app.HEIGHT, app.POSITION_W, app.POSITION_H))

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.frame = MainGui(self)


class MainGui(CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color='#FCF7FF')
        self.master = master
        self.rowconfigure(0, weight=10)
        self.rowconfigure(1, weight=10)
        self.rowconfigure(2, weight=1)
        self.columnconfigure((0, 2), weight=1)
        self.columnconfigure(1, weight=10)
        self.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)

        self.title_label = CTkLabel(self, text="Quiz App", text_font=('Impact', -200, 'bold'))
        self.title_label.grid(column=0, row=0,columnspan=3, sticky='n', pady=40, padx=20)

        self.start_button = CTkButton(self, text='START', command=self.start,
                                      fg_color=('#00C0A3', '#00C0A3'), text_font=(app.FONT, -80, 'bold'),
                                      hover_color=('#00896F', '#00896F'))
        self.start_button.grid(column=1, row=1, sticky='n', pady=20, padx=20)

        self.log_b_var = StringVar(self, 'Login')
        self.log_button = CTkButton(self, textvariable=self.log_b_var, command=self.login_window,
                                    text_font=(app.FONT, -30, 'bold'))
        self.log_button.grid(column=0, row=2, sticky='n', pady=20, padx=20)

        self.rank_button = CTkButton(self, text='Ranking', command=self.ranking_window,
                                     text_font=(app.FONT, -30, 'bold'))
        self.rank_button.grid(column=2, row=2, sticky='n', pady=20, padx=20)

    def logout(self):
        app.user_logout()
        showinfo('Logout', 'You have been successfully logout')
        self.update_login_button()

    def update_login_button(self):
        if app.is_user_logged():
            self.log_b_var.set('Logout')
            self.log_button.config(command=self.logout)
        else:
            self.log_b_var.set('Login')
            self.log_button.config(command=self.login_window)

    def login_window(self):
        login_page.LoginGUI(self, self.update_login_button)

    def ranking_window(self):
        rankingpage.RankingGUI(self.master)

    def quiz_window(self):
        frame = quiz_page.QuizPage(self.master)
        frame.tkraise()

    def start(self):
        if app.is_user_logged():
            self.quiz_window()
        else:
            showwarning('Warning', 'You need to be logged first')
            self.login_window()
