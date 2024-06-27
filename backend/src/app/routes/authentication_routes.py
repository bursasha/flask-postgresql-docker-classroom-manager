from flask_restx import Resource, Namespace
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..services import AuthenticationService
from ..serializations import create_login_post_model, create_login_get_model, create_refresh_get_model


authentication_namespace = Namespace("authentication", description="Authentication related operations.")
login_post_model = create_login_post_model(authentication_namespace)
login_get_model = create_login_get_model(authentication_namespace)
refresh_get_model = create_refresh_get_model(authentication_namespace)


@authentication_namespace.route('/login')
class AuthenticationLoginRoute(Resource):
    """
    AuthenticationLoginRoute provides an endpoint for user authentication. It processes POST requests, validating user
    credentials against the UserRepository, and on successful authentication, it generates and returns JWT access and
    refresh tokens.

    The route utilizes the AuthenticationService to abstract the complexities of the authentication process,
    including token generation and validation. This separation of concerns makes the route solely responsible for
    handling HTTP requests and delegating authentication logic to the AuthenticationService.

    AuthenticationService - An instance of AuthenticationService used to authenticate users.
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes the AuthenticationLoginRoute with an instance of AuthenticationService. The AuthenticationService
        is essential for managing the complexities of user authentication, including verifying user credentials, and
        generating JWT access and refresh tokens upon successful login.
        """
        super().__init__(*args, **kwargs)
        self.authentication_service = AuthenticationService()

    @authentication_namespace.expect(login_post_model)
    @authentication_namespace.marshal_with(login_get_model)
    def post(self):
        """
        Processes the POST request to authenticate a user using their login. This method utilizes the
        AuthenticationService to verify the login and, upon successful authentication, generate JWT access and
        refresh tokens.

        On successful authentication, it returns JWT access and refresh tokens.
        On failure, it returns an error message.

        :return: A tuple containing the response (either tokens or error message) and the HTTP status code.
        :rtype: (flask.Response, int)
        """
        login = request.json.get('login')

        try:
            response = self.authentication_service.authenticate_user(login)
            return response, 200

        except ValueError as e:
            return {"message": str(e)}, 401


@authentication_namespace.route('/logout')
class AuthenticationLogoutRoute(Resource):
    """
    AuthenticationLogoutRoute provides an endpoint for user logout. It handles POST requests to terminate the user
    session by unsetting JWT cookies. This route leverages the AuthenticationService to manage the logout process,
    ensuring that the user's session is securely closed, and their authentication tokens are invalidated.

    AuthenticationService - An instance of AuthenticationService used to manage the logout process.
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes the AuthenticationLogoutRoute with an instance of AuthenticationService. The AuthenticationService
        is used to manage the complexities of the logout process, including unsetting JWT cookies and ensuring the user
        session is securely terminated.
        """
        super().__init__(*args, **kwargs)
        self.authentication_service = AuthenticationService()

    @jwt_required()
    def post(self):
        """
        Processes the POST request to logout a user. This method uses the AuthenticationService to unset the JWT
        cookies, effectively logging the user out.

        It requires a valid JWT access token to identify the current user.
        On successful logout, it returns a success message.
        On failure, it returns an error message.

        :return: A tuple containing the response (either a success message or error message) and the HTTP status code.
        :rtype: (flask.Response, int)
        """
        login = get_jwt_identity()

        try:
            response = self.authentication_service.logout_user(login)
            return response, 200

        except ValueError as e:
            return {"message": str(e)}, 401


@authentication_namespace.route('/refresh')
class AuthenticationRefreshRoute(Resource):
    """
    AuthenticationRefreshRoute provides an endpoint for refreshing JWT access tokens using a valid refresh token. This
    route processes POST requests and uses the AuthenticationService to validate the refresh token and generate a new
    access token. This ensures that users can continue their session without re-authentication, maintaining a balance
    between security and convenience.

    AuthenticationService - An instance of AuthenticationService used to handle the refreshing of access tokens.
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes the AuthenticationRefreshRoute with an instance of AuthenticationService. The AuthenticationService
        is crucial for validating the refresh token and generating a new access token. It abstracts the complexities
        involved in the token refresh process, allowing this route to focus solely on handling HTTP requests and
        responses.
        """
        super().__init__(*args, **kwargs)
        self.authentication_service = AuthenticationService()

    @authentication_namespace.marshal_with(refresh_get_model)
    @jwt_required(refresh=True)
    def post(self):
        """
        Processes the POST request to refresh an access token using a provided refresh token. This method relies on
        the AuthenticationService to validate the refresh token and generate a new access token.

        On success, it returns a new access token.
        On failure, it returns an error message.

        :return: A tuple containing the response (either a new access token or error message) and the HTTP status code.
        :rtype: (flask.Response, int)
        """
        refresh_token = request.cookies.get('refresh_token')

        try:
            response = self.authentication_service.refresh_access_token(refresh_token)
            return response, 200

        except ValueError as e:
            return {"message": str(e)}, 401
