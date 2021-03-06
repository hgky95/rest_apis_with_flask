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

        user_db = UserModel(**data)
        user_db.save_to_db()
        return "{'message': 'User created successfully'}", 201
