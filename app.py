from flask import Flask, render_template, session
from flask_socketio import SocketIO, emit, join_room
from config import Config

app = Flask(__name__)
app.secret_key = Config.SECRET_KEY

# ── WebSocket ──────────────────────────────────────────────
socketio = SocketIO(app, cors_allowed_origins="*")

# ── Blueprints with /api prefix (FIX #1) ──────────────────
from routes.auth      import auth_bp
from routes.tasks     import tasks_bp
from routes.analytics import analytics_bp

app.register_blueprint(auth_bp,      url_prefix='/api')
app.register_blueprint(tasks_bp,     url_prefix='/api')
app.register_blueprint(analytics_bp, url_prefix='/api')

# ── Frontend ───────────────────────────────────────────────
@app.route('/')
def index():
    return render_template('index.html')

# ── WebSocket Events (FIX #2) ──────────────────────────────
@socketio.on('connect')
def handle_connect():
    user_id = session.get('user_id')
    if user_id:
        join_room(f'user_{user_id}')
        emit('connected', {'message': f'Connected as user {user_id}'})
    else:
        emit('connected', {'message': 'Connected (guest)'})

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('task_action')
def handle_task_action(data):
    """Receive task event from frontend and broadcast back to user's room."""
    user_id = session.get('user_id')
    if user_id:
        emit('task_update', {
            'action':  data.get('action'),
            'task':    data.get('task'),
            'message': f"Task {data.get('action')} successfully"
        }, room=f'user_{user_id}')

def notify_task_event(user_id, action, task):
    """Call from route handlers to push real-time updates."""
    socketio.emit('task_update', {
        'action':  action,
        'task':    task,
        'message': f'Task {action}'
    }, room=f'user_{user_id}')

# ── Run ────────────────────────────────────────────────────
if __name__ == '__main__':
    print("Smart Task Manager → http://localhost:5000")
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
