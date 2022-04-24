from tkinter import *
from tkinter.ttk import Treeview, Style
import app
import database_connection


class RankingGUI:
    def __init__(self):
        self.tree = None
        self.root = Tk()
        self.root.geometry("{}x{}".format(800, app.HEIGHT))
        self.root.resizable(False, False)
        self.root.title('Ranking Page')

        self.frame = Frame(self.root, width=800, height=600, bg='white')
        self.frame.place(x=0, y=0)

        self.login_label = Label(self.frame, text="Ranking TOP 10", font=(app.FONT, 35, 'bold'), bg='white')
        self.login_label.place(x=400, y=20, anchor=CENTER)

        self.ranking = database_connection.get_ranking()
        self.display_ranking()

        self.root.mainloop()

    def display_ranking(self):
        columns = ('Place', 'Player', 'Score', 'Date')
        width = 100, 300, 100, 300
        # style = Style()
        # style.configure('Treeview.Heading', font=(app.FONT, 20))
        # style.configure('Treeview', font=(app.FONT, 18), rowheigth=45)
        tree = Treeview(self.frame, columns=columns, show='headings')
        tree.place(x=0, y=60)

        for i, col in enumerate(columns):
            tree.column(col, width=width[i])
            tree.heading(col, text=col)

        for row in self.ranking:
            tree.insert('', 'end', values=row)
