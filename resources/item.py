from flask_jwt import jwt_required
from flask_restful import Resource, reqparse

from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field could not be blank")
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="Item need a store id")

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': f'Item with name {name} is not exist'}

    def post(self, name):
        item_db = ItemModel.find_by_name(name)
        if item_db:
            return {'message': 'An item is already exist'}, 400
        data = Item.parser.parse_args()
        item = ItemModel(name, data['price'], data['store_id']) #ItemModel(name, **data)
        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting the item"}, 500
        return item.json(), 201

    def delete(self, name):
        item_db = ItemModel.find_by_name(name)
        if item_db is None:
            return {"message": "Item '{}' not found ".format(name)}
        item_db.delete_from_db()
        return {'message': f'Item {name} is deleted'}

    def put(self, name):
        data = self.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, data['price'], data['store_id']) #ItemModel(name, **data)
        else:
            item.price = data['price']
        item.save_to_db()
        return item.json()


class ItemList(Resource):
    def get(self):
        items_db = ItemModel.query.all()
        items = [item.json() for item in items_db]
        # items = [(lambda item: item.json())(item) for item in items_db]
        # items = list(map(lambda item: item.json(), ItemModel.query.all()))
        return {'items': items}
