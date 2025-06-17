import time # Necesitamos el módulo 'time' para medir el tiempo de ejecución.
import random # Necesitamos el módulo 'random' para generar datos.


def generate_sorted_data(size, min_val=0, max_val=1_000_000):
    """
    Genera una lista de enteros únicos y ordenados de forma ascendente.
    Esto simula los datos que nuestros índices (RMI y B-Tree) van a manejar.

    Args:
        size (int): El número de elementos (enteros) que queremos en la lista.
        min_val (int): El valor mínimo posible para los enteros generados.
        max_val (int): El valor máximo posible para los enteros generados.

    Returns:
        list: Una lista de enteros ordenados.
    """
    if size <= 0:
        return [] # Si el tamaño es 0 o negativo, retornamos una lista vacía.
    
    if max_val - min_val + 1 < size:
        # Esto significa que no hay suficientes números únicos en el rango especificado
        # para generar la cantidad 'size' de elementos.
        # Por ejemplo, si pido 100 números entre 1 y 5.
        print(f"Advertencia: El rango de valores ({min_val}-{max_val}) no es lo suficientemente grande para generar {size} valores únicos.")
        # Intentamos generar tantos como sea posible.
        size = max_val - min_val + 1

    print(f"Generando {size:,} datos ordenados entre {min_val} y {max_val}...")
    
    # 1. Crear un conjunto (set) para asegurar que todos los números sean únicos.
    # Un set es como una bolsa donde solo puedes tener un ejemplar de cada cosa.
    unique_numbers = set()
    
    # 2. Rellenar el set con números aleatorios hasta alcanzar el tamaño deseado.
    while len(unique_numbers) < size:
        # Generamos un número aleatorio dentro del rango.
        num = random.randint(min_val, max_val)
        unique_numbers.add(num) # Lo añadimos al set. Si ya existe, no hace nada.

    # 3. Convertir el set a una lista y ordenarla.
    # Los RMI y B-Trees (especialmente para búsqueda eficiente) operan sobre
    # datos ordenados. Por eso, este paso es crucial.
    sorted_data = list(unique_numbers) # Convertimos el set a una lista.
    sorted_data.sort() # ¡Ordenamos la lista!

    print("Generación de datos completada.")
    return sorted_data


def measure_time(func, *args, **kwargs):
    """
    Mide el tiempo de ejecución de una función dada.
    Esta utilidad es fundamental para el benchmarking, ya que nos permite
    comparar qué tan rápido son nuestras implementaciones de RMI y B-Tree.

    Args:
        func (function): La función cuyo tiempo de ejecución queremos medir.
        *args: Argumentos posicionales que se pasarán a 'func'.
        **kwargs: Argumentos de palabra clave que se pasarán a 'func'.

    Returns:
        tuple: Una tupla que contiene (resultado_de_la_funcion, tiempo_en_segundos).
               'resultado_de_la_funcion' es lo que 'func' normalmente retornaría.
    """
    # time.perf_counter() nos da el tiempo con alta precisión.
    # Es ideal para medir intervalos cortos.
    start_time = time.perf_counter() # Registramos el momento de inicio.
    
    # Ejecutamos la función que nos pasaron, con todos sus argumentos.
    result = func(*args, **kwargs)
    
    end_time = time.perf_counter() # Registramos el momento de finalización.
    
    # Calculamos la duración restando el tiempo de inicio al tiempo de finalización.
    elapsed_time = end_time - start_time
    
    return result, elapsed_time


# -----------------------------------------------------------------------------
# Función de Demostración para las Utilidades
# -----------------------------------------------------------------------------
# Esta función es solo para probar las utilidades por separado.
# No forma parte de la lógica principal de RMI/B-Tree.
# -----------------------------------------------------------------------------

def demo_utils():
    """
    Demuestra el uso de las funciones de utilidad:
    - generate_sorted_data
    - measure_time
    """
    print("--- Demostración de las Funciones Utilitarias ---")

    # Demostración de generate_sorted_data
    print("\n1. Demostrando 'generate_sorted_data':")
    
    # Generamos 10 datos para una prueba rápida.
    data_size = 10
    generated_list = generate_sorted_data(data_size, min_val=10, max_val=100)
    print(f"   Lista generada ({len(generated_list)} elementos): {generated_list}")
    
    # Verificamos que esté ordenada
    is_sorted = True
    for i in range(len(generated_list) - 1):
        if generated_list[i] > generated_list[i+1]:
            is_sorted = False
            break
    print(f"   ¿Está la lista ordenada? {'Sí' if is_sorted else 'No'}")

    # Demostración de measure_time
    print("\n2. Demostrando 'measure_time':")

    # Definimos una función de ejemplo simple para medir su tiempo de ejecución.
    def example_long_operation(iterations):
        print(f"   Ejecutando una operación que tardará un poco (iteraciones: {iterations:,})...")
        total = 0
        for i in range(iterations):
            total += i * i # Una operación simple para consumir tiempo
        print("   Operación de ejemplo terminada.")
        return total

    # Medimos el tiempo de nuestra función de ejemplo.
    num_iterations = 5_000_000 # Un número grande para que tarde algo de tiempo.
    result, time_taken = measure_time(example_long_operation, num_iterations)
    
    print(f"   Resultado de la operación: {result}")
    print(f"   Tiempo tomado para 'example_long_operation': {time_taken:.6f} segundos.")

    print("\n--- Demostración de las Funciones Utilitarias finalizada ---")


# Esta línea asegura que la función demo_utils() se ejecute solo cuando el archivo
# 'utils.py' se corre directamente, no cuando se importa en otro script.
if __name__ == "__main__":
    demo_utils()