import sqlalchemy as sa
from sqlalchemy import orm
import models as m
from models import Base

Engine = sa.create_engine('sqlite:///test.db', convert_unicode=True)
Session = orm.scoped_session(orm.sessionmaker(
    autocommit=False, autoflush=False, bind=Engine))
Base.query = Session.query_property()


def create(engine=Engine):
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def hydrate(engine=Engine, session=Session):

    accounts = {
        'bk': m.Account(name='Burger Kwik'),
        'cl': m.Account(name='Chikin Likin'),
        'pf': m.Account(name='Pizza Face')}

    locations = [
        m.Location(
            name='BK1',
            address='314 Circle Ct',
            account=accounts['bk']),
        m.Location(
            name='BK2',
            address='1350 American Way',
            account=accounts['bk']),
        m.Location(
            name='CL1',
            address='2718 Euler Blvd',
            account=accounts['cl'])]

    users = [
        m.User(
            name='Peter',
            account=accounts['bk']),
        m.User(
            name='Paul',
            account=accounts['bk']),
        m.User(
            name='Mary',
            account=accounts['bk']),
        m.User(
            name='Karen',
            account=accounts['pf']),
        m.User(
            name='Richard',
            account=accounts['pf'])]

    session.add_all(accounts.values())
    session.add_all(locations)
    session.add_all(users)
    session.commit()
