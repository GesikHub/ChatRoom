from application import create_app
from flask_socketio import SocketIO, send

app = create_app()
socketio = SocketIO(app)


@socketio.on('message')
def handle_message(msg):
    print('Message: ')
    send(msg, namespace='/test/1')


if __name__ == '__main__':
    app.run(debug=True)