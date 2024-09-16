from flask import Blueprint, render_template, session, redirect, url_for
from .models import FollowUp  # Import the FollowUp model
from . import db  # SQLAlchemy instance

hr = Blueprint('hr', __name__)

@hr.route('/hr_dashboard')
def hr_dashboard():
    # Check if the logged-in user is HR
    if session.get('role') != 'hr':
        return redirect(url_for('main.login'))  # Redirect to login if not HR

    # Fetch follow-up data from the database using SQLAlchemy ORM
    follow_ups = FollowUp.query.order_by(FollowUp.follow_up_date.desc()).all()

    return render_template('hr_dashboard.html', results=follow_ups)
