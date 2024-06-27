from ..repositories import UserRepository, DepartmentRepository, ClassroomRepository


class UserService:
    """
    The UserService class provides a high-level interface for interacting with User-related data and operations.
    It acts as a mediator between the higher-level application logic and the lower-level database operations
    carried out by the repositories.

    This service encapsulates the logic needed to perform common tasks related to users, such as creating,
    updating, and retrieving user information. It abstracts the complexities of direct database interactions
    and provides a set of easy-to-use methods for the rest of the application.

    UserRepository - Manages interactions with the User data model, handling creation, retrieval,
    and updating of user records.

    DepartmentRepository - Provides access to department-related operations and data, which are often required when
    dealing with user information, especially in context of their departmental associations.

    ClassroomRepository - Used for accessing and modifying information about classrooms, as users can have associations
    with classrooms as occupants or managers.
    """

    def __init__(self):
        """
        Initializes the UserService with instances of UserRepository, DepartmentRepository,
        and ClassroomRepository. This setup allows for direct interaction with the data models
        and database operations related to users, their departments, and classrooms they are associated with.
        """
        self.user_repository = UserRepository()
        self.department_repository = DepartmentRepository()
        self.classroom_repository = ClassroomRepository()

    def get_user_requests_by_id(self, user_id):
        """
        Retrieves all requests made by a specific user based on the user's ID.

        :param user_id: The ID of the user whose requests are to be retrieved.
        :type user_id: int

        :return: A list of Request objects made by the specified user, or an empty list if none are found.
        :rtype: list[Request]
        """
        user = self.user_repository.get_user_by_id(user_id)
        if user:
            return user.get_requests()
        return []

    def create_user(self, first_name, last_name, login, is_admin):
        """
        Creates a new user with the given first name, last name, and login.

        :param first_name: The first name of the user. Must be a string with a length between 1 and 100 characters.
        :type first_name: str

        :param last_name: The last name of the user. Must be a string with a length between 1 and 100 characters.
        :type last_name: str

        :param login: The login identifier for the user. Must be a unique string with a length between
                      1 and 50 characters.
        :type login: str

        :param is_admin: Indicates whether the user has administrative privileges. Must be a boolean value.
        :type is_admin: bool

        :return: The newly created User object.
        :rtype: User

        :raises ValueError: If the first name or last name is not within the valid length range (1-100 characters),
                            if the login is not within the valid length range (1-50 characters),
                            or if the login already exists.
        """
        if not self.user_repository.validate_name(first_name):
            raise ValueError("Invalid first name length. Name must be 1-100 characters long.")

        if not self.user_repository.validate_name(last_name):
            raise ValueError("Invalid last name length. Name must be 1-100 characters long.")

        if not self.user_repository.validate_login(login):
            raise ValueError("Invalid login length. Login must be 1-50 characters long.")

        existing_user = self.user_repository.get_user_by_login(login)
        if existing_user:
            raise ValueError(f"The login '{login}' is already in use. Please choose a different login.")

        user = self.user_repository.create_user(first_name, last_name, login, is_admin)

        return self.user_repository.serialize_user(user)

    def update_user(self, user_id, new_first_name=None, new_last_name=None, new_department_id=None,
                    new_occupied_classroom_ids=None):
        """
        Updates the details of an existing user.

        :param user_id: The ID of the user to update.
        :type user_id: int

        :param new_first_name: (Optional) The new first name for the user.
        :type new_first_name: str or None

        :param new_last_name: (Optional) The new last name for the user.
        :type new_last_name: str or None

        :param new_department_id: (Optional) The ID of the new department for the user.
        :type new_department_id: int or None

        :param new_occupied_classroom_ids: (Optional) A list of IDs for the new classrooms the user occupies.
        :type new_occupied_classroom_ids: list[int] or None

        :return: The updated User object reflecting the changes made.
        :rtype: User

        :raises ValueError: If the specified user does not exist, the provided names are invalid,
                            the specified department does not exist, one or more of the specified classrooms
                            do not exist, or the provided data is otherwise invalid.
        """
        user = self.user_repository.get_user_by_id(user_id)
        if not user:
            raise ValueError(f"No user found with ID: {user_id}")

        if new_first_name:
            if not self.user_repository.validate_name(new_first_name):
                raise ValueError("Invalid first name length. Name must be 1-100 characters long.")
            user.set_first_name(new_first_name)

        if new_last_name:
            if not self.user_repository.validate_name(new_last_name):
                raise ValueError("Invalid last name length. Name must be 1-100 characters long.")
            user.set_last_name(new_last_name)

        if new_department_id:
            new_department = self.department_repository.get_department_by_id(new_department_id)
            if not new_department:
                raise ValueError(f"No department found with ID: {new_department_id}")
            user.set_department(new_department)

        if new_occupied_classroom_ids:
            new_occupied_classrooms = []
            for classroom_id in new_occupied_classroom_ids:
                classroom = self.classroom_repository.get_classroom_by_id(classroom_id)
                if not classroom:
                    raise ValueError(f"No classroom found with ID: {classroom_id}")
                new_occupied_classrooms.append(classroom)
            self.user_repository.update_user_occupied_classrooms(user, new_occupied_classrooms)

        return self.user_repository.serialize_user(user)

    def find_user(self, user_id):
        """
        Retrieves a user by their ID.

        :param user_id: The ID of the user to retrieve.
        :type user_id: int

        :return: The User object with the specified ID, or None if no user is found.
        :rtype: User or None

        :raises ValueError: If no user is found with the provided ID, indicating that the user does not exist
                            or the ID is incorrect.
        """
        user = self.user_repository.get_user_by_id(user_id)
        if not user:
            raise ValueError(f"No user found with ID: {user_id}")

        return self.user_repository.serialize_user(user)

    def find_all_users(self):
        """
        Retrieves all users from the database.

        :return: A list of all User objects.
        :rtype: list[User]

        :raises ValueError: If no users are found in the database, indicating an empty user list.
        """
        users = self.user_repository.get_all_users()
        if not users:
            raise ValueError("No users found in the database.")

        return {'users': [self.user_repository.serialize_user(user) for user in users]}
