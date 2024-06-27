from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Resource, Namespace
from flask import request

from ..services import UserService, AuthenticationService
from ..serializations import create_user_post_model, create_user_put_model, create_user_get_model, \
    create_users_get_model

user_namespace = Namespace("user", description="User related operations.")
user_post_model = create_user_post_model(user_namespace)
user_put_model = create_user_put_model(user_namespace)
user_get_model = create_user_get_model(user_namespace)
users_get_model = create_users_get_model(user_namespace)


@user_namespace.route('/')
class UserRoute(Resource):
    """
    UserRoute provides an endpoint for creating users within the application. It processes
    POST requests to create new users and uses the UserService to handle the underlying logic,
    ensuring that user data is added accurately and efficiently.

    UserService - An instance of UserService used to handle the creation of users.
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes the UserRoute with an instance of UserService. This service is crucial for handling
        the logic related to user operations, such as validating input data, interacting with the database,
        and providing a response back to the client.
        """
        super().__init__(*args, **kwargs)
        self.user_service = UserService()

    @user_namespace.expect(user_post_model)
    @user_namespace.marshal_with(user_get_model)
    def post(self):
        """
        Processes the POST request to create a new user. It expects a payload containing the user's
        first name, last name, and login. This method delegates the creation process to the UserService,
        which validates the input data and adds the new user to the database.

        On success, it returns the details of the created user.
        On failure, it returns an error message.

        :return: A tuple containing the response (either user details or error message) and the HTTP status code.
        :rtype: (flask.Response, int)
        """
        data = request.json

        try:
            user_to_create = self.user_service.create_user(data.get('first_name'), data.get('last_name'),
                                                           data.get('login'), data.get('is_admin'))
            return user_to_create, 201

        except ValueError as e:
            return {"message": str(e)}, 400


@user_namespace.route('/<int:id>')
class UserIdRoute(Resource):
    """
    UserIdRoute provides endpoints for retrieving and updating a specific user by their ID.
    It processes GET requests for retrieving user details and PUT requests for updating user information.
    This route utilizes the UserService to manage interactions with the User data model.
    It includes authorization checks to ensure that only authenticated users can access these endpoints.

    UserService - An instance of UserService used to interact with user data.
    AuthenticationService - An instance of AuthenticationService used to verify user authentication.
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes the UserIdRoute with instances of UserService and AuthenticationService.
        This service is responsible for handling the logic associated with user operations and user authentication.
        """
        super().__init__(*args, **kwargs)
        self.user_service = UserService()
        self.authentication_service = AuthenticationService()

    @user_namespace.marshal_with(user_get_model)
    @jwt_required()
    def get(self, id):
        """
        Processes the GET request to retrieve details of a specific user by their ID using the UserService.
        It includes an authorization check to ensure that the request is made by an authenticated user.

        On success, it returns the details of the specified user.
        On failure (e.g., user not found or unauthorized access), it returns an error message.

        :return: A tuple containing the response (either user details or error message) and the HTTP status code.
        :rtype: (flask.Response, int)
        """
        login = get_jwt_identity()

        try:
            self.authentication_service.is_user_authenticated(login)
            user_to_find = self.user_service.find_user(id)
            return user_to_find, 200

        except ValueError as e:
            return {"message": str(e)}, 400

    @user_namespace.expect(user_put_model)
    @user_namespace.marshal_with(user_get_model)
    @jwt_required()
    def put(self, id):
        """
        Processes the PUT request to update details of a specific user by their ID. This method uses the
        UserService to update the user's details based on the provided data.

        On success, it returns the updated user details.
        On failure (e.g., invalid data or user not found), it returns an error message.

        :param id: The identifier of the user to update.
        :type id: int

        :return: A tuple containing the response (either updated user details or error message) and the HTTP
                 status code.
        :rtype: (flask.Response, int)
        """
        data = request.json
        login = get_jwt_identity()

        try:
            self.authentication_service.is_user_admin_or_manager_of_another_user_department(login, id)
            user_to_update = self.user_service.update_user(id, data.get('new_first_name'), data.get('new_last_name'),
                                                           data.get('new_department_id'),
                                                           data.get('new_occupied_classroom_ids'))
            return user_to_update, 200

        except ValueError as e:
            return {"message": str(e)}, 400


@user_namespace.route('/all')
class UserAllRoute(Resource):
    """
    UserAllRoute provides an endpoint for retrieving all users within the system. It processes GET requests,
    returning a list of all users. The route leverages the UserService to access user data and ensures
    a comprehensive list of all users is provided.

    UserService - An instance of UserService used to retrieve a list of all users from the database.
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes the UserAllRoute with an instance of UserService. The UserService is essential for
        accessing the repository of user data and retrieving a comprehensive list of users.
        """
        super().__init__(*args, **kwargs)
        self.user_service = UserService()

    @user_namespace.marshal_with(users_get_model)
    def get(self):
        """
        Processes the GET request to retrieve a list of all users. This method utilizes the UserService to
        fetch all users from the database and return them in a list format.

        On success, it returns a list of all users along with a 200 HTTP status code.
        On failure (e.g., if an error occurs during retrieval), it returns an error message and the corresponding HTTP
        status code.

        :return: A tuple containing the response (either a list of users or an error message) and the HTTP status code.
        :rtype: (flask.Response, int)
        """
        try:
            users_to_find = self.user_service.find_all_users()
            return users_to_find, 200

        except ValueError as e:
            return {"message": str(e)}, 400
