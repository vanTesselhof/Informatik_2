################################################################################
# Author:      Jakob Marktl
# MatNr:       12335939
# File:        reservationSystem.py
# Description: File for the Reservationsystem class
# Comments:    ... comments for the tutors ...
#              ... can be multiline ...
################################################################################


from cinema.errors import (
    AccountError,
    MovieAlreadyExistsError,
    MovieNotAvailableError,
    NotEnoughSeatsAvailableError,
)
from cinema.movie import Movie, User


class ReservationSystem:
    def __init__(self, cinema_name: str, admin_account: User):
        # name of the cinema
        self._name: str = cinema_name

        self._movies: dict[str, Movie] = {}

        self._reservations: dict[User, dict[Movie, int]] = {}
        self._users = {}

        # the admin User
        self._admin: User = admin_account
        self._users[admin_account.username] = admin_account

    # Getter
    @property
    def name(self) -> str:
        """Name of the cinema (read-only)."""
        return self._name

    # Methods
    def add_movie(self, user: str, movie_name: str, duration: float, datetime: str, available_seats: int) -> None:
        if self._admin.username != user:
            raise AccountError("You do not have the permission to add a movie!")
        if movie_name in self._movies:
            raise MovieAlreadyExistsError
        new_movie = Movie(movie_name, duration, datetime, available_seats)
        self._movies[movie_name] = new_movie

    def add_user(self, username: str, password: str) -> None:
        if username in self._users:
            raise AccountError("A User with this name already exists")
        new_user = User(username, password)
        self._users[username] = new_user

    def make_reservation(self, user: User, movie_title: str, seats: int) -> None:
        if user is None:
            raise AccountError("You need to be logged in to make a reservation")
        if movie_title not in self._movies:
            raise MovieNotAvailableError("Movie not available")
        if seats > self._movies[movie_title].available_seats:
            raise NotEnoughSeatsAvailableError("Not enough seats available")
        self._movies[movie_title].reserve_seats(seats)

        if user not in self._reservations:
            self._reservations[user] = {}

        user_reservations = self._reservations[user]

        movie_obj = self._movies[movie_title]
        if movie_obj in user_reservations:
            user_reservations[movie_obj] += seats
        else:
            user_reservations[movie_obj] = seats

    def get_reservations(self, user: User) -> list[tuple[Movie, int]]:
        if user is None:
            raise AccountError("You need to be logged in to make a reservation")
        reservations_for_user = self._reservations.get(user)
        if not reservations_for_user:
            return []

        # turn the mapping Movie -> seats into a list of tuples
        return list(reservations_for_user.items())

    def get_available_movies(self) -> list[Movie]:
        available: list[Movie] = []
        for movie in self._movies.values():
            if movie.available_seats >= 1:
                available.append(movie)
        return available

    def login_user(self, username: str, password: str) -> User:
        if username not in self._users:
            raise AccountError("Invalid Username or Password")
        if password != self._users[username].password:
            raise AccountError("Invalid Username or Password")
        return self._users[username]
