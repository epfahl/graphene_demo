"""Automatically create a base graphene query object from SQLAlchemy models.
"""

import cytoolz as cz
import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType

import models as m
import database as db

MODELS = (
    m.Account,
    m.Location,
    m.User,
    m.Feature)


def _root_name(model):
    return model.__name__.lower() + "s"


def _resolver_name(model):
    return "resolve_" + _root_name(model)


def _type_class(model):
    meta = type("Meta", (), dict(model=model))
    return type(model.__name__, (SQLAlchemyObjectType,), dict(Meta=meta))


def _root_list(type_class):
    return graphene.List(type_class)


def _resolver_all(model, db_session):

    def _res(self, args, context, info):
        return db_session.query(model).all()

    return _res


def _build_roots(models):
    return {
        _root_name(m): _root_list(_type_class(m))
        for m in models}


def _build_resolvers(models, db_session):
    return {
        _resolver_name(m): _resolver_all(m, db_session)
        for m in models}


def build_query(models, db_session):
    """Build a query object by registering a List root and corresponding
    resolver for each of the given SQLAlchemy models and DB session.
    """
    roots = _build_roots(models)
    resolvers = _build_resolvers(models, db_session)
    return type('Query', (graphene.ObjectType,), cz.merge(roots, resolvers))


Schema = graphene.Schema(query=build_query(MODELS, db.Session))
