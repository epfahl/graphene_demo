Graphene Demo
===========================

This is a small *work-in-progress* demonstration of Graphene that uses
* SQLAlchemy to model and interact with the database
* SQLite as the database
* Flask to provide the web server

## Graphene/GraphQL highlights

Graphene is a Python library that implements the GraphQL spec for buliding declarative APIs.  A GraphQL API provides

* a declarative query syntax, where the client specifies the shape and content of the requested data
* a single endpoint that satisfies all the data needs of the client
* self-documentation and type safety via a schema
* the ability to build complex queries using query fragments and named variables


## Get started

Clone the repo and install the stuff you'll need (there's no guarantee that everything you'll need is in the requirements file):

```bash
> git clone https://github.com/epfahl/graphene_demo
> cd graphene_demo
> pip install -r requirements.txt
```

Now try it out by running, the app in the repo directory:

```bash
> ./app.py
```

Go to [http://localhost:5000/graphql](http://localhost:5000/graphql) and try some queries in the GraphiQL UI.  Click on the `Docs` tab in GraphiQL to explore the query and mutation schemas.


## Models

The demo is built around SQLAlchemy models for an `Account`, a `Location` under an `Account`, a `User` under an `Account`, and a `Feature` under a `Location`.  Appropriate foreign keys and relationships are specified in the models.  The `features` table reflected by the `Feature` model records a time series of named features.  These models reflect a business case where one is serving a web-based product to multiple users that belong to a multi-location enterprise.

Feel free to play around with the models in `model.py` and the data added in `database.py`.  Add more models with deeper relationships, or include a richer data set.


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

In the last example above, note that the field `account_id` on the `User` model must be converted to camel case (`accountId`) in the query.  If you forget this, the autocomplete feature of GraphiQL will come to the rescue.

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

This returns feature data for the Location with id 1, where the feature name is 'high' and the dates range from '2016-12-2' to '2016-12-5' (inclusive).


## Mutations

Mutations in GraphQL play the roles of PUT/POST in REST.  The following mutation creates a new location on the account with id 2 and then queries for the location and account data on the newly created object.

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

To demonstrate server-side flexibility, two schema roots are included that perform a computation at run time: `add`, which adds two floats and returns a float, and `addjson`, which returns a JSONized payload with the input arguments and the result of the addition. For example,

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

The schema dictates that the type of `x` must be a float.  Graphene validates the request against the schema before attempting any additional computation and returns an appropriate error message if the validation fails.


## Automatic schema generation

After studying `schema.py`, one might notice that the ObjectType classes are sructurally identical, as are the root-resolver pairs for the list-based rooots (accounts, locations, etc.) in the Query class.  And one might then ask, "Can these constructs be generated automatically, given a list of SQLAlchemy models."  The answer is, "Yes!"

The module `schema_auto.py` is a preliminary attempt to automatically create a query class and a schema from the models used in this demo.  Only the list roots are exposed in the query.  To test this functionality for yourself, run

```bash
> ./app.py --auto
```

and try out a few queries in the GraphiQL UI.


## Relay and pagination

As best I currently understand it operationally, Relay imbues GraphQL with an additional layer of abstraction.  If one imagines that the query roots provide access to nodes in a graph, Relay, in effect, exposes certain metadata on the edges, such as cursor identifiers, which can be used for pagination.  

To try out the Relay interface, start the app with

```bash
> ./app.py --auto-relay       
```

Now each of the plural root accessors (accounts, locations, ...) are exposed as Relay connection fields.  A query to get all the location names and address is

```bash
{
  locations {
    edges {
      node {
        id
        name
        address
      }
    }
  }
}
```

The default operation of Relay is to expose node identifiers as *globally unique* opaque strings.  Copy and paste the encoded location `id` of BK1 and try a new query that retrieves data for the first 3 feature rows corresponding to the *node* occupied by that location:

```bash
{
  node(id: "TG9jYXRpb246MQ==") {
    id
    ... on Location {
      features(first: 3) {
        edges {
          cursor
          node {
            id
            name
            date
            value
            locationId
          }
        }
        pageInfo {
          hasNextPage
          hasPreviousPage
          startCursor
          endCursor
        }
      }
    }
  }
}
```

Don't worry about the additional syntax just yet, but pay close attention to the `cursor` field requested on each of the feature edges, as well as `pageInfo` field on the feature connection.  The `cursor` gives us an opaque identenfier for the edge object that we can reuse in subsequent queries; in particular, we can use this field for pagination.  The data returned for `pageInfo` shows us introspective data on the requested collection including the first and last cursor, and booleans that indicate whether there is a next page or previous page.

To get the next three feature rows, add the `after` argument to the feature connection and use the value of the `endCursor` in the previous query:


```bash
{
  node(id: "TG9jYXRpb246MQ==") {
    id
    ... on Location {
      features(first: 3, after:"YXJyYXljb25uZWN0aW9uOjI=") {
        edges {
          cursor
          node {
            id
            name
            date
            value
            locationId
          }
        }
        pageInfo {
          hasNextPage
          hasPreviousPage
          startCursor
          endCursor
        }
      }
    }
  }
}
```

Voila! We now have pagination!  Additional structure comes with Relay, but the new features may well be worth the extra typing.

