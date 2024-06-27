from ..orm import orm
from ..models import Building


class BuildingRepository:
    """
    A repository for handling operations on Building objects. This class provides
    methods to interact with the Building data model, including creating buildings,
    validating building data, and retrieving buildings from the database.

    :ivar session: An instance of SQLAlchemy session for database operations.
    :type session: Session
    """

    def __init__(self):
        """
        Initializes the BuildingRepository with a database session.
        """
        self.session = orm.session

    @staticmethod
    def validate_name(name):
        """
        Validates the name of a building based on length constraints.

        :param name: The name of the building to validate.
        :type name: str

        :return: True if the name is valid (length between 1 and 50 characters), False otherwise.
        :rtype: bool
        """
        return 0 < len(name) <= 50

    @staticmethod
    def validate_address(address):
        """
        Validates the address of a building based on length constraints.

        :param address: The address of the building to validate.
        :type address: str

        :return: True if the address is valid (length between 1 and 100 characters), False otherwise.
        :rtype: bool
        """
        return 0 < len(address) <= 100

    def create_building(self, name, address):
        """
        Creates and saves a new Building object if the provided name and address are valid.

        :param name: The name of the building.
        :type name: str

        :param address: The address of the building.
        :type address: str

        :return: The newly created Building object.
        :rtype: Building
        """

        new_building = Building(name=name, address=address)
        self.session.add(new_building)
        self.session.commit()
        return new_building

    def get_all_buildings(self):
        """
        Retrieves all buildings from the database.

        :return: A list of all Building objects.
        :rtype: list[Building]
        """
        return self.session.query(Building).all()

    def get_building_by_id(self, id):
        """
        Retrieves a building by its ID.

        :param id: The ID of the building to retrieve.
        :type id: int

        :return: The Building object with the specified ID, or None if not found.
        :rtype: Building or None
        """
        return self.session.query(Building).filter_by(id=id).first()

    def get_building_by_name(self, name):
        """
        Retrieves the first building matching the given name.

        :param name: The name of the building to retrieve.
        :type name: str

        :return: The first Building object with the specified name, or None if not found.
        :rtype: Building or None
        """
        return self.session.query(Building).filter_by(name=name).first()

    def get_building_by_address(self, address):
        """
        Retrieves the first building matching the given address.

        :param address: The address of the building to retrieve.
        :type address: str

        :return: The first Building object with the specified address, or None if not found.
        :rtype: Building or None
        """
        return self.session.query(Building).filter_by(address=address).first()

    def update_building_name(self, building, new_name):
        """
        Updates the name of a specific building.

        :param building: The Building object to update.
        :type building: Building

        :param new_name: The new name for the building.
        :type new_name: str

        :return: The updated Building object.
        :rtype: Building
        """
        building.set_name(new_name)
        self.session.add(building)
        self.session.commit()
        return building

    def update_building_address(self, building, new_address):
        """
        Updates the address of a specific building.

        :param building: The Building object to update.
        :type building: Building

        :param new_address: The new address for the building.
        :type new_address: str

        :return: The updated Building object.
        :rtype: Building
        """
        building.set_address(new_address)
        self.session.add(building)
        self.session.commit()
        return building

    @staticmethod
    def serialize_building(building):
        """
        Converts a Building object into a dictionary for easy serialization.

        :param building: The Building object to serialize.
        :type building: Building

        :return: A dictionary representation of the Building object.
        :rtype: dict
        """
        return {
            'id': building.get_id(),
            'name': building.get_name(),
            'address': building.get_address(),
            'classrooms': [classroom.get_id() for classroom in building.get_classrooms()]
        }

