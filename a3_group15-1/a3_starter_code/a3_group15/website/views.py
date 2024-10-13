from flask import render_template, redirect, url_for, flash, Blueprint
from .forms import RegistrationForm, EventForm, BookingForm, CommentForm
from .models import User, Event, Booking, Comment, db, bcrypt
from flask_login import login_user, current_user

# Define the blueprint
main_bp = Blueprint('main', __name__)

# Main Index Route
@main_bp.route('/')
def index():
    return render_template('index.html')


# MVP: User table storing information about users, including their login credentials
@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Check if the email is already in use
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Email is already registered. Please log in.', 'danger')
            return redirect(url_for('main.login'))

        # Hash the password using Flask-Bcrypt
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        # Create a new user instance
        new_user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            password_hash=hashed_password
        )

        # Add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        # Automatically log the user in after registration
        login_user(new_user)
        flash('Account created successfully! You are now logged in.', 'success')
        return redirect(url_for('main.index'))

    return render_template('user.html', form=form, heading='Register')


# MVP: Event table containing event details
@main_bp.route('/create-event', methods=['GET', 'POST'])
def create_event():
    form = EventForm()
    if form.validate_on_submit():
        # Create a new event instance (MVP: Event creation, storing event details)
        new_event = Event(
            name=form.name.data,
            description=form.description.data,
            date=form.date.data,
            start_time=form.start_time.data,
            end_time=form.end_time.data,
            venue=form.venue.data,
            price=form.price.data,
            total_tickets=form.total_tickets.data,
            creator_id=current_user.id  # User creating the event MVP: Linked to user
        )
        
        # Add the new event to the database MVP: Event table
        db.session.add(new_event)
        db.session.commit()
        flash('Event created successfully!', 'success')
        return redirect(url_for('main.index'))

    return render_template('eventcreate.html', form=form) 


# MVP: Booking table storing price, quantity, and date
@main_bp.route('/book/<int:event_id>', methods=['GET', 'POST'])
def book_tickets(event_id):
    form = BookingForm()
    event = Event.query.get_or_404(event_id)
    if form.validate_on_submit():
        # Create a new booking
        booking = Booking(
            user_id=current_user.id,  
            event_id=event.id, 
            quantity=form.quantity.data,  
            total_price=form.quantity.data * event.price  
        )

        # Add the booking to the database
        db.session.add(booking)
        db.session.commit()
        flash('Booking successful!', 'success')
        return redirect(url_for('main.event_details', event_id=event.id))

    return render_template('book.html', form=form, event=event)  


# MVP: Comments table
@main_bp.route('/event/<int:event_id>/comment', methods=['POST'])
def leave_comment(event_id):
    form = CommentForm()
    event = Event.query.get_or_404(event_id)
    if form.validate_on_submit():
        # Create a new comment instance
        comment = Comment(
            content=form.content.data,  
            user_id=current_user.id, 
            event_id=event_id 
        )

        # Add the comment to the database
        db.session.add(comment)
        db.session.commit()
        flash('Comment posted successfully!', 'success')
        return redirect(url_for('main.event_details', event_id=event_id))

    return render_template('eventdetail.html', event=event, form=form)  

# MVP: Handling errors (404, 500, etc.)
@main_bp.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', error_code=404, message="Page Not Found"), 404

@main_bp.errorhandler(500)
def internal_server_error(e):
    return render_template('error.html', error_code=500, message="Internal Server Error"), 500

@main_bp.errorhandler(403)
def forbidden(e):
    return render_template('error.html', error_code=403, message="Access Forbidden"), 403

@main_bp.errorhandler(401)
def unauthorized(e):
    return render_template('error.html', error_code=401, message="Unauthorized Access"), 401

# Error handler for unexpected errors (MVP: Handling errors)
@main_bp.errorhandler(Exception)
def handle_unexpected_error(e):
    return render_template('error.html', error_code=500, message="Something went wrong"), 500
