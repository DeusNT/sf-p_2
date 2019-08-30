import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from users import User, connect_db

DB_PATH = "sqlite:///sochi_athletes.sqlite3"
Base = declarative_base()

class Athelete(Base):
    __tablename__ = "athelete"
    id = sa.Column(sa.INTEGER, primary_key=True)
    age = sa.Column(sa.INTEGER)
    birthdate = sa.Column(sa.Text)
    gender = sa.Column(sa.Text)
    height = sa.Column(sa.REAL)
    name = sa.Column(sa.Text)
    weight = sa.Column(sa.INTEGER)
    gold_medals = sa.Column(sa.INTEGER)
    silver_medals = sa.Column(sa.INTEGER)
    bronze_medals = sa.Column(sa.INTEGER)
    total_medals = sa.Column(sa.INTEGER)
    sport = sa.Column(sa.Text)
    country = sa.Column(sa.Text)

def find(id, session):
    query = session.query(User).filter(User.id == id).count()
    if query:
        return True
    else:
        return False

def match(id, session):
    user_query = session.query(User).filter(User.id == id)
    user_birthdate = int(user_query.value("birthdate").replace("-", ""))
    user_height = user_query.value("height")
    athelete_birthdate_list = [int(athelete.birthdate.replace("-", ""))
                               for athelete in session.query(Athelete).all()]
    athelete_height_list = [athelete.height for athelete in session.query(Athelete).all()]
    birth_dif = None
    birth_match = 0
    for val in athelete_birthdate_list:
        if birth_dif is None or abs(user_birthdate - val) < birth_dif:
            birth_dif = abs(user_birthdate - val)
            birth_match = str(val)
    height_dif = None
    height_match = 0
    for val in athelete_height_list:
        if val is not None:
            if height_dif is None or abs(user_height - val) < height_dif:
                height_dif = abs(user_height - val)
                height_match = val
    athelete_birthdate_match = session.query(Athelete).\
        filter(Athelete.birthdate == birth_match[:4] + "-" + birth_match[4]
               + birth_match[5] + "-" + birth_match[6:]).first()
    athelete_height_match = session.query(Athelete).\
        filter(Athelete.height == height_match).first()
    print("User name: %s -- User birth date: %s -- User height: %s\n"
        "The most matching athlete by birth date is %s, who was born at %s\n"
          "And - by height is %s, who is %s meters tall" %
          (user_query.first().first_name + " " + user_query.first().last_name,
           user_query.first().birthdate, user_query.first().height, athelete_birthdate_match.name,
           athelete_birthdate_match.birthdate, athelete_height_match.name, athelete_height_match.height))

if __name__ == "__main__":
    session = connect_db()
    id = input("Please, enter user id... ")
    if find(id, session):
        match(id, session)
    else:
        print("There is no user with given id")
    input("Press enter to close ")