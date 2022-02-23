import sqlite3

from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from user import User


class Item(Resource):
    # def __init__(self, name, price):
    #     self.name = name
    #     self.price = price

    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field could not be blank")

    @jwt_required()
    def get(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM items where name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()
        if row:
            return {'item': {'name': row[0], 'price': row[1]}}
        return {'message': f'Item with name {name} is not exist'}

    def post(self, name):
        item_db = Item.find_by_name(name)
        if item_db:
            return {'message': 'An item is already exist'}, 400
        data = Item.parser.parse_args()
        item = {'name': name, 'price': data['price']}
        try:
            self.insert(item)
        except:
            return {"message": "An error occurred inserting the item"}, 500
        return item, 201

    def delete(self, name):
        item_db = Item.find_by_name(name)
        if item_db is None:
            return {"message": "Item '{}' not found ".format(name)}
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query, (name,))
        connection.commit()
        connection.close()
        return {'message': f'Item {name} is deleted'}

    def put(self, name):
        data = self.parser.parse_args()
        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            item = {'name': name, 'price': data['price']}
            items.append(item)
        else:
            item.update(data)
        return item

    @classmethod
    def insert(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "INSERT INTO items VALUES (?, ?)"
        cursor.execute(query, (item['name'], item['price'],))
        connection.commit()
        connection.close()

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        if row:
            item = {'name': row[0], 'price': row[1]}
        else:
            item = None
        connection.close()
        return item


class ItemList(Resource):
    def get(self):
        return {'items': items}
