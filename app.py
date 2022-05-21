import main_page

FONT = 'Roboto Medium'
WIDTH = 900
HEIGHT = 600
POSITION_W = 0
POSITION_H = 0

USER = None


def user_logged(id_u, login, score):
    global USER
    USER = User(id_u, login, score)


def user_logout():
    global USER
    USER = None


def is_user_logged():
    if USER is None:
        return False
    else:
        return True


class User:
    def __init__(self, id_u, login, score):
        self.id = id_u
        self.login = login
        self.best_score = score


if __name__ == '__main__':
    app = main_page.MainGui()
    app.mainloop()
