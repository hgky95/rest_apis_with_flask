import sqlite3

from flask_restful import Resource, reqparse

from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field could not be blank")
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field could not be blank")

    def post(self):
        data = UserRegister.parser.parse_args()
        user_db = UserModel.find_by_username(data['username'])
        if user_db:
            return "{'message': 'User already existed in the db'}", 400

        connection = sqlite3.connect('../data.db')
        cursor = connection.cursor()
        query = "INSERT INTO users VALUES (NULL, ?, ?)"
        cursor.execute(query, (data['username'], data['password'],))

        connection.commit()
        connection.close()
        return "{'message': 'User created successfully'}", 201
