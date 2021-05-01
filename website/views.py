from flask import Blueprint, render_template
from flask_login import login_required,current_user

from website.models import User

views = Blueprint('views',__name__)

@views.route('/')
@login_required
def home():
    return render_template("home.html",user=current_user)


@views.route('/employees')
@login_required
def employees():
    employees = User.query.order_by(User.email).all()
    return render_template("employees.html",user=current_user,employees=employees)

@views.route('/employees/<int:id>')
@login_required
def employee_more_info(id):
    employee = User.query.get(id)
    return render_template("employee_more_info.html",user=current_user,employee=employee)