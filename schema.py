
import graphene
from graphene import relay
from graphene_sqlalchemy import (
    SQLAlchemyObjectType,
    SQLAlchemyConnectionField)
import models as m


class Account(SQLAlchemyObjectType):

    class Meta:
        model = m.Account
        interfaces = (relay.Node,)


class Location(SQLAlchemyObjectType):

    class Meta:
        model = m.Location
        interfaces = (relay.Node,)


class User(SQLAlchemyObjectType):

    class Meta:
        model = m.User
        interfaces = (relay.Node,)


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    accounts = SQLAlchemyConnectionField(Account)
    locations = SQLAlchemyConnectionField(Location)
    accounts = SQLAlchemyConnectionField(Account)


schema = graphene.Schema(
    query=Query,
    types=[Account, Location, User])
