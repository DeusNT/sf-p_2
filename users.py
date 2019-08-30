import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_PATH = "sqlite:///sochi_athletes.sqlite3"
Base = declarative_base()


class User(Base):
    __tablename__ = "user"
    id = sa.Column(sa.INTEGER, primary_key=True)
    first_name = sa.Column(sa.Text)
    last_name = sa.Column(sa.Text)
    gender = sa.Column(sa.Text)
    email = sa.Column(sa.Text)
    birthdate = sa.Column(sa.Text)
    height = sa.Column(sa.REAL)


def connect_db():
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()


def request_data():
    print("Please, provide user data")
    first_name = input("User first name... ")
    last_name = input("User last name... ")
    gender = input("User gender... ")
    email = input("User email... ")
    birthdate = input("User birth date (YYYY-MM-DD)... ")
    height = input("User height (meters.centimeters)... ")
    user = User(
        first_name=first_name,
        last_name=last_name,
        gender=gender,
        email=email,
        birthdate=birthdate,
        height=float(height)
    )
    return user


if __name__ == "__main__":
    session = connect_db()
    user = request_data()
    session.add(user)
    session.commit()
    print("User data successfully saved")
    input("Press enter to close ")
