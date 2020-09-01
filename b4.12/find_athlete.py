import datetime

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
    birthdate = sa.Column(sa.DATE)
    height = sa.Column(sa.REAL)

class Athelete(Base):
    __tablename__ = 'athelete'
    id = sa.Column(sa.INTEGER, primary_key=True)
    birthdate = sa.Column(sa.Text)
    height = sa.Column(sa.REAL)
    name = sa.Column(sa.Text)

def connect_db():
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)

    return session()
#Ищем пользователя по id
def find_user_by_id(user_id):
    session = connect_db()
    user = session.query(User).filter(User.id == user_id).first()
    session.close()

    return user
#Ищем близайшего атлета по росту
def find_athelete_by_hieght(user_height):
    session = connect_db()
    atheletes = session.query(Athelete).filter(Athelete.height > 0).all()
    session.close()
    candidate = atheletes[0]
    for athelete in atheletes:
        candidate_dif = abs(candidate.height - user_height)
        athelete_dif = abs(athelete.height - user_height)
    if athelete_dif < candidate_dif:
        candidate = athelete

    return candidate

def date_dif(date_1, date_2):
    datetime_1 = datetime.strptime(date_1, "%Y-%m-%d")
    datetime_2 = datetime.strptime(date_2, "%Y-%m-%d")
    dif = abs(datetime_1 - datetime_2)
    return dif

#Ищем атлета по дню рождения
def find_athelete_by_birthdate(user_birthdate):
    session = connect_db()
    athelete1 = session.query(Athelete.birthdate).all()
    session.close()
    candidate1 = athelete1[0]
    for athelete in athelete1:
        candidate_dif = date_dif(candidate1.birthdate, user_birthdate)
        atheletes_dif = date_dif(athelete1.birthdate, user_birthdate)
        if atheletes_dif < candidate_dif:
            candidate1 = athelete1
    return candidate1


def main():
    user_id = int(input("Введите id пользователя: "))
    user = find_user_by_id(user_id)
    if user:
        athelete_close_height = find_athelete_by_hieght(user.height)
        print(f"Близжайсший атлет по возрасту {athelete_close_height.name} - {athelete_close_height.height}")
        athelete_close_birthdate = find_athelete_by_birthdate(user.birthdate)
        print(f"Близшайший по возрасту атлет: {athelete_close_birthdate.name} - {athelete_close_birthdate.birthdate}")
    else:
        print("Пользователь с таким id не найден")

if __name__ == '__main__':
    main()