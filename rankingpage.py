from tkinter import *
from tkinter.messagebox import showerror
from tkinter.ttk import Treeview, Style
from customtkinter import *
import app


class RankingGUI(Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.geometry("{}x{}".format(900, 400))

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.frame = CTkFrame(self, fg_color='#EEFBFA')
        self.frame.grid(row=0, column=0, sticky="nswe", padx=15, pady=15)

        self.frame.rowconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=1)
        self.frame.columnconfigure((0, 1), weight=1)
        self.rank_label = CTkLabel(self.frame, text="Ranking TOP 10", text_font=(app.App.FONT, -30, 'bold'))
        self.rank_label.grid(row=0, column=0, columnspan=2, padx=20, pady=5, sticky='nswe')
        try:
            db = app.App.get_db()
            self.ranking = db.get_ranking()
            self.display_ranking()
        except ConnectionError:
            showerror('Error', 'No data base Connection')

    def display_ranking(self):
        columns = ('Place', 'Player', 'Score', 'Date')
        width = 100, 300, 100, 300  # width of columns
        style = Style()
        style.theme_use('clam')
        style.configure('Treeview.Heading', font=(app.App.FONT, 20))  # columns font
        style.configure('Treeview', font=(app.App.FONT, 12), )  # rows font
        tree = Treeview(self.frame, columns=columns, show='headings')
        tree.grid(row=1, column=0, columnspan=2, padx=20, pady=5, sticky='nswe')

        for i, col in enumerate(columns):
            tree.column(col, width=width[i], anchor=CENTER)
            tree.heading(col, text=col)

        for row in self.ranking:
            tree.insert('', 'end', values=row)  # add values to tree(table)
