from flask_restx import fields


def create_classroom_post_model(namespace):
    """
    Defines and returns the model for a classroom POST request. This model specifies the expected structure and
    data types for the payload when creating a new classroom via a POST request.

    :return: A Flask-RESTx model object representing the structure of a classroom POST request.
    :rtype: flask_restx.fields.Model
    """
    return namespace.model(
        "ClassroomPost", {
            "name": fields.String(description="The name of the classroom.", required=True),
            "floor": fields.Integer(description="The floor number where the classroom is located.", required=True),
            "is_private": fields.Boolean(description="Indicates whether the classroom is private.", required=True)
        })


def create_classroom_put_model(namespace):
    """
    Defines and returns the model for a classroom PUT request. This model specifies the expected structure and
    data types for the payload when updating an existing classroom via a PUT request.

    :return: A Flask-RESTx model object representing the structure of a classroom PUT request.
    :rtype: flask_restx.fields.Model
    """
    return namespace.model(
        "ClassroomPut", {
            "new_name": fields.String(description="The new name for the classroom.", required=False),
            "new_building_id": fields.Integer(description="The new building ID for the classroom.", required=False),
            "new_department_id": fields.Integer(description="The new department ID for the classroom.", required=False),
            "new_manager_id": fields.Integer(description="The new manager ID for the classroom.", required=False),
            "new_is_private": fields.Boolean(description="The new privacy status for the classroom.", required=False)
        })


def create_classroom_get_model(namespace):
    """
    Defines and returns the model for a single classroom GET response. This model specifies the structure and
    data types of the response payload when retrieving details of a classroom.

    :return: A Flask-RESTx model object representing the structure of a single classroom GET response.
    :rtype: flask_restx.fields.Model
    """
    return namespace.model(
        "ClassroomGet", {
            "id": fields.Integer(description="The unique identifier of the classroom."),
            "name": fields.String(description="The name of the classroom."),
            "floor": fields.Integer(description="The floor number where the classroom is located."),
            "is_private": fields.Boolean(description="Indicates whether the classroom is private."),
            "building": fields.Integer(description="The ID of the building in which the classroom is located."),
            "department": fields.Integer(description="The ID of the department to which the classroom belongs."),
            "manager": fields.Integer(description="The ID of the user who manages the classroom."),
            "occupants": fields.List(fields.Integer, description="A list of IDs of users who occupy the classroom."),
            "requests": fields.List(fields.Integer, description="A list of IDs of requests related to the classroom.")
        })


def create_classrooms_get_model(namespace):
    """
    Defines and returns the model for a classrooms GET response. This model specifies the structure and
    data types of the response payload when retrieving a list of classrooms.

    :param namespace: The namespace in which the model is being created.
    :type namespace: flask_restx.Namespace

    :return: A Flask-RESTx model object representing the structure of a classrooms GET response.
    :rtype: flask_restx.fields.Model
    """
    classroom_model = create_classroom_get_model(namespace)

    return namespace.model(
        "ClassroomsGet", {
            "classrooms": fields.List(fields.Nested(classroom_model), description="A list of classrooms.")
        })
