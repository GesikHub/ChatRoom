from flask import Blueprint

bp = Blueprint('login', __name__)

from application.auth import routes, forms
