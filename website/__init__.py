from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'thisisthekey'
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url__prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    
    return app