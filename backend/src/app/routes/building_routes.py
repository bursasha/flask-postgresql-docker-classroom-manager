from flask_restx import Resource, Namespace
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..services import BuildingService, AuthenticationService
from ..serializations import create_building_post_model, create_building_put_model, create_building_get_model, \
    create_buildings_get_model

building_namespace = Namespace("building", description="Building related operations.")
building_post_model = create_building_post_model(building_namespace)
building_put_model = create_building_put_model(building_namespace)
building_get_model = create_building_get_model(building_namespace)
buildings_get_model = create_buildings_get_model(building_namespace)


@building_namespace.route('/')
class BuildingRoute(Resource):
    """
    BuildingRoute provides an endpoint for creating and managing buildings within the application. It processes
    POST requests to create new buildings and uses the BuildingService to handle the underlying logic, ensuring
    that building data is added accurately and efficiently.

    BuildService - An instance of BuildingService used to handle the creation of buildings.
    AuthenticationService - An instance of AuthenticationService used to handle user authentication and authorization.
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes the BuildingRoute with instances of BuildingService and AuthenticationService.
        These services are crucial for handling the logic related to building operations, such as validating
        input data, interacting with the database, providing a response back to the client, and ensuring that only
        authorized users can create buildings.
        """
        super().__init__(*args, **kwargs)
        self.building_service = BuildingService()
        self.authentication_service = AuthenticationService()

    @building_namespace.expect(building_post_model)
    @building_namespace.marshal_with(building_get_model)
    @jwt_required()
    def post(self):
        """
        Processes the POST request to create a new building. It expects a payload containing the building's name
        and address. This method delegates the creation process to the BuildingService, which validates the input
        data and adds the new building to the database.

        On success, it returns the details of the created building.
        On failure, it returns an error message.

        :return: A tuple containing the response (either building details or error message) and the HTTP status code.
        :rtype: (flask.Response, int)
        """
        login = get_jwt_identity()
        data = request.json

        try:
            self.authentication_service.is_user_admin(login)
            building_to_create = self.building_service.create_building(data.get('name'), data.get('address'))
            return building_to_create, 201

        except ValueError as e:
            return {"message": str(e)}, 400


@building_namespace.route('/<int:id>')
class BuildingIdRoute(Resource):
    """
    BuildingIdRoute provides endpoints for retrieving and updating a specific building by its ID.
    It processes GET requests for retrieving building details and PUT requests for updating building information.
    This route utilizes the BuildingService to manage the interaction with the Building data model, ensuring
    efficient and consistent access and modification of building records.

    BuildingService - An instance of BuildingService used to interact with building data.
    AuthenticationService - An instance of AuthenticationService used to verify the authentication status of users
    making requests to this route.
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes the BuildingIdRoute with instances of BuildingService and AuthenticationService. The BuildingService
        is responsible for handling the logic associated with building operations, such as retrieving and updating
        building details, while the AuthenticationService is used to verify the authentication status of users making
        requests to this route.
        """
        super().__init__(*args, **kwargs)
        self.building_service = BuildingService()
        self.authentication_service = AuthenticationService()

    @building_namespace.marshal_with(building_get_model)
    @jwt_required()
    def get(self, id):
        """
        Processes the GET request to retrieve details of a specific building by its ID using the BuildingService.
        This method also ensures that the request is made by an authenticated user by verifying the JWT token
        provided in the request headers. If the user is not authenticated, it returns an unauthorized error.

        On success, it returns the details of the specified building.
        On failure (e.g., building not found), it returns an error message.

        :param id: The identifier of the building to retrieve.
        :type id: int

        :return: A tuple containing the response (either building details or error message) and the HTTP status code.
        :rtype: (flask.Response, int)
        """
        login = get_jwt_identity()

        try:
            self.authentication_service.is_user_authenticated(login)
            building_to_find = self.building_service.find_building(id)
            return building_to_find, 200

        except ValueError as e:
            return {"message": str(e)}, 400

    @building_namespace.expect(building_put_model)
    @building_namespace.marshal_with(building_get_model)
    @jwt_required()
    def put(self, id):
        """
        Processes the PUT request to update details of a specific building by its ID. This method uses the
        BuildingService to update the building's name and/or address based on the provided data.

        On success, it returns the updated building details.
        On failure (e.g., invalid data or building not found), it returns an error message.

        :param id: The identifier of the building to update.
        :type id: int

        :return: A tuple containing the response (either updated building details or error message) and the HTTP status
                 code.
        :rtype: (flask.Response, int)
        """
        data = request.json
        login = get_jwt_identity()

        try:
            self.authentication_service.is_user_admin(login)
            building_to_update = self.building_service.update_building(id, data.get('new_name'),
                                                                       data.get('new_address'))
            return building_to_update, 200

        except ValueError as e:
            return {"message": str(e)}, 400


@building_namespace.route('/all')
class BuildingAllRoute(Resource):
    """
    BuildingListRoute provides an endpoint for retrieving all buildings in the system. It processes GET requests,
    returning a list of all buildings. The route leverages the BuildingService to access building data and ensures
    a comprehensive list of all buildings is provided.

    The route's primary responsibility is to handle HTTP requests for building data retrieval and to utilize the
    BuildingService to perform the actual data fetching. This separation of concerns allows for clear, maintainable
    code.

    BuildingService - An instance of BuildingService used to retrieve a list of all buildings.
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes the BuildingListRoute with an instance of BuildingService. The BuildingService is essential for
        accessing the repository of building data and retrieving a comprehensive list of buildings.
        """
        super().__init__(*args, **kwargs)
        self.building_service = BuildingService()

    @building_namespace.marshal_with(buildings_get_model)
    def get(self):
        """
        Processes the GET request to retrieve a list of all buildings. This method utilizes the BuildingService to
        fetch all buildings from the database and return them in a list format.

        On success, it returns a list of all buildings along with a 200 HTTP status code.
        On failure (e.g., if an error occurs during retrieval), it returns an error message and the corresponding HTTP
        status code.

        :return: A tuple containing the response (either a list of buildings or an error message) and the HTTP status
                 code.
        :rtype: (flask.Response, int)
        """
        try:
            buildings_to_find = self.building_service.find_all_buildings()
            return buildings_to_find, 200

        except ValueError as e:
            return {"message": str(e)}, 400
