from flask import jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, unset_jwt_cookies, set_access_cookies, \
    set_refresh_cookies, decode_token

from ..repositories import UserRepository, DepartmentRepository, ClassroomRepository, RequestRepository


class AuthenticationService:
    """
    The AuthenticationService class provides a high-level interface for managing user authentication within the
    application. It facilitates the generation of JWT access and refresh tokens, handles user login and logout
    procedures, and manages token lifecycles, ensuring secure and efficient user authentication.

    The service acts as an intermediary between the application's higher-level logic and the lower-level database
    operations carried out by the repositories, abstracting the complexities of direct database interactions into a
    set of straightforward methods.

    UserRepository - A repository handling interactions with the User data model, managing the retrieval and updating
    of user records.
    DepartmentRepository - A repository handling interactions with the Department data model, managing the retrieval
    and updating of department records.
    ClassroomRepository - A repository handling interactions with the Classroom data model, managing the retrieval and
    updating of classroom records.
    RequestRepository - A repository handling interactions with the Request data model, managing the retrieval and
    updating of request records.
    """

    def __init__(self):
        """
        Initializes the AuthenticationService with instances of UserRepository, DepartmentRepository,
        ClassroomRepository, and RequestRepository. These repositories provide a layer of abstraction over the
        database, ensuring that the service's interactions with user, department, classroom, and request data
        are efficient and well-organized.
        """
        self.user_repository = UserRepository()
        self.department_repository = DepartmentRepository()
        self.classroom_repository = ClassroomRepository()
        self.request_repository = RequestRepository()

    def authenticate_user(self, login):
        """
        Authenticates a user based on the provided login. If authentication is successful, it generates and returns
        JWT access and refresh tokens set as cookies in the response.

        :param login: The login identifier of the user attempting to authenticate.
        :type login: str

        :return: A response object containing the user's data and authentication tokens set as cookies if the login is
                 valid.
        :rtype: flask.Response

        :raises ValueError: If the login is invalid or the user does not exist.
        """
        current_user = self.user_repository.get_user_by_login(login)
        if not current_user:
            raise ValueError("Invalid login.")

        access_token = create_access_token(identity=login)
        refresh_token = create_refresh_token(identity=login)
        # response = jsonify({"user": current_user, "access_token": access_token, "refresh_token": refresh_token})
        response = {"user": self.user_repository.serialize_user(current_user),
                    "access_token": access_token, "refresh_token": refresh_token}

        # set_access_cookies(response, access_token)
        # set_refresh_cookies(response, refresh_token)

        return response

    def logout_user(self, login):
        """
        Handles the logout process for the user specified by the login. It verifies the user's existence and
        then unsets JWT cookies, effectively logging the user out.

        :param login: The login of the user attempting to logout.
        :type login: str

        :return: A response object with unset JWT cookies, indicating successful logout.
        :rtype: flask.Response

        :raises ValueError: If the login is invalid or the user does not exist.
        """
        current_user = self.user_repository.get_user_by_login(login)
        if not current_user:
            raise ValueError("Invalid login.")

        response = jsonify({"message": "Logout successful."})

        unset_jwt_cookies(response)

        return response

    def refresh_access_token(self, refresh_token):
        """
        Generates a new access token for the user using the provided refresh token. It decodes the refresh token to
        retrieve the user's login, validates it, and then generates a new access token set as a cookie in the response.

        :param refresh_token: The refresh token provided by the user.
        :type refresh_token: str

        :return: A response object containing the new access token set as a cookie.
        :rtype: flask.Response

        :raises ValueError: If the refresh token is invalid or the user does not exist.
        """
        login = decode_token(refresh_token).get("sub")
        if not login:
            raise ValueError("Invalid refresh token.")

        current_user = self.user_repository.get_user_by_login(login)
        if not current_user:
            raise ValueError("User not found.")

        new_access_token = create_access_token(identity=current_user.get_login())
        response = jsonify({"access_token": new_access_token})

        set_access_cookies(response, new_access_token)

        return response

    def is_user_authenticated(self, login):
        """
        Checks if the user with the provided login is authenticated.

        :param login: The login of the user to check.
        :type login: str

        :return: True if the user is authenticated, otherwise False.
        :rtype: bool

        :raises ValueError: If the login is invalid or the user does not exist.
        """
        current_user = self.user_repository.get_user_by_login(login)
        if not current_user:
            raise ValueError("User with such login does not exist.")

        return True

    def is_user_classroom_occupant(self, login, classroom_id):
        """
        Checks if the user with the provided login is in a specific classroom.

        :param login: The login of the user to check.
        :type login: str

        :param classroom_id: The ID of the classroom to check against.
        :type classroom_id: int

        :return: True if the user is in the specified classroom, otherwise False.
        :rtype: bool

        :raises ValueError: If the login is invalid or the user does not exist.
        """
        current_user = self.user_repository.get_user_by_login(login)
        if not current_user:
            raise ValueError("Invalid login.")

        return classroom_id in current_user.get_occupied_classrooms()

    def is_user_classroom_manager(self, login, classroom_id):
        """
        Checks if the user with the provided login is the manager of a specific classroom.

        :param login: The login of the user to check.
        :type login: str

        :param classroom_id: The ID of the classroom to check against.
        :type classroom_id: int

        :return: True if the user is the manager of the specified classroom, otherwise False.
        :rtype: bool

        :raises ValueError: If the login is invalid or the user does not exist.
        """
        current_user = self.user_repository.get_user_by_login(login)
        if not current_user:
            raise ValueError("Invalid login.")

        return classroom_id in current_user.get_managed_classrooms()

    def is_user_department_occupant(self, login, department_id):
        """
        Checks if the user with the provided login is in a specific department.

        :param login: The login of the user to check.
        :type login: str

        :param department_id: The ID of the department to check against.
        :type department_id: int

        :return: True if the user is in the specified department, otherwise False.
        :rtype: bool

        :raises ValueError: If the login is invalid or the user does not exist.
        """
        current_user = self.user_repository.get_user_by_login(login)
        if not current_user:
            raise ValueError("Invalid login.")

        return current_user.get_department_id() == department_id

    def is_user_department_manager(self, login, department_id):
        """
        Checks if the user with the provided login is the manager of a specific department.

        :param login: The login of the user to check.
        :type login: str
        :param department_id: The ID of the department to check against.
        :type department_id: int

        :return: True if the user is the manager of the specified department, otherwise False.
        :rtype: bool

        :raises ValueError: If the login is invalid, the user does not exist, or the department does not exist.
        """
        current_user = self.user_repository.get_user_by_login(login)
        if not current_user:
            raise ValueError("Invalid login.")

        department = self.department_repository.get_department_by_id(department_id)
        if not department:
            raise ValueError("Department does not exist.")

        return department.get_manager_id() == current_user.get_id()

    def is_user_manager_of_department_by_classroom(self, login, classroom_id):
        """
        Checks if the user with the provided login is the manager of the department associated with a specific
        classroom.

        This method first retrieves the department associated with the given classroom ID and then checks if the user
        is the manager of that department.

        :param login: The login of the user to check.
        :type login: str

        :param classroom_id: The ID of the classroom to check against.
        :type classroom_id: int

        :return: True if the user is the manager of the department associated with the specified classroom,
                 otherwise False.
        :rtype: bool

        :raises ValueError: If the login is invalid, the user does not exist, the classroom does not exist,
                            or the department does not exist.
        """
        current_user = self.user_repository.get_user_by_login(login)
        if not current_user:
            raise ValueError("Invalid login.")

        classroom = self.classroom_repository.get_classroom_by_id(classroom_id)
        if not classroom:
            raise ValueError("Classroom does not exist.")

        department = self.department_repository.get_department_by_id(classroom.get_department_id())
        if not department:
            raise ValueError("Department does not exist.")

        return department.get_manager_id() == current_user.get_id()

    def is_user_manager_of_another_user_department(self, manager_login, user_id):
        """
        Checks if the user with the provided login is the manager of the department that another user
        (specified by their ID) belongs to.

        :param manager_login: The login of the user to check if they're a manager.
        :type manager_login: str

        :param user_id: The ID of the user whose department manager to verify.
        :type user_id: int

        :return: True if the user with manager_login is the manager of the department of the user specified by user_id,
                 otherwise False.
        :rtype: bool

        :raises ValueError: If the login is invalid, the users do not exist, or the departments do not exist.
        """
        potential_manager = self.user_repository.get_user_by_login(manager_login)
        if not potential_manager:
            raise ValueError("Manager with such login does not exist.")

        user_in_question = self.user_repository.get_user_by_id(user_id)
        if not user_in_question:
            raise ValueError("User with such ID does not exist.")

        department_of_user_in_question = self.department_repository.get_department_by_id(
            user_in_question.get_department_id())

        if not department_of_user_in_question:
            raise ValueError("Department for the given user does not exist.")

        return department_of_user_in_question.get_manager_id() == potential_manager.get_id()

    def is_user_classroom_manager_in_request(self, login, request_id):
        """
        Checks if the user with the provided login is the manager of the classroom specified in a request.

        :param login: The login of the user to check.
        :type login: str

        :param request_id: The ID of the request to check against.
        :type request_id: int

        :return: True if the user is the manager of the classroom specified in the request, otherwise False.
        :rtype: bool

        :raises ValueError: If the login is invalid, the user does not exist, the request does not exist,
                            or the classroom does not exist.
        """
        manager_user = self.user_repository.get_user_by_login(login)
        if not manager_user:
            raise ValueError("Invalid login.")

        request = self.request_repository.get_request_by_id(request_id)
        if not request:
            raise ValueError("Request does not exist.")

        classroom_id = request.get_classroom_id()

        return self.is_user_classroom_manager(login, classroom_id)

    def is_user_department_manager_in_request(self, login, request_id):
        """
        Checks if the user with the provided login is the manager of the department of the classroom specified in
        a request.

        :param login: The login of the user to check.
        :type login: str

        :param request_id: The ID of the request to check against.
        :type request_id: int

        :return: True if the user is the manager of the department of the classroom specified in the request,
                 otherwise False.
        :rtype: bool

        :raises ValueError: If the login is invalid, the user does not exist, the request does not exist,
                            or the department does not exist.
        """
        manager_user = self.user_repository.get_user_by_login(login)
        if not manager_user:
            raise ValueError("Invalid login.")

        request = self.request_repository.get_request_by_id(request_id)
        if not request:
            raise ValueError("Request does not exist.")

        classroom_id = request.get_classroom_id()
        classroom = self.classroom_repository.get_classroom_by_id(classroom_id)
        if not classroom:
            raise ValueError("Classroom does not exist.")

        department_id = classroom.get_department_id()

        return self.is_user_manager_of_department_by_classroom(login, department_id)

    def is_user_admin(self, login):
        """
        Checks if the user with the provided login is an administrator.

        :param login: The login of the user to check.
        :type login: str

        :return: True if the user is the admin, otherwise False.
        :rtype: bool

        :raises ValueError: If the login is invalid, the user does not exist, or the user is not an administrator.
        """
        user = self.user_repository.get_user_by_login(login)
        if not user:
            raise ValueError("User with such login does not exist.")

        if not user.get_is_admin():
            raise ValueError("Access denied. User is not an administrator.")

        return True

    def is_user_admin_or_manager_of_department_by_classroom(self, login, classroom_id):
        """
        Checks if the user with the provided login is either an administrator or the manager of the department
        associated with a specific classroom.

        This method uses two other methods: is_user_admin to check if the user is an administrator, and
        is_user_manager_of_department_by_classroom to check if the user is the manager of the department
        associated with the classroom. If neither condition is true, it raises a ValueError.

        :param login: The login of the user to check.
        :type login: str

        :param classroom_id: The ID of the classroom to check against.
        :type classroom_id: int

        :raises ValueError: If the login is invalid, the user does not exist, the user is neither an admin nor a
                            department manager, the classroom does not exist, or the department does not exist.
        """
        try:
            if self.is_user_admin(login):
                return True
        except ValueError:
            pass

        try:
            if self.is_user_manager_of_department_by_classroom(login, classroom_id):
                return True
        except ValueError:
            pass

        raise ValueError("Access denied. User is neither an administrator nor a manager of the specified department.")

    def is_user_admin_or_manager_of_another_user_department(self, login, user_id):
        """
        Checks if the user with the provided login is either an administrator or the manager of the department that
        another user (specified by their ID) belongs to.

        :param login: The login of the user to check.
        :type login: str

        :param user_id: The ID of the user whose department manager to verify.
        :type user_id: int

        :return: True if the user with login is an administrator or the manager of the department of the user specified
                 by user_id, otherwise False.
        :rtype: bool

        :raises ValueError: If the login is invalid, the users do not exist, the user is not an administrator,
                            and the user is not a manager of the department.
        """
        try:
            if self.is_user_admin(login):
                return True
        except ValueError:
            pass

        try:
            if self.is_user_manager_of_another_user_department(login, user_id):
                return True
        except ValueError:
            pass

        raise ValueError("Access denied. User is neither an administrator nor a manager of the specified department.")

    def is_user_admin_or_manager_in_request(self, login, request_id):
        """
        Checks if the user with the provided login is either an administrator, the manager of the classroom, or
        the manager of the department associated with the classroom specified in a request.

        :param login: The login of the user to check.
        :type login: str
        :param request_id: The ID of the request to check against.
        :type request_id: int

        :return: True if the user with login is an administrator, the manager of the classroom, or the manager of the
                 department associated with the classroom specified in the request, otherwise False.
        :rtype: bool

        :raises ValueError: If the login is invalid, the user does not exist, the request does not exist,
                            the classroom does not exist, the department does not exist, the user is not an
                            administrator, and the user is neither a manager of the classroom nor of the department.
        """
        try:
            if self.is_user_admin(login):
                return True
        except ValueError:
            pass

        try:
            if self.is_user_classroom_manager_in_request(login, request_id):
                return True
        except ValueError:
            pass

        try:
            if self.is_user_department_manager_in_request(login, request_id):
                return True
        except ValueError:
            pass

        raise ValueError(
            "Access denied. User does not have the necessary administrative or managerial rights for the request.")
