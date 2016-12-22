
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import orm
from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    Enum,
    Float,
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
    features = orm.relationship('Feature', backref='location')


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey('accounts.id'))
    name = Column(String)


class Feature(Base):
    __tablename__ = 'features'
    id = Column(Integer, primary_key=True)
    location_id = Column(Integer, ForeignKey('locations.id'))
    name = Column(Enum('high', 'low'))
    date = Column(Date)
    value = Column(Float)
