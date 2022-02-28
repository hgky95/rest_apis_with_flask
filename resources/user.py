from flask_restful import Resource, reqparse

from models.user import UserModel
from hmac import compare_digest
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity

user_parser = reqparse.RequestParser()
user_parser.add_argument('username',
                    type=str,
                    required=True,
                    help="This field could not be blank")
user_parser.add_argument('password',
                    type=str,
                    required=True,
                    help="This field could not be blank")

class UserRegister(Resource):
    def post(self):
        data = user_parser.parse_args()
        user_db = UserModel.find_by_username(data['username'])
        if user_db:
            return "{'message': 'User already existed in the db'}", 400

        user_db = UserModel(**data)
        user_db.save_to_db()
        return "{'message': 'User created successfully'}", 201

class User(Resource):
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        return user.json()

    @classmethod
    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        UserModel.delete_from_db(user)
        return {'message': 'User is deleted'}, 200


class UserLogin(Resource):
    @classmethod
    def post(cls):
        data = user_parser.parse_args()
        user = UserModel.find_by_username(data['username'])
        if user and compare_digest(user.password, data['password']):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200
        return {'message:' 'Invalid Credential'}, 401

class TokenRefresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        print("TokenRefresh")
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user.id, fresh=False)
        return {'access_token': new_token}, 200


