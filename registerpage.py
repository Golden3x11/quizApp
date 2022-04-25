from tkinter import *
from tkinter.messagebox import *
import mysql.connector
from mysql.connector import Error
import app


class RegisterGUI:
    def __init__(self):
        self.root = Tk()
        self.root.geometry("{}x{}".format(app.WIDTH, app.HEIGHT))
        self.root.resizable(False, False)
        self.root.title('Registration Page')

        self.frame = Frame(self.root, bg='white', width=560, height=320)
        self.frame.place(x=180, y=140)

        self.title_label = Label(self.frame, text="Registration Form", font=(app.FONT, 22, 'bold'), bg='white')
        self.title_label.place(x=150, y=5)

        self.login_label = Label(self.frame, text='Login', font=(app.FONT, 18, 'bold'), bg='white',
                                 fg='gray20', )
        self.login_label.place(x=20, y=80)
        self.login_entry = Entry(self.frame, font=(app.FONT, 18), bg='lightgray')
        self.login_entry.place(x=20, y=115, width=250)

        self.password_label = Label(self.frame, text='Password', font=(app.FONT, 18, 'bold'), bg='white', fg='gray20', )
        self.password_label.place(x=20, y=150)
        self.password_entry = Entry(self.frame, font=(app.FONT, 18), bg='lightgray', show='*')
        self.password_entry.place(x=20, y=185, width=250)

        self.c_password_label = Label(self.frame, text='Confirm Password', font=(app.FONT, 18, 'bold'), bg='white',
                                      fg='gray20')
        self.c_password_label.place(x=20, y=220)
        self.confirm_password_entry = Entry(self.frame, font=(app.FONT, 18), bg='lightgray', show='*')
        self.confirm_password_entry.place(x=20, y=255, width=250)

        self.register_button = Button(self.frame, text='Register', font=(app.FONT, 18, 'bold'), bd=0, bg='gray20',
                                      fg='white',
                                      command=self.register)
        self.register_button.place(x=350, y=175)

        self.root.bind('<Return>', lambda event: self.register())

        self.root.mainloop()

    def clear(self):
        self.password_entry.delete(0, END)
        self.login_entry.delete(0, END)
        self.confirm_password_entry.delete(0, END)

    def register(self):
        if self.login_entry.get() == '' or self.password_entry.get() == '' or self.confirm_password_entry.get() == '':
            showerror('Error', 'All Fields Are Required')

        elif self.password_entry.get() != self.confirm_password_entry.get():
            showerror('Error', 'Password Mismatch')

        else:
            success = False
            try:
                connection = mysql.connector.connect(host='localhost', user='golden3x11', password='pass',
                                                     database='quizapp')
                if connection.is_connected():
                    cursor = connection.cursor()
                    query = 'select * from users where userlogin=%s'
                    cursor.execute(query, (self.login_entry.get(),))
                    if cursor.fetchone() is not None:
                        showerror('Error', 'User Already Exists')
                    else:
                        query = 'insert into users (userlogin, pswd) values (%s, MD5(%s))'
                        cursor.execute(query, (self.login_entry.get(), self.password_entry.get()))
                        connection.commit()
                        showinfo('Success', "Registration Successful")
                        success = True
                        self.clear()

            except Error as e:
                print("Error while connecting to MySQL", e)

            finally:
                if connection.is_connected():
                    cursor.close()
                    connection.close()
            if success:
                self.root.destroy()
