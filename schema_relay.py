"""Schema using relay.

***Work in progress.***
"""

import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType

import models as m
import database as db


# Opportunity for code generation here, since these type classes are all the
# same up to the name.

class Account(SQLAlchemyObjectType):

    class Meta:
        model = m.Account


class Location(SQLAlchemyObjectType):

    class Meta:
        model = m.Location


class User(SQLAlchemyObjectType):

    class Meta:
        model = m.User


class Query(graphene.ObjectType):

    accounts = graphene.List(Account)
    locations = graphene.List(Location)
    users = graphene.List(User)

    account = graphene.Field(Account, id=graphene.Int())
    location = graphene.Field(Location, id=graphene.Int())
    user = graphene.Field(User, id=graphene.Int())

    # There is structural repetition here. We should be able to add the resolve
    # methods dynamically.  Distinguish between multiple and single entity
    # accessors.

    def resolve_accounts(self, *args, **kwargs):
        return db.Session.query(m.Account).all()

    def resolve_locations(self, *args, **kwargs):
        return db.Session.query(m.Location).all()

    def resolve_users(self, *args, **kwargs):
        return db.Session.query(m.User).all()

    def resolve_account(self, args, context, info):
        return db.Session.query(m.Account).get(args.get('id'))

    def resolve_location(self, args, context, info):
        return db.Session.query(m.Location).get(args.get('id'))

    def resolve_user(self, args, context, info):
        return db.Session.query(m.User).get(args.get('id'))


Schema = graphene.Schema(query=Query)
