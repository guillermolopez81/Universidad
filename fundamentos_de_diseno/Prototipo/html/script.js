// Sistema de Inventarios - JavaScript Principal

// Simulación de datos del inventario
let inventario = {
    articulos: [],
    movimientos: [],
    nextId: 1
};

// Cargar datos del localStorage si existen
function cargarDatos() {
    const datosGuardados = localStorage.getItem('inventarioData');
    if (datosGuardados) {
        inventario = JSON.parse(datosGuardados);
    }
}

// Guardar datos en localStorage
function guardarDatos() {
    localStorage.setItem('inventarioData', JSON.stringify(inventario));
}

// Generar ID único
function generarId() {
    return inventario.nextId++;
}

// Mostrar alertas
function mostrarAlerta(mensaje, tipo = 'info') {
    const alertContainer = document.getElementById('alert-container');
    if (!alertContainer) return;
    
    const alert = document.createElement('div');
    alert.className = `alert alert-${tipo}`;
    alert.innerHTML = `
        ${mensaje}
        <button onclick="this.parentElement.remove()" style="float: right; background: none; border: none; font-size: 1.2em; cursor: pointer;">&times;</button>
    `;
    
    alertContainer.appendChild(alert);
    
    // Auto-remover después de 5 segundos
    setTimeout(() => {
        if (alert.parentElement) {
            alert.remove();
        }
    }, 5000);
}

// Validar formularios
function validarCampo(valor, nombre) {
    if (!valor || valor.trim() === '') {
        mostrarAlerta(`El campo ${nombre} es obligatorio`, 'error');
        return false;
    }
    return true;
}

// Funciones para artículos
function agregarArticulo(codigo, nombre, descripcion, unidadMedida) {
    // Validaciones
    if (!validarCampo(codigo, 'Código')) return false;
    if (!validarCampo(nombre, 'Nombre')) return false;
    if (!validarCampo(unidadMedida, 'Unidad de Medida')) return false;
    
    // Verificar si ya existe el código
    if (inventario.articulos.find(art => art.codigo === codigo.toUpperCase())) {
        mostrarAlerta(`Ya existe un artículo con el código ${codigo}`, 'error');
        return false;
    }
    
    const nuevoArticulo = {
        id: generarId(),
        codigo: codigo.toUpperCase(),
        nombre: nombre.trim(),
        descripcion: descripcion.trim(),
        unidadMedida: unidadMedida.trim(),
        cantidad: 0
    };
    
    inventario.articulos.push(nuevoArticulo);
    guardarDatos();
    mostrarAlerta(`Artículo '${nombre}' agregado exitosamente`, 'success');
    return true;
}

function obtenerArticulo(codigo) {
    return inventario.articulos.find(art => art.codigo === codigo.toUpperCase());
}

function actualizarStockArticulo(codigo, nuevaCantidad) {
    const articulo = obtenerArticulo(codigo);
    if (articulo) {
        articulo.cantidad = nuevaCantidad;
        guardarDatos();
        return true;
    }
    return false;
}

// Funciones para movimientos
function registrarMovimiento(codigoArticulo, tipo, cantidad, motivo, usuario = 'Usuario') {
    const movimiento = {
        id: generarId(),
        codigoArticulo: codigoArticulo.toUpperCase(),
        tipo: tipo,
        cantidad: parseFloat(cantidad),
        motivo: motivo.trim(),
        usuario: usuario,
        fechaHora: new Date().toISOString()
    };
    
    inventario.movimientos.push(movimiento);
    guardarDatos();
    return movimiento;
}

function entradaMercancia(codigo, cantidad, motivo = 'Entrada de mercancía') {
    const articulo = obtenerArticulo(codigo);
    if (!articulo) {
        mostrarAlerta(`No existe un artículo con el código ${codigo}`, 'error');
        return false;
    }
    
    const cantidadNum = parseFloat(cantidad);
    if (isNaN(cantidadNum) || cantidadNum <= 0) {
        mostrarAlerta('La cantidad debe ser un número mayor a 0', 'error');
        return false;
    }
    
    const stockAnterior = articulo.cantidad;
    const nuevoStock = stockAnterior + cantidadNum;
    
    actualizarStockArticulo(codigo, nuevoStock);
    registrarMovimiento(codigo, 'ENTRADA', cantidadNum, motivo);
    
    mostrarAlerta(`Entrada registrada exitosamente. Stock: ${stockAnterior} → ${nuevoStock} ${articulo.unidadMedida}`, 'success');
    return true;
}

function salidaMercancia(codigo, cantidad, motivo = 'Salida de mercancía') {
    const articulo = obtenerArticulo(codigo);
    if (!articulo) {
        mostrarAlerta(`No existe un artículo con el código ${codigo}`, 'error');
        return false;
    }
    
    const cantidadNum = parseFloat(cantidad);
    if (isNaN(cantidadNum) || cantidadNum <= 0) {
        mostrarAlerta('La cantidad debe ser un número mayor a 0', 'error');
        return false;
    }
    
    if (cantidadNum > articulo.cantidad) {
        mostrarAlerta(`Stock insuficiente. Disponible: ${articulo.cantidad} ${articulo.unidadMedida}`, 'error');
        return false;
    }
    
    const stockAnterior = articulo.cantidad;
    const nuevoStock = stockAnterior - cantidadNum;
    
    actualizarStockArticulo(codigo, nuevoStock);
    registrarMovimiento(codigo, 'SALIDA', cantidadNum, motivo);
    
    mostrarAlerta(`Salida registrada exitosamente. Stock: ${stockAnterior} → ${nuevoStock} ${articulo.unidadMedida}`, 'success');
    return true;
}

// Funciones de visualización
function mostrarArticulos(contenedorId) {
    const contenedor = document.getElementById(contenedorId);
    if (!contenedor) return;
    
    if (inventario.articulos.length === 0) {
        contenedor.innerHTML = '<p>No hay artículos registrados en el inventario.</p>';
        return;
    }
    
    let html = `
        <table>
            <thead>
                <tr>
                    <th>Código</th>
                    <th>Nombre</th>
                    <th>Descripción</th>
                    <th>Stock</th>
                    <th>Unidad</th>
                    <th>Acciones</th>
                </tr>
            </thead>
            <tbody>
    `;
    
    inventario.articulos.forEach(articulo => {
        html += `
            <tr>
                <td>${articulo.codigo}</td>
                <td>${articulo.nombre}</td>
                <td>${articulo.descripcion}</td>
                <td>${articulo.cantidad}</td>
                <td>${articulo.unidadMedida}</td>
                <td>
                    <button class="btn btn-secondary" onclick="verDetalleArticulo('${articulo.codigo}')">Ver</button>
                </td>
            </tr>
        `;
    });
    
    html += '</tbody></table>';
    contenedor.innerHTML = html;
}

function mostrarMovimientos(contenedorId, codigoArticulo = null) {
    const contenedor = document.getElementById(contenedorId);
    if (!contenedor) return;
    
    let movimientos = inventario.movimientos;
    if (codigoArticulo) {
        movimientos = movimientos.filter(mov => mov.codigoArticulo === codigoArticulo.toUpperCase());
    }
    
    if (movimientos.length === 0) {
        contenedor.innerHTML = '<p>No hay movimientos registrados.</p>';
        return;
    }
    
    let html = `
        <table>
            <thead>
                <tr>
                    <th>Fecha/Hora</th>
                    <th>Artículo</th>
                    <th>Tipo</th>
                    <th>Cantidad</th>
                    <th>Motivo</th>
                    <th>Usuario</th>
                </tr>
            </thead>
            <tbody>
    `;
    
    movimientos.sort((a, b) => new Date(b.fechaHora) - new Date(a.fechaHora));
    
    movimientos.forEach(mov => {
        const fecha = new Date(mov.fechaHora).toLocaleString();
        const tipoClass = mov.tipo === 'ENTRADA' ? 'success' : 'danger';
        
        html += `
            <tr>
                <td>${fecha}</td>
                <td>${mov.codigoArticulo}</td>
                <td><span class="btn btn-${tipoClass}" style="padding: 2px 8px; font-size: 0.8em;">${mov.tipo}</span></td>
                <td>${mov.cantidad}</td>
                <td>${mov.motivo}</td>
                <td>${mov.usuario}</td>
            </tr>
        `;
    });
    
    html += '</tbody></table>';
    contenedor.innerHTML = html;
}

function actualizarEstadisticas() {
    const totalArticulos = document.getElementById('total-articulos');
    const totalMovimientos = document.getElementById('total-movimientos');
    const articulosBajoStock = document.getElementById('articulos-bajo-stock');
    
    if (totalArticulos) {
        totalArticulos.textContent = inventario.articulos.length;
    }
    
    if (totalMovimientos) {
        totalMovimientos.textContent = inventario.movimientos.length;
    }
    
    if (articulosBajoStock) {
        const bajoStock = inventario.articulos.filter(art => art.cantidad < 10).length;
        articulosBajoStock.textContent = bajoStock;
    }
}

// Función para ver detalle de artículo
function verDetalleArticulo(codigo) {
    const articulo = obtenerArticulo(codigo);
    if (!articulo) return;
    
    const movimientosArticulo = inventario.movimientos.filter(mov => mov.codigoArticulo === codigo);
    
    let detalleHtml = `
        <div class="card">
            <div class="card-header">
                <h3>Detalle del Artículo: ${articulo.nombre}</h3>
            </div>
            <p><strong>Código:</strong> ${articulo.codigo}</p>
            <p><strong>Descripción:</strong> ${articulo.descripcion}</p>
            <p><strong>Stock Actual:</strong> ${articulo.cantidad} ${articulo.unidadMedida}</p>
            <p><strong>Total de Movimientos:</strong> ${movimientosArticulo.length}</p>
        </div>
    `;
    
    // Mostrar en modal o nueva ventana (simplificado)
    const nuevaVentana = window.open('', '_blank', 'width=600,height=400');
    nuevaVentana.document.write(`
        <html>
            <head>
                <title>Detalle - ${articulo.nombre}</title>
                <link rel="stylesheet" href="styles.css">
            </head>
            <body>
                <div class="container">
                    ${detalleHtml}
                    <button onclick="window.close()" class="btn">Cerrar</button>
                </div>
            </body>
        </html>
    `);
}

// Función para limpiar formularios
function limpiarFormulario(formId) {
    const form = document.getElementById(formId);
    if (form) {
        form.reset();
    }
}

// Función para generar reporte básico
function generarReporte() {
    const fecha = new Date().toLocaleString();
    let reporte = `
        <div class="card">
            <div class="card-header">
                <h3>Reporte de Inventario - ${fecha}</h3>
            </div>
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-number">${inventario.articulos.length}</div>
                    <div class="stat-label">Total Artículos</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">${inventario.movimientos.length}</div>
                    <div class="stat-label">Total Movimientos</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">${inventario.articulos.filter(art => art.cantidad < 10).length}</div>
                    <div class="stat-label">Artículos Bajo Stock</div>
                </div>
            </div>
        </div>
    `;
    
    return reporte;
}

// Inicialización
document.addEventListener('DOMContentLoaded', function() {
    cargarDatos();
    actualizarEstadisticas();
    
    // Auto-actualizar estadísticas cada 30 segundos
    setInterval(actualizarEstadisticas, 30000);
});

// Función para exportar datos (simulación)
function exportarDatos() {
    const datos = JSON.stringify(inventario, null, 2);
    const blob = new Blob([datos], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    
    const a = document.createElement('a');
    a.href = url;
    a.download = `inventario_${new Date().toISOString().split('T')[0]}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    
    mostrarAlerta('Datos exportados exitosamente', 'success');
}

// Función para importar datos (simulación)
function importarDatos(event) {
    const file = event.target.files[0];
    if (!file) return;
    
    const reader = new FileReader();
    reader.onload = function(e) {
        try {
            const datos = JSON.parse(e.target.result);
            inventario = datos;
            guardarDatos();
            mostrarAlerta('Datos importados exitosamente', 'success');
            location.reload(); // Recargar para mostrar los nuevos datos
        } catch (error) {
            mostrarAlerta('Error al importar los datos. Verifique el formato del archivo.', 'error');
        }
    };
    reader.readAsText(file);
}