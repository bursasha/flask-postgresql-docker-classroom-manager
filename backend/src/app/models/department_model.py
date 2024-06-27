from ..orm import orm


class Department(orm.Model):
    """
    The Department data model class represents the structure of a department's data within the database.
    Departments are administrative units within an institution, such as a university or a company,
    typically managing several users and classrooms.

    :ivar id: Unique identifier for a department, acting as the primary key in the database.
    :type id: int

    :ivar full_name: The formal, complete name of the department, which may include its function
                     or area of expertise.
    :type full_name: str

    :ivar code_name: A short code name or abbreviation for the department, used for easier
                     reference and in situations where space is limited.
    :type code_name: str

    :ivar manager_id: Foreign key to associate the department with its manager (a user).
    :type manager_id: int

    :ivar users: A collection of User objects that are part of the department, defined by a
                 one-to-many relationship. This represents all the users, including employees,
                 students, or staff, associated with the department.
    :type users: list[User]

    :ivar classrooms: A collection of Classroom objects that are administratively grouped under
                      the department, defined by a one-to-many relationship. This represents the
                      physical spaces the department is responsible for.
    :type classrooms: list[Classroom]
    """
    __tablename__ = 'department_table'

    id = orm.Column(orm.Integer, primary_key=True)
    full_name = orm.Column(orm.String(100), nullable=False)
    code_name = orm.Column(orm.String(50), nullable=False)

    manager_id = orm.Column(orm.Integer, unique=True, nullable=True)
    # manager_id = 0
    users = orm.relationship('User', foreign_keys='User.department_id', back_populates='department')
    # users = []

    classrooms = orm.relationship('Classroom', foreign_keys='Classroom.department_id', back_populates='department')
    # classrooms = []

    def __init__(self, full_name, code_name):
        """
        Initializes a new instance of the Department model with a given full name and code name.

        :param full_name: The full, formal name of the department.
        :param code_name: The short code name or abbreviation for the department.
        """
        self.full_name = full_name
        self.code_name = code_name
        orm.session.add(self)
        orm.session.commit()

    def __repr__(self):
        """
        Provides a string representation of the Department instance, containing its code name
        and full name, which can be useful for debugging and logging purposes.

        :return: A string representation of the Department instance, formatted for readability.
        :rtype: str
        """
        return f"<Department '{self.code_name}' - '{self.full_name}'>"

    def set_manager_id(self, user_id):
        """
        Sets the given user ID as the manager of the department.

        :param user_id: The ID of the user to be set as the manager of the department.
        :type user_id: int
        """
        self.manager_id = user_id
        orm.session.add(self)
        orm.session.commit()

    def set_full_name(self, new_full_name):
        """
        Sets a new formal, complete name for the department.

        :param new_full_name: The new formal, complete name for the department.
        :type new_full_name: str
        """
        self.full_name = new_full_name
        orm.session.add(self)
        orm.session.commit()

    def set_code_name(self, new_code_name):
        """
        Sets a new code name or abbreviation for the department.

        :param new_code_name: The new code name or abbreviation for the department.
        :type new_code_name: str
        """
        self.code_name = new_code_name
        orm.session.add(self)
        orm.session.commit()

    def get_id(self):
        """
        Retrieves the unique identifier of the department.

        :return: The unique identifier of the department.
        :rtype: int
        """
        return self.id

    def get_full_name(self):
        """
        Retrieves the formal, complete name of the department.

        :return: The formal, complete name of the department.
        :rtype: str
        """
        return self.full_name

    def get_code_name(self):
        """
        Retrieves the short code name or abbreviation for the department.

        :return: The short code name or abbreviation for the department.
        :rtype: str
        """
        return self.code_name

    def get_manager_id(self):
        """
        Retrieves the foreign key id of the user who manages the department.

        :return: The foreign key id of the manager.
        :rtype: int or None
        """
        return self.manager_id

    def get_users(self):
        """
        Retrieves a collection of User objects that are part of the department.

        :return: A list of User objects associated with the department.
        :rtype: list[User]
        """
        return self.users

    def get_classrooms(self):
        """
        Retrieves a collection of Classroom objects that are administratively grouped under the department.

        :return: A list of Classroom objects associated with the department.
        :rtype: list[Classroom]
        """
        return self.classrooms
