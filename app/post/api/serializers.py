from flask_restful import fields

user_serializers = {
    "id": fields.Integer,
    "username":fields.String,
    "email":fields.String,
}

post_serializers ={
    "id": fields.Integer,
    "name": fields.String,
    "description": fields.String,
    "user_id": fields.Integer,
    "user": fields.Nested(user_serializers),
    "image": fields.String
}