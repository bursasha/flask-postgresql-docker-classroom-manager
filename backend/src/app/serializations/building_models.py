from flask_restx import fields


def create_building_post_model(namespace):
    """
    Defines and returns the model for a building POST request. This model specifies the expected structure and
    data types for the payload when creating a new building via a POST request.

    :return: A Flask-RESTx model object representing the structure of a building POST request.
    :rtype: flask_restx.fields.Model
    """
    return namespace.model(
        "BuildingPost", {
            "name": fields.String(description="The name of the building.", required=True),
            "address": fields.String(description="The address of the building.", required=True)
        })


def create_building_put_model(namespace):
    """
    Defines and returns the model for a building PUT request. This model specifies the expected structure and
    data types for the payload when updating an existing building via a PUT request.

    :return: A Flask-RESTx model object representing the structure of a building PUT request.
    :rtype: flask_restx.fields.Model
    """
    return namespace.model(
        "BuildingPut", {
            "new_name": fields.String(description="The new name for the building.", required=False),
            "new_address": fields.String(description="The new address for the building.", required=False)
        })


def create_building_get_model(namespace):
    """
    Defines and returns the model for a single building GET response. This model specifies the structure and
    data types of the response payload when retrieving details of a building.

    :return: A Flask-RESTx model object representing the structure of a single building GET response.
    :rtype: flask_restx.fields.Model
    """
    return namespace.model(
        "BuildingGet", {
            "id": fields.Integer(description="The unique identifier of a building."),
            "name": fields.String(description="The name of the building."),
            "address": fields.String(description="The address of the building."),
            "classrooms": fields.List(fields.Integer, description="A list of IDs of classrooms in the building.")
        })


def create_buildings_get_model(namespace):
    """
    Defines and returns the model for a buildings GET response. This model specifies the structure and
    data types of the response payload when retrieving a list of buildings.

    :return: A Flask-RESTx model object representing the structure of a buildings GET response.
    :rtype: flask_restx.fields.Model
    """
    building_model = create_building_get_model(namespace)  # Reuse the single building model.

    return namespace.model(
        "BuildingsGet", {
            "buildings": fields.List(fields.Nested(building_model), description="A list of buildings.")
        })
