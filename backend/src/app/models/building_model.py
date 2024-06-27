from ..orm import orm


class Building(orm.Model):
    """
    The Building data model class represents the structure of a building's data within the database.
    Buildings are identified by their name and address and can contain multiple classrooms.

    :ivar id: Unique identifier for a building, acting as the primary key.
    :type id: int

    :ivar name: The formal name of the building, which may include numbers or names of significant figures.
    :type name: str

    :ivar address: The physical street address of the building for locating it geographically.
    :type address: str

    :ivar classrooms: A collection of Classroom objects that are physically located within the building,
                      establishing a one-to-many relationship with the Classroom model.
    :type classrooms: list[Classroom]
    """
    __tablename__ = 'building_table'

    id = orm.Column(orm.Integer, primary_key=True)
    name = orm.Column(orm.String(50), nullable=False)
    address = orm.Column(orm.String(100), nullable=False)

    classrooms = orm.relationship('Classroom', back_populates='building')

    def __init__(self, name, address):
        """
        Initializes a new instance of the Building model with a given name and address.

        :param name: The name of the building.
        :type name: str

        :param address: The physical address of the building.
        :type address: str
        """
        self.name = name
        self.address = address
        orm.session.add(self)
        orm.session.commit()

    def __repr__(self):
        """
        Provides a string representation of the Building instance, containing its name and address,
        which can be useful for debugging and logging purposes.

        :return: A string representation of the Building instance, formatted for readability.
        :rtype: str
        """
        return f"<Building '{self.name}' at '{self.address}'>"

    def set_name(self, new_name):
        """
        Sets a new name for the building.

        :param new_name: The new name to assign to the building.
        :type new_name: str
        """
        self.name = new_name
        orm.session.add(self)
        orm.session.commit()

    def set_address(self, new_address):
        """
        Sets a new address for the building.

        :param new_address: The new address to assign to the building.
        :type new_address: str
        """
        self.address = new_address
        orm.session.add(self)
        orm.session.commit()

    def get_id(self):
        """
        Retrieves the unique identifier of the building.

        :return: The unique identifier of the building.
        :rtype: int
        """
        return self.id

    def get_name(self):
        """
        Retrieves the name of the building.

        :return: The name of the building.
        :rtype: str
        """
        return self.name

    def get_address(self):
        """
        Retrieves the address of the building.

        :return: The address of the building.
        :rtype: str
        """
        return self.address

    def get_classrooms(self):
        """
        Retrieves the collection of Classroom objects that are physically located within the building.

        :return: A list of Classroom objects located within the building.
        :rtype: list[Classroom]
        """
        return self.classrooms
