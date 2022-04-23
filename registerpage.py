from tkinter import *
from tkinter.messagebox import *
import mysql.connector
from mysql.connector import Error


# Functions
def clear():
    password_entry.delete(0, END)
    login_entry.delete(0, END)
    confirm_password_entry.delete(0, END)


def register():
    if login_entry.get() == '' or password_entry.get() == '' or confirm_password_entry.get() == '':
        showerror('Error', 'All Fields Are Required')

    elif password_entry.get() != confirm_password_entry.get():
        showerror('Error', 'Password Mismatch')

    else:
        success = False
        try:
            connection = mysql.connector.connect(host='localhost', user='golden3x11', password='pass',
                                                 database='quizapp')
            if connection.is_connected():
                cursor = connection.cursor()
                query = 'select * from users where userlogin=%s'
                cursor.execute(query, (login_entry.get(),))
                if cursor.fetchone() is not None:
                    showerror('Error', 'User Already Exists')
                else:
                    query = 'insert into users (userlogin, pswd) values (%s, MD5(%s))'
                    cursor.execute(query, (login_entry.get(), password_entry.get()))
                    connection.commit()
                    showinfo('Success', "Registration Successful")
                    success = True
                    clear()

        except Error as e:
            print("Error while connecting to MySQL", e)

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
        if success:
            root.destroy()
            import mainpage


# GUI
root = Tk()
root.geometry('900x600')
root.resizable(False, False)
root.title('Registration Page')


frame = Frame(root, bg='white', width=560, height=320)
frame.place(x=180, y=140)

title_label = Label(frame, text="Registration Form", font=('arial', 22, 'bold'), bg='white')
title_label.place(x=150, y=5)

login_label = Label(frame, text='Login', font=('arial', 18, 'bold'), bg='white',
                    fg='gray20', )
login_label.place(x=20, y=80)
login_entry = Entry(frame, font=('arial', 18), bg='lightgray')
login_entry.place(x=20, y=115, width=250)

password_label = Label(frame, text='Password', font=('arial', 18, 'bold'), bg='white', fg='gray20', )
password_label.place(x=20, y=150)
password_entry = Entry(frame, font=('arial', 18), bg='lightgray', show='*')
password_entry.place(x=20, y=185, width=250)

c_password_label = Label(frame, text='Confirm Password', font=('arial', 18, 'bold'), bg='white', fg='gray20')
c_password_label.place(x=20, y=220)
confirm_password_entry = Entry(frame, font=('arial', 18), bg='lightgray', show='*')
confirm_password_entry.place(x=20, y=255, width=250)

register_button = Button(frame, text='Register', font=('arial', 18, 'bold'), bd=0, bg='gray20', fg='white',
                         command=register)
register_button.place(x=350, y=175)

root.mainloop()
