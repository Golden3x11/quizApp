from tkinter import *
from tkinter.messagebox import *
import app


def login_window():
    root.destroy()
    import loginpage


def ranking_window():
    import rankingpage


def quiz_window():
    root.destroy()
    import quizpage


def logout():
    app.user_logout()
    showinfo('Logout', 'You have been successfully logout')


def start():
    if app.is_user_logged():
        quiz_window()
    else:
        showerror('Error', 'You need to be logged first')
        login_window()


# GUI
root = Tk()
app.POSITION_W = int(root.winfo_screenwidth()/2 - app.WIDTH/2)
app.POSITION_H = int(root.winfo_screenheight()/2 - app.HEIGHT/2)
root.geometry("{}x{}+{}+{}".format(app.WIDTH, app.HEIGHT, app.POSITION_W, app.POSITION_H))
root.resizable(False, False)
root.title('Welcome')

frame = Frame(root, bg='white', width=560, height=320)
frame.place(x=180, y=140)

title_label = Label(frame, text="Welcome in Quiz App", font=(app.FONT, 25, 'bold'), bg='white')
title_label.place(x=280, y=20, anchor=CENTER)

start_button = Button(frame, text='START', font=(app.FONT, 30, 'bold'), bd=0, bg='green', fg='white',
                      command=start)
start_button.place(x=280, y=150, anchor=CENTER)

if not app.is_user_logged():
    login_button = Button(frame, text='Login', font=(app.FONT, 18, 'bold'), bd=0, bg='gray20', fg='white',
                          command=login_window)
    login_button.place(x=450, y=250)
else:
    logout_button = Button(frame, text='Logout', font=(app.FONT, 18, 'bold'), bd=0, bg='gray20', fg='white',
                           command=logout)
    logout_button.place(x=450, y=250)

rank_button = Button(frame, text='Ranking', font=(app.FONT, 18, 'bold'), bd=0, bg='gray20', fg='white',
                     command=ranking_window)
rank_button.place(x=35, y=250)

root.mainloop()
