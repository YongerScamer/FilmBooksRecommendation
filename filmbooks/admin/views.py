from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from models import User, Book, Movie, RatingBook, RatingMovie
from forms import EmptyForm, BookForm, MovieForm
from functools import wraps

admin_bp = Blueprint('admin_bp', __name__, template_folder='templates/admin')
book_admin_bp = Blueprint('book_admin_bp', __name__, template_folder='templates/admin/books')
movie_admin_bp = Blueprint('movie_admin_bp', __name__, template_folder='templates/admin/movies')

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash('Доступ запрещён', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated

@admin_bp.route('/')
@admin_required
def dashboard():
    form = EmptyForm()
    users = User.query.order_by(User.username).all()
    return render_template('admin/dashboard.html', users=users, form=form)

@admin_bp.route('/user/<int:user_id>/toggle_role', methods=['POST'])
@admin_required
def toggle_role(user_id):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.get_or_404(user_id)
        user.role = 'admin' if user.role == 'user' else 'user'
        db.session.commit()
        flash('Роль пользователя изменена', 'success')
    return redirect(url_for('admin_bp.dashboard'))

# CRUD для книг
@book_admin_bp.route('/', methods=['GET'])
@admin_required
def list_books_admin():
    books = Book.query.order_by(Book.bookTitle).all()
    return render_template('admin/books/list.html', books=books, form=EmptyForm())

@book_admin_bp.route('/create', methods=['GET', 'POST'])
@admin_required
def create_book():
    form = BookForm()
    if form.validate_on_submit():
        book = Book(ISBN=form.ISBN.data,
                    bookTitle=form.bookTitle.data,
                    bookAuthor=form.bookAuthor.data,
                    yearOfPublication=form.yearOfPublication.data,
                    publisher=form.publisher.data)
        db.session.add(book)
        db.session.commit()
        flash('Книга добавлена', 'success')
        return redirect(url_for('book_admin_bp.list_books_admin'))
    return render_template('admin/books/form.html', form=form)

@book_admin_bp.route('/<int:book_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_book(book_id):
    book = Book.query.get_or_404(book_id)
    form = BookForm(obj=book)
    if form.validate_on_submit():
        form.populate_obj(book)
        db.session.commit()
        flash('Книга обновлена', 'success')
        return redirect(url_for('book_admin_bp.list_books_admin'))
    return render_template('admin/books/form.html', form=form)

@book_admin_bp.route('/<int:book_id>/delete', methods=['POST'])
@admin_required
def delete_book(book_id):
    form = EmptyForm()
    if form.validate_on_submit():
        # Сначала удаляем все рейтинги к этой книге
        RatingBook.query.filter_by(book_id=book_id).delete()
        db.session.commit()
        # Затем удаляем саму книгу
        Book.query.filter_by(id=book_id).delete()
        db.session.commit()
        flash('Книга и связанные оценки удалены', 'info')
    return redirect(url_for('book_admin_bp.list_books_admin'))


# CRUD для фильмов
@movie_admin_bp.route('/', methods=['GET'])
@admin_required
def list_movies_admin():
    movies = Movie.query.order_by(Movie.title).all()
    return render_template('admin/movies/list.html', movies=movies, form=EmptyForm())

@movie_admin_bp.route('/create', methods=['GET', 'POST'])
@admin_required
def create_movie():
    form = MovieForm()
    if form.validate_on_submit():
        movie = Movie(title=form.title.data, genres=form.genres.data)
        db.session.add(movie)
        db.session.commit()
        flash('Фильм добавлен', 'success')
        return redirect(url_for('movie_admin_bp.list_movies_admin'))
    return render_template('admin/movies/form.html', form=form)

@movie_admin_bp.route('/<int:movie_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_movie(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    form = MovieForm(obj=movie)
    if form.validate_on_submit():
        form.populate_obj(movie)
        db.session.commit()
        flash('Фильм обновлён', 'success')
        return redirect(url_for('movie_admin_bp.list_movies_admin'))
    return render_template('admin/movies/form.html', form=form)

@movie_admin_bp.route('/<int:movie_id>/delete', methods=['POST'])
@admin_required
def delete_movie(movie_id):
    form = EmptyForm()
    if form.validate_on_submit():
        RatingMovie.query.filter_by(movie_id=movie_id).delete()
        db.session.commit()
        Movie.query.filter_by(movieId=movie_id).delete()
        db.session.commit()
        flash('Фильм и связанные оценки удалены', 'info')
    return redirect(url_for('movie_admin_bp.list_movies_admin'))
