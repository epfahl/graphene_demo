"""Automatically create a base graphene query object from SQLAlchemy models.
"""

import cytoolz as cz
import graphene
from graphene import relay
from graphene_sqlalchemy import (
    SQLAlchemyObjectType, SQLAlchemyConnectionField)


def _root_name(model):
    """Return the plural (append 's') lower case name of the model for the
    query root name.
    """
    return model.__name__.lower() + "s"


def _resolver_name(model):
    """Return the name of the resolver function corresponding to the query
    root.
    """
    return "resolve_" + _root_name(model)


def _type_class(model, with_relay):
    """Return an ObjectType class based on the SQLAlchemy model.
    """
    meta_model = dict(model=model)
    if with_relay:
        meta_interfaces = dict(interfaces=(relay.Node,))
    else:
        meta_interfaces = dict()
    meta = type("Meta", (), cz.merge(meta_model, meta_interfaces))
    return type(model.__name__, (SQLAlchemyObjectType,), dict(Meta=meta))


def _root(type_class, with_relay):
    if with_relay:
        return SQLAlchemyConnectionField(type_class)
    else:
        return graphene.List(type_class)


def _resolver_all(model, db_session):

    def _res(self, args, context, info):
        return db_session.query(model).all()

    return _res


def _build_roots(models, with_relay):
    return {
        _root_name(m): _root(_type_class(m, with_relay), with_relay)
        for m in models}


def _build_resolvers(models, db_session):
    return {
        _resolver_name(m): _resolver_all(m, db_session)
        for m in models}


def build_query(models, db_session, with_relay=False):
    """Build a query object by registering a List root and corresponding
    resolver for each of the given SQLAlchemy models and DB session.
    """
    roots = _build_roots(models, with_relay)
    if with_relay:
        resolvers = dict()
    else:
        resolvers = _build_resolvers(models, db_session)
    return type('Query', (graphene.ObjectType,), cz.merge(roots, resolvers))
