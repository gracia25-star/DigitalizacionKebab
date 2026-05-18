from flask import Flask, render_template, jsonify
import sqlite3
import os

app = Flask(__name__)
DB_FILE = 'doner.db'

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def admin_index():
    return render_template('admin.html')

@app.route('/api/orders')
def get_orders():
    if not os.path.exists(DB_FILE):
        return jsonify([])
        
    conn = get_db_connection()
    # Obtenemos los últimos 50 pedidos que estén pendientes
    orders = conn.execute("SELECT * FROM orders WHERE status = 'pending' ORDER BY target_time ASC LIMIT 50").fetchall()
    
    orders_data = []
    for order in orders:
        order_dict = dict(order)
        # Obtenemos los productos de cada pedido
        items = conn.execute('''
            SELECT oi.quantity, oi.price, p.name 
            FROM order_items oi
            JOIN products p ON oi.product_id = p.id
            WHERE oi.order_id = ?
        ''', (order['id'],)).fetchall()
        
        order_dict['items'] = [dict(item) for item in items]
        orders_data.append(order_dict)
        
    conn.close()
    return jsonify(orders_data)

@app.route('/api/orders/<int:order_id>/complete', methods=['POST'])
def complete_order(order_id):
    conn = get_db_connection()
    conn.execute("UPDATE orders SET status = 'completed' WHERE id = ?", (order_id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

if __name__ == '__main__':
    # Ejecutamos en el puerto 5001 para que no interfiera con la app de clientes (puerto 5000)
    app.run(debug=True, port=5001)
