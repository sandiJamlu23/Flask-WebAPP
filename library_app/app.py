from flask import Flask, Blueprint, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define blueprint
library_bp = Blueprint('library', __name__)

# Book model
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(50), nullable=False)
    is_borrowed = db.Column(db.Boolean, default=False)


@library_bp.route('/')
def index():
    return render_template('base.html')

@library_bp.route('/books')
def list_books():
    books = Book.query.all()
    return render_template('books.html', books=books)

@library_bp.route('/borrow/<int:book_id>', methods=['GET', 'POST'])
def borrow_book(book_id):
    book = Book.query.get_or_404(book_id)
    if request.method == 'POST':
        if not book.is_borrowed:
            book.is_borrowed = True
            db.session.commit()
            return redirect(url_for('library.list_books'))
    return render_template('borrow.html', book=book)

@library_bp.route('/return/<int:book_id>', methods=['GET', 'POST'])
def return_book(book_id):
    book = Book.query.get_or_404(book_id)
    if request.method == 'POST':
        if book.is_borrowed:
            book.is_borrowed = False
            db.session.commit()
            return redirect(url_for('library.list_books'))
    return render_template('return.html', book=book)

# Create database and register blueprint *after* defining routes
with app.app_context():
    db.create_all()

# Register blueprint
app.register_blueprint(library_bp)

if __name__ == '__main__':
    app.run(debug=True)