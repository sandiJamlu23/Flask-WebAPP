# Library App Documentation

## Overview
The Library App is a simple web application built with Flask, allowing users to browse a catalog of books, borrow them, and return them. It uses SQLite for data storage and Bootstrap for a responsive, modern UI.

## Features
- **View Books**: Display a list of books with title, author, and availability status.
- **Borrow Books**: Mark a book as borrowed (unavailable).
- **Return Books**: Mark a borrowed book as available again.
- **Responsive UI**: Clean, mobile-friendly design with Bootstrap 5.

## Tech Stack
- **Backend**: Flask (Python web framework)
- **Database**: SQLite (via Flask-SQLAlchemy)
- **Frontend**: Jinja2 templates, Bootstrap 5, custom CSS
- **Directory**: `D:\Flask WebAPP\library_app`

## Project Structure
```
library_app/
├── app.py                 # Main Flask app with blueprint and routes
├── templates/             # HTML templates
│   ├── base.html         # Base template with navbar
│   ├── books.html        # Book list page
│   ├── borrow.html       # Borrow confirmation page
│   └── return.html       # Return confirmation page
├── static/                # Static files
│   └── style.css         # Custom CSS
├── library.db             # SQLite database (auto-generated)
└── requirements.txt       # Python dependencies
```

## Setup Instructions
1. **Clone or Navigate to Project**:
   ```bash
   cd D:\Flask WebAPP\library_app
   ```

2. **Set Up Virtual Environment** (if not already done):
   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # Windows
   ```

3. **Install Dependencies**:
   ```bash
   pip install flask flask-sqlalchemy
   pip freeze > requirements.txt
   ```

4. **Run the App**:
   ```bash
   python app.py
   ```
   - Access at `http://127.0.0.1:5000/`.
   - Main page: `http://127.0.0.1:5000/books`.

5. **Populate Database** (optional, to add sample books):
   ```bash
   python
   ```
   ```python
   from app import app, db, Book
   with app.app_context():
       db.session.add(Book(title="The Great Gatsby", author="F. Scott Fitzgerald"))
       db.session.add(Book(title="1984", author="George Orwell"))
       db.session.commit()
   ```

## Usage
- **Home Page** (`/`): Displays a welcome page with navigation.
- **Books Page** (`/books`): Lists all books in a table with “Borrow” or “Return” buttons.
- **Borrow Page** (`/borrow/<id>`): Confirms borrowing a book (marks it as borrowed).
- **Return Page** (`/return/<id>`): Confirms returning a book (marks it as available).
- Navigate using the top navbar or links in the book list.

## Key Components
### Backend (`app.py`)
- **Flask Blueprint**: `library_bp` organizes routes (`/`, `/books`, `/borrow/<id>`, `/return/<id>`).
- **Database Model**: `Book` table with columns:
  - `id`: Integer, primary key
  - `title`: String, book title
  - `author`: String, book author
  - `is_borrowed`: Boolean, tracks borrow status
- **Routes**:
  - `index`: Renders home page.
  - `list_books`: Displays all books.
  - `borrow_book`: Handles borrowing logic.
  - `return_book`: Handles returning logic.

### Frontend (Templates)
- **base.html**: Base template with Bootstrap navbar and container.
- **books.html**: Table-based book list with action buttons.
- **borrow.html**/**return.html**: Card-based forms for borrow/return actions.
- **style.css**: Custom styles for background, card alignment, and table tweaks.

## Troubleshooting
- **No Books Displayed**:
  - Ensure `library.db` exists in `library_app/`.
  - Run the database population script (see Setup).
  - Check `app.py` console for debug prints (e.g., `print(books)`).
- **404 Errors**:
  - Verify `url_for('library.<route>')` matches route names in `app.py`.
  - Ensure blueprint is registered after routes.
- **Template Errors**:
  - Confirm all templates are in `templates/` and named correctly.
- **Database Issues**:
  - Run `db.create_all()` in a Python shell if `library.db` is missing.

## Future Improvements
- **User Authentication**: Add login system with Flask-Login.
- **Search Functionality**: Implement a search bar to filter books by title/author.
- **Admin Panel**: Allow adding/editing books via a web interface.
- **Enhanced UI**: Add book images, categories, or pagination.
- **Deployment**: Host on Render or Heroku for public access.

## Notes
- Built and tested on Windows with Python (Conda environment: `webAppFlask`).
- Last updated: April 17, 2025.
- Refer to this documentation for resuming development or debugging.