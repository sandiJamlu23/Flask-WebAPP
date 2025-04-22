from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'my-super-secret-key-123'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'library.login'

# Define blueprint
library_bp = Blueprint('library', __name__)

# user model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

# Book model
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(50), nullable=False)
    is_borrowed = db.Column(db.Boolean, default=False)
    image_url = db.Column(db.String(200), nullable=True)
    description = db.Column(db.Text, nullable=True)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@library_bp.route('/')
def index():
    return render_template('base.html')

@library_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('library.list_books'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if User.query.filter_by(username=username).first():
            flash('Username already exists.', 'danger')
            return redirect(url_for('library.register'))
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('library.login'))
    return render_template('register.html')

@library_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('library.list_books'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('library.list_books'))
        flash('Invalid username or password.', 'danger')
    return render_template('login.html')

@library_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out success', 'success')
    return redirect(url_for('library.index'))

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
@login_required
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
    return render_template('borrow.html', book=book)

@library_bp.route('/return/<int:book_id>', methods=['GET', 'POST'])
@login_required
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

# Create database and register blueprint *after* defining routes
# with app.app_context():
#     db.drop_all()
#     db.create_all()

# Register blueprint
app.register_blueprint(library_bp)

if __name__ == '__main__':
    app.run(debug=True)