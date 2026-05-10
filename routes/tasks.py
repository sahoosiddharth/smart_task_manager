from flask import Blueprint, request, jsonify, session
import models

tasks_bp = Blueprint('tasks', __name__)

def get_user():
    return session.get('user_id')

@tasks_bp.route('/tasks', methods=['POST'])
def add_task():
    user_id = get_user()
    if not user_id: return jsonify({'error': 'Login required'}), 401
    data = request.get_json()
    title = data.get('title','').strip()
    if not title: return jsonify({'error': 'Title required'}), 400
    priority = data.get('priority', 'medium')
    status = data.get('status', 'pending')
    if priority not in ['low','medium','high']: return jsonify({'error': 'Invalid priority'}), 400
    if status not in ['pending','in_progress','completed']: return jsonify({'error': 'Invalid status'}), 400
    task = models.create_task(user_id, title, data.get('description',''), priority, status)
    task['created_date'] = str(task['created_date']); task['updated_at'] = str(task['updated_at'])
    return jsonify({'message': 'Task created', 'task': task}), 201

@tasks_bp.route('/tasks', methods=['GET'])
def get_tasks():
    user_id = get_user()
    if not user_id: return jsonify({'error': 'Login required'}), 401
    tasks = models.get_all_tasks(user_id)
    for t in tasks: t['created_date'] = str(t['created_date']); t['updated_at'] = str(t['updated_at'])
    return jsonify({'tasks': tasks, 'count': len(tasks)}), 200

@tasks_bp.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    user_id = get_user()
    if not user_id: return jsonify({'error': 'Login required'}), 401
    existing = models.get_task_by_id(task_id, user_id)
    if not existing: return jsonify({'error': 'Task not found'}), 404
    data = request.get_json()
    title = data.get('title', existing['title']).strip()
    description = data.get('description', existing['description'])
    priority = data.get('priority', existing['priority'])
    status = data.get('status', existing['status'])
    task = models.update_task(task_id, user_id, title, description, priority, status)
    task['created_date'] = str(task['created_date']); task['updated_at'] = str(task['updated_at'])
    return jsonify({'message': 'Task updated', 'task': task}), 200

@tasks_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    user_id = get_user()
    if not user_id: return jsonify({'error': 'Login required'}), 401
    deleted = models.delete_task(task_id, user_id)
    if not deleted: return jsonify({'error': 'Task not found'}), 404
    return jsonify({'message': f'Task {task_id} deleted'}), 200
