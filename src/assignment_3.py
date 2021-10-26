from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
import jwt
from datetime import datetime, timedelta

app = Flask(__name__)

app.config['SECRET_KEY'] = 's3cr3tk3y'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/python'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column('id', db.Integer, primary_key=True)
    login = db.Column('login', db.String(50))
    password = db.Column('password', db.String(255))
    token = db.Column('token', db.String(255))
    def __init__(self, login, password):
        self.login = login
        self.password = password

@app.route('/login')
def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password: 
        return make_response('Please, your login and password', 401, {'WWW-Authenticate':'Basic realm="Login required"'})
    user = User.query.filter_by(login = auth.username).first()
    if not user: 
        return make_response('Could not found a user with login: ' + auth.username, 401, {'WWW-Authenticate':'Basic realm="Login required"'})
    if (user.password, auth.password):
        token = jwt.encode({'id' : user.id, 'exp' : datetime.utcnow() + timedelta(minutes = 30)}, app.config['SECRET_KEY'])
        update_token = User.query.filter_by(id = user.id).first()
        update_token.token = token
        db.session.commit()
        return jsonify({'token' : token})
    return make_response('Could not verify', 401, {'WWW-Authenticate':'Basic realm="Login required"'})

@app.route('/protected', methods = ['GET'])
def pass_token():
    token = request.args.get('token')
    user = User.query.filter_by(token = token).first()
    if not user:
        return 'Hello, token which is provided is correct'
    return 'Hello, could not verify the token'


if __name__ == '__main__':
    app.run(debug=True) 