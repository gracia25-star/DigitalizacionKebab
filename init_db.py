import sqlite3
import os
from werkzeug.security import generate_password_hash

DB_FILE = 'doner.db'

def init_db():
    connection = sqlite3.connect(DB_FILE)

    with open('schema.sql', 'w', encoding='utf-8') as f:
        f.write('''
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS order_items;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    email TEXT,
    role TEXT NOT NULL DEFAULT 'cliente',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    price REAL NOT NULL,
    category TEXT NOT NULL,
    image_path TEXT
);

CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name TEXT NOT NULL,
    customer_phone TEXT,
    customer_address TEXT,
    total_price REAL NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    target_time TIMESTAMP,
    status TEXT DEFAULT 'pending'
);

CREATE TABLE order_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    price REAL NOT NULL,
    FOREIGN KEY(order_id) REFERENCES orders(id),
    FOREIGN KEY(product_id) REFERENCES products(id)
);
''')

    with open('schema.sql', 'r', encoding='utf-8') as f:
        connection.executescript(f.read())

    cur = connection.cursor()

    # Agregar usuarios de prueba
    test_users = [
        ('cliente_demo', generate_password_hash('cliente123'), 'cliente@example.com', 'cliente'),
        ('trabajador_demo', generate_password_hash('trabajador123'), 'trabajador@example.com', 'trabajador'),
    ]
    
    cur.executemany("INSERT INTO users (username, password, email, role) VALUES (?, ?, ?, ?)", test_users)

    menu_items = [
        # Menús
        ("Menú Dürüm", "Dürüm a elegir + patatas fritas + bebida", 8.50, "Menús", None),
        ("Menú Pita", "Pita a elegir + patatas fritas + bebida", 7.50, "Menús", None),
        ("Menú XXXL", "Durum gigante, patatas, bebida", 12.00, "Menús", None),
        
        # Dürüms
        ("Dürüm de Ternera", "Carne de ternera asada, lechuga, tomate, cebolla y salsas", 5.50, "Dürüms", None),
        ("Dürüm de Pollo", "Carne de pollo asada, lechuga, tomate, cebolla y salsas", 5.00, "Dürüms", None),
        ("Dürüm Mixto", "Mezcla de ternera y pollo con verduras y salsas", 5.50, "Dürüms", None),
        ("Dürüm Solo Carne", "Extra de carne con queso fundido y salsas", 6.50, "Dürüms", None),
        
        # Platos
        ("Plato Kebab Mixto", "Carne mixta acompañada de arroz, ensalada, pan de pita y salsas", 9.00, "Platos", None),
        ("Plato Vegetariano", "Falafel, arroz, ensalada, hummus y pan de pita", 8.00, "Platos", None),
        
        # Complementos
        ("Ración de Patatas", "Patatas fritas crujientes", 3.00, "Complementos", None),
        ("Nuggets de Pollo (6 uds)", "Crujientes nuggets de pollo", 4.50, "Complementos", None),
        ("Falafel (5 uds)", "Croquetas de garbanzo con salsa de yogur", 4.50, "Complementos", None),
        
        # Bebidas
        ("Refresco 33cl", "Coca-Cola, Fanta, Sprite", 1.50, "Bebidas", None),
        ("Agua", "Botella de agua 50cl", 1.20, "Bebidas", None),
        ("Ayran", "Bebida tradicional turca a base de yogur", 1.80, "Bebidas", None)
    ]

    cur.executemany("INSERT INTO products (name, description, price, category, image_path) VALUES (?, ?, ?, ?, ?)", menu_items)

    connection.commit()
    connection.close()
    print("✅ Base de datos inicializada correctamente con el menú de Mega Döner Kebab.")
    print("\n📝 Usuarios de prueba creados:")
    print("   Cliente - usuario: cliente_demo, contraseña: cliente123")
    print("   Trabajador - usuario: trabajador_demo, contraseña: trabajador123")

if __name__ == '__main__':
    init_db()
