from flask import Blueprint, render_template, session, redirect, url_for, flash, request  # Added request import
from .models import FollowUp  # Assuming FollowUp model is defined in models.py
from . import db  # SQLAlchemy instance

counselor = Blueprint('counselor', __name__)

# Counselor Dashboard Route
@counselor.route('/counselor_dashboard')
def counselor_dashboard():
    # Check if the logged-in user is a counselor
    if session.get('role') != 'counselor':
        flash('Access Denied. You must be a counselor to view this page.')
        return redirect(url_for('main.login'))

    # Fetch follow-up data related to counselor from the database
    counselor_number = session.get('employee_number')  # Assuming session holds counselor's employee number
    if not counselor_number:
        flash('Invalid session data. Please log in again.')
        return redirect(url_for('main.login'))

    follow_ups = FollowUp.query.filter_by(counselor_name=counselor_number).order_by(FollowUp.follow_up_date.desc()).all()

    return render_template('counselor_dashboard.html', follow_ups=follow_ups)

# View Details of a Specific Follow-up
@counselor.route('/follow_up/<int:follow_up_id>')
def follow_up_detail(follow_up_id):
    # Check if the logged-in user is a counselor
    if session.get('role') != 'counselor':
        flash('Access Denied. You must be a counselor to view this page.')
        return redirect(url_for('main.login'))

    # Fetch the specific follow-up details
    follow_up = FollowUp.query.get_or_404(follow_up_id)
    
    return render_template('follow_up_detail.html', follow_up=follow_up)

# Mark a Follow-Up as Completed
@counselor.route('/complete_follow_up/<int:follow_up_id>', methods=['POST'])
def complete_follow_up(follow_up_id):
    # Check if the logged-in user is a counselor
    if session.get('role') != 'counselor':
        flash('Access Denied. You must be a counselor to view this page.')
        return redirect(url_for('main.login'))

    # Fetch and update the follow-up status
    follow_up = FollowUp.query.get_or_404(follow_up_id)
    follow_up.follow_up_status = 'Completed'
    db.session.commit()

    flash('Follow-up marked as completed.')
    return redirect(url_for('counselor.counselor_dashboard'))

# Add Notes to a Follow-up
@counselor.route('/add_notes/<int:follow_up_id>', methods=['POST'])
def add_notes(follow_up_id):
    # Check if the logged-in user is a counselor
    if session.get('role') != 'counselor':
        flash('Access Denied. You must be a counselor to view this page.')
        return redirect(url_for('main.login'))

    # Fetch the follow-up and add notes
    follow_up = FollowUp.query.get_or_404(follow_up_id)
    follow_up.notes = request.form.get('notes')
    db.session.commit()

    flash('Notes added successfully.')
    return redirect(url_for('counselor.follow_up_detail', follow_up_id=follow_up_id))
