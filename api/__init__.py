from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
import os
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager

# Initialize extensions
load_dotenv(verbose=True, override=True)
db = SQLAlchemy()
mail = Mail()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)

    # Configure the app
    # Database configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('CONNECTION_STRING')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # JWT Configuration
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your_jwt_secret_key')  # Set a strong secret key

    # Mail configuration
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
    app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT'))
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')
    app.config['MAIL_RECIPIENTS'] = ['cooldeana@gmail.com']
    app.config['MAIL_DEBUG'] = True
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 3600


    for key, value in app.config.items():
        print(f"{key}: {value}")

    # Initialize extensions
    db.init_app(app)
    mail.init_app(app)
    jwt.init_app(app)

    # Register blueprints
    from api.controllers.user_controller import user_bp
    from api.controllers.communication_controller import communication_bp
    from api.controllers.error_controller import error_bp

    app.register_blueprint(user_bp, url_prefix='/api')
    app.register_blueprint(communication_bp, url_prefix='/api')
    app.register_blueprint(error_bp, url_prefix='/api')

    # Error handling
    @app.errorhandler(500)
    def internal_server_error(error):
        error_message = str(error)
        print(f"Sending internal error : {error_message}")
        send_error_email(app, error_message)
        return jsonify({'error': 'An internal server error occurred. Please try again later.'}), 500

    # Ensure tables are created
    with app.app_context():
        from api.models.user import User  # Import models
        from api.models.communication import Communication
        db.create_all()
    return app

def send_error_email(app, error_message):
    """Send error details via email."""
    with app.app_context():  # Ensure the app context is active
        msg = Message(
            subject="Internal Server Error (500)",
            recipients=app.config['MAIL_RECIPIENTS'],
            body=(
                f"An error occurred during request processing:\n\n"
                f"Request Path: {request.path}\n"
                f"Request Method: {request.method}\n"
                f"Error Message: {error_message}\n"
            )
        )
        mail.send(msg)