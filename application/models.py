from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from application import db, login
from datetime import datetime


class TimeTableMixin:
    create = db.Column(db.DateTime, default=datetime.utcnow())
    update = db.Column(db.DateTime, onupdate=datetime.utcnow())


class User(db.Model, UserMixin, TimeTableMixin):
    id = db.Column(db.Integer(), primary_key=True)
    login = db.Column(db.String(128), unique=True)
    password = db.Column(db.String(255))

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return self.login


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Message(db.Model, TimeTableMixin):
    id_message = db.Column(db.Integer(), primary_key=True)
    text_message = db.Column(db.Text())
    sender = db.Column(db.Integer, db.ForeignKey('user.id'))
    chat_room = db.Column(db.Integer, db.ForeignKey('chat_room.id_chat_room'), nullable=False)
    view = db.Column(db.Boolean)

    def __repr__(self):
        return self.id_message


class ChatRoom(db.Model, TimeTableMixin):
    id_chat_room = db.Column(db.Integer(), primary_key=True)
    user_1 = db.Column(db.Integer, db.ForeignKey('user.id'))
    user_2 = db.Column(db.Integer, db.ForeignKey('user.id'))
    messages = db.relationship('Message', backref='chatroom', lazy='dynamic')

    def __repr__(self):
        return self.id_chat_room
