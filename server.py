import json
from flask import Flask
from flask_socketio import SocketIO, emit
from tabu import main as tabu

app = Flask(__name__)
io = SocketIO(app, cors_allowed_origins="*")

running = False


@io.on('start')
def start(res):
  print('START start')
  print(f'res: {str(res)}')
  global running
  running = True

  if res['type'] == 'annealing':
    solution, value = 10, 20
    print(f'annealing: {solution}, {value}')
    emit('update', json.dumps({ 'solution': solution, 'value': value }))

  if res['type'] == 'tabu':
    for count, objectives, masses, distances in tabu(res['settings']):
      if not running:
        break
      data = {
        'count': count,
        'objectives': objectives,
        'masses': masses,
        'distances': distances,
      }
      emit('update', json.dumps(data))

  if res['type'] == 'genetic':
    pass
  
  running = False
  emit('stop', json.dumps({ 'message': 'stopped' }))
  print('START end')


@io.on('stop')
def stop(res):
  print('STOP start')
  print(f'res: {str(res)}')
  global running

  running = False
  emit('stop', json.dumps({ 'message': 'stopped' }))
  print('STOP end')


if __name__ == '__main__':
  io.run(app)
