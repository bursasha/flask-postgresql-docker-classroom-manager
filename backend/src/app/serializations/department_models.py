from flask_restx import fields


def create_department_post_model(namespace):
    """
    Defines and returns the model for a department POST request. This model specifies the expected structure and
    data types for the payload when creating a new department via a POST request.

    :return: A Flask-RESTx model object representing the structure of a department POST request.
    :rtype: flask_restx.fields.Model
    """
    return namespace.model(
        "DepartmentPost", {
            "full_name": fields.String(description="The full, formal name of the department.", required=True),
            "code_name": fields.String(description="The short code name or abbreviation for the department.",
                                       required=True)
        })


def create_department_put_model(namespace):
    """
    Defines and returns the model for a department PUT request. This model specifies the expected structure and
    data types for the payload when updating an existing department via a PUT request.

    :return: A Flask-RESTx model object representing the structure of a department PUT request.
    :rtype: flask_restx.fields.Model
    """
    return namespace.model(
        "DepartmentPut", {
            "new_full_name": fields.String(description="The new full name for the department.", required=False),
            "new_code_name": fields.String(description="The new code name for the department.", required=False),
            "new_manager_id": fields.Integer(description="The ID of the new manager for the department.",
                                             required=False)
        })


def create_department_get_model(namespace):
    """
    Defines and returns the model for a single department GET response. This model specifies the structure and
    data types of the response payload when retrieving details of a department.

    :return: A Flask-RESTx model object representing the structure of a single department GET response.
    :rtype: flask_restx.fields.Model
    """
    return namespace.model(
        "DepartmentGet", {
            "id": fields.Integer(description="The unique identifier of a department."),
            "full_name": fields.String(description="The full name of the department."),
            "code_name": fields.String(description="The code name or abbreviation of the department."),
            "manager": fields.Integer(description="The ID of the manager of the department."),
            "users": fields.List(fields.Integer, description="A list of IDs of users belonging to the department."),
            "classrooms": fields.List(fields.Integer,
                                      description="A list of IDs of classrooms managed by the department.")
        })


def create_departments_get_model(namespace):
    """
    Defines and returns the model for a departments GET response. This model specifies the structure and
    data types of the response payload when retrieving a list of departments.

    :return: A Flask-RESTx model object representing the structure of a departments GET response.
    :rtype: flask_restx.fields.Model
    """
    department_model = create_department_get_model(namespace)

    return namespace.model(
        "DepartmentsGet", {
            "departments": fields.List(fields.Nested(department_model), description="A list of departments.")
        })
