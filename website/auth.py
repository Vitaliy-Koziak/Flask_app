from flask import Blueprint, render_template, request,flash

auth = Blueprint('auth',__name__)

@auth.route('/login',methods = ['GET','POST'])
def lodin():

    return render_template("login.html")


@auth.route('/logout')
def logout():
    return "<p>logout</p>"
@auth.route('/sign-up',methods = ['GET','POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        if len(email) < 6:
            flash('Email length must be more than 5 characters! ',category='error')
        elif len(first_name) < 3 :
            flash('Name length must be more than 3 characters! ',category='error')
        elif len(password1) < 5:
            flash('Password length must be more than 4 characters! ',category='error')
        elif password1 != password2:
            flash('Passwords do not match',category='error')
        else:
            flash('Account created!',category='success')

    return render_template('sign_up.html')
