
class pizza:
    def __init__(self, name:str, number: int):
        self._name = name
        self.number = number

    def __str__(self) -> str:
        return f"Name: {name + Number: {number}}"

    @property
    def name(self) -> str:
        return self._name
    
    @name.setter
    def name(self,name:str) -> None:
        self._name = name

    @property
    def id(self) -> str:
        return f"Name: {name + Number: {number}}"

class CanNotEatPizzaError(Exception):
    """Raised when the customer is full and cannot eat more pizza."""

class customer:
    def __init__(self, name:str,budget:float, hunger_level: int):
        self.name = name
        self.budget = budget
        self._name = name
        self.pizza_pass: list[str] = [] 

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self,name:str) -> None:
        self._name = name