import json
from flask import Flask
from flask_socketio import SocketIO, emit

app = Flask(__name__)
io = SocketIO(app, cors_allowed_origins="*")

@io.on('start')
def start(res):
  print('received message: ' + str(res))
  data = { 'data': ['wow', 'such data', 'amazing'] }
  emit('update', json.dumps(data))

if __name__ == '__main__':
  io.run(app)
