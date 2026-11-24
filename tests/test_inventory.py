import pytest
from src.inventory import Inventory


def make():
    return Inventory(items={})


def test_add_and_total():
    inv = make()
    inv.add_item("apple", 10, 0.5)
    inv.add_item("pear", 2, 1.0)
    assert inv.total_value() == pytest.approx(7.0)


def test_add_existing_increases_qty():
    inv = make()
    inv.add_item("apple", 3, 0.5)
    inv.add_item("apple", 2, 0.6)
    assert inv.items["apple"] == {"qty": 5, "price": 0.6}


def test_remove_item():
    inv = make()
    inv.add_item("apple", 10, 0.5)
    inv.remove_item("apple", 4)
    assert inv.items["apple"]["qty"] == 6


def test_remove_too_many():
    inv = make()
    inv.add_item("apple", 1, 0.5)
    with pytest.raises(ValueError):
        inv.remove_item("apple", 5)


def test_invalid_add():
    inv = make()
    with pytest.raises(ValueError):
        inv.add_item("", 1, 1)
    with pytest.raises(ValueError):
        inv.add_item("x", -1, 1)
