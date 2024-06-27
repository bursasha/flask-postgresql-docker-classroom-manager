from ..orm import orm
from .associations import user_occupied_classroom_association, user_request_association


class User(orm.Model):
    """
    The User data model class encapsulates user information and their relationships with departments,
    classrooms, and requests within the database.

    :ivar id: Unique identifier for a user, serving as the primary key.
    :type id: int

    :ivar first_name: The user's given name.
    :type first_name: str

    :ivar last_name: The user's family name.
    :type last_name: str

    :ivar login: A unique string identifier used for the user's login credentials.
    :type login: str

    :ivar registration_date: The timestamp of when the user's information was entered into the system.
    :type registration_date: datetime

    :ivar is_admin: A boolean flag indicating whether the user has administrative privileges.
    :type is_admin: bool

    :ivar department_id: The foreign key linking the user to their department.
    :type department_id: int

    :ivar department: A reference to the Department model, establishing a many-to-one relationship,
                      where a user is part of only one department.
    :type department: Department

    :ivar managed_classrooms: A list of Classroom instances that the user manages, reflecting a one-to-many
                              relationship, where a user can manage multiple classrooms.
    :type managed_classrooms: list[Classroom]

    :ivar occupied_classrooms: A list of Classroom instances that the user occupies, defined by a many-to-many
                               relationship, representing the classrooms where the user is an occupant.
    :type occupied_classrooms: list[Classroom]

    :ivar authored_requests: A list of Request instances that the user has authored, representing a one-to-many
                             relationship, where a user can author multiple requests.
    :type authored_requests: list[Request]

    :ivar requests: A list of Request instances involving the user, defined by a many-to-many relationship,
                    representing the requests that the user is part of.
    :type requests: list[Request]
    """
    __tablename__ = 'user_table'

    id = orm.Column(orm.Integer, primary_key=True)
    first_name = orm.Column(orm.String(50), nullable=False)
    last_name = orm.Column(orm.String(50), nullable=False)
    login = orm.Column(orm.String(50), unique=True, nullable=False)
    registration_date = orm.Column(orm.DateTime, nullable=False)
    is_admin = orm.Column(orm.Boolean, default=False, nullable=False)

    department_id = orm.Column(orm.Integer, orm.ForeignKey('department_table.id'), nullable=True)
    department = orm.relationship('Department', foreign_keys=[department_id], back_populates='users')
    # department_id = 0
    # department = None

    managed_classrooms = orm.relationship('Classroom', foreign_keys='Classroom.manager_id', back_populates='manager')
    occupied_classrooms = orm.relationship(
        'Classroom', secondary='user_occupied_classroom_association',
        primaryjoin='User.id == user_occupied_classroom_association.c.user_id',
        secondaryjoin='user_occupied_classroom_association.c.classroom_id == Classroom.id',
        back_populates='occupants'
    )
    # managed_classrooms = []
    # occupied_classrooms = []

    authored_requests = orm.relationship('Request', foreign_keys='Request.author_id', back_populates='author')
    requests = orm.relationship(
        'Request', secondary=user_request_association,
        primaryjoin='User.id == user_request_association.c.user_id',
        secondaryjoin='user_request_association.c.request_id == Request.id',
        back_populates='requesting_users'
    )
    # authored_requests = []
    # requests = []

    def __init__(self, first_name, last_name, login, registration_date, is_admin):
        """
        Initializes a new User instance with the specified personal details, login credentials, registration date,
        and an optional department association.

        :param first_name: User's given name.
        :param last_name: User's family name.
        :param login: Unique login identifier for the user.
        :param registration_date: Timestamp of the user's registration.
        :param is_admin: Boolean flag indicating whether the user has administrative privileges.
        """
        self.first_name = first_name
        self.last_name = last_name
        self.login = login
        self.registration_date = registration_date
        self.is_admin = is_admin
        orm.session.add(self)
        orm.session.commit()

    def __repr__(self):
        """
        Provides a human-readable string representation of the User object, which is helpful for debugging and logging.

        :return: String representation of the User instance.
        :rtype: str
        """
        return f"<User '{self.login}' - {self.first_name} {self.last_name}>"

    def set_department(self, department):
        """
        Sets the department for the user and updates the department_id to match the given department.

        :param department: The Department object to associate with the user.
        :type department: Department
        """
        self.department = department
        orm.session.add(self)
        orm.session.commit()

    def set_first_name(self, new_first_name):
        """
        Sets a new given name for the user.

        :param new_first_name: The new given name for the user.
        :type new_first_name: str
        """
        self.first_name = new_first_name
        orm.session.add(self)
        orm.session.commit()

    def set_last_name(self, new_last_name):
        """
        Sets a new family name for the user.

        :param new_last_name: The new family name for the user.
        :type new_last_name: str
        """
        self.last_name = new_last_name
        orm.session.add(self)
        orm.session.commit()

    def set_occupied_classrooms(self, classrooms):
        """
        Sets the classrooms in which the user works.

        :param classrooms: A list of Classroom instances that the user will occupy.
        :type classrooms: list[Classroom]
        """
        self.occupied_classrooms = classrooms
        orm.session.add(self)
        orm.session.commit()

    def get_id(self):
        """
        Retrieves the unique identifier of the user.

        :return: The unique identifier of the user.
        :rtype: int
        """
        return self.id

    def get_first_name(self):
        """
        Retrieves the given name of the user.

        :return: The given name of the user.
        :rtype: str
        """
        return self.first_name

    def get_last_name(self):
        """
        Retrieves the family name of the user.

        :return: The family name of the user.
        :rtype: str
        """
        return self.last_name

    def get_login(self):
        """
        Retrieves the login identifier of the user.

        :return: The login identifier of the user.
        :rtype: str
        """
        return self.login

    def get_registration_date(self):
        """
        Retrieves the timestamp of when the user's information was entered into the system.

        :return: The registration date and time of the user.
        :rtype: datetime
        """
        return self.registration_date

    def get_is_admin(self):
        """
        Retrieves the admin status of the user.

        :return: True if the user is an admin, otherwise False.
        :rtype: bool
        """
        return self.is_admin

    def get_department_id(self):
        """
        Retrieves the foreign key linking the user to their department.

        :return: The foreign key id of the department.
        :rtype: int or None
        """
        return self.department_id

    def get_department(self):
        """
        Retrieves the Department object to which the user belongs.

        :return: The Department object associated with the user.
        :rtype: Department or None
        """
        return self.department

    def get_managed_classrooms(self):
        """
        Retrieves a list of Classroom instances that the user manages.

        :return: A list of managed Classroom objects.
        :rtype: list[Classroom]
        """
        return self.managed_classrooms

    def get_occupied_classrooms(self):
        """
        Retrieves a list of Classroom instances that the user occupies.

        :return: A list of occupied Classroom objects.
        :rtype: list[Classroom]
        """
        return self.occupied_classrooms

    def get_authored_requests(self):
        """
        Retrieves a list of Request instances that the user has authored.

        :return: A list of authored Request objects.
        :rtype: list[Request]
        """
        return self.authored_requests

    def get_requests(self):
        """
        Retrieves a list of Request instances involving the user.

        :return: A list of involved Request objects.
        :rtype: list[Request]
        """
        return self.requests
