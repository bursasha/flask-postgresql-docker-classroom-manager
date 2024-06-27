from ..repositories import DepartmentRepository, UserRepository


class DepartmentService:
    """
    The DepartmentService class provides a high-level interface for managing and interacting with Department-related
    data and operations. It acts as a mediator between the application logic and the database operations conducted by
    the DepartmentRepository, ensuring efficient and organized access to departmental information.

    This service centralizes the logic needed to perform common tasks related to departments, such as creating,
    updating, and retrieving department information. It abstracts away the complexities of direct database interactions
    and offers a simplified set of methods for the application to utilize.

    DepartmentRepository - Manages interactions with the Department data model, handling the creation, retrieval,
    and updating of department records.

    UserRepository - Used for accessing and modifying user information, particularly when dealing with departmental
    associations or managing department heads.
    """

    def __init__(self):
        """
        Initializes the DepartmentService with instances of DepartmentRepository and UserRepository.
        This setup allows for comprehensive management of departmental data, including handling the associations between
        departments and users, such as department heads and members.
        """
        self.department_repository = DepartmentRepository()
        self.user_repository = UserRepository()

    def create_department(self, full_name, code_name):
        """
        Creates a new department with the specified full name and code name.

        :param full_name: The full, formal name of the department.
        :type full_name: str

        :param code_name: The short code name or abbreviation for the department.
        :type code_name: str

        :return: The newly created Department object.
        :rtype: Department

        :raises ValueError: If the full name or code name is invalid or if a department with the same full and
                            code names already exists.
        """
        if not self.department_repository.validate_full_name(full_name):
            raise ValueError("Invalid full name length. Full name must be 1-100 characters long.")

        if not self.department_repository.validate_code_name(code_name):
            raise ValueError("Invalid code name length. Code name must be 1-50 characters long.")

        existing_department_by_full_name = self.department_repository.get_department_by_full_name(full_name)
        existing_department_by_code_name = self.department_repository.get_department_by_code_name(code_name)

        if existing_department_by_full_name and existing_department_by_code_name:
            if existing_department_by_full_name.get_id() == existing_department_by_code_name.get_id():
                raise ValueError(
                    f"A department with the full name '{full_name}' and code name '{code_name}' already exists.")

        department = self.department_repository.create_department(full_name, code_name)

        return self.department_repository.serialize_department(department)

    def update_department(self, department_id, new_full_name=None, new_code_name=None, new_manager_id=None):
        """
        Updates the specified department's details.

        :param department_id: The ID of the department to update.
        :type department_id: int

        :param new_full_name: (Optional) A new full name for the department.
        :type new_full_name: str or None

        :param new_code_name: (Optional) A new code name for the department.
        :type new_code_name: str or None

        :param new_manager_id: (Optional) The ID of the new manager for the department.
        :type new_manager_id: int or None

        :return: The updated Department object.
        :rtype: Department

        :raises ValueError: If the specified department or new manager doesn't exist, if names are invalid,
                            or if names are already taken.
        """
        department = self.department_repository.get_department_by_id(department_id)
        if not department:
            raise ValueError(f"No department found with ID: {department_id}")

        if new_full_name:
            if not self.department_repository.validate_full_name(new_full_name):
                raise ValueError("Invalid full name length. Full name must be 1-100 characters long.")
            self.department_repository.update_department_full_name(department, new_full_name)

        if new_code_name:
            if not self.department_repository.validate_code_name(new_code_name):
                raise ValueError("Invalid code name length. Code name must be 1-50 characters long.")
            self.department_repository.update_department_code_name(department, new_code_name)

        if new_manager_id:
            new_manager = self.user_repository.get_user_by_id(new_manager_id)
            if not new_manager:
                raise ValueError(f"No manager found with ID: {new_manager_id}")
            self.department_repository.update_department_manager(department, new_manager_id)

        return self.department_repository.serialize_department(department)

    def find_department(self, department_id):
        """
        Retrieves a department by its ID.

        :param department_id: The ID of the department to retrieve.
        :type department_id: int

        :return: The Department object with the specified ID.
        :rtype: Department

        :raises ValueError: If no department is found with the provided ID, indicating that the department does not exist
                            or the ID is incorrect.
        """
        department = self.department_repository.get_department_by_id(department_id)
        if department is None:
            raise ValueError(f"No department found with ID: {department_id}")

        return self.department_repository.serialize_department(department)

    def find_all_departments(self):
        """
        Retrieves all departments from the database.

        :return: A list of all Department objects.
        :rtype: list[Department]

        :raises ValueError: If no departments are found in the database, indicating an empty department list.
        """
        departments = self.department_repository.get_all_departments()
        if not departments:
            raise ValueError("No departments found in the database.")

        return {'departments':
                [self.department_repository.serialize_department(department) for department in departments]}
