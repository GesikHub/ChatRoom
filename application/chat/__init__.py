from flask import Blueprint

bp = Blueprint('chat', __name__)

from application.chat import routes
