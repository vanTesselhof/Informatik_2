################################################################################
# Author:      Jakob Marktl
# MatNr:       12335939
# File:        movie.py
# Description: File dataclass user and class movie
# Comments:    ... comments for the tutors ...
#              ... can be multiline ...
################################################################################

from dataclasses import dataclass

from cinema.errors import NotEnoughSeatsAvailableError


@dataclass(frozen=True)
class User:
    username: str
    password: str


class Movie:
    def __init__(self, title: str, duration: float, datetime: str, available_seats: int):
        self.title = title
        self.duration = duration
        self._datetime = datetime
        self._available_seats = available_seats
        self._reserved_seats = 0

    # Getters

    @property
    def available_seats(self) -> int:
        return self._available_seats

    @property
    def datetime(self) -> str:
        return self._datetime

    @property
    def reserved_seats(self) -> int:
        return self._reserved_seats

    # Methods

    def __repr__(self) -> str:
        return f"""Title: {self.title}
Duration: {self.duration:.2f} hours
Time: {self.datetime}"""

    def reserve_seats(self, amount: int) -> None:
        if amount > self.available_seats:
            raise NotEnoughSeatsAvailableError(
                f"There are not enough seats available. Available seats: {self.available_seats}"
            )
        self._available_seats = self._available_seats - amount
        self._reserved_seats = self._reserved_seats + amount
