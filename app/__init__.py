from flask import Flask
from flask_migrate import Migrate
from app.models import db
from app.config import config_options
from app.post import post_blueprint
from app.user import user_blueprint
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager
from flask import render_template
from app.models import User
from flask_restful import Resource, Api
def create_app (config_name="production"):
    app=Flask(__name__)
    current_config = config_options[config_name] 
    app.config.from_object(current_config)
    db.init_app(app)
    migrate = Migrate(app, db)
    bootstrap = Bootstrap5(app)
    app.register_blueprint(post_blueprint)
    api = Api(app)
    login_manager = LoginManager(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    app.register_blueprint(user_blueprint)
    @app.route('/',endpoint="landing")
    def landing():
        return render_template('landing.html')


    from app.post.api.views import  PostList, PostResource,UserList
    api.add_resource(PostList, '/api/posts')
    api.add_resource(UserList, '/api/users')
    api.add_resource(PostResource, '/api/posts/<int:id>')
    return app


