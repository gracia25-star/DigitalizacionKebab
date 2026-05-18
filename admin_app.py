from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import sqlite3
import os
from datetime import datetime
from functools import wraps
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.secret_key = 'clave_secreta_admin_segura'  # Cambiar en producción
DB_FILE = 'doner.db'
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def worker_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login_admin'))
        
        conn = get_db_connection()
        user = conn.execute('SELECT role FROM users WHERE id = ?', (session['user_id'],)).fetchone()
        conn.close()
        
        if not user or user['role'] != 'trabajador':
            return redirect(url_for('login_admin'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def admin_index():
    if 'user_id' not in session:
        return redirect(url_for('login_admin'))
    return render_template('worker.html', username=session.get('username'))

@app.route('/login', methods=['GET', 'POST'])
def login_admin():
    if request.method == 'POST':
        data = request.json
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'error': 'Datos incompletos'}), 400
        
        conn = get_db_connection()
        user = conn.execute('SELECT id, username, password, role FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()
        
        if user and user['role'] == 'trabajador' and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            return jsonify({'success': True})
        
        return jsonify({'error': 'Credenciales inválidas o no eres trabajador'}), 401
    
    return render_template('admin_login.html')

@app.route('/logout')
def logout_admin():
    session.clear()
    return redirect(url_for('login_admin'))

# ========== RUTAS DE PRODUCTOS ==========

@app.route('/api/products', methods=['GET'])
@worker_required
def get_products():
    conn = get_db_connection()
    products = conn.execute('SELECT * FROM products').fetchall()
    conn.close()
    return jsonify([dict(p) for p in products])

@app.route('/api/products', methods=['POST'])
@worker_required
def add_product():
    name = request.form.get('name')
    description = request.form.get('description')
    price = request.form.get('price')
    category = request.form.get('category')
    
    if not all([name, price, category]):
        return jsonify({'error': 'Datos incompletos'}), 400
    
    image_path = None
    if 'image' in request.files:
        file = request.files['image']
        if file and allowed_file(file.filename):
            filename = secure_filename(f"{datetime.now().timestamp()}_{file.filename}")
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            image_path = f"uploads/{filename}"
    
    conn = get_db_connection()
    try:
        conn.execute('''
            INSERT INTO products (name, description, price, category, image_path)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, description, float(price), category, image_path))
        conn.commit()
        product = conn.execute('SELECT * FROM products ORDER BY id DESC LIMIT 1').fetchone()
        return jsonify(dict(product)), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/products/<int:product_id>', methods=['PUT'])
@worker_required
def update_product(product_id):
    name = request.form.get('name')
    description = request.form.get('description')
    price = request.form.get('price')
    category = request.form.get('category')
    
    conn = get_db_connection()
    product = conn.execute('SELECT * FROM products WHERE id = ?', (product_id,)).fetchone()
    
    if not product:
        conn.close()
        return jsonify({'error': 'Producto no encontrado'}), 404
    
    image_path = product['image_path']
    
    if 'image' in request.files:
        file = request.files['image']
        if file and allowed_file(file.filename):
            if product['image_path'] and os.path.exists(os.path.join(UPLOAD_FOLDER, product['image_path'].split('/')[-1])):
                os.remove(os.path.join(UPLOAD_FOLDER, product['image_path'].split('/')[-1]))
            
            filename = secure_filename(f"{datetime.now().timestamp()}_{file.filename}")
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            image_path = f"uploads/{filename}"
    
    try:
        conn.execute('''
            UPDATE products
            SET name = ?, description = ?, price = ?, category = ?, image_path = ?
            WHERE id = ?
        ''', (name or product['name'], description or product['description'], 
              float(price) if price else product['price'], category or product['category'], 
              image_path, product_id))
        conn.commit()
        updated = conn.execute('SELECT * FROM products WHERE id = ?', (product_id,)).fetchone()
        return jsonify(dict(updated))
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/products/<int:product_id>', methods=['DELETE'])
@worker_required
def delete_product(product_id):
    conn = get_db_connection()
    product = conn.execute('SELECT * FROM products WHERE id = ?', (product_id,)).fetchone()
    
    if not product:
        conn.close()
        return jsonify({'error': 'Producto no encontrado'}), 404
    
    if product['image_path'] and os.path.exists(os.path.join(UPLOAD_FOLDER, product['image_path'].split('/')[-1])):
        os.remove(os.path.join(UPLOAD_FOLDER, product['image_path'].split('/')[-1]))
    
    try:
        conn.execute('DELETE FROM products WHERE id = ?', (product_id,))
        conn.commit()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

# ========== RUTAS DE PEDIDOS ==========

@app.route('/api/orders', methods=['GET'])
@worker_required
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
@worker_required
def complete_order(order_id):
    conn = get_db_connection()
    conn.execute("UPDATE orders SET status = 'completed' WHERE id = ?", (order_id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

if __name__ == '__main__':
    # Ejecutamos en el puerto 5001 para que no interfiera con la app de clientes (puerto 5000)
    app.run(debug=True, port=5001)
