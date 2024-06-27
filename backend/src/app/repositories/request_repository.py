from datetime import datetime as dt

from ..orm import orm
from ..models import Request


class RequestRepository:
    """
    A repository for handling operations on Request objects. This class provides
    methods to interact with the Request data model, including creating requests,
    and retrieving requests from the database.

    :ivar session: An instance of SQLAlchemy session for database operations.
    :type session: Session
    """

    def __init__(self):
        """
        Initializes the RequestRepository with a database session.
        """
        self.session = orm.session

    @staticmethod
    def validate_dates(start_date, end_date):
        """
        Validates the start and end dates of a request.

        :param start_date: The start date of the request.
        :type start_date: datetime

        :param end_date: The end date of the request.
        :type end_date: datetime

        :return: True if the dates are valid, False otherwise.
        :rtype: bool
        """
        return start_date < end_date

    def create_request(self, start_date, end_date):
        """
        Creates and saves a new Request object if the provided dates are valid.

        :param start_date: The start date and time for the request.
        :type start_date: datetime

        :param end_date: The end date and time for the request.
        :type end_date: datetime

        :return: The newly created Request object without an author or a classroom.
        :rtype: Request
        """
        new_request = Request(start_date=start_date, end_date=end_date, registration_date=dt.now(), is_approved=False)
        self.session.add(new_request)
        self.session.commit()
        return new_request

    def get_all_requests(self):
        """
        Retrieves all requests from the database.

        :return: A list of all Request objects.
        :rtype: list[Request]
        """
        return self.session.query(Request).all()

    def get_request_by_id(self, id):
        """
        Retrieves a request by its ID.

        :param id: The ID of the request to retrieve.
        :type id: int

        :return: The Request object with the specified ID, or None if not found.
        :rtype: Request or None
        """
        return self.session.query(Request).filter_by(id=id).first()

    def get_requests_by_author_id(self, author_id):
        """
        Retrieves requests authored by a specific user based on the user's ID.

        :param author_id: The ID of the author of the requests.
        :type author_id: int

        :return: A list of Request objects authored by the specified user.
        :rtype: list[Request]
        """
        return self.session.query(Request).filter_by(author_id=author_id).all()

    def get_requests_by_classroom_id(self, classroom_id):
        """
        Retrieves requests associated with a specific classroom based on the classroom's ID.

        :param classroom_id: The ID of the classroom of the requests.
        :type classroom_id: int

        :return: A list of Request objects associated with the specified classroom.
        :rtype: list[Request]
        """
        return self.session.query(Request).filter_by(classroom_id=classroom_id).all()

    def get_requests_by_date_range(self, start_date, end_date):
        """
        Retrieves requests within a specific date range.

        :param start_date: The start date of the range.
        :type start_date: datetime

        :param end_date: The end date of the range.
        :type end_date: datetime

        :return: A list of Request objects within the specified date range.
        :rtype: list[Request]
        """
        return self.session.query(Request).filter(Request.start_date >= start_date, Request.end_date <= end_date).all()

    def update_request_author(self, request, new_author):
        """
        Updates the author of a specific request.

        :param request: The Request object to update.
        :type request: Request

        :param new_author: The new author for the request.
        :type new_author: User

        :return: The updated Request object.
        :rtype: Request
        """
        request.set_author(new_author)
        self.session.add(request)
        self.session.commit()
        return request

    def update_request_classroom(self, request, new_classroom):
        """
        Updates the target classroom of a specific request.

        :param request: The Request object to update.
        :type request: Request

        :param new_classroom: The new target classroom for the request.
        :type new_classroom: Classroom

        :return: The updated Request object.
        :rtype: Request
        """
        request.set_classroom(new_classroom)
        self.session.add(request)
        self.session.commit()
        return request

    def update_requesting_users(self, request, new_requesting_users):
        """
        Updates the requesting users for a given request.

        :param request: The Request object to update.
        :type request: Request

        :param new_requesting_users: A list of User objects who are requesting or involved in the request.
        :type new_requesting_users: list[User]

        :return: The updated Request object.
        :rtype: Request
        """
        request.set_requesting_users(new_requesting_users)
        self.session.add(request)
        self.session.commit()
        return request

    def update_request_approval(self, request, is_approved):
        """
        Updates the approval status of a given request.

        :param request: The Request object to update.
        :type request: Request

        :param is_approved: The new approval status for the request.
        :type is_approved: bool

        :return: The updated Request object.
        :rtype: Request
        """
        request.set_is_approved(is_approved)
        self.session.add(request)
        self.session.commit()
        return request

    @staticmethod
    def serialize_request(request):
        """
        Converts a Request object into a dictionary for easy serialization.

        :param request: The Request object to serialize.
        :type request: Request

        :return: A dictionary representation of the Request object.
        :rtype: dict
        """
        return {
            'id': request.get_id(),
            'start_date': request.get_start_date(),
            'end_date': request.get_end_date(),
            'registration_date': request.get_registration_date(),
            'is_approved': request.get_is_approved(),
            'author': request.get_author_id(),
            'requesting_users': [user.get_id() for user in request.get_requesting_users()],
            'classroom': request.get_classroom_id()
        }
