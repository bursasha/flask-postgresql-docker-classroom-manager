from datetime import datetime

from ..orm import orm
from ..models import User


class UserRepository:
    """
    A repository for handling operations on User objects. This class provides
    methods to interact with the User data model, including creating users,
    validating user data, and retrieving users from the database.

    :ivar session: An instance of SQLAlchemy session for database operations.
    :type session: Session
    """

    def __init__(self):
        """
        Initializes the UserRepository with a database session.
        """
        self.session = orm.session

    @staticmethod
    def validate_name(name):
        """
        Validates the name (first or last) of a user based on length constraints.

        :param name: The name of the user to validate.
        :type name: str

        :return: True if the name is valid (length between 1 and 100 characters), False otherwise.
        :rtype: bool
        """
        return 0 < len(name) <= 100

    @staticmethod
    def validate_login(login):
        """
        Validates the login of a user based on length and format constraints.

        :param login: The login of the user to validate.
        :type login: str

        :return: True if the login is valid, False otherwise.
        :rtype: bool
        """
        return 0 < len(login) <= 50

    def create_user(self, first_name, last_name, login, is_admin):
        """
        Creates and saves a new User object with the provided details.

        :param first_name: The first name of the user.
        :type first_name: str

        :param last_name: The last name of the user.
        :type last_name: str

        :param login: The login of the user.
        :type login: str

        :param is_admin: Indicates if the user has administrative privileges.
        :type is_admin: bool

        :return: The newly created User object.
        :rtype: User
        """
        new_user = User(first_name=first_name, last_name=last_name, login=login, registration_date=datetime.now(),
                        is_admin=is_admin)
        self.session.add(new_user)
        self.session.commit()
        return new_user

    def get_all_users(self):
        """
        Retrieves all users from the database.

        :return: A list of all User objects.
        :rtype: list[User]
        """
        return self.session.query(User).all()

    def get_user_by_id(self, id):
        """
        Retrieves a user by their ID.

        :param id: The ID of the user to retrieve.
        :type id: int

        :return: The User object with the specified ID, or None if not found.
        :rtype: User or None
        """
        return self.session.query(User).filter_by(id=id).first()

    def get_user_by_login(self, login):
        """
        Retrieves a user by their login.

        :param login: The login of the user to retrieve.
        :type login: str

        :return: The User object with the specified login, or None if not found.
        :rtype: User or None
        """
        return self.session.query(User).filter_by(login=login).first()

    def update_user_first_name(self, user, new_first_name):
        """
        Updates the first name of a specific user.

        :param user: The User object to update.
        :type user: User

        :param new_first_name: The new first name for the user.
        :type new_first_name: str

        :return: The updated User object.
        :rtype: User
        """
        user.set_first_name(new_first_name)
        self.session.add(user)
        self.session.commit()
        return user

    def update_user_last_name(self, user, new_last_name):
        """
        Updates the last name of a specific user.

        :param user: The User object to update.
        :type user: User

        :param new_last_name: The new last name for the user.
        :type new_last_name: str

        :return: The updated User object.
        :rtype: User
        """
        user.set_last_name(new_last_name)
        self.session.add(user)
        self.session.commit()
        return user

    def update_user_occupied_classrooms(self, user, new_occupied_classrooms):
        """
        Updates the classrooms that the user occupies with a new list of Classroom objects.

        :param user: The User object to update.
        :type user: User

        :param new_occupied_classrooms: A list of new Classroom objects for the user to occupy.
        :type new_occupied_classrooms: list[Classroom]

        :return: The updated User object.
        :rtype: User
        """
        user.set_occupied_classrooms(new_occupied_classrooms)
        self.session.add(user)
        self.session.commit()
        return user

    @staticmethod
    def serialize_user(user):
        """
        Converts a User object into a dictionary for easy serialization.

        :param user: The User object to serialize.
        :type user: User

        :return: A dictionary representation of the User object.
        :rtype: dict
        """
        return {
            'id': user.get_id(),
            'first_name': user.get_first_name(),
            'last_name': user.get_last_name(),
            'login': user.get_login(),
            'registration_date': user.get_registration_date(),
            'is_admin': user.get_is_admin(),
            'department': user.get_department_id(),
            'managed_classrooms': [classroom.get_id() for classroom in user.get_managed_classrooms()],
            'occupied_classrooms': [classroom.get_id() for classroom in user.get_occupied_classrooms()],
            'authored_requests': [request.get_id() for request in user.get_authored_requests()],
            'requests': [request.get_id() for request in user.get_requests()]
        }
