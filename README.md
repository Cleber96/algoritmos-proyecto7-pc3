# Proyecto: Recursive Model Index (RMI) sobre array de enteros con comparativa a B-Tree

## Estructura del proyecto (carpetas y archivos)

```bash
rmi_vs_btree_project/
├── README.md                         # Documentación principal del proyecto
├── requirements.txt                 # Dependencias del proyecto (si aplica)
├── setup.py                         # Script de instalación (opcional)
├── src/                             # Código fuente principal
│   ├── __init__.py
│   ├── rmi/                         # Módulo de RMI
│   │   ├── __init__.py
│   │   ├── rmi_model.py            # Implementación del modelo RMI
│   │   ├── linear_model.py         # Ajuste de mínimos cuadrados
│   │   └── utils.py                # Utilidades generales
│   ├── btree/                      # Módulo de B-Tree
│   │   ├── __init__.py
│   │   └── btree.py                # Implementación de B-Tree
│   └── benchmark/                  # Benchmark y análisis comparativo
│       ├── __init__.py
│       ├── run_benchmark.py       # Script de benchmarking general
│       └── visualizations.py      # Gráficas y visualización de resultados
├── tests/                           # Pruebas unitarias
│   ├── __init__.py
│   ├── test_rmi.py
│   ├── test_btree.py
│   └── test_utils.py
├── demos/                           # Casos de uso demostrativos
│   ├── demo_rmi.py
│   └── demo_btree.py
├── profiling/                       # Scripts para análisis de rendimiento
│   └── profile_memory_time.py
├── docs/
│   ├── informe_tecnico.pdf         # Informe técnico final (3–5 páginas)
│   ├── presentacion.pdf            # Presentación para exposición
│   └── referencias.bib             # Bibliografía en BibTeX (opcional)
├── data/                            # Datos sintéticos o reales
│   └── sample_dataset.npy
└── notebook/                        # Jupyter Notebooks explicativos del desarrollo
    ├── 01_rmi_model.ipynb          # Construcción detallada de rmi_model.py
    ├── 02_linear_model.ipynb       # Entrenamiento y ajuste de modelos lineales
    ├── 03_utils.ipynb              # Funciones auxiliares de soporte
    ├── 04_btree.ipynb              # Desarrollo paso a paso del B-Tree
    ├── 05_benchmarking.ipynb       # Explicación de pruebas comparativas
    └── 06_visualizations.ipynb     # Generación y explicación de gráficas de resultados
```

---

## Detalles a investigar y desarrollar paso a paso

### 1. Implementación funcional y optimización del RMI

* **Investigar:**

  * Qué es un Recursive Model Index (RMI) y sus niveles (Aprendizaje clásico: Kraska et al.).
  * Modelos lineales simples y su entrenamiento por mínimos cuadrados (regresión lineal básica).
  * Cómo dividir el array ordenado en tramos óptimos para los modelos del segundo nivel.
* **Desarrollar:**

  * Clase `RMIModel` con `fit(array)`, `predict(key)` y `insert(key)` (si aplica).
  * Clase auxiliar `LinearModel` con método de ajuste por mínimos cuadrados.
  * Módulo `utils.py` para manejo de errores y división de segmentos.

### 2. Implementación del B-Tree comparador

* **Investigar:**

  * Estructura de B-Trees clásicos o B+Trees simplificados (inserción, búsqueda, altura, etc.).
  * Manejo de punteros y nodos en memoria.
* **Desarrollar:**

  * Clase `BTree` con operaciones: `insert(key)`, `search(key)`, `delete(key)` (opcional).
  * Añadir lógica para contar punteros usados y medir espacio.

### 3. Benchmarking y análisis empírico

* **Investigar:**

  * Técnicas para benchmarking: tiempo de búsqueda/inserción, espacio, construcción.
  * Uso de `time`, `tracemalloc`, `memory_profiler`, `matplotlib` para visualización.
* **Desarrollar:**

  * `run_benchmark.py` para comparar RMI vs B-Tree en tamaños variados.
  * `visualizations.py` para generar gráficos de barras o líneas con resultados.

### 4. Pruebas unitarias y validación

* **Investigar:**

  * Uso de `pytest` o `unittest` para validar correctitud funcional.
  * Cobertura de pruebas (coverage) y manejo de casos borde.
* **Desarrollar:**

  * Pruebas unitarias para cada clase y función pública (incluso para errores).

### 5. Informe técnico (PDF)

* **Contenido:**

  1. Fundamentos teóricos: RMI vs B-Tree (con referencias a papers como Kraska et al.).
  2. Diseño e implementación: decisiones tomadas, variantes consideradas.
  3. Resultados empíricos: gráficos comparativos, conclusiones.
  4. Limitaciones y propuestas futuras.

### 6. README.md (documentación completa)

* **Secciones clave:**

  * Descripción del proyecto y motivación teórica.
  * Cómo instalar dependencias y ejecutar ejemplos/pruebas.
  * Estructura del proyecto.
  * Documentación técnica de la API pública (métodos y atributos importantes).
  * Citas/referencias (enlace al informe técnico si aplica).

### 7. Demos y exposición oral

* **Desarrollar:**

  * Archivos `demo_rmi.py` y `demo_btree.py` con ejemplos avanzados: predicciones, errores de posición, casos borde.
* **Preparar:**

  * Diapositivas con teoría, arquitectura, resultados y análisis final.
  * Tener listas respuestas para:

    * ¿Por qué usar modelos en lugar de árboles?
    * ¿Cuándo RMI falla más que B-Tree?
    * ¿Cómo escalarías el sistema a millones de datos?

### 8. Scripts de profiling

* **Objetivo:** Comparar memoria y tiempo para búsqueda/inserción/construcción.
* **Herramientas sugeridas:**

  * `cProfile`, `tracemalloc`, `line_profiler`, `matplotlib`.
* **Desarrollar:**

  * `profile_memory_time.py` que genere reportes para cada tamaño de entrada.

---
