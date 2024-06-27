from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Resource, Namespace
from flask import request

from ..services import ClassroomService, AuthenticationService
from ..serializations import create_classroom_post_model, create_classroom_put_model, create_classroom_get_model, \
    create_classrooms_get_model

classroom_namespace = Namespace("classroom", description="Classroom related operations.")
classroom_post_model = create_classroom_post_model(classroom_namespace)
classroom_put_model = create_classroom_put_model(classroom_namespace)
classroom_get_model = create_classroom_get_model(classroom_namespace)
classrooms_get_model = create_classrooms_get_model(classroom_namespace)


@classroom_namespace.route('/')
class ClassroomRoute(Resource):
    """
    ClassroomRoute provides an endpoint for creating classrooms within the application. It processes POST
    requests to create new classrooms and uses the ClassroomService and AuthenticationService to handle the
    underlying logic, ensuring that classroom data is added accurately and efficiently and that the request
    comes from an authenticated admin user.

    ClassroomService - An instance of ClassroomService used to handle the creation of classrooms.
    AuthenticationService - An instance of AuthenticationService used to handle authentication and admin checks.
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes the ClassroomRoute with instances of ClassroomService and AuthenticationService.
        These services are crucial for handling the logic related to classroom operations and user authentication,
        such as validating input data, interacting with the database, verifying admin privileges,
        and providing a structured response back to the client.
        """
        super().__init__(*args, **kwargs)
        self.classroom_service = ClassroomService()
        self.authentication_service = AuthenticationService()

    @classroom_namespace.expect(classroom_post_model)
    @classroom_namespace.marshal_with(classroom_get_model)
    @jwt_required()
    def post(self):
        """
        Processes the POST request to create a new classroom. It expects a payload containing the necessary
        details for the classroom. Before proceeding, it checks if the requesting user is an administrator.
        This method delegates the creation process to the ClassroomService, which validates the input data
        and adds the new classroom to the database if the user is verified as an admin.

        On success, it returns the details of the created classroom.
        On failure, it returns an error message.

        :return: A tuple containing the response (either classroom details or error message) and the HTTP status code.
        :rtype: (flask.Response, int)
        """
        data = request.json
        login = get_jwt_identity()

        try:
            self.authentication_service.is_user_admin(login)
            classroom_to_create = self.classroom_service.create_classroom(data.get('name'), data.get('floor'),
                                                                          data.get('is_private'))
            return classroom_to_create, 201

        except ValueError as e:
            return {"message": str(e)}, 400


@classroom_namespace.route('/<int:id>')
class ClassroomIdRoute(Resource):
    """
    ClassroomIdRoute provides endpoints for retrieving and updating a specific classroom by its ID.
    It handles GET requests for retrieving classroom details and PUT requests for updating classroom information.
    This route utilizes the ClassroomService to manage the interaction with the Classroom data model, ensuring
    efficient and consistent access and modification of classroom records. Additionally, it leverages the
    AuthenticationService to ensure that only authenticated users can access and modify the data, providing
    an extra layer of security and integrity.

    ClassroomService - An instance of ClassroomService used to interact with classroom data.
    AuthenticationService - An instance of AuthenticationService used to verify the authentication status of users
    making requests to this route.
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes the ClassroomIdRoute with an instance of ClassroomService. This service is responsible for
        handling the logic associated with classroom operations, such as retrieving and updating classroom details,
        thereby abstracting these complexities from the route itself. AuthenticationService is used to verify
        the authentication status of users making requests to this route.
        """
        super().__init__(*args, **kwargs)
        self.classroom_service = ClassroomService()
        self.authentication_service = AuthenticationService()

    @classroom_namespace.marshal_with(classroom_get_model)
    @jwt_required()
    def get(self, id):
        """
        Processes the GET request to retrieve details of a specific classroom by its ID using the ClassroomService.

        On success, it returns the details of the specified classroom.
        On failure (e.g., classroom not found), it returns an error message.

        :param id: The identifier of the classroom to retrieve.
        :type id: int

        :return: A tuple containing the response (either classroom details or error message) and the HTTP status code.
        :rtype: (flask.Response, int)
        """
        login = get_jwt_identity()

        try:
            self.authentication_service.is_user_authenticated(login)
            classroom_to_find = self.classroom_service.find_classroom(id)
            return classroom_to_find, 200

        except ValueError as e:
            return {"message": str(e)}, 400

    @classroom_namespace.expect(classroom_put_model)
    @classroom_namespace.marshal_with(classroom_get_model)
    @jwt_required()
    def put(self, id):
        """
        Processes the PUT request to update details of a specific classroom by its ID. This method uses the
        ClassroomService to update the classroom's details based on the provided data.

        On success, it returns the updated classroom details.
        On failure (e.g., invalid data or classroom not found), it returns an error message.

        :param id: The identifier of the classroom to update.
        :type id: int

        :return: A tuple containing the response (either updated classroom details or error message) and the
                 HTTP status code.
        :rtype: (flask.Response, int)
        """
        data = request.json
        login = get_jwt_identity()

        try:
            self.authentication_service.is_user_admin_or_manager_of_department_by_classroom(login, id)
            classroom_to_update = self.classroom_service.update_classroom(id, data.get('new_name'),
                                                                          data.get('new_building_id'),
                                                                          data.get('new_department_id'),
                                                                          data.get('new_manager_id'),
                                                                          data.get('new_is_private'))
            return classroom_to_update, 200

        except ValueError as e:
            return {"message": str(e)}, 400


@classroom_namespace.route('/all/non-private')
class ClassroomAllNonPrivateRoute(Resource):
    """
    ClassroomAllNonPrivateRoute provides an endpoint for retrieving all non-private classrooms within the system.
    It processes GET requests, returning a list of all non-private classrooms. This route uses the ClassroomService
    to access classroom data and ensures a comprehensive list of all non-private classrooms is provided.

    ClassroomService - An instance of ClassroomService used to retrieve a list of all non-private classrooms from the
    database. This service is critical for ensuring that all interactions with classroom data are handled efficiently
    and consistently, offering a simplified interface for the route to interact with non-private classroom data.
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes the ClassroomAllNonPrivateRoute with an instance of ClassroomService. The ClassroomService is
        essential for accessing the repository of classroom data and retrieving a comprehensive list of non-private
        classrooms.
        """
        super().__init__(*args, **kwargs)
        self.classroom_service = ClassroomService()

    @classroom_namespace.marshal_with(classrooms_get_model)
    def get(self):
        """
        Processes the GET request to retrieve a list of all non-private classrooms. This method utilizes the
        ClassroomService to fetch all non-private classrooms from the database and return them in a list format.

        On success, it returns a list of all non-private classrooms along with a 200 HTTP status code.
        On failure (e.g., if an error occurs during retrieval), it returns an error message and the corresponding
        HTTP status code.

        :return: A tuple containing the response (either a list of non-private classrooms or an error message) and the
                 HTTP status code.
        :rtype: (flask.Response, int)
        """
        try:
            classrooms_to_find = self.classroom_service.find_all_non_private_classrooms()
            return classrooms_to_find, 200

        except ValueError as e:
            return {"message": str(e)}, 400


@classroom_namespace.route('/all')
class ClassroomAllRoute(Resource):
    """
    ClassroomAllRoute provides an endpoint for retrieving all classrooms within the system. It processes GET requests,
    returning a list of all classrooms. This route uses the ClassroomService to access classroom data and ensures
    a comprehensive list of all classrooms is provided.

    ClassroomService - An instance of ClassroomService used to retrieve a list of all classrooms from the database.
    AuthenticationService - An instance of AuthenticationService used to verify user authentication.
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes the ClassroomAllRoute with instances of ClassroomService and AuthenticationService. These services
        are essential for accessing the repository of classroom data, retrieving a comprehensive list of classrooms,
        and verifying user authentication.
        """
        super().__init__(*args, **kwargs)
        self.classroom_service = ClassroomService()
        self.authentication_service = AuthenticationService()

    @classroom_namespace.marshal_with(classrooms_get_model)
    @jwt_required()  # Добавлен декоратор для проверки JWT токена
    def get(self):
        """
        Processes the GET request to retrieve a list of all classrooms. This method utilizes the ClassroomService to
        fetch all classrooms from the database and return them in a list format. It includes an authorization check
        to ensure that the request is made by an authenticated user.

        On success, it returns a list of all classrooms along with a 200 HTTP status code.
        On failure (e.g., if an error occurs during retrieval), it returns an error message and the corresponding
        HTTP status code.

        :return: A tuple containing the response (either a list of classrooms or an error message) and the
                 HTTP status code.
        :rtype: (flask.Response, int)
        """
        login = get_jwt_identity()

        try:
            self.authentication_service.is_user_authenticated(login)
            classrooms_to_find = self.classroom_service.find_all_classrooms()
            return classrooms_to_find, 200

        except ValueError as e:
            return {"message": str(e)}, 400
