from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    app.secret_key = 'supersecretkey'

    db.init_app(app)

    # Register Blueprints (routes)
    from .routes import main
    from .auth import auth
    from .survey import survey
    from .hr import hr
    from .counselor import counselor

    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(survey)
    app.register_blueprint(hr)
    app.register_blueprint(counselor)

    return app
