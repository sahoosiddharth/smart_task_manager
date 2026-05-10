from flask import Blueprint, jsonify, session
import pandas as pd
import numpy as np
import models

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/analytics', methods=['GET'])
def get_analytics():
    user_id = session.get('user_id')
    if not user_id: return jsonify({'error': 'Login required'}), 401
    raw_tasks = models.get_tasks_for_analytics(user_id)
    if not raw_tasks:
        return jsonify({'total_tasks':0,'completed_tasks':0,'pending_tasks':0,'in_progress_tasks':0,'completion_percentage':0.0,'priority_breakdown':{'low':0,'medium':0,'high':0}}), 200
    df = pd.DataFrame(raw_tasks)
    total = len(df)
    completed = int(df[df['status']=='completed'].shape[0])
    pending = int(df[df['status']=='pending'].shape[0])
    in_progress = int(df[df['status']=='in_progress'].shape[0])
    pct = float(np.round((completed/total)*100, 2))
    priority_counts = df['priority'].value_counts().to_dict()
    return jsonify({
        'total_tasks': total, 'completed_tasks': completed,
        'pending_tasks': pending, 'in_progress_tasks': in_progress,
        'completion_percentage': pct,
        'priority_breakdown': {'low': int(priority_counts.get('low',0)), 'medium': int(priority_counts.get('medium',0)), 'high': int(priority_counts.get('high',0))}
    }), 200
