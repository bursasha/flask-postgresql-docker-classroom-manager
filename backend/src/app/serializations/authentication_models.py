from flask_restx import fields

from .user_models import create_user_get_model


def create_login_post_model(namespace):
    """
    Defines and returns the model for the login POST request. This model specifies the structure and data types
    of the request payload expected by the login endpoint.

    :return: A Flask-RESTx model object representing the structure of a login POST request.
    :rtype: flask_restx.fields.Model
    """
    return namespace.model(
        "LoginPost", {
            "login": fields.String(description="The unique login identifier for the user.", required=True)
        })


def create_refresh_get_model(namespace):
    """
    Defines and returns the model for the refresh GET response. This model specifies the structure and data types
    of the response payload provided by the refresh endpoint.

    :return: A Flask-RESTx model object representing the structure of a refresh GET response.
    :rtype: flask_restx.fields.Model
    """
    return namespace.model(
        "RefreshGet", {
            "access_token": fields.String(description="The new JWT access token for the user.")
        })


def create_login_get_model(namespace):
    """
    Defines and returns the model for the login GET response. This model specifies the structure and data types
    of the response payload provided by the login endpoint.

    :return: A Flask-RESTx model object representing the structure of a login GET response.
    :rtype: flask_restx.fields.Model
    """
    user_model = create_user_get_model(namespace)
    return namespace.model(
        "LoginGet", {
            "user": fields.Nested(user_model, description="Serialized user data."),
            "access_token": fields.String(description="The JWT access token for the user."),
            "refresh_token": fields.String(description="The JWT refresh token for the user.")
        })
