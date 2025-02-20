import pandas as pd
from leer_config import obtener_valor
from graphs import ReportePDF

class MainApp:
    def __init__(self):
        """
        Inicializa la aplicación principal cargando la configuración.
        """
        self.config = {
            "input_csv": obtener_valor("input_csv"),
            "test_mode": obtener_valor("test_mode", 0),
            "top": obtener_valor("top", 5),
            "campo_fechas": obtener_valor("campo_fechas", "Date")  # Campo de fechas
        }
        self.df = None  # Variable para almacenar el DataFrame en RAM

    def leer_archivo(self):
        """
        Lee el archivo CSV especificado en la configuración, analiza los datos
        y, si `test_mode` está activo, imprime la información clave.
        """
        archivo_csv = self.config["input_csv"]

        try:
            self.df = pd.read_csv(archivo_csv)  # Cargar el archivo una sola vez
        except FileNotFoundError:
            print(f"⚠️ Error: No se encontró el archivo '{archivo_csv}'")
            return
        except pd.errors.EmptyDataError:
            print(f"⚠️ Error: El archivo '{archivo_csv}' está vacío.")
            return
        except pd.errors.ParserError:
            print(f"⚠️ Error: No se pudo analizar el CSV. Verifica el formato.")
            return

        # Contar registros y clientes únicos
        total_registros = self.df["ID"].count()
        total_clientes = self.df["Company"].nunique()

        # Si el modo de prueba está activado, mostrar información
        if self.config["test_mode"] == 1:
            print(f"📂 Se ha abierto el archivo '{archivo_csv}'")
            print(f"📊 Se han encontrado {total_registros} registros, para {total_clientes} clientes.")

    def obtener_datos(self):
        """
        Devuelve el DataFrame con los datos cargados. Si aún no se ha leído,
        primero ejecuta `leer_archivo()`.
        """
        if self.df is None:
            self.leer_archivo()
        return self.df

    def obtener_fechas(self):
        """
        Busca el campo de fechas definido en `campo_fechas` y retorna la menor y mayor fecha.
        """
        df = self.obtener_datos()

        if self.config["campo_fechas"] not in df.columns:
            print(f"⚠️ El campo '{self.config['campo_fechas']}' no existe en el archivo CSV.")
            return None, None

        # Convertir a formato de fecha para evitar errores
        df[self.config["campo_fechas"]] = pd.to_datetime(df[self.config["campo_fechas"]], errors="coerce")

        fecha_menor = df[self.config["campo_fechas"]].min()
        fecha_mayor = df[self.config["campo_fechas"]].max()

        if self.config["test_mode"] == 1:
            print(f"📆 Fechas encontradas: Mayor - {fecha_mayor}, Menor - {fecha_menor}")

        return fecha_mayor, fecha_menor

    def leer_proactividad(self):
        """
        Calcula el porcentaje de valores 'True' en la columna 'Proactive'.
        """
        df = self.obtener_datos()

        if "Proactive" not in df.columns:
            print("⚠️ La columna 'Proactive' no existe en el archivo CSV.")
            return None

        total_valores = len(df["Proactive"].dropna())  # Contar valores no nulos
        total_true = (df["Proactive"] == True).sum()  # Contar valores True

        porcentaje_proactivo = (total_true / total_valores * 100) if total_valores > 0 else 0

        if self.config["test_mode"] == 1:
            print(f"📈 Porcentaje de valores 'True' en 'Proactive': {porcentaje_proactivo:.2f}%")

        return porcentaje_proactivo

    def llenar_tablas(self, campo, orden, campo_filtro=None, valor_filtro=None):
        """
        Obtiene los 'Top' valores más altos o bajos de un campo específico,
        mostrando su cantidad de apariciones, opcionalmente filtrando por otro campo.

        Parámetros:
        - campo (str): El campo a analizar.
        - orden (int): 1 para los valores más altos, 0 para los valores más bajos.
        - campo_filtro (str, opcional): Campo donde se aplicará el filtro.
        - valor_filtro (str, opcional): Valor que debe contener el campo de filtro.

        Retorna:
        - list: Arreglo bidimensional con los resultados en formato [criterio, cantidad].
        """
        df = self.obtener_datos()

        if campo not in df.columns:
            print(f"⚠️ El campo '{campo}' no existe en el archivo CSV.")
            return []

        if campo_filtro and campo_filtro not in df.columns:
            print(f"⚠️ El campo de filtro '{campo_filtro}' no existe en el archivo CSV.")
            return []

        if campo_filtro and valor_filtro:
            df = df[df[campo_filtro].astype(str).str.contains(valor_filtro, case=False, na=False)]

        conteo = df[campo].value_counts().reset_index()
        conteo.columns = [campo, "Cantidad"]

        conteo_sorted = conteo.sort_values(by="Cantidad", ascending=(orden == 0))

        top_n = self.config["top"]
        resultado = conteo_sorted.head(top_n).values.tolist()

        if self.config["test_mode"] == 1:
            filtro_info = f" revisando que el '{campo_filtro}' sea '{valor_filtro}'" if campo_filtro and valor_filtro else ""
            print(f"📊 Para el campo: '{campo}', los {top_n} valores más {'altos' if orden == 1 else 'bajos'}{filtro_info} son:")
            for item in resultado:
                print(f"   - {item[0]}: {item[1]}")

        return resultado

    def llamar_a_graphs(self):
        """
        Ejecuta toda la secuencia necesaria para generar el reporte PDF con `graphs.py`.
        """
        reporte = ReportePDF()

        # Asignar proactividad
        reporte.asignar_proactividad(self.leer_proactividad())

        # Asignar fechas
        fecha_mayor, fecha_menor = self.obtener_fechas()
        if fecha_mayor and fecha_menor:
            reporte.asignar_fechas(fecha_mayor, fecha_menor)

        # Agregar valores de prueba
        top_ips = self.llenar_tablas("IP", 1, "Attack Type", "Phishing")
        reporte.agregar_valor(top_ips, "barras", "IPs con más intentos de Phishing")

        top_Domains = self.llenar_tablas("Domain", 1, "Attack Type", "Phishing")
        reporte.agregar_valor(top_Domains, "torta", "Dominios más abusados (Phishing)")

        top_clientes = self.llenar_tablas("Client", 1)
        reporte.agregar_valor(top_clientes, "torta", "Clientes con más actividad")

        max_attacks = self.llenar_tablas("Attack Type", 1)
        reporte.agregar_valor(max_attacks, "torta", "Ataques más frecuentes")

        max_customers = self.llenar_tablas("Company", 1)
        reporte.agregar_valor(max_customers, "torta", "Clientes más atacados")

        min_customers = self.llenar_tablas("Company", 0)
        reporte.agregar_valor(min_customers, "torta", "Clientes menos atacados")

        max_customersR = self.llenar_tablas("Company", 1,"Proactive", "false")
        reporte.agregar_valor(max_customersR, "torta", "Clientes más reactivos")

        reporte.imprimir()

# Ejecutar si es el script principal
if __name__ == "__main__":
    app = MainApp()
    app.leer_archivo()

    # Llamar a graphs para generar el reporte
    app.llamar_a_graphs()
