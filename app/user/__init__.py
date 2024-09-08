from flask import Blueprint
user_blueprint = Blueprint('user', __name__,url_prefix='/user')


from app.user import views