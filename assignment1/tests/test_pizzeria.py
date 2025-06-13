################################################################################
# Author:      Info2 Tutors
# MatNr:       -
# File:        test_pizzeria.py
# Description: This is the testing file for the Pizzeria task.
# Comments:    You can modify this file during development, but make sure
#              to test with the orignial file in the end.
################################################################################

import pytest

try:
    from pizzeria import Pizza
except ImportError:
    pass

try:
    from pizzeria import CanNotEatPizzaError
except ImportError:
    pass

try:
    from pizzeria import Customer
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


@skip_if_not_implemented_oop("pizzeria", "Pizza")
@skip_if_not_implemented_oop("pizzeria", "Pizza", "__str__")
def test_01_check_str() -> None:
    test_pizza = Pizza("Funghi", 23, ["Tomato", "Mozzarella", "Basil", "Mushrooms"])
    assert str(test_pizza) == "Funghi: 23 cm"


@skip_if_not_implemented_oop("pizzeria", "Pizza")
@skip_if_not_implemented_oop("pizzeria", "Pizza", "nutrition_value")
def test_03_nutrition_value() -> None:
    test_pizza = Pizza("Funghi", 23, ["Tomato", "Mozzarella", "Basil", "Mushrooms"])
    assert test_pizza.nutrition_value == 100


@skip_if_not_implemented_oop("pizzeria", "Customer")
def test_05_customer_init() -> None:
    test_customer = Customer("Peter", 15, 100)
    assert test_customer.name == "Peter"
    assert test_customer.budget == 15
    assert test_customer.pizza_pass == []


@skip_if_not_implemented_oop("pizzeria", "Customer")
def test_06_hunger_level_getter() -> None:
    test_customer = Customer("Peter", 15, 100)
    assert test_customer.hunger_level == 100


@skip_if_not_implemented_oop("pizzeria", "Customer")
def test_08_hunger_level_setter() -> None:
    test_customer = Customer("Peter", 15, 100)
    with pytest.raises(CanNotEatPizzaError):
        test_customer.hunger_level = -10


@skip_if_not_implemented_oop("pizzeria", "Pizza")
@skip_if_not_implemented_oop("pizzeria", "Customer")
@skip_if_not_implemented_oop("pizzeria", "Customer", "eat")
def test_10_eat_normally() -> None:
    test_pizza = Pizza("Margherita", 15, ["Tomato", "Mozzarella", "Basil"])
    test_customer = Customer("Peter", 15, 100)
    test_customer.eat(test_pizza)
    assert test_customer.hunger_level == 34


@skip_if_not_implemented_oop("pizzeria", "Pizza")
@skip_if_not_implemented_oop("pizzeria", "Customer")
@skip_if_not_implemented_oop("pizzeria", "Customer", "eat")
def test_12_eat_too_much() -> None:
    test_pizza = Pizza("Margherita", 15, ["Tomato", "Mozzarella", "Basil"])
    test_customer = Customer("Peter", 15, 10)
    with pytest.raises(CanNotEatPizzaError):
        test_customer.eat(test_pizza)


@skip_if_not_implemented_oop("pizzeria", "Pizza")
@skip_if_not_implemented_oop("pizzeria", "Customer")
@skip_if_not_implemented_oop("pizzeria", "Customer", "order")
def test_14_order() -> None:
    test_pizza = Pizza("Margherita", 15, ["Tomato", "Mozzarella", "Basil"])
    test_customer = Customer("Peter", 15, 100)
    test_customer.order(test_pizza, 10)
    assert test_customer.budget == 5
    assert test_customer.pizza_pass == ["Margherita"]
    assert test_customer.hunger_level == 100


@skip_if_not_implemented_oop("pizzeria", "Pizza")
@skip_if_not_implemented_oop("pizzeria", "Customer")
@skip_if_not_implemented_oop("pizzeria", "Customer", "order")
def test_16_order_no_money() -> None:
    test_pizza = Pizza("Margherita", 15, ["Tomato", "Mozzarella", "Basil"])
    test_customer = Customer("Peter", 5, 100)
    with pytest.raises(ValueError):
        test_customer.order(test_pizza, 10)


@skip_if_not_implemented_oop("pizzeria", "Pizza")
@skip_if_not_implemented_oop("pizzeria", "Customer")
@skip_if_not_implemented_oop("pizzeria", "Customer", "pizza_dinner")
def test_18_pizza_dinner(capsys) -> None:
    test_menu = [
        (Pizza("Capricciosa", 30, ["Tomato", "Mozzarella", "Ham", "Mushrooms"]), 12),
        (Pizza("Margherita", 15, ["Tomato", "Mozzarella", "Basil"]), 5),
        (Pizza("Salami", 36, ["Tomato", "Mozzarella", "Salami", "Extra Cheese", "Olives"]), 15),
        (Pizza("Funghi", 23, ["Tomato", "Mozzarella", "Basil", "Mushrooms"]), 10),
        (Pizza("Hawaii", 30, ["Tomato", "Mozzarella", "Pineapple", "Ham"]), 12),
        (Pizza("Pepperoni", 30, ["Tomato", "Mozzarella", "Pepperoni"]), 12),
    ]
    test_customer = Customer("Peter", 70, 800)
    test_customer.pizza_dinner(test_menu)
    # we don't care about the output here, but otherwise the output will be shown in the pytest output
    _ = capsys.readouterr().out
    assert test_customer.budget == 16
    assert test_customer.pizza_pass == ["Pepperoni"]
    assert test_customer.hunger_level == 98


@skip_if_not_implemented_oop("pizzeria", "Pizza")
@skip_if_not_implemented_oop("pizzeria", "Customer")
@skip_if_not_implemented_oop("pizzeria", "Customer", "pizza_dinner")
def test_19_pizza_dinner_no_money(capsys) -> None:
    test_menu = [
        (Pizza("Margherita", 15, ["Tomato", "Mozzarella", "Basil"]), 5),
        (Pizza("Salami", 36, ["Tomato", "Mozzarella", "Salami", "Extra Cheese", "Olives"]), 15),
        (Pizza("Funghi", 23, ["Tomato", "Mozzarella", "Basil", "Mushrooms"]), 10),
        (Pizza("Hawaii", 30, ["Tomato", "Mozzarella", "Pineapple", "Ham"]), 12),
        (Pizza("Pepperoni", 30, ["Tomato", "Mozzarella", "Pepperoni"]), 12),
        (Pizza("Capricciosa", 30, ["Tomato", "Mozzarella", "Ham", "Mushrooms"]), 12),
    ]
    test_customer = Customer("Peter", 42, 800)
    test_customer.order(test_menu[0][0], test_menu[0][1])
    test_customer.order(test_menu[1][0], test_menu[1][1])
    test_customer.pizza_dinner(test_menu)
    your_output = capsys.readouterr().out
    expected_output = "Peter ate Margherita: 15 cm -> 17.00€ and 734 hunger left!\n"
    expected_output += "Peter ate Salami: 36 cm -> 2.00€ and 580 hunger left!\n"
    expected_output += "Peter ate Funghi: 23 cm -> 2.00€ and 480 hunger left!\n"
    expected_output += "Peter does not have enough budget to order a Hawaii: 30 cm!\n"
    assert expected_output == your_output


@skip_if_not_implemented_oop("pizzeria", "Pizza")
@skip_if_not_implemented_oop("pizzeria", "Customer")
@skip_if_not_implemented_oop("pizzeria", "Customer", "pizza_dinner")
def test_20_pizza_dinner_no_hunger(capsys) -> None:
    your_output = capsys.readouterr().out
    test_menu = [
        (Pizza("Pepperoni", 30, ["Tomato", "Mozzarella", "Pepperoni"]), 12),
        (Pizza("Margherita", 15, ["Tomato", "Mozzarella", "Basil"]), 5),
        (Pizza("Salami", 36, ["Tomato", "Mozzarella", "Salami", "Extra Cheese", "Olives"]), 15),
        (Pizza("Funghi", 23, ["Tomato", "Mozzarella", "Basil", "Mushrooms"]), 10),
        (Pizza("Hawaii", 30, ["Tomato", "Mozzarella", "Pineapple", "Ham"]), 12),
        (Pizza("Capricciosa", 30, ["Tomato", "Mozzarella", "Ham", "Mushrooms"]), 12),
    ]
    test_customer = Customer("Peter", 400, 500)
    test_customer.order(test_menu[0][0], test_menu[0][1])
    test_customer.order(test_menu[1][0], test_menu[1][1])
    test_customer.pizza_dinner(test_menu)
    your_output = capsys.readouterr().out
    expected_output = "Peter ate Pepperoni: 30 cm -> 371.00€ and 374 hunger left!\n"
    expected_output += "Peter ate Margherita: 15 cm -> 366.00€ and 308 hunger left!\n"
    expected_output += "Peter ate Salami: 36 cm -> 366.00€ and 154 hunger left!\n"
    expected_output += "Peter ate Funghi: 23 cm -> 356.00€ and 54 hunger left!\n"
    expected_output += "Peter is completely full and can not finish Hawaii: 30 cm anymore!\n"
    assert expected_output == your_output
