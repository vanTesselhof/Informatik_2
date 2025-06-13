from collections.abc import Sequence

from pizzeria.errors import CanNotEatPizzaError
from pizzeria.pizza import Pizza


class Customer:
    def __init__(self, name: str, budget: float, hunger_level: int):
        self.name = name
        self.budget = budget
        self._hunger_level = hunger_level
        self.pizza_pass: list[str] = []

    @property
    def hunger_level(self) -> int:
        return self._hunger_level

    @hunger_level.setter
    def hunger_level(self, new_level: int) -> None:
        if new_level < 0:
            raise CanNotEatPizzaError(f"{self.name} cannot have negative hunger!")
        self._hunger_level = new_level

    def eat(self, pizza: Pizza) -> None:
        self.hunger_level = self.hunger_level - pizza.nutrition_value

    def order(self, pizza: Pizza, price: float) -> None:
        if len(self.pizza_pass) == 4:
            self.pizza_pass.append(pizza.name)
            self.pizza_pass = []
            return  # Free pizza

        if self.budget >= price:
            self.budget -= price
            self.pizza_pass.append(pizza.name)
        else:
            raise ValueError(f"{self.name} cannot afford the pizza costing {price:.2f} €")

    def pizza_dinner(self, pizza_menu: Sequence[tuple[Pizza, int | float]]) -> None:
        for pizza, price in pizza_menu:
            if self.hunger_level <= 0 or pizza.nutrition_value > self.hunger_level:
                print(f"{self.name} is completely full and can not finish {pizza.name}: {pizza.diameter} cm anymore!")
                break

            try:
                is_free = len(self.pizza_pass) == 4
                actual_price = 0.00 if is_free else price

                self.order(pizza, actual_price)
                self.eat(pizza)

                print(
                    f"{self.name} ate {pizza.name}: {pizza.diameter} cm -> {self.budget:.2f}€ and {self.hunger_level} hunger left!"
                )

            except ValueError:
                print(f"{self.name} does not have enough budget to order a {pizza.name}: {pizza.diameter} cm!")
                break
            except CanNotEatPizzaError:
                print(f"{self.name} is completely full and can not finish {pizza.name}: {pizza.diameter} cm anymore!")
                break
