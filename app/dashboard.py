from flask import Blueprint, render_template, session, redirect, url_for

bp = Blueprint('dashboard', __name__)

@bp.route('/dashboard')
def dashboard():
    if 'role' not in session:
        return redirect(url_for('auth.home'))

    role = session['role']
    if role == 'employee':
        return render_template('factors.html')
    elif role == 'hr':
        return render_template('hr_dashboard.html')
    elif role == 'counselor':
        return render_template('counselor_dashboard.html')
