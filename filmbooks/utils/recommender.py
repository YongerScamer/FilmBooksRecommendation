import requests
from config import Config


def get_book_recommendations(user_id):
    """Запрос рекомендаций книг для пользователя по REST API.
    Если сервис недоступен, возвращает пустой список."""
    url = f"{Config.RECOMMENDER_API_URL}/books"
    headers = {'Authorization': f"Bearer {Config.RECOMMENDER_API_KEY}"}
    try:
        resp = requests.post(url, json={'user_id': user_id}, headers=headers, timeout=5)
        resp.raise_for_status()
        data = resp.json()
        return data.get('recommendations', [])
    except Exception as e:
        # Логгирование можно добавить здесь
        return []


def get_movie_recommendations(user_id):
    """Запрос рекомендаций фильмов для пользователя по REST API.
    Если сервис недоступен, возвращает пустой список."""
    url = f"{Config.RECOMMENDER_API_URL}/movies"
    headers = {'Authorization': f"Bearer {Config.RECOMMENDER_API_KEY}"}
    try:
        resp = requests.post(url, json={'user_id': user_id}, headers=headers, timeout=5)
        resp.raise_for_status()
        data = resp.json()
        return data.get('recommendations', [])
    except Exception as e:
        # Логгирование можно добавить здесь
        return [0, 1]