let currentOrders = [];

async function fetchOrders() {
    try {
        const response = await fetch('/api/orders');
        currentOrders = await response.json();
        renderOrders(currentOrders);
        updateTimers(); // Actualizar inmediatamente después de renderizar
    } catch (e) {
        console.error("Error fetching orders", e);
    }
}

function renderOrders(orders) {
    const container = document.getElementById('orders-container');
    container.innerHTML = '';

    if (orders.length === 0) {
        container.innerHTML = '<p style="font-size: 1.2rem; color: #7f8c8d; grid-column: 1 / -1; text-align: center;">No hay pedidos activos actualmente.</p>';
        return;
    }

    orders.forEach(order => {
        const orderEl = document.createElement('div');
        orderEl.className = 'order-card';

        const itemsHtml = order.items.map(item =>
            `<li><span><strong>${item.quantity}x</strong> ${item.name}</span> <span>${item.price.toFixed(2)}€</span></li>`
        ).join('');

        orderEl.innerHTML = `
            <div class="order-header">
                <span class="order-id">Pedido #${order.id}</span>
                <span class="order-total">${order.total_price.toFixed(2)}€</span>
            </div>
            <div class="order-customer">
                <p><strong>Cliente:</strong> ${order.customer_name}</p>
                <p><strong>Teléfono:</strong> ${order.customer_phone}</p>
                <p><strong>Dirección:</strong> ${order.customer_address}</p>
            </div>
            <ul class="order-items">
                ${itemsHtml}
            </ul>
            <div class="timer-section">
                <div class="progress-container">
                    <div class="progress-bar" id="bar-${order.id}" data-created="${order.created_at}" data-target="${order.target_time}"></div>
                </div>
                <div class="time-left" id="time-${order.id}">Calculando...</div>
                <button class="btn-complete" onclick="completeOrder(${order.id})">Marcar como entregado</button>
            </div>
        `;
        container.appendChild(orderEl);
    });
}

function updateTimers() {
    const bars = document.querySelectorAll('.progress-bar');
    const now = new Date(); // Hora actual del navegador

    bars.forEach(bar => {
        const targetStr = bar.getAttribute('data-target');
        const createdStr = bar.getAttribute('data-created');
        if (!targetStr || !createdStr) return;

        // Reemplazar el espacio por T para formato ISO
        // createdStr por defecto viene en UTC de SQLite (ej. "2024-05-15 09:30:00").
        // Como app.py guardó targetTime en local, vamos a usar simple parsing:
        const targetTime = new Date(targetStr.replace(' ', 'T'));
        const createdTime = new Date(createdStr.replace(' ', 'T') + 'Z'); // UTC

        const diffMs = targetTime - now;

        const id = bar.id.split('-')[1];
        const timeLabel = document.getElementById(`time-${id}`);

        if (diffMs <= 0) {
            bar.style.width = '100%';
            bar.className = 'progress-bar danger';
            timeLabel.innerText = '¡RETRASADO / HORA LLEGADA!';
            timeLabel.style.color = '#e74c3c';
        } else {
            const diffMins = Math.floor(diffMs / 60000);
            const diffSecs = Math.floor((diffMs % 60000) / 1000);

            // Tiempo total es la diferencia entre el target (local) y created (UTC a local)
            // Si hay problemas de zona horaria, podemos asumir al menos una hora (3600000 ms) como fallback.
            let totalMs = targetTime - createdTime;
            if (totalMs <= 0) totalMs = 60 * 60000; // Si falla, 60 mins fallback

            let percentage = ((totalMs - diffMs) / totalMs) * 100;
            if (percentage > 100) percentage = 100;
            if (percentage < 0) percentage = 0;

            bar.style.width = `${100 - percentage}%`; // La barra se vacía

            // 100-percentage es lo que queda.
            const remainingPercent = 100 - percentage;

            if (remainingPercent < 15) {
                bar.className = 'progress-bar danger';
                timeLabel.style.color = '#e74c3c';
            } else if (remainingPercent < 35) {
                bar.className = 'progress-bar warning';
                timeLabel.style.color = '#f39c12';
            } else {
                bar.className = 'progress-bar';
                timeLabel.style.color = '#27ae60';
            }

            timeLabel.innerText = `Quedan ${diffMins}m ${diffSecs}s`;
        }
    });
}

async function completeOrder(id) {
    if (!confirm('¿Estás seguro de marcar este pedido como entregado? Desaparecerá de esta vista.')) return;

    try {
        const response = await fetch(`/api/orders/${id}/complete`, { method: 'POST' });
        if (response.ok) {
            fetchOrders(); // Recargar para ocultarlo
        }
    } catch (e) {
        console.error("Error completing order", e);
    }
}

// Consultar nuevos pedidos de la base de datos cada 5 segundos
setInterval(fetchOrders, 5000);
// Actualizar visualmente la cuenta atrás cada segundo
setInterval(updateTimers, 1000);

// Primera carga de datos al iniciar
fetchOrders();
