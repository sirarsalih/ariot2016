#!/usr/bin/env python

# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on available packages.
async_mode = None

if async_mode is None:
    try:
        import eventlet
        async_mode = 'eventlet'
    except ImportError:
        pass

    if async_mode is None:
        try:
            from gevent import monkey
            async_mode = 'gevent'
        except ImportError:
            pass

    if async_mode is None:
        async_mode = 'threading'

    print('async_mode is ' + async_mode)

# monkey patching is necessary because this application uses a background
# thread
if async_mode == 'eventlet':
    import eventlet
    eventlet.monkey_patch()
elif async_mode == 'gevent':
    from gevent import monkey
    monkey.patch_all()

import time
from threading import Thread
import flask
from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect
from flask.ext.cors import CORS

from pyardrone import ARDrone


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
CORS(app)
socketio = SocketIO(app, async_mode=async_mode)
thread = None


drone = ARDrone()

# drone.navdata_ready.wait()


def report_status(status_id):
    try:
        s = drone.state
        status = {
            'flying': s.fly_mask,
            'motor_problem': s.motors_mask,
            'connection_problem': s.com_lost_mask,
            'low_battery': s.vbat_low,
        }
    except Exception as e:
        status = {
            'error': str(e)
        }

    emit('drone status',
         {'data': status, 'status_id': status_id},
         broadcast=True)


def background_thread():
    """Example of how to send server generated events to clients."""

    count = 0
    while True:
        time.sleep(10)
        count += 1
        socketio.emit('indy takeoff',
                      {'data': 'Server generated event', 'count': count},
                      namespace='/indianadrones')


@app.route('/')
def index():
    global thread
    if thread is None:
        thread = Thread(target=background_thread)
        thread.daemon = True
        thread.start()
    return render_template('index.html')


MANUAL_OVERRIDE = True


@socketio.on('test', namespace='/indy')
def test():
    global MANUAL_OVERRIDE
    if MANUAL_OVERRIDE:
        print("Manual override")
    else:
        print("Not manual")
    emit('test response',
         {'override': MANUAL_OVERRIDE},
         broadcast=True)


@socketio.on('indy override', namespace='/indianadrones')
def indianadrones_override(message):
    global MANUAL_OVERRIDE
    try:
        MANUAL_OVERRIDE = message['override']
    except Exception as e:
        print('Did not receive override in message' + str(e))
    emit('indy response',
         {'data': 'Manual override is set to: ' + str(MANUAL_OVERRIDE)},
         broadcast=True)


@socketio.on('indy takeoff', namespace='/indianadrones')
def indianadrones_takeoff():
    try:
        drone.takeoff()
        m = 'Attempting to takeoff...'
    except Exception as e:
        m = str(e)
    session['receive_count'] = session.get('receive_count', 0) + 1
    report_status(session['receive_count'])
    emit('indy response',
         {'data': m, 'count': session['receive_count']},
         broadcast=True)


@socketio.on('indy land', namespace='/indianadrones')
def indianadrones_land():
    try:
        drone.land()
        m = 'Initiating a landing operation...'
    except Exception as e:
        m = str(e)
    session['receive_count'] = session.get('receive_count', 0) + 1
    report_status(session['receive_count'])
    emit('indy response',
         {'data': m, 'count': session['receive_count']},
         broadcast=True)


@socketio.on('indy left', namespace='/indianadrones')
def indianadrones_left():
    try:
        drone.move(left=1.0)
        m = 'Going left...'
    except Exception as e:
        m = str(e)
    session['receive_count'] = session.get('receive_count', 0) + 1
    report_status(session['receive_count'])
    emit('indy response',
         {'data': m, 'count': session['receive_count']},
         broadcast=True)


@socketio.on('indy right', namespace='/indianadrones')
def indianadrones_right():
    try:
        drone.move(right=1.0)
        m = 'Going right...'
    except Exception as e:
        m = str(e)
    session['receive_count'] = session.get('receive_count', 0) + 1
    report_status(session['receive_count'])
    emit('indy response',
         {'data': m, 'count': session['receive_count']},
         broadcast=True)


@socketio.on('indy forward', namespace='/indianadrones')
def indianadrones_forward():
    try:
        drone.move(forward=1.0)
        m = 'Forward!!!'
    except Exception as e:
        m = str(e)
    session['receive_count'] = session.get('receive_count', 0) + 1
    report_status(session['receive_count'])
    emit('indy response',
         {'data': m, 'count': session['receive_count']},
         broadcast=True)


@socketio.on('indy backward', namespace='/indianadrones')
def indianadrones_backward():
    try:
        drone.move(backward=1.0)
        m = 'Backing up, backing up, backing up, backing up!'
    except Exception as e:
        m = str(e)
    session['receive_count'] = session.get('receive_count', 0) + 1
    report_status(session['receive_count'])
    emit('indy response',
         {'data': m, 'count': session['receive_count']},
         broadcast=True)


@socketio.on('disconnect request', namespace='/indianadrones')
def disconnect_request():
    session['receive_count'] = session.get('receive_count', 0) + 1
    report_status(session['receive_count'])
    try:
        drone.land()
    except Exception as e:
        print(e)
    emit('indy response',
         {'data': 'Disconnected and landed', 'count': session['receive_count']})
    disconnect()


@socketio.on('connect', namespace='/indianadrones')
def test_connect():
    report_status(0)
    emit('indy response', {'data': 'Connected', 'count': 0})


@socketio.on('disconnect', namespace='/indianadrones')
def test_disconnect():
    print('Client disconnected', request.sid)


if __name__ == '__main__':
    socketio.run(app, debug=True)
