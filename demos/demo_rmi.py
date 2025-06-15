# demos/demo_rmi.py

# Importamos las herramientas necesarias:
# sys y os: Para ajustar las rutas de importación y que Python encuentre nuestros módulos.
import sys
import os

# Ajustamos la ruta para que Python pueda encontrar nuestros módulos
# ubicados en la carpeta 'src'. Esto es crucial cuando ejecutamos este script
# directamente desde la carpeta 'demos'.
script_dir = os.path.dirname(__file__) # Obtenemos la ruta del script actual (demos/)
project_root = os.path.abspath(os.path.join(script_dir, '..', '..')) # Subimos dos niveles para llegar a la raíz del proyecto
sys.path.insert(0, project_root) # Añadimos la raíz del proyecto al camino de búsqueda de módulos de Python.

# Ahora importamos nuestras implementaciones desde 'src':
from src.rmi.rmi_model import RMI # Nuestro modelo RMI
from src.rmi.utils import generate_sorted_data # Nuestra utilidad para generar datos ordenados

# -----------------------------------------------------------------------------
# Demostración del Índice de Modelo Recursivo (RMI)
# -----------------------------------------------------------------------------
# El RMI es un tipo de índice muy moderno que usa "modelos" (como pequeñas
# fórmulas matemáticas) para predecir dónde se encuentra un dato en una lista
# ordenada, en lugar de usar estructuras tradicionales como árboles.
#
# Nuestra implementación tiene dos niveles:
# - **Nivel 0:** Un modelo grande que toma una clave (el número que buscamos)
#   y nos dice *aproximadamente* en qué "segmento" de nuestros datos podría estar.
# - **Nivel 1:** Una serie de modelos más pequeños, uno para cada "segmento".
#   El modelo del segmento predicho nos ayuda a afinar la posición del dato.
# -----------------------------------------------------------------------------

def demo_rmi():
    """
    Función principal de demostración para el RMI.
    Crea un RMI, inserta (implícitamente al construir) datos y realiza búsquedas.
    """
    print("--- INICIANDO DEMOSTRACIÓN DEL RMI ---")

    # 1. Preparar los datos:
    # El RMI, al igual que el B-Tree, funciona mejor con datos ya ordenados.
    # Generamos una lista de números ordenados que servirá como nuestro "array de datos".
    # Usaremos 100,000 elementos para esta demo, un tamaño significativo pero manejable.
    data_size = 100_000
    print(f"\n1. Generando un conjunto de datos ordenado con {data_size:,} elementos...")
    # 'generate_sorted_data' es nuestra utilidad que crea esta lista.
    sorted_data = generate_sorted_data(data_size, min_val=0, max_val=data_size * 5)
    print(f"   Primeros 10 elementos de los datos: {sorted_data[:10]}")
    print(f"   Últimos 10 elementos de los datos: {sorted_data[-10:]}")
    
    # 2. Construir el RMI:
    # Aquí creamos nuestra instancia del RMI. Le pasamos los datos ordenados
    # y configuramos cuántos modelos de Nivel 1 queremos y el "buffer de búsqueda"
    # (una pequeña ventana para ajustar la predicción final).
    num_level1_models = 100 # Dividimos los datos en 100 segmentos, cada uno con su propio modelo.
    search_buffer = 50     # El RMI buscará en un rango de +/- 50 posiciones alrededor de su predicción.
    
    print(f"\n2. Construyendo el RMI con {num_level1_models} modelos de Nivel 1 y un buffer de {search_buffer}...")
    # La construcción del RMI implica entrenar estos modelos para que aprendan
    # la relación entre el valor del dato y su posición en la lista.
    rmi_index = RMI(sorted_data, num_level1_models, search_buffer)
    print("   RMI construido exitosamente.")
    print(f"   Número de modelos en Nivel 1: {len(rmi_index.level1_models)}")

    # 3. Realizar búsquedas:
    # Vamos a probar la capacidad de búsqueda del RMI.
    # Probaremos con claves que existen y claves que no existen.
    
    print("\n3. Realizando búsquedas en el RMI:")
    
    # Clave existente (ejemplo: el elemento en la mitad de nuestra lista)
    key_to_find_existing = sorted_data[data_size // 2] 
    print(f"\n   Buscando una clave existente: {key_to_find_existing}")
    # El método 'search' del RMI intentará encontrar la posición de esta clave.
    predicted_pos = rmi_index.search(key_to_find_existing)
    if predicted_pos is not None:
        print(f"     -> ¡Clave {key_to_find_existing} encontrada!")
        print(f"        El RMI predijo que estaba cerca de la posición {predicted_pos}.")
        print(f"        El valor real en esa posición es: {sorted_data[predicted_pos]}.")
        print(f"        (Su posición real en la lista es {sorted_data.index(key_to_find_existing)})")
    else:
        print(f"     -> Clave {key_to_find_existing} NO encontrada por el RMI.")

    # Clave existente (ejemplo: un elemento al principio de la lista)
    key_to_find_beginning = sorted_data[5]
    print(f"\n   Buscando otra clave existente (al principio): {key_to_find_beginning}")
    predicted_pos = rmi_index.search(key_to_find_beginning)
    if predicted_pos is not None:
        print(f"     -> ¡Clave {key_to_find_beginning} encontrada!")
        print(f"        El RMI predijo que estaba cerca de la posición {predicted_pos}.")
        print(f"        El valor real en esa posición es: {sorted_data[predicted_pos]}.")
        print(f"        (Su posición real en la lista es {sorted_data.index(key_to_find_beginning)})")
    else:
        print(f"     -> Clave {key_to_find_beginning} NO encontrada por el RMI.")


    # Clave que NO existe (un número que no está en nuestra lista)
    key_to_find_non_existing = sorted_data[-1] + 100 # Un número garantizado de no estar en la lista
    print(f"\n   Buscando una clave que NO existe: {key_to_find_non_existing}")
    predicted_pos = rmi_index.search(key_to_find_non_existing)
    if predicted_pos is not None:
        print(f"     -> ¡Algo inesperado! La clave {key_to_find_non_existing} fue 'encontrada' cerca de la posición {predicted_pos}.")
        print(f"        El valor real en esa posición es: {sorted_data[predicted_pos]}.")
        print(f"        Esto ocurre porque el RMI predice una posición; la verificación final valida si es el valor exacto.")
    else:
        print(f"     -> ¡Correcto! Clave {key_to_find_non_existing} NO encontrada por el RMI. (Así debe ser si no existe).")

    print("\n--- DEMOSTRACIÓN DEL RMI FINALIZADA ---")

# Este bloque asegura que la función demo_rmi() se ejecute solo cuando
# este archivo se corre directamente, no cuando es importado por otro script.
if __name__ == "__main__":
    demo_rmi()