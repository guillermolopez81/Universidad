"""
Clase Articulo para incluir los productos en el inventario
"""

class Articulo:
    def __init__(self, codigo, nombre, descripcion, unidad_medida):
        """
        Inicia  un artículo del inventario
        
        Args:
            codigo (str): Código único del artículo
            nombre (str): Nombre del artículo
            descripcion (str): Descripción del artículo
            unidad_medida (str): medida ( unidad.)
        """
        self.codigo = codigo
        self.nombre = nombre
        self.descripcion = descripcion
        self.unidad_medida = unidad_medida
        self.cantidad = 0.0
    
    def __str__(self):
        return f"Artículo: {self.nombre} ({self.codigo}) - {self.cantidad} {self.unidad_medida}"
    
    def __repr__(self):
        return f"Articulo(codigo='{self.codigo}', nombre='{self.nombre}', cantidad={self.cantidad})"
    
    def actualizar_cantidad(self, nueva_cantidad):
        """
        Actualiza la cantidad del artículo
        
        Args:
            nueva_cantidad (float): Nueva cantidad del artículo
        """
        if nueva_cantidad < 0:
            raise ValueError("La cantidad no puede ser negativa")
        self.cantidad = nueva_cantidad
    
    def obtener_info(self):
        """
        Retorna información completa del artículo
        
        Returns:
            dict: Diccionario con la información del artículo
        """
        return {
            'codigo': self.codigo,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'unidad_medida': self.unidad_medida,
            'cantidad': self.cantidad
        }