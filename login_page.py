from tkinter import *
from customtkinter import *
from tkinter.messagebox import *
import database_connection
import register_page
import app


class LoginGUI(Toplevel):
    def __init__(self, master, refreshMain):
        super().__init__(master)
        self.master = master
        self.refreshMain = refreshMain  # function that update button when loging is successful
        self.geometry("{}x{}".format(320, 300))

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.frame = CTkFrame(self, fg_color='#EEFBFA')
        self.frame.grid(row=0, column=0, sticky="nswe", padx=15, pady=15)

        self.frame.rowconfigure(0, weight=10)
        self.frame.rowconfigure((1, 2, 3, 4), weight=1)
        self.frame.columnconfigure((0, 1), weight=1)
        self.title_label = CTkLabel(self.frame, text="Log in", text_font=(app.App.FONT, -25, 'bold'))
        self.title_label.grid(row=0, column=0, columnspan=2, padx=20, pady=5, sticky='nswe')

        self.login_entry = CTkEntry(self.frame, width=250, placeholder_text='login')
        self.login_entry.grid(row=1, column=0, columnspan=2, padx=20, pady=5, sticky='we')

        self.password_entry = CTkEntry(self.frame, width=250, placeholder_text='password', show='*')
        self.password_entry.grid(row=2, column=0, columnspan=2, padx=20, pady=5, sticky='we')

        self.registration_button = CTkButton(self.frame, text='register New Account?',
                                             borderwidth=0, fg_color=None, hover_color=None,
                                             command=self.register_window)
        self.registration_button.grid(row=3, column=1, padx=20, pady=5, sticky='nswe')

        self.login_button = CTkButton(self.frame, text='Log in', command=self.log_in, fg_color='#2EC4B6')
        self.login_button.grid(row=4, column=0, columnspan=2, padx=20, pady=20, sticky='nswe')

        self.bind('<Return>', lambda event: self.log_in())

    def register_window(self):  # create TopLevel window with register functionality
        self.destroy()
        register_page.RegisterGui(master=self.master)

    def close_window(self):
        self.destroy()
        self.refreshMain()

    def log_in(self):
        if self.login_entry.get() == '' or self.password_entry.get() == '':
            showerror('Error', 'All Fields Are Required')
            self.destroy()
        else:
            try:
                result = database_connection.log_in(self.login_entry.get(), self.password_entry.get())
                if not result:
                    showerror('Error', 'Invalid Login or Password')
                else:   # successful log in
                    self.close_window()
            except ConnectionError:
                showerror('Error', 'No data base Connection')

