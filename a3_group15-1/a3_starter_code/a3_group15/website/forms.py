from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, IntegerField, FloatField, SubmitField, DateField, TimeField
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange

# MVP: User table storing information about users, including their login credentials
class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=150)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=150)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=150)])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=6),
        EqualTo('confirm_password', message='Passwords must match')
    ])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Create Account')

# MVP: Event table containing event details
class EventForm(FlaskForm):
    name = StringField('Event Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    date = DateField('Event Date', format='%Y-%m-%d', validators=[DataRequired()])
    start_time = TimeField('Start Time', validators=[DataRequired()])
    end_time = TimeField('End Time', validators=[DataRequired()])
    venue = StringField('Venue', validators=[DataRequired()])
    price = FloatField('Ticket Price', validators=[DataRequired(), NumberRange(min=0.0)])
    total_tickets = IntegerField('Total Tickets', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Create Event')

# MVP: Booking table storing price, quantity, and date
class BookingForm(FlaskForm):
    quantity = IntegerField('Number of Tickets', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Book Tickets')

# MVP: Comments table
class CommentForm(FlaskForm):
    content = TextAreaField('Leave a Comment', validators=[DataRequired(), Length(min=1, max=500)])
    submit = SubmitField('Submit Comment')



# MVP: Login form 
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=150)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Login')