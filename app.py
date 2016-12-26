#!/usr/bin/env python

import sys
from flask import Flask
from flask_graphql import GraphQLView
from argparse import ArgumentParser

import database as db
import schema
import schema_auto

app = Flask(__name__)
# app.add_url_rule(
#     '/graphql',
#     view_func=GraphQLView.as_view(
#         'graphql', schema=schema.Schema, graphiql=True))


def init_db():
    db.create()
    db.hydrate()


def start_app(auto):
    if not auto:
        sch = schema.Schema
    else:
        sch = schema_auto.Schema
    app.add_url_rule(
        '/graphql',
        view_func=GraphQLView.as_view(
            'graphql', schema=sch, graphiql=True))
    app.run('127.0.0.1', port=5000, debug=True)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db.Session.remove()


def parse_args(clargs):
    parser = ArgumentParser()
    parser.add_argument(
        "--auto", default=False, action="store_true",
        help="use automatic schema generation from models")
    return parser.parse_args(clargs)


def main(clargs):
    args = parse_args(clargs)
    init_db()
    start_app(args.auto)


if __name__ == '__main__':
    main(sys.argv[1:])
    # db.create()
    # db.hydrate()
    # app.run('127.0.0.1', port=5000, debug=True)
