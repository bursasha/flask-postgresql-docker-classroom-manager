from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate, upgrade
from flask_restx import Api

from .orm import orm
from .routes import authentication_namespace, building_namespace, classroom_namespace, department_namespace, \
    request_namespace, user_namespace


def create_app(config):
    """
    Create a Flask application instance.

    This function handles the setup and initialization of major components for the app, including:

    - Flask: The core framework.
    - CORS (Cross-Origin Resource Sharing): Handles potential issues from making
      requests to the server from different origins.
    - Flask-SQLAlchemy: Initializes the database component.
    - Flask-Migrate: Handles database migrations.
    - JWTManager: Handles JSON Web Tokens for authentication.
    - Flask-Restx and Namespaces: For easy creation of REST APIs.
    - Shell context: Simplifies shell context for Flask shell.

    :param config: The configuration object for Flask.
    :return: Flask app instance.
    """
    # Create Flask app instance.
    app = Flask(__name__)

    # Load configs from configs object.
    app.config.from_object(config)

    # Enable CORS for the app.
    CORS(app, supports_credentials=True)

    # Initialize SQLAlchemy with app.
    orm.init_app(app)

    # Initialize Flask-Migrate for handling migrations.
    Migrate(app, orm)

    with app.app_context():
        # Apply database migrations.
        upgrade()

    # Setup the Flask-JWT-Extended extension.
    JWTManager(app)

    # Initialize Flask-Restx Api.
    api = Api(app, doc='/docs')

    # Add namespaces.
    api.add_namespace(authentication_namespace)
    api.add_namespace(building_namespace)
    api.add_namespace(classroom_namespace)
    api.add_namespace(department_namespace)
    api.add_namespace(request_namespace)
    api.add_namespace(user_namespace)

    return app
