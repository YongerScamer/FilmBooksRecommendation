from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models import Book, Movie
from utils.recommender import get_book_recommendations, get_movie_recommendations

rec_bp = Blueprint('rec_bp', __name__, template_folder='templates/recommendations')

@rec_bp.route('/')
@login_required
def index():
    return render_template('recommendations/index.html')

@rec_bp.route('/books')
@login_required
def books():
    rec_ids = get_book_recommendations(current_user.id)
    books = Book.query.filter(Book.id.in_(rec_ids)).all()
    return render_template('recommendations/books.html', books=books)

@rec_bp.route('/movies')
@login_required
def movies():
    rec_ids = get_movie_recommendations(current_user.id)
    movies = Movie.query.filter(Movie.movieId.in_(rec_ids)).all()
    return render_template('recommendations/movies.html', movies=movies)