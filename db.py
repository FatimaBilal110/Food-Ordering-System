import sqlite3
from datetime import datetime

conn = sqlite3.connect('food_order.db')
cursor = conn.cursor()

def init_db():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Menu (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE,
            price REAL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER,
            item_id INTEGER,
            quantity INTEGER,
            total_price REAL,
            FOREIGN KEY (order_id) REFERENCES orders(id),
            FOREIGN KEY (item_id) REFERENCES Menu(id)
        )
    ''')

    # ✅ Check if Menu is empty before inserting
    cursor.execute("SELECT COUNT(*) FROM Menu")
    count = cursor.fetchone()[0]
    if count == 0:
        cursor.execute("INSERT INTO Menu (name, price) VALUES ('Burger', 350)")
        cursor.execute("INSERT INTO Menu (name, price) VALUES ('Pizza', 1270)")
        cursor.execute("INSERT INTO Menu (name, price) VALUES ('Fries', 120)")
        cursor.execute("INSERT INTO Menu (name, price) VALUES ('Coke', 70)")

    conn.commit()

def get_menu():
    cursor.execute("SELECT * FROM Menu")
    return cursor.fetchall()

def get_price(item_id):
    cursor.execute("SELECT price FROM Menu WHERE id = ?", (item_id,))
    return cursor.fetchone()

def create_order(customer_name):
    cursor.execute("INSERT INTO orders (customer_name) VALUES (?)", (customer_name,))
    conn.commit()
    return cursor.lastrowid

def add_order_item(order_id, item_id, quantity, total_price):
    cursor.execute('''
        INSERT INTO order_items (order_id, item_id, quantity, total_price)
        VALUES (?, ?, ?, ?)
    ''', (order_id, item_id, quantity, total_price))
    conn.commit()

def get_all_orders():
    cursor.execute('''
        SELECT o.id, o.customer_name, m.name, oi.quantity, oi.total_price
        FROM orders o
        JOIN order_items oi ON o.id = oi.order_id
        JOIN Menu m ON oi.item_id = m.id
        ORDER BY o.id
    ''')
    return cursor.fetchall()
