def _normalize_values(values, scale_factor=50):
    """
    Normaliza una lista de valores para que se ajusten a una escala de visualización.
    Esto es útil para que los gráficos de barras no se salgan de la pantalla.

    Args:
        values (list): La lista de números a normalizar.
        scale_factor (int): El ancho máximo deseado para la barra de gráfico.

    Returns:
        list: Una lista de valores normalizados (escalados).
    """
    if not values:
        return []

    # Encontramos el valor máximo para escalar proporcionalmente.
    max_val = max(values)
    if max_val == 0: # Evitar división por cero
        return [0] * len(values)
    
    # Escalamos cada valor. Multiplicamos por scale_factor para que el máximo
    # sea igual a 'scale_factor' (o cercano, si redondeamos).
    normalized_values = [int((val / max_val) * scale_factor) for val in values]
    return normalized_values


def plot_bar_chart_ascii(title, labels, values1, label1, values2, label2):
    """
    Genera un gráfico de barras simple usando caracteres ASCII para comparar dos conjuntos de datos.

    Args:
        title (str): El título del gráfico.
        labels (list): Etiquetas para cada barra (e.g., tamaños de datos).
        values1 (list): Valores para el primer conjunto de datos (e.g., tiempos del RMI).
        label1 (str): Etiqueta para el primer conjunto de datos (e.g., "RMI").
        values2 (list): Valores para el segundo conjunto de datos (e.g., tiempos del B-Tree).
        label2 (str): Etiqueta para el segundo conjunto de datos (e.g., "B-Tree").
    """
    print(f"\n{'-' * 10} {title.upper()} {'-' * 10}")

    # Normalizamos los valores para que el gráfico no sea demasiado ancho.
    # Hacemos una lista combinada para normalizar ambos conjuntos a la misma escala.
    all_values = values1 + values2
    normalized_all_values = _normalize_values(all_values, scale_factor=60) # Ancho máximo de la barra

    # Dividimos los valores normalizados de nuevo.
    normalized_values1 = normalized_all_values[:len(values1)]
    normalized_values2 = normalized_all_values[len(values1):]

    # Encontramos el ancho máximo de las etiquetas para alinear bien.
    max_label_len = max(len(str(label)) for label in labels) if labels else 0
    max_val_str_len = max(len(f"{max(values1 + values2):.6f}"), len(f"{min(values1 + values2):.6f}")) if all_values else 0

    print(f"  (Escala relativa: Cada '#' representa una porción del valor máximo en este gráfico.)")
    
    # Imprimimos la leyenda
    print(f"  Leyenda: {label1} = # {label2} = *")

    for i in range(len(labels)):
        label = str(labels[i]).ljust(max_label_len) # Alinea la etiqueta a la izquierda
        
        # Formateamos los valores numéricos originales para que sean legibles
        val1_str = f"{values1[i]:.6f}".ljust(max_val_str_len)
        val2_str = f"{values2[i]:.6f}".ljust(max_val_str_len)

        # Creamos las barras usando '#' y '*'
        bar1 = '#' * normalized_values1[i]
        bar2 = '*' * normalized_values2[i]

        print(f"\n{label} | {label1}: [{bar1}] {val1_str}")
        print(f"{' ' * (max_label_len + 3)}| {label2}: [{bar2}] {val2_str}")
    
    print(f"{'-' * (25 + max_label_len + max_val_str_len)}") # Línea de cierre


# -----------------------------------------------------------------------------
# Función Principal para Generar Visualizaciones
# -----------------------------------------------------------------------------
# Esta función es la que llamaremos desde el script de benchmarking.
# -----------------------------------------------------------------------------

def generate_visualizations(benchmark_results):
    """
    Toma los resultados de los benchmarks y genera diferentes visualizaciones
    (gráficos de barras ASCII).

    Args:
        benchmark_results (dict): Un diccionario que contiene los resultados
                                  de los benchmarks (tiempos, memoria, etc.).
    """
    print("\n--- GENERANDO VISUALIZACIONES ---")

    data_sizes_labels = [f"Tamaño: {s:,}" for s in benchmark_results['data_sizes']]

    # 1. Gráfico de Tiempos de Construcción
    plot_bar_chart_ascii(
        "Tiempos de Construcción de Índices",
        data_sizes_labels,
        benchmark_results['rmi_build_times'], "RMI",
        benchmark_results['btree_build_times'], "B-Tree"
    )

    # 2. Gráfico de Tiempos Promedio de Búsqueda
    plot_bar_chart_ascii(
        "Tiempos Promedio de Búsqueda",
        data_sizes_labels,
        benchmark_results['rmi_search_times'], "RMI",
        benchmark_results['btree_search_times'], "B-Tree"
    )

    # 3. Gráfico de Uso de Memoria Estimado
    plot_bar_chart_ascii(
        "Uso de Memoria Estimado",
        data_sizes_labels,
        benchmark_results['rmi_memory_usage'], "RMI",
        benchmark_results['btree_memory_usage'], "B-Tree"
    )

    print("\n--- VISUALIZACIONES COMPLETADAS ---")


# Este bloque se ejecuta solo si el archivo 'visualizations.py' se corre directamente.
# Es útil para una demostración independiente si no se tienen los resultados
# del benchmarking ya listos.
if __name__ == "__main__":
    print("Este script generalmente se ejecuta después de 'run_benchmark.py'.")
    print("Generando datos de ejemplo para la demostración de visualización.")

    # Generamos datos de ejemplo (esto no es real, solo para probar los gráficos)
    example_results = {
        'data_sizes': [1000, 5000, 10000, 20000],
        'rmi_build_times': [0.01, 0.05, 0.12, 0.25],
        'rmi_search_times': [0.000001, 0.000002, 0.000003, 0.000004],
        'rmi_memory_usage': [20, 20, 20, 20], # RMI usa memoria constante para modelos
        'btree_build_times': [0.02, 0.15, 0.5, 1.2],
        'btree_search_times': [0.000005, 0.000007, 0.000009, 0.000011],
        'btree_memory_usage': [100, 500, 1000, 2000] # B-Tree usa más memoria con más datos
    }

    generate_visualizations(example_results)
    print("\nDemostración de visualizaciones con datos de ejemplo finalizada.")