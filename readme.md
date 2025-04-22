# Library App Documentation

## Overview

A Flask web application for a library system, allowing users to browse, search, borrow, and return books with cover images. Uses SQLite, a Flask blueprint, and Bootstrap for a responsive UI with cards, modals, flash messages, search, and book covers.

### Features

- **View Books**: Books displayed as Bootstrap cards with title, author, status, and cover images.
- **Search Books**: Filter books by title or author.
- **Borrow/Return Books**: Handled via modals with flash message feedback.
- **Responsive UI**: Bootstrap navbar, cards, modals, and library-themed design.

## Project Structure

```
library_app/
├── app.py                 # Main Flask app with blueprint, routes, search, and book covers
├── templates/             # HTML templates
│   ├── base.html          # Base template with navbar and flash messages
│   ├── books.html         # Book list with cards, modals, search, and images
├── static/                # Static files
│   └── style.css          # Custom CSS with library theme
├── library.db             # SQLite database
└── requirements.txt       # Dependencies
```

## Setup Instructions

1. **Navigate to Project**:

   ```bash
   cd D:\Flask WebAPP\library_app
   ```

2. **Activate Environment**:

   ```bash
   conda activate webAppFlask
   ```

3. **Install Dependencies**:

   ```bash
   pip install flask flask-sqlalchemy
   ```

4. **Run the App**:

   ```bash
   python app.py
   ```

   Open `http://127.0.0.1:5000/books`.

5. **Populate Database**:

   ```python
   from app import app, db, Book
   with app.app_context():
       db.session.add(Book(
           title="The Great Gatsby",
           author="F. Scott Fitzgerald",
           image_url="https://images.unsplash.com/photo-1544716278-ca5e3f4b2d6e?ixlib=rb-4.0.3&auto=format&fit=crop&w=300&q=80"
       ))
       db.session.add(Book(
           title="1984",
           author="George Orwell",
           image_url="https://images.unsplash.com/photo-1544947950-fa07a98d237f?ixlib=rb-4.0.3&auto=format&fit=crop&w=300&q=80"
       ))
       db.session.commit()
   ```

## Code Breakdown

### `app.py`

Handles routes, database, search, and book covers.

```python
from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-super-secret-key-123'
db = SQLAlchemy(app)

library_bp = Blueprint('library', __name__)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(50), nullable=False)
    is_borrowed = db.Column(db.Boolean, default=False)
    image_url = db.Column(db.String(200), nullable=True)

@library_bp.route('/')
def index():
    return render_template('base.html')

@library_bp.route('/books', methods=['GET', 'POST'])
def list_books():
    search_query = request.form.get('search', '') if request.method == 'POST' else request.args.get('search', '')
    if search_query:
        books = Book.query.filter(
            (Book.title.ilike(f'%{search_query}%')) | (Book.author.ilike(f'%{search_query}%'))
        ).all()
    else:
        books = Book.query.all()
    return render_template('books.html', books=books, search_query=search_query)

@library_bp.route('/borrow/<int:book_id>', methods=['GET', 'POST'])
def borrow_book(book_id):
    book = Book.query.get_or_404(book_id)
    if request.method == 'POST':
        if not book.is_borrowed:
            book.is_borrowed = True
            db.session.commit()
            flash(f"Successfully borrowed '{book.title}'!", "success")
            return redirect(url_for('library.list_books'))
        else:
            flash("This book is already borrowed.", "danger")
    return render_template('books.html', book=book)

@library_bp.route('/return/<int:book_id>', methods=['GET', 'POST'])
def return_book(book_id):
    book = Book.query.get_or_404(book_id)
    if request.method == 'POST':
        if book.is_borrowed:
            book.is_borrowed = False
            db.session.commit()
            flash(f"Successfully returned '{book.title}'!", "success")
            return redirect(url_for('library.list_books'))
        else:
            flash("This book is already available.", "danger")
    return render_template('books.html', book=book)

with app.app_context():
    db.drop_all()
    db.create_all()

app.register_blueprint(library_bp)

if __name__ == '__main__':
    app.run(debug=True)
```

**Key Points**:

- **Book Covers**: `image_url` column stores cover image URLs.
- **Search**: `list_books` uses `ilike` for title/author filtering.
- **Flash Messages**: Feedback for borrow/return.

### Templates

- `base.html`: Bootstrap navbar, flash message alerts.
- `books.html`: Cards with images, modals, and search form.

### `style.css`

```css
body {
    font-family: 'Arial', sans-serif;
    background-color: #f8f9fa;
    background-image: url('https://www.transparenttextures.com/patterns/wood-pattern.png');
    background-attachment: fixed;
}
.card {
    transition: transform 0.2s;
    max-width: 500px;
    margin: 0 auto;
    border-color: #8b4513;
}
.card:hover {
    transform: scale(1.05);
}
.card-img-top {
    border-bottom: 1px solid #8b4513;
}
.table th, .table td {
    vertical-align: middle;
}
.modal-dialog {
    max-width: 400px;
}
.navbar-dark {
    background-color: #2c3e50;
}
.btn-primary {
    background-color: #4682b4;
    border-color: #4682b4;
}
.btn-success {
    background-color: #228b22;
    border-color: #228b22;
}
.input-group {
    max-width: 500px;
    margin: 0 auto;
}
```

## UI Details

- **Bootstrap 5**: Navbar, cards, modals, alerts, input-group.
- **Cards**: Include cover images (`card-img-top`) with fallback placeholder.
- **Search Form**: Centered input for title/author search.
- **Flash Messages**: `alert-success` or `alert-danger`.
- **Theme**: Library colors (blue navbar, brown borders, wood background).

## Common Issues

1. **Images Don’t Load**:
   - Check `image_url` in database; ensure URLs are valid.
   - Verify `<img>` tag in `books.html`.
2. **Search Fails**:
   - Confirm `ilike` in `app.py` and `name="search"` in form.
3. **Database Empty**:
   - Repopulate with sample books and `image_url`.

## Learning Takeaways

- **Flask**: Form handling, flash messages, secret key.
- **SQLAlchemy**: `ilike` queries, database schema updates.
- **Bootstrap**: Cards, modals, input-group, images.
- **Next Steps**: Add user login or UI animations.

## Future Enhancements

- **User Login**: Track borrowers with Flask-Login.
- **Admin Panel**: Add/edit books.
- **Book Details**: Show more info in a modal.

## Review Tips

- Test book cover images and search.
- Tweak image styles (e.g., add shadow).
- Review `app.py` for `image_url` and `ilike`.