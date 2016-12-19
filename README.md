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