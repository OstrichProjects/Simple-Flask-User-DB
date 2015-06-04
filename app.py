from flask import Flask, request
from flask.ext.sqlalchemy import SQLAlchemy
import bcrypt
import os

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(120))

    def __init__(self, username, password):
        self.username = username
        self.password = bcrypt.hashpw(password, bcrypt.gensalt())

    def __repr__(self):
        return '<User %r>' % self.username

    def changePassword(self, old_pw, new_pw):
        if authenticateUser(self.username, old_pw):
            self.password = bcrypt.hashpw(new_pw, bcrypt.gensalt())
            return (True, "Password changed.")
        return (False, "Incorrect old password.")

def authenticateUser(username, password):
    user = User.query.filter_by(username = username).first()
    if not user:
        return ("User doesn't exist.", 404)
    if bcrypt.hashpw(password, user.password.encode('utf-8')) == user.password:
        return ("User authenticated.", 200)
    else:
        return ("Invalid password.", 401)

def createUser(username, password):
    if User.query.filter_by(username = username).first():
        return ("User with username, {}, already exists.".format(username), 400)
    user = User(username, password)
    db.session.add(user)
    db.session.commit()
    return ("{} added to database.".format(username), 201)

def removeUser(username):
    user = User.query.filter_by(username = username).first()
    if not user:
        return ("User doesn't exist.", 404)
    db.session.delete(user)
    return ("User deleted from database.", 201)


@app.route('/create', methods = ['POST'])
def create():
    username = request.args.get('username')
    password = request.args.get('password').encode('utf-8')

    return createUser(username, password)

@app.route('/remove', methods = ['POST'])
def remove():
    username = request.args.get('username')

    return removeUser(username)

@app.route('/authenticate', methods = ['POST'])
def authenticate():
    username = request.args.get('username')
    password = request.args.get('password').encode('utf-8')

    return authenticateUser(username, password)

if __name__ == '__main__':
    app.run(debug = True)
