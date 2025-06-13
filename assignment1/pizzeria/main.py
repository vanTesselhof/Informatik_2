"""
This is just a simple example of how you can use the Pizzaria class.
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

from pizzeria.customer import Customer
from pizzeria.pizza import Pizza


def main() -> None:
    funghi = Pizza("Funghi", 5, ["tomato", "cheese", "mushrooms"])
    margherita = Pizza("Margherita", 8, ["tomato", "cheese"])
    pepperoni = Pizza("Pepperoni", 12, ["tomato", "cheese", "pepperoni"])
    hawaii = Pizza("Hawaii", 11, ["tomato", "cheese", "pineapple"])
    veggie = Pizza("Veggie", 9, ["tomato", "cheese", "veggies"])

    pizza_menu = [
        (funghi, 10),
        (margherita, 8),
        (pepperoni, 12),
        (hawaii, 11),
        (veggie, 9),
    ]

    customer = Customer(name="Jakob", budget=400, hunger_level=1000)
    customer.pizza_dinner(pizza_menu)

    print(f"{customer.name} has {customer.budget:.2f}€ left and hunger level {customer.hunger_level}")
    print("Pizza pass:", customer.pizza_pass)


if __name__ == "__main__":
    main()
