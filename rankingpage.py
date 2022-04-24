from tkinter import *
from tkinter.ttk import Treeview, Style
import mysql.connector
from mysql.connector import Error
import app


def display_ranking(rank):
    columns = ('Place', 'Player', 'Score', 'Date')
    width = 100, 300, 100, 300
    style = Style()
    style.configure('Treeview.Heading', font=(app.FONT, 20))
    style.configure('Treeview', font=(app.FONT, 18), rowheigth=45)
    tree = Treeview(frame, columns=columns, show='headings')
    tree.place(x=0, y=60)

    for i, col in enumerate(columns):
        tree.column(col, width=width[i])
        tree.heading(col, text=col)

    for row in rank:
        tree.insert('', 'end', values=row)


def get_ranking(rank):
    try:
        connection = mysql.connector.connect(host='localhost', user='golden3x11', password='pass',
                                             database='quizapp')
        if connection.is_connected():
            cursor = connection.cursor()
            query = 'SELECT row_number() over () as nr, userlogin, score, dateTime FROM ranking ' \
                    'LEFT JOIN users u on u.idU = ranking.idU order by score DESC limit 10;'
            cursor.execute(query)
            for row in cursor:
                rank.append((row[0], row[1], row[2], str(row[3])))

    except Error as e:

        print("Error while connecting to MySQL", e)

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


# GUI
root = Tk()
root.geometry("{}x{}+{}+{}".format(800, app.HEIGHT, app.POSITION_W, app.POSITION_H))
root.resizable(False, False)
root.title('Ranking Page')

frame = Frame(root, width=800, height=600, bg='white')
frame.place(x=0, y=0)

login_label = Label(frame, text="Ranking TOP 10", font=(app.FONT, 35, 'bold'), bg='white')
login_label.place(x=400, y=20, anchor=CENTER)

ranking = []
get_ranking(ranking)
display_ranking(ranking)


root.mainloop()
