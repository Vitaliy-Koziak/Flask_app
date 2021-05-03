from flask import Blueprint, render_template, redirect, request, flash
from flask_login import login_required,current_user
from . import db


from website.models import User

views = Blueprint('views',__name__)

@views.route('/')
@login_required
def home():
    return render_template("home.html",user=current_user)


@views.route('/employees',methods = {'POST','GET'})
@login_required
def employees():
    surn = request.args.get('surn')
    q = request.args.get('q')
    dat_1 = request.args.get('dat_1')
    dat_2 = request.args.get('dat_2')
    if surn:
        employees = User.query.filter(User.first_name == surn).all()
        return render_template("employees_by_date.html", user=current_user, employees=employees)
    elif q:
        employees = User.query.filter(User.date == q).all()
        return render_template("employees_by_date.html",user=current_user,employees=employees)
    elif (dat_1 and dat_2 and dat_1 < dat_2):
        employees_1 = User.query.filter( User.date>=dat_1 ).all()
        employees_2 = User.query.filter( User.date<=dat_2 ).all()
        employees = set(employees_1) & set(employees_2)
        return render_template("employees_by_date.html",user=current_user,employees=employees)

    else:
        employees = User.query.order_by(User.email).all()
        return render_template("employees.html",user=current_user,employees=employees)
@views.route('/departments',methods = {'POST','GET'})
@login_required
def departments():
    departments = []
    employees = User.query.order_by(User.email).all()
    for employee in employees:
        departments.append(employee.department)


    return render_template("departments.html",user=current_user,departments=set(departments))

@views.route('/departments/<string:department>')
@login_required
def  department_more_info(department):
    employees = User.query.filter(User.department == department).all()
    avarege_salary = 0
    counter = 0
    for employee in employees:
        avarege_salary+=employee.salary
        counter+=1
    avarege_salary = round(avarege_salary/counter,3)

    return render_template("department_more_info.html",user=current_user,department=department,employees=employees,aver_sal=avarege_salary)




@views.route('/employees/<int:id>')
@login_required
def employee_more_info(id):
    employee = User.query.get(id)
    return render_template("employee_more_info.html",user=current_user,employee=employee)

@views.route('/employees/<int:id>/delete')
@login_required
def employee_delete(id):
    employee = User.query.get_or_404(id)
    try:
        db.session.delete(employee)
        db.session.commit()
        return redirect('/employees')
    except:
        return "Error ocuired"

@views.route('/employees/<int:id>/edit',methods= {'POST','GET'})
@login_required
def employee_edit(id):
    employee = User.query.get(id)

    if request.method == 'POST':
        if employee.email == request.form.get('email'):
            employee.email = request.form.get('email')
            employee.first_name = request.form.get('firstName')
            employee.department = request.form.get('department')

            try:
                db.session.commit()
                return redirect('/employees')
            except:
                return "Some error"
        else:
            user = User.query.filter_by(email=request.form.get('email')).first()
            if user:
                flash('Email already exist',category='error')
                return render_template('employee_edit.html',user=employee)


    else:
        return render_template('employee_edit.html',user=employee)

