class Pizza:
    def __init__(self, name: str, size: int, toppings: list[str]):
        self.name = name
        self.size = size
        self.toppings = toppings

    @property
    def nutrition_value(self) -> int:
        return round(2 * len(self.toppings) + 4 * self.size)

    def __str__(self) -> str:
        return f"{self.name}: {self.size} cm"

class CanNotEatPizzaError(Exception):
    """Raises when Pizaa cannot be eaten"""

