from ..orm import orm
from ..models import Classroom


class ClassroomRepository:
    """
    A repository for handling operations on Classroom objects. This class provides
    methods to interact with the Classroom data model, including creating classrooms,
    validating classroom data, and retrieving classrooms from the database.

    :ivar session: An instance of SQLAlchemy session for database operations.
    :type session: Session
    """

    def __init__(self):
        """
        Initializes the ClassroomRepository with a database session.
        """
        self.session = orm.session

    @staticmethod
    def validate_name(name):
        """
        Validates the name of a classroom based on length constraints.

        :param name: The name of the classroom to validate.
        :type name: str

        :return: True if the name is valid (length between 1 and 50 characters), False otherwise.
        :rtype: bool
        """
        return 0 < len(name) <= 50

    def create_classroom(self, name, floor, is_private):
        """
        Creates and saves a new Classroom object with the provided details.

        :param name: The name of the classroom.
        :type name: str

        :param floor: The floor where the classroom is located.
        :type floor: int

        :param is_private: Indicates whether the classroom is private or not.
        :type is_private: bool

        :return: The newly created Classroom object.
        :rtype: Classroom
        """
        new_classroom = Classroom(name=name, floor=floor, is_private=is_private)
        self.session.add(new_classroom)
        self.session.commit()
        return new_classroom

    def get_all_classrooms(self):
        """
        Retrieves all classrooms from the database.

        :return: A list of all Classroom objects.
        :rtype: list[Classroom]
        """
        return self.session.query(Classroom).all()

    def get_classroom_by_id(self, id):
        """
        Retrieves a classroom by its ID.

        :param id: The ID of the classroom to retrieve.
        :type id: int

        :return: The Classroom object with the specified ID, or None if not found.
        :rtype: Classroom or None
        """
        return self.session.query(Classroom).filter_by(id=id).first()

    def update_classroom_building(self, classroom, new_building):
        """
        Updates the building of a specific classroom.

        :param classroom: The Classroom object to update.
        :type classroom: Classroom

        :param new_building: The new Building object for the classroom.
        :type new_building: Building

        :return: The updated Classroom object.
        :rtype: Classroom
        """
        classroom.set_building(new_building)
        self.session.add(classroom)
        self.session.commit()
        return classroom

    def update_classroom_department(self, classroom, new_department):
        """
        Updates the department of a specific classroom.

        :param classroom: The Classroom object to update.
        :type classroom: Classroom

        :param new_department: The new Department object for the classroom.
        :type new_department: Department

        :return: The updated Classroom object.
        :rtype: Classroom
        """
        classroom.set_department(new_department)
        self.session.add(classroom)
        self.session.commit()
        return classroom

    def update_classroom_manager(self, classroom, new_manager):
        """
        Updates the manager of a specific classroom.

        :param classroom: The Classroom object to update.
        :type classroom: Classroom

        :param new_manager: The new User object to be set as the manager of the classroom.
        :type new_manager: User

        :return: The updated Classroom object.
        :rtype: Classroom
        """
        classroom.set_manager(new_manager)
        self.session.add(classroom)
        self.session.commit()
        return classroom

    def update_classroom_name(self, classroom, new_name):
        """
        Updates the name of a specific classroom.

        :param classroom: The Classroom object to update.
        :type classroom: Classroom

        :param new_name: The new name for the classroom.
        :type new_name: str

        :return: The updated Classroom object.
        :rtype: Classroom
        """
        classroom.set_name(new_name)
        self.session.add(classroom)
        self.session.commit()
        return classroom

    @staticmethod
    def serialize_classroom(classroom):
        """
        Converts a Classroom object into a dictionary for easy serialization.

        :param classroom: The Classroom object to serialize.
        :type classroom: Classroom

        :return: A dictionary representation of the Classroom object.
        :rtype: dict
        """
        return {
            'id': classroom.get_id(),
            'name': classroom.get_name(),
            'floor': classroom.get_floor(),
            'is_private': classroom.get_is_private(),
            'building': classroom.get_building_id(),
            'department': classroom.get_department_id(),
            'manager': classroom.get_manager_id(),
            'occupants': [occupant.get_id() for occupant in classroom.get_occupants()],
            'requests': [request.get_id() for request in classroom.get_requests()]
        }
