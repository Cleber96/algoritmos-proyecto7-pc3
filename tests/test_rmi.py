# tests/test_rmi.py

# Importamos las herramientas necesarias:
# pytest: El framework que usamos para escribir y ejecutar nuestras pruebas.
import pytest
# sys y os: Para ajustar las rutas de importación y que Python encuentre nuestros módulos.
import sys
import os

# Ajustamos la ruta para que Python pueda encontrar nuestros módulos
# ubicados en la carpeta 'src'. Esto es crucial para que las pruebas puedan
# importar correctamente las clases y funciones que van a probar.
script_dir = os.path.dirname(__file__) # Obtenemos la ruta del script actual (tests/)
project_root = os.path.abspath(os.path.join(script_dir, '..', '..')) # Subimos dos niveles para llegar a la raíz del proyecto
sys.path.insert(0, project_root) # Añadimos la raíz del proyecto al camino de búsqueda de módulos de Python.

# Importamos las clases y funciones de RMI que queremos probar.
from src.rmi.rmi_model import RMI
from src.rmi.utils import generate_sorted_data

# -----------------------------------------------------------------------------
# Pruebas Unitarias para el RMI (Recursive Model Index)
# -----------------------------------------------------------------------------
# ¿Qué son las pruebas unitarias y por qué son importantes para el RMI?
#
# Las pruebas unitarias son pequeñas verificaciones automáticas que confirman
# que cada "unidad" o componente de nuestro código (como una función o una clase)
# se comporta correctamente de forma aislada.
#
# Para el RMI, esto significa:
# - **Construcción Correcta:** ¿Se crea el RMI sin errores? ¿Tiene el número
#   correcto de modelos en cada nivel?
# - **Búsqueda Precisa:** ¿El RMI encuentra las claves que existen?
#   ¿Indica correctamente cuando una clave no existe?
# - **Rendimiento Básico:** Aunque los benchmarks miden el tiempo, las pruebas
#   aseguran que las operaciones básicas sean rápidas para casos pequeños.
#
# Cada función que comienza con `test_` será ejecutada por `pytest`.
# -----------------------------------------------------------------------------

# Una "fixture" en pytest es una función que proporciona datos o configuraciones
# comunes para varias pruebas. Aquí, generamos un dataset de ejemplo una vez
# y lo pasamos a todas las pruebas que lo necesiten, evitando duplicar código.
@pytest.fixture
def sample_rmi_data():
    """Proporciona un conjunto de datos ordenado para las pruebas del RMI."""
    # Generamos un conjunto de 1000 elementos ordenados.
    # Usamos un tamaño pequeño para que las pruebas sean rápidas.
    return generate_sorted_data(1000, 0, 2000)

@pytest.fixture
def trained_rmi(sample_rmi_data):
    """Crea y entrena una instancia de RMI con datos de ejemplo."""
    # Utilizamos los datos generados por la fixture 'sample_rmi_data'.
    # Configuramos el RMI con 10 modelos de Nivel 1 y un buffer de 10.
    # Estos parámetros son adecuados para un dataset de prueba.
    return RMI(sample_rmi_data, num_level1_models=10, search_buffer=10)

def test_rmi_initialization(sample_rmi_data):
    """
    Verifica que el RMI se inicialice correctamente.
    Nos aseguramos de que los modelos del Nivel 0 y Nivel 1 se creen.
    """
    print("\n--- Test: Inicialización del RMI ---")
    # Creamos una instancia de RMI. Si hay errores aquí, la prueba fallará.
    rmi = RMI(sample_rmi_data, num_level1_models=5, search_buffer=5)
    
    # Assertions: Son las "afirmaciones" que nuestra prueba hace. Si una afirmación
    # es falsa, la prueba falla.
    
    # Comprobamos que el modelo de Nivel 0 (el primer modelo) existe.
    assert rmi.level0_model is not None, "El modelo de Nivel 0 no debe ser None."
    # Comprobamos que la lista de modelos de Nivel 1 existe.
    assert rmi.level1_models is not None, "La lista de modelos de Nivel 1 no debe ser None."
    # Comprobamos que haya el número correcto de modelos en Nivel 1.
    assert len(rmi.level1_models) == 5, "Debería haber 5 modelos en Nivel 1."
    print("   Inicialización del RMI: OK")


def test_rmi_search_existing_key(trained_rmi, sample_rmi_data):
    """
    Verifica que el RMI pueda encontrar una clave que definitivamente existe
    en el conjunto de datos.
    """
    print("\n--- Test: Búsqueda de clave existente en RMI ---")
    # Tomamos una clave del medio del dataset para probar.
    # El RMI debería encontrarla o al menos estar muy cerca.
    key_to_find = sample_rmi_data[len(sample_rmi_data) // 2]
    
    # Realizamos la búsqueda.
    found_index = trained_rmi.search(key_to_find)
    
    # Afirmamos que se encontró un índice (no es None).
    assert found_index is not None, f"La clave {key_to_find} debería haber sido encontrada."
    # Afirmamos que el valor en el índice encontrado es realmente la clave que buscamos.
    assert sample_rmi_data[found_index] == key_to_find, \
           f"El valor encontrado {sample_rmi_data[found_index]} no coincide con la clave {key_to_find}."
    print(f"   Clave existente {key_to_find} encontrada correctamente en el RMI: OK")


def test_rmi_search_non_existing_key(trained_rmi, sample_rmi_data):
    """
    Verifica que el RMI devuelva None (o su equivalente) cuando la clave
    buscada no existe en el conjunto de datos.
    """
    print("\n--- Test: Búsqueda de clave NO existente en RMI ---")
    # Elegimos una clave que sabemos que no está en los datos.
    # Por ejemplo, un número muy grande o un número que esté entre dos elementos existentes
    # pero que no esté en la lista.
    non_existing_key_high = sample_rmi_data[-1] + 100 # Mayor que el último elemento
    non_existing_key_mid = sample_rmi_data[10] + 0.5 # Un valor decimal que no estaría en una lista de enteros, o un entero entre dos.
    # Para enteros, podemos tomar un valor entre dos consecutivos, si es que no se genera.
    if len(sample_rmi_data) > 1:
        non_existing_key_mid = sample_rmi_data[10] + 1 # Asumiendo que sorted_data[10]+1 no existe si los datos son consecutivos
        if non_existing_key_mid in sample_rmi_data: # Asegurarse de que no esté
             non_existing_key_mid = sample_rmi_data[10] + 2 # Ajustar si es necesario
    else:
        non_existing_key_mid = 10000000 # Un valor grande si el dataset es muy pequeño.


    # Probamos con una clave alta y que no existe.
    found_index_high = trained_rmi.search(non_existing_key_high)
    assert found_index_high is None, f"Clave no existente {non_existing_key_high} NO debe ser encontrada."
    print(f"   Clave no existente {non_existing_key_high} no encontrada: OK")

    # Probamos con una clave intermedia que no existe.
    found_index_mid = trained_rmi.search(non_existing_key_mid)
    assert found_index_mid is None, f"Clave no existente {non_existing_key_mid} NO debe ser encontrada."
    print(f"   Clave no existente {non_existing_key_mid} no encontrada: OK")


def test_rmi_empty_data():
    """
    Verifica que el RMI maneje correctamente un conjunto de datos vacío.
    Debería inicializarse sin problemas y no encontrar nada.
    """
    print("\n--- Test: RMI con datos vacíos ---")
    empty_data = []
    # La inicialización debería ocurrir sin errores.
    rmi = RMI(empty_data, num_level1_models=1, search_buffer=1)
    
    # Buscar en un RMI vacío siempre debe resultar en None.
    found_index = rmi.search(10)
    assert found_index is None, "Buscar en un RMI vacío siempre debe devolver None."
    print("   RMI con datos vacíos manejado correctamente: OK")

def test_rmi_single_element_data():
    """
    Verifica el comportamiento del RMI con un único elemento en el dataset.
    """
    print("\n--- Test: RMI con un solo elemento ---")
    single_element_data = [50]
    rmi = RMI(single_element_data, num_level1_models=1, search_buffer=1)
    
    # Buscar el elemento existente
    found_index_existing = rmi.search(50)
    assert found_index_existing is not None, "El único elemento debería ser encontrado."
    assert single_element_data[found_index_existing] == 50, "El valor encontrado debe coincidir."
    print("   Búsqueda de elemento único existente: OK")

    # Buscar un elemento no existente
    found_index_non_existing = rmi.search(100)
    assert found_index_non_existing is None, "Un elemento no existente no debe ser encontrado."
    print("   Búsqueda de elemento único no existente: OK")

# Cómo ejecutar estas pruebas:
# Abre tu terminal, navega a la carpeta 'algoritmos-proyecto7-pc3/'
# y ejecuta el comando: `pytest tests/test_rmi.py`
# O simplemente `pytest` para ejecutar todas las pruebas en la carpeta 'tests/'.