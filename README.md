Simple Python User DB
=====================

This is a small flask skeleton for creating a user database using Flask, SQLAlchemy, and bcrypt.

In order to get up and running locally:

``` bash
git clone https://github.com/OstrichProjects/Simple-Flask-User-DB.git
cd Simple-Flask-User-DB
# Create virtualenv if you want
pip install -r requirements.txt
python create_db.py
python app.py
```

There are 3 routes included: create, delete, and authenticate.  All routes only take POST requests with the data in the query string as `username` and `password`.  The password is hashed in the `User` model by bcrypt during creation and authentication.  The routes will return a status code and message depending on the arguments given.
