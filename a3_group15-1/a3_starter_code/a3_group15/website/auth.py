from flask import Blueprint, flash, render_template, request, url_for, redirect
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user
from .models import User
from .forms import LoginForm, RegistrationForm
from . import db


# Create a blueprint - make sure all BPs have unique names
auth_bp = Blueprint('auth', __name__)

# this is a hint for a login function
@auth_bp.route('/login', methods=['GET', 'POST'])
# view function
def login():
    login_form = LoginForm()
    error = None
    if login_form.validate_on_submit():
        user_name = login_form.user_name.data
        password = login_form.password.data
        user = db.session.scalar(db.select(User).where(User.name==user_name))
        if user is None:
            error = 'Incorrect user name'
        elif not check_password_hash(user.password_hash, password): # takes the hash and cleartext password
            error = 'Incorrect password'
        if error is None:
            login_user(user)
            nextp = request.args.get('next') # this gives the url from where the login page was accessed
            print(nextp)
            if next is None or not nextp.startswith('/'):
                return redirect(url_for('index'))
            return redirect(nextp)
        else:
            flash(error)
    return render_template('user.html', form=login_form, heading='Login')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()  
    flash('You have been logged out.', 'success') 
    return redirect(url_for('auth.login'))  # Redirect to the login page after logging out

## register
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    reg_form = RegistrationForm()
    if reg_form.validate_on_submit():  # verify
        email = reg_form.email.data
        password = reg_form.password.data
        first_name = reg_form.first_name.data
        last_name = reg_form.last_name.data

        # check the email is available or not
        if User.find_by_email(email):
            flash('the email is already in use, try another email.', 'danger')
            return redirect(url_for('auth.login'))

        User.create(first_name,last_name,email, password)
        flash('Register sucessfully!', 'success')
        return redirect(url_for('login.home'))  # back to login

    return render_template('register.html', form=reg_form)

