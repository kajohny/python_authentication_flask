# PYTHON AUTHENTICATION WITH FLASK

## Installation
```
pip install flask
pip install flask-sqlalchemy
pip install PyJwt
```

## Usage
```
from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
import jwt
from datetime import datetime, timedelta
```
## Examples

*SQLAlchemy*:
```
app = Flask(__name__)

app.config['SECRET_KEY'] = 's3cr3tk3y'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/python'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

if __name__ == '__main__':
    app.run(debug=True) 
```

*PyJWT*:
```
token = jwt.encode({'id' : user.id, 'exp' : datetime.utcnow() + timedelta(minutes = 30)}, app.config['SECRET_KEY'])
```

*Routes*:
```
@app.route('/login')
@app.route('/protected', methods = ['GET'])
```

*Database table*:
```
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column('id', db.Integer, primary_key=True)
    login = db.Column('login', db.String(50))
    password = db.Column('password', db.String(255))
    token = db.Column('token', db.String(255))
```
