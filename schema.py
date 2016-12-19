
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


class Query(graphene.ObjectType):

    accounts = graphene.List(Account)
    locations = graphene.List(Location)
    users = graphene.List(User)

    def resolve_accounts(self, *args, **kwargs):
        return db.Session.query(m.Account).all()

    def resolve_locations(self, *args, **kwargs):
        return db.Session.query(m.Location).all()

    def resolve_users(self, *args, **kwargs):
        return db.Session.query(m.User).all()


Schema = graphene.Schema(query=Query)
