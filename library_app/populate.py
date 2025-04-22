import sys
import os

# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app import app, db, Book

# Create the database and the database table
with app.app_context():
    db.drop_all()  # Drop all tables if they exist
    db.create_all()  # Create all tables

# Insert sample data if the table is empty
with app.app_context():
    # Create the database and the database table
    db.create_all()

    # Insert sample data
    if not Book.query.first():
        book1 = Book(title='The Great Gatsby', 
                     author='F. Scott Fitzgerald', 
                     image_url='https://static.qobuz.com/images/covers/aa/y3/jqq4w9zaoy3aa_600.jpg',
                     description='A novel set in the 1920s that tells the story of Jay Gatsby and his unrequited love for Daisy Buchanan.')
        book2 = Book(title='To Kill a Mockingbird', 
                     author='Harper Lee', 
                     image_url='https://th.bing.com/th/id/OIP.fAqE1L_Pb64qgodg74ZfRAHaKj?rs=1&pid=ImgDetMain',
                     description='A novel about the serious issues')
        book3 = Book(title='1984', 
                     author='George Orwell', 
                     image_url='https://res.cloudinary.com/jerrick/image/upload/d_642250b563292b35f27461a7.png,f_jpg,fl_progressive,q_auto,w_1024/64c78717dbf9e1001d096f33.jpg',
                     )
        db.session.add(book1)
        db.session.add(book2)
        db.session.add(book3)
        db.session.commit()

        # cd "D:\Flask WebAPP\library_app"
        # python instance/populate.py

