import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-default-secret-key'
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get('DATABASE_URL') or 'postgresql://postgres:1234@localhost:5432/movies_db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # URL и ключ для внешнего сервиса рекомендаций
    RECOMMENDER_API_URL = os.environ.get('RECOMMENDER_API_URL') or 'https://api.recommender.local'
    RECOMMENDER_API_KEY = os.environ.get('RECOMMENDER_API_KEY') or 'your-api-key'