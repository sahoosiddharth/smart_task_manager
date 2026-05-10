import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'smarttask_secret_key_2024')
    DB_HOST     = os.environ.get('DB_HOST', 'localhost')
    DB_PORT     = os.environ.get('DB_PORT', '5432')
    DB_NAME     = os.environ.get('DB_NAME', 'smart_task_db')
    DB_USER     = os.environ.get('DB_USER', 'postgres')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', 'admin123')   
