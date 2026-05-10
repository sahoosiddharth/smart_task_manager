from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
import models

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username','').strip()
    email = data.get('email','').strip()
    password = data.get('password','')
    if not username or not email or not password:
        return jsonify({'error': 'All fields required'}), 400
    if len(password) < 6:
        return jsonify({'error': 'Password must be at least 6 characters'}), 400
    try:
        user = models.create_user(username, email, generate_password_hash(password))
        session['user_id'] = user['id']; session['username'] = user['username']
        return jsonify({'message': 'Registration successful', 'user': user}), 201
    except Exception as e:
        if 'unique' in str(e).lower(): return jsonify({'error': 'Username or email already exists'}), 409
        return jsonify({'error': 'Registration failed'}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username','').strip()
    password = data.get('password','')
    if not username or not password: return jsonify({'error': 'All fields required'}), 400
    user = models.get_user_by_username(username)
    if not user or not check_password_hash(user['password'], password):
        return jsonify({'error': 'Invalid credentials'}), 401
    session['user_id'] = user['id']; session['username'] = user['username']
    return jsonify({'message': 'Login successful', 'user': {'id': user['id'], 'username': user['username'], 'email': user['email']}}), 200

@auth_bp.route('/logout', methods=['GET'])
def logout():
    session.clear(); return jsonify({'message': 'Logged out'}), 200

@auth_bp.route('/me', methods=['GET'])
def me():
    user_id = session.get('user_id')
    if not user_id: return jsonify({'error': 'Not logged in'}), 401
    user = models.get_user_by_id(user_id)
    return jsonify({'user': user}), 200
