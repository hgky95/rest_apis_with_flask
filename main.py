from flask import Flask, jsonify, request

app = Flask(__name__)

stores = [
    {
        'name': 'BlackBerry Store',
        'items': [
            {
                'name': 'Item 1',
                'price': 150
            }
        ]
    }
]

@app.route('/stores', methods=['POST'])
def create_stores():
    request_data = request.get_json()
    new_store = {
        'name': request_data['name'],
        'items': []
    }
    stores.append(new_store)
    return jsonify(new_store)

@app.route("/stores/<string:name>", methods=['GET'])
def get_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify(store)
    return jsonify({'message': 'store not found'})

@app.route("/stores", methods=['GET'])
def get_stores():
    return jsonify({'stores': stores})  # jsonify allow dictionary

@app.route("/stores/<string:name>/items", methods=['POST'])
def create_items_in_store(name):
    request_data = request.get_json()
    for store in stores:
        if store['name'] == name:
            new_item = {
                'name': request_data['name'],
                'price': request_data['price']
            }
            store['items'].append(new_item)
            return jsonify(new_item)
    return jsonify({'message': 'store not found'})

@app.route("/stores/<string:name>/items", methods=['GET'])
def get_items_in_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify(store['items'])
    return jsonify({'message': 'store not found'})

app.run()