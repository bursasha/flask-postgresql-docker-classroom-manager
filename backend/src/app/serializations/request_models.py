from flask_restx import fields


def create_request_post_model(namespace):
    """
    Defines and returns the model for a request POST operation. This model specifies the expected structure and
    data types for the payload when creating a new reservation request via a POST request.

    :return: A Flask-RESTx model object representing the structure of a request POST operation.
    :rtype: flask_restx.fields.Model
    """
    return namespace.model(
        "RequestPost", {
            "start_date": fields.DateTime(description="The start date and time for the reservation.", required=True),
            "end_date": fields.DateTime(description="The end date and time for the reservation.", required=True),
            "author_id": fields.Integer(description="The ID of the user making the reservation.", required=True),
            "classroom_id": fields.Integer(description="The ID of the classroom to reserve.", required=True),
            "requesting_user_logins": fields.List(fields.String,
                                                  description="List of user logins involved in the reservation.",
                                                  required=True)
        })


def create_request_put_model(namespace):
    """
    Defines and returns the model for a request PUT operation. This model specifies the expected structure and
    data types for the payload when updating an existing reservation request via a PUT request.

    :return: A Flask-RESTx model object representing the structure of a request PUT operation.
    :rtype: flask_restx.fields.Model
    """
    return namespace.model(
        "RequestPut", {
            "new_author_id": fields.Integer(description="The new author's user ID for the request.", required=False),
            "new_classroom_id": fields.Integer(description="The new classroom ID for the request.", required=False),
            "new_requesting_user_logins": fields.List(fields.String,
                                                      description="List of new user logins involved in the reservation."
                                                      , required=False)
        })


def create_request_approve_put_model(namespace):
    """
    Defines and returns the model for a request approval PUT operation. This model specifies the expected structure and
    data types for the payload when approving a reservation request via a PUT request.

    :return: A Flask-RESTx model object representing the structure of a request approval PUT operation.
    :rtype: flask_restx.fields.Model
    """
    return namespace.model(
        "RequestApprovePut", {
            "manager_id": fields.Integer(description="The manager's user ID approving the request.", required=True)
        })


def create_request_get_model(namespace):
    """
    Defines and returns the model for a single request GET response. This model specifies the structure and
    data types of the response payload when retrieving details of a request.

    :return: A Flask-RESTx model object representing the structure of a single request GET response.
    :rtype: flask_restx.fields.Model
    """
    return namespace.model(
        "RequestGet", {
            "id": fields.Integer(description="The unique identifier of the request."),
            "start_date": fields.DateTime(description="The start date and time of the reservation."),
            "end_date": fields.DateTime(description="The end date and time of the reservation."),
            "registration_date": fields.DateTime(description="The date and time the request was registered."),
            "is_approved": fields.Boolean(description="Indicates whether the request is approved."),
            "author": fields.Integer(description="The ID of the user who made the reservation."),
            "requesting_users": fields.List(fields.Integer,
                                            description="A list of IDs of users involved in the reservation."),
            "classroom": fields.Integer(description="The ID of the classroom being requested.")
        })


def create_requests_get_model(namespace):
    """
    Defines and returns the model for a requests GET response. This model specifies the structure and
    data types of the response payload when retrieving a list of requests.

    :return: A Flask-RESTx model object representing the structure of a requests GET response.
    :rtype: flask_restx.fields.Model
    """
    request_model = create_request_get_model(namespace)

    return namespace.model(
        "RequestsGet", {
            "requests": fields.List(fields.Nested(request_model), description="A list of requests.")
        })
