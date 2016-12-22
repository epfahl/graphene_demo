"""Define the schema for queries and mutations.

Notes
-----
* There's an opportunity to reduce typing (and copy-pasting) for type and
  mutation classes, as well as for resolve methods in Query.  Perhaps some
  variety of code generation?
"""

import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType

import models as m
import database as db


class Account(SQLAlchemyObjectType):

    class Meta:
        model = m.Account


class Location(SQLAlchemyObjectType):

    class Meta:
        model = m.Location


class User(SQLAlchemyObjectType):

    class Meta:
        model = m.User


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

    accounts = graphene.List(Account)
    locations = graphene.List(Location)
    users = graphene.List(User)

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


Schema = graphene.Schema(query=Query, mutation=Mutation)
