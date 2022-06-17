from sqlalchemy.orm import sessionmaker
from db import engine, User, Rank
from hashlib import md5


class DAO:  # data access object
    Session = sessionmaker(bind=engine)

    def create_session(self):
        session = DAO.Session()
        return session

    def add(self, value, session=None):
        if session is None:
            session = self.create_session()

        session.add(value)
        session.commit()

    # get record from given table by given condition
    def get(self, obj, condition, session=None):
        # check if session is given
        flag = session is None
        if session is None:
            session = self.create_session()

        result = session.query(obj).filter(condition).first()

        # if session created upper not commit
        if not flag:
            session.commit()

        return result


class DBServices:
    def __init__(self):
        self.__dao = DAO()

    def login(self, login, password):
        result = []
        user = self.__dao.get(User, User.login == login)
        if md5(password.encode()).hexdigest() == user.password:
            result = [user.id, user.login, user.best_score]

        return result

    def register(self, login, password):
        success = False
        user = self.__dao.get(User, User.login == login)
        if user is None:
            user = User(login, md5(password.encode()).hexdigest())
            self.__dao.add(user)
            success = True
        return success

    def update_best_result(self, user, score):
        session = self.__dao.create_session()
        user = self.__dao.get(User, User.id == user.id, session=session)
        user.best_score = score
        session.flush()
        session.commit()

    def add_result_to_db(self, user, score):
        self.__dao.add(Rank(user.id, score))

    def get_ranking(self):
        session = self.__dao.create_session()
        result = session.query(User, Rank) \
            .filter(User.id == Rank.id_U) \
            .order_by(-Rank.score).limit(10).all()
        data = [(u.id, u.login, r.score, r.date) for u, r in result]
        return data
