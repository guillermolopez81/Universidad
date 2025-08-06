"""
Módulo para generar reportes de inventario en formato PDF
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.platypus.flowables import HRFlowable
from datetime import datetime
import os

class GeneradorReportePDF:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.titulo_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=18,
            spaceAfter=30,
            alignment=1,  # Centrado
            textColor=colors.darkblue
        )
        self.subtitulo_style = ParagraphStyle(
            'CustomSubtitle',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceAfter=20,
            textColor=colors.darkgreen
        )
    
    def generar_reporte_inventario(self, inventario, nombre_archivo=None):
        """
        Genera un reporte completo del inventario en PDF
        
        Args:
            inventario: Instancia de la clase Inventario
            nombre_archivo: Nombre del archivo PDF (opcional)
            
        Returns:
            str: Ruta del archivo PDF generado
        """
        if nombre_archivo is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nombre_archivo = f"reporte_inventario_{timestamp}.pdf"
        
        # Crear el documento PDF
        doc = SimpleDocTemplate(
            nombre_archivo,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18
        )
        
        # Contenido del documento
        story = []
        
        # Título principal
        titulo = Paragraph("REPORTE DE INVENTARIO", self.titulo_style)
        story.append(titulo)
        story.append(Spacer(1, 12))
        
        # Información general
        reporte_data = inventario.generar_reporte_inventario()
        fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        
        info_general = [
            f"<b>Fecha de generación:</b> {fecha_actual}",
            f"<b>Total de artículos:</b> {reporte_data['total_articulos']}",
            f"<b>Total de movimientos:</b> {reporte_data['total_movimientos']}"
        ]
        
        for info in info_general:
            p = Paragraph(info, self.styles['Normal'])
            story.append(p)
            story.append(Spacer(1, 6))
        
        story.append(Spacer(1, 20))
        story.append(HRFlowable(width="100%", thickness=1, lineCap='round', color=colors.grey))
        story.append(Spacer(1, 20))
        
        # Sección de artículos
        subtitulo_articulos = Paragraph("DETALLE DE ARTÍCULOS", self.subtitulo_style)
        story.append(subtitulo_articulos)
        story.append(Spacer(1, 12))
        
        if reporte_data['articulos']:
            # Crear tabla de artículos
            headers = ['Código', 'Nombre', 'Descripción', 'Stock', 'Unidad']
            data = [headers]
            
            for articulo in reporte_data['articulos']:
                fila = [
                    articulo['codigo'],
                    articulo['nombre'],
                    articulo['descripcion'][:30] + '...' if len(articulo['descripcion']) > 30 else articulo['descripcion'],
                    str(articulo['cantidad']),
                    articulo['unidad_medida']
                ]
                data.append(fila)
            
            # Crear y estilizar la tabla
            tabla_articulos = Table(data, colWidths=[1*inch, 1.5*inch, 2*inch, 0.8*inch, 1*inch])
            tabla_articulos.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]))
            
            story.append(tabla_articulos)
        else:
            no_articulos = Paragraph("No hay artículos registrados en el inventario.", self.styles['Normal'])
            story.append(no_articulos)
        
        story.append(Spacer(1, 30))
        story.append(HRFlowable(width="100%", thickness=1, lineCap='round', color=colors.grey))
        story.append(Spacer(1, 20))
        
        # Sección de movimientos recientes
        subtitulo_movimientos = Paragraph("MOVIMIENTOS RECIENTES", self.subtitulo_style)
        story.append(subtitulo_movimientos)
        story.append(Spacer(1, 12))
        
        movimientos = inventario.obtener_todos_movimientos()
        if movimientos:
            # Mostrar solo los últimos 10 movimientos
            movimientos_recientes = movimientos[-10:] if len(movimientos) > 10 else movimientos
            movimientos_recientes.reverse()  # Mostrar los más recientes primero
            
            headers_mov = ['Fecha/Hora', 'Artículo', 'Tipo', 'Cantidad', 'Usuario']
            data_mov = [headers_mov]
            
            for mov in movimientos_recientes:
                info_mov = mov.obtener_info()
                fila_mov = [
                    info_mov['fecha_hora'],
                    info_mov['codigo_articulo'],
                    info_mov['tipo_movimiento'],
                    str(info_mov['cantidad']),
                    info_mov['usuario']
                ]
                data_mov.append(fila_mov)
            
            tabla_movimientos = Table(data_mov, colWidths=[1.3*inch, 1*inch, 0.8*inch, 0.8*inch, 1*inch])
            tabla_movimientos.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.lightblue),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]))
            
            story.append(tabla_movimientos)
            
            if len(movimientos) > 10:
                nota = Paragraph(f"<i>Mostrando los 10 movimientos más recientes de {len(movimientos)} totales.</i>", 
                               self.styles['Normal'])
                story.append(Spacer(1, 10))
                story.append(nota)
        else:
            no_movimientos = Paragraph("No hay movimientos registrados.", self.styles['Normal'])
            story.append(no_movimientos)
        
        # Pie de página
        story.append(Spacer(1, 30))
        story.append(HRFlowable(width="100%", thickness=1, lineCap='round', color=colors.grey))
        story.append(Spacer(1, 10))
        
        pie = Paragraph(
            "<i>Reporte generado automáticamente por el Sistema de Inventarios</i>", 
            self.styles['Normal']
        )
        story.append(pie)
        
        # Construir el PDF
        doc.build(story)
        
        return os.path.abspath(nombre_archivo)
    
    def generar_reporte_articulo(self, inventario, codigo_articulo, nombre_archivo=None):
        """
        Genera un reporte detallado de un artículo específico en PDF
        
        Args:
            inventario: Instancia de la clase Inventario
            codigo_articulo: Código del artículo
            nombre_archivo: Nombre del archivo PDF (opcional)
            
        Returns:
            str: Ruta del archivo PDF generado o None si el artículo no existe
        """
        articulo = inventario.obtener_articulo(codigo_articulo)
        if not articulo:
            return None
        
        if nombre_archivo is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nombre_archivo = f"reporte_articulo_{codigo_articulo}_{timestamp}.pdf"
        
        doc = SimpleDocTemplate(
            nombre_archivo,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18
        )
        
        story = []
        
        # Título
        titulo = Paragraph(f"REPORTE DE ARTÍCULO: {articulo.nombre}", self.titulo_style)
        story.append(titulo)
        story.append(Spacer(1, 20))
        
        # Información del artículo
        info_articulo = [
            f"<b>Código:</b> {articulo.codigo}",
            f"<b>Nombre:</b> {articulo.nombre}",
            f"<b>Descripción:</b> {articulo.descripcion}",
            f"<b>Unidad de medida:</b> {articulo.unidad_medida}",
            f"<b>Stock actual:</b> {articulo.cantidad} {articulo.unidad_medida}",
            f"<b>Fecha de consulta:</b> {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
        ]
        
        for info in info_articulo:
            p = Paragraph(info, self.styles['Normal'])
            story.append(p)
            story.append(Spacer(1, 8))
        
        story.append(Spacer(1, 20))
        story.append(HRFlowable(width="100%", thickness=1, lineCap='round', color=colors.grey))
        story.append(Spacer(1, 20))
        
        # Historial de movimientos
        subtitulo_movimientos = Paragraph("HISTORIAL DE MOVIMIENTOS", self.subtitulo_style)
        story.append(subtitulo_movimientos)
        story.append(Spacer(1, 12))
        
        movimientos = inventario.obtener_movimientos_articulo(codigo_articulo)
        if movimientos:
            headers = ['Fecha/Hora', 'Tipo', 'Cantidad', 'Motivo', 'Usuario']
            data = [headers]
            
            # Ordenar movimientos por fecha (más recientes primero)
            movimientos_ordenados = sorted(movimientos, key=lambda x: x.fecha_hora, reverse=True)
            
            for mov in movimientos_ordenados:
                info_mov = mov.obtener_info()
                fila = [
                    info_mov['fecha_hora'],
                    info_mov['tipo_movimiento'],
                    str(info_mov['cantidad']),
                    info_mov['motivo'][:25] + '...' if len(info_mov['motivo']) > 25 else info_mov['motivo'],
                    info_mov['usuario']
                ]
                data.append(fila)
            
            tabla = Table(data, colWidths=[1.3*inch, 0.8*inch, 0.8*inch, 1.5*inch, 1*inch])
            tabla.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.darkgreen),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.lightgreen),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]))
            
            story.append(tabla)
        else:
            no_movimientos = Paragraph("No hay movimientos registrados para este artículo.", self.styles['Normal'])
            story.append(no_movimientos)
        
        # Pie de página
        story.append(Spacer(1, 30))
        story.append(HRFlowable(width="100%", thickness=1, lineCap='round', color=colors.grey))
        story.append(Spacer(1, 10))
        
        pie = Paragraph(
            "<i>Reporte generado automáticamente por el Sistema de Inventarios</i>", 
            self.styles['Normal']
        )
        story.append(pie)
        
        doc.build(story)
        
        return os.path.abspath(nombre_archivo)