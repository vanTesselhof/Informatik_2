    ################################################################################
# Author:      Jakob Marktl
# MatNr:       12335939
# File:        pizza.py
# Description: Pizza class
# Comments:    ... comments for the tutors ...
#              ... can be multiline ...
################################################################################


class Pizza:
    def __init__(self, name: str, diameter: int, ingredients: list[str]):
        self.name = name
        self.diameter = diameter
        self.ingredients = ingredients

    def __str__(self) -> str:
        return f"{self.name}: {self.diameter} cm"

    @property
    def nutrition_value(self) -> int:
        return round(2 * len(self.ingredients) + 4 * self.diameter)
