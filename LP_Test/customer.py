from pizza import Pizza
from pizza import CanNotEatPizzaError

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
    def hunger_level(self, hunger_level:int) -> None:
        if hunger_level < 0:
            raise CanNotEatPizzaError(f"{self.name} cannot have negative hunger!")
        self._hunger_level = hunger_level

    def eat(self, pizza: Pizza) -> None:
        new_hunger_level = self.hunger_level - pizza.nutrition_value
        self.hunger_level(self,new_hunger_level)

    def order(self, pizza: Pizza, price:float) -> None:
        if len(self.pizza_pass) > 4:
            self.pizza_pass = []
            return
        elif self.budget >= price:
            self.budget -= price
            self.pizza_pass.append(pizza.name)
            return
        else:
            raise ValueError("not possible")

    def pizza_dinner(self, pizza_menu: list[tuple[Pizza,float]]) -> None:
        for pizza,price in pizza_menu:
            if  self.hunger_level < pizza.nutrition_value:
                raise CanNotEatPizzaError(f"{self.name} is completely full and can not finish {pizza.name} anymore!")
                break
            try:
                self.order(pizza,price)
                self.eat(pizza)
                print(f"{self.name} ate {pizza.name} -> {self.budget}€ and {self.hunger_level} hunger left!")
            except ValueError:
                print(f"{self.name} does not have enough budget to order a {pizza.name}")
                break
            except CanNotEatPizzaError:
                print(f"{self.name} is completely full and can not finish {pizza.name} anymore!")