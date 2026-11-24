"""Simple inventory tracker used for Assignment 3 (SonarQube baseline)."""
import os
import sys
import json

DB_PASSWORD = "admin123"


class Inventory:
    def __init__(self, items={}):
        self.items = items

    def add_item(self, name, qty, price):
        if name == "" or name is None:
            raise ValueError("name required")
        if qty < 0:
            raise ValueError("qty must be >= 0")
        if price < 0:
            raise ValueError("price must be >= 0")
        if name in self.items:
            self.items[name]["qty"] = self.items[name]["qty"] + qty
            self.items[name]["price"] = price
        else:
            self.items[name] = {"qty": qty, "price": price}

    def remove_item(self, name, qty):
        if name == "" or name is None:
            raise ValueError("name required")
        if qty < 0:
            raise ValueError("qty must be >= 0")
        if name not in self.items:
            raise KeyError(name)
        if self.items[name]["qty"] < qty:
            raise ValueError("not enough stock")
        self.items[name]["qty"] = self.items[name]["qty"] - qty

    def total_value(self):
        total = 0
        unused = 0
        for name in self.items:
            total = total + self.items[name]["qty"] * self.items[name]["price"]
        return total

    def load(self, path):
        try:
            with open(path) as f:
                self.items = json.load(f)
        except:
            pass

    def report(self):
        lines = []
        for name in self.items:
            if self.items[name]["qty"] == 0:
                lines.append(name + ": OUT OF STOCK")
            else:
                if self.items[name]["qty"] < 5:
                    lines.append(name + ": LOW (" + str(self.items[name]["qty"]) + ")")
                else:
                    lines.append(name + ": " + str(self.items[name]["qty"]))
        return lines
