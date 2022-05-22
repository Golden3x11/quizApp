import main_page
from customtkinter import *


class App(CTk):
    __USER = None
    FONT = 'Roboto Medium'
    WIDTH = 900
    HEIGHT = 650
    POSITION_W = 0
    POSITION_H = 0

    def __init__(self):
        super().__init__()
        set_appearance_mode('light')
        set_default_color_theme('dark-blue')

        self.title('Quiz App')
        App.POSITION_W = int(self.winfo_screenwidth() / 2 - App.WIDTH / 2)
        App.POSITION_H = int(self.winfo_screenheight() / 2 - App.HEIGHT / 2)
        self.geometry("{}x{}+{}+{}".format(App.WIDTH, App.HEIGHT, App.POSITION_W, App.POSITION_H))

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.frame = main_page.MainGui(self)

    @staticmethod
    def get_USER():
        return App.__USER

    @staticmethod
    def user_logged(id_u, login, score):
        App.__USER = User(id_u, login, score)

    @staticmethod
    def user_logout():
        App.__USER = None

    @staticmethod
    def is_user_logged():
        if App.__USER is None:
            return False
        else:
            return True


class User:
    def __init__(self, id_u, login, score):
        self.__id = id_u
        self.__login = login
        self.__best_score = score

    @property
    def id(self):
        return self.__id

    @property
    def login(self):
        return self.__login

    @property
    def best_score(self):
        return self.__best_score

    @best_score.setter
    def best_score(self, value):
        self.__best_score = value


if __name__ == '__main__':
    app = App()
    app.mainloop()
