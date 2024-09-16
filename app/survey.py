from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from ..app import insert_survey
from ..app import insert_phq9

bp = Blueprint('survey', __name__)

@bp.route('/submit_survey', methods=['POST'])
def submit_survey():
    employee_number = session.get('employee_number')
    if not employee_number:
        return redirect(url_for('auth.home'))

    # Get survey responses
    job_stress_score = sum([int(request.form.get(f'q{i}', '0')) for i in range(1, 5)])
    org_factors_score = sum([int(request.form.get(f'q{i}', '0')) for i in range(5, 9)])
    personal_factors_score = sum([int(request.form.get(f'q{i}', '0')) for i in range(9, 13)])

    # Insert survey into the database
    insert_survey(employee_number, job_stress_score, org_factors_score, personal_factors_score)

    return redirect(url_for('survey.assesment'))

@bp.route('/assesment')
def assessment():
    return render_template('assesment.html')

# Route to submit the PHQ-9 assessment
@bp.route('/submit_assessment', methods=['POST'])
def submit_assessment():
    employee_number = session.get('employee_number')
    if not employee_number:
        flash('You must be logged in to submit an assessment.')
        return redirect(url_for('auth.home'))

    # Collect PHQ-9 responses
    phq9_responses = []
    for i in range(1, 10):
        q_value = request.form.get(f'q{i}', '0')
        phq9_responses.append(int(q_value))

    # Calculate total PHQ-9 score
    phq9_score = sum(phq9_responses)

    # Interpret the PHQ-9 score
    def interpret_phq9(score):
        if score <= 4:
            return "None-minimal", "None"
        elif 5 <= score <= 9:
            return "Mild", "Watchful waiting; repeat PHQ-9 at follow-up"
        elif 10 <= score <= 14:
            return "Moderate", "Treatment plan, considering counseling, follow-up, and/or pharmacotherapy"
        elif 15 <= score <= 19:
            return "Moderately Severe", "Active treatment with pharmacotherapy and/or psychotherapy"
        else:
            return "Severe", "Immediate initiation of pharmacotherapy and referral to a mental health specialist"

    phq9_severity, treatment_action = interpret_phq9(phq9_score)

    # Insert or update PHQ-9 data in the database
    insert_phq9(employee_number, phq9_score, phq9_severity, treatment_action)

    # Redirect to the result page
    return redirect(url_for('survey.result', score=phq9_score, severity=phq9_severity, recommendation=treatment_action))

# Render the PHQ-9 assessment form
@bp.route('/assesment')
def assessment():
    return render_template('assesment.html')

# Render the result page (redirected after submission)
@bp.route('/result')
def result():
    score = request.args.get('score')
    severity = request.args.get('severity')
    recommendation = request.args.get('recommendation')
    return render_template('result.html', score=score, severity=severity, recommendation=recommendation)

