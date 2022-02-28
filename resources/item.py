from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
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

    @jwt_required(fresh=True)
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

    @jwt_required()
    def delete(self, name):
        claims = get_jwt()
        if not claims['is_admin']:
            return {'message': 'Admin privilege required'}, 401
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
    @jwt_required(optional=True)
    def get(self):
        # items = [(lambda item: item.json())(item) for item in items_db]
        # items = list(map(lambda item: item.json(), ItemModel.query.all()))
        user_id = get_jwt_identity()
        items = [item.json() for item in ItemModel.find_all()]
        if user_id:
            return {'items': items}
        return {'items': [item['name'] for item in items],
                'message': 'More data available if you log in'}, 200
