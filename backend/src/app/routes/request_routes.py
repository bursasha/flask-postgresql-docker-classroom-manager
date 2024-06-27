from flask_restx import Resource, Namespace
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..services import RequestService, AuthenticationService
from ..serializations import create_request_post_model, create_request_put_model, create_request_approve_put_model, \
    create_request_get_model, create_requests_get_model

request_namespace = Namespace("request", description="Request related operations.")
request_post_model = create_request_post_model(request_namespace)
request_put_model = create_request_put_model(request_namespace)
request_approve_put_model = create_request_approve_put_model(request_namespace)
request_get_model = create_request_get_model(request_namespace)
requests_get_model = create_requests_get_model(request_namespace)


@request_namespace.route('/')
class RequestRoute(Resource):
    """
    RequestRoute provides an endpoint for creating reservation requests within the application. It processes POST
    requests to create new reservation requests and uses the RequestService to manage the underlying logic, ensuring
    efficient and accurate addition of request data.

    RequestService - An instance of RequestService used to handle the creation and management of reservation requests.
    AuthenticationService - An instance of AuthenticationService used to verify user authentication and authorization.
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes the RequestRoute with instances of RequestService and AuthenticationService. These services are
        crucial for handling the logic related to request operations and user authentication, such as validating input
        data, interacting with the database, and providing a structured response back to the client.
        """
        super().__init__(*args, **kwargs)
        self.request_service = RequestService()
        self.authentication_service = AuthenticationService()

    @request_namespace.expect(request_post_model)
    @request_namespace.marshal_with(request_get_model)
    @jwt_required()
    def post(self):
        """
        Processes the POST request to create a new reservation request. It expects a payload containing the necessary
        details for the reservation. This method delegates the request creation process to the RequestService, which
        validates the input data and adds the new request to the database. It includes an authorization check to ensure
        that the request is made by an authenticated and authorized user.

        On success, it returns the details of the created request.
        On failure, it returns an error message.

        :return: A tuple containing the response (either request details or error message) and the HTTP status code.
        :rtype: (flask.Response, int)
        """
        data = request.json
        login = get_jwt_identity()

        try:
            self.authentication_service.is_user_authenticated(login)
            request_to_create = self.request_service.create_reservation_request(
                data.get('start_date'), data.get('end_date'), data.get('author_id'),
                data.get('classroom_id'), data.get('requesting_user_logins'))
            return request_to_create, 201

        except ValueError as e:
            return {"message": str(e)}, 400


@request_namespace.route('/<int:id>')
class RequestIdRoute(Resource):
    """
    RequestIdRoute provides endpoints for retrieving and updating a specific request by its ID.
    It handles GET requests for retrieving request details and PUT requests for updating request information.
    This route utilizes the RequestService to manage interactions with the Request data model, ensuring
    efficient and consistent access and modification of request records.
    It includes authorization checks to ensure that only authenticated users can access these endpoints.

    RequestService - An instance of RequestService used to interact with request data.
    AuthenticationService - An instance of AuthenticationService used to verify user authentication.
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes the RequestIdRoute with instances of RequestService and AuthenticationService.
        This service is responsible for handling the logic associated with request operations and user authentication.
        """
        super().__init__(*args, **kwargs)
        self.request_service = RequestService()
        self.authentication_service = AuthenticationService()

    @request_namespace.marshal_with(request_get_model)
    @jwt_required()
    def get(self, id):
        """
        Processes the GET request to retrieve details of a specific request by its ID using the RequestService.
        It includes an authorization check to ensure that the request is made by an authenticated user.

        On success, it returns the details of the specified request.
        On failure (e.g., request not found), it returns an error message.

        :param id: The identifier of the request to retrieve.
        :type id: int

        :return: A tuple containing the response (either request details or error message) and the HTTP status code.
        :rtype: (flask.Response, int)
        """
        login = get_jwt_identity()

        try:
            self.authentication_service.is_user_authenticated(login)
            request_to_find = self.request_service.find_request(id)
            return request_to_find, 200

        except ValueError as e:
            return {"message": str(e)}, 400

    @request_namespace.expect(request_put_model)
    @request_namespace.marshal_with(request_get_model)
    @jwt_required()
    def put(self, id):
        """
        Processes the PUT request to update details of a specific request by its ID. This method uses the
        RequestService to update the request's details based on the provided data.

        On success, it returns the updated request details.
        On failure (e.g., invalid data or request not found), it returns an error message.

        :param id: The identifier of the request to update.
        :type id: int

        :return: A tuple containing the response (either updated request details or error message) and the HTTP status
                 code.
        :rtype: (flask.Response, int)
        """
        data = request.json
        login = get_jwt_identity()

        try:
            self.authentication_service.is_user_admin_or_manager_in_request(login, id)
            request_to_update = self.request_service.update_reservation_request(
                id, data.get('new_author_id'), data.get('new_classroom_id'), data.get('new_requesting_user_logins'))
            return request_to_update, 200

        except ValueError as e:
            return {"message": str(e)}, 400


@request_namespace.route('/<int:id>/approve')
class RequestIdApproveRoute(Resource):
    """
    RequestIdApprove provides an endpoint for approving a specific request by its ID.
    It processes PUT requests to change the approval status of a request using the RequestService and
    AuthenticationService.

    RequestService - An instance of RequestService used for request approval operations.
    AuthenticationService - An instance of AuthenticationService used to authenticate the user and verify
    their permissions.
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes the RequestIdApprove with instances of RequestService and AuthenticationService. These services
        are essential for handling the logic related to request approval, such as validating the manager's identity,
        authenticating the user, and changing the request's approval status.
        """
        super().__init__(*args, **kwargs)
        self.request_service = RequestService()
        self.authentication_service = AuthenticationService()

    @request_namespace.expect(request_approve_put_model)
    @request_namespace.marshal_with(request_get_model)
    @jwt_required()
    def put(self, id):
        """
        Processes the PUT request to approve a specific request by its ID. This method relies on the RequestService and
        AuthenticationService to validate the manager's authority, authenticate the user, and update the request's
        approval status.

        On success, it returns the approved request details.
        On failure (e.g., invalid manager, user not authorized, or request not found), it returns an error message.

        :param id: The identifier of the request to approve.
        :type id: int

        :return: A tuple containing the response (either approved request details or error message) and the HTTP status
                 code.
        :rtype: (flask.Response, int)
        """
        data = request.json
        login = get_jwt_identity()

        try:
            self.authentication_service.is_user_admin_or_manager_in_request(login, id)
            request_to_approve = self.request_service.approve_reservation_request(id, data.get('manager_id'))
            return request_to_approve, 200

        except ValueError as e:
            return {"message": str(e)}, 400


@request_namespace.route('/all')
class RequestAllRoute(Resource):
    """
    RequestAllRoute provides an endpoint for retrieving all requests within the system. It processes GET requests,
    returning a list of all requests. This route uses the RequestService to access request data and ensures
    a comprehensive list of all requests is provided.

    RequestService - An instance of RequestService used to retrieve a list of all requests from the database.
    This service is critical for ensuring that all interactions with request data are handled efficiently and
    consistently, offering a simplified interface for the route to interact with request data.
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes the RequestAllRoute with an instance of RequestService. The RequestService is essential for
        accessing the repository of request data and retrieving a comprehensive list of requests.
        """
        super().__init__(*args, **kwargs)
        self.request_service = RequestService()

    @request_namespace.marshal_with(requests_get_model)
    def get(self):
        """
        Processes the GET request to retrieve a list of all requests. This method utilizes the RequestService to
        fetch all requests from the database and return them in a list format.

        On success, it returns a list of all requests along with a 200 HTTP status code.
        On failure (e.g., if an error occurs during retrieval), it returns an error message and the corresponding HTTP
        status code.

        :return: A tuple containing the response (either a list of requests or an error message) and the HTTP status
                 code.
        :rtype: (flask.Response, int)
        """
        try:
            requests_to_find = self.request_service.find_all_requests()
            return requests_to_find, 200

        except ValueError as e:
            return {"message": str(e)}, 400
