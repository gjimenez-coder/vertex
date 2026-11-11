# Capítulo 6 — Distribution (Distribución) — Estudio

## Tarjetas de repaso

- P: ¿Qué es un histograma y qué representa la altura de cada barra? / R: Es un tipo de gráfico de barras que muestra la frecuencia tabulada de los datos en intervalos (*bins*) que suman la distribución total; la altura indica el número de observaciones en ese intervalo.

- P: ¿Qué efecto tiene el ancho de los *bins* en un histograma? / R: Bins demasiado anchos ocultan patrones y demasiado estrechos difuminan la forma global; no hay número "correcto", pero hay pruebas estadísticas (raíces cuadradas, logaritmos, raíces cúbicas) para elegirlo.

- P: ¿Qué formas de distribución ayuda a identificar el histograma? / R: Right-skewed, left-skewed, bimodal, multimodal, simétrica y uniforme.

- P: ¿Qué es un gráfico de Pareto y por qué es excepción a la regla contra ejes duales? / R: Barras con los valores individuales de cada grupo más una línea con el total acumulado; es excepción porque ambas series son la misma métrica (distribución marginal y distribución acumulada).

- P: ¿Qué es el percentil 50 y por qué los percentiles son comparables entre grupos? / R: Es la mediana, el punto que divide a todos en dos mitades iguales; son comparables porque son independientes del tamaño de la población.

- P: ¿Por qué la mediana resiste los valores extremos mejor que la media? / R: La media se calcula sumando todos los valores entre el número de observaciones, así que un valor muy grande la distorsiona; la mediana no cambia porque ese valor sigue en el extremo.

- P: ¿Qué es un pyramid chart y a qué categoría pertenece? / R: Un gráfico que coloca dos grupos a cada lado de un eje vertical central, usado para métricas de población; es una subcategoría del diverging bar chart.

- P: ¿Cuáles son los dos tipos de incertidumbre estadística? / R: La *uncertainty from randomness* (confianza estadística, modelable y visualizable) y la *uncertainty from unknowns* (datos inexactos o desconocidos, no siempre resoluble con más datos).

- P: ¿Qué son las error bars y qué sesgo introducen en barras? / R: Marcadores que señalan el margen de error o el intervalo de confianza, un añadido a barras o líneas; introducen el sesgo "within-the-bar" (juzgar los puntos dentro de la barra como más probables).

- P: ¿Qué distingue a un gradient chart y a un fan chart? / R: El gradient chart (stripe plot) añade un degradado a uno o ambos lados del valor principal; el fan chart es su equivalente para líneas, con los valores más próximos a la estimación central más oscuros y aclarándose hacia fuera.

- P: ¿Cuáles son los cinco componentes principales del box-and-whisker plot? / R: Mediana, dos *hinges* (bordes de la caja, normalmente percentiles 25 y 75, cuya diferencia es el IQR), extremos superior e inferior (a 1,5 veces el IQR), dos *whiskers* y *outliers*.

- P: ¿En qué se diferencian candlestick y box-and-whisker aunque se parezcan? / R: El candlestick visualiza cambios de precio de acciones, bonos y materias primas en el tiempo; el box-and-whisker muestra distribución/incertidumbre mediante percentiles.

- P: ¿Qué muestra un violin chart y qué técnica requiere? / R: La forma de toda la distribución (zonas anchas = más valores); requiere estimar la *kernel density*, como un histograma pero suavizado para parecer continuo.

- P: ¿Qué es un ridgeline plot? / R: Una serie de histogramas o density plots de distintos grupos, alineados sobre el mismo eje horizontal con ligero solapamiento vertical; funciona bien cuando las distribuciones difieren de una fila a otra.

- P: ¿Qué es el jittering en un beeswarm plot y cuál es su riesgo? / R: Alterar ligeramente los valores para que los puntos no se solapen; el riesgo es que con demasiados puntos el desplazamiento modifique la forma de la distribución.

## Preguntas de autoevaluación

- P: ¿Cuál es la tesis central del capítulo sobre los gráficos de distribución difíciles? / R: Que no son malos gráficos: con buen etiquetado y diseño, incluso el más esotérico puede ser claro y útil, y la clave está siempre en conocer a la audiencia. (Sección: Lo que necesitas saber)

- P: ¿Por qué visualizar los datos es inestimable antes de aplicar pruebas estadísticas? / R: Porque dos distribuciones muy distintas pueden compartir media y mediana, y solo la forma revela la diferencia. (Sección: Histograma)

- P: Según Jessica Hullman, ¿por qué omiten los autores la incertidumbre y qué efecto tiene? / R: Por no querer confundir al lector, no tener acceso a la información, no saber calcularla y no querer que los datos parezcan cuestionables; omitirla hace que se interpreten como más creíbles de lo que son. (Sección: Visualizar la incertidumbre estadística)

- P: ¿Qué decisión implícita tomamos al dibujar solo percentiles (p. ej., en un box-and-whisker)? / R: Decidimos explícitamente no mostrar toda la distribución, por lo que conviene explorar bien los datos para no ocultar patrones. (Sección: Box-and-whisker plot y candlestick)

- P: ¿Por qué cuesta comparar el total de hombres y mujeres en un pyramid chart, y qué alternativa cabe? / R: Porque las barras no están contiguas; si ese es el objetivo conviene un paired bar chart o un dot plot. (Sección: Pyramid chart)

- P: ¿Qué aporta el wheat plot frente al Wilkinson Dot Plot y cuál es el trade-off general? / R: El wheat plot muestra los valores reales sobre el eje (aún agrupados por bins y apilados); el trade-off es que ofrece más detalle y atractivo, pero el histograma es más inmediato. (Sección: Visualizar la incertidumbre mostrando los datos)

- P: ¿Qué muestra un raincloud plot y a qué costa? / R: La densidad (como un violin) y los puntos reales debajo a la vez, permitiendo ver resumen, outliers y patrones, a costa de más esfuerzo de lectura. (Sección: Violin chart y ridgeline plot / Visualizar la incertidumbre mostrando los datos)

- P: ¿Qué recuerda la regla transversal del capítulo sobre la audiencia? / R: Que en entornos técnicos no hace falta explicar la mediana o el IC del 95 %, pero ante público general hay que definir y anotar. (Sección: Ideas clave)

## Checklist

- Al construir un histograma, prueba varios anchos de *bin* (y las pruebas de raíces cuadradas, logaritmos o raíces cúbicas) y observa cómo cambia la forma de 5 a 30, 50 o 120 bins.
- Antes de aplicar pruebas estadísticas, visualiza la distribución para comprobar que media y mediana no ocultan formas distintas.
- Si muestras incertidumbre, etiqueta claramente qué representan los extremos de las error bars (percentiles, error estándar, IC del 95 % o número fijo).
- En un confidence interval chart, destaca la línea central (más gruesa u oscura) frente a las líneas superior e inferior.
- En un box-and-whisker, ordena por valor en lugar de alfabéticamente, salvo que el lector necesite localizar categorías concretas.
- Al usar jittering (beeswarm), manipula los puntos lo justo para hacerlos visibles sin cambiar la forma de la distribución, y anota algunos outliers.
- Elige entre mostrar percentiles concretos o toda la distribución según qué estés dispuesto a ocultar, y considera a tu audiencia al decidir cuánto explicar.
- No confundas el candlestick (precios financieros en el tiempo) con el box-and-whisker (distribución/incertidumbre).
