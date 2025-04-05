from flask import Blueprint

views = Blueprint('views', __name__)

@views.route('/login')
def home():
    return "<h1>test</h2>"