from flask_restful import Resource, Api, marshal_with
from app.models import  db,Post,User
from app.post.api.serializers import  post_serializers,user_serializers
from app.post.api.parsers import  post_parser

class PostList(Resource):
    @marshal_with(post_serializers)
    def get(self):
        posts=  Post.query.all()
        return posts, 200

    @marshal_with(post_serializers)
    def post(self):
        post_args = post_parser.parse_args() 
        print(post_args)
        post = Post(**post_args) 
        db.session.add(post)
        db.session.commit()
        return post, 201


class UserList(Resource):
    @marshal_with(user_serializers)
    def get(self):
        users=  User.query.all()
        return users, 200


class PostResource(Resource):
    @marshal_with(post_serializers)
    def get(self,id):
        post = db.get_or_404(Post, id)
        return post, 200

    @marshal_with(post_serializers)
    def put(self,id):
        post = db.get_or_404(Post, id)
        post_args = post_parser.parse_args()
        post.name= post_args['name']
        post.description= post_args['description']
        post.image= post_args['image']
        post.user_id= post_args['user_id']
        db.session.add(post)
        db.session.commit()
        return post, 200

    def delete(self,id):
        post = db.get_or_404(Post, id)
        db.session.delete(post)
        db.session.commit()
        return "deleted", 204
