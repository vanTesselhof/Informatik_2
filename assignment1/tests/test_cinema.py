################################################################################
# Author:      Info2 Tutors
# MatNr:       -
# File:        test_cinema.py
# Description: This is the testing file for the Cinema task.
# Comments:    You can modify this file during development, but make sure
#              to test with the orignial file in the end.
################################################################################

import sys
from pathlib import Path

import pytest

TEST_DATA_DIR = Path(__file__).parent / "TEST_DATA"

try:
    from cinema import MovieNotAvailableError
except ImportError:
    pass

try:
    from cinema import NotEnoughSeatsAvailableError
except ImportError:
    pass

try:
    from cinema import AccountError
except ImportError:
    pass

try:
    from cinema import MovieAlreadyExistsError
except ImportError:
    pass

try:
    from cinema import User
except ImportError:
    pass

try:
    from cinema import Movie
except ImportError:
    pass

try:
    from cinema import ReservationSystem
except ImportError:
    pass

try:
    from cinema import CLI
except ImportError:
    pass


def skip_if_not_implemented_oop(
    assignment_name: str, class_name: str, function_or_property_name: str | None = None
) -> pytest.mark.skipif:
    try:
        exec(f"from {assignment_name} import {class_name}")

        if function_or_property_name is not None:
            try:
                has_function_or_property = hasattr(eval(class_name), function_or_property_name)
            except AttributeError:
                has_function_or_property = False
            if not has_function_or_property:
                return pytest.mark.skipif(
                    condition=True, reason=f'"""Function {function_or_property_name} not defined"""'
                )
    except ImportError:
        return pytest.mark.skipif(condition=True, reason=f'"""Class {class_name} not implemented"""')

    return pytest.mark.skipif(condition=False, reason="")


try:

    @pytest.fixture()
    def simple_reservation_system() -> ReservationSystem:
        admin = User("admin_user", "admin123")
        return ReservationSystem("Cinema", admin)

except ImportError:
    pass
except NameError:
    pass


try:

    @pytest.fixture()
    def reservation_system() -> ReservationSystem:
        admin = User("admin_user", "admin123")
        reservation_system = ReservationSystem("Cinema", admin)
        reservation_system.add_movie("admin_user", "The Dark Knight", 3.0, "2021-10-12 20:00", 100)
        reservation_system.add_movie("admin_user", "Inception", 2.8, "2021-10-11 20:00", 150)
        reservation_system.add_movie("admin_user", "The Matrix", 2.5, "2021-10-10 20:00", 100)
        reservation_system.add_movie("admin_user", "Interstellar", 3.2, "2021-10-13 20:00", 200)
        return reservation_system

except ImportError:
    pass
except NameError:
    pass


try:

    @pytest.fixture()
    def advanced_reservation_system() -> ReservationSystem:
        admin = User("admin", "admin")
        advanced_reservation_system = ReservationSystem("Cinema", admin)
        advanced_reservation_system.add_user("user_account", "***")
        advanced_reservation_system.add_movie("admin", "The Dark Knight", 3.0, "2021-10-12 20:00", 100)
        advanced_reservation_system.add_movie("admin", "Inception", 2.8, "2021-10-11 20:00", 150)
        advanced_reservation_system.add_movie("admin", "The Matrix", 2.5, "2021-10-10 20:00", 100)
        advanced_reservation_system.add_movie("admin", "Interstellar", 3.2, "2021-10-13 20:00", 200)
        return advanced_reservation_system

except ImportError:
    pass
except NameError:
    pass


@skip_if_not_implemented_oop("cinema", "User")
def test_cinema_01_check_user() -> None:
    user = User("Peter", "mysupersecurepassword")
    assert user.username == "Peter"
    assert user.password == "mysupersecurepassword"


@skip_if_not_implemented_oop("cinema", "Movie")
@skip_if_not_implemented_oop("cinema", "Movie", "__repr__")
def test_cinema_02_movie_repr() -> None:
    movie = Movie("The Matrix", 2.5, "2021-10-10 20:00", 100)
    assert repr(movie) == "Title: The Matrix\nDuration: 2.50 hours\nTime: 2021-10-10 20:00"


@skip_if_not_implemented_oop("cinema", "Movie")
@skip_if_not_implemented_oop("cinema", "Movie", "reserve_seats")
def test_cinema_03_movie_reserve_seats() -> None:
    movie = Movie("Inception", 2.8, "2021-10-11 20:00", 150)
    movie.reserve_seats(10)
    assert movie.available_seats == 140
    assert movie.reserved_seats == 10


@skip_if_not_implemented_oop("cinema", "ReservationSystem")
def test_cinema_05_reservation_system_init() -> None:
    admin = User("admin", "admin")
    reservation_system = ReservationSystem("Cinema", admin)
    assert reservation_system.name == "Cinema"


@skip_if_not_implemented_oop("cinema", "ReservationSystem")
@skip_if_not_implemented_oop("cinema", "ReservationSystem", "get_available_movies")
@skip_if_not_implemented_oop("cinema", "ReservationSystem", "add_movie")
def test_cinema_06_add_movie_and_get_available_movies(simple_reservation_system) -> None:
    assert len(simple_reservation_system.get_available_movies()) == 0
    simple_reservation_system.add_movie("admin_user", "The Dark Knight", 3.0, "2021-10-12 20:00", 100)
    assert len(simple_reservation_system.get_available_movies()) == 1
    assert simple_reservation_system.get_available_movies()[0].title == "The Dark Knight"


@skip_if_not_implemented_oop("cinema", "ReservationSystem")
@skip_if_not_implemented_oop("cinema", "ReservationSystem", "add_movie")
def test_cinema_07_add_movie_account_fail(simple_reservation_system) -> None:
    with pytest.raises(AccountError, match="You do not have the permission to add a movie!"):
        simple_reservation_system.add_movie("user", "The Dark Knight", 3.0, "2021-10-12 20:00", 100)


@skip_if_not_implemented_oop("cinema", "ReservationSystem")
@skip_if_not_implemented_oop("cinema", "ReservationSystem", "add_movie")
def test_cinema_08_add_movie_movie_fail(reservation_system) -> None:
    with pytest.raises(MovieAlreadyExistsError):
        reservation_system.add_movie("admin_user", "The Dark Knight", 3.0, "2021-10-12 20:00", 100)


@skip_if_not_implemented_oop("cinema", "ReservationSystem")
@skip_if_not_implemented_oop("cinema", "ReservationSystem", "add_user")
@skip_if_not_implemented_oop("cinema", "ReservationSystem", "login_user")
def test_cinema_09_add_user_and_login(simple_reservation_system) -> None:
    simple_reservation_system.add_user("Tarek", "123456")
    simple_reservation_system.login_user("Tarek", "123456")


@skip_if_not_implemented_oop("cinema", "ReservationSystem")
@skip_if_not_implemented_oop("cinema", "ReservationSystem", "login_user")
def test_cinema_11_login_with_wrong_username(reservation_system) -> None:
    with pytest.raises(AccountError, match="Invalid Username or Password"):
        reservation_system.login_user("admin", "admin")


@skip_if_not_implemented_oop("cinema", "ReservationSystem")
@skip_if_not_implemented_oop("cinema", "ReservationSystem", "add_user")
def test_cinema_12_add_user_with_existing_user(reservation_system) -> None:
    with pytest.raises(AccountError, match="A User with this name already exists"):
        reservation_system.add_user("admin_user", "hello")


@skip_if_not_implemented_oop("cinema", "ReservationSystem")
@skip_if_not_implemented_oop("cinema", "ReservationSystem", "get_available_movies")
def test_cinema_13_get_available_movies_empty(simple_reservation_system) -> None:
    assert len(simple_reservation_system.get_available_movies()) == 0


@skip_if_not_implemented_oop("cinema", "ReservationSystem")
@skip_if_not_implemented_oop("cinema", "ReservationSystem", "__repr__")
@skip_if_not_implemented_oop("cinema", "ReservationSystem", "get_available_movies")
def test_cinema_14_get_available_movies(reservation_system) -> None:
    available_movies = reservation_system.get_available_movies()
    assert len(available_movies) == 4

    expected_available_movies = [
        Movie("The Dark Knight", 3.0, "2021-10-12 20:00", 100),
        Movie("Inception", 2.8, "2021-10-11 20:00", 150),
        Movie("The Matrix", 2.5, "2021-10-10 20:00", 100),
        Movie("Interstellar", 3.2, "2021-10-13 20:00", 200),
    ]

    for i, movie in enumerate(available_movies):
        available_movies[i] = repr(movie)
    available_movies = sorted(available_movies)
    for i, movie in enumerate(expected_available_movies):
        expected_available_movies[i] = repr(movie)
    expected_available_movies = sorted(expected_available_movies)

    assert available_movies == expected_available_movies


@skip_if_not_implemented_oop("cinema", "ReservationSystem")
@skip_if_not_implemented_oop("cinema", "ReservationSystem", "get_reservations")
def test_cinema_16_get_reservation_empty(reservation_system) -> None:
    assert reservation_system.get_reservations(User("admin", "admin")) == []


@skip_if_not_implemented_oop("cinema", "ReservationSystem")
@skip_if_not_implemented_oop("cinema", "ReservationSystem", "make_reservation")
def test_cinema_17_make_reservation_movie_fails(reservation_system) -> None:
    with pytest.raises(MovieNotAvailableError):
        reservation_system.make_reservation(User("admin", "admin"), "Barbie", 10)


@skip_if_not_implemented_oop("cinema", "ReservationSystem")
@skip_if_not_implemented_oop("cinema", "ReservationSystem", "make_reservation")
def test_cinema_18_make_reservation_seats_fails(reservation_system) -> None:
    reservation_system.make_reservation(User("admin", "admin"), "The Dark Knight", 10)
    reservation_system.make_reservation(User("admin", "admin"), "The Dark Knight", 20)
    reservation_system.make_reservation(User("admin", "admin"), "The Dark Knight", 25)
    with pytest.raises(NotEnoughSeatsAvailableError):
        reservation_system.make_reservation(User("admin", "admin"), "The Dark Knight", 50)


@skip_if_not_implemented_oop("cinema", "CLI")
@skip_if_not_implemented_oop("cinema", "CLI", "login")
def test_cinema_20_cli_login_fails(advanced_reservation_system, capsys) -> None:
    cli = CLI(advanced_reservation_system)
    path = Path(TEST_DATA_DIR / "preprogrammed_inputs_20.txt")
    with path.open() as sys.stdin:
        cli.login()
        your_output = capsys.readouterr().out
        expected_output = "Invalid Username or Password\n"
        assert your_output.endswith(expected_output)


@skip_if_not_implemented_oop("cinema", "CLI")
@skip_if_not_implemented_oop("cinema", "CLI", "create_account")
@skip_if_not_implemented_oop("cinema", "CLI", "login")
def test_cinema_21_cli_create_account_and_login(advanced_reservation_system, capsys) -> None:
    cli = CLI(advanced_reservation_system)
    path = Path(TEST_DATA_DIR / "preprogrammed_inputs_21.txt")
    with path.open() as sys.stdin:
        cli.create_account()
        your_output = capsys.readouterr().out
        expected_output = "Account created successfully!\n"
        assert your_output.endswith(expected_output)

        return_value = cli.login()
        your_output = capsys.readouterr().out
        expected_output = "Hello Peter :D\n"
        assert return_value is True
        assert your_output.endswith(expected_output)


@skip_if_not_implemented_oop("cinema", "CLI")
@skip_if_not_implemented_oop("cinema", "CLI", "reservation_process")
def test_cinema_22_cli_reservation_process_go_back(advanced_reservation_system, capsys) -> None:
    cli = CLI(advanced_reservation_system)
    path = Path(TEST_DATA_DIR / "preprogrammed_inputs_22.txt")
    with path.open() as sys.stdin:
        return_value = cli.reservation_process()
        your_output = capsys.readouterr().out
        expected_output = (
            "What movie do you want to watch?\n"
            "----------------------------------------\n"
            "0. Go Back\n"
            "1. Inception\n"
            "2. Interstellar\n"
            "3. The Dark Knight\n"
            "4. The Matrix\n"
            "----------------------------------------\n"
            "Enter your choice: "
        )
        assert return_value is None
        assert your_output == expected_output


@skip_if_not_implemented_oop("cinema", "CLI")
@skip_if_not_implemented_oop("cinema", "CLI", "login")
@skip_if_not_implemented_oop("cinema", "CLI", "reservation_process")
def test_cinema_24_cli_reservation_process_fails(advanced_reservation_system, capsys) -> None:
    cli = CLI(advanced_reservation_system)
    path = Path(TEST_DATA_DIR / "preprogrammed_inputs_24.txt")
    with path.open() as sys.stdin:
        cli.login()
        return_value = cli.reservation_process()
        your_output = capsys.readouterr().out
        expected_output = (
            "Enter your user-name: Enter your password: Hello admin :D\n"
            "What movie do you want to watch?\n"
            "----------------------------------------\n"
            "0. Go Back\n"
            "1. Inception\n"
            "2. Interstellar\n"
            "3. The Dark Knight\n"
            "4. The Matrix\n"
            "----------------------------------------\n"
            "Enter your choice: Enter the amount of seats: There are not enough seats available.\n"
        )
        assert return_value is None
        assert your_output == expected_output


@skip_if_not_implemented_oop("cinema", "CLI")
@skip_if_not_implemented_oop("cinema", "CLI", "login")
@skip_if_not_implemented_oop("cinema", "CLI", "show_reservations")
def test_cinema_25_show_reservations_empty(advanced_reservation_system, capsys) -> None:
    cli = CLI(advanced_reservation_system)
    path = Path(TEST_DATA_DIR / "preprogrammed_inputs_25.txt")
    with path.open() as sys.stdin:
        cli.login()
        return_value = cli.show_reservations()
        your_output = capsys.readouterr().out
        expected_output = (
            "Enter your user-name: Enter your password: Hello admin :D\nYou do not have any reservations yet.\n"
        )
        assert return_value is None
        assert your_output == expected_output


@skip_if_not_implemented_oop("cinema", "CLI")
@skip_if_not_implemented_oop("cinema", "CLI", "login")
@skip_if_not_implemented_oop("cinema", "CLI", "reservation_process")
@skip_if_not_implemented_oop("cinema", "CLI", "show_reservations")
def test_cinema_26_show_reservations(advanced_reservation_system, capsys) -> None:
    cli = CLI(advanced_reservation_system)
    path = Path(TEST_DATA_DIR / "preprogrammed_inputs_26.txt")
    with path.open() as sys.stdin:
        cli.login()
        cli.reservation_process()
        cli.reservation_process()
        cli.reservation_process()
        return_value = cli.show_reservations()
        your_output = capsys.readouterr().out
        expected_output = (
            "Enter your user-name: Enter your password: Hello admin :D\n"
            "What movie do you want to watch?\n"
            "----------------------------------------\n"
            "0. Go Back\n"
            "1. Inception\n"
            "2. Interstellar\n"
            "3. The Dark Knight\n"
            "4. The Matrix\n"
            "----------------------------------------\n"
            "Enter your choice: Enter the amount of seats: Reservation for The Dark Knight successful.\n"
            "What movie do you want to watch?\n"
            "----------------------------------------\n"
            "0. Go Back\n"
            "1. Inception\n"
            "2. Interstellar\n"
            "3. The Dark Knight\n"
            "4. The Matrix\n"
            "----------------------------------------\n"
            "Enter your choice: Enter the amount of seats: Reservation for Inception successful.\n"
            "What movie do you want to watch?\n"
            "----------------------------------------\n"
            "0. Go Back\n"
            "1. Inception\n"
            "2. Interstellar\n"
            "3. The Dark Knight\n"
            "4. The Matrix\n"
            "----------------------------------------\n"
            "Enter your choice: Enter the amount of seats: Reservation for The Dark Knight successful.\n"
            "You have reservations for:\n"
            "----------------------------------------\n"
            "1. Inception (Amount of seats: 4)\n"
            "2. The Dark Knight (Amount of seats: 38)\n"
            "----------------------------------------\n"
        )
        assert return_value is None
        assert your_output == expected_output


@skip_if_not_implemented_oop("cinema", "CLI")
@skip_if_not_implemented_oop("cinema", "CLI", "show_available_movies")
def test_cinema_28_show_available_movies_empty(simple_reservation_system, capsys) -> None:
    cli = CLI(simple_reservation_system)
    cli.show_available_movies()
    your_output = capsys.readouterr().out
    expected_output = "Currently this cinema does not show any movies :(\n"
    assert your_output == expected_output


@skip_if_not_implemented_oop("cinema", "CLI")
@skip_if_not_implemented_oop("cinema", "CLI", "run")
def test_cinema_30_run_advanced_test(advanced_reservation_system, capsys) -> None:
    cli = CLI(advanced_reservation_system)
    path_output = Path(TEST_DATA_DIR / "expected_output_30.txt")
    with path_output.open() as output_file_content:
        expected_output = output_file_content.read()
    path_input = Path(TEST_DATA_DIR / "preprogrammed_inputs_30.txt")
    with path_input.open() as sys.stdin:
        return_value = cli.run()
        your_output = capsys.readouterr().out
        assert return_value is None
        assert your_output == expected_output
