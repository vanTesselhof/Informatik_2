"""
This is just a simple example of how you can use the Cinema class.
A main.py file is always nice to test your code and see if everything works as expected.
This can be used for quick tests when you do not want to use the test cases for now.

The imports can look different. Again, this is just an example.
The structure and the name of the modules can be different.

Make sure that you always use "from <main module>.<module> import <class>", where the main module is either
cinema or pizzaria in all your imports.
The lines 14 to 17 are only needed in this main.py file.
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from cinema.cli import CLI
from cinema.movie import User
from cinema.reservations_system import ReservationSystem


def main() -> None:
    admin = User("admin", "admin")
    advanced_reservation_system = ReservationSystem("Cinema", admin)
    advanced_reservation_system.add_user("user_account", "***")
    advanced_reservation_system.add_movie("admin", "The Dark Knight", 3.0, "2021-10-12 20:00", 100)
    advanced_reservation_system.add_movie("admin", "Inception", 2.8, "2021-10-11 20:00", 150)
    advanced_reservation_system.add_movie("admin", "The Matrix", 2.5, "2021-10-10 20:00", 100)
    advanced_reservation_system.add_movie("admin", "Interstellar", 3.2, "2021-10-13 20:00", 200)
    cli = CLI(advanced_reservation_system)

    cli.run()


if __name__ == "__main__":
    main()
