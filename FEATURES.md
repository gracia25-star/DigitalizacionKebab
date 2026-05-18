# ✨ Características Implementadas

## Sistema de Usuarios

### Autenticación
- ✅ Registro de nuevos usuarios con validación
- ✅ Login con credenciales
- ✅ Sesiones seguras con Flask
- ✅ Logout con limpieza de sesión
- ✅ Hash de contraseñas con Werkzeug

### Roles de Usuario
- ✅ **CLIENTE**: Usuario regular para hacer pedidos
- ✅ **TRABAJADOR**: Usuario con permisos de administración

### Sistema de Sesiones
- ✅ Protección de rutas con decoradores
- ✅ Redirección automática a login si no autenticado
- ✅ Verificación de rol para acceso a funciones específicas

---

## Funcionalidades de Cliente

### Visualización de Menú
- ✅ Catálogo de productos organizado por categorías
- ✅ Información de cada producto (nombre, descripción, precio, imagen)
- ✅ Carga dinámica de menú desde base de datos
- ✅ Vista responsive adaptable a móviles y escritorio

### Carrito de Compras
- ✅ Agregar productos al carrito
- ✅ Incrementar/decrementar cantidades
- ✅ Eliminar productos del carrito
- ✅ Visualización del total
- ✅ Contador de productos en carrito
- ✅ Carrito persistente en navegador (localStorage)

### Proceso de Pedido
- ✅ Datos de cliente (nombre, teléfono, dirección)
- ✅ Selección de hora de entrega
- ✅ Validación de hora (mínimo 1 hora en futuro)
- ✅ Confirmación de pedido
- ✅ Número de pedido generado
- ✅ Mensaje de éxito

### Experiencia de Usuario
- ✅ Interfaz intuitiva y atractiva
- ✅ Animaciones suaves
- ✅ Modal de carrito lateral
- ✅ Modal de checkout
- ✅ Barras de error/éxito
- ✅ Mensajes de validación

---

## Funcionalidades de Trabajador

### Panel de Administración
- ✅ Interfaz dedicada para trabajadores
- ✅ Vista en grid de todos los productos
- ✅ Información de usuario en navbar
- ✅ Botón de cierre de sesión

### Gestión de Productos

#### Agregar Producto
- ✅ Formulario modal para agregar
- ✅ Campos: nombre, descripción, precio, categoría
- ✅ Carga de imagen (PNG, JPG, GIF)
- ✅ Vista previa de imagen antes de guardar
- ✅ Validación de campos obligatorios
- ✅ Mensajes de error/éxito

#### Editar Producto
- ✅ Modal de edición con datos precargados
- ✅ Cambiar nombre, descripción, precio, categoría
- ✅ Cambiar imagen del producto
- ✅ Mantener imagen actual si no se cambia
- ✅ Vista previa de imagen actual

#### Eliminar Producto
- ✅ Botón de eliminar con confirmación
- ✅ Eliminación de archivo de imagen
- ✅ Confirmación antes de eliminar

#### Visualización de Productos
- ✅ Grid responsivo de productos
- ✅ Tarjetas con imagen del producto
- ✅ Información: nombre, categoría, precio
- ✅ Botones de editar y eliminar
- ✅ Mensaje de vacío si no hay productos

### Gestión de Imágenes
- ✅ Carga de archivos con validación
- ✅ Generación de nombres únicos (timestamp)
- ✅ Almacenamiento en `static/uploads/`
- ✅ Eliminación de imagen anterior al actualizar
- ✅ Vista previa antes de guardar
- ✅ Formatos permitidos: PNG, JPG, JPEG, GIF

---

## Base de Datos

### Tablas Implementadas

#### Tabla: users
```sql
- id (PK): Identificador único
- username: Nombre de usuario único
- password: Contraseña hasheada
- email: Correo electrónico
- role: 'cliente' o 'trabajador'
- created_at: Timestamp de creación
```

#### Tabla: products
```sql
- id (PK): Identificador único
- name: Nombre del producto
- description: Descripción
- price: Precio en euros
- category: Categoría
- image_path: Ruta a la imagen en servidor
```

#### Tabla: orders
```sql
- id (PK): Identificador único
- customer_name: Nombre del cliente
- customer_phone: Teléfono
- customer_address: Dirección de entrega
- total_price: Precio total del pedido
- created_at: Timestamp de creación
- target_time: Hora deseada de entrega
- status: 'pending' o 'completed'
```

#### Tabla: order_items
```sql
- id (PK): Identificador único
- order_id (FK): Referencia al pedido
- product_id (FK): Referencia al producto
- quantity: Cantidad
- price: Precio en momento del pedido
```

### Relaciones
- ✅ Relación 1:N entre users y orders (usuario puede hacer múltiples pedidos)
- ✅ Relación N:M entre orders y products (mediante order_items)
- ✅ Integridad referencial con FOREIGN KEY

---

## API REST

### Endpoints de Autenticación
```
POST /login              - Iniciar sesión
POST /register           - Registrarse como nuevo usuario
GET  /logout             - Cerrar sesión
```

### Endpoints de Productos (Cliente)
```
GET  /api/products       - Obtener lista de todos los productos
```

### Endpoints de Productos (Trabajador)
```
POST   /api/products              - Crear nuevo producto
PUT    /api/products/<id>         - Actualizar producto
DELETE /api/products/<id>         - Eliminar producto
```

### Endpoints de Pedidos
```
POST /api/order          - Crear nuevo pedido (Cliente)
GET  /api/orders         - Obtener pedidos pendientes (Admin)
POST /api/orders/<id>/complete - Marcar pedido como completado
```

---

## Seguridad Implementada

- ✅ Contraseñas hasheadas con algoritmo PBKDF2
- ✅ Validación de entrada en formularios
- ✅ Protección CSRF con sesiones
- ✅ Decoradores `@login_required` para rutas protegidas
- ✅ Decoradores `@worker_required` para rutas de trabajador
- ✅ Validación de extensiones de archivo
- ✅ Renombrado seguro de archivos (timestamp + nombre)
- ✅ Eliminación de archivos al eliminar productos

---

## Experiencia de Usuario

### Diseño Visual
- ✅ Gradiente naranja/dorado (colores de marca)
- ✅ Fuente "Outfit" de Google Fonts
- ✅ Interfaz moderna y limpia
- ✅ Consistencia visual entre todas las páginas

### Responsividad
- ✅ Diseño responsive (mobile, tablet, desktop)
- ✅ Grid adaptativo para productos
- ✅ Navegación móvil optimizada
- ✅ Formularios con inputs apropiados

### Animaciones y Transiciones
- ✅ Animación de entrada en modales
- ✅ Transiciones suaves en botones
- ✅ Escalado en carrito al agregar
- ✅ Hover effects en tarjetas
- ✅ Spinner de carga

### Mensajería
- ✅ Mensajes de error en color rojo
- ✅ Mensajes de éxito en color verde
- ✅ Validación de formularios con feedback
- ✅ Confirmaciones antes de acciones destructivas

---

## Características Técnicas

### Backend
- ✅ Flask 3.0.0
- ✅ SQLite 3 (base de datos integrada)
- ✅ Werkzeug 3.0.0 (utilerías de seguridad)
- ✅ Manejo de sesiones con secreto seguro
- ✅ Decoradores Python para autorización

### Frontend
- ✅ HTML5 semántico
- ✅ CSS3 moderno (flexbox, grid, gradientes)
- ✅ JavaScript vanilla (sin frameworks)
- ✅ Fetch API para comunicación con backend
- ✅ LocalStorage para persistencia del carrito

### Desarrollo
- ✅ Estructura modular de código
- ✅ Separación de responsabilidades
- ✅ Documentación incluida (README, GUIDE)
- ✅ Base de datos de fácil inicialización

---

## Casos de Uso Cubiertos

### Cliente
1. ✅ Registrarse como nuevo cliente
2. ✅ Iniciar sesión
3. ✅ Ver catálogo completo
4. ✅ Filtrar por categoría
5. ✅ Agregar a carrito
6. ✅ Ajustar cantidades
7. ✅ Hacer pedido
8. ✅ Cerrar sesión

### Trabajador
1. ✅ Registrarse como nuevo trabajador
2. ✅ Iniciar sesión
3. ✅ Ir a panel de administración
4. ✅ Ver todos los productos
5. ✅ Agregar producto con imagen
6. ✅ Editar producto existente
7. ✅ Cambiar imagen de producto
8. ✅ Eliminar producto
9. ✅ Cerrar sesión

---

## Datos de Inicialización

### Productos Precargados
- 3 Menús
- 4 Dürüms
- 2 Platos
- 3 Complementos
- 3 Bebidas

**Total**: 15 productos de ejemplo

### Usuarios de Prueba
- Cliente demo: `cliente_demo` / `cliente123`
- Trabajador demo: `trabajador_demo` / `trabajador123`

---

## Extensibilidad

La aplicación está diseñada para fácil expansión:

- ✅ Agregar nuevas categorías (sin modificar código)
- ✅ Sistema de permisos preparado para más roles
- ✅ API REST lista para integración con terceros
- ✅ Estructura de BD normalizada
- ✅ Código modular y bien documentado

---

## Estado de Características

| Característica | Estado | Notas |
|---|---|---|
| Autenticación | ✅ Completa | Login/Registro funcional |
| Roles de usuario | ✅ Completa | Cliente y Trabajador |
| Catálogo de productos | ✅ Completa | Con imágenes |
| Carrito de compras | ✅ Completa | Con persistencia |
| Pedidos | ✅ Completa | Con validación de hora |
| Gestión de productos | ✅ Completa | CRUD funcional |
| Carga de imágenes | ✅ Completa | Con validación |
| Seguridad | ✅ Completa | Hash, sesiones, validación |
| Responsive | ✅ Completa | Mobile-friendly |

---

**Proyecto completado y funcional** ✅
