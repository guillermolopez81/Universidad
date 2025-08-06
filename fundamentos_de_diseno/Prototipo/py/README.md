# Sistema de Inventarios importadora - Prototipo

Un sistema básico de gestión de inventarios desarrollado en Python con programación orientada a objetos, adicional el backend esta hecho en html ya que me facilito este diseño para este prototipo

## 1. Descripción

Este prototipo permite gestionar un inventario básico con las siguientes funciones:
- Registro de artículos con código, nombre, descripción y unidad (medida)
- Control de entradas y salidas de mercancía para tener control de los mismos
- Seguimiento de movimientos de inventario hacer un trazabilidad sencilla
- Consultas de estado inventarios y reportes
- **Generación de reportes en PDF** me base en repositorios de gente mas dura que uno para hacer esto posible

## 2.Estructura de este prototipo
segun en las calses organize el codigo de aucuerdo a la estructura de esta manera separe las clases como nos recomendo

```
prototipo-inventarios/
│
├── py/
│   ├── __pycache__/             # cahce de  Python al ejecutar 
│   ├── articulo.py              # Clase Articulo - Representa los productos
│   ├── movimiento_inventario.py# Clase MovimientoInventario - Registra entradas/salidas
│   ├── inventario.py           # Clase Inventario - Núcleo del sistema
│   ├── reporte_pdf.py          # Generador de reportes en PDF
│   ├── main.py                 # Archivo principal con interfaz de usuario
│   ├── requirements.txt        # Dependencias del proyecto
│   └── README.md               # Documentación del proyecto
│
├── html/
│   ├── index.html               # Página principal del sistema de inventario
│   ├── agregar-articulo.html    # Formulario para agregar artículos
│   ├── consultar-inventario.html # Consulta de artículos en inventario
│   ├── entrada-mercancia.html   # Registro de entradas de mercancía
│   ├── salida-mercancia.html    # Registro de salidas de mercancía
│   ├── generar-reportes.html    # Página para generar reportes
│   ├── ver-movimientos.html     # Consulta de movimientos de inventario
│   ├── listar-articulos.html    # Listado general de artículos
│   ├── script.js                # Lógica JavaScript principal
│   └── styles.css               # Estilos CSS del sitio web

```

##  estructura  del Sistema

### 1. Clase `Articulo` (articulo.py)
Es el  producto en el inventario.

**Atributos:**
- `codigo`: Código único del artículo
- `nombre`: Nombre del artículo
- `descripcion`: Descripción del artículo
- `unidad_medida`: Unidad de medida (kg, unidades, litros, etc.)
- `cantidad`: Cantidad actual en stock

**Métodos principales:**
- `actualizar_cantidad(nueva_cantidad)`: Actualiza el stock
- `obtener_info()`: Retorna información completa del artículo

### 2. Clase `MovimientoInventario` (movimiento_inventario.py)
Registra  entrada y salida de mercancía.

**Atributos:**
- `id`: Identificador único del movimiento
- `codigo_articulo`: Código del artículo afectado
- `tipo_movimiento`: ENTRADA o SALIDA
- `cantidad`: Cantidad del movimiento
- `motivo`: Razón del movimiento
- `usuario`: Usuario que realiza la operación
- `fecha_hora`: Timestamp del movimiento

**Métodos principales:**
- `es_entrada()`: Verifica si es una entrada
- `es_salida()`: Verifica si es una salida
- `obtener_info()`: Retorna información completa del movimiento

### 3. Clase `Inventario` (inventario.py)
Gestiona todos los artículos y movimientos.

**Métodos principales:**
- `agregar_articulo()`: Registra un nuevo artículo
- `entrada_mercancia()`: Procesa entrada de stock
- `salida_mercancia()`: Procesa salida de stock
- `obtener_articulo()`: Busca un artículo por código
- `listar_articulos()`: Lista todos los artículos
- `obtener_stock_actual()`: Consulta stock de un artículo
- `obtener_movimientos_articulo()`: Historial de movimientos
- `generar_reporte_inventario()`: Genera reporte completo

### 4. Clase `GeneradorReportePDF` (reporte_pdf.py)
Genera reportes PDF.

**Métodos principales:**
- `generar_reporte_inventario()`: Crea reporte completo del inventario
- `generar_reporte_articulo()`: Crea reporte detallado de un artículo específico

**Características de los reportes:**
- Formato profesional con tablas y estilos
- Información completa del inventario
- Historial de movimientos
- Generación automática de nombres de archivo

### 5. Sistema Principal (main.py)
Menu principal.

**Funcionalidades:**
1. Agregar nuevo artículo
2. Entrada de mercancía
3. Salida de mercancía
4. Consultar stock de artículo
5. Listar todos los artículos
6. Ver movimientos de un artículo
7. Ver todos los movimientos
8. Generar reporte de inventario
9. **Generar reporte PDF completo**
10. **Generar reporte PDF de artículo**
11. Salir del sistema

##  Instalación

### Requisitos
- Python 3.6 o superior
- pip (gestor de paquetes de Python)

### Instalación
1. Descargar los archivos del proyecto
2. Instalar Python
3. Instala reportlab
   ```bash
   pip install -r requirements.txt
   ```
   O instala manualmente:
   ```bash
   pip install reportlab   #este paquet fue una guia de como instalar Pdf
   ```

### Ejecución
```bash
python main.py # en modo consola
index.html     # en modo visual

##  Autor

Prototipo es un desarrollo en Python y Html

##  Licencia

Este es un proyecto de prototipo educativo.