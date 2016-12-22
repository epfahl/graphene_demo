#!/usr/bin/env python

from flask import Flask
from flask_graphql import GraphQLView

import database as db
import schema

app = Flask(__name__)
app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql', schema=schema.Schema, graphiql=True))


@app.teardown_appcontext
def shutdown_session(exception=None):
    db.Session.remove()


if __name__ == '__main__':
    db.create()
    db.hydrate()
    app.run('127.0.0.1', port=5000, debug=True)
