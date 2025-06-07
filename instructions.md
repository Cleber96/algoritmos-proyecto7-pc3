### **Práctica calificada 3 CC0E5**

**Consideraciones generales para todos los proyectos:**

1. **Alcance:**

   * Implementación funcional y eficiente del núcleo de la estructura o algoritmo elegido, incluyendo al menos una optimización clave basada en bibliografía o variantes de rendimiento documentadas.
   * No es necesario cubrir todas las variantes posibles; basta con justificar por qué se escogen las optimizaciones seleccionadas.

2. **Repositorio público:**

   * Lenguaje: Python, C++ o Rust.
   * Código modular, bien comentado (especialmente en secciones complejas), fácil de entender y mantener.
   * **README.md** exhaustivo que incluya:

     * Descripción del proyecto y su motivación teórica.
     * Instrucciones de compilación/ejecución (dependencias, comandos paso a paso).
     * Estructura del proyecto (organización de carpetas y archivos).
     * Documentación de la API pública (firma de funciones, parámetros, valores de retorno, excepciones).
   * **Drivers/demo** que muestren usos avanzados de la estructura (casos de uso variados).
   * **Suite de pruebas unitarias** (pytest, Google Test, etc.) con alta cobertura, y scripts para profiling/benchmarking comparativo (por ejemplo, medir tiempos en distintos tamaños de datos).

3. **Documentación adicional (informe técnico PDF, 3–5 páginas):**

   * Teoría subyacente (pruebas de correctitud, complejidad, referencias bibliográficas).
   * Decisiones de diseño (alternativas estudiadas, por qué se eligió la opción final).
   * Análisis empírico de rendimiento (resultados de benchmarking y comparación con implementaciones existentes).
   * Limitaciones actuales y posibles mejoras o extensiones futuras.

4. **Exposición (12 de junio):**

   * Cada grupo debe preparar una presentación (PowerPoint, PDF, etc.) que explique brevemente la teoría, la implementación y los resultados experimentales.
   * Se valorará la claridad al responder preguntas sobre diseño y benchmarking.
   * Si el número de estudiantes o grupos excede el tiempo disponible el 12 de junio, o por problemas de horario, se reservará un segundo día adicional para que los grupos pendientes realicen su exposición (con las mismas condiciones de preguntas y ponderación).

En ese caso, se comunicará oportunamente la fecha y hora exacta a los grupos que aún no hayan expuesto.

5. **Ponderación de calificaciones:**

   * Entrega del repositorio (README, código, pruebas, benchmarking, informe PDF): 5 puntos.
   * Exposición oral y respuesta de preguntas: 15 puntos.

Se priorizará el manejo de los conceptos y códigos vistos en la clase, así como la capacidad de explicar decisiones de diseño y resultados experimentales.

### Proyectos propuestos

7. **RMI (Recursive Model Index) básico sobre array de enteros y comparativa con B-Tree**

   * **Temáticas combinadas:** RMI; B-Tree; benchmarking de índices basados en modelos vs. tradicionales.
   * **Descripción breve:**

     1. Implementar un **RMI de dos niveles** sobre un array ordenado de enteros (o strings codificados).

        * Nivel 0: modelo lineal que predice rango aproximado.
        * Nivel 1: modelos lineales más pequeños (uno por tramo) para afinar la predicción de posición.
     2. Construir un **B-Tree** clásico en memoria (o una B+Tree simplificada) para servir de comparador.
     3. Medir:

        * Tiempo de construcción de índices.
        * Tiempo de búsqueda exacta de un entero (por ejemplo, rank query).
        * Espacio ocupado (parámetros de modelo vs. punteros de B-Tree).
     4. Documentar la forma de entrenar modelos lineales (mínimos cuadrados) y cómo ajustarlos para minimizar error de posición.