# demos/demo_btree.py

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

# Ahora importamos nuestra implementación desde 'src':
from src.btree.btree import BTree # Nuestra implementación del B-Tree
from src.rmi.utils import generate_sorted_data # Nuestra utilidad para generar datos ordenados

# -----------------------------------------------------------------------------
# Demostración del B-Tree (Árbol B)
# -----------------------------------------------------------------------------
# Un B-Tree es una estructura de datos tipo árbol muy utilizada para organizar
# grandes volúmenes de información, especialmente en bases de datos y sistemas
# de archivos. Su principal característica es que sus "ramas" (nodos) pueden
# tener muchos "hijos", lo que lo hace muy eficiente para buscar datos.
#
# A diferencia de un árbol binario (que tiene 2 hijos por nodo), un B-Tree
# puede tener muchos más. Esto reduce la "altura" del árbol, es decir,
# cuántos "saltos" hay que dar desde el principio hasta el final para encontrar
# un dato. Menos saltos significan búsquedas más rápidas.
#
# La propiedad clave del B-Tree es que siempre se mantiene "balanceado",
# lo que significa que el tiempo de búsqueda es casi siempre el mismo,
# sin importar dónde esté el dato o cuántos datos haya.
# -----------------------------------------------------------------------------

def demo_btree():
    """
    Función principal de demostración para el B-Tree.
    Crea un B-Tree, inserta elementos y realiza búsquedas.
    """
    print("--- INICIANDO DEMOSTRACIÓN DEL B-TREE ---")

    # 1. Inicializar el B-Tree:
    # Definimos el "orden" (t) de nuestro B-Tree.
    # El orden 't' controla cuántas claves y cuántos hijos puede tener cada nodo.
    # Un 't' de 3 significa que un nodo puede tener de 2 a 5 claves y de 3 a 6 hijos.
    btree_order_t = 3 
    print(f"\n1. Inicializando el B-Tree con orden t = {btree_order_t}...")
    my_btree = BTree(btree_order_t)
    print("   B-Tree creado. Inicialmente está vacío.")

    # 2. Insertar elementos en el B-Tree:
    # A diferencia del RMI que se construye sobre datos ya existentes,
    # en un B-Tree, los elementos se insertan uno por uno.
    # Vamos a usar un conjunto pequeño para poder visualizar mejor cómo crece el árbol.
    keys_to_insert = [10, 20, 5, 30, 15, 25, 35, 2, 7, 12, 18, 22, 28, 32, 38, 1, 3, 40, 42, 45, 47, 49, 50]
    
    print("\n2. Insertando elementos en el B-Tree (observa cómo se reestructura):")
    for i, key in enumerate(keys_to_insert):
        print(f"   Insertando clave: {key} (Elemento {i+1}/{len(keys_to_insert)})")
        my_btree.insert(key)
        # my_btree.print_tree() # Descomenta esta línea para ver el árbol después de cada inserción.
        #                     # ¡Cuidado! Para muchos elementos, esto imprimirá mucho texto.

    print("\n   Todos los elementos han sido insertados.")
    print("\n--- Estructura final del B-Tree después de todas las inserciones ---")
    my_btree.print_tree() # Imprimimos la estructura completa del árbol al final.

    # 3. Realizar búsquedas:
    # Ahora que el B-Tree está construido, vamos a buscar algunas claves.
    
    print("\n3. Realizando búsquedas en el B-Tree:")
    
    # Claves para buscar (algunas existen, otras no)
    keys_to_search = [15, 25, 10, 1, 38, 99, 0, 21, 50, 41] 

    for key in keys_to_search:
        print(f"\n   Buscando clave: {key}")
        # El método 'search' del B-Tree devolverá el nodo y el índice si encuentra la clave.
        result = my_btree.search(key)
        if result:
            node_found, index_found = result
            print(f"     -> ¡Clave {key} encontrada!")
            print(f"        Está en el nodo con claves {node_found.keys} en la posición (índice) {index_found}.")
        else:
            print(f"     -> Clave {key} NO encontrada en el B-Tree. (Esto es correcto si la clave no fue insertada).")
    
    print("\n--- DEMOSTRACIÓN DEL B-TREE FINALIZADA ---")

# Este bloque asegura que la función demo_btree() se ejecute solo cuando
# este archivo se corre directamente, no cuando es importado por otro script.
if __name__ == "__main__":
    demo_btree()