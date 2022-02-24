from db import db
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from resources.user import UserRegister
from security import authenticate, identity
from resources.item import Item, ItemList

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db"
app.secret_key = 'test'
api = Api(app)


@app.before_first_request
def create_db():
    db.create_all()


jwt = JWT(app, authenticate, identity)

api.add_resource(Item, '/items/<string:name>')  # ex: 127.0.0.1:5000/items/chair
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

db.init_app(app)

app.run(debug=True)
