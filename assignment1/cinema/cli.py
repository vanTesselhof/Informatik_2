################################################################################
# Author:      Jakob Marktl
# MatNr:       12335939
# File:        cli.py
# Description: File class for the CLI
# Comments:    ... comments for the tutors ...
#              ... can be multiline ...
################################################################################
from cinema.errors import (
    AccountError,
    MovieAlreadyExistsError,
    NotEnoughSeatsAvailableError,
)
from cinema.movie import User
from cinema.reservations_system import ReservationSystem


class CLI:
    def __init__(self, reservation_system: ReservationSystem) -> None:
        self._reservation_system = reservation_system
        self._current_user: User | None

    # Method
    def login_menu(self) -> None:
        print(
            f"Welcome to {self._reservation_system.name}\n"
            f"{'-' * 40}\n"
            "1. Create Account\n"
            "2. Log in to existing Account\n"
            "3. Exit\n"
            f"{'-' * 40}"
        )

    def option_menu(self) -> None:
        options = ["List available movies", "Reserve a seat", "Show reservations", "Add a movie", "Logout"]
        print("What do you want to do?")
        print("-" * 40)
        for nr, option in enumerate(options):
            print(f"{nr + 1}. {option}")
        print("-" * 40)

    def create_account(self) -> None:
        try:
            username = input("Enter user-name: ")
            password = input("Choose a password: ")
            self._reservation_system.add_user(username, password)
        except AccountError as e:
            print(e)
        else:
            print("Account created successfully!")
            # retrieve and set the new user as current
            try:
                self._current_user = self._reservation_system.login_user(username, password)
            except AccountError as e:
                print(e)
                return

    def login(self) -> bool:
        try:
            username = input("Enter your user-name: ")
            password = input("Enter your password: ")
            user = self._reservation_system.login_user(username, password)
        except AccountError as e:
            print(e)
            return False
        else:
            self._current_user = user
            print(f"Hello {username} :D")
            return True

    def show_available_movies(self) -> None:
        if not self._reservation_system.get_available_movies():
            print("Currently this cinema does not show any movies :(")
            return
        sorted_movies = sorted(self._reservation_system.get_available_movies(), key=lambda m: m.title)
        for count, movie in enumerate(sorted_movies, start=1):
            print(f"{count}. {movie.title}")
        print("-" * 40)

    def reservation_process(self) -> None:
        movies = self._reservation_system.get_available_movies()
        if not movies:
            print("Currently no movies available for reservation.")
            return

        print("What movie do you want to watch?")
        print("-" * 40)
        # show numbered list
        print("0. Go Back")
        self.show_available_movies()

        choice = int(input("Enter your choice: "))
        if choice == 0:
            return

        sorted_movies = sorted(movies, key=lambda m: m.title)
        selected = sorted_movies[choice - 1]
        seats = int(input("Enter the amount of seats: "))
        try:
            if self._current_user is not None:
                self._reservation_system.make_reservation(self._current_user, selected.title, seats)
        except NotEnoughSeatsAvailableError:
            print("There are not enough seats available.")
            return
        else:
            print(f"Reservation for {selected.title} successful.")

    def show_reservations(self) -> None:
        try:
            if self._current_user is not None:
                reservations = self._reservation_system.get_reservations(self._current_user)
        except AccountError:
            print("No User logged in")
            return

        if not reservations:
            print("You do not have any reservations yet.")
            return

        sorted_res = sorted(reservations, key=lambda pair: pair[0].title)
        print("You have reservations for:")
        print("-" * 40)
        for idx, (movie, seats) in enumerate(sorted_res, start=1):
            print(f"{idx}. {movie.title} (Amount of seats: {seats})")
        print("-" * 40)

    def add_movie(self) -> None:
        if self._current_user is None:
            print("You need to be logged in to add a movie.")
            return

        title = input("Enter movie-title: ")
        try:
            duration = float(input("Enter movie-duration: "))
        except ValueError:
            print("Invalid duration format.")
            return
        datetime_str = input("Enter movie-datetime: ")
        try:
            seats = int(input("Enter available seats: "))
        except ValueError:
            print("Invalid seats format.")
            return
        try:
            if self._current_user is not None:
                self._reservation_system.add_movie(self._current_user.username, title, duration, datetime_str, seats)
        except AccountError as e:
            print(e)
        except MovieAlreadyExistsError:
            print("This movie already exists!")
        else:
            print(f"{title} added!")

    def run(self) -> None:
        while True:
            # Login Menu
            print("Welcome to Cinema")
            print("-" * 40)
            print("1. Create Account")
            print("2. Log in to existing Account")
            print("3. Exit")
            print("-" * 40)
            choice = input("Enter your choice: ")
            if choice == "1":
                self.create_account()
                continue
            if choice == "2":
                if not self.login():
                    continue
                # Option Menu
                while True:
                    print("What do you want to do?")
                    print("-" * 40)
                    print("1. List available movies")
                    print("2. Reserve a seat")
                    print("3. Show reservations")
                    print("4. Add a movie")
                    print("5. Logout")
                    print("-" * 40)
                    opt = input("Enter your choice: ")

                    if opt == "1":
                        print("We are offering these movies currently:")
                        print("-" * 40)
                        self.show_available_movies()
                    elif opt == "2":
                        self.reservation_process()
                    elif opt == "3":
                        self.show_reservations()
                    elif opt == "4":
                        self.add_movie()
                    elif opt == "5":
                        print("Bye bye!")
                        self._current_user = None
                        break
                    else:
                        print("Invalid choice. Please try again.")
                continue
            if choice == "3":
                print("Exiting...")
                return
            print("Invalid choice. Please try again.")
            continue
