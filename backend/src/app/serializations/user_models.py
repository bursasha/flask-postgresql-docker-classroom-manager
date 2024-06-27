from flask_restx import fields


def create_user_post_model(namespace):
    """
    Defines and returns the model for a user POST operation. This model specifies the expected structure and
    data types for the payload when creating a new user via a POST request.

    :return: A Flask-RESTx model object representing the structure of a user POST operation.
    :rtype: flask_restx.fields.Model
    """
    return namespace.model(
        "UserPost", {
            "first_name": fields.String(description="The first name of the user.", required=True),
            "last_name": fields.String(description="The last name of the user.", required=True),
            "login": fields.String(description="The login identifier for the user.", required=True),
            "is_admin": fields.Boolean(description="The admin identifier for the user.", required=True)
        })


def create_user_put_model(namespace):
    """
    Defines and returns the model for a user PUT operation. This model specifies the expected structure and
    data types for the payload when updating an existing user via a PUT request.

    :return: A Flask-RESTx model object representing the structure of a user PUT operation.
    :rtype: flask_restx.fields.Model
    """
    return namespace.model(
        "UserPut", {
            "new_first_name": fields.String(description="The new first name of the user.", required=False),
            "new_last_name": fields.String(description="The new last name of the user.", required=False),
            "new_department_id": fields.Integer(description="The ID of the new department for the user.",
                                                required=False),
            "new_occupied_classroom_ids": fields.List(fields.Integer,
                                                      description="A list of new classroom IDs the user occupies.",
                                                      required=False)
        })


def create_user_get_model(namespace):
    """
    Defines and returns the model for a single user GET response. This model specifies the structure and
    data types of the response payload when retrieving details of a user.

    :return: A Flask-RESTx model object representing the structure of a single user GET response.
    :rtype: flask_restx.fields.Model
    """
    return namespace.model(
        "UserGet", {
            "id": fields.Integer(description="The unique identifier of the user."),
            "first_name": fields.String(description="The first name of the user."),
            "last_name": fields.String(description="The last name of the user."),
            "login": fields.String(description="The login identifier of the user."),
            "registration_date": fields.DateTime(description="The registration date of the user."),
            "is_admin": fields.Boolean(description="The admin identifier of the user."),
            "managed_department": fields.Integer(description="ID of the department managed by the user."),
            "department": fields.Integer(description="ID of the department the user belongs to."),
            "managed_classrooms": fields.List(fields.Integer,
                                              description="List of IDs of classrooms managed by the user."),
            "occupied_classrooms": fields.List(fields.Integer,
                                               description="List of IDs of classrooms occupied by the user."),
            "authored_requests": fields.List(fields.Integer,
                                             description="List of IDs of requests authored by the user."),
            "requests": fields.List(fields.Integer, description="List of IDs of requests involving the user.")
        })


def create_users_get_model(namespace):
    """
    Defines and returns the model for a users GET response. This model specifies the structure and
    data types of the response payload when retrieving a list of users.

    :return: A Flask-RESTx model object representing the structure of a users GET response.
    :rtype: flask_restx.fields.Model
    """
    user_model = create_user_get_model(namespace)

    return namespace.model(
        "UsersGet", {
            "users": fields.List(fields.Nested(user_model), description="A list of users.")
        })
