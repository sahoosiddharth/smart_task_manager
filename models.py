import psycopg2
import psycopg2.extras
from config import Config

def get_db_connection():
    conn = psycopg2.connect(
        host=Config.DB_HOST, port=Config.DB_PORT,
        dbname=Config.DB_NAME, user=Config.DB_USER, password=Config.DB_PASSWORD
    )
    return conn

def create_user(username, email, hashed_password):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    try:
        cur.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s) RETURNING id, username, email",
                    (username, email, hashed_password))
        user = cur.fetchone(); conn.commit(); return dict(user)
    except Exception as e: conn.rollback(); raise e
    finally: cur.close(); conn.close()

def get_user_by_username(username):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    try:
        cur.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cur.fetchone(); return dict(user) if user else None
    finally: cur.close(); conn.close()

def get_user_by_id(user_id):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    try:
        cur.execute("SELECT id, username, email, created_at FROM users WHERE id = %s", (user_id,))
        user = cur.fetchone(); return dict(user) if user else None
    finally: cur.close(); conn.close()

def create_task(user_id, title, description, priority, status):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    try:
        cur.execute("INSERT INTO tasks (user_id, title, description, priority, status) VALUES (%s,%s,%s,%s,%s) RETURNING *",
                    (user_id, title, description, priority, status))
        task = cur.fetchone(); conn.commit(); return dict(task)
    except Exception as e: conn.rollback(); raise e
    finally: cur.close(); conn.close()

def get_all_tasks(user_id):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    try:
        cur.execute("SELECT * FROM tasks WHERE user_id = %s ORDER BY created_date DESC", (user_id,))
        return [dict(t) for t in cur.fetchall()]
    finally: cur.close(); conn.close()

def get_task_by_id(task_id, user_id):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    try:
        cur.execute("SELECT * FROM tasks WHERE id = %s AND user_id = %s", (task_id, user_id))
        task = cur.fetchone(); return dict(task) if task else None
    finally: cur.close(); conn.close()

def update_task(task_id, user_id, title, description, priority, status):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    try:
        cur.execute("UPDATE tasks SET title=%s,description=%s,priority=%s,status=%s,updated_at=CURRENT_TIMESTAMP WHERE id=%s AND user_id=%s RETURNING *",
                    (title, description, priority, status, task_id, user_id))
        task = cur.fetchone(); conn.commit(); return dict(task) if task else None
    except Exception as e: conn.rollback(); raise e
    finally: cur.close(); conn.close()

def delete_task(task_id, user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM tasks WHERE id=%s AND user_id=%s RETURNING id", (task_id, user_id))
        deleted = cur.fetchone(); conn.commit(); return deleted is not None
    except Exception as e: conn.rollback(); raise e
    finally: cur.close(); conn.close()

def get_tasks_for_analytics(user_id):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    try:
        cur.execute("SELECT status, priority, created_date FROM tasks WHERE user_id = %s", (user_id,))
        return [dict(t) for t in cur.fetchall()]
    finally: cur.close(); conn.close()
