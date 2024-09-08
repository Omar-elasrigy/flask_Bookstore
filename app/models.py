from flask_sqlalchemy import SQLAlchemy
from flask import url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
db=SQLAlchemy()


class Post(db.Model):
    __tablename__="post"
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50))
    description=db.Column(db.String(500))
    image=db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('posts', lazy=True))
    @property
    def image_url(self):
        return url_for("static", filename=f"posts/images/{self.image}")
    
    @property
    def delete_url(self):
        return  url_for("post.delete", id=self.id)

    @property
    def show_url(self):
        return url_for("post.show", id=self.id)

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(40), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    # is_active = db.Column(db.Boolean, default=True) 
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    

