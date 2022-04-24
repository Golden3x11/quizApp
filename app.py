
FONT = 'arial'
USER = None


def user_logged(login):
    global USER
    USER = User(login)


def user_logout(login):
    global USER
    USER = None


class User:
    def __init__(self, login):
        self.login = login
