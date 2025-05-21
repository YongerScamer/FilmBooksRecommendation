from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from models import Book, FavoriteBook, RatingBook
from forms import SearchBookForm, EmptyForm, RatingForm, SearchForm

books_bp = Blueprint('books', __name__)

@books_bp.route('/', methods=['GET'])
def list_books():
    form = SearchForm(request.args)
    fav_form = EmptyForm()
    query = Book.query
    if form.q.data:
        query = query.filter(Book.bookTitle.ilike(f"%{form.q.data}%"))
    if form.genres.data:
        query = query.filter(Book.bookAuthor.ilike(f"%{form.genres.data}%"))  # genres → author for books
    books = query.order_by(Book.bookTitle).all()
    return render_template('books/list.html', books=books, form=form, fav_form=fav_form)

@books_bp.route('/<int:book_id>', methods=['GET', 'POST'])
def book_detail(book_id):
    book = Book.query.get_or_404(book_id)
    fav_form = EmptyForm()
    rating_form = RatingForm()
    is_fav = False
    user_rating = None
    if current_user.is_authenticated:
        is_fav = FavoriteBook.query.filter_by(user_id=current_user.id, book_id=book_id).first() is not None
        existing = RatingBook.query.filter_by(user_id=current_user.id, book_id=book_id).first()
        if existing:
            user_rating = existing.rating
        if rating_form.validate_on_submit():
            if existing:
                existing.rating = rating_form.rating.data
            else:
                new_rating = RatingBook(user_id=current_user.id, book_id=book_id, rating=rating_form.rating.data)
                db.session.add(new_rating)
            db.session.commit()
            flash('Оценка сохранена', 'success')
            return redirect(url_for('books.book_detail', book_id=book_id))
    avg_rating = db.session.query(db.func.avg(RatingBook.rating)).filter(RatingBook.book_id==book_id).scalar()
    return render_template('books/detail.html', book=book, is_fav=is_fav,
                           fav_form=fav_form, rating_form=rating_form, user_rating=user_rating,
                           avg_rating=avg_rating)

@books_bp.route('/<int:book_id>/favorite', methods=['POST'])
@login_required
def toggle_favorite(book_id):
    fav = FavoriteBook.query.filter_by(user_id=current_user.id, book_id=book_id).first()
    if fav:
        db.session.delete(fav)
        flash('Книга удалена из избранного', 'info')
    else:
        db.session.add(FavoriteBook(user_id=current_user.id, book_id=book_id))
        flash('Книга добавлена в избранное', 'success')
    db.session.commit()
    return redirect(request.referrer or url_for('books.list_books'))

@books_bp.route('/favorites', methods=['GET'])
@login_required
def favorites_list():
    favs = FavoriteBook.query.filter_by(user_id=current_user.id).all()
    books = [fav.book for fav in favs]
    return render_template('books/favorites.html', books=books)