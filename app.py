from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import sqlite3
import os
from datetime import datetime, timedelta
from functools import wraps
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_segura_aqui'  # Cambiar en producción
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

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def worker_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        
        conn = get_db_connection()
        user = conn.execute('SELECT role FROM users WHERE id = ?', (session['user_id'],)).fetchone()
        conn.close()
        
        if not user or user['role'] != 'trabajador':
            return jsonify({'error': 'Acceso denegado'}), 403
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    if not os.path.exists(DB_FILE):
        return "Error: La base de datos no existe. Ejecuta 'python init_db.py' primero."
    
    # Si hay sesión activa, redirigir según el rol
    if 'user_id' in session:
        conn = get_db_connection()
        user = conn.execute('SELECT role FROM users WHERE id = ?', (session['user_id'],)).fetchone()
        conn.close()
        if user and user['role'] == 'trabajador':
            return redirect(url_for('worker_panel'))
    
    conn = get_db_connection()
    categories = conn.execute('SELECT DISTINCT category FROM products').fetchall()
    
    menu = {}
    for cat in categories:
        cat_name = cat['category']
        products = conn.execute('SELECT * FROM products WHERE category = ?', (cat_name,)).fetchall()
        menu[cat_name] = [dict(p) for p in products]
    
    conn.close()
    return render_template('index.html', menu=menu, user_id=session.get('user_id'), username=session.get('username'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.json
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'error': 'Datos incompletos'}), 400
        
        conn = get_db_connection()
        user = conn.execute('SELECT id, username, password, role FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()
        
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            return jsonify({'success': True, 'role': user['role']})
        
        return jsonify({'error': 'Credenciales inválidas'}), 401
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.json
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        role = data.get('role', 'cliente')
        
        if not username or not password:
            return jsonify({'error': 'Datos incompletos'}), 400
        
        if role not in ['cliente', 'trabajador']:
            return jsonify({'error': 'Rol inválido'}), 400
        
        conn = get_db_connection()
        try:
            conn.execute('''
                INSERT INTO users (username, password, email, role)
                VALUES (?, ?, ?, ?)
            ''', (username, generate_password_hash(password), email, role))
            conn.commit()
            
            user = conn.execute('SELECT id FROM users WHERE username = ?', (username,)).fetchone()
            session['user_id'] = user['id']
            session['username'] = username
            session['role'] = role
            
            return jsonify({'success': True, 'role': role})
        except sqlite3.IntegrityError:
            return jsonify({'error': 'El usuario ya existe'}), 400
        finally:
            conn.close()
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/api/order', methods=['POST'])
@login_required
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

# ========== RUTAS PARA TRABAJADORES ==========

@app.route('/worker')
@worker_required
def worker_panel():
    return render_template('worker.html', username=session.get('username'))

@app.route('/api/products', methods=['GET'])
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

if __name__ == '__main__':
    app.run(debug=True, port=5000)
