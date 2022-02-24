from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from resources.user import UserRegister
from security import authenticate, identity
from resources.item import Item, ItemList

app = Flask(__name__)
app.secret_key = 'test'
api = Api(app)
jwt = JWT(app, authenticate, identity)

api.add_resource(Item, '/items/<string:name>')  # ex: 127.0.0.1:5000/items/chair
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

app.run(debug=True)
