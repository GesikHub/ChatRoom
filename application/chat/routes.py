from application.chat import bp
from application.models import ChatRoom, Message, User
from application import db
from flask_login import current_user, login_required
from flask import redirect, url_for, request, render_template, jsonify


@bp.route('/chat/<chat_id>')
@login_required
def chat(chat_id):
    chat_room = ChatRoom.query.filter_by(id_chat_room=chat_id).first()
    if chat_room is None:
        return redirect(url_for('main.start'))
    if current_user.id != chat_room.user_1 and current_user.id != chat_room.user_2:
        return redirect(url_for('main.start'))
    messages = Message.query.filter(Message.chat_room == chat_room.id_chat_room, Message.view == True).all()
    if current_user.id == chat_room.user_1:
        user = User.query.filter_by(id=chat_room.user_2).first()
    else:
        user = User.query.filter_by(id=chat_room.user_1).first()
    return render_template('chat/chat.html', messages=messages, user_name=user.login, chat_room=chat_id)


@bp.route('/send_message', methods=['GET', 'POST'])
def send_message():
    chat_room = ChatRoom.query.filter(
        (ChatRoom.user_1 == request.args['s'] and ChatRoom.user_2 == request.args['l'])).first()
    if chat_room is None:
        chat_room = ChatRoom.query.filter(
            (ChatRoom.user_1 == request.args['l'] and ChatRoom.user_2 == request.args['s'])).first()
        if chat_room is None:
            chat_room = ChatRoom(user_1=request.args['s'], user_2=request.args['l'])
            db.session.add(chat_room)
            db.session.commit()
    return redirect('/chat/'+str(chat_room.id_chat_room))


@bp.route('/set_message', methods=['POST'])
def set_message():
    message = Message(text_message=request.form['text'], sender=request.form['sender'],
                      chat_room=request.form['chat_room'])
    message.view = False
    db.session.add(message)
    db.session.commit()
    return jsonify({'message': '200'})


@bp.route('/get_message/<chat_id>/<user_id>', methods=['GET'])
def get_message(chat_id, user_id):
    messages = Message.query.filter(Message.chat_room == chat_id, Message.sender != user_id, Message.view == False).all()
    send_message = []
    for message in messages:
        message.view = True
        send_message.append(message.text_message)
    db.session.commit()
    return jsonify({'message': send_message})
