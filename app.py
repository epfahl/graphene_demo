#!/usr/bin/env python

import sys
import graphene
from flask import Flask
from flask_graphql import GraphQLView
from argparse import ArgumentParser

import database as db
import schema
import schema_auto
import models as m


app = Flask(__name__)

MODELS = (
    m.Account,
    m.Location,
    m.User,
    m.Feature)


def init_db():
    """Initialize the DB.
    """
    db.create()
    db.hydrate()


def _schema(auto, auto_relay):
    """Return the Schema class.
    """
    if (not auto) and (not auto_relay):
        return graphene.Schema(query=schema.Query, mutation=schema.Mutation)

    elif (auto and (not auto_relay)) or (auto and auto_relay):
        # auto generated schema _without_ relay
        return graphene.Schema(query=schema_auto.build_query(
            MODELS, db.Session))

    elif (not auto) and auto_relay:
        # auto generated schema _with_ relay
        return graphene.Schema(query=schema_auto.build_query(
            MODELS, db.Session, with_relay=True))


def start_app(auto, auto_relay):
    """Start the app with schema generated according to the given args.
    """
    app.add_url_rule(
        '/graphql',
        view_func=GraphQLView.as_view(
            'graphql', schema=_schema(auto, auto_relay), graphiql=True))
    app.run('127.0.0.1', port=5000, debug=True)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db.Session.remove()


def parse_args(clargs):
    """Parse command-line arguments.
    """
    parser = ArgumentParser()
    parser.add_argument(
        "--auto", default=False, action="store_true",
        help="use automatic schema generation")
    parser.add_argument(
        "--auto-relay", default=False, action="store_true",
        help="use automatic schema generation with relay interface")
    return parser.parse_args(clargs)


def main(clargs):
    args = parse_args(clargs)
    init_db()
    start_app(args.auto, args.auto_relay)


if __name__ == '__main__':
    main(sys.argv[1:])
