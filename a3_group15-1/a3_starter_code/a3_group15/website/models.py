from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_bcrypt import Bcrypt
from sqlalchemy.sql import func

# Launch the database and bcrypt
db = SQLAlchemy()
bcrypt = Bcrypt()

# MVP: User table storing information about users, including:
# full name, email, password, number, street address
class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(150), nullable=False)
    last_name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(150), nullable=False)
    contact_number = db.Column(db.String(20), nullable=True)
    street_address = db.Column(db.String(200), nullable=True)

    # Relationships: one user can have many events, bookings, comments, and likes
    events = db.relationship('Event', backref='creator', lazy=True)
    bookings = db.relationship('Booking', backref='user', lazy=True)
    comments = db.relationship('Comment', backref='user', lazy=True)
    likes = db.relationship('Like', backref='user', lazy=True)


# MVP: Event table containing the event details, name, description, times, venue, price
# total tickers, sold tickets, status and date
class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime(timezone=True), nullable=False, default=func.now())
    start_time = db.Column(db.String(50), nullable=False)
    end_time = db.Column(db.String(50), nullable=False)
    venue = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)  # Ticke
    total_tickets = db.Column(db.Integer, nullable=False)
    tickets_sold = db.Column(db.Integer, nullable=False, default=0)
    status = db.Column(db.String(20), nullable=False, default='Open')

    # Foreign key to link event to the creator (user)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Relationships: one event can have many bookings, comments, and likes
    bookings = db.relationship('Booking', backref='event', lazy=True)
    comments = db.relationship('Comment', backref='event', lazy=True)
    likes = db.relationship('Like', backref='event', lazy=True)

# MVP: Booking table storing price, quantity, booking time and date
# with relationship to a user and an event
class Booking(db.Model):
    __tablename__ = 'bookings'

    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    booking_date = db.Column(db.DateTime(timezone=True), default=func.now())

    # Booking status: Tracks if the booking is completed, cancelled, or upcoming
    status = db.Column(db.String(20), nullable=False, default='Upcoming')

    # Date for when the user attended the event ---> I need to double check if team wants to have past event dates included 
    attended_date = db.Column(db.DateTime(timezone=True), nullable=True)

    # Foreign keys to link booking to user and event
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)

# MVP: Comments table: comment content and time stamp 
class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    comment_date = db.Column(db.DateTime(timezone=True), default=func.now())

    # Foreign keys to link comment to user and event
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)

# Like model: stores likes on events ---> Likes recorded on events, but I need to check with team
class Like(db.Model):
    __tablename__ = 'likes'

    id = db.Column(db.Integer, primary_key=True)

    # Foreign keys to link the like to both the user and the event
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)

    # Track when the like was made
    like_date = db.Column(db.DateTime(timezone=True), default=func.now())

# Function to Launch the database and create tables if they don't exist
def init_db(app):
    with app.app_context():
        db.create_all()
