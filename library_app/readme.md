# Library App Documentation

## Overview

This is a Flask web application for a library system, allowing users to browse books, borrow them, and return them. The app uses a SQLite database, a Flask blueprint for routing, and Bootstrap for a modern UI.

### Features

- **View Books**: Displays a list of books with title, author, and availability status.
- **Borrow Books**: Users can borrow available books, marking them as borrowed.
- **Return Books**: Users can return borrowed books, making them available again.
- **Responsive UI**: Styled with Bootstrap for a clean, mobile-friendly interface.

## Project Structure

```
library_app/
├── app.py                 # Main Flask app with blueprint and routes
├── templates/             # HTML templates
│   ├── base.html          # Base template with navbar
│   ├── books.html         # Book list page
│   ├── borrow.html        # Borrow confirmation page
│   └── return.html        # Return confirmation page
├── static/                # Static files
│   └── style.css          # Custom CSS
├── library.db             # SQLite database (created on first run)
└── requirements.txt       # Python dependencies
```

## Setup Instructions

1. **Clone or Create the Project**:

   - Ensure the project is in `D:\Flask WebAPP\library_app`.
   - Verify the structure matches the above.

2. **Set Up Virtual Environment**:

   - Use your Conda environment (`webAppFlask`):

     ```bash
     conda activate webAppFlask
     ```

3. **Install Dependencies**:

   - Run:

     ```bash
     pip install flask flask-sqlalchemy
     pip freeze > requirements.txt
     ```

4. **Run the App**:

   - Navigate to the project folder:

     ```bash
     cd D:\Flask WebAPP\library_app
     ```

   - Start the Flask server:

     ```bash
     python app.py
     ```

   - Open `http://127.0.0.1:5000/books` in a browser.

5. **Populate the Database**:

   - If no books appear, add sample data via Python shell:

     ```bash
     python
     ```

     ```python
     from app import app, db, Book
     with app.app_context():
         db.session.add(Book(title="The Great Gatsby", author="F. Scott Fitzgerald"))
         db.session.add(Book(title="1984", author="George Orwell"))
         db.session.commit()
         books = Book.query.all()
         for book in books:
             print(book.id, book.title, book.author, book.is_borrowed)
     ```

## Code Breakdown

### `app.py`

The main Flask app defines the blueprint, database, and routes.

```python
from flask import Flask, Blueprint, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask app
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

# Routes
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

# Initialize database and register blueprint
with app.app_context():
    db.create_all()

app.register_blueprint(library_bp)

if __name__ == '__main__':
    app.run(debug=True)
```

**Key Points**:

- **Blueprint**: `library_bp` organizes routes under the `library` namespace (e.g., `url_for('library.list_books')`).
- **Database**: SQLite stores books in `library.db`. The `Book` model tracks `id`, `title`, `author`, and `is_borrowed`.
- **Routes**: `/books` lists books, `/borrow/<id>` and `/return/<id>` handle actions.

### Templates

- `base.html`: Base template with Bootstrap navbar and container.
- `books.html`: Displays books in a Bootstrap table with borrow/return buttons.
- `borrow.html`: Confirms borrowing with a Bootstrap card and form.
- `return.html`: Confirms returning with a Bootstrap card and form.

### `static/style.css`

Custom CSS enhances Bootstrap:

```css
body {
    font-family: 'Arial', sans-serif;
    background-color: #f8f9fa;
}
.card {
    max-width: 500px;
    margin: 0 auto;
}
.table th, .table td {
    vertical-align: middle;
}
```

## UI Details

- **Bootstrap 5**: Used via CDN for responsive design (navbar, tables, cards, buttons).
- **Navbar**: Dark-themed, collapsible for mobile.
- **Book List**: Styled as a striped, hoverable table.
- **Borrow/Return Pages**: Use cards for a clean, centered form layout.

## Common Issues and Fixes

1. **Database Empty**:
   - Run the Python shell command to add books.
   - Check `library.db` exists in `library_app/`.
2. **404 Errors**:
   - Ensure `url_for('library.<route>')` matches blueprint route names (e.g., `library.list_books`).
   - Verify `app.py` has all routes defined before `app.register_blueprint`.
3. **Templates Not Found**:
   - Confirm `templates/` contains `base.html`, `books.html`, `borrow.html`, and `return.html`.

## Learning Takeaways

- **Flask Basics**: Learned routes, templates, blueprints, and `url_for`.
- **SQLAlchemy**: Used to manage SQLite database and `Book` model.
- **Bootstrap**: Applied classes like `btn-primary`, `table-striped`, and `card`.
- **Debugging**: Fixed blueprint registration and database issues.
- **Next Steps**: Experiment with adding routes, tweak Bootstrap classes, or explain code in your own words to solidify understanding.

## Future Enhancements

- **User Authentication**: Add login with Flask-Login.
- **Search Feature**: Filter books by title or author.
- **Admin Panel**: Add/edit books via a form.
- **Deployment**: Host on Render or Heroku.

## Review Tips

- **Re-run the App**: Follow setup steps to refresh your memory.
- **Tweak Code**: Change a button color or add a new book to practice.
- **Debug**: If errors appear, check the console and revisit “Common Issues.”
- **Ask Questions**: If confused, note specific topics (e.g., blueprints, SQLAlchemy) for clarification.