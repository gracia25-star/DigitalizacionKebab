from flask import Flask, render_template, request, jsonify
import sqlite3
import os
from datetime import datetime, timedelta

app = Flask(__name__)
DB_FILE = 'doner.db'

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    if not os.path.exists(DB_FILE):
        return "Error: La base de datos no existe. Ejecuta 'python init_db.py' primero."
        
    conn = get_db_connection()
    categories = conn.execute('SELECT DISTINCT category FROM products').fetchall()
    
    menu = {}
    for cat in categories:
        cat_name = cat['category']
        products = conn.execute('SELECT * FROM products WHERE category = ?', (cat_name,)).fetchall()
        menu[cat_name] = [dict(p) for p in products]
    
    conn.close()
    return render_template('index.html', menu=menu)

@app.route('/api/order', methods=['POST'])
def place_order():
    data = request.json
    customer_name = data.get('name')
    customer_phone = data.get('phone')
    customer_address = data.get('address')
    cart = data.get('cart', [])
    
    if not cart or not customer_name or not customer_address:
        return jsonify({'error': 'Datos incompletos'}), 400
    
    total = sum(item['price'] * item['quantity'] for item in cart)
    
    target_time_str = data.get('target_time')
    
    if target_time_str:
        target_time = f"{datetime.now().strftime('%Y-%m-%d')} {target_time_str}:00"
    else:
        target_time = (datetime.now() + timedelta(minutes=60)).strftime('%Y-%m-%d %H:%M:%S')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO orders (customer_name, customer_phone, customer_address, total_price, target_time)
            VALUES (?, ?, ?, ?, ?)
        ''', (customer_name, customer_phone, customer_address, total, target_time))
        
        order_id = cursor.lastrowid
        
        for item in cart:
            cursor.execute('''
                INSERT INTO order_items (order_id, product_id, quantity, price)
                VALUES (?, ?, ?, ?)
            ''', (order_id, item['id'], item['quantity'], item['price']))
            
        conn.commit()
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()
    
    return jsonify({'success': True, 'order_id': order_id, 'message': 'Pedido realizado con éxito'})

@app.route('/api/products', methods=['GET'])
def get_products():
    conn = get_db_connection()
    products = conn.execute('SELECT * FROM products').fetchall()
    conn.close()
    return jsonify([dict(p) for p in products])

if __name__ == '__main__':
    app.run(debug=True, port=5000)
