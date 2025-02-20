import json
import os

# Variable global para almacenar la configuración cargada
_config_data = None

def cargar_config(ruta_config="config.json"):
    """
    Carga el archivo de configuración JSON y devuelve un diccionario con los parámetros.
    Si 'test_mode' está activo, imprime los valores en consola.
    Almacena la configuración en memoria para evitar recargarla innecesariamente.
    """
    global _config_data  # Usamos una variable global para evitar recargar el JSON

    if _config_data is not None:
        return _config_data  # Si ya fue cargado, retornamos la configuración en memoria

    if not os.path.exists(ruta_config):
        print(f"⚠️ El archivo de configuración '{ruta_config}' no existe.")
        return None

    try:
        with open(ruta_config, "r", encoding="utf-8") as file:
            _config_data = json.load(file)
    except json.JSONDecodeError:
        print("⚠️ Error al leer el archivo JSON. Verifica que la sintaxis sea correcta.")
        return None

    # Si test_mode está activo, imprimimos TODAS las variables encontradas
    if _config_data.get("test_mode", 0) == 1:
        print("📌 Configuración cargada correctamente:")
        for key, value in _config_data.items():
            print(f"   - {key}: {value}")

    return _config_data

def obtener_valor(clave, valor_por_defecto=None):
    """
    Retorna el valor de una clave específica en la configuración.
    Si la clave no existe, devuelve un valor por defecto.
    """
    config = cargar_config()
    return config.get(clave, valor_por_defecto)


if __name__ == "__main__":
    config = cargar_config()

