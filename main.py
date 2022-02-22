from flask import Flask, jsonify

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
    pass

@app.route("/stores/<string:name>", methods=['GET'])
def get_store():
    pass

@app.route("/stores", methods=['GET'])
def get_stores():
    return jsonify({'stores': stores})  # jsonify allow dictionary

@app.route("/stores/<string:name>/items", methods=['POST'])
def create_items_in_store():
    pass

@app.route("/stores/<string:name>/items", methods=['GET'])
def get_items_in_store():
    pass

app.run()