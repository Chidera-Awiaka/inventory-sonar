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


def test_default_items_not_shared():
    a = Inventory()
    b = Inventory()
    a.add_item("x", 1, 1)
    assert b.items == {}


def test_report_levels():
    inv = make()
    inv.add_item("a", 0, 1)
    inv.add_item("b", 3, 1)
    inv.add_item("c", 9, 1)
    assert inv.report() == ["a: OUT OF STOCK", "b: LOW (3)", "c: 9"]


def test_load_ok(tmp_path):
    p = tmp_path / "inv.json"
    p.write_text('{"apple": {"qty": 2, "price": 1.5}}')
    inv = make()
    inv.load(p)
    assert inv.total_value() == pytest.approx(3.0)


def test_load_bad_file_raises(tmp_path):
    inv = make()
    with pytest.raises(ValueError):
        inv.load(tmp_path / "missing.json")


def test_remove_missing_and_invalid():
    inv = make()
    with pytest.raises(KeyError):
        inv.remove_item("ghost", 1)
    with pytest.raises(ValueError):
        inv.remove_item("", 1)
    with pytest.raises(ValueError):
        inv.add_item("x", 1, -1)
