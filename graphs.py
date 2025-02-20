import matplotlib.pyplot as plt
import random
from fpdf import FPDF
from datetime import datetime
import os
from leer_config import obtener_valor

class ReportePDF:
    def __init__(self):
        self.config = {
            "output_folder": obtener_valor("output_folder"),
            "output_tittle": obtener_valor("output_tittle"),
            "test_mode": obtener_valor("test_mode", 0),
            "author": obtener_valor("author", "Desconocido")
        }
        self.fecha_actual = datetime.now().strftime("%B %d, %Y")
        self.nombre_archivo = f"{self.config['output_tittle']} - {self.fecha_actual}.pdf"
        self.ruta_salida = os.path.join(self.config["output_folder"], self.nombre_archivo)

        self.proactividad = None
        self.fecha_menor = None
        self.fecha_mayor = None
        self.graficos = []

        if not os.path.exists(self.config["output_folder"]):
            os.makedirs(self.config["output_folder"])

        # Paleta de colores para los gráficos
        self.colores = [
            "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd",
            "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"
        ]

    def asignar_proactividad(self, proactividad):
        self.proactividad = proactividad
        if self.config["test_mode"] == 1:
            print(f"✅ Se ha asignado el porcentaje de proactividad: {self.proactividad:.2f}%")

    def asignar_fechas(self, fecha_mayor, fecha_menor):
        self.fecha_mayor = fecha_mayor
        self.fecha_menor = fecha_menor
        if self.config["test_mode"] == 1:
            print(f"✅ Fechas asignadas: Mayor - {self.fecha_mayor}, Menor - {self.fecha_menor}")

    def agregar_valor(self, datos, tipo_grafico, titulo=None):
        if not datos:
            print("⚠️ No se agregaron datos, la lista está vacía.")
            return

        self.graficos.append({"datos": datos, "tipo": tipo_grafico, "titulo": titulo})
        if self.config["test_mode"] == 1:
            print(f"✅ Se ha agregado la variable '{titulo or 'Sin título'}' con {len(datos)} registros.")

    def generar_grafico(self, datos, tipo_grafico, titulo):
        categorias = [item[0] for item in datos]
        valores = [item[1] for item in datos]
        colores = random.sample(self.colores, min(len(categorias), len(self.colores)))

        plt.figure(figsize=(6, 4))

        if tipo_grafico == "barras":
            plt.bar(categorias, valores, color=colores)
            plt.xticks(rotation=45)
        elif tipo_grafico == "torta":
            plt.pie(valores, labels=categorias, autopct="%1.1f%%", colors=colores)

        plt.title(titulo)
        plt.tight_layout()

        ruta_imagen = f"temp_{titulo}.png"
        plt.savefig(ruta_imagen)
        plt.close()

        return ruta_imagen

    def imprimir(self):
        """
        Genera el archivo PDF con los datos, gráficos y tablas.
        """
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", "", 12)

        # Título del Reporte
        titulo_reporte = f"Reporte de gestión del día {self.fecha_mayor} \nevaluado desde el {self.fecha_menor}, por {self.config['author']}"
        pdf.cell(200, 10, titulo_reporte.encode("latin-1", "ignore").decode("latin-1"), ln=True, align="C")
        pdf.ln(10)

        # Sección de Proactividad
        if self.proactividad is not None:
            proactividad_texto = f"Nivel de Proactividad: {self.proactividad:.2f}%"
            pdf.cell(200, 10, proactividad_texto.encode("latin-1", "ignore").decode("latin-1"), ln=True)
        pdf.ln(5)

        # Agregar gráficos y tablas al PDF
        for grafico in self.graficos:
            datos, tipo_grafico, titulo = grafico["datos"], grafico["tipo"], grafico["titulo"]
            ruta_imagen = self.generar_grafico(datos, tipo_grafico, titulo)

            pdf.cell(200, 10, titulo.encode("latin-1", "ignore").decode("latin-1"), ln=True, align="C")
            pdf.ln(5)

            pdf.image(ruta_imagen, x=10, w=180)
            pdf.ln(10)

            # Eliminar la imagen temporal
            os.remove(ruta_imagen)

            # 🔹 Agregar tabla debajo del gráfico
            pdf.set_font("Arial", "B", 10)
            pdf.cell(80, 10, "Categoría", 1, 0, "C")
            pdf.cell(50, 10, "Cantidad", 1, 1, "C")
            pdf.set_font("Arial", "", 10)

            for item in datos:
                pdf.cell(80, 10, str(item[0]), 1, 0, "C")
                pdf.cell(50, 10, str(item[1]), 1, 1, "C")

            pdf.ln(5)

        pdf.output(self.ruta_salida, "F")
        print(f"📄 Reporte generado: {self.ruta_salida}")
