from flask import Flask
from validator import MyRequestValidator
from core import db, oauth
from views import yoloapi


def create_app():
    app = Flask(__name__)

    # Update configuration
    app.config.update({
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///db.sqlite',
        'DEBUG': True
    })

    # Initialize extensions on the application
    db.init_app(app)
    oauth.init_app(app)
    oauth._validator = MyRequestValidator()

    # Register views on the application
    app.register_blueprint(yoloapi)

    return app

if __name__ == '__main__':

    # We like flask_oauthlib logging for this application
    import logging
    logger = logging.getLogger('flask_oauthlib')
    logger.addHandler(logging.StreamHandler())
    logger.setLevel(logging.DEBUG)

    # Create app, create SQL schemes in db and run the application
    app = create_app()
    db.create_all(app=app)
    app.run()
