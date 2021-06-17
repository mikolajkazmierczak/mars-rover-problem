from copy import Error
import json
from flask import Flask
from flask_socketio import SocketIO, emit
from tabu import main as tabu
from annealing import main as annealing
from genetic import main as genetic


app = Flask(__name__)
io = SocketIO(app, cors_allowed_origins="*")

running = False


def run(algorithm, settings):
  for count, objectives, masses, distances in algorithm(settings):
    if not running:
      break
    data = {
      'count': count,
      'objectives': objectives,
      'masses': masses,
      'distances': distances,
    }
    emit('update', json.dumps(data))


@io.on('start')
def start(res):
  print('START start')
  print(f'res: {str(res)}')
  global running
  running = True

  settings = res['settings']
  if res['type'] == 'annealing':
    run(annealing, settings)
  if res['type'] == 'tabu':
    run(tabu, settings)
  if res['type'] == 'genetic':
    run(genetic, settings)
  
  running = False
  emit('stop')
  print('START end')


@io.on('stop')
def stop(res):
  print('STOP start')
  print(f'res: {str(res)}')
  global running

  running = False
  emit('stop')
  print('STOP end')


@io.on('save')
def save(res):
  data = res['data']
  with open(res['filepath'], 'w') as file:
    json.dump(data, file)


@io.on('read')
def read(res):
  try:
    file = open(res['filepath'],)
    emit('read', {
      'name': res['name'],
      'data': json.load(file)
    })
  except Error as e:
    print(f'An error occured while opening the file:\n{e}')


if __name__ == '__main__':
  io.run(app)
