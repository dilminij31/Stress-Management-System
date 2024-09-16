from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models import get_user

bp = Blueprint('auth', __name__)

@bp.route('/')
def home():
    return render_template('login.html')

@bp.route('/login', methods=['POST'])
def login():
    employee_number = request.form.get('employee_number')
    password = request.form.get('password')
    role = request.form.get('role')

    user = get_user(employee_number, role)

    if user and user[2] == password:
        session['employee_number'] = user[0]
        session['role'] = user[3]
        return redirect(url_for('dashboard.dashboard'))
    else:
        flash('Invalid credentials, please try again.')
        return redirect(url_for('auth.home'))
