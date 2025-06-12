# src/rmi/rmi_model.py

# -----------------------------------------------------------------------------
# Implementaciones básicas sin librerías especializadas
# -----------------------------------------------------------------------------
# Para este proyecto, necesitamos algunas herramientas matemáticas básicas
# que normalmente encontraríamos en librerías como NumPy. Sin embargo,
# para cumplir con el requisito de "desde cero", las implementaremos aquí.
# -----------------------------------------------------------------------------

def _calculate_mean(data_list):
    """Calcula la media (promedio) de una lista de números."""
    if not data_list:
        return 0
    return sum(data_list) / len(data_list)

def _linear_regression_fit(x_values, y_values):
    """
    Ajusta un modelo de regresión lineal simple (y = mx + b)
    a los datos dados usando el método de Mínimos Cuadrados.
    Sin usar NumPy, solo operaciones básicas de Python.

    Args:
        x_values (list): Lista de valores de entrada (independientes).
        y_values (list): Lista de valores de salida (dependientes).

    Returns:
        tuple: (m, b) donde m es la pendiente y b es la intersección y.
               Retorna (0, 0) si hay datos insuficientes o un problema.
    """
    n = len(x_values)
    if n < 2: # Necesitamos al menos 2 puntos para definir una línea
        # Si solo hay un punto, asumimos una línea horizontal en ese punto.
        # Esto es una simplificación, en un caso real se manejaría mejor.
        if n == 1:
            return 0.0, float(y_values[0])
        return 0.0, 0.0 # No hay datos

    mean_x = _calculate_mean(x_values)
    mean_y = _calculate_mean(y_values)

    numerator = 0.0 # Numerador para calcular la pendiente (m)
    denominator = 0.0 # Denominador para calcular la pendiente (m)

    for i in range(n):
        numerator += (x_values[i] - mean_x) * (y_values[i] - mean_y)
        denominator += (x_values[i] - mean_x) ** 2

    if denominator == 0: # Si todos los x son iguales, la pendiente es indefinida o 0.
        # En este caso, la línea es vertical o no hay variación en X.
        # Asumimos una línea horizontal a la media de Y.
        return 0.0, mean_y
    
    m = numerator / denominator # Calculamos la pendiente
    b = mean_y - m * mean_x # Calculamos la intersección y

    return m, b

class SimpleLinearModel:
    """
    Una clase simple para representar un modelo lineal (y = mx + b).
    Sin dependencia de NumPy.
    """
    def __init__(self):
        self.m = 0.0 # Pendiente
        self.b = 0.0 # Intercepto

    def fit(self, x_values, y_values):
        """Ajusta el modelo lineal a los datos."""
        self.m, self.b = _linear_regression_fit(x_values, y_values)

    def predict(self, x):
        """Realiza una predicción usando el modelo."""
        return self.m * x + self.b

def _is_sorted(data_list):
    """Verifica si una lista está ordenada de forma ascendente."""
    for i in range(len(data_list) - 1):
        if data_list[i] > data_list[i+1]:
            return False
    return True

# -----------------------------------------------------------------------------
# Clase RMI (Recursive Model Index) - Implementación desde cero
# -----------------------------------------------------------------------------
# Un RMI es un índice que usa modelos de aprendizaje automático para predecir
# la ubicación de un dato en un conjunto de datos ordenado. En lugar de tablas
# o estructuras de árbol fijas, "aprende" dónde están los datos.
# Nuestro RMI será de dos niveles:
# Nivel 0: Un modelo general que toma una clave (el número que buscamos)
#          y predice aproximadamente en qué "segmento" del Nivel 1 buscar.
# Nivel 1: Múltiples modelos más pequeños, cada uno encargado de un segmento
#          específico de datos. Estos modelos predicen la posición exacta dentro
#          de su segmento.
# -----------------------------------------------------------------------------

class RMI:
    def __init__(self, data_list, num_level1_models, search_window_buffer=100):
        """
        Inicializa el Índice de Modelo Recursivo (RMI).

        Args:
            data_list (list): Una lista de enteros ORDENADA sobre la que se construirá el índice.
            num_level1_models (int): El número de modelos que se usarán en el Nivel 1.
                                     Más modelos pueden dar mayor precisión pero usan más memoria.
            search_window_buffer (int): Un "margen de seguridad" para la búsqueda lineal en el Nivel 1.
                                        Como el modelo puede no ser perfecto, buscamos unos pocos
                                        elementos antes y después de la posición predicha.
        """
        self.data = data_list # Guardamos una referencia a los datos originales.
        self.num_level1_models = num_level1_models # Cuántos "expertos" tendremos en el nivel 1.
        self.search_window_buffer = search_window_buffer # Cuántos elementos mirar alrededor de la predicción.

        # Paso crucial: Asegurarnos de que los datos estén ORDENADOS.
        # Si no lo están, un RMI no funcionará correctamente.
        if not _is_sorted(data_list):
            raise ValueError("Los datos deben estar ordenados para construir un RMI.")

        # Si no hay datos, no podemos construir el RMI.
        if not data_list:
            self.level0_model = None
            self.level1_models = []
            print("Advertencia: No hay datos para construir el RMI.")
            return

        # ---------------------------------------------------------------------
        # Paso 1: Entrenar el modelo del Nivel 0 (el "Maestro")
        # ---------------------------------------------------------------------
        # Este modelo es un "maestro" que aprende cómo se distribuyen los datos en general.
        # Su objetivo es, dada una clave (un número), predecir aproximadamente
        # a cuál de nuestros modelos de Nivel 1 (los "expertos") debemos ir.
        print("\n--- Iniciando el entrenamiento del RMI ---")
        print("1. Entrenando el modelo del Nivel 0 (el 'maestro')...")

        self.level0_model = SimpleLinearModel() # Creamos una instancia de nuestro modelo lineal simple.

        # Las "entradas" (X) para este modelo son las claves (los números) de nuestros datos.
        # Las "salidas" (Y) son los índices aproximados de los modelos del Nivel 1
        # a los que debería "dirigir" cada clave.
        # Distribuimos estos índices de 0 a (num_level1_models - 1) uniformemente.
        # Por ejemplo, si tenemos 1000 modelos de Nivel 1, el primer dato irá al índice 0,
        # el último dato irá al índice 999, y los intermedios se escalarán.
        x_level0 = data_list
        y_level0 = [i * (num_level1_models - 1) / (len(data_list) - 1) for i in range(len(data_list))]
        
        self.level0_model.fit(x_level0, y_level0) # Entrenamos el modelo.
        print(f"   Modelo del Nivel 0 entrenado: m={self.level0_model.m:.6f}, b={self.level0_model.b:.6f}")


        # ---------------------------------------------------------------------
        # Paso 2: Entrenar los modelos del Nivel 1 (los "Expertos de Segmento")
        # ---------------------------------------------------------------------
        # Ahora crearemos y entrenaremos múltiples modelos más pequeños.
        # Cada uno de estos "expertos" se encargará de una parte específica de los datos.
        print(f"\n2. Entrenando {num_level1_models} modelos en el Nivel 1 ('expertos')...")

        self.level1_models = [None] * num_level1_models # Creamos una lista vacía para guardar estos modelos.

        # Para saber qué datos le corresponden a cada modelo de Nivel 1,
        # primero obtenemos las predicciones del modelo del Nivel 0 para *cada clave original*.
        # Esto nos dirá a qué "segmento" (o modelo de Nivel 1) el modelo maestro cree que pertenece cada clave.
        level0_predictions_for_all_data = [self.level0_model.predict(x) for x in data_list]
        
        # Redondeamos y aseguramos que estas predicciones sean índices válidos (enteros y dentro de rango).
        level0_indices = []
        for pred in level0_predictions_for_all_data:
            idx = int(round(pred)) # Redondeamos al entero más cercano.
            # Aseguramos que el índice no se salga de los límites (0 a num_level1_models - 1).
            idx = max(0, min(idx, num_level1_models - 1))
            level0_indices.append(idx)

        # Ahora, necesitamos agrupar los datos para cada modelo de Nivel 1.
        # Creamos una lista de listas, donde cada sub-lista contendrá los pares (clave, posición)
        # para un modelo específico del Nivel 1.
        segment_data = [[] for _ in range(num_level1_models)]
        for i in range(len(data_list)):
            segment_data[level0_indices[i]].append((data_list[i], i)) # Guardamos (clave, posición real)

        # Iteramos sobre cada posible índice de modelo del Nivel 1.
        for i in range(num_level1_models):
            current_segment_pairs = segment_data[i] # Los (clave, posición) para este segmento.

            if len(current_segment_pairs) > 1: # Necesitamos al menos 2 puntos para entrenar una línea.
                # Extraemos las claves (X) y sus posiciones reales (Y) para este segmento.
                segment_keys = [pair[0] for pair in current_segment_pairs]
                segment_positions = [pair[1] for pair in current_segment_pairs]

                # Entrenamos un modelo lineal específico para este "experto" del segmento.
                model = SimpleLinearModel()
                model.fit(segment_keys, segment_positions)
                self.level1_models[i] = model # Guardamos el modelo entrenado.
            elif len(current_segment_pairs) == 1:
                # Si solo hay un punto en este segmento, no podemos entrenar una línea.
                # Creamos un modelo "tonto" que siempre predice la posición de ese único punto.
                model = SimpleLinearModel()
                model.m = 0.0 # Pendiente cero
                model.b = float(current_segment_pairs[0][1]) # Intercepto es la posición del único elemento
                self.level1_models[i] = model
            else:
                # Si no hay datos asignados a este modelo del Nivel 1, lo dejamos como None.
                # Esto puede pasar si los datos no están uniformemente distribuidos o si
                # el número de modelos de Nivel 1 es muy alto.
                self.level1_models[i] = None # No hay modelo para este segmento vacío.
            
            # Opcional: Imprimir el progreso para grandes cantidades de modelos
            # if (i + 1) % (num_level1_models // 10) == 0:
            #    print(f"   ... {i+1}/{num_level1_models} modelos de Nivel 1 entrenados.")

        print("--- Entrenamiento del RMI completado. ---")

    def search(self, key):
        """
        Busca una clave en el RMI y retorna su índice real en el array de datos.

        Args:
            key: La clave (número entero) a buscar.

        Returns:
            int or None: El índice de la clave en la lista 'data' si se encuentra,
                         o None si no se encuentra.
        """
        if not self.data:
            return None # No hay datos para buscar

        # ---------------------------------------------------------------------
        # Paso 1: Usar el modelo del Nivel 0 para obtener el índice del "Experto"
        # ---------------------------------------------------------------------
        # Le preguntamos al modelo maestro dónde cree que debería estar la clave.
        predicted_level1_float = self.level0_model.predict(key)
        
        # Redondeamos la predicción a un entero para obtener un índice de modelo.
        predicted_level1_idx = int(round(predicted_level1_float))
        
        # Aseguramos que este índice esté dentro de los límites válidos de nuestra lista de modelos de Nivel 1.
        predicted_level1_idx = max(0, min(predicted_level1_idx, self.num_level1_models - 1))

        # Obtenemos el modelo "experto" del Nivel 1 que el maestro nos indicó.
        level1_model = self.level1_models[predicted_level1_idx]

        # ---------------------------------------------------------------------
        # Paso 2: Usar el modelo del Nivel 1 para predecir la posición exacta
        # ---------------------------------------------------------------------
        # Si no hay un modelo en este segmento (porque no había datos para entrenarlo),
        # significa que la clave no puede estar en este segmento principal.
        if level1_model is None:
            # En un RMI real, se podría intentar buscar en segmentos adyacentes si
            # la predicción del Nivel 0 fue un poco errónea y el segmento vecino
            # sí tiene un modelo. Para esta implementación simple, retornamos None.
            return None
        
        # El modelo del Nivel 1 nos da una predicción de la posición *aproximada*
        # de la clave dentro de nuestro array de datos original.
        predicted_position_float = level1_model.predict(key)
        predicted_position = int(round(predicted_position_float))

        # ---------------------------------------------------------------------
        # Paso 3: Refinar la búsqueda con una "Ventana de Corrección"
        # ---------------------------------------------------------------------
        # Los modelos (especialmente los lineales simples) no son perfectos.
        # La predicción puede tener un pequeño error. Por eso, no vamos
        # directamente a la posición predicha, sino que buscamos en una
        # pequeña "ventana" (rango) alrededor de ella.
        
        # Calculamos el inicio y fin de nuestra ventana de búsqueda lineal.
        # Aseguramos que los índices no se salgan de los límites de nuestro array de datos.
        start_idx = max(0, predicted_position - self.search_window_buffer)
        end_idx = min(len(self.data) - 1, predicted_position + self.search_window_buffer)

        # Realizamos una búsqueda lineal (recorrido simple) dentro de esta pequeña ventana.
        # Como los datos están ordenados, esta búsqueda es muy rápida dentro de un rango pequeño.
        for i in range(start_idx, end_idx + 1):
            if self.data[i] == key:
                return i # ¡Encontramos la clave! Retornamos su posición real.
            elif self.data[i] > key:
                # Si el valor actual en la lista es mayor que la clave que buscamos,
                # y como la lista está ordenada, sabemos que la clave no puede estar
                # más adelante. Así que podemos detener la búsqueda aquí.
                return None
        
        # Si terminamos de recorrer la ventana y no encontramos la clave, significa que no está.
        return None

# -----------------------------------------------------------------------------
# Función de demostración para el RMI (Ejemplo de uso)
# -----------------------------------------------------------------------------
# Esta función es solo para probar el RMI. No forma parte de la clase en sí,
# pero nos ayuda a ver cómo funciona cuando se ejecuta este archivo directamente.
# -----------------------------------------------------------------------------

def demo_rmi():
    """
    Función de demostración para el RMI.
    Genera datos de ejemplo y muestra cómo se construye y busca en el RMI.
    """
    print("--- Demostración del Índice de Modelo Recursivo (RMI) ---")

    # 1. Generar datos de ejemplo
    # Como no usamos librerías externas, generamos los datos manualmente.
    # Para datasets grandes, esto puede ser lento o inviable sin NumPy.
    data_size = 1000 # Un tamaño pequeño para la demo sin NumPy.
    print(f"\n1. Generando datos de ejemplo (tamaño: {data_size:,})...")
    
    # Generamos una lista de números crecientes para simular datos ordenados.
    # Podríamos añadir un poco de aleatoriedad para que no sea perfectamente lineal,
    # pero manteniendo el orden.
    data = []
    current_val = 0
    for _ in range(data_size):
        data.append(current_val)
        current_val += int(1 + (abs(hash(_)) % 5)) # Añade un incremento semi-aleatorio
    
    print(f"   Datos generados (primeros 5): {data[:5]} ... (últimos 5): {data[-5:]}")
    print(f"   Verificando orden: {'Ordenado correctamente' if _is_sorted(data) else '¡ERROR: Datos no ordenados!'}")

    # 2. Inicializar y construir el RMI
    # Definimos el número de modelos en el Nivel 1 y la ventana de búsqueda.
    num_level1_models = 10 # Para este tamaño de datos, 10 modelos son suficientes para la demo.
    search_buffer = 10     # Buscar +/- 10 posiciones alrededor de la predicción.
    
    print(f"\n2. Construyendo RMI con {num_level1_models} modelos de Nivel 1 y buffer {search_buffer}...")
    
    # En una aplicación real, mediríamos el tiempo de construcción aquí.
    # Por ahora, simplemente llamamos al constructor.
    rmi_instance = RMI(data, num_level1_models, search_buffer)
    print("   RMI construido.")

    # 3. Realizar búsquedas de ejemplo
    print("\n3. Realizando búsquedas de ejemplo...")

    # Claves a buscar (algunas que existen, algunas que no)
    keys_to_find = [
        data[len(data) // 4],  # Un valor en el primer cuarto
        data[len(data) // 2],  # Un valor en el medio
        data[len(data) * 3 // 4], # Un valor en el tercer cuarto
        data[0],               # El primer valor
        data[-1],              # El último valor
        data[len(data) // 3 + 5], # Otro valor existente
        data[0] - 1,           # Un valor que no existe (menor que el mínimo)
        data[-1] + 1,          # Un valor que no existe (mayor que el máximo)
        data[len(data) // 2] + 1, # Un valor que podría no existir si es par
        99999999               # Un valor muy grande que definitivamente no existe
    ]

    for key in keys_to_find:
        # En una aplicación real, mediríamos el tiempo de búsqueda aquí.
        found_index = rmi_instance.search(key)
        
        if found_index is not None:
            # Si la clave fue encontrada, verificamos que el valor en el índice sea el correcto.
            print(f"   Buscando {key}: ENCONTRADO en índice {found_index}. Valor real: {rmi_instance.data[found_index]}")
            if rmi_instance.data[found_index] != key:
                print(f"     ERROR: El valor en el índice {found_index} NO COINCIDE con {key}!")
        else:
            print(f"   Buscando {key}: NO ENCONTRADO.")

    print("\n--- Demostración del RMI finalizada ---")

# Esta línea asegura que la función demo_rmi() se ejecute solo cuando el archivo
# 'rmi_model.py' se corre directamente, no cuando se importa en otro script.
if __name__ == "__main__":
    demo_rmi()