import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_PATH = "sqlite:///sochi_athletes.sqlite3"
Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = sa.Column(sa.INTEGER, primary_key=True)
    first_name = sa.Column(sa.Text)
    last_name = sa.Column(sa.Text)
    gender = sa.Column(sa.Text)
    email = sa.Column(sa.Text)
    birthdate = sa.Column(sa.Text)
    height = sa.Column(sa.REAL)


def connect_db():
    engine = sa.create_engine(DB_PATH)
    session = sessionmaker(engine)
    return session()

#Регистрация новых пользователей
def check_in_new_user():
    first_name = input("Введи своё имя: ")
    last_name = input("А теперь фамилию: ")
    gender = input("Ввидите свой пол: ")
    email = input("Мне еще понадобится адрес твоей электронной почты: ")
    birthdate = input("Введите дату вашего рождения: ")
    height = input("Введите ваш рост: ")

    user = User(
        first_name=first_name,
        last_name=last_name,
        gender=gender,
        email=email,
        birthdate=birthdate,
        height=height,
    )
    return user

#Запуск взаимодействия с пользователем
def main():
    session = connect_db()
    user = check_in_new_user()
    session.add(user)
    session.commit()

if __name__ == "__main__":
    main()
