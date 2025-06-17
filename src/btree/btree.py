class BTreeNode:
    """
    Representa un nodo dentro del B-Tree.
    Cada nodo contiene claves ordenadas y punteros a sus hijos.
    """
    def __init__(self, t, leaf=False):
        """
        Inicializa un nodo del B-Tree.

        Args:
            t (int): El "orden" mínimo del B-Tree.
                     Esto significa que cada nodo (excepto la raíz) debe tener
                     al menos (t-1) claves y 't' hijos.
                     Un nodo puede tener como máximo (2t-1) claves y (2t) hijos.
            leaf (bool): True si este nodo es una hoja (no tiene hijos), False en caso contrario.
        """
        self.t = t          # El orden mínimo del árbol.
        self.leaf = leaf    # Indica si este es un nodo hoja (True) o un nodo interno (False).
        self.keys = []      # Lista para almacenar las claves en este nodo, estarán ordenadas.
        self.children = []  # Lista para almacenar los nodos hijos (si no es una hoja).
        # Para un nodo con N claves, tendrá N+1 hijos.
        
        # Una bandera que nos ayudará a saber si el nodo está lleno, lo que
        # requerirá dividirlo antes de insertar.
        self.full = False # Se actualiza internamente si el número de claves llega a (2t - 1)

    def is_full(self):
        """Verifica si el nodo está lleno."""
        return len(self.keys) == (2 * self.t - 1)

    def __repr__(self):
        """Representación amigable del nodo para depuración."""
        return f"Node(keys={self.keys}, leaf={self.leaf})"


class BTree:
    """
    Implementa la estructura de datos B-Tree.
    """
    def __init__(self, t):
        """
        Inicializa el B-Tree.

        Args:
            t (int): El orden mínimo del B-Tree.
                     Un valor común es 2, 3 o 4 para demostraciones.
                     Un 't' más grande significa nodos más grandes y menos niveles.
        """
        self.t = t # El orden del B-Tree.
        # La raíz es el punto de entrada a nuestro árbol.
        # Inicialmente, el árbol está vacío, así que creamos una raíz que es también una hoja.
        self.root = BTreeNode(t, leaf=True)
        print(f"B-Tree inicializado con orden t={t}. Raíz creada.")

    # -------------------------------------------------------------------------
    # Operación de Búsqueda (Search)
    # -------------------------------------------------------------------------
    # La búsqueda en un B-Tree es similar a la de un árbol binario de búsqueda,
    # pero en lugar de solo dos caminos (izquierda o derecha), un nodo puede
    # tener múltiples caminos.
    # -------------------------------------------------------------------------
    def search(self, key, node=None):
        """
        Busca una clave en el B-Tree.

        Args:
            key: La clave a buscar.
            node (BTreeNode, opcional): El nodo desde el cual iniciar la búsqueda.
                                        Por defecto, comienza desde la raíz.

        Returns:
            tuple or None: Una tupla (nodo, índice_clave) si la clave es encontrada,
                           donde 'nodo' es el BTreeNode que contiene la clave y
                           'índice_clave' es la posición de la clave dentro de ese nodo.
                           Retorna None si la clave no se encuentra.
        """
        if node is None:
            node = self.root # Si no se especifica un nodo, empezamos desde la raíz.

        i = 0
        # Paso 1: Buscar la posición correcta de la clave dentro de las claves del nodo actual.
        # Recorremos las claves del nodo hasta encontrar una que sea igual o mayor que la clave buscada.
        while i < len(node.keys) and key > node.keys[i]:
            i += 1

        # Paso 2: Verificar si la clave fue encontrada en este nodo.
        if i < len(node.keys) and key == node.keys[i]:
            # ¡La clave fue encontrada en este nodo en la posición 'i'!
            print(f"  Búsqueda: Clave {key} encontrada en nodo con claves {node.keys} en índice {i}.")
            return (node, i) # Retornamos el nodo y el índice.

        # Paso 3: Si la clave no está en este nodo, decidir a qué hijo ir (si no es una hoja).
        if node.leaf:
            # Si somos una hoja y no encontramos la clave, significa que no está en el árbol.
            print(f"  Búsqueda: Clave {key} no encontrada (llegó a una hoja sin encontrarla).")
            return None
        else:
            # Si no somos una hoja, bajamos al hijo apropiado.
            # El hijo en la posición 'i' es el subárbol que contendría la clave.
            print(f"  Búsqueda: Clave {key} no en nodo {node.keys}, bajando al hijo {i}.")
            return self.search(key, node.children[i]) # Llamada recursiva al hijo.

    # -------------------------------------------------------------------------
    # Operación de Inserción (Insert)
    # -------------------------------------------------------------------------
    # La inserción en un B-Tree es más compleja que la búsqueda, porque debe
    # mantener las propiedades del árbol (especialmente el balanceo).
    # Si un nodo se llena durante la inserción, debe dividirse.
    # -------------------------------------------------------------------------
    def insert(self, key):
        """
        Inserta una nueva clave en el B-Tree.

        Args:
            key: La clave a insertar.
        """
        print(f"\n--- Insertando clave: {key} ---")
        root_node = self.root

        # Si la raíz está llena, el árbol necesita crecer en altura.
        # Esto ocurre antes de la inserción, para mantener la raíz no-llena
        # cuando la inserción final ocurre.
        if root_node.is_full():
            print(f"  Raíz {root_node.keys} está llena. Dividiendo la raíz para crecer el árbol.")
            # Creamos una nueva raíz que será un nodo interno.
            new_root = BTreeNode(self.t, leaf=False)
            new_root.children.append(root_node) # La vieja raíz se convierte en su primer hijo.
            self.root = new_root # Actualizamos la raíz del árbol.
            
            # Dividimos la vieja raíz. La clave media subirá a la nueva raíz.
            self._split_child(new_root, 0) # Dividimos el hijo 0 (la vieja raíz).
            
            # Ahora que la nueva raíz tiene un espacio, insertamos la clave.
            self._insert_non_full(new_root, key)
        else:
            # Si la raíz no está llena, podemos insertar directamente.
            self._insert_non_full(root_node, key)
        print(f"--- Clave {key} insertada. ---")

    def _insert_non_full(self, node, key):
        """
        Inserta una clave en un nodo que *no está lleno*.
        Este es un método auxiliar recursivo.

        Args:
            node (BTreeNode): El nodo en el que insertar (se asume que no está lleno).
            key: La clave a insertar.
        """
        i = len(node.keys) - 1 # Empezamos desde el final de las claves del nodo.

        if node.leaf:
            # Si el nodo es una hoja, significa que encontramos el lugar exacto para la clave.
            print(f"  Insertando {key} directamente en hoja {node.keys}.")
            # Movemos las claves existentes para hacer espacio a la nueva clave, manteniendo el orden.
            while i >= 0 and key < node.keys[i]:
                # Si 'i' es el último índice de la lista, debemos añadir un espacio.
                if i + 1 >= len(node.keys):
                    node.keys.append(node.keys[i])
                else:
                    node.keys[i + 1] = node.keys[i]
                i -= 1
            
            # Si 'i+1' es un índice válido para la nueva clave, lo insertamos.
            # Si 'i' se volvió -1, significa que la clave va al principio.
            if i + 1 >= len(node.keys): # Si necesitamos expandir la lista
                node.keys.append(key)
            else: # Si hay espacio o movemos un elemento
                node.keys.insert(i + 1, key)
            
        else:
            # Si el nodo no es una hoja, necesitamos encontrar el hijo adecuado para descender.
            # Buscamos la posición del hijo donde debería ir la clave.
            while i >= 0 and key < node.keys[i]:
                i -= 1
            i += 1 # 'i' ahora apunta al índice del hijo donde debemos descender.

            # Antes de descender al hijo, verificamos si ese hijo está lleno.
            if node.children[i].is_full():
                print(f"  Hijo {node.children[i].keys} está lleno. Dividiendo hijo {i}.")
                # Si el hijo está lleno, lo dividimos.
                # La clave media de ese hijo subirá al nodo actual.
                self._split_child(node, i)

                # Después de dividir, la clave que subió ha dividido el nodo actual.
                # Ahora tenemos que decidir en cuál de los dos nuevos hijos (el original o el nuevo)
                # debemos insertar la clave.
                # Si la clave es mayor que la clave que subió al nodo padre,
                # entonces la clave va al nuevo hijo de la derecha.
                if key > node.keys[i]:
                    i += 1 # Movemos al siguiente hijo (el nuevo)
            
            # Ahora que el hijo está garantizado no estar lleno (o ha sido dividido),
            # llamamos recursivamente para insertar en ese hijo.
            print(f"  Descendiendo a hijo {i} ({node.children[i].keys}) para insertar {key}.")
            self._insert_non_full(node.children[i], key)

    def _split_child(self, parent_node, child_index):
        """
        Divide un hijo de un nodo padre.
        Esta operación es fundamental para mantener el balanceo del B-Tree.
        Cuando un nodo hijo se llena, su clave media sube al padre,
        y el hijo se divide en dos nuevos nodos.

        Args:
            parent_node (BTreeNode): El nodo padre que tiene un hijo lleno.
            child_index (int): El índice del hijo lleno en la lista de hijos del padre.
        """
        # Obtenemos el nodo que está lleno y que vamos a dividir.
        child_node = parent_node.children[child_index]
        
        # Creamos un nuevo nodo hermano que recibirá la mitad derecha de las claves del nodo dividido.
        new_sibling_node = BTreeNode(self.t, leaf=child_node.leaf)

        # La clave media del nodo hijo subirá al nodo padre.
        # El índice de la clave media es t-1.
        median_key = child_node.keys[self.t - 1]
        print(f"    Clave media que sube al padre: {median_key}")

        # Movemos la mitad derecha de las claves del nodo hijo al nuevo nodo hermano.
        # Las claves desde el índice 't' hasta el final.
        new_sibling_node.keys = child_node.keys[self.t:]
        
        # Mantenemos solo la mitad izquierda de las claves en el nodo hijo original.
        # Las claves desde el inicio hasta el índice 't-1'.
        child_node.keys = child_node.keys[:self.t - 1]

        # Si el nodo que se está dividiendo no es una hoja, también debemos dividir sus hijos.
        if not child_node.leaf:
            # Movemos la mitad derecha de los hijos del nodo dividido al nuevo nodo hermano.
            # Los hijos desde el índice 't' hasta el final.
            new_sibling_node.children = child_node.children[self.t:]
            
            # Mantenemos solo la mitad izquierda de los hijos en el nodo hijo original.
            # Los hijos desde el inicio hasta el índice 't'.
            child_node.children = child_node.children[:self.t]

        # Ahora, insertamos la clave media (que subió) en el nodo padre.
        # Y también insertamos el nuevo nodo hermano en la lista de hijos del padre.

        # Primero, hacemos espacio para la nueva clave en el padre.
        # Empezamos desde el final de las claves del padre.
        i = len(parent_node.keys) - 1
        while i >= child_index and median_key < parent_node.keys[i]:
            # Movemos las claves a la derecha.
            if i + 1 >= len(parent_node.keys): # Si necesitamos expandir la lista
                parent_node.keys.append(parent_node.keys[i])
            else:
                parent_node.keys[i + 1] = parent_node.keys[i]
            i -= 1
        
        # Insertamos la clave media en su posición correcta en el padre.
        if i + 1 >= len(parent_node.keys):
            parent_node.keys.append(median_key)
        else:
            parent_node.keys.insert(i + 1, median_key)

        # Finalmente, insertamos el nuevo nodo hermano en la lista de hijos del padre.
        # Va justo después del hijo original que se dividió.
        parent_node.children.insert(child_index + 1, new_sibling_node)

        print(f"    Nodo padre actualizado: {parent_node.keys}. Hijos: {[c.keys for c in parent_node.children]}")


    # -------------------------------------------------------------------------
    # Visualización (Opcional, para entender la estructura)
    # -------------------------------------------------------------------------
    # Aunque no es parte del algoritmo central, una función para imprimir
    # el árbol es muy útil para depurar y entender cómo se ve la estructura.
    # -------------------------------------------------------------------------
    def print_tree(self, node=None, level=0):
        """
        Imprime la estructura del B-Tree de forma legible para visualización.
        """
        if node is None:
            node = self.root
            print("\n--- Estructura del B-Tree ---")

        indent = "  " * level # Para crear la indentación de los niveles.
        node_type = "Hoja" if node.leaf else "Interno"
        print(f"{indent}Nivel {level} ({node_type}): Claves {node.keys}")

        if not node.leaf:
            # Si no es una hoja, recursivamente imprimimos sus hijos.
            for i, child in enumerate(node.children):
                print(f"{indent}  Hijo {i}:")
                self.print_tree(child, level + 1)
        
        if level == 0:
            print("--- Fin de la estructura del B-Tree ---")


# -----------------------------------------------------------------------------
# Función de Demostración para el B-Tree (Ejemplo de uso)
# -----------------------------------------------------------------------------
# Esta función nos permite ver el B-Tree en acción, insertando elementos
# y luego buscándolos.
# -----------------------------------------------------------------------------

def demo_btree():
    """
    Función de demostración para el B-Tree.
    Crea un B-Tree, inserta algunas claves y luego realiza búsquedas.
    """
    print("--- Demostración del B-Tree ---")

    # Definimos el orden de nuestro B-Tree.
    # Un orden t=2 significa:
    # - Cada nodo (excepto la raíz) debe tener al menos 1 clave y 2 hijos.
    # - Cada nodo puede tener como máximo 3 claves y 4 hijos.
    btree_order_t = 2
    my_btree = BTree(btree_order_t)

    # Claves para insertar en el B-Tree.
    # Observa cómo el árbol se reestructura a medida que insertamos.
    keys_to_insert = [10, 20, 5, 30, 15, 25, 35, 2, 7, 12, 18, 22, 28, 32, 38, 1, 3]

    for key in keys_to_insert:
        my_btree.insert(key)
        # my_btree.print_tree() # Descomentar para ver el árbol después de cada inserción.

    print("\n--- B-Tree final después de todas las inserciones ---")
    my_btree.print_tree() # Imprimimos la estructura final del árbol.

    print("\n--- Realizando búsquedas en el B-Tree ---")
    keys_to_search = [15, 25, 10, 1, 38, 99, 0, 21] # Claves existentes y no existentes.

    for key in keys_to_search:
        result = my_btree.search(key)
        if result:
            node_found, index_found = result
            print(f"  Clave {key} encontrada. Está en el nodo con claves {node_found.keys} en la posición (índice) {index_found}.")
        else:
            print(f"  Clave {key} NO encontrada en el B-Tree.")
    
    print("\n--- Demostración del B-Tree finalizada ---")

# Esta línea asegura que la función demo_btree() se ejecute solo cuando el archivo
# 'btree.py' se corre directamente, no cuando se importa en otro script.
if __name__ == "__main__":
    demo_btree()