# ⚡ Quick Start - Inicio Rápido

## Instalación (30 segundos)

```bash
# 1. Navega a la carpeta
cd "MegaDonerKebab"

# 2. Instala dependencias
pip install -r requirements.txt

# 3. Inicializa la BD
python init_db.py

# 4. Ejecuta la app
python app.py
```

## Acceso (inmediato)

Abre tu navegador en: **http://localhost:5000**

---

## Credenciales de Prueba

### Cuenta Cliente:
```
Usuario: cliente_demo
Contraseña: cliente123
```

### Cuenta Trabajador:
```
Usuario: trabajador_demo
Contraseña: trabajador123
```

---

## Lo que puedes hacer

### Con Cliente (cliente_demo):
1. Ver menú de productos
2. Agregar al carrito
3. Hacer pedidos con hora

### Con Trabajador (trabajador_demo):
1. Ir a panel de administrador
2. Agregar nuevos productos
3. Editar productos existentes
4. Cambiar fotos de productos
5. Eliminar productos

---

## Estructura Rápida

```
Proyecto/
├── app.py                  ← Aplicación principal
├── init_db.py             ← Crear/inicializar base de datos
├── requirements.txt       ← Librerías necesarias
├── templates/
│   ├── index.html        ← Página de clientes
│   ├── login.html        ← Login
│   ├── register.html     ← Registro
│   └── worker.html       ← Panel trabajador
├── static/
│   ├── css/              ← Estilos
│   ├── js/               ← JavaScript
│   └── uploads/          ← Imágenes de productos
└── doner.db             ← Base de datos (se crea)
```

---

## Troubleshooting Rápido

| Problema | Solución |
|---|---|
| "No existe doner.db" | Ejecutar: `python init_db.py` |
| "Puerto 5000 en uso" | Cambiar puerto en app.py |
| "Las imágenes no se ven" | Recargar Ctrl+F5 |
| "Error de login" | Usar credenciales de prueba |

---

## Cambios Realizados ✅

- ✅ Sistema de autenticación con 2 roles
- ✅ Panel de administración para trabajadores
- ✅ Gestión completa de productos (CRUD)
- ✅ Carga de imágenes de productos
- ✅ Carrito de compras mejorado
- ✅ Base de datos actualizada
- ✅ Interfaz de usuario renovada

---

## Próximas mejoras opcionales

- [ ] Panel de administración para ver pedidos (incluido admin_app.py)
- [ ] Sistema de notificaciones por email
- [ ] Historial de pedidos del cliente
- [ ] Descuentos y promociones
- [ ] Historial de cambios de productos
- [ ] Sistema de ratings de productos
- [ ] Métodos de pago integrados

---

¡Ya está listo! Disfruta 🌮
