let cart = [];

function addToCart(id, name, price) {
    const existingItem = cart.find(item => item.id === id);
    if (existingItem) {
        existingItem.quantity += 1;
    } else {
        cart.push({ id, name, price, quantity: 1 });
    }
    updateCartUI();
    
    const cartIcon = document.getElementById('cart-toggle');
    cartIcon.style.transform = 'scale(1.2)';
    setTimeout(() => cartIcon.style.transform = 'scale(1)', 200);
}

function removeFromCart(id) {
    const itemIndex = cart.findIndex(item => item.id === id);
    if (itemIndex > -1) {
        if (cart[itemIndex].quantity > 1) {
            cart[itemIndex].quantity -= 1;
        } else {
            cart.splice(itemIndex, 1);
        }
        updateCartUI();
    }
}

function updateCartUI() {
    const cartCount = document.getElementById('cart-count');
    const cartItems = document.getElementById('cart-items');
    const cartTotalElement = document.getElementById('cart-total-price');
    
    let totalItems = 0;
    let totalPrice = 0;
    
    cartItems.innerHTML = '';
    
    if (cart.length === 0) {
        cartItems.innerHTML = '<p style="color: #a0a5b1; text-align: center; margin-top: 20px;">El carrito está vacío</p>';
    } else {
        cart.forEach(item => {
            totalItems += item.quantity;
            totalPrice += item.price * item.quantity;
            
            const itemElement = document.createElement('div');
            itemElement.className = 'cart-item';
            itemElement.innerHTML = `
                <div class="cart-item-info">
                    <h5>${item.name}</h5>
                    <span class="cart-item-price">${(item.price * item.quantity).toFixed(2)}€</span>
                </div>
                <div class="cart-controls">
                    <button onclick="removeFromCart(${item.id})">-</button>
                    <span>${item.quantity}</span>
                    <button onclick="addToCart(${item.id}, '${item.name}', ${item.price})">+</button>
                </div>
            `;
            cartItems.appendChild(itemElement);
        });
    }
    
    cartCount.innerText = totalItems;
    cartTotalElement.innerText = totalPrice.toFixed(2);
}

document.getElementById('cart-toggle').addEventListener('click', () => {
    document.getElementById('cart-sidebar').classList.add('active');
});

document.getElementById('close-cart').addEventListener('click', () => {
    document.getElementById('cart-sidebar').classList.remove('active');
});

document.getElementById('btn-checkout').addEventListener('click', () => {
    if (cart.length === 0) {
        alert('Añade algunos productos a tu pedido primero.');
        return;
    }
    
    // Verificar si el usuario está logueado
    if (!window.location.pathname.includes('cliente') && !document.querySelector('.user-info')) {
        // Si no está logueado, redirigir a login
        const loginBtn = document.querySelector('a[href*="login"]');
        if (loginBtn) {
            window.location.href = loginBtn.href;
            return;
        }
    }
    
    document.getElementById('cart-sidebar').classList.remove('active');
    document.getElementById('checkout-modal').classList.add('active');
});

document.getElementById('btn-cancel-checkout').addEventListener('click', () => {
    document.getElementById('checkout-modal').classList.remove('active');
});

document.getElementById('checkout-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const name = document.getElementById('cust-name').value;
    const phone = document.getElementById('cust-phone').value;
    const address = document.getElementById('cust-address').value;
    const timeStr = document.getElementById('cust-target-time').value;
    
    // Validación de la hora (mínimo 1 hora de diferencia)
    if (timeStr) {
        const now = new Date();
        const targetDate = new Date();
        const [hours, minutes] = timeStr.split(':');
        targetDate.setHours(parseInt(hours), parseInt(minutes), 0, 0);
        
        // Si la hora pedida es menor a la actual + 59 minutos (damos 1 minuto de gracia)
        if (targetDate < new Date(now.getTime() + 59 * 60000)) {
            alert('La hora de entrega debe ser al menos 1 hora después de la hora actual.');
            return;
        }
    } else {
        alert('Por favor, selecciona una hora de entrega.');
        return;
    }
    
    const orderData = {
        name,
        phone,
        address,
        target_time: timeStr,
        cart
    };
    
    const btn = e.target.querySelector('button[type="submit"]');
    btn.innerText = 'Procesando...';
    btn.disabled = true;
    
    try {
        const response = await fetch('/api/order', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(orderData)
        });
        
        const data = await response.json();
        
        if (response.ok && data.success) {
            alert(`¡Pedido realizado con éxito! Tu número de pedido es #${data.order_id}`);
            cart = [];
            updateCartUI();
            document.getElementById('checkout-modal').classList.remove('active');
            e.target.reset();
        } else {
            alert('Error al realizar el pedido: ' + (data.error || 'Desconocido'));
        }
    } catch (error) {
        alert('Error de conexión.');
        console.error(error);
    } finally {
        btn.innerText = 'Confirmar Pedido';
        btn.disabled = false;
    }
});

updateCartUI();
