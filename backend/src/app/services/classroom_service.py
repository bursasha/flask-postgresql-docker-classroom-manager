from ..repositories import BuildingRepository, ClassroomRepository, DepartmentRepository, UserRepository


class ClassroomService:
    """
    The ClassroomService class provides a centralized interface for managing and interacting with Classroom-related
    data and operations. It serves as a mediator between the application logic and the database operations conducted by
    various repositories, ensuring streamlined and organized access to classroom information.

    This service encapsulates the logic required to perform tasks related to classrooms, such as creating, updating,
    and retrieving classroom details. It abstracts the complexities of direct database interactions and offers a
    simplified set of methods for the application to interact with classroom data.

    ClassroomRepository - Manages interactions with the Classroom data model, handling the creation, retrieval,
    and updating of classroom records.

    BuildingRepository - Provides access to building-related operations and data, crucial for managing the physical
    location and context of classrooms.

    DepartmentRepository - Used for accessing and managing information about departments, as classrooms are often
    associated with specific departments within an institution.

    UserRepository - Utilized for managing user information, particularly when dealing with classroom occupancy and
    management, as users can be associated with classrooms in various roles.
    """

    def __init__(self):
        """
        Initializes the ClassroomService with instances of ClassroomRepository, BuildingRepository,
        DepartmentRepository, and UserRepository. This setup allows for comprehensive management of classroom data,
        including handling associations between classrooms, buildings, departments, and users.
        """
        self.classroom_repository = ClassroomRepository()
        self.building_repository = BuildingRepository()
        self.department_repository = DepartmentRepository()
        self.user_repository = UserRepository()

    def create_classroom(self, name, floor, is_private):
        """
        Creates a new classroom with the given name, floor, and privacy status.

        :param name: The name of the classroom.
        :type name: str

        :param floor: The floor number where the classroom is located.
        :type floor: int

        :param is_private: Indicates whether the classroom is private.
        :type is_private: bool

        :return: The newly created Classroom object.
        :rtype: Classroom

        :raises ValueError: If the name is invalid or the classroom already exists.
        """
        if not self.classroom_repository.validate_name(name):
            raise ValueError("Invalid name length. Name must be 1-50 characters long.")

        classroom = self.classroom_repository.create_classroom(name, floor, is_private)

        return self.classroom_repository.serialize_classroom(classroom)

    def update_classroom(self, classroom_id, new_name=None, new_building_id=None, new_department_id=None,
                         new_manager_id=None, new_is_private=None):
        """
        Updates the details of an existing classroom.

        :param classroom_id: The ID of the classroom to update.
        :type classroom_id: int

        :param new_name: (Optional) The new name for the classroom.
        :type new_name: str or None

        :param new_building_id: (Optional) The ID of the new building for the classroom.
        :type new_building_id: int or None

        :param new_department_id: (Optional) The ID of the new department for the classroom.
        :type new_department_id: int or None

        :param new_manager_id: (Optional) The ID of the new manager for the classroom.
        :type new_manager_id: int or None

        :param new_is_private: (Optional) The new privacy status for the classroom.
        :type new_is_private: bool or None

        :return: The updated Classroom object.
        :rtype: Classroom

        :raises ValueError: If the specified classroom or related entities don't exist or
                            if the provided data is invalid.
        """
        classroom = self.classroom_repository.get_classroom_by_id(classroom_id)
        if not classroom:
            raise ValueError(f"No classroom found with ID: {classroom_id}")

        if new_name:
            if not self.classroom_repository.validate_name(new_name):
                raise ValueError("Invalid name length. Name must be 1-50 characters long.")
            classroom.set_name(new_name)

        if new_building_id:
            new_building = self.building_repository.get_building_by_id(new_building_id)
            if not new_building:
                raise ValueError(f"No building found with ID: {new_building_id}")
            classroom.set_building(new_building)

        if new_department_id:
            new_department = self.department_repository.get_department_by_id(new_department_id)
            if not new_department:
                raise ValueError(f"No department found with ID: {new_department_id}")
            classroom.set_department(new_department)

        if new_manager_id:
            new_manager = self.user_repository.get_user_by_id(new_manager_id)
            if not new_manager:
                raise ValueError(f"No manager found with ID: {new_manager_id}")
            classroom.set_manager(new_manager)

        if new_is_private:
            classroom.set_is_private(new_is_private)

        return self.classroom_repository.serialize_classroom(classroom)

    def find_classroom(self, classroom_id):
        """
        Retrieves a classroom by its ID.

        :param classroom_id: The ID of the classroom to retrieve.
        :type classroom_id: int

        :return: The Classroom object with the specified ID.
        :rtype: Classroom

        :raises ValueError: If no classroom is found with the provided ID, indicating that the classroom does not exist
                            or the ID is incorrect.
        """
        classroom = self.classroom_repository.get_classroom_by_id(classroom_id)
        if not classroom:
            raise ValueError(f"No classroom found with ID: {classroom_id}")

        return self.classroom_repository.serialize_classroom(classroom)

    def find_all_classrooms(self):
        """
        Retrieves all classrooms from the database.

        :return: A list of all Classroom objects.
        :rtype: list[Classroom]

        :raises ValueError: If no classrooms are found in the database, indicating an empty classroom list.
        """
        classrooms = self.classroom_repository.get_all_classrooms()
        if not classrooms:
            raise ValueError("No classrooms found in the database.")

        return {'classrooms': [self.classroom_repository.serialize_classroom(classroom) for classroom in classrooms]}

    def find_all_non_private_classrooms(self):
        """
        Retrieves all non-private classrooms from the database.

        :return: A dictionary with a key 'classrooms' containing a list of all non-private Classroom objects.
        :rtype: dict

        :raises ValueError: If no non-private classrooms are found in the database, indicating an empty classroom list.
        """
        all_classrooms = self.classroom_repository.get_all_classrooms()
        non_private_classrooms = [classroom for classroom in all_classrooms if not classroom.get_is_private()]

        if not non_private_classrooms:
            raise ValueError("No non-private classrooms found in the database.")

        return {'classrooms': [self.classroom_repository.serialize_classroom(classroom) for classroom in
                               non_private_classrooms]}

