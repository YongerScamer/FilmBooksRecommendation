from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from models import Movie, FavoriteMovie, RatingMovie
from forms import SearchMovieForm, EmptyForm, RatingForm, SearchForm

movies_bp = Blueprint('movies', __name__)

@movies_bp.route('/', methods=['GET'])
def list_movies():
    form = SearchForm(request.args)
    query = Movie.query
    if form.q.data:
        query = query.filter(Movie.title.ilike(f"%{form.q.data}%"))
    if form.genres.data:
        query = query.filter(Movie.genres.ilike(f"%{form.genres.data}%"))
    movies = query.order_by(Movie.title).all()
    return render_template('movies/list.html', movies=movies, form=form)

@movies_bp.route('/<int:movie_id>', methods=['GET', 'POST'])
def movie_detail(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    fav_form = EmptyForm()
    rating_form = RatingForm()
    is_fav = False
    user_rating = None
    if current_user.is_authenticated:
        is_fav = FavoriteMovie.query.filter_by(user_id=current_user.id, movie_id=movie_id).first() is not None
        existing = RatingMovie.query.filter_by(user_id=current_user.id, movie_id=movie_id).first()
        if existing:
            user_rating = existing.rating
        if rating_form.validate_on_submit():
            if existing:
                existing.rating = rating_form.rating.data
            else:
                new_rating = RatingMovie(user_id=current_user.id, movie_id=movie_id, rating=rating_form.rating.data)
                db.session.add(new_rating)
            db.session.commit()
            flash('Оценка сохранена', 'success')
            return redirect(url_for('movies.movie_detail', movie_id=movie_id))
    avg_rating = db.session.query(db.func.avg(RatingMovie.rating)).filter(RatingMovie.movie_id==movie_id).scalar()
    return render_template('movies/detail.html', movie=movie, is_fav=is_fav,
                           fav_form=fav_form, rating_form=rating_form, user_rating=user_rating,
                           avg_rating=avg_rating)

@movies_bp.route('/<int:movie_id>/favorite', methods=['POST'])
@login_required
def toggle_favorite(movie_id):
    fav = FavoriteMovie.query.filter_by(user_id=current_user.id, movie_id=movie_id).first()
    if fav:
        db.session.delete(fav)
        flash('Фильм удалён из избранного', 'info')
    else:
        db.session.add(FavoriteMovie(user_id=current_user.id, movie_id=movie_id))
        flash('Фильм добавлен в избранное', 'success')
    db.session.commit()
    return redirect(request.referrer or url_for('movies.list_movies'))

@movies_bp.route('/favorites', methods=['GET'])
@login_required
def favorites_list():
    favs = FavoriteMovie.query.filter_by(user_id=current_user.id).all()
    movies = [fav.movie for fav in favs]
    return render_template('movies/favorites.html', movies=movies)