# tests/test_btree.py

# Importamos las herramientas necesarias:
import pytest
import sys
import os

# Ajustamos la ruta para que Python pueda encontrar nuestros módulos.
script_dir = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(script_dir, '..', '..'))
sys.path.insert(0, project_root)

# Importamos la clase BTree que queremos probar.
from src.btree.btree import BTree

# -----------------------------------------------------------------------------
# Pruebas Unitarias para el B-Tree
# -----------------------------------------------------------------------------
# Para el B-Tree, las pruebas unitarias son esenciales para verificar:
# - **Inicialización:** ¿Se crea el árbol correctamente con el orden especificado?
# - **Inserción:** ¿Se añaden los elementos correctamente? ¿El árbol se reestructura
#   (se divide, etc.) como se espera cuando los nodos se llenan?
# - **Búsqueda:** ¿Encuentra las claves existentes? ¿Maneja las claves no existentes?
# - **Balanceo:** Aunque no lo probaremos explícitamente aquí, las inserciones
#   deberían mantener el árbol balanceado según las reglas del B-Tree.
# -----------------------------------------------------------------------------

@pytest.fixture
def empty_btree():
    """Proporciona un B-Tree vacío de orden 3 para las pruebas."""
    # Un orden de 3 significa que cada nodo tendrá entre t-1=2 y 2t-1=5 claves,
    # y entre t=3 y 2t=6 hijos.
    return BTree(order=3)

@pytest.fixture
def small_populated_btree():
    """Proporciona un B-Tree pequeño con algunos elementos para pruebas de búsqueda."""
    btree = BTree(order=3)
    # Insertamos un conjunto de claves ordenadas para facilitar la verificación.
    keys = [10, 20, 30, 5, 15, 25, 35, 2, 7, 12, 18]
    for key in keys:
        btree.insert(key)
    return btree

def test_btree_initialization():
    """Verifica que el B-Tree se inicialice correctamente con el orden dado."""
    print("\n--- Test: Inicialización del B-Tree ---")
    tree = BTree(order=3)
    # Aseguramos que la raíz exista y sea una hoja al principio.
    assert tree.root is not None, "La raíz del B-Tree no debe ser None."
    assert tree.root.leaf is True, "La raíz debe ser una hoja al inicializar."
    assert tree.order == 3, "El orden del B-Tree debe ser 3."
    assert len(tree.root.keys) == 0, "La raíz debe estar vacía al inicializar."
    print("   Inicialización del B-Tree: OK")

def test_btree_insert_single_element(empty_btree):
    """Verifica la inserción de un solo elemento."""
    print("\n--- Test: Inserción de un solo elemento ---")
    empty_btree.insert(10)
    assert len(empty_btree.root.keys) == 1, "La raíz debe tener 1 clave después de insertar."
    assert empty_btree.root.keys[0] == 10, "La clave insertada debe ser 10."
    print("   Inserción de un solo elemento: OK")

def test_btree_insert_multiple_elements(empty_btree):
    """Verifica la inserción de múltiples elementos y la división de nodos."""
    print("\n--- Test: Inserción de múltiples elementos y división de nodos ---")
    # Insertamos elementos para forzar la división del nodo raíz.
    # Orden 3: máx 5 claves por nodo. La sexta clave debería forzar la división.
    keys = [10, 20, 30, 40, 50, 60]
    for i, key in enumerate(keys):
        empty_btree.insert(key)
        # print(f"   Después de insertar {key}:")
        # empty_btree.print_tree() # Descomenta para depurar
    
    # Después de insertar 60 (la sexta clave para t=3), el nodo raíz debería dividirse.
    # Esto significa que el árbol debería tener una altura mayor a 1,
    # y la raíz ya no debería ser una hoja.
    assert not empty_btree.root.leaf, "La raíz ya no debe ser una hoja después de divisiones."
    assert len(empty_btree.root.keys) == 1, "La nueva raíz debe tener 1 clave (la clave media)."
    assert empty_btree.root.keys[0] == 30, "La clave promovida a la raíz debe ser 30."
    print("   Inserción de múltiples elementos y división de nodos: OK")

def test_btree_search_existing_key(small_populated_btree):
    """Verifica que el B-Tree pueda encontrar una clave existente."""
    print("\n--- Test: Búsqueda de clave existente en B-Tree ---")
    keys_to_check = [5, 15, 25, 35, 18, 10]
    for key in keys_to_check:
        result = small_populated_btree.search(key)
        assert result is not None, f"La clave {key} debería ser encontrada."
        node, index = result
        assert node.keys[index] == key, f"El valor encontrado ({node.keys[index]}) no coincide con la clave buscada ({key})."
        print(f"   Clave existente {key} encontrada: OK")

def test_btree_search_non_existing_key(small_populated_btree):
    """Verifica que el B-Tree no encuentre una clave que no existe."""
    print("\n--- Test: Búsqueda de clave NO existente en B-Tree ---")
    keys_to_check = [1, 13, 22, 40, 100]
    for key in keys_to_check:
        result = small_populated_btree.search(key)
        assert result is None, f"La clave {key} NO debería ser encontrada."
        print(f"   Clave no existente {key} no encontrada: OK")

def test_btree_empty_tree_search(empty_btree):
    """Verifica que la búsqueda en un árbol vacío devuelva None."""
    print("\n--- Test: Búsqueda en un B-Tree vacío ---")
    result = empty_btree.search(10)
    assert result is None, "La búsqueda en un árbol vacío debe devolver None."
    print("   Búsqueda en B-Tree vacío: OK")

# Cómo ejecutar estas pruebas:
# Abre tu terminal, navega a la carpeta 'algoritmos-proyecto7-pc3/'
# y ejecuta el comando: `pytest tests/test_btree.py`
# O simplemente `pytest` para ejecutar todas las pruebas en la carpeta 'tests/'.