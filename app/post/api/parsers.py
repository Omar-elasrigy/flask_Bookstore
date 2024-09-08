from flask_restful import reqparse


post_parser = reqparse.RequestParser()

post_parser.add_argument("name", required=True, type=str, help="Name is required")
post_parser.add_argument("description", required=True, type=str, help="description is required")
post_parser.add_argument("image", required=True, type=str, help="image is required")
post_parser.add_argument("user_id", required=True, type=int, help="user_id is required")