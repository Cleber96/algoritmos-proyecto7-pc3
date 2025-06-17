class LinearModel:
    """
    Implementa un modelo de regresión lineal simple (y = mx + b)
    utilizando el método de Mínimos Cuadrados.
    """
    def __init__(self):
        """
        Inicializa el modelo lineal.
        Por defecto, la pendiente (m) y el intercepto (b) son cero.
        Estos valores se calcularán cuando se "entrene" el modelo.
        """
        self.m = 0.0 # La pendiente de nuestra línea.
        self.b = 0.0 # El punto donde la línea cruza el eje Y.

    def fit(self, x_values, y_values):
        """
        Entrena el modelo lineal ajustando la línea a los datos proporcionados.
        Este proceso calcula los valores óptimos de 'm' y 'b' usando el método
        de Mínimos Cuadrados.

        Args:
            x_values (list): Una lista de números que representan las entradas (variables independientes).
            y_values (list): Una lista de números que representan las salidas (variables dependientes)
                             que corresponden a cada 'x_value'.
        """
        n = len(x_values)

        # ---------------------------------------------------------------------
        # Paso 1: Manejar casos especiales para pocos datos
        # ---------------------------------------------------------------------
        # Si no tenemos suficientes puntos de datos, no podemos calcular una línea.
        if n == 0:
            self.m = 0.0
            self.b = 0.0
            # No podemos entrenar sin datos.
            return
        elif n == 1:
            # Si solo tenemos un punto, la "línea" es un punto.
            # Podemos definirla como una línea horizontal que pasa por 'y_values[0]'.
            self.m = 0.0
            self.b = float(y_values[0])
            return

        # ---------------------------------------------------------------------
        # Paso 2: Calcular las medias (promedios) de X e Y
        # ---------------------------------------------------------------------
        # La media es el punto central de nuestros datos.
        # Es el primer paso para calcular la relación entre X e Y.
        sum_x = sum(x_values)
        sum_y = sum(y_values)
        mean_x = sum_x / n
        mean_y = sum_y / n

        # ---------------------------------------------------------------------
        # Paso 3: Calcular la pendiente (m) y el intercepto (b)
        # ---------------------------------------------------------------------
        # El método de Mínimos Cuadrados busca minimizar la distancia vertical
        # entre cada punto de datos y la línea. Los cálculos se basan en la
        # "covarianza" (cómo X e Y varían juntas) y la "varianza" de X.

        numerator = 0.0   # Suma de (x_i - media_x) * (y_i - media_y)
        denominator = 0.0 # Suma de (x_i - media_x)^2

        for i in range(n):
            # Calculamos la diferencia de cada punto con respecto a su media.
            diff_x = x_values[i] - mean_x
            diff_y = y_values[i] - mean_y
            
            # Sumamos para el numerador y el denominador.
            numerator += diff_x * diff_y
            denominator += diff_x * diff_x

        # Si el denominador es cero, significa que todos los valores de 'x' son iguales.
        # En este caso, la línea es vertical (pendiente infinita) o es una línea
        # horizontal que pasa por la media de Y. Como nuestra ecuación es y=mx+b,
        # no podemos representar una línea vertical. Asumimos una horizontal.
        if denominator == 0:
            self.m = 0.0
            self.b = mean_y
        else:
            self.m = numerator / denominator # Calculamos la pendiente 'm'.
            # Una vez que tenemos 'm', podemos calcular 'b' usando las medias.
            self.b = mean_y - self.m * mean_x

        # Ahora, 'self.m' y 'self.b' contienen los mejores valores para nuestra línea.

    def predict(self, x):
        """
        Usa el modelo entrenado para predecir un valor 'y' dado un valor 'x'.

        Args:
            x (float or int): El valor de entrada para el cual queremos una predicción.

        Returns:
            float: El valor 'y' predicho por el modelo lineal.
        """
        # Simplemente aplicamos la ecuación de la línea que aprendimos.
        return self.m * x + self.b

# -----------------------------------------------------------------------------
# Función de demostración para el Modelo Lineal (Ejemplo de uso)
# -----------------------------------------------------------------------------
# Esta función es solo para probar la clase LinearModel. No forma parte
# de la clase en sí, pero nos ayuda a ver cómo funciona cuando se ejecuta
# este archivo directamente.
# -----------------------------------------------------------------------------

def demo_linear_model():
    """
    Demuestra cómo se entrena y usa un SimpleLinearModel.
    """
    print("--- Demostración del Modelo Lineal Simple (y = mx + b) ---")

    # Datos de ejemplo: Queremos predecir 'y' basándonos en 'x'.
    # Imagina que 'x' podría ser la cantidad de estudio (horas)
    # y 'y' podría ser la nota obtenida.
    x_data = [1, 2, 3, 4, 5, 6, 7]  # Horas de estudio
    y_data = [2, 4, 5, 4, 6, 7, 8]  # Notas obtenidas

    print(f"\nDatos de entrada (x): {x_data}")
    print(f"Datos de salida (y):   {y_data}")

    # 1. Crear una instancia de nuestro modelo lineal
    print("\n1. Creando una instancia del modelo lineal...")
    model = LinearModel()
    print(f"   Valores iniciales: m={model.m}, b={model.b}")

    # 2. Entrenar el modelo con nuestros datos
    print("\n2. Entrenando el modelo con los datos...")
    model.fit(x_data, y_data)
    print(f"   Modelo entrenado: m={model.m:.4f}, b={model.b:.4f}")
    print("   Esto significa que nuestra línea es aproximadamente: y = {model.m:.4f}x + {model.b:.4f}")

    # 3. Hacer predicciones usando el modelo entrenado
    print("\n3. Haciendo predicciones con el modelo entrenado...")
    
    test_x_values = [0, 2.5, 8, 10] # Horas de estudio para las que queremos predicciones
    
    for x_val in test_x_values:
        predicted_y = model.predict(x_val)
        print(f"   Si x = {x_val}, y (predicción) = {predicted_y:.4f}")

    # Visualización (requeriría una librería como Matplotlib, no incluida aquí)
    # Si tuvieras Matplotlib, podrías hacer algo como:
    # import matplotlib.pyplot as plt
    # plt.scatter(x_data, y_data, label='Datos Reales')
    # plt.plot(x_data, [model.predict(x) for x in x_data], color='red', label='Línea de Regresión')
    # plt.xlabel('X (Entrada)')
    # plt.ylabel('Y (Salida)')
    # plt.title('Regresión Lineal Simple')
    # plt.legend()
    # plt.grid(True)
    # plt.show()

    print("\n--- Demostración del Modelo Lineal Simple finalizada ---")

# Esta línea asegura que la función demo_linear_model() se ejecute solo cuando el archivo
# 'linear_model.py' se corre directamente, no cuando se importa en otro script.
if __name__ == "__main__":
    demo_linear_model()