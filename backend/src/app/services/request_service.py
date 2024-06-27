from ..repositories import ClassroomRepository, RequestRepository, UserRepository


class RequestService:
    """
    The RequestService class offers a high-level interface for managing and interacting with Request-related data and
    operations. It serves as a bridge between the application logic and the database operations conducted by the
    repositories, ensuring a separation of concerns and more manageable code.

    This service encapsulates the logic necessary for performing typical tasks related to requests, such as creating,
    updating, and retrieving request information. It simplifies the complexities involved in direct database
    interactions and provides a streamlined set of methods for the application to use.

    RequestRepository - Manages interactions with the Request data model, handling the creation, retrieval,
    and updating of request records.

    ClassroomRepository - Provides access to classroom-related data and operations, crucial for handling requests
    related to classroom bookings or allocations.

    UserRepository - Used for accessing and modifying user information, as requests typically involve users either as
    authors or participants.
    """

    def __init__(self):
        """
        Initializes the RequestService with instances of RequestRepository, ClassroomRepository, and UserRepository.
        This setup allows the service to perform comprehensive operations related to requests, involving not just the
        requests themselves but also the associated classrooms and users.
        """
        self.classroom_repository = ClassroomRepository()
        self.request_repository = RequestRepository()
        self.user_repository = UserRepository()

    def approve_reservation_request(self, request_id, manager_id):
        """
        Confirms a reservation request, setting its approval status to True.

        :param request_id: The ID of the request to be confirmed.
        :type request_id: int

        :param manager_id: The ID of the manager confirming the reservation.
        :type manager_id: int

        :return: The updated Request object with the approval status set to True.
        :rtype: Request

        :raises ValueError: If no manager or request with the given IDs is found,
                            or if the manager does not have the authority to confirm the request.
        """
        request_to_approve = self.request_repository.get_request_by_id(request_id)
        if not request_to_approve:
            raise ValueError(f"No request found with ID: {request_id}")

        manager = self.user_repository.get_user_by_id(manager_id)
        if not manager:
            raise ValueError(f"No manager found with ID: {manager_id}")

        self.request_repository.update_request_approval(request_to_approve, True)

        return self.request_repository.serialize_request(request_to_approve)

    def create_reservation_request(self, start_date, end_date, author_id, classroom_id, requesting_user_logins):
        """
        Creates a reservation request for a classroom.

        :param start_date: The start date and time for the reservation.
        :type start_date: datetime

        :param end_date: The end date and time for the reservation.
        :type end_date: datetime

        :param author_id: The ID of the user who is making the reservation.
        :type author_id: int

        :param classroom_id: The ID of the classroom to reserve.
        :type classroom_id: int

        :param requesting_user_logins: List of user logins who are requesting or involved in the reservation.
        :type requesting_user_logins: list[str]

        :return: The newly created Request object.
        :rtype: Request
        """
        if not self.request_repository.validate_dates(start_date, end_date):
            raise ValueError("Invalid dates. The end date must be after the start date.")

        author = self.user_repository.get_user_by_id(author_id)
        if not author:
            raise ValueError(f"No user found with author ID: {author_id}")

        classroom = self.classroom_repository.get_classroom_by_id(classroom_id)
        if not classroom:
            raise ValueError(f"No classroom found with ID: {classroom_id}")

        requesting_users = []
        for login in requesting_user_logins:
            user = self.user_repository.get_user_by_login(login)
            if not user:
                raise ValueError(f"No user found with login: {login}")
            requesting_users.append(user)

        new_request = self.request_repository.create_request(start_date, end_date)
        self.request_repository.update_request_author(new_request, author)
        self.request_repository.update_request_classroom(new_request, classroom)
        self.request_repository.update_requesting_users(new_request, requesting_users)

        return self.request_repository.serialize_request(new_request)

    def update_reservation_request(self, request_id, new_author_id=None, new_classroom_id=None,
                                   new_requesting_user_logins=None):
        """
        Updates the specified reservation request with new details.

        :param request_id: The ID of the request to be updated.
        :type request_id: int

        :param new_author_id: (Optional) The ID of the new author for the request.
        :type new_author_id: int or None

        :param new_classroom_id: (Optional) The ID of the new classroom for the request.
        :type new_classroom_id: int or None

        :param new_requesting_user_logins: (Optional) List of user logins who are newly requesting or involved
                                           in the reservation.
        :type new_requesting_user_logins: list[str] or None

        :return: The updated Request object.
        :rtype: Request

        :raises ValueError: If the specified request, new author, or new classroom doesn't exist.
        """
        request = self.request_repository.get_request_by_id(request_id)
        if not request:
            raise ValueError(f"No request found with ID: {request_id}")

        if new_author_id:
            new_author = self.user_repository.get_user_by_id(new_author_id)
            if not new_author:
                raise ValueError(f"No user found with ID: {new_author_id}")
            self.request_repository.update_request_author(request, new_author)

        if new_classroom_id:
            new_classroom = self.classroom_repository.get_classroom_by_id(new_classroom_id)
            if not new_classroom:
                raise ValueError(f"No classroom found with ID: {new_classroom_id}")
            self.request_repository.update_request_classroom(request, new_classroom)

        if new_requesting_user_logins:
            new_requesting_users = []
            for login in new_requesting_user_logins:
                user = self.user_repository.get_user_by_login(login)
                if not user:
                    raise ValueError(f"No user found with login: {login}")
                new_requesting_users.append(user)
            self.request_repository.update_requesting_users(request, new_requesting_users)

        return self.request_repository.serialize_request(request)

    def find_request(self, request_id):
        """
        Retrieves a request by its ID.

        :param request_id: The ID of the request to retrieve.
        :type request_id: int

        :return: The Request object with the specified ID.
        :rtype: Request

        :raises ValueError: If no request is found with the provided ID, indicating that the request does not exist
                            or the ID is incorrect.
        """
        request = self.request_repository.get_request_by_id(request_id)
        if not request:
            raise ValueError(f"No request found with ID: {request_id}")

        return self.request_repository.serialize_request(request)

    def find_all_requests(self):
        """
        Retrieves all requests from the database.

        :return: A list of all Request objects.
        :rtype: list[Request]

        :raises ValueError: If no requests are found in the database, indicating an empty request list.
        """
        requests = self.request_repository.get_all_requests()
        if not requests:
            raise ValueError("No requests found in the database.")

        return {'requests': [self.request_repository.serialize_request(request) for request in requests]}
