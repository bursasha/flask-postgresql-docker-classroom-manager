from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Resource, Namespace
from flask import request

from ..services import DepartmentService, AuthenticationService
from ..serializations import create_department_post_model, create_department_put_model, create_department_get_model, \
    create_departments_get_model

department_namespace = Namespace("department", description="Department related operations.")
department_post_model = create_department_post_model(department_namespace)
department_put_model = create_department_put_model(department_namespace)
department_get_model = create_department_get_model(department_namespace)
departments_get_model = create_departments_get_model(department_namespace)


@department_namespace.route('/')
class DepartmentCreateRoute(Resource):
    """
    DepartmentCreateRoute provides an endpoint for creating new departments. It processes POST requests with department
    details and uses the DepartmentService to add the department to the system. It requires the user to be an
    administrator to perform the operation.

    DepartmentService - An instance of DepartmentService used to handle the creation of departments.
    AuthenticationService - An instance of AuthenticationService used to verify the user's admin status.
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes the DepartmentCreateRoute with instances of DepartmentService and AuthenticationService.
        The services are crucial for handling the logic related to department operations and user authentication,
        such as validating input data, verifying admin privileges, interacting with the database,
        and providing a response back to the client.
        """
        super().__init__(*args, **kwargs)
        self.department_service = DepartmentService()
        self.authentication_service = AuthenticationService()

    @department_namespace.expect(department_post_model)
    @department_namespace.marshal_with(department_get_model)
    @jwt_required()
    def post(self):
        """
        Processes the POST request to create a new department. It expects a payload containing the department's full
        name and code name. Before proceeding, it checks if the requesting user is an administrator.
        This method delegates the creation process to the DepartmentService, which validates the input data and adds
        the new department to the database if the user is verified as an admin.

        On success, it returns the details of the created department.
        On failure, it returns an error message.

        :return: A tuple containing the response (either department details or error message) and the HTTP status code.
        :rtype: (flask.Response, int)
        """
        data = request.json
        login = get_jwt_identity()

        try:
            self.authentication_service.is_user_admin(login)
            department_to_create = self.department_service.create_department(data.get('full_name'),
                                                                             data.get('code_name'))
            return department_to_create, 201

        except ValueError as e:
            return {"message": str(e)}, 400


@department_namespace.route('/<int:id>')
class DepartmentIdRoute(Resource):
    """
    DepartmentIdRoute provides endpoints for retrieving and updating a specific department by its ID.
    It processes GET requests for retrieving department details and PUT requests for updating department information.
    It includes authorization checks to ensure that only authenticated users can access these endpoints.

    DepartmentService - An instance of DepartmentService used to interact with department data.
    AuthenticationService - An instance of AuthenticationService used to verify user authentication.
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes the DepartmentIdRoute with instances of DepartmentService and AuthenticationService.
        This service is responsible for handling the logic associated with department operations and user
        authentication.
        """
        super().__init__(*args, **kwargs)
        self.department_service = DepartmentService()
        self.authentication_service = AuthenticationService()

    @department_namespace.marshal_with(department_get_model)
    @jwt_required()
    def get(self, id):
        """
        Processes the GET request to retrieve details of a specific department by its ID. It includes an authorization
        check to ensure that the request is made by an authenticated user.

        On success, it returns the details of the specified department.
        On failure (e.g., department not found or unauthorized access), it returns an error message.

        :return: A tuple containing the response (either department details or error message) and the HTTP status code.
        :rtype: (flask.Response, int)
        """
        login = get_jwt_identity()

        try:
            self.authentication_service.is_user_authenticated(login)
            department_to_find = self.department_service.find_department(id)
            return department_to_find, 200

        except ValueError as e:
            return {"message": str(e)}, 400

    @department_namespace.expect(department_put_model)
    @department_namespace.marshal_with(department_get_model)
    @jwt_required()
    def put(self, id):
        """
        Processes the PUT request to update details of a specific department by its ID. This method uses the
        DepartmentService to update the department's full name, code name, and/or manager based on the provided data.

        Before proceeding, it checks if the requesting user is an administrator. Only administrators are allowed to
        update  department details. If the user is not an administrator, the method returns an access denied error.

        On success, it returns the updated department details.
        On failure (e.g., invalid data or department not found, or user not an admin), it returns an error message.

        :param id: The identifier of the department to update.
        :type id: int

        :return: A tuple containing the response (either updated department details or error message) and the
                 HTTP status code.
        :rtype: (flask.Response, int)
        """
        data = request.json
        login = get_jwt_identity()

        try:
            self.authentication_service.is_user_admin(login)
            department_to_update = self.department_service \
                .update_department(id, data.get('new_full_name'), data.get('new_code_name'), data.get('new_manager_id'))
            return department_to_update, 200

        except ValueError as e:
            return {"message": str(e)}, 400


@department_namespace.route('/all')
class DepartmentAllRoute(Resource):
    """
    DepartmentAllRoute provides an endpoint for retrieving all departments in the system. It processes GET requests,
    returning a list of all departments. The route leverages the DepartmentService to access department data and ensures
    a comprehensive list of all departments is provided.

    DepartmentService - An instance of DepartmentService used to retrieve a list of all departments.
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes the DepartmentAllRoute with an instance of DepartmentService. The DepartmentService is essential for
        accessing the repository of department data and retrieving a comprehensive list of departments.
        """
        super().__init__(*args, **kwargs)
        self.department_service = DepartmentService()

    @department_namespace.marshal_with(departments_get_model)
    def get(self):
        """
        Processes the GET request to retrieve a list of all departments. This method utilizes the DepartmentService to
        fetch all departments from the database and return them in a list format.

        On success, it returns a list of all departments along with a 200 HTTP status code.
        On failure (e.g., if an error occurs during retrieval), it returns an error message and the corresponding HTTP
        status code.

        :return: A tuple containing the response (either a list of departments or an error message) and the HTTP status
                 code.
        :rtype: (flask.Response, int)
        """
        try:
            departments_to_find = self.department_service.find_all_departments()
            return departments_to_find, 200

        except ValueError as e:
            return {"message": str(e)}, 400
