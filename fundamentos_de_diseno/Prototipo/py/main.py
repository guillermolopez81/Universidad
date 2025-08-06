"""
Archivo principal del sistema de inventarios importadora este seria el panel principal
"""

from inventario import Inventario
from movimiento_inventario import TipoMovimiento
from reporte_pdf import GeneradorReportePDF
import os

class SistemaInventario:
    def __init__(self):
        self.inventario = Inventario()
        self.usuario_actual = "Administrador"
        self.generador_pdf = GeneradorReportePDF()
    
    def mostrar_menu(self):
        """este seria el panel principal"""
        print("\n" + "="*50)
        print("    SISTEMA DE INVENTARIOS - IMPORTADORA")
        print("="*50)
        print("1. Agregar nuevo artículo")
        print("2. Entrada de mercancía")
        print("3. Salida de mercancía")
        print("4. Consultar Inventario ")
        print("5. Listar todos los artículos del inventario")
        print("6. Ver movimientos")
        print("7. Ver todos los movimientos del inventario")
        print("8. Generar reporte de inventario basico")
        print("9. Generar reporte PDF del inventario")
        print("10. Generar reporte PDF de artículo")
        print("11. Salir")
        print("="*50)
    
    def agregar_articulo(self):
        """Menu para agregar un nuevo artículo"""
        print("\n--- AGREGAR NUEVO ARTÍCULO ---")
        codigo = input("Código del artículo: ").strip().upper()
        if not codigo:
            print("Error: El código no puede estar vacío")
            return
        
        nombre = input("Nombre del artículo: ").strip()
        if not nombre:
            print("Error: El nombre no puede estar vacío")
            return
        
        descripcion = input("Descripción: ").strip()
        unidad_medida = input("Unidad:  esciba Un para clasificarlo").strip()
        
        if self.inventario.agregar_articulo(codigo, nombre, descripcion, unidad_medida):
            print(f" Artículo '{nombre}' agregado exitosamente")
        else:
            print(f" Error: Ya existe un artículo con el código '{codigo}'")
    
    def entrada_mercancia(self):
        """Interfaz para registrar entrada de mercancía"""
        print("\n--- ENTRADA DE MERCANCÍA ---")
        codigo = input("Código del artículo: ").strip().upper()
        
        articulo = self.inventario.obtener_articulo(codigo)
        if not articulo:
            print(f" Error: No existe un artículo con el código '{codigo}'")
            return
        
        print(f"Artículo: {articulo.nombre} (Stock actual: {articulo.cantidad} {articulo.unidad_medida})")
        
        try:
            cantidad = float(input("Cantidad a ingresar: "))
            if cantidad <= 0:
                print(" Error: La cantidad debe ser mayor a 0")
                return
        except ValueError:
            print(" Error: Ingrese un número válido")
            return
        
        motivo = input("Motivo (opcional): ").strip()
        if not motivo:
            motivo = "Entrada de mercancía"
        
        if self.inventario.entrada_mercancia(codigo, cantidad, motivo, self.usuario_actual):
            nuevo_stock = self.inventario.obtener_stock_actual(codigo)
            print(f" Entrada registrada exitosamente")
            print(f"  Stock anterior: {articulo.cantidad - cantidad} {articulo.unidad_medida}")
            print(f"  Stock actual: {nuevo_stock} {articulo.unidad_medida}")
        else:
            print(" Error al registrar la entrada")
    
    def salida_mercancia(self):
        """Interfaz para registrar salida de mercancía"""
        print("\n--- SALIDA DE MERCANCÍA ---")
        codigo = input("Código del artículo: ").strip().upper()
        
        articulo = self.inventario.obtener_articulo(codigo)
        if not articulo:
            print(f" Error: No existe un artículo con el código '{codigo}'")
            return
        
        print(f"Artículo: {articulo.nombre} (Stock actual: {articulo.cantidad} {articulo.unidad_medida})")
        
        try:
            cantidad = float(input("Cantidad a retirar: "))
            if cantidad <= 0:
                print(" Error: La cantidad debe ser mayor a 0")
                return
        except ValueError:
            print(" Error: Ingrese un número válido")
            return
        
        if cantidad > articulo.cantidad:
            print(f" Error: Stock insuficiente. Stock disponible: {articulo.cantidad} {articulo.unidad_medida}")
            return
        
        motivo = input("Motivo (opcional): ").strip()
        if not motivo:
            motivo = "Salida de mercancía"
        
        if self.inventario.salida_mercancia(codigo, cantidad, motivo, self.usuario_actual):
            nuevo_stock = self.inventario.obtener_stock_actual(codigo)
            print(f" Salida registrada exitosamente")
            print(f"  Stock anterior: {articulo.cantidad + cantidad} {articulo.unidad_medida}")
            print(f"  Stock actual: {nuevo_stock} {articulo.unidad_medida}")
        else:
            print(" Error al registrar la salida")
    
    def consultar_stock(self):
        """Interfaz para consultar stock de un artículo"""
        print("\n--- CONSULTAR STOCK ---")
        codigo = input("Código del artículo: ").strip().upper()
        
        articulo = self.inventario.obtener_articulo(codigo)
        if not articulo:
            print(f" Error: No existe un artículo con el código '{codigo}'")
            return
        
        print(f"\nInformación del artículo:")
        print(f"  Código: {articulo.codigo}")
        print(f"  Nombre: {articulo.nombre}")
        print(f"  Descripción: {articulo.descripcion}")
        print(f"  Stock actual: {articulo.cantidad} {articulo.unidad_medida}")
    
    def listar_articulos(self):
        """Interfaz para listar todos los artículos"""
        print("\n--- LISTADO DE ARTÍCULOS ---")
        articulos = self.inventario.listar_articulos()
        
        if not articulos:
            print("No hay artículos registrados en el inventario")
            return
        
        print(f"{'Código':<10} {'Nombre':<20} {'Stock':<15} {'Unidad':<10}")
        print("-" * 60)
        for articulo in articulos:
            print(f"{articulo.codigo:<10} {articulo.nombre:<20} {articulo.cantidad:<15} {articulo.unidad_medida:<10}")
    
    def ver_movimientos_articulo(self):
        """Interfaz para ver movimientos de un artículo específico"""
        print("\n--- MOVIMIENTOS DE ARTÍCULO ---")
        codigo = input("Código del artículo: ").strip().upper()
        
        articulo = self.inventario.obtener_articulo(codigo)
        if not articulo:
            print(f" Error: No existe un artículo con el código '{codigo}'")
            return
        
        movimientos = self.inventario.obtener_movimientos_articulo(codigo)
        
        if not movimientos:
            print(f"No hay movimientos registrados para el artículo '{articulo.nombre}'")
            return
        
        print(f"\nMovimientos del artículo: {articulo.nombre}")
        print(f"{'Fecha/Hora':<20} {'Tipo':<10} {'Cantidad':<12} {'Motivo':<25} {'Usuario':<15}")
        print("-" * 85)
        
        for mov in movimientos:
            info = mov.obtener_info()
            print(f"{info['fecha_hora']:<20} {info['tipo_movimiento']:<10} {info['cantidad']:<12} {info['motivo']:<25} {info['usuario']:<15}")
    
    def ver_todos_movimientos(self):
        """Interfaz para ver todos los movimientos"""
        print("\n--- TODOS LOS MOVIMIENTOS ---")
        movimientos = self.inventario.obtener_todos_movimientos()
        
        if not movimientos:
            print("No hay movimientos registrados")
            return
        
        print(f"{'Fecha/Hora':<20} {'Artículo':<12} {'Tipo':<10} {'Cantidad':<12} {'Motivo':<25}")
        print("-" * 85)
        
        for mov in movimientos:
            info = mov.obtener_info()
            print(f"{info['fecha_hora']:<20} {info['codigo_articulo']:<12} {info['tipo_movimiento']:<10} {info['cantidad']:<12} {info['motivo']:<25}")
    
    def generar_reporte(self):
        """Interfaz para generar reporte de inventario"""
        print("\n--- REPORTE DE INVENTARIO ---")
        reporte = self.inventario.generar_reporte_inventario()
        
        print(f"Fecha del reporte: {reporte['fecha_reporte']}")
        print(f"Total de artículos: {reporte['total_articulos']}")
        print(f"Total de movimientos: {reporte['total_movimientos']}")
        print("\nDetalle de artículos:")
        print(f"{'Código':<10} {'Nombre':<20} {'Stock':<15} {'Unidad':<10}")
        print("-" * 60)
        
        for articulo_info in reporte['articulos']:
            print(f"{articulo_info['codigo']:<10} {articulo_info['nombre']:<20} {articulo_info['cantidad']:<15} {articulo_info['unidad_medida']:<10}")
    
    def generar_reporte_pdf_completo(self):
        """Interfaz para generar reporte completo en PDF"""
        print("\n--- GENERAR REPORTE PDF COMPLETO ---")
        
        try:
            archivo_pdf = self.generador_pdf.generar_reporte_inventario(self.inventario)
            print(f" Reporte PDF generado exitosamente:")
            print(f"  Archivo: {archivo_pdf}")
            print(f"  Ubicación: {os.path.dirname(archivo_pdf)}")
        except ImportError:
            print(" Error: La librería 'reportlab' no está instalada.")
            print("  Para instalar, ejecute: pip install reportlab")
        except Exception as e:
            print(f" Error al generar el reporte PDF: {e}")
    
    def generar_reporte_pdf_articulo(self):
        """Interfaz para generar reporte PDF de un artículo """
        print("\n--- GENERAR REPORTE PDF DE ARTÍCULO ---")
        codigo = input("Código del artículo: ").strip().upper()
        
        articulo = self.inventario.obtener_articulo(codigo)
        if not articulo:
            print(f" Error: No existe un artículo con el código '{codigo}'")
            return
        
        try:
            archivo_pdf = self.generador_pdf.generar_reporte_articulo(self.inventario, codigo)
            if archivo_pdf:
                print(f" Reporte PDF del artículo '{articulo.nombre}' generado exitosamente:")
                print(f"  Archivo: {archivo_pdf}")
                print(f"  Ubicación: {os.path.dirname(archivo_pdf)}")
            else:
                print(" Error al generar el reporte PDF")
        except ImportError:
            print(" Error: La librería 'reportlab' no está instalada.")
            print("  Para instalar, ejecute: pip install reportlab")
        except Exception as e:
            print(f" Error al generar el reporte PDF: {e}")
    
    def ejecutar(self):
        """Ejecuta el sistema principal"""
        print("¡Bienvenido al Sistema de Inventarios de la importadora!")
        
        while True:
            self.mostrar_menu()
            opcion = input("\nSeleccione una opción (1-11): ").strip()
            
            if opcion == "1":
                self.agregar_articulo()
            elif opcion == "2":
                self.entrada_mercancia()
            elif opcion == "3":
                self.salida_mercancia()
            elif opcion == "4":
                self.consultar_stock()
            elif opcion == "5":
                self.listar_articulos()
            elif opcion == "6":
                self.ver_movimientos_articulo()
            elif opcion == "7":
                self.ver_todos_movimientos()
            elif opcion == "8":
                self.generar_reporte()
            elif opcion == "9":
                self.generar_reporte_pdf_completo()
            elif opcion == "10":
                self.generar_reporte_pdf_articulo()
            elif opcion == "11":
                print("\n¡Hasta Luego!")
                break
            else:
                print(" Opción no válida. Por favor seleccione una opción del 1 al 11.")
            
            input("\nPresione Enter para continuar...")
            os.system('cls' if os.name == 'nt' else 'clear')

def main():
    """Función principal"""
    sistema = SistemaInventario()
    sistema.ejecutar()

if __name__ == "__main__":
    main()