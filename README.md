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
and try some queries in the graphical UI.

Here's an example query you can copy and paste into the GraphiQL query window:

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
```

The following queries also work:

```bash
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

In the last example, note that the model field `account_id` must be converted
to camel case (`accountId`) in the query.
