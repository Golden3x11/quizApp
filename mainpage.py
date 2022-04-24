from tkinter import *
from tkinter.messagebox import *

import app


def login_window():
    root.destroy()
    import loginpage


def logout():
    app.user_logout()
    showinfo('Logout', 'You have been successfully logout')


# GUI
root = Tk()
root.geometry('900x600')
root.resizable(False, False)
root.title('Welcome')

frame = Frame(root, bg='white', width=560, height=320)
frame.place(x=180, y=140)

title_label = Label(frame, text="Welcome in Quiz App", font=('arial', 25, 'bold'), bg='white')
title_label.place(x=120, y=5)

if app.USER is None:
    login_button = Button(frame, text='Login', font=('arial', 18, 'bold'), bd=0, bg='gray20', fg='white',
                          command=login_window)
    login_button.place(x=240, y=240)
else:
    logout_button = Button(frame, text='Logout', font=('arial', 18, 'bold'), bd=0, bg='gray20', fg='white',
                           command=logout)
    logout_button.place(x=240, y=240)

root.mainloop()
