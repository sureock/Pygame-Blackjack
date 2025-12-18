"""Модуль для работы с базой данных на основе библиотеки sqlalchemy."""
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import DeclarativeBase, sessionmaker


engine = create_engine("sqlite:///game.db", echo=False)


class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(100), nullable=False)

class Score(Base):
    __tablename__ = "scores"

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    win = Column(Integer, default=0)
    lose = Column(Integer, default=0)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

class Auth:
    def __init__(self, user, password):
        self.user = user
        self.password = password

    def login(self):
        session = Session()

        user = session.query(User).filter_by(username = self.user).first()

        if not user:
            session.close()
            return f"Пользователь не найден", False
        else:
            if user.password != self.password:
                session.close()
                return f"Пароль не верный!", False
            else:
                return f"Авторизация прошла успешно", True

    def regist(self):
        session = Session()

        send, key = self.login()
        if send == "Пользователь не найден":
            user = User(username = self.user, password = self.password)
            session.add(user)
            session.commit()
            session.close()
            return f"Пользователь успешно создан", True
        else:
            return f"Пользователь с таким именем уже существует", False

    def del_user(self):
        session = Session()

        send, key = self.login()
        if send == "Авторизация прошла успешно":
            user = User(username = self.user, password = self.password)
            session.delete(user)
            session.commit()
            session.close()
            return f"Пользователь успешно удален", True
        else:
            return f"Пользователь с таким именем уже существует", False

class Scorelist:
    # user можно указать all
    def __init__(self, user):
        self.user = user

    def score_list(self):
        session = Session()
        result = []

        if self.user != "all":
            user = session.query(User).filter_by(username = self.user).first()
            if not user:
                session.close()
                return f"Пользователь не найден", False
            else:
                exists = session.query(Score).filter_by(username = self.user).first()
                if not exists:
                    score = Score(username = self.user, win = 0, lose = 0)
                    session.add(score)
                    session.commit()
                exists = session.query(Score).filter_by(username = self.user).first()
                
                data = {
                    # "id": score.id, #раскоменти если понадобится
                    "username": exists.username,
                    "win": exists.win,
                    "lose": exists.lose
                }
                session.close()
                return data
        else:
            result = []
            users = session.query(User).all()
            for user in users:
                score = session.query(Score).filter_by(username = user.username).first()
                if not score:
                    score = Score(username = user.username, win=0, lose=0)
                    session.add(score)
                    session.commit()

                data = {
                    # "id": score.id,  #раскоменти если понадобится
                    "username": score.username,
                    "win": score.win,
                    "lose": score.lose
                }
                result.append(data)
            session.close()
            return result

    def score_plus(self, mes): #mes lose or win
        session = Session()

        score = session.query(Score).filter_by(username = self.user).first()
        if not score:
            user = session.query(User).filter_by(username = self.user).first()
            if not user:
                session.close()
                return f"Пользователь не найден", False
            else:
                score = Score(username = self.user, win=0, lose=0)
                session.add(score)
                session.commit()
        if mes == "win":
            score.win += 1
        else:
            score.lose += 1

        session.commit()
        session.close()
        return f"Игра защитана", True

if __name__ == "__main__":
    # регистрация пользователя
    auth = Auth("vla1", "12345")
    print(auth.regist())

    # авторизация
    print(auth.login())

    # добавление очков
    score_service = Scorelist("vlad")
    print(score_service.score_plus("win"))
    print(score_service.score_plus("lose"))

    # вывод профиля одного пользователя
    print(score_service.score_list())

    # вывод всех пользователей важно если пользователь есть в базе с очками но в базе с паролями его нет он не отобразится 
    score_all = Scorelist("all")
    print(score_all.score_list())