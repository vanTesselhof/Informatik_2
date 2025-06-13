################################################################################
# Author:      Jakob Marktl
# MatNr:       12335939
# File:        errors.py
# Description: Class for all different kind of Exceptions
# Comments:    ... comments for the tutors ...
#              ... can be multiline ...
################################################################################


class MovieNotAvailableError(Exception):
    """it is raised when a user tries to book a movie that does not exist in the system."""


class NotEnoughSeatsAvailableError(Exception):
    """it is raised when a user tries to book a movie that has not enough available seats."""


class AccountError(Exception):
    """it is raised when there is an issue with user account creation or login."""


class MovieAlreadyExistsError(Exception):
    """it is raised when the admin user tries to add an already existing Movie."""
