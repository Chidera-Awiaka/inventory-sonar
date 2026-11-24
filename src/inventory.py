"""Simple inventory tracker used for Assignment 3 (refactored after SonarQube scan)."""
import json
import os

LOW_STOCK_THRESHOLD = 5


class Inventory:
    def __init__(self, items=None):
        self.items = items if items is not None else {}

    @staticmethod
    def _validate(name, qty):
        if not name:
            raise ValueError("name required")
        if qty < 0:
            raise ValueError("qty must be >= 0")

    def add_item(self, name, qty, price):
        self._validate(name, qty)
        if price < 0:
            raise ValueError("price must be >= 0")
        current = self.items.get(name, {"qty": 0})["qty"]
        self.items[name] = {"qty": current + qty, "price": price}

    def remove_item(self, name, qty):
        self._validate(name, qty)
        if name not in self.items:
            raise KeyError(name)
        if self.items[name]["qty"] < qty:
            raise ValueError("not enough stock")
        self.items[name]["qty"] -= qty

    def total_value(self):
        return sum(item["qty"] * item["price"] for item in self.items.values())

    def load(self, path):
        try:
            with open(path, encoding="utf-8") as f:
                self.items = json.load(f)
        except (OSError, json.JSONDecodeError) as exc:
            raise ValueError(f"could not load inventory from {path}") from exc

    def report(self):
        lines = []
        for name, item in self.items.items():
            qty = item["qty"]
            if qty == 0:
                lines.append(f"{name}: OUT OF STOCK")
            elif qty < LOW_STOCK_THRESHOLD:
                lines.append(f"{name}: LOW ({qty})")
            else:
                lines.append(f"{name}: {qty}")
        return lines


def db_password():
    """Credentials come from the environment, never source code."""
    return os.environ.get("DB_PASSWORD", "")
