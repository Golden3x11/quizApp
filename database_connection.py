import mysql.connector
from mysql.connector import Error

import app


def update_best_result(user, score):
    try:
        connection = mysql.connector.connect(host='localhost', user='golden3x11', password='pass',
                                             database='quizapp')
        if connection.is_connected():
            cursor = connection.cursor()
            query = 'UPDATE quizapp.users t SET t.bestScore = %s WHERE t.idU = %s'
            cursor.execute(query, (score, user.id))
            connection.commit()

    except Error as e:

        print("Error while connecting to MySQL", e)

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def add_result_to_db(user, score):
    try:
        connection = mysql.connector.connect(host='localhost', user='golden3x11', password='pass',
                                             database='quizapp')
        if connection.is_connected():
            cursor = connection.cursor()
            query = 'insert into ranking(idU,score) values (%s, %s)'
            cursor.execute(query, (user.id, score))
            connection.commit()

    except Error as e:

        print("Error while connecting to MySQL", e)

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def get_ranking():
    rank = []
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

    return rank
