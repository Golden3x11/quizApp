from tkinter import *
from customtkinter import *
from tkinter.messagebox import *
import database_connection
import app


class RegisterGui(Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.geometry("{}x{}".format(320, 300))

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.frame = CTkFrame(self, fg_color='#FCF7FF')
        self.frame.grid(row=0, column=0, sticky="nswe", padx=15, pady=15)

        self.frame.rowconfigure(0, weight=10)
        self.frame.rowconfigure((1, 2, 3, 4), weight=1)
        self.frame.columnconfigure((0, 1), weight=1)
        self.title_label = CTkLabel(self.frame, text="Registration Form", text_font=(app.FONT, -25, 'bold'))
        self.title_label.grid(row=0, column=0, columnspan=2, padx=20, pady=5, sticky='nswe')

        self.login_entry = CTkEntry(self.frame, width=250, placeholder_text='login')
        self.login_entry.grid(row=1, column=0, columnspan=2, padx=20, pady=5, sticky='we')

        self.password_entry = CTkEntry(self.frame, width=250, placeholder_text='password', show='*')
        self.password_entry.grid(row=2, column=0, columnspan=2, padx=20, pady=5, sticky='we')

        self.confirm_password_entry = CTkEntry(self.frame, width=250, placeholder_text='confirm password', show='*')
        self.confirm_password_entry.grid(row=3, column=0, columnspan=2, padx=20, pady=5, sticky='we')

        self.login_button = CTkButton(self.frame, text='Register', command=self.register)
        self.login_button.grid(row=4, column=0, columnspan=2, padx=20, pady=20, sticky='nswe')

        self.bind('<Return>', lambda event: self.log_in())

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
            if database_connection.register(self.login_entry.get(), self.password_entry.get()):
                showinfo('Success', "Registration Successful")
                self.destroy()
            else:
                showerror('Error', 'User Already Exists')
                self.clear()
