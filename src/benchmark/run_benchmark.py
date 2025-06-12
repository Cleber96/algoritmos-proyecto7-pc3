# src/benchmark/run_benchmark.py

# Importamos las clases y funciones que vamos a comparar y medir.
# Vienen de nuestros propios módulos, implementados desde cero.
from ..rmi.rmi_model import RMI # Nuestro Índice de Modelo Recursivo
from ..btree.btree import BTree # Nuestro B-Tree
from ..rmi.utils import generate_sorted_data, measure_time # Utilidades para datos y tiempo

# Importamos sys para manejar el path si es necesario en entornos específicos
import sys
import os

# Ajuste del PATH para asegurar que los módulos se encuentren correctamente
# Esto es útil cuando se ejecutan scripts desde diferentes directorios.
# Agregamos la carpeta 'src' al path de Python.
# Si el script se ejecuta desde 'algoritmos-proyecto7-pc3/',
# sys.path.append(os.path.abspath('.')) debería ser suficiente.
# Si se ejecuta desde 'algoritmos-proyecto7-pc3/src/benchmark/',
# entonces sys.path.append(os.path.abspath('../../')) sería más apropiado.
# Para esta demostración, asumimos una ejecución desde la raíz del proyecto.
# Una forma más robusta es usar el path relativo del propio archivo.
script_dir = os.path.dirname(__file__) # Directorio actual del script
project_root = os.path.abspath(os.path.join(script_dir, '..', '..')) # Sube dos niveles para la raíz del proyecto
sys.path.insert(0, project_root) # Añade la raíz del proyecto al path de Python

# Es importante que las importaciones relativas (e.g., from ..rmi.rmi_model)
# funcionen, lo que a menudo requiere que el módulo 'src' se trate como un paquete
# (tener un __init__.py en src/ y sus subcarpetas) y que se ejecute desde
# la raíz del proyecto usando `python -m src.benchmark.run_benchmark`.
# Para una ejecución simple `python src/benchmark/run_benchmark.py`,
# el ajuste de sys.path es crucial.

# -----------------------------------------------------------------------------
# Script de Benchmarking General
# -----------------------------------------------------------------------------
# Este script es el "laboratorio" de nuestro proyecto. Aquí es donde ponemos
# a prueba nuestros algoritmos (RMI y B-Tree) para ver qué tan bien funcionan
# en diferentes escenarios.
#
# ¿Por qué hacemos benchmarking?
# - **Comparación:** Nos permite ver si el RMI es realmente más rápido o más
#   eficiente que el B-Tree para ciertos tipos de operaciones.
# - **Rendimiento:** Nos ayuda a entender cómo escalan nuestros algoritmos
#   a medida que el tamaño de los datos aumenta.
# - **Validación:** Confirma que nuestras implementaciones son eficientes
#   y se comportan como esperamos.
#
# Mediremos principalmente:
# - **Tiempo de Construcción:** Cuánto tardan en crearse los índices.
# - **Tiempo de Búsqueda:** Cuánto tardan en encontrar un elemento.
# - **Uso de Memoria (Estimado):** Una aproximación de cuánto espacio ocupan.
# -----------------------------------------------------------------------------

def run_benchmarks(data_sizes, num_searches_per_data_size):
    """
    Ejecuta un conjunto de pruebas de rendimiento (benchmarks)
    para el RMI y el B-Tree en diferentes tamaños de datos.

    Args:
        data_sizes (list): Una lista de enteros, donde cada entero es un
                           tamaño de conjunto de datos a probar (e.g., [1000, 10000, 100000]).
        num_searches_per_data_size (int): El número de búsquedas a realizar
                                          para cada tamaño de datos para obtener un promedio.

    Returns:
        dict: Un diccionario con los resultados de los benchmarks,
              incluyendo tiempos de construcción, tiempos de búsqueda y tamaños de memoria.
    """
    print("\n--- INICIANDO BENCHMARKS ---")
    results = {
        'data_sizes': data_sizes,
        'rmi_build_times': [],
        'rmi_search_times': [],
        'rmi_memory_usage': [],
        'btree_build_times': [],
        'btree_search_times': [],
        'btree_memory_usage': [],
    }

    # Parámetros para el RMI y B-Tree (pueden ser ajustados para pruebas)
    # Estos son solo valores iniciales; en un análisis profundo, se probarían diferentes 't' y 'num_level1_models'.
    RMI_NUM_LEVEL1_MODELS = 100 # Número de modelos de Nivel 1 para el RMI
    RMI_SEARCH_BUFFER = 50     # Ventana de búsqueda para el RMI
    BTREE_ORDER_T = 3          # Orden del B-Tree (t)

    # Iteramos sobre cada tamaño de datos que queremos probar.
    for size in data_sizes:
        print(f"\n--- Probando con un tamaño de datos de: {size:,} elementos ---")

        # ---------------------------------------------------------------------
        # Preparación de los datos
        # ---------------------------------------------------------------------
        # Generamos un nuevo conjunto de datos ordenado para cada prueba,
        # para asegurar que las pruebas sean justas y que los índices se construyan
        # sobre datos "frescos".
        data = generate_sorted_data(size, 0, size * 10) # Generamos datos con un rango más amplio.
        
        # Seleccionamos algunas claves aleatorias para buscar.
        # Es importante que algunas existan y otras no, para simular un uso real.
        search_keys = []
        for _ in range(num_searches_per_data_size):
            # 70% de probabilidad de buscar una clave existente, 30% de una no existente
            if random.random() < 0.7:
                search_keys.append(data[random.randint(0, size - 1)]) # Clave existente
            else:
                # Clave no existente (fuera del rango de datos o en un hueco)
                search_keys.append(random.randint(0, size * 10 + 100))

        # ---------------------------------------------------------------------
        # Benchmarking del RMI
        # ---------------------------------------------------------------------
        print(f"\n  >> Benchmarking de RMI (tamaño: {size:,})...")
        
        # 1. Medir tiempo de construcción del RMI
        # Usamos nuestra utilidad measure_time para capturar el tiempo.
        rmi_instance, build_time_rmi = measure_time(RMI, data, RMI_NUM_LEVEL1_MODELS, RMI_SEARCH_BUFFER)
        results['rmi_build_times'].append(build_time_rmi)
        print(f"    Tiempo de construcción del RMI: {build_time_rmi:.6f} segundos.")

        # 2. Medir tiempo promedio de búsqueda del RMI
        total_search_time_rmi = 0
        num_successful_searches_rmi = 0
        for key in search_keys:
            _, search_time = measure_time(rmi_instance.search, key)
            total_search_time_rmi += search_time
            # Opcional: Contar búsquedas exitosas si es relevante para el análisis
            if rmi_instance.search(key) is not None:
                num_successful_searches_rmi += 1

        avg_search_time_rmi = total_search_time_rmi / num_searches_per_data_size
        results['rmi_search_times'].append(avg_search_time_rmi)
        print(f"    Tiempo promedio de búsqueda del RMI (sobre {num_searches_per_data_size} búsquedas): {avg_search_time_rmi:.9f} segundos.")
        
        # 3. Estimar uso de memoria del RMI
        # Esto es una estimación MUY simplificada sin librerías especializadas.
        # Contamos el número de modelos y sus parámetros (m, b).
        # Cada modelo tiene 2 flotantes (m y b).
        # Los datos originales también ocupan memoria, pero los consideramos para ambos.
        # Una estimación más precisa consideraría el overhead de las listas, etc.
        estimated_rmi_memory = (1 * 2) + (RMI_NUM_LEVEL1_MODELS * 2) # Nivel 0 (m,b) + Nivel 1 (m,b) por modelo
        results['rmi_memory_usage'].append(estimated_rmi_memory)
        print(f"    Estimación de uso de memoria del RMI (parámetros): {estimated_rmi_memory} unidades.")


        # ---------------------------------------------------------------------
        # Benchmarking del B-Tree
        # ---------------------------------------------------------------------
        print(f"\n  >> Benchmarking de B-Tree (tamaño: {size:,})...")

        # 1. Medir tiempo de construcción del B-Tree
        # Para construir el B-Tree, insertamos cada elemento del 'data' en él.
        # Medimos el tiempo total de todas las inserciones.
        
        # Creamos una función auxiliar para la construcción para poder medirla.
        def build_btree_func(data_list, order_t):
            tree = BTree(order_t)
            for item in data_list:
                tree.insert(item)
            return tree

        btree_instance, build_time_btree = measure_time(build_btree_func, data, BTREE_ORDER_T)
        results['btree_build_times'].append(build_time_btree)
        print(f"    Tiempo de construcción del B-Tree: {build_time_btree:.6f} segundos.")

        # 2. Medir tiempo promedio de búsqueda del B-Tree
        total_search_time_btree = 0
        num_successful_searches_btree = 0
        for key in search_keys:
            _, search_time = measure_time(btree_instance.search, key)
            total_search_time_btree += search_time
            # Opcional: Contar búsquedas exitosas
            if btree_instance.search(key) is not None:
                num_successful_searches_btree += 1

        avg_search_time_btree = total_search_time_btree / num_searches_per_data_size
        results['btree_search_times'].append(avg_search_time_btree)
        print(f"    Tiempo promedio de búsqueda del B-Tree (sobre {num_searches_per_data_size} búsquedas): {avg_search_time_btree:.9f} segundos.")

        # 3. Estimar uso de memoria del B-Tree
        # Esto es una estimación MUY simplificada.
        # Contamos el número total de claves y el número de nodos.
        # Una estimación más precisa contaría los punteros, el overhead de las listas, etc.
        estimated_btree_memory = 0
        # Recorremos el árbol para contar nodos y claves.
        nodes_to_visit = [btree_instance.root]
        num_nodes = 0
        num_keys = 0
        while nodes_to_visit:
            current_node = nodes_to_visit.pop(0) # Tomamos el primer nodo (FIFO)
            num_nodes += 1
            num_keys += len(current_node.keys)
            if not current_node.leaf:
                nodes_to_visit.extend(current_node.children) # Añadimos los hijos a la lista

        # La memoria se estima en base al número de claves y nodos.
        # Asumimos que cada clave y cada puntero a hijo ocupa una "unidad" de memoria.
        # Cada nodo tiene un costo base más el costo de sus claves y punteros.
        # En un B-Tree, un nodo con K claves tiene K+1 hijos.
        # Entonces, memoria = (número de nodos * costo base de nodo) + (número de claves * costo de clave) + (número de hijos * costo de puntero)
        # Aquí simplificamos a num_keys + num_nodes para tener un valor de referencia.
        estimated_btree_memory = num_keys + num_nodes * BTREE_ORDER_T # Una aproximación simple
        results['btree_memory_usage'].append(estimated_btree_memory)
        print(f"    Estimación de uso de memoria del B-Tree (claves+nodos): {estimated_btree_memory} unidades.")

    print("\n--- BENCHMARKS COMPLETADOS ---")
    return results

# Este bloque se ejecuta cuando el script se corre directamente.
if __name__ == "__main__":
    # Definimos los tamaños de datos que queremos probar.
    # Empezamos pequeños y aumentamos para ver el rendimiento.
    # NOTA: Para tamaños muy grandes (e.g., 1_000_000+), la ejecución sin NumPy
    # puede ser EXTREMADAMENTE lenta, especialmente la construcción del B-Tree
    # y la generación de datos. Considera esto para la exposición.
    test_data_sizes = [1000, 5000, 10000, 20000] # Tamaños de datos a probar

    # Número de búsquedas para promediar el tiempo de búsqueda.
    # Un número mayor da un promedio más estable, pero tarda más.
    num_searches = 500

    # Ejecutamos los benchmarks.
    benchmark_results = run_benchmarks(test_data_sizes, num_searches)

    # Imprimimos los resultados finales en un formato legible.
    print("\n--- RESUMEN DE RESULTADOS DE BENCHMARKING ---")
    print("Tamaños de datos probados:", benchmark_results['data_sizes'])
    print("\n--- Tiempos de Construcción (segundos) ---")
    print("RMI:", [f"{t:.6f}" for t in benchmark_results['rmi_build_times']])
    print("B-Tree:", [f"{t:.6f}" for t in benchmark_results['btree_build_times']])
    
    print("\n--- Tiempos Promedio de Búsqueda (segundos) ---")
    print("RMI:", [f"{t:.9f}" for t in benchmark_results['rmi_search_times']])
    print("B-Tree:", [f"{t:.9f}" for t in benchmark_results['btree_search_times']])

    print("\n--- Uso de Memoria Estimado (unidades) ---")
    print("RMI:", benchmark_results['rmi_memory_usage'])
    print("B-Tree:", benchmark_results['btree_memory_usage'])

    # En una aplicación real, estos resultados se pasarían a 'visualizations.py'
    # para generar gráficos. Aquí, solo los imprimimos.
    print("\nLos resultados anteriores pueden ser usados para generar gráficas.")