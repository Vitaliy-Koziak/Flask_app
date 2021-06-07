import csv
from flask import Blueprint, render_template, redirect, request, send_file
from flask_login import login_required,current_user
from sqlalchemy import select
from . import db
from website.models import User,Department

views = Blueprint('views',__name__)


@views.route('/')
@login_required
def home():
    """render home.html template"""
    return render_template("home.html",user=current_user)


@views.route('/employees',methods = {'POST','GET'})
@login_required
def employees():

    surn = request.args.get('surn')
    q = request.args.get('q')
    dat_1 = request.args.get('dat_1')
    dat_2 = request.args.get('dat_2')
    sort=request.args.get('sort')
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
    elif sort:
        if sort == 'name':
            employees = User.query.order_by(User.first_name).all()
            return render_template("employees.html", user=current_user, employees=employees)
        else:
            employees = User.query.order_by(User.date).all()
            return render_template("employees.html", user=current_user, employees=employees)
    else:
        employees = User.query.order_by(User.email).all()
        temp = []
        employees_csv= []
        for item in employees:
            temp.append((str(item)))
        for item in temp:
            employees_csv.append(item.split(", "))
        with open("D:\\Python core\\Flask_app\\info.csv", "w") as file:
            writer = csv.writer(file)
            writer.writerows(employees_csv)

        return render_template("employees.html",user=current_user,employees=employees)


@views.route('/departments',methods = {'POST','GET'})
@login_required
def departments():
    """
        Receive all departments from a database and render departments
        template transferring departments there
    """
    departments = Department.query.order_by(Department.id).all()

    return render_template("departments.html",user=current_user,departments=departments)


@views.route('/departments/<string:department>')
@login_required
def  department_more_info(department):
    """
        Receive  department by  name  from a database, count avarage salary for each
        department for this I take the salary for each department  of each worker and divide by
        the number of workers in this department, than I render department_more_info template
    """
    department = Department.query.filter(Department.name == department).first()
    employees = User.query.filter(User.department_id == department.id).all()
    avarege_salary = 0
    counter = 0
    if employees:
        for employee in employees:
            avarege_salary+=employee.salary
            counter+=1
        avarege_salary = round(avarege_salary/counter,3)
    else:
        avarege_salary = 0
    return render_template("department_more_info.html",department = department,user=current_user,employees=employees,aver_sal=avarege_salary)


@views.route('/employees/<int:id>')
@login_required
def employee_more_info(id):
    """Receive  employee by id from database and  render employee_more_info template """
    employee = User.query.get(id)
    return render_template("employee_more_info.html",user=current_user,employee=employee)


@views.route('/employees/<int:id>/delete')
@login_required
def employee_delete(id):

    """
        Receive  employee by  id  from a database, delete this employee,save changes in database,
        and make redirect on employees page
    """
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
    """
        Receive  employee by  id  from a database, edit fields of this employee,save changes in database,
        and make redirect on employees page
    """
    employee = User.query.get(id)
    if request.method == 'POST':
        employee.first_name = request.form.get('firstName')
        employee.date = request.form.get('date')
        employee.salary= request.form.get('salary')

        try:
            db.session.commit()
            return redirect('/employees')
        except:
            return "Some error"
    else:
        return render_template('employee_edit.html',user=employee)


@views.route('/download')
@login_required
def download_file():
    p = 'D:\\Python core\\Flask_app\\info.csv'
    return send_file(p,as_attachment=True)


