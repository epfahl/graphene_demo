
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import orm
from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey)

Base = declarative_base()


class Account(Base):
    __tablename__ = 'accounts'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    locations = orm.relationship('Location', backref='account')
    users = orm.relationship('User', backref='account')


class Location(Base):
    __tablename__ = 'locations'
    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey('accounts.id'))
    name = Column(String)
    address = Column(String)
    account = orm.relationship('Account', backref='location')


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey('accounts.id'))
    name = Column(String)
