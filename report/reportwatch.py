from flask import Flask
from flask.ext.socketio import SocketIO
from dirwatch import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


@socketio.on('connect')
def test_connect():
    print("Client connected")


@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')


def report_file_event_handler(ev, src):
    data = {'event': ev, "src": src}
    socketio.emit('filesWatcher', data)


if __name__ == '__main__':
    ReportEventHandler("results", report_file_event_handler)
    socketio.run(app, port=5001)
