from tkinter import *
from tkinter.messagebox import *
import app
import loginpage
import quizpage
import rankingpage


class MainGUI:
    def __init__(self):
        MainGUI.WINDOW = self
        self.root = Tk()
        app.POSITION_W = int(self.root.winfo_screenwidth() / 2 - app.WIDTH / 2)
        app.POSITION_H = int(self.root.winfo_screenheight() / 2 - app.HEIGHT / 2)
        self.root.geometry("{}x{}+{}+{}".format(app.WIDTH, app.HEIGHT, app.POSITION_W, app.POSITION_H))
        self.root.resizable(False, False)
        self.root.title('Welcome')

        self.frame = Frame(self.root, bg='white', width=560, height=320)
        self.frame.place(x=180, y=140)

        self.title_label = Label(self.frame, text="Welcome in Quiz App", font=(app.FONT, 25, 'bold'), bg='white')
        self.title_label.place(x=280, y=20, anchor=CENTER)

        self.start_button = Button(self.frame, text='START', font=(app.FONT, 30, 'bold'), bd=0, bg='green', fg='white',
                                   command=self.start)
        self.start_button.place(x=280, y=150, anchor=CENTER)

        self.log_button = Button(self.frame, text='Login', font=(app.FONT, 18, 'bold'), bd=0, bg='gray20',
                                 fg='white',
                                 command=self.login_window)
        self.log_button.place(x=450, y=250)
        self.update_login_button()

        rank_button = Button(self.frame, text='Ranking', font=(app.FONT, 18, 'bold'), bd=0, bg='gray20', fg='white',
                             command=self.ranking_window)
        rank_button.place(x=35, y=250)

        self.root.mainloop()

    def logout(self):
        app.user_logout()
        showinfo('Logout', 'You have been successfully logout')
        self.update_login_button()

    def update_login_button(self):
        if app.is_user_logged():
            self.log_button['text'] = 'Logout'
            self.log_button['command'] = self.logout
        else:
            self.log_button['text'] = 'Login'
            self.log_button['command'] = self.login_window

    def login_window(self):
        loginpage.LoginGUI(self.update_login_button)

    @staticmethod
    def ranking_window():
        rankingpage.RankingGUI()

    def quiz_window(self):
        self.root.destroy()
        quizpage.QuizGUI()

    def start(self):
        if app.is_user_logged():
            self.quiz_window()
        else:
            showerror('Error', 'You need to be logged first')
            self.login_window()

# GUI
