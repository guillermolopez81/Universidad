"""
Clase Inventario para gestionar el  inventarios
"""

from articulo import Articulo
from movimiento_inventario import MovimientoInventario, TipoMovimiento
from datetime import datetime

class Inventario:
    def __init__(self):
        """
        Inicializa el sistema de inventario
        """
        self.articulos = {}  # Diccionario con código como clave y Articulo como valor
        self.movimientos = []  # Lista de todos los movimientos
    
    def agregar_articulo(self, codigo, nombre, descripcion, unidad_medida):
        """
        Agrega un nuevo artículo al inventario
        
        Args:
            codigo (str): Código único del artículo
            nombre (str): Nombre del artículo
            descripcion (str): Descripción del artículo
            unidad_medida (str): Unidad de medida
            
        Returns:
            bool: True si se agregó exitosamente, False si ya existe
        """
        if codigo in self.articulos:
            return False
        
        nuevo_articulo = Articulo(codigo, nombre, descripcion, unidad_medida)
        self.articulos[codigo] = nuevo_articulo
        return True
    
    def obtener_articulo(self, codigo):
        """
        Obtiene un artículo por su código
        
        Args:
            codigo (str): Código del artículo
            
        Returns:
            Articulo: El artículo encontrado o None si no existe
        """
        return self.articulos.get(codigo)
    
    def entrada_mercancia(self, codigo_articulo, cantidad, motivo="Entrada de mercancía", usuario="Sistema"):
        """
        Registra una entrada de mercancía
        
        Args:
            codigo_articulo (str): Código del artículo
            cantidad (float): Cantidad a ingresar
            motivo (str): Motivo de la entrada
            usuario (str): Usuario que realiza la operación
            
        Returns:
            bool: True si la operación fue exitosa, False en caso contrario
        """
        if codigo_articulo not in self.articulos:
            return False
        
        if cantidad <= 0:
            return False
        
        articulo = self.articulos[codigo_articulo]
        nueva_cantidad = articulo.cantidad + cantidad
        articulo.actualizar_cantidad(nueva_cantidad)
        
        # Registrar el movimiento
        movimiento = MovimientoInventario(
            codigo_articulo, 
            TipoMovimiento.ENTRADA, 
            cantidad, 
            motivo, 
            usuario
        )
        self.movimientos.append(movimiento)
        
        return True
    
    def salida_mercancia(self, codigo_articulo, cantidad, motivo="Salida de mercancía", usuario="Sistema"):
        """
        Registra una salida de mercancía
        
        Args:
            codigo_articulo (str): Código del artículo
            cantidad (float): Cantidad a retirar
            motivo (str): Motivo de la salida
            usuario (str): Usuario que realiza la operación
            
        Returns:
            bool: True si la operación fue exitosa, False en caso contrario
        """
        if codigo_articulo not in self.articulos:
            return False
        
        if cantidad <= 0:
            return False
        
        articulo = self.articulos[codigo_articulo]
        
        # Verificar que hay suficiente stock
        if articulo.cantidad < cantidad:
            return False
        
        nueva_cantidad = articulo.cantidad - cantidad
        articulo.actualizar_cantidad(nueva_cantidad)
        
        # Registrar el movimiento
        movimiento = MovimientoInventario(
            codigo_articulo, 
            TipoMovimiento.SALIDA, 
            cantidad, 
            motivo, 
            usuario
        )
        self.movimientos.append(movimiento)
        
        return True
    
    def listar_articulos(self):
        """
        Lista todos los artículos del inventario
        
        Returns:
            list: Lista de artículos
        """
        return list(self.articulos.values())
    
    def obtener_stock_actual(self, codigo_articulo):
        """
        Obtiene el stock actual de un artículo
        
        Args:
            codigo_articulo (str): Código del artículo
            
        Returns:
            float: Cantidad actual o None si no existe el artículo
        """
        articulo = self.obtener_articulo(codigo_articulo)
        return articulo.cantidad if articulo else None
    
    def obtener_movimientos_articulo(self, codigo_articulo):
        """
        Obtiene todos los movimientos de un artículo específico
        
        Args:
            codigo_articulo (str): Código del artículo
            
        Returns:
            list: Lista de movimientos del artículo
        """
        return [mov for mov in self.movimientos if mov.codigo_articulo == codigo_articulo]
    
    def obtener_todos_movimientos(self):
        """
        Obtiene todos los movimientos del inventario
        
        Returns:
            list: Lista de todos los movimientos
        """
        return self.movimientos.copy()
    
    def generar_reporte_inventario(self):
        """
        Genera un reporte completo del inventario
        
        Returns:
            dict: Reporte con información del inventario
        """
        total_articulos = len(self.articulos)
        total_movimientos = len(self.movimientos)
        
        articulos_info = []
        for articulo in self.articulos.values():
            articulos_info.append(articulo.obtener_info())
        
        return {
            'fecha_reporte': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'total_articulos': total_articulos,
            'total_movimientos': total_movimientos,
            'articulos': articulos_info
        }