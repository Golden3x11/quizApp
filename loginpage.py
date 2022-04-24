from tkinter import *
from tkinter.messagebox import *
import mysql.connector
from mysql.connector import Error
import app
import mainpage
import rankingpage
import registerpage


class LoginGUI:
    def __init__(self, refreshMain):
        self.refreshMain = refreshMain
        self.root = Tk()
        self.root.geometry("{}x{}".format(app.WIDTH, app.HEIGHT))
        self.root.resizable(False, False)
        self.root.title('Login Page')

        self.frame = Frame(self.root, width=560, height=320, bg='white')
        self.frame.place(x=180, y=140)

        self.login_label = Label(self.frame, text="Login", font=(app.FONT, 22, 'bold'), bg='white')
        self.login_label.place(x=220, y=30)
        self.login_entry = Entry(self.frame, font=(app.FONT, 22), bg='white')
        self.login_entry.place(x=220, y=70)

        self.password_label = Label(self.frame, text="Password", font=(app.FONT, 22, 'bold'), bg='white')
        self.password_label.place(x=220, y=120)
        self.password_entry = Entry(self.frame, font=(app.FONT, 22), bg='white', show='*')
        self.password_entry.place(x=220, y=160)

        self.registration_button = Button(self.frame, text='Register New Account?', font=(app.FONT, 12), bd=0,
                                          bg='white',
                                          activebackground='white', fg='red', command=self.register_window)
        self.registration_button.place(x=220, y=200)

        self.login_button = Button(self.frame, text='Login', font=(app.FONT, 18, 'bold'), bd=0, bg='gray20', fg='white',
                                   command=self.log_in)
        self.login_button.place(x=450, y=240)

        self.root.mainloop()

    def register_window(self):
        self.root.destroy()
        registerpage.RegisterGUI()

    def close_window(self):
        self.root.destroy()
        self.refreshMain()

    def log_in(self):
        if self.login_entry.get() == '' or self.password_entry.get() == '':
            showerror('Error', 'All Fields Are Required')
        else:
            try:
                connection = mysql.connector.connect(host='localhost', user='golden3x11', password='pass',
                                                     database='quizapp')
                if connection.is_connected():
                    cursor = connection.cursor()
                    query = 'select idU, userlogin, pswd, bestScore from users where userlogin=%s and pswd=MD5(%s)'
                    cursor.execute(query, (self.login_entry.get(), self.password_entry.get()))
                    data = cursor.fetchall()
                    if not data:
                        showerror('Error', 'Invalid Login or Password')
                    else:
                        for row in data:
                            app.user_logged(row[0], row[1], row[3])
                            self.close_window()

            except Error as e:

                print("Error while connecting to MySQL", e)

            finally:
                if connection.is_connected():
                    cursor.close()
                    connection.close()
