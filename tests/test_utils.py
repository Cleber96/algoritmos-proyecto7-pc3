# tests/test_utils.py

# Importamos las herramientas necesarias:
import pytest
import sys
import os
import time # Necesario para probar la función measure_time

# Ajustamos la ruta para que Python pueda encontrar nuestros módulos.
script_dir = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(script_dir, '..', '..'))
sys.path.insert(0, project_root)

# Importamos las funciones de utilidad que queremos probar.
from src.rmi.utils import generate_sorted_data, measure_time
from src.rmi.linear_model import LinearModel # Necesitamos LinearModel para un test de measure_time

# -----------------------------------------------------------------------------
# Pruebas Unitarias para las Utilidades Generales
# -----------------------------------------------------------------------------
# Las utilidades son funciones auxiliares que soportan a nuestros algoritmos.
# Aunque no son el "núcleo" del proyecto, es vital que funcionen correctamente.
#
# Para nuestras utilidades, esto significa:
# - **Generación de Datos:** ¿Los datos generados están ordenados y tienen el
#   tamaño y rango correctos?
# - **Medición de Tiempo:** ¿La función 'measure_time' mide el tiempo de forma
#   precisa y devuelve el resultado esperado?
# -----------------------------------------------------------------------------

def test_generate_sorted_data_size():
    """Verifica que generate_sorted_data cree un array del tamaño correcto."""
    print("\n--- Test: Tamaño de datos generados ---")
    size = 1000
    data = generate_sorted_data(size, 0, 10000)
    assert len(data) == size, f"El tamaño de los datos generados debería ser {size}."
    print(f"   Tamaño de los datos generados ({size}): OK")

def test_generate_sorted_data_order():
    """Verifica que generate_sorted_data cree un array ordenado."""
    print("\n--- Test: Orden de datos generados ---")
    data = generate_sorted_data(500, 0, 10000)
    # Comprobamos que cada elemento sea menor o igual que el siguiente.
    for i in range(len(data) - 1):
        assert data[i] <= data[i+1], "Los datos generados no están ordenados."
    print("   Orden de los datos generados: OK")

def test_generate_sorted_data_range():
    """Verifica que generate_sorted_data genere datos dentro del rango especificado."""
    print("\n--- Test: Rango de datos generados ---")
    min_val = 100
    max_val = 500
    data = generate_sorted_data(100, min_val, max_val)
    # Comprobamos que todos los elementos estén dentro del rango.
    for val in data:
        assert min_val <= val <= max_val, f"El valor {val} está fuera del rango [{min_val}, {max_val}]."
    # También, verificamos que el primer elemento no sea menor que min_val
    assert data[0] >= min_val, "El primer elemento es menor que min_val."
    # Y que el último elemento no sea mayor que max_val
    assert data[-1] <= max_val, "El último elemento es mayor que max_val."
    print(f"   Rango de los datos generados ({min_val}-{max_val}): OK")

def test_measure_time_accuracy():
    """Verifica que measure_time mida el tiempo de ejecución correctamente."""
    print("\n--- Test: Precisión de measure_time ---")
    # Definimos una función simple que tome un tiempo conocido.
    def dummy_function(duration_seconds):
        time.sleep(duration_seconds) # Pausa la ejecución por un tiempo.
        return "Done"

    expected_duration = 0.05 # 50 milisegundos

    # Medimos el tiempo de la función dummy.
    result, elapsed_time = measure_time(dummy_function, expected_duration)
    
    # Comprobamos que el resultado de la función sea el esperado.
    assert result == "Done", "La función dummy no devolvió el resultado esperado."
    # Comprobamos que el tiempo transcurrido esté cerca del esperado.
    # Usamos una tolerancia pequeña debido a la imprecisión de time.sleep y el scheduling del SO.
    assert elapsed_time >= expected_duration * 0.9 and elapsed_time <= expected_duration * 1.5, \
           f"El tiempo medido ({elapsed_time:.4f}s) no está dentro del rango esperado ({expected_duration}s)."
    print(f"   Precisión de measure_time: OK (medido: {elapsed_time:.4f}s, esperado: ~{expected_duration}s)")


def test_measure_time_with_class_method():
    """Verifica que measure_time funcione con métodos de una clase (como en RMI/BTree)."""
    print("\n--- Test: measure_time con método de clase ---")
    # Creamos una clase simple con un método para probar.
    class MyTestClass:
        def my_method(self, value):
            return value * 2

    instance = MyTestClass()
    
    # Medimos el tiempo de ejecución del método.
    result, elapsed_time = measure_time(instance.my_method, 5)
    
    assert result == 10, "El resultado del método de clase no es el esperado."
    assert elapsed_time >= 0, "El tiempo transcurrido debe ser no negativo."
    print("   measure_time con método de clase: OK")

def test_measure_time_with_no_args_function():
    """Verifica que measure_time funcione con funciones sin argumentos."""
    print("\n--- Test: measure_time con función sin argumentos ---")
    def no_arg_func():
        return True

    result, elapsed_time = measure_time(no_arg_func)
    
    assert result is True, "El resultado de la función sin argumentos no es el esperado."
    assert elapsed_time >= 0, "El tiempo transcurrido debe ser no negativo."
    print("   measure_time con función sin argumentos: OK")

# Cómo ejecutar estas pruebas:
# Abre tu terminal, navega a la carpeta 'algoritmos-proyecto7-pc3/'
# y ejecuta el comando: `pytest tests/test_utils.py`
# O simplemente `pytest` para ejecutar todas las pruebas en la carpeta 'tests/'.