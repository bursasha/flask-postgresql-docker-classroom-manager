from ..orm import orm
# from .associations import user_request_association


class Request(orm.Model):
    """
    The Request data model class describes the structure of a request in the database.

    :ivar id: Unique identifier for a request, acting as the primary key.
    :type id: int

    :ivar start_date: The date and time when the request starts.
    :type start_date: datetime

    :ivar end_date: The date and time when the request ends.
    :type end_date: datetime

    :ivar registration_date: The date and time when the request was registered.
    :type registration_date: datetime

    :ivar is_approved: Indicates whether the request has been approved.
    :type is_approved: bool

    :ivar author_id: The identifier for the user who authored the request.
    :type author_id: int

    :ivar author: The User who authored the request, establishing a many-to-one relationship.
    :type author: User

    :ivar requesting_users: List of users who are requesting or are involved in the request,
                            defined by a many-to-many relationship.
    :type requesting_users: list[User]

    :ivar classroom_id: The identifier for the classroom to which the request refers.
    :type classroom_id: int

    :ivar classroom: The Classroom to which the request refers, establishing a many-to-one relationship.
    :type classroom: Classroom
    """
    __tablename__ = 'request_table'

    id = orm.Column(orm.Integer, primary_key=True)
    start_date = orm.Column(orm.DateTime, nullable=False)
    end_date = orm.Column(orm.DateTime, nullable=False)
    registration_date = orm.Column(orm.DateTime, nullable=False)
    is_approved = orm.Column(orm.Boolean, nullable=False)

    author_id = orm.Column(orm.Integer, orm.ForeignKey('user_table.id'), nullable=True)
    author = orm.relationship('User', foreign_keys=[author_id], back_populates='authored_requests')
    requesting_users = orm.relationship('User', secondary='user_request_association',
                                        primaryjoin='Request.id == user_request_association.c.request_id',
                                        secondaryjoin='user_request_association.c.user_id == User.id',
                                        back_populates='requests')
    # author_id = 0
    # author = None
    # requesting_users = []

    classroom_id = orm.Column(orm.Integer, orm.ForeignKey('classroom_table.id'), nullable=True)
    classroom = orm.relationship('Classroom', foreign_keys=[classroom_id], back_populates='requests')
    # classroom_id = 0
    # classroom = None

    def __init__(self, start_date, end_date, registration_date, is_approved):
        """
        Initializes a new instance of the Request model with given dates, author, and associated classroom.

        :param start_date: The start date and time for the request.
        :param end_date: The end date and time for the request.
        :param registration_date: The date and time when the request was made.
        :param is_approved: Indicates whether the request has been approved or not.
        """
        self.start_date = start_date
        self.end_date = end_date
        self.registration_date = registration_date
        self.is_approved = is_approved
        orm.session.add(self)
        orm.session.commit()

    def __repr__(self):
        """
        Provides a string representation of the Request instance, useful for debugging and logging.

        :return: A string representation of the Request instance.
        :rtype: str
        """
        return f"<Request id - {self.id}, author - {self.author.login}, classroom - {self.classroom.name}>"

    def set_author(self, user):
        """
        Sets the given User as the author of the request.

        :param user: The User instance to be set as the author of the request.
        :type user: User
        """
        self.author = user
        orm.session.add(self)
        orm.session.commit()

    def set_classroom(self, classroom):
        """
        Sets the given Classroom as the target of the request.

        :param classroom: The Classroom instance to be associated with the request.
        :type classroom: Classroom
        """
        self.classroom = classroom
        orm.session.add(self)
        orm.session.commit()

    def set_is_approved(self, new_value):
        """
        Sets the approval status of the request.

        :param new_value: The new approval status for the request.
        :type new_value: bool
        """
        self.is_approved = new_value
        orm.session.add(self)
        orm.session.commit()

    def set_requesting_users(self, users):
        """
        Sets the list of requesting users for the request.

        :param users: A list of User objects who are requesting or involved in the request.
        :type users: list[User]
        """
        self.requesting_users = users
        orm.session.add(self)
        orm.session.commit()

    def get_id(self):
        """
        Retrieves the unique identifier of the request.

        :return: The unique identifier of the request.
        :rtype: int
        """
        return self.id

    def get_start_date(self):
        """
        Retrieves the start date and time of the request.

        :return: The start date and time of the request.
        :rtype: datetime
        """
        return self.start_date

    def get_end_date(self):
        """
        Retrieves the end date and time of the request.

        :return: The end date and time of the request.
        :rtype: datetime
        """
        return self.end_date

    def get_registration_date(self):
        """
        Retrieves the registration date and time of the request.

        :return: The registration date and time of the request.
        :rtype: datetime
        """
        return self.registration_date

    def get_is_approved(self):
        """
        Retrieves the approval status of the request.

        :return: The approval status of the request.
        :rtype: bool
        """
        return self.is_approved

    def get_author_id(self):
        """
        Retrieves the identifier for the user who authored the request.

        :return: The identifier of the author.
        :rtype: int or None
        """
        return self.author_id

    def get_author(self):
        """
        Retrieves the User object who authored the request.

        :return: The User object representing the author of the request.
        :rtype: User or None
        """
        return self.author

    def get_requesting_users(self):
        """
        Retrieves the list of users who are requesting or are involved in the request.

        :return: A list of User objects who are requesting or involved in the request.
        :rtype: list[User]
        """
        return self.requesting_users

    def get_classroom_id(self):
        """
        Retrieves the identifier for the classroom to which the request refers.

        :return: The identifier for the classroom.
        :rtype: int or None
        """
        return self.classroom_id

    def get_classroom(self):
        """
        Retrieves the Classroom object to which the request refers.

        :return: The Classroom object associated with the request.
        :rtype: Classroom or None
        """
        return self.classroom
