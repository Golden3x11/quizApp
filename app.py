
FONT = 'arial'
WIDTH = 900
HEIGHT = 600
POSITION_W = 0
POSITION_H = 0

USER = None


def user_logged(login):
    global USER
    USER = User(login)


def user_logout():
    global USER
    USER = None


def is_user_logged():
    if USER is None:
        return False
    else:
        return True


class User:
    def __init__(self, login):
        self.login = login


if __name__ == '__main__':
    import mainpage
