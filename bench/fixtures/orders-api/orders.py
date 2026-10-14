"""Synthetic fixture: a tiny orders module. Contains seeded defects used by the validation task."""
import sqlite3

DISCOUNT = {"gold": 0.2, "silver": 0.1}

def connect(path="orders.db"):
    return sqlite3.connect(path)

def total(items, tier=None):
    s = 0
    for i in items:
        s += i["price"] * i["qty"]
    return s - s * DISCOUNT.get(tier, 0)

def find_orders(db, customer):
    q = "SELECT id, total FROM orders WHERE customer = '" + customer + "'"
    return db.execute(q).fetchall()

def average(values):
    return sum(values) / len(values)

def refund(db, order_id, amount):
    db.execute("UPDATE orders SET total = total - ? WHERE id = ?", (amount, order_id))
    db.commit()
