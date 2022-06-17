import mysql.connector
from mysql.connector import Error


# not orm database connection not used

class Database:
    def __init__(self):
        try:
            self._conn = mysql.connector.connect(host='localhost', user='golden3x11', password='pass',
                                                 database='quizapp')
            self._cursor = self._conn.cursor()
        except Error as e:
            raise ConnectionError('Error while connecting to MySQL', e)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._close()

    @property
    def _connection(self):
        return self._conn

    def _commit(self):
        self._connection.commit()

    def _close(self, commit=True):
        if commit:
            self._commit()
        self._connection.close()

    def _execute(self, sql, params=None):
        self._cursor.execute(sql, params or ())

    def _fetchall(self):
        return self._cursor.fetchall()

    def _query(self, sql, params=None):
        self._cursor.execute(sql, params or ())
        return self._fetchall()

    def login(self, login, password):
        result = []
        try:
            if self._connection.is_connected():
                query = 'select idU, userlogin, bestScore from users where userlogin=%s and pswd=MD5(%s)'
                data = self._query(query, (login, password))
                if not data:
                    result = []
                else:
                    for row in data:
                        result = [row[0], row[1], row[2]]
        except Error as e:
            raise ConnectionError('Error while connecting to MySQL', e)
        return result

    def update_best_result(self, user, score):
        try:
            if self._connection.is_connected():
                query = 'UPDATE quizapp.users t SET t.bestScore = %s WHERE t.idU = %s'
                self._query(query, (score, user.id))
                self._commit()
        except Error as e:
            raise ConnectionError('Error while connecting to MySQL', e)

    def add_result_to_db(self, user, score):
        try:
            if self._connection.is_connected():
                query = 'insert into ranking(idU,score) values (%s, %s)'
                self._query(query, (user.id, score))
                self._commit()
        except Error as e:
            raise ConnectionError('Error while connecting to MySQL', e)

    def get_ranking(self):
        rank = []
        try:
            if self._connection.is_connected():
                query = 'SELECT row_number() over () as nr, userlogin, score, dateTime FROM ranking ' \
                        'LEFT JOIN users u on u.idU = ranking.idU order by score DESC limit 10;'
                data = self._query(query)
                for row in data:
                    rank.append((row[0], row[1], row[2], str(row[3])))

        except Error as e:
            raise ConnectionError('Error while connecting to MySQL', e)

        return rank

    def register(self, login, password):
        success = False
        try:
            if self._connection.is_connected():
                query = 'select * from users where userlogin=%s'
                data = self._query(query, (login,))
                data
                if data:
                    success = False
                else:
                    query = 'insert into users (userlogin, pswd) values (%s, MD5(%s))'
                    self._query(query, (login, password))
                    self._commit()
                    success = True

        except Error as e:
            raise ConnectionError('Error while connecting to MySQL', e)

        return success
