# 🌮 Mega Döner Kebab - Aplicación Web

Sistema de pedidos online para el restaurante Mega Döner Kebab con soporte para dos tipos de usuarios: **Clientes** y **Trabajadores**.

## 🎯 Características

### Para Clientes:
- ✅ Registro e inicio de sesión
- ✅ Visualizar menú completo organizado por categorías
- ✅ Agregar/quitar productos del carrito
- ✅ Realizar pedidos especificando:
  - Nombre y apellidos
  - Teléfono
  - Dirección de entrega
  - Hora deseada de entrega (mínimo 1 hora)

### Para Trabajadores:
- ✅ Registro e inicio de sesión con rol de trabajador
- ✅ **Panel de administración** para gestionar productos
- ✅ **Agregar productos** con:
  - Nombre
  - Descripción
  - Precio
  - Categoría
  - Imagen (carga de archivos)
- ✅ **Editar productos** existentes
- ✅ **Eliminar productos** del catálogo
- ✅ **Cambiar imágenes** de productos

## 🚀 Instalación y uso

### Requisitos previos:
- Python 3.8 o superior
- pip

### Pasos de instalación:

1. **Clonar o descargar el proyecto**
   ```bash
   cd MegaDonerKebab
   ```

2. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

3. **Inicializar la base de datos**
   ```bash
   python init_db.py
   ```
   Esto creará:
   - Base de datos `doner.db`
   - Tabla de usuarios, productos, pedidos
   - Menú inicial de ejemplo
   - Usuarios de prueba

4. **Ejecutar la aplicación**
   ```bash
   python app.py
   ```
   La aplicación estará disponible en: **http://localhost:5000**

## 👥 Usuarios de Prueba

La base de datos se inicializa con dos usuarios de prueba:

### Cliente:
- **Usuario**: `cliente_demo`
- **Contraseña**: `cliente123`
- **Rol**: Cliente (puede hacer pedidos)

### Trabajador:
- **Usuario**: `trabajador_demo`
- **Contraseña**: `trabajador123`
- **Rol**: Trabajador (puede gestionar productos)

## 📂 Estructura del Proyecto

```
MegaDonerKebab/
├── app.py                      # Aplicación principal Flask
├── init_db.py                  # Script de inicialización de BD
├── requirements.txt            # Dependencias del proyecto
├── schema.sql                  # Esquema de la base de datos (generado)
├── doner.db                    # Base de datos SQLite (generada)
├── static/
│   ├── css/
│   │   ├── style.css          # Estilos para clientes
│   │   └── admin_style.css    # Estilos para administración
│   ├── js/
│   │   ├── main.js            # Lógica del cliente
│   │   └── admin.js           # Lógica del administrador
│   ├── img/                   # Imágenes estáticas
│   └── uploads/               # Imágenes de productos (generada)
└── templates/
    ├── index.html             # Página principal (clientes)
    ├── login.html             # Página de inicio de sesión
    ├── register.html          # Página de registro
    ├── worker.html            # Panel de trabajador
    └── admin.html             # Panel de administración (antiguo)
```

## 🔐 Seguridad

- Las contraseñas se almacenan hasheadas con **werkzeug.security**
- Las sesiones se protegen con claves secretas de Flask
- Los archivos cargados se validan y se renombran de forma segura
- Las rutas sensibles están protegidas con decoradores `@login_required` y `@worker_required`

## 🗄️ Base de Datos

### Tabla: users
- `id` (PK): Identificador único
- `username`: Nombre de usuario único
- `password`: Contraseña hasheada
- `email`: Correo electrónico
- `role`: 'cliente' o 'trabajador'
- `created_at`: Fecha de creación

### Tabla: products
- `id` (PK): Identificador único
- `name`: Nombre del producto
- `description`: Descripción
- `price`: Precio en euros
- `category`: Categoría
- `image_path`: Ruta a la imagen

### Tabla: orders
- `id` (PK): Identificador único
- `customer_name`: Nombre del cliente
- `customer_phone`: Teléfono del cliente
- `customer_address`: Dirección de entrega
- `total_price`: Precio total
- `created_at`: Fecha de creación del pedido
- `target_time`: Hora deseada de entrega
- `status`: Estado del pedido ('pending', 'completed')

### Tabla: order_items
- `id` (PK): Identificador único
- `order_id` (FK): Referencia al pedido
- `product_id` (FK): Referencia al producto
- `quantity`: Cantidad del producto
- `price`: Precio en el momento del pedido

## 🔄 Flujo de uso

### Como Cliente:
1. Acceder a la aplicación
2. Registrarse o iniciar sesión
3. Explorar el menú
4. Agregar productos al carrito
5. Hacer clic en el carrito y completar el pedido
6. Especificar datos de entrega e hora

### Como Trabajador:
1. Registrarse con rol "Trabajador" o iniciar sesión
2. Ir al panel de trabajador
3. Agregar nuevos productos con imagen
4. Editar productos existentes (cambiar precio, descripción, imagen)
5. Eliminar productos que ya no estén disponibles

## 🎨 Personalización

### Cambiar colores:
Editar los valores en los archivos CSS:
- Color primario: `#ff6b35` (naranja)
- Color secundario: `#f7931e` (naranja claro)

### Agregar nuevas categorías:
Los trabajadores pueden crear categorías nuevas directamente al crear productos. No hay límite de categorías.

### Cambiar la clave secreta:
En `app.py`, cambiar la línea:
```python
app.secret_key = 'tu_clave_secreta_segura_aqui'
```

**IMPORTANTE**: Generar una clave segura aleatoria para producción.

## 📝 Notas

- Las imágenes se guardan en `static/uploads/`
- El tamaño máximo de imagen recomendado es 5MB
- Los formatos permitidos son: PNG, JPG, JPEG, GIF
- La hora de entrega debe ser mínimo 1 hora en el futuro

## 🐛 Solución de problemas

### La base de datos no se crea:
```bash
python init_db.py
```

### Las imágenes no se muestran:
- Verificar que la carpeta `static/uploads/` existe
- Verificar permisos de lectura en la carpeta
- Recargar el navegador con Ctrl+F5

### Error de conexión:
- Verificar que `doner.db` existe
- Verificar que el puerto 5000 está disponible

## 📄 Licencia

Proyecto para Kit Digital.

## ✉️ Contacto

Para preguntas o reportar problemas, contactar al equipo de desarrollo.
