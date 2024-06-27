from ..orm import orm
from .associations import user_occupied_classroom_association


class Classroom(orm.Model):
    """
    The Classroom data model class describes the structure of a classroom's data within the database.
    Classrooms are spaces where educational activities take place and are managed by designated users.

    :ivar id: Unique identifier for a classroom, acting as the primary key in the database.
    :type id: int

    :ivar name: The designated name of the classroom, which may include numbers or special designations.
    :type name: str

    :ivar floor: The floor number within the building on which the classroom is located, providing
                 a reference for its physical location.
    :type floor: int

    :ivar is_private: Indicates whether the classroom is private. Private classrooms might have restricted access
                      or special rules.
    :type is_private: bool

    :ivar building_id: Foreign key that associates the classroom with a specific building.
    :type building_id: int

    :ivar building: The Building object that the classroom belongs to, forming a many-to-one relationship.
                    This indicates that multiple classrooms can be part of a single building.
    :type building: Building

    :ivar department_id: Foreign key that associates the classroom with a specific department.
    :type department_id: int

    :ivar department: The Department object that the classroom belongs to, forming a many-to-one relationship.
                      This represents the administrative grouping within an institution that the classroom is associated
                      with.
    :type department: Department

    :ivar manager_id: Foreign key that associates the classroom with its manager, who is a user.
    :type manager_id: int

    :ivar manager: The User object representing the manager of the classroom. This relationship is one-to-one,
                   indicating that each classroom is managed by a single user.
    :type manager: User

    :ivar occupants: A list of User objects representing the occupants of the classroom. This is defined through
                     a many-to-many relationship with the User model, facilitated by the
                     'user_occupied_classroom_association' table.
    :type occupants: list[User]

    :ivar requests: A list of Request objects representing requests made for the classroom. This relationship is
                    one-to-many, indicating that a classroom can have multiple requests associated with it.
    :type requests: list[Request]
    """
    __tablename__ = 'classroom_table'

    id = orm.Column(orm.Integer, primary_key=True)
    name = orm.Column(orm.String(50), nullable=False)
    floor = orm.Column(orm.Integer, nullable=False)
    is_private = orm.Column(orm.Boolean, nullable=False)

    building_id = orm.Column(orm.Integer, orm.ForeignKey('building_table.id'), nullable=True)
    building = orm.relationship('Building', foreign_keys=[building_id], back_populates='classrooms')
    # building_id = 0
    # building = None

    department_id = orm.Column(orm.Integer, orm.ForeignKey('department_table.id'), nullable=True)
    department = orm.relationship('Department', foreign_keys=[department_id], back_populates='classrooms')
    # department_id = 0
    # department = None

    manager_id = orm.Column(orm.Integer, orm.ForeignKey('user_table.id'), nullable=True)
    manager = orm.relationship('User', foreign_keys=[manager_id], back_populates='managed_classrooms', uselist=False)
    occupants = orm.relationship('User',
                                 secondary='user_occupied_classroom_association',
                                 primaryjoin='Classroom.id == user_occupied_classroom_association.c.classroom_id',
                                 secondaryjoin='user_occupied_classroom_association.c.user_id == User.id',
                                 back_populates='occupied_classrooms')
    # manager_id = 0
    # manager = None
    # occupants = []

    requests = orm.relationship('Request', foreign_keys='Request.classroom_id', back_populates='classroom')
    # requests = []

    def __init__(self, name, floor, is_private):
        """
        Initializes a new instance of the Classroom model with specified attributes.

        :param name: The name of the classroom.
        :type name: str

        :param floor: The floor where the classroom is located.
        :type floor: int

        :param is_private: Indicates if the classroom is private.
        :type is_private: bool
        """
        self.name = name
        self.floor = floor
        self.is_private = is_private
        orm.session.add(self)
        orm.session.commit()

    def __repr__(self):
        """
        Provides a string representation of the Classroom instance, which includes its name,
        floor number, and the building it is located in, useful for debugging and logging.

        :return: A string representation of the Classroom instance.
        :rtype: str
        """
        return f"<Classroom '{self.name}' on floor {self.floor}, in building '{self.building.name}'>"

    def set_building(self, building):
        """
        Sets the given Building as the location of the classroom.

        :param building: The Building instance where the classroom is located.
        :type building: Building
        """
        self.building = building
        orm.session.add(self)
        orm.session.commit()

    def set_department(self, department):
        """
        Sets the given Department as the administrative unit of the classroom.

        :param department: The Department instance to which the classroom belongs.
        :type department: Department
        """
        self.department = department
        orm.session.add(self)
        orm.session.commit()

    def set_manager(self, user):
        """
        Sets the given User as the manager of the classroom.

        :param user: The User instance to be set as the manager of the classroom.
        :type user: User
        """
        self.manager = user
        orm.session.add(self)
        orm.session.commit()

    def set_name(self, new_name):
        """
        Sets a new name for the classroom.

        :param new_name: The new name for the classroom.
        :type new_name: str
        """
        self.name = new_name
        orm.session.add(self)
        orm.session.commit()

    def set_is_private(self, new_value):
        """
        Sets the privacy status of the classroom.

        :param new_value: The new privacy status of the classroom.
        :type new_value: bool
        """
        self.is_private = new_value
        orm.session.add(self)
        orm.session.commit()

    def get_is_private(self):
        """
        Retrieves the privacy status of the classroom.

        :return: The privacy status of the classroom.
        :rtype: bool
        """
        return self.is_private

    def get_id(self):
        """
        Retrieves the unique identifier of the classroom.

        :return: The unique identifier of the classroom.
        :rtype: int
        """
        return self.id

    def get_name(self):
        """
        Retrieves the name of the classroom.

        :return: The name of the classroom.
        :rtype: str
        """
        return self.name

    def get_floor(self):
        """
        Retrieves the floor number where the classroom is located.

        :return: The floor number of the classroom.
        :rtype: int
        """
        return self.floor

    def get_building_id(self):
        """
        Retrieves the foreign key id of the building to which the classroom belongs.

        :return: The foreign key id of the building.
        :rtype: int or None
        """
        return self.building_id

    def get_building(self):
        """
        Retrieves the Building object associated with the classroom.

        :return: The Building object associated with the classroom.
        :rtype: Building or None
        """
        return self.building

    def get_department_id(self):
        """
        Retrieves the foreign key id of the department to which the classroom belongs.

        :return: The foreign key id of the department.
        :rtype: int or None
        """
        return self.department_id

    def get_department(self):
        """
        Retrieves the Department object associated with the classroom.

        :return: The Department object associated with the classroom.
        :rtype: Department or None
        """
        return self.department

    def get_manager_id(self):
        """
        Retrieves the foreign key id of the user who manages the classroom.

        :return: The foreign key id of the manager.
        :rtype: int or None
        """
        return self.manager_id

    def get_manager(self):
        """
        Retrieves the User object representing the manager of the classroom.

        :return: The User object representing the manager of the classroom.
        :rtype: User or None
        """
        return self.manager

    def get_occupants(self):
        """
        Retrieves a list of User objects representing the occupants of the classroom.

        :return: A list of User objects representing the occupants.
        :rtype: list[User]
        """
        return self.occupants

    def get_requests(self):
        """
        Retrieves a list of Request objects representing requests made for the classroom.

        :return: A list of Request objects associated with the classroom.
        :rtype: list[Request]
        """
        return self.requests
