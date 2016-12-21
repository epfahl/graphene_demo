Small Graphene Test Project
===========================

Demo Graphene with SQLAlchemy, SQLite, and Flask.

Get stuff
---------
Install the stuff you'll need:

```bash
pip install -r requirements.txt
```

Try it
------
In the repo directory, run

```bash
> ./app.py
```

then go to [http://localhost:5000/graphql](http://localhost:5000/graphql)
and try some queries in the graphical UI.  Click on the `Docs` tab in GraphiQl
to explore the query and mutation schemas.

Queries
-------

Here are example queries you can copy and past into the GraphiQL editor window:

```bash
{
  accounts {
    name
    locations {
      name 
      address
    }
  }
}

{
  account(id: 1) {
    id
  }
  locations {
    id
    name
    address
  }
}

{
  location(id: 2) {
    id
    name
    address
  }
}

{
  user(id: 1) {
    name
    accountId
  }
}
```

In the last example, note that the field `account_id` on the `User` model must
be converted to camel case (`accountId`) in the query.  If you forget this,
the autocomplete feature of GraphiQL will come to the rescue.

Mutations
---------

Mutations in GraphQL play the roles of PUT/POST in REST.  The following
mutation creates a new location on the account with ID 2 and then queries for
the location and account data on the newly created object.

```bash
mutation {
  addLocation(accountId: 2, name: "E Coli's", address: "111 GI Tract") {
    location {
      id
      account {
        id
        name
      }
      name
      address
    }
  }
}
```

The lead keyword `mutation` signals Graphene to follow the muation codepath.

Runtime Flexibility
-------------------

To demonstrate server-side flexibility, two new schema roots have been added:
`add`, which adds two floats and returns a float, and `addjson`, which returns
a JSONized payload with the input arguments and the addition.  For example,

```bash
{
  add(x: 1.2, y: 1.3)
}

{
  addjson(x: 1.2, y: 1.3)
}
```

Try submitting the following query and read the helpful error message.

```bash
{
  add(x: "1.2", y: 1.3)
}
```

The schema dictates that the type of `x` must be a float.  Graphene validates
the request against the schema before attempting any additional computation
and returns an appropriate error message if the validation fails.