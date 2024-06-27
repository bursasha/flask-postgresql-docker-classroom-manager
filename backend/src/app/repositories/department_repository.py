from ..orm import orm
from ..models import Department


class DepartmentRepository:
    """
    A repository for handling operations on Department objects. This class provides
    methods to interact with the Department data model, including creating departments,
    validating department data, and retrieving departments from the database.

    :ivar session: An instance of SQLAlchemy session for database operations.
    :type session: Session
    """

    def __init__(self):
        """
        Initializes the DepartmentRepository with a database session.
        """
        self.session = orm.session

    @staticmethod
    def validate_full_name(full_name):
        """
        Validates the full name of a department based on length constraints.

        :param full_name: The full name of the department to validate.
        :type full_name: str

        :return: True if the full name is valid (length between 1 and 100 characters), False otherwise.
        :rtype: bool
        """
        return 0 < len(full_name) <= 100

    @staticmethod
    def validate_code_name(code_name):
        """
        Validates the code name of a department based on length constraints.

        :param code_name: The code name of the department to validate.
        :type code_name: str

        :return: True if the code name is valid (length between 1 and 50 characters), False otherwise.
        :rtype: bool
        """
        return 0 < len(code_name) <= 50

    def create_department(self, full_name, code_name):
        """
        Creates and saves a new Department object if the provided full name and code name are valid.

        :param full_name: The full name of the department.
        :type full_name: str

        :param code_name: The code name of the department.
        :type code_name: str

        :return: The newly created Department object.
        :rtype: Department
        """
        new_department = Department(full_name=full_name, code_name=code_name)
        self.session.add(new_department)
        self.session.commit()
        return new_department

    def get_all_departments(self):
        """
        Retrieves all departments from the database.

        :return: A list of all Department objects.
        :rtype: list[Department]
        """
        return self.session.query(Department).all()

    def get_department_by_id(self, id):
        """
        Retrieves a department by its ID.

        :param id: The ID of the department to retrieve.
        :type id: int

        :return: The Department object with the specified ID, or None if not found.
        :rtype: Department or None
        """
        return self.session.query(Department).filter_by(id=id).first()

    def get_department_by_full_name(self, full_name):
        """
        Retrieves a department by its full name.

        :param full_name: The full name of the department to retrieve.
        :type full_name: str

        :return: The Department object with the specified full name, or None if not found.
        :rtype: Department or None
        """
        return self.session.query(Department).filter_by(full_name=full_name).first()

    def get_department_by_code_name(self, code_name):
        """
        Retrieves a department by its code name.

        :param code_name: The code name of the department to retrieve.
        :type code_name: str

        :return: The Department object with the specified code name, or None if not found.
        :rtype: Department or None
        """
        return self.session.query(Department).filter_by(code_name=code_name).first()

    def update_department_full_name(self, department, new_full_name):
        """
        Updates the full name of a specific department.

        :param department: The Department object to update.
        :type department: Department

        :param new_full_name: The new full name for the department.
        :type new_full_name: str

        :return: The updated Department object.
        :rtype: Department
        """
        department.set_full_name(new_full_name)
        self.session.add(department)
        self.session.commit()
        return department

    def update_department_code_name(self, department, new_code_name):
        """
        Updates the code name of a specific department.

        :param department: The Department object to update.
        :type department: Department

        :param new_code_name: The new code name for the department.
        :type new_code_name: str

        :return: The updated Department object.
        :rtype: Department
        """
        department.set_code_name(new_code_name)
        self.session.add(department)
        self.session.commit()
        return department

    def update_department_manager(self, department, new_manager_id):
        """
        Updates the manager of a specific department.

        :param department: The Department object to update.
        :type department: Department

        :param new_manager_id: The new manager's id (User object) for the department.
        :type new_manager_id: int

        :return: The updated Department object.
        :rtype: Department
        """
        department.set_manager_id(new_manager_id)
        self.session.add(department)
        self.session.commit()
        return department

    @staticmethod
    def serialize_department(department):
        """
        Converts a Department object into a dictionary for easy serialization.

        :param department: The Department object to serialize.
        :type department: Department

        :return: A dictionary representation of the Department object.
        :rtype: dict
        """
        return {
            'id': department.get_id(),
            'full_name': department.get_full_name(),
            'code_name': department.get_code_name(),
            'manager': department.get_manager_id(),
            'users': [user.get_id() for user in department.get_users()],
            'classrooms': [classroom.get_id() for classroom in department.get_classrooms()]
        }
