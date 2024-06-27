from ..repositories import BuildingRepository


class BuildingService:
    """
    The BuildingService class offers a high-level interface for managing Building-related data and operations within
    the application. It acts as a liaison between the application's higher-level logic and the lower-level database
    operations executed by the BuildingRepository.

    This service centralizes the logic necessary to carry out common tasks related to buildings, such as creating,
    updating, and retrieving building information. It simplifies interactions with building data, abstracting the
    intricacies of direct database transactions into a set of straightforward methods for the application to utilize.

    BuildingRepository - Handles interactions with the Building data model, managing the creation, retrieval, and
    updating of building records. It ensures that building data is accessed and modified in a consistent and controlled
    manner, providing a reliable foundation for the service's operations.
    """

    def __init__(self):
        """
        Initializes the BuildingService with an instance of BuildingRepository. The repository provides a layer of
        abstraction over the database, ensuring that the service's interactions with building data are efficient and
        well-organized.
        """
        self.building_repository = BuildingRepository()

    def create_building(self, name, address):
        """
        Creates a new building with the specified name and address.

        :param name: The name of the building.
        :type name: str

        :param address: The address of the building.
        :type address: str

        :return: The newly created Building object.
        :rtype: Building

        :raises ValueError: If the name or address is invalid or if a building with the same name
                            and address already exists.
        """
        if not self.building_repository.validate_name(name):
            raise ValueError("Invalid name length. Name must be 1-50 characters long.")

        if not self.building_repository.validate_address(address):
            raise ValueError("Invalid address length. Address must be 1-100 characters long.")

        existing_building_by_name = self.building_repository.get_building_by_name(name)
        existing_building_by_address = self.building_repository.get_building_by_address(address)

        if existing_building_by_name and existing_building_by_address:
            if existing_building_by_name.get_id() == existing_building_by_address.get_id():
                raise ValueError(f"A building with the name '{name}' at address '{address}' already exists.")

        building = self.building_repository.create_building(name, address)

        return self.building_repository.serialize_building(building)

    def update_building(self, building_id, new_name=None, new_address=None):
        """
        Updates the specified building's details.

        :param building_id: The ID of the building to update.
        :type building_id: int

        :param new_name: (Optional) A new name for the building.
        :type new_name: str or None

        :param new_address: (Optional) A new address for the building.
        :type new_address: str or None

        :return: The updated Building object.
        :rtype: Building

        :raises ValueError: If the specified building doesn't exist, if the new name or address is invalid,
                            or if the new name conflicts with an existing building.
        """
        building = self.building_repository.get_building_by_id(building_id)
        if not building:
            raise ValueError(f"No building found with ID: {building_id}")

        if new_name:
            if not self.building_repository.validate_name(new_name):
                raise ValueError("Invalid name length. Name must be 1-50 characters long.")
            building.set_name(new_name)

        if new_address:
            if not self.building_repository.validate_address(new_address):
                raise ValueError("Invalid address length. Address must be 1-100 characters long.")
            building.set_address(new_address)

        return self.building_repository.serialize_building(building)

    def find_building(self, building_id):
        """
        Retrieves a building by its ID.

        :param building_id: The ID of the building to retrieve.
        :type building_id: int

        :return: The Building object with the specified ID.
        :rtype: Building

        :raises ValueError: If no building is found with the provided ID, indicating that the building does not exist
                            or the ID is incorrect.
        """
        building = self.building_repository.get_building_by_id(building_id)
        if building is None:
            raise ValueError(f"No building found with ID: {building_id}")

        return self.building_repository.serialize_building(building)

    def find_all_buildings(self):
        """
        Retrieves all buildings from the database.

        :return: A list of all Building objects.
        :rtype: list[Building]

        :raises ValueError: If no buildings are found in the database.
        """
        buildings = self.building_repository.get_all_buildings()
        if not buildings:
            raise ValueError("No buildings found in the database.")

        return {'buildings': [self.building_repository.serialize_building(building) for building in buildings]}
