import os

class Config:
    SECRET_KEY = 'supersecretkey'
    
    # Example with specific MySQL credentials
    SQLALCHEMY_DATABASE_URI = 'mysql://root:Sidj@312@localhost/stress_management_db'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
