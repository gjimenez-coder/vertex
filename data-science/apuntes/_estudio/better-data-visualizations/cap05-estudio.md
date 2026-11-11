# Time (Tiempo) — Estudio

## Tarjetas de repaso

P: ¿Cuál es la tesis pragmática del capítulo sobre gráficos de tiempo? / R: No importa la cantidad de datos, sino el propósito y cómo dirigir la atención del lector; hay pocas reglas duras y la mayoría de decisiones dependen de los datos y el objetivo.

P: ¿Debe el eje de un gráfico de línea empezar en cero? / R: No; a diferencia de las barras, puede no empezar en cero, y el rango elegido altera la percepción del nivel y del cambio según los datos y el objetivo.

P: ¿Qué es la estrategia "Start with Gray" aplicada a líneas? / R: Con muchas series, colorear y engrosar solo las de interés y dejar las demás en gris fino, aprovechando que color y grosor son atributos preatentivos para enfocar la atención.

P: ¿Qué es la ilusión de anchura de línea? / R: Al comparar dos curvas tendemos a juzgar la distancia en su punto más cercano en vez de la distancia vertical real; la solución más sencilla es graficar directamente la diferencia.

P: ¿Por qué el autor prefiere círculos como marcadores de datos? / R: Son simétricos, así que no importa dónde los corte la línea, a diferencia de triángulos o cuadrados.

P: ¿Cómo deben tratarse los datos faltantes en una serie? / R: Señalándolos: cambiar el formato de la línea (discontinua), no conectar los puntos o añadir una nota; nunca aparentar una serie continua e ininterrumpida.

P: ¿Cuáles son los tres problemas de los gráficos de doble eje? / R: Son difíciles de leer (qué línea va con qué eje), las cuadrículas no coinciden y, lo más importante, el cruce de líneas se vuelve foco de atención aunque no signifique nada.

P: ¿Qué ventaja tiene el slope chart frente a barras emparejadas? / R: Sitúa cada punto en un eje vertical propio y los conecta con una línea, mostrando de un vistazo valores relativos y cambio, sin el esfuerzo mental de procesar nivel y cambio por separado.

P: ¿Qué son las sparklines y quién las inventó? / R: Un estilo de small multiples para líneas, inventado por Edward Tufte: gráficos pequeños, intensos, simples, del tamaño de una palabra, que muestran patrones y tendencias, no valores exactos.

P: ¿Para qué sirve un bump chart y cuál es su compromiso? / R: Grafica cambios de rango en el tiempo, útil cuando interesan rangos relativos o hay outliers; su trade-off es que no muestra valores crudos ni diferencias relativas.

P: ¿Cuándo conviene un cycle chart? / R: Para comparar unidades pequeñas de tiempo (semanas, meses) a lo largo de varios años, ideal para tendencias estacionales fuertes.

P: ¿Por qué el eje vertical de un gráfico de área debería empezar en cero? / R: Porque un área puede pensarse como barras de ancho infinitamente fino, y las barras siempre deben partir de cero.

P: ¿Cuáles son las tres desventajas del área apilada? / R: La ilusión de anchura exagera cambios bruscos; solo la serie inferior se apoya en el eje horizontal; y el orden de apilado altera la percepción de las cuotas.

P: ¿Qué distingue a un streamgraph de un área apilada? / R: Su eje horizontal central no marca necesariamente el cero (los datos pueden ser positivos a ambos lados), dando una forma fluida idónea para series muy volátiles.

P: ¿Qué es un horizon chart y qué atributo es clave en él? / R: Un gráfico de área cortado en intervalos horizontales iguales y colapsado en bandas; el color es clave: tonos oscuros = valores grandes, claros = pequeños.

## Preguntas de autoevaluación

P: ¿Cómo se puede comparar dos series de unidades distintas sin recurrir al doble eje? / R: Poniendo los gráficos lado a lado o apilados verticalmente (small multiples), calculando un índice o cambio porcentual desde un año base, o usando un connected scatterplot con más etiquetas y anotación. (Sección "Evita los gráficos de doble eje")

P: ¿Por qué conviene oscurecer o engrosar la línea del cero cuando hay valores positivos y negativos? / R: Porque tendemos a asumir que la base del eje es cero; destacarla deja ver, por ejemplo, que el gasto sanitario cayó interanualmente en tres años. (Sección "Line chart")

P: ¿Qué riesgo tiene resumir solo dos momentos en un slope chart? / R: Igual que el dot plot, puede ocultar cambios ocurridos en los años intermedios. (Sección "Slope chart")

P: ¿Qué problema surge al mostrar dos o más series en un gráfico de área y cómo se mitiga? / R: Una serie puede ocluir a otra sin importar el orden, y el lector puede confundirlas como suma de un total; se mitiga con título y anotación aclaratorios, añadiendo transparencia a una o ambas series, o usando un gráfico de línea. (Sección "Area chart")

P: ¿Qué diferencia a un flow chart de una timeline? / R: La timeline muestra cuándo ocurren eventos (de básica a rica en anotaciones); el flow chart mapea un proceso paso a paso, no necesariamente en días o meses, facilitando entender rutas. (Sección "Flow charts y timelines")

P: ¿Qué representa el connected scatterplot y qué necesita el lector para interpretarlo? / R: Reúne dos series temporales sin doble eje (una en cada eje) conectando puntos que son instantes de tiempo; al ser poco habitual, requiere más tiempo y anotación: etiquetas de eje, flechas y el año en el primer y último punto. (Sección "Connected scatterplot")

P: Según el recuadro del capítulo, ¿por qué pueden engañar los totales frente a las métricas per cápita? / R: India y el Reino Unido tenían un PIB total similar (~2,6 billones en 2017) pero un PIB per cápita muy distinto (39.720 frente a 1.940 dólares) por la población; conviene normalizar métricas cuando es más informativo. (Sección "Flow charts y timelines")

## Puntos a dominar

- Elegir el tipo de gráfico según el propósito y la atención deseada, no según la cantidad de datos.
- Aplicar "Start with Gray", color y grosor para enfocar la atención con muchas series.
- Decidir el rango del eje de una línea de forma consciente, evitando que el valor extremo coincida con el máximo/mínimo del eje.
- Reconocer y evitar la ilusión de anchura de línea graficando directamente la diferencia.
- Rechazar los gráficos de doble eje y aplicar sus alternativas (small multiples, índice, connected scatterplot).
- Señalizar siempre los datos faltantes y nunca aparentar continuidad.
- En área apilada, elegir el orden de apilado sabiendo que guía la percepción y que solo la base se compara con precisión.
- Asociar cada tipo a su uso: slope (dos momentos), bump (rangos), cycle (estacionalidad), sparklines/horizon (tendencias en poco espacio), streamgraph (series volátiles), Gantt (duraciones), connected scatterplot (relación entre dos series).
- Normalizar o estandarizar métricas (per cápita, por 100.000, por hora) cuando resulta más informativo que los totales.
