import sqlalchemy as sa
from sqlalchemy import orm
import models as m

ENGINE = sa.create_engine('sqlite:///test.db', echo=True)
SESSION = orm.scoped_session(orm.sessionmaker(
    autocommit=False, autoflush=False, bind=ENGINE))


def create(engine=ENGINE):
    m.Base.metadata.drop_all(bind=engine)
    m.Base.metadata.create_all(bind=engine)


def hydrate(session=SESSION):
    accounts = {
        'burger kwik': m.Account(name='Burger Kwik'),
        'chikin likin': m.Account(name='Chikin Likin'),
        'pizza face': m.Account(name='Pizza Face'),
        'pasta slurp': m.Account(name='Pasta Slurp')}
    locations = {
        'bk1': m.Location(
            name='BK1',
            address='37 Circle Ct',
            account=accounts['burger kwik'])}
    session.add_all(accounts.values())
    session.add_all(locations.values())
    session.commit()
