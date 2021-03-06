"""Define the schema for queries and mutations.

Notes
-----
* The filtering on features is inappropriate.  Part of the confusion is that
  features is also a relationship field on locations, so that we get different
  behaviors if features is part of a sub-query vs when it is the root.  How do
  we get the semantics right?  Does resolve features need to be added to the
  Location type?
"""

from dateutil import parser
import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType

import models as m
import database as db


def parse_date(d):
    """Parse datetime-like value to datetime.date.
    """
    return parser.parse(d).date()


class Account(SQLAlchemyObjectType):
    """Account info.
    """

    class Meta:
        model = m.Account


class Location(SQLAlchemyObjectType):
    """Location info.
    """

    class Meta:
        model = m.Location


class User(SQLAlchemyObjectType):
    """User info.
    """

    class Meta:
        model = m.User


class Feature(SQLAlchemyObjectType):
    """Feature time series data.
    """

    class Meta:
        model = m.Feature


class AddAccount(graphene.Mutation):

    class Input:
        name = graphene.Int()

    account = graphene.Field(lambda: Account)

    def mutate(self, args, context, info):
        new = m.Account(name=args.get('name'))
        db.Session.add(new)
        db.Session.commit()
        return AddAccount(account=new)


class AddLocation(graphene.Mutation):

    class Input:
        account_id = graphene.Int()
        name = graphene.String()
        address = graphene.String()

    location = graphene.Field(lambda: Location)

    def mutate(self, args, context, info):
        new = m.Location(
            account_id=args.get('account_id'),
            name=args.get('name'),
            address=args.get('address'))
        db.Session.add(new)
        db.Session.commit()
        return AddLocation(location=new)


class AddUser(graphene.Mutation):

    class Input:
        account_id = graphene.Int()
        name = graphene.String()

    user = graphene.Field(lambda: User)

    def mutate(self, args, context, info):
        new = m.User(
            account_id=args.get('account_id'),
            name=args.get('name'))
        db.Session.add(new)
        db.Session.commit()
        return AddUser(user=new)


class Query(graphene.ObjectType):

    accounts = graphene.List(
        Account, description="info on multiple accounts")
    locations = graphene.List(
        Location, description="info on multiple locations")
    users = graphene.List(
        User, description="info on multiple users")
    features = graphene.List(
        Feature,
        description="plural feature data accessor",
        location_id=graphene.Int(default_value=None),
        name=graphene.String(default_value=None),
        start_date=graphene.String(default_value=None),
        end_date=graphene.String(default_value=None))

    account = graphene.Field(Account, id=graphene.Int())
    location = graphene.Field(Location, id=graphene.Int())
    user = graphene.Field(User, id=graphene.Int())

    add = graphene.Float(
        x=graphene.Float(),
        y=graphene.Float())
    addjson = graphene.types.json.JSONString(
        x=graphene.Float(),
        y=graphene.Float())

    def resolve_accounts(self, args, context, info):
        return db.Session.query(m.Account).all()

    def resolve_locations(self, args, context, info):
        return db.Session.query(m.Location).all()

    def resolve_users(self, args, context, info):
        return db.Session.query(m.User).all()

    def resolve_features(self, args, context, info):
        location_id = args.get('location_id')
        name = args.get('name')
        start_date = args.get('start_date')
        end_date = args.get('end_date')
        if all(x is None for x in (location_id, name, start_date, end_date)):
            return db.Session.query(m.Feature).all()
        else:
            filters = []
            if location_id is not None:
                filters.append(m.Feature.location_id == location_id)
            if name is not None:
                filters.append(m.Feature.name == name)
            if None not in (start_date, end_date):
                filters.extend([
                    m.Feature.date >= parse_date(start_date),
                    m.Feature.date <= parse_date(end_date)])
            return db.Session.query(m.Feature).filter(*filters)

    def resolve_account(self, args, context, info):
        return db.Session.query(m.Account).get(args.get('id'))

    def resolve_location(self, args, context, info):
        return db.Session.query(m.Location).get(args.get('id'))

    def resolve_user(self, args, context, info):
        return db.Session.query(m.User).get(args.get('id'))

    def resolve_add(self, args, context, info):
        return args.get('x') + args.get('y')

    def resolve_addjson(self, args, context, info):
        x = args.get('x')
        y = args.get('y')
        return {'x': x, 'y': y, 'result': x + y}


class Mutation(graphene.ObjectType):

    add_account = AddAccount.Field()
    add_location = AddLocation.Field()
    add_user = AddUser.Field()
