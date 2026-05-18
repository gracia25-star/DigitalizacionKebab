# Mega Döner Kebab 🥙

Un sistema completo de gestión web para un restaurante tipo Kebab. Incluye una interfaz moderna para que los clientes realicen pedidos y un panel de administración para que los trabajadores gestionen el menú y los pedidos entrantes.

## 🌟 Características Principales

### Para Clientes (App Principal)
- **Exploración del Menú**: Navegación por categorías (Menús, Dürüms, Platos, Complementos, Bebidas).
- **Carrito de Compras**: Añadir productos, ajustar cantidades y ver el total dinámicamente.
- **Pedidos Online**: Realizar pedidos indicando la hora de recogida preferida y datos de contacto.
- **Diseño Atractivo**: Interfaz fluida y moderna (HTML/CSS/JS).

### Para Trabajadores (Panel de Administración)
- **Autenticación**: Acceso seguro mediante inicio de sesión.
- **Gestión del Menú (CRUD)**: Añadir nuevos productos con imágenes, editar existentes o eliminarlos.
- **Gestión de Pedidos**: Visualización en tiempo real de los pedidos pendientes (fecha, hora objetivo, productos).
- **Completar Pedidos**: Marcar pedidos como completados cuando estén listos.

## 🛠️ Tecnologías y Herramientas

- **Backend**: Python con [Flask](https://flask.palletsprojects.com/) y [Werkzeug](https://werkzeug.palletsprojects.com/).
- **Base de Datos**: SQLite3 (`doner.db`).
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla).
- **Tipografía**: 'Outfit' de Google Fonts.

## 🚀 Requisitos e Instalación

1. **Clonar o descargar el proyecto** a tu máquina local.
2. **Instalar dependencias**:
   Asegúrate de tener Python 3 instalado. Abre una terminal en la raíz del proyecto y ejecuta:
   ```bash
   pip install -r requirements.txt
   ```
3. **Inicializar la base de datos**:
   Antes de ejecutar la aplicación, debes crear las tablas y los datos de prueba iniciales:
   ```bash
   python init_db.py
   ```
   *Esto generará el archivo `doner.db` y poblará la base de datos con el menú inicial.*

## 🏃‍♂️ Cómo Ejecutar la Aplicación

El proyecto se divide en dos servicios que corren simultáneamente en puertos diferentes.

**1. Interfaz de Clientes:**
Abre una terminal y ejecuta:
```bash
python app.py
```
Accede desde tu navegador a: `http://localhost:5000`

**2. Panel de Trabajadores:**
Abre una **segunda terminal** y ejecuta:
```bash
python admin_app.py
```
Accede desde tu navegador a: `http://localhost:5001`

## 👥 Cuentas de Prueba

Al inicializar la base de datos (`init_db.py`), se crean las siguientes cuentas para hacer pruebas en el sistema (las contraseñas se guardan de forma segura usando hashes):

- **Trabajador (Panel de Administración)**
  - Usuario: `trabajador_demo`
  - Contraseña: `trabajador123`

- **Cliente**
  - Usuario: `cliente_demo`
  - Contraseña: `cliente123`

## 📁 Estructura del Proyecto

```text
MegaDonerKebab/
├── app.py              # App principal para clientes (Puerto 5000)
├── admin_app.py        # App de gestión para trabajadores (Puerto 5001)
├── init_db.py          # Script de inicialización de la base de datos SQLite
├── requirements.txt    # Dependencias de Python necesarias
├── doner.db            # Base de datos SQLite (se genera automáticamente)
├── schema.sql          # Archivo generado temporalmente durante init_db.py
├── static/
│   └── uploads/        # Directorio donde se guardan las imágenes subidas
└── templates/          # Plantillas HTML de la aplicación
    ├── index.html      # Página principal para los clientes
    ├── worker.html     # Dashboard completo para trabajadores
    ├── login.html      # Formulario de inicio de sesión
    ├── register.html   # Formulario de registro
    └── admin_login.html# Inicio de sesión exclusivo para trabajadores
```
