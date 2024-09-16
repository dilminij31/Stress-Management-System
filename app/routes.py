from flask import Blueprint, render_template, request, redirect, url_for, session
from .models import db, User

# Define the blueprint for the main routes
main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('login.html')

@main.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        employee_id = request.form.get('employee_id')
        password = request.form.get('password')

        # Validate login with the database
        user = User.query.filter_by(employee_id=employee_id).first()
        if user and user.password == password:
            session['employee_id'] = employee_id
            return redirect(url_for('main.dashboard'))
        else:
            return 'Invalid Credentials'
    return render_template('login.html')

@main.route('/dashboard')
def dashboard():
    if 'employee_id' not in session:
        return redirect(url_for('main.login'))
    return 'Dashboard for logged-in user'
