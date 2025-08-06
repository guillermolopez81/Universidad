"""
Clase MovimientoInventario para registrar entradas y salidas de mercancía
"""

from datetime import datetime
from enum import Enum

class TipoMovimiento(Enum):
    ENTRADA = "ENTRADA"
    SALIDA = "SALIDA"

class MovimientoInventario:
    def __init__(self, codigo_articulo, tipo_movimiento, cantidad, motivo="", usuario="Sistema"):
        """
        Inicializa un movimiento de inventario
        
        Args:
            codigo_articulo (str): Código del artículo afectado
            tipo_movimiento (TipoMovimiento): Tipo de movimiento (ENTRADA o SALIDA)
            cantidad (float): Cantidad del movimiento
            motivo (str): Motivo del movimiento
            usuario (str): Usuario que realiza el movimiento
        """
        self.id = self._generar_id()
        self.codigo_articulo = codigo_articulo
        self.tipo_movimiento = tipo_movimiento
        self.cantidad = cantidad
        self.motivo = motivo
        self.usuario = usuario
        self.fecha_hora = datetime.now()
    
    def _generar_id(self):
        """
        Genera un ID único para el movimiento basado en timestamp
        
        Returns:
            str: ID único del movimiento
        """
        return f"MOV_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
    
    def __str__(self):
        return f"{self.tipo_movimiento.value}: {self.cantidad} - {self.codigo_articulo} ({self.fecha_hora.strftime('%Y-%m-%d %H:%M:%S')})"
    
    def __repr__(self):
        return f"MovimientoInventario(id='{self.id}', tipo='{self.tipo_movimiento.value}', cantidad={self.cantidad})"
    
    def obtener_info(self):
        """
        Retorna información completa del movimiento
        
        Returns:
            dict: Diccionario con la información del movimiento
        """
        return {
            'id': self.id,
            'codigo_articulo': self.codigo_articulo,
            'tipo_movimiento': self.tipo_movimiento.value,
            'cantidad': self.cantidad,
            'motivo': self.motivo,
            'usuario': self.usuario,
            'fecha_hora': self.fecha_hora.strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def es_entrada(self):
        """
        Verifica si el movimiento es una entrada
        
        Returns:
            bool: True si es entrada, False si es salida
        """
        return self.tipo_movimiento == TipoMovimiento.ENTRADA
    
    def es_salida(self):
        """
        Verifica si el movimiento es una salida
        
        Returns:
            bool: True si es salida, False si es entrada
        """
        return self.tipo_movimiento == TipoMovimiento.SALIDA