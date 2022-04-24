from tkinter import *
from tkinter.messagebox import *
import mysql.connector
from mysql.connector import Error
import app


def register_window():
    root.destroy()
    import registerpage


def main_window():
    root.destroy()
    import mainpage


def sign_in():
    if login_entry.get() == '' or password_entry.get() == '':
        showerror('Error', 'All Fields Are Required')
    else:
        try:
            connection = mysql.connector.connect(host='localhost', user='golden3x11', password='pass',
                                                 database='quizapp')
            if connection.is_connected():
                cursor = connection.cursor()
                query = 'select userlogin, pswd from users where userlogin=%s and pswd=MD5(%s)'
                cursor.execute(query, (login_entry.get(), password_entry.get()))
                if cursor.fetchone() is None:
                    showerror('Error', 'Invalid Login or Password')
                else:
                    app.userLogged(login_entry.get())
                    main_window()

        except Error as e:

            print("Error while connecting to MySQL", e)

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()


# GUI
root = Tk()
root.geometry("{}x{}+{}+{}".format(app.WIDTH, app.HEIGHT, app.POSITION_W, app.POSITION_H))
root.resizable(False, False)
root.title('Login Page')

frame = Frame(root, width=560, height=320, bg='white')
frame.place(x=180, y=140)

login_label = Label(frame, text="Login", font=(app.FONT, 22, 'bold'), bg='white')
login_label.place(x=220, y=30)
login_entry = Entry(frame, font=(app.FONT, 22), bg='white')
login_entry.place(x=220, y=70)

password_label = Label(frame, text="Password", font=(app.FONT, 22, 'bold'), bg='white')
password_label.place(x=220, y=120)
password_entry = Entry(frame, font=(app.FONT, 22), bg='white', show='*')
password_entry.place(x=220, y=160)

registration_button = Button(frame, text='Register New Account?', font=(app.FONT, 12), bd=0, bg='white',
                             activebackground='white', fg='red', command=register_window)
registration_button.place(x=220, y=200)

login_button = Button(frame, text='Login', font=(app.FONT, 18, 'bold'), bd=0, bg='gray20', fg='white', command=sign_in)
login_button.place(x=450, y=240)

root.mainloop()
