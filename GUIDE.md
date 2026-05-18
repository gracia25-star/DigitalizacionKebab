# 📖 Guía de Uso - Mega Döner Kebab

## 🚀 Iniciando por primera vez

### 1. Preparar el entorno

```bash
# Navegar a la carpeta del proyecto
cd MegaDonerKebab

# Instalar dependencias
pip install -r requirements.txt

# Inicializar la base de datos
python init_db.py
```

Verás un mensaje como este:
```
✅ Base de datos inicializada correctamente con el menú de Mega Döner Kebab.

📝 Usuarios de prueba creados:
   Cliente - usuario: cliente_demo, contraseña: cliente123
   Trabajador - usuario: trabajador_demo, contraseña: trabajador123
```

### 2. Ejecutar la aplicación

```bash
python app.py
```

Verás:
```
 * Running on http://127.0.0.1:5000
```

Abre tu navegador en: **http://localhost:5000**

---

## 👤 Usando como Cliente

### Registrarse como Cliente:

1. Haz clic en **"Iniciar Sesión"** (esquina superior derecha)
2. En la página de login, haz clic en **"Registrarse"**
3. Completa el formulario:
   - **Usuario**: elige un nombre único (min. 3 caracteres)
   - **Email**: tu correo electrónico
   - **Contraseña**: contraseña segura (min. 6 caracteres)
   - **Confirmar Contraseña**: repite la contraseña
   - **Tipo de usuario**: selecciona "Cliente - Hacer pedidos"
4. Haz clic en **"Crear Cuenta"**

### O usar la cuenta de prueba:
- **Usuario**: `cliente_demo`
- **Contraseña**: `cliente123`

### Hacer un pedido:

1. Una vez iniciada sesión, verás el menú completo
2. **Explora el menú** por categorías:
   - Menús
   - Dürüms
   - Platos
   - Complementos
   - Bebidas
3. Haz clic en **"Añadir"** en los productos que quieras
4. Haz clic en el **carrito** 🛒 (arriba a la derecha)
5. Ajusta cantidades si es necesario
6. Haz clic en **"Finalizar Pedido"**
7. Completa los datos:
   - **Nombre y Apellidos**
   - **Teléfono**
   - **Dirección de Entrega**
   - **Hora deseada** (mínimo 1 hora en el futuro)
8. Haz clic en **"Confirmar Pedido"**

¡Tu pedido se ha realizado! 🎉

---

## 👷 Usando como Trabajador

### Registrarse como Trabajador:

1. Haz clic en **"Iniciar Sesión"** (esquina superior derecha)
2. En la página de login, haz clic en **"Registrarse"**
3. Completa el formulario:
   - **Usuario**: elige un nombre único (min. 3 caracteres)
   - **Email**: tu correo electrónico
   - **Contraseña**: contraseña segura (min. 6 caracteres)
   - **Confirmar Contraseña**: repite la contraseña
   - **Tipo de usuario**: selecciona "Trabajador - Gestionar productos"
4. Haz clic en **"Crear Cuenta"**

### O usar la cuenta de prueba:
- **Usuario**: `trabajador_demo`
- **Contraseña**: `trabajador123`

Serás redirigido automáticamente al **Panel de Trabajador**.

### Panel de Trabajador:

Verás una interfaz con:
- Tu nombre de usuario (arriba a la derecha)
- Botón "Cerrar Sesión"
- Botón **"➕ Agregar Nuevo Producto"**
- **Grid de productos** mostrando los productos actuales

### Agregar un nuevo producto:

1. Haz clic en **"➕ Agregar Nuevo Producto"**
2. Se abre un formulario modal
3. Completa los campos:
   - **Nombre del Producto** ⭐ (obligatorio)
     - Ej: "Dürüm de Pollo Extra"
   - **Descripción**
     - Ej: "Pollo asado con verduras y salsas especiales"
   - **Precio (€)** ⭐ (obligatorio)
     - Ej: 5.50
   - **Categoría** ⭐ (obligatorio)
     - Puedes usar existentes: Menús, Dürüms, Platos, Complementos, Bebidas
     - O crear una nueva: "Sándwiches", "Postres", etc.
   - **Imagen del Producto**
     - Haz clic para seleccionar una imagen (PNG, JPG, GIF, max 5MB)
4. Haz clic en **"Guardar Producto"**

### Editar un producto:

1. En el grid de productos, busca el que quieras editar
2. Haz clic en el botón **"✏️ Editar"** (azul)
3. Se abrirá el formulario con los datos actuales
4. Modifica los campos que necesites
5. Si quieres cambiar la imagen:
   - Haz clic en "📷 Haz clic para seleccionar imagen"
   - Selecciona una nueva imagen
6. Haz clic en **"Guardar Producto"**

### Eliminar un producto:

1. En el grid de productos, busca el que quieras eliminar
2. Haz clic en el botón **"🗑️ Eliminar"** (rojo)
3. Se te pedirá confirmación
4. Haz clic en "Aceptar"

⚠️ **Nota**: Esta acción no se puede deshacer

---

## 🔄 Flujo completo de uso

### Escenario 1: Cliente hace un pedido

```
1. Visita http://localhost:5000
   ↓
2. Haz clic en "Iniciar Sesión"
   ↓
3. Registrate como cliente (o usa cliente_demo)
   ↓
4. Explora el menú
   ↓
5. Agrega productos al carrito
   ↓
6. Haz clic en el carrito 🛒
   ↓
7. Completa datos de envío
   ↓
8. Selecciona hora de entrega
   ↓
9. ¡Pedido realizado! 🎉
```

### Escenario 2: Trabajador gestiona productos

```
1. Visita http://localhost:5000
   ↓
2. Registrate como trabajador (o usa trabajador_demo)
   ↓
3. Automáticamente irás al Panel de Trabajador
   ↓
4. Haz clic en "Agregar Nuevo Producto"
   ↓
5. Completa el formulario con datos del producto
   ↓
6. Sube una imagen (opcional pero recomendado)
   ↓
7. Haz clic en "Guardar Producto"
   ↓
8. El producto aparece en el menú para los clientes
   ↓
9. Puedes editar o eliminar en cualquier momento
```

---

## 💡 Consejos y trucos

### Para Clientes:

- 📱 La app es responsive, úsala desde tu teléfono
- 🛒 El carrito se guarda en tu navegador (no se pierde al recargar)
- ⏰ La hora mínima de entrega es 1 hora desde ahora
- 💬 Sé específico en la dirección para que el repartidor te encuentre

### Para Trabajadores:

- 🖼️ Las imágenes mejoran mucho la apariencia del menú
- 📸 Sube fotos de buena calidad (mínimo 300x300px)
- 📝 Una buena descripción ayuda a vender más
- 🏷️ Organiza los productos por categorías lógicas
- 🔄 Puedes cambiar precios fácilmente editando el producto

---

## 🆘 Solución rápida de problemas

### "No puedo iniciar sesión"
- Verifica que escribiste correctamente el usuario y contraseña
- Usa las cuentas de prueba si es la primera vez
- Si olvidaste la contraseña, crea una nueva cuenta

### "La imagen no aparece en mi producto"
- Recarga la página (Ctrl+F5)
- Asegúrate de que la imagen es menor a 5MB
- Formatos permitidos: PNG, JPG, GIF
- Intenta con una imagen más pequeña

### "Me dice 'Acceso denegado'"
- Estás intentando acceder a área de trabajador como cliente
- Crea cuenta como trabajador o usa `trabajador_demo`

### "Las imágenes de productos no se muestran"
- Verifica que la carpeta `static/uploads/` existe
- Si no existe, créala manualmente
- Reinicia la aplicación

### "Error: La base de datos no existe"
- Ejecuta: `python init_db.py`

---

## 📞 Información útil

- **Puerto**: 5000 (si está ocupado, cambiar en `app.py`)
- **Base de datos**: SQLite (`doner.db`)
- **Carpeta de imágenes**: `static/uploads/`
- **Navegador recomendado**: Chrome, Firefox, Edge (actualizado)

---

## ✅ Checklist antes de producción

- [ ] Cambiar `app.secret_key` en `app.py` con una clave segura
- [ ] Eliminar las cuentas de prueba
- [ ] Verificar que los productos tienen imágenes de calidad
- [ ] Probar pedidos completos como cliente
- [ ] Probar agregar/editar/eliminar productos como trabajador
- [ ] Hacer copia de seguridad de la base de datos
- [ ] Documentar cualquier cambio personalizado

---

¡Disfruta usando Mega Döner Kebab! 🌮
