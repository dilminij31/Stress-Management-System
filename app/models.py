from . import db
from datetime import date

class User(db.Model):
    __tablename__ = 'users'
    employee_id = db.Column(db.String(100), primary_key=True)
    name = db.Column(db.String(100))
    password = db.Column(db.String(100))
    role = db.Column(db.String(50))

class SurveyResponse(db.Model):
    __tablename__ = 'survey_responses'
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.String(100), db.ForeignKey('users.employee_id'))
    job_stress_score = db.Column(db.Integer)
    organizational_factors_score = db.Column(db.Integer)
    personal_factors_score = db.Column(db.Integer)
    phq9_score = db.Column(db.Integer)
    phq9_severity = db.Column(db.String(100))
    treatment_action = db.Column(db.String(200))

class FollowUp(db.Model):
    __tablename__ = 'follow_ups'

    id = db.Column(db.Integer, primary_key=True)
    employee_number = db.Column(db.String(100), db.ForeignKey('users.employee_id'))
    counselor_name = db.Column(db.String(100))  # The name of the counselor conducting the follow-up
    follow_up_date = db.Column(db.Date, default=date.today)  # Date of follow-up
    follow_up_status = db.Column(db.String(50), default='Pending')  # Status of the follow-up (e.g., Pending, Completed)
    notes = db.Column(db.Text, nullable=True)  # Optional notes from the counselor

    # Optional relationship if you need to access employee details
    employee = db.relationship('User', backref='follow_ups', lazy=True)


# Function to get user by employee number and role
def get_user(employee_number, role):
    return User.query.filter_by(employee_id=employee_number, role=role).first()

# Function to insert survey responses (for job stress, organizational, personal factors)
def insert_survey(employee_number, job_stress_score, org_factors_score, personal_factors_score):
    survey_response = SurveyResponse.query.filter_by(employee_id=employee_number).first()
    if survey_response:
        # Update existing survey response
        survey_response.job_stress_score = job_stress_score
        survey_response.organizational_factors_score = org_factors_score
        survey_response.personal_factors_score = personal_factors_score
    else:
        # Insert a new survey response
        survey_response = SurveyResponse(
            employee_id=employee_number,
            job_stress_score=job_stress_score,
            organizational_factors_score=org_factors_score,
            personal_factors_score=personal_factors_score
        )
        db.session.add(survey_response)
    db.session.commit()

# Function to insert PHQ-9 survey response
def insert_phq9(employee_number, phq9_score, phq9_severity, treatment_action):
    survey_response = SurveyResponse.query.filter_by(employee_id=employee_number).first()
    if survey_response:
        # Update existing PHQ-9 details
        survey_response.phq9_score = phq9_score
        survey_response.phq9_severity = phq9_severity
        survey_response.treatment_action = treatment_action
    else:
        # Insert new PHQ-9 survey response
        survey_response = SurveyResponse(
            employee_id=employee_number,
            phq9_score=phq9_score,
            phq9_severity=phq9_severity,
            treatment_action=treatment_action
        )
        db.session.add(survey_response)
    db.session.commit()

