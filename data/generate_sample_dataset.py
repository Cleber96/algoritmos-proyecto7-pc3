# data/generate_sample_dataset.py

# Importamos NumPy, la librería especializada para trabajar con arrays numéricos.
# Aunque nuestras implementaciones de RMI y B-Tree son "desde cero",
# NumPy es la herramienta estándar y eficiente para GENERAR y manipular
# grandes volúmenes de datos numéricos en Python.
import numpy as np
# Importamos 'os' para interactuar con el sistema operativo,
# como crear directorios si no existen.
import os          

# -----------------------------------------------------------------------------
# ¿Para qué sirve este script? (Generación del Conjunto de Datos de Ejemplo)
# -----------------------------------------------------------------------------
# Este script es como nuestra "fábrica de datos". Su único propósito es crear
# un archivo llamado 'sample_dataset.npy' que contendrá un conjunto muy grande
# de números enteros ordenados.
#
# Nuestros algoritmos de indexación (RMI y B-Tree) necesitan datos para funcionar.
# Almacenar estos datos en un archivo .npy ofrece varias ventajas:
# - **Eficiencia:** Los archivos .npy guardan los datos en un formato binario
#   compacto, lo que los hace pequeños en disco y rápidos de leer.
# - **Velocidad de Carga:** Cargar un .npy es mucho más rápido que leer un
#   archivo de texto grande línea por línea, lo cual es crucial para pruebas
#   de rendimiento (benchmarks).
# - **Preparación:** Asegura que todos usemos el mismo conjunto de datos
#   ordenados, haciendo nuestras pruebas comparables y reproducibles.
#
# Para tu exposición, puedes explicar que este es el paso inicial para preparar
# los datos sobre los cuales RMI y B-Tree competirán en velocidad y eficiencia.
# -----------------------------------------------------------------------------

def create_sample_dataset(size=1_000_000, filename="sample_dataset.npy", directory="."):
    """
    Genera un array de enteros únicos y ordenados y lo guarda en un archivo .npy.
    Estos datos simulan un conjunto de claves ordenadas que nuestros índices
    (RMI y B-Tree) buscarán y gestionarán.

    Args:
        size (int): El número de elementos (enteros) a generar en el dataset.
                    Un millón es un tamaño común para empezar a ver el rendimiento
                    de algoritmos a gran escala.
        filename (str): El nombre del archivo .npy que se creará.
        directory (str): El directorio donde se guardará el archivo.
                         Por defecto, se guardará en el mismo directorio donde
                         se ejecute este script.
    """
    print(f"--- Iniciando la generación del conjunto de datos de ejemplo ---")
    print(f"  Tamaño deseado del dataset: {size:,} elementos.")
    print(f"  Nombre del archivo de salida: '{filename}'")
    print(f"  Directorio de salida: '{directory}'")

    # Paso 1: Definir el rango de los números.
    # Queremos que nuestros datos sean "dispersos" para simular un escenario
    # más realista, donde las claves no son solo 0, 1, 2, ...
    # Multiplicamos el tamaño por un factor (ej. 5) para tener un rango más amplio.
    min_val = 0
    max_val = size * 5 
    
    # Aseguramos que el rango sea suficientemente grande para generar 'size'
    # números únicos. Si el rango es más pequeño que el 'size' deseado,
    # lo ajustamos para evitar problemas.
    if (max_val - min_val + 1) < size:
        max_val = min_val + size # Ajustamos el límite superior del rango.
        print(f"  Advertencia: Rango de valores ajustado a {max_val} para asegurar suficientes valores únicos.")

    # Paso 2: Generar los números aleatorios y ordenarlos.
    # Utilizamos `np.random.randint` para generar 'size' números enteros
    # aleatorios dentro de nuestro rango definido (min_val a max_val).
    # Luego, `np.sort` los ordena de forma ascendente.
    # Es crucial que los datos estén ordenados para el funcionamiento correcto
    # de RMI y para que el B-Tree pueda ser construido eficientemente.
    print(f"  Generando {size:,} números aleatorios y luego ordenándolos...")
    data_array = np.sort(np.random.randint(min_val, max_val, size=size, dtype=np.int64))
    
    # Opcional: Si quisiéramos asegurarnos de que todos los números son estrictamente
    # únicos (sin duplicados), usaríamos `np.unique`. Para datasets muy grandes,
    # `np.random.randint` es eficiente, y los duplicados (si los hay) son pocos.
    # data_array = np.unique(data_array)
    # print(f"  Tamaño final del dataset (después de ordenar y eliminar duplicados): {len(data_array):,}")

    print("  Array de datos generado y ordenado.")

    # Paso 3: Crear el directorio de salida si no existe.
    # Esto asegura que el script no falle si la carpeta 'data/' aún no está creada.
    os.makedirs(directory, exist_ok=True) 

    # Paso 4: Guardar el array en un archivo .npy.
    # `np.save()` es la función de NumPy que hace la magia de guardar el array
    # en el formato binario '.npy'.
    output_filepath = os.path.join(directory, filename) # Construye la ruta completa al archivo.
    print(f"  Guardando el array en '{output_filepath}'...")
    np.save(output_filepath, data_array)
    
    print("  ¡Dataset de ejemplo creado exitosamente!")
    print(f"  Puedes encontrar el archivo binario '{filename}' en el directorio '{directory}'.")
    print(f"--- Generación del conjunto de datos de ejemplo finalizada ---")


# Este bloque se ejecuta solo cuando 'generate_sample_dataset.py' se corre directamente
# (por ejemplo, desde la línea de comandos con `python generate_sample_dataset.py`).
# No se ejecutará si el archivo es importado como un módulo por otro script.
if __name__ == "__main__":
    # Definimos el tamaño del dataset que queremos generar.
    # Puedes ajustar este valor:
    # - `100_000` para pruebas rápidas o demos.
    # - `1_000_000` o más para benchmarks más serios.
    dataset_size = 100_000 # Un tamaño razonable para empezar.

    # Definimos dónde se guardará el archivo .npy.
    # `os.path.dirname(os.path.abspath(__file__))` obtiene el directorio
    # donde se encuentra este script ('data/').
    current_script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = current_script_dir 

    # ¡Llamamos a nuestra función para que genere el dataset!
    create_sample_dataset(size=dataset_size, directory=output_dir)

    # Una vez que este script termina, el archivo 'sample_dataset.npy' estará
    # en la carpeta 'data/'. Para cargar estos datos en otros scripts (como
    # 'run_benchmark.py'), simplemente usarías:
    # `loaded_data = np.load('data/sample_dataset.npy')`