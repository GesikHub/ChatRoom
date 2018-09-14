from application.main import bp
from flask import render_template
from flask_login import login_required, current_user
from application.models import User


@bp.route('/', methods=['POST', 'GET'])
@login_required
def start():
    users = User.query.filter(User.id != current_user.id).all()
    return render_template('main/index.html', users=users)
