import os

from flask import Flask
from flask_jwt import JWT
from flask_restful import Api

from db import db
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from resources.user import UserRegister, User
from security import authenticate, identity

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db_uri = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
if db_uri.startswith("postgres://"):
    db_uri = db_uri.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'test'
api = Api(app)


@app.before_first_request
def create_db():
    db.create_all()


jwt = JWT(app, authenticate, identity)

api.add_resource(Store, '/stores/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(Item, '/items/<string:name>')  # ex: 127.0.0.1:5000/items/chair
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(User, '/users/<int:user_id>')

db.init_app(app)
if __name__ == '__main__':
    app.run(debug=True)
