from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker, scoped_session

engine = create_engine('sqlite:///telegrambot.db')
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(Integer)
    balance = Column(Integer)

    def __repr__(self):
        return f"User {self.telegram_id}"

class Tovar(Base):
    __tablename__ = 'tovars'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    amount = Column(Integer)
    cost = Column(Integer)
    photo = Column(String)

# table creating
# Base.metadata.create_all(engine)
session = scoped_session(sessionmaker(bind=engine))

# qwe = User(telegram_id=11111, balance=100)
# session.add(qwe)
# session.commit()

# tovars = session.query(Tovar).all()
# text = ""
# for tovar in tovars:
#     asd = f"{tovar.name}: {tovar.amount}шт. цена: {tovar.cost}р./шт.\n"
#     text += asd
# print(text)

