Graphene Demo
===========================

This is a small demonstration of Graphene that uses
* SQLAlchemy to model and interact with the database
* SQLite as the database
* Flask to provide the web server

## Graphene/GraphQL highlights

Graphene is a Python library that implements the GraphQL spec for buliding
declarative APIs.  A GraphQL API provides

* a declarative query syntax, where the client specifies the shape and content of the requested data
* a single endpoint that satisfies all the data needs of the client
* self-documentation and type safety via a schema
* the ability to build complex queries using query fragments and named variables


## Get started

Clone the repo and install the stuff you'll need (there's no guarantee that
everything you'll need is in the requirements file):

```bash
> git clone https://github.com/epfahl/graphene_demo
> cd graphene_demo
> pip install -r requirements.txt
```

Now try it out by running, the app in the repo directory:

```bash
> ./app.py
```

Go to [http://localhost:5000/graphql](http://localhost:5000/graphql)
and try some queries in the GraphiQL UI.  Click on the `Docs` tab in GraphiQL
to explore the query and mutation schemas.


## Models

The demo is built around SQLAlchemy models for an `Account`, a `Location` under an account, a `User` under an account, and a `Feature` under a Location.  Appropriate foreign keys and relationships are specified in the models.  The `features` table
reflected by the `Feature` model records a time series of named features.

Feel free to play around with the models in `model.py` and the data added in `database.py'.  Add more models with deeper relationships, or include a richer data set.


## Queries

Here are example queries you can copy and past into the GraphiQL editor window:

```python
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

In the last example above, note that the field `account_id` on the `User` model
must be converted to camel case (`accountId`) in the query.  If you forget
this, the autocomplete feature of GraphiQL will come to the rescue.

Below is a query with rich filtering on the fields of the Feature model:

```python
{
  features(locationId: 1, name: "high", startDate: "2016-12-2", endDate: "2016-12-5") {
    name
    date
    value
  }
}
```

This returns feature data for the Location with id 1, where the feature name is
'high' and the dates range from '2016-12-2' to '2016-12-5' (inclusive).


## Mutations

Mutations in GraphQL play the roles of PUT/POST in REST.  The following
mutation creates a new location on the account with id 2 and then queries for
the location and account data on the newly created object.

```python
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


## Runtime Flexibility

To demonstrate server-side flexibility, two new schema roots have been added:
`add`, which adds two floats and returns a float, and `addjson`, which returns
a JSONized payload with the input arguments and the result of the addition.
For example,

```python
{
  add(x: 1.2, y: 1.3)
}

{
  addjson(x: 1.2, y: 1.3)
}
```

Try submitting the following query and read the helpful error message.

```python
{
  add(x: "1.2", y: 1.3)
}
```

The schema dictates that the type of `x` must be a float.  Graphene validates
the request against the schema before attempting any additional computation
and returns an appropriate error message if the validation fails.