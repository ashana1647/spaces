from market import app
from flask import render_template, redirect, url_for, flash
from market.models import Hostels, User
from market.forms import RegisterForm, LoginForm
from market import db
from flask_login import login_user, logout_user, login_required

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/search')
@login_required
def search_page():
    hostels = Hostels.query.all()
    return render_template('search.html', hostels=hostels)

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f"Account created successfully! You are now logged in as {user_to_create.username}", category='success')
        return redirect(url_for('search_page'))
    if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('search_page'))
        else:
            flash('Username and password are not match! Please try again', category='danger')

    return render_template('login.html', form=form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for("home_page"))

@app.route('/register_hostel', methods=['GET', 'POST'])
def add_hostel():
    form1 = RegisterHostel()
    if form1.validate_on_submit():
        hs_name = request.form['Hostel name']
        hs_address = request.form['Hostel Address']
        hs_contact = request.form['contact']
        hs_rent = request.form['rent']
        hs_description = request.form['description']
        rooms = request.form['no. of rooms']
        caution = request.form['caution']
        curfew = request.form['curfew']
        maps_link = request.form['maps link']
        type = request.form['Choose the hostel type']

        record = Hostels(hs_name, hs_address, hs_contact, hs_rent, hs_description, rooms, caution, curfew, maps_link, type)
        db.session.add(record)
        db.session.commit()
        return render_template('search.html')
    else:
        return render_template('registerhostel.html')

