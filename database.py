"""Instantiate and hydrate the database.
"""

import random
import datetime
import sqlalchemy as sa
from sqlalchemy import orm

import models as m
from models import Base

Engine = sa.create_engine('sqlite:///test.db', convert_unicode=True)
Session = orm.scoped_session(orm.sessionmaker(
    autocommit=False, autoflush=False, bind=Engine))
Base.query = Session.query_property()


def _date_iter(start_date, end_date):
    """Return a generator of sequential dates over the given inclusive date
    range.
    """
    ndays = (end_date - start_date).days + 1
    return (start_date + datetime.timedelta(days=i) for i in range(ndays))


def _features(location, name, start_date, end_date):
    """Return a list of Feature rows for the given feature name and date range.
    The values are generated randomly.
    """

    def _val(d):
        return m.Feature(
            location=location,
            name=name,
            date=d,
            value=round(random.random(), 3))

    return map(_val, _date_iter(start_date, end_date))


def create(engine=Engine):
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def hydrate(engine=Engine, session=Session):

    accounts = [
        m.Account(name='Burger Kwik'),
        m.Account(name='Chikin Likin'),
        m.Account(name='Pizza Face')]

    locations = [
        m.Location(
            name='BK1',
            address='314 Circle Ct',
            account=accounts[0]),
        m.Location(
            name='BK2',
            address='1350 American Way',
            account=accounts[0]),
        m.Location(
            name='CL1',
            address='2718 Euler Blvd',
            account=accounts[1])]

    users = [
        m.User(
            name='Peter',
            account=accounts[0]),
        m.User(
            name='Paul',
            account=accounts[0]),
        m.User(
            name='Mary',
            account=accounts[0]),
        m.User(
            name='Karen',
            account=accounts[2]),
        m.User(
            name='Richard',
            account=accounts[2])]

    features = _features(
        locations[0], 'low',
        datetime.date(2016, 12, 1), datetime.date(2016, 12, 7))
    features += _features(
        locations[0], 'high',
        datetime.date(2016, 12, 1), datetime.date(2016, 12, 7))

    session.add_all(accounts)
    session.add_all(locations)
    session.add_all(users)
    session.commit()
