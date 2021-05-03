import random
from flask import Blueprint, render_template, request,flash,redirect,url_for
from .models import User
from werkzeug.security import generate_password_hash,check_password_hash
from . import db
from flask_login import login_user,login_required,logout_user,current_user
auth = Blueprint('auth',__name__)
@auth.route('/login',methods = ['GET','POST'])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            if user.password == password :
                flash("Logged in succesfully!",category='success')
                login_user(user,remember=True)
                return redirect(url_for("views.home"))
            else:
                flash("Incorrect password, try again!",category='error')
        else:
            flash("Email does not exist!",category='error')
    return render_template("login.html",user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
@auth.route('/sign-up',methods = ['GET','POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        date = request.form.get('date')
        department = request.form.get('department')
        user = User.query.filter_by(email=email).first()
        em = email.split("@")
        if user:
            flash("Email already exist!",category='error')

        elif len(email) < 6:
            flash('Email length must be more than 5 characters! ',category='error')
        elif em[1] != 'epam.com':
            flash('Email wronf format! ', category='error')
        elif len(first_name) < 3 :
            flash('Name length must be more than 3 characters! ',category='error')
        elif len(password1) < 5:
            flash('Password length must be more than 4 characters! ',category='error')
        elif password1 != password2:
            flash('Passwords do not match',category='error')

        else:
            new_user = User(email=email,
                            first_name=first_name,
                            password=password1,
                            date=date,
                            department=department,
                            salary = set_salary())
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!',category='success')
            return redirect(url_for("views.home"))

    return render_template('sign_up.html',user=current_user)

def set_salary()->int:
    base_salary = 500
    return int(base_salary * random.uniform(0.7,10))