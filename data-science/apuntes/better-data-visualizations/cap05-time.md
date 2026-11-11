# Better Data Visualizations — Jonathan Schwabish (Columbia University Press, 2021)
## Capítulo 5 — Time (Tiempo)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF (libro muy visual, los gráficos se describen con palabras); las citas usan la página del PDF.

## Lo que necesitas saber

El capítulo recopila los tipos de gráfico para mostrar cambios a lo largo del tiempo. Parte de los más familiares (línea, área, área apilada) y avanza hacia otros menos conocidos pero igual de útiles: gráficos circulares de línea, de pendiente (slope), sparklines, bump charts, cycle charts, streamgraphs, horizon charts, Gantt, diagramas de flujo, líneas de tiempo y connected scatterplots. Muchos son variaciones de la línea o el área.

La tesis es pragmática: no importa la cantidad de datos en el gráfico, sino el propósito y cómo dirigir la atención del lector. Hay pocas reglas duras; la mayoría de decisiones (rango del eje, número de series, orden de apilado) dependen de los datos y del objetivo, y conllevan compensaciones entre precisión perceptual y compacidad o atractivo visual. Los ejemplos del capítulo siguen la guía de estilo del Urban Institute.

Sales sabiendo cuándo y por qué usar cada tipo, qué ilusiones perceptuales evitar (línea-anchura, ejes duales) y cómo técnicas transversales —"Start with Gray", small multiples, marcadores de datos, señalización de datos faltantes— mejoran la lectura. Buena parte de los datos de ejemplo son el gasto sanitario como porcentaje del PIB en EE. UU. y otros países de la OCDE, y muertes por sobredosis de drogas.

## Line chart (gráfico de línea)

El gráfico de línea y el de barras son quizá los más comunes del mundo: fácil de leer, claro y dibujable a mano. Conecta valores con líneas sobre un periodo continuo para seguir tendencias. El ejemplo base muestra el gasto sanitario de EE. UU. como porcentaje del PIB entre 2000 y 2015 (de 12,5% a 16,8%). Se sitúa alto en la escala de ranking perceptual: al compartir eje horizontal, las comparaciones entre y dentro de series son fáciles.

No hay límite al número de líneas. La clave no es el volumen de datos, sino enfocar la atención del lector. Con muchas series conviene resaltar un subconjunto: en lugar de dar a todas el mismo color y grosor, se colorean y engrosan solo las de interés (p. ej. EE. UU. y Alemania) y se dejan las demás en gris fino —la estrategia "Start with Gray" del capítulo 2—. Color y grosor son atributos preatentivos (PDF p. 25), así que la atención va a las líneas destacadas y el lector aprecia el patrón general sin perder el foco. Otra opción son los small multiples: romper un gráfico denso en varios paneles (p. ej. nueve países de la OCDE), lo que da espacio para más detalle y anotación aunque se pierda algo de comparación relativa.

A diferencia de las barras, el eje de un gráfico de línea no tiene por qué empezar en cero. El rango elegido altera la percepción del nivel y del cambio: un eje de 0 a 20 muestra un aumento leve; rangos cada vez más ajustados hacen el cambio más dramático. No hay respuesta correcta: depende de los datos y del objetivo. El autor evita el caso en que el valor máximo o mínimo del eje coincide con el dato extremo, porque el gráfico queda "demasiado apretado" y sugiere falsamente que los datos no pueden subir ni bajar más. Además, tendemos a asumir que la base del eje es cero; cuando hay valores positivos y negativos conviene oscurecer o engrosar la línea del cero para que se vea, por ejemplo, que el gasto sanitario cayó interanualmente en tres años.

La ilusión de anchura de línea: al comparar dos curvas tendemos a juzgar la distancia en su punto más cercano en vez de la distancia vertical real. El gráfico de Playfair (1785) de exportaciones e importaciones entre Inglaterra y las Indias Orientales (1700–1780) lo ilustra: el repunte de la balanza comercial entre 1762 y 1764 es difícil de ver. La solución más sencilla es graficar directamente la diferencia cuando esa es la métrica de interés.

Los marcadores de datos (símbolos sobre la línea) dan peso visual y sirven para pocas líneas o puntos, o para etiquetar valores concretos. El autor prefiere círculos: son simétricos, así que no importa dónde los corte la línea, a diferencia de triángulos o cuadrados. Otras formas pueden ser necesarias por accesibilidad: en EE. UU. las agencias federales siguen la Section 508, y muchos lectores de pantalla no distinguen series solo por color, por lo que distintos marcadores ayudan (ver capítulo 12).

Datos faltantes: siempre falta algo, y la mayoría de datos son instantáneas tratadas como continuas. Cuando una serie regular se interrumpe porque no se recogieron datos, hay que señalarlo: cambiar el formato de la línea (p. ej. discontinua), no conectar los puntos, o añadir una nota. Lo que nunca se debe hacer es ignorar los valores faltantes y aparentar una serie continua e ininterrumpida.

## Evita los gráficos de doble eje

Comparar dos series de unidades distintas tienta a añadir un segundo eje vertical, pero conviene resistirse. El ejemplo combina la cuota de ingresos dedicada a vivienda (eje izquierdo) y la tasa de desempleo (eje derecho) en EE. UU. (2000–2018). Tres problemas: (1) son difíciles de leer, no es obvio qué línea va con qué eje; (2) las cuadrículas no coinciden, dejando los números de un eje "flotando"; y (3), lo más importante, el punto donde las líneas se cruzan se vuelve foco de atención aunque no signifique nada —el cruce en 2009 es solo una coincidencia—. Como el eje no necesita empezar en cero, se pueden manipular arbitrariamente las dimensiones para hacer que las líneas se crucen donde se quiera, por lo que el creador puede engañar sobre la relación entre series (la web Spurious Correlations de Tyler Vigen lo lleva al absurdo). Combinar área y línea no resuelve el problema.

Soluciones: (1) poner los gráficos lado a lado (small multiples), o apilados verticalmente con una línea que cruce ambos para marcar un año; (2) calcular un índice o el cambio porcentual desde un año base (p. ej. puntos porcentuales de cambio desde 2000), perdiendo el nivel pero ganando comparabilidad; (3) usar otro tipo, como el connected scatterplot, con más etiquetas y anotación. Posible excepción a la regla: traducir una misma medida a dos escalas (Fahrenheit y Celsius), donde no se rastrean dos variables sino un mapeo directo.

## Circular line chart (gráfico de línea circular)

Igual que las barras pueden envolverse en un círculo, también las líneas. El ejemplo muestra el porcentaje de visitas a urgencias por gripe en EE. UU. por semana (2014–2017). La línea estándar da la vista habitual (subida en invierno, caída en verano); la versión radial "se inclina" hacia las tres en punto cuando hay más infecciones en otoño-invierno. Es más compacta, pero dificulta las comparaciones precisas porque las líneas no comparten un eje horizontal. Suele valer para mejorar una metáfora visual.

## Slope chart (gráfico de pendiente)

Cuando no hace falta mostrar toda la serie, el slope chart —una línea simplificada— es útil. Frente al gráfico de barras emparejadas, que obliga al lector a procesar nivel y cambio con mucho esfuerzo mental, el slope chart sitúa cada punto en un eje vertical propio (p. ej. enero 2000 a la izquierda, enero 2018 a la derecha) y los conecta con una línea. Así se ven de un vistazo los valores relativos (Montana el mayor desempleo inicial, Connecticut el menor) y el cambio (bajó en Montana, Hawái e Idaho; subió en los otros tres estados). Se puede estilizar con dos colores para subidas/bajadas, etiquetas opcionales, grosor según una tercera variable o la estrategia "Start with Gray" para incluir todos los estados resaltando unos pocos. Un gráfico más alto ayuda a ver el detalle. Cuidado: igual que el dot plot, resumir solo dos momentos puede ocultar cambios en los años intermedios.

## Sparklines

Estilo específico de small multiples para líneas, inventado por Edward Tufte: gráficos "pequeños, intensos, simples, del tamaño de una palabra, con resolución tipográfica". Se usan en tablas densas, al final de una fila o columna. No buscan valores exactos, sino mostrar patrones y tendencias generales. En el ejemplo, dos columnas dan el gasto sanitario de 2000 y 2015 y las sparklines muestran los dieciséis años; se ve rápido que subió en todos los países salvo Turquía (resaltada).

## Bump chart

Variación de la línea para graficar cambios de rango en el tiempo (encuestas, posiciones en un torneo de golf). Útil cuando interesan los rangos relativos más que los valores absolutos, o cuando hay outliers, porque al graficar rangos se abstrae de las grandes diferencias de magnitud. El compromiso: no muestra valores crudos. Los ejemplos ordenan los diez países con mayor gasto sanitario en 2015; una versión solo sigue esos diez (con huecos), otra incluye todos los países cada año (requiere más etiquetado). La modificación "ribbon" (cinta), como en el gráfico del Berliner Morgenpost, escala el ancho de las cintas según el valor real, con aspecto orgánico y fluido parecido al streamgraph. Trade-off frente a la línea: el bump muestra rangos relativos pero no diferencias relativas.

## Cycle chart (gráfico de ciclo)

Compara unidades pequeñas de tiempo (semanas, meses) a lo largo de varios años; ideal para tendencias estacionales fuertes. El ejemplo muestra nacimientos mensuales en EE. UU. (2007–2017), con una línea amarilla para el promedio de cada mes y un punto al final de cada línea para el año más reciente: se ve la tendencia descendente de la década y el pico veraniego (julio, agosto, septiembre). Comparado con una línea estándar, el cycle chart tiene más información pero resulta menos recargado. También puede dividir un gráfico de columnas denso (p. ej. desempleo por grupos raciales) en paneles por grupo, como un small multiples.

## Area chart (gráfico de área)

Son gráficos de línea con el área bajo la línea rellena, lo que da más peso visual; pueden pensarse como barras de ancho infinitamente fino, por lo que el eje vertical debería empezar siempre en cero. El ejemplo muestra muertes por sobredosis de opioides con receta en EE. UU. (2000–2016). El problema: con dos o más series, una puede ocultar ("ocluir") a la otra sin importar el orden, y el lector podría confundirlas como suma de un total. Conviene usar título y anotación para aclarar que son series distintas. Estrategias: añadir transparencia a una o ambas series (ojo: dar transparencia solo a una la resta importancia), o usar un gráfico de línea.

## Stacked area chart (gráfico de área apilada)

Muestra varias series a la vez que suman un total o un 100%. El ejemplo de muertes por sobredosis (1999–2016) tiene dos versiones: en valores absolutos el ojo va al gran aumento total; en porcentajes, a los cambios de distribución (caída de cocaína, aumento de heroína, benzodiacepinas y otras). Tres desventajas: (1) la ilusión de anchura de línea hace ver cambios bruscos mayores de lo real; (2) solo la serie inferior se apoya en el eje horizontal, dificultando comparar el resto; (3) el orden de apilado altera la percepción de las cuotas. Poner la serie de interés en la base la hace más comparable, pero no hay un orden "correcto": la decisión guía la percepción del lector. El autor etiqueta los segmentos directamente en vez de usar leyenda. Un small multiples (seis gráficos) muestra mejor el patrón exacto de cada categoría pero peor las cuotas relativas; el apilado es más compacto. El área apilada también puede mostrar distribuciones usando otra medida de tiempo: p. ej. causas de muerte en EE. UU. en 2017 por edad (0–100), con causas externas hacia los 25 años y cáncer hacia los 60.

## Streamgraph

Como el área apilada, apila series, pero el eje horizontal central no marca necesariamente el cero: los datos pueden ser positivos a ambos lados. Produce una forma fluida y orgánica, idónea para series temporales muy volátiles, con picos y valles. Minimiza la distorsión de la línea base que se acumula en el área apilada y orienta más hacia los aumentos globales que hacia series concretas. Los investigadores reconocen que es inusual y puede costar de entender —sobre una pieza del New York Times (2008) señalaron tensión entre lo estéticamente atractivo y la legibilidad—, pero puede resultar más interesante según la audiencia. Ejemplo reciente: el Hindustan Times (2016) con los máximos premios civiles de la India.

## Horizon chart

Es un gráfico de área cortado en intervalos horizontales iguales y colapsado en bandas únicas, lo que lo hace compacto y parecido a un heatmap. Los valores positivos se colapsan y los negativos se voltean sobre el eje. Varios horizon charts juntos condensan un conjunto denso; útiles cuando las series temporales son tan cercanas en valor que en una línea se solaparían. El color es el atributo clave: tonos oscuros = valores grandes, claros = pequeños. Como en sparklines y heatmaps, no busca valores exactos sino detectar tendencias y valores extremos. El ejemplo usa el gasto público en salud (% del PIB) de diez países en quince años; la serie de Suecia se construye troceando su área cada 0,5 puntos. Una serie de líneas no tiene el mismo "punch": el ojo no encuentra una región que lo atraiga, mientras que el color del horizon dirige la atención.

## Gantt chart

Usa líneas o barras horizontales para mostrar la duración de valores o acciones; típico como herramienta de seguimiento de calendarios (fases de proyecto o presupuesto). Inventado por Henry Laurence Gantt, ingeniero de inicios del siglo XX, se usó primero para seguir cronogramas de producción. El ejemplo muestra turnos de personal en una cafetería a lo largo de un día (huecos blancos = descansos, grises = almuerzos, rayas = ausencias). Se puede extender escalando el ancho de las barras según otra variable (p. ej. el salario). Joseph Priestley, en *A Chart of Biography* (1765), mostró con barras horizontales las vidas de unos dos mil personajes entre 1200 a.C. y mediados del siglo XVIII; suele llamarse línea de tiempo, pero se parece más a un Gantt por las barras y los inicios (nacimientos) y finales (muertes) concretos, con puntos para fechas inciertas.

## Flow charts y timelines (diagramas de flujo y líneas de tiempo)

Pueden mostrar cambios en el tiempo o procesos, secuencias y jerarquías; unos ligados a datos y otros más ilustrativos (en PowerPoint, el menú "SmartArt"). Una línea de tiempo muestra cuándo ocurren eventos: puede ser básica (un marcador) o rica (anotaciones, imágenes, gráficos), y horizontal, vertical o de otras formas. El ejemplo del autor en la Congressional Budget Office traza hitos del programa SNAP (antes food stamps), con cajas grises de detalle legislativo a la derecha y cambios en gasto y participantes a la izquierda.

Los diagramas de flujo mapean un proceso paso a paso, no necesariamente en días o meses, facilitando entender rutas mejor que un texto largo o una tabla enrevesada. El ejemplo describe el programa de Social Security Disability Insurance (DI): los solicitantes entran en "Disability Determination Services" y, si se aprueba, son "Allowed"; si no, apelan en cada etapa o salen. Las formas pueden significar cosas distintas (rectángulos, puntos de decisión, rectángulos redondeados para inicio/fin) y el color ayuda a diferenciar partes; se pueden escalar las ramas según sus cuotas, como un diagrama de Sankey (PDF p. 126). Un organigrama es un tipo de flujo que muestra la jerarquía (ver capítulo 8). El diagrama del Affordable Care Act (Joint Economic Committee, 2010) tenía el propósito implícito de mostrar la complejidad de la propuesta. La cantidad de notas, iconos y texto debe ajustarse a las necesidades del lector.

Un recuadro sobre totales vs. per cápita advierte que los totales pueden engañar: India y el Reino Unido tenían un PIB total similar (~2,6 billones de dólares en 2017), pero su PIB per cápita difería enormemente (39.720 frente a 1.940 dólares) por la población. Conviene normalizar o estandarizar métricas (tasas de mortalidad por 100.000, salarios por hora) cuando resulta más informativo.

## Connected scatterplot

Reúne dos series temporales sin usar doble eje: una va en el eje horizontal y otra en el vertical, y los puntos (cada uno un instante de tiempo) se conectan con una línea para ver su relación. El ejemplo usa esperanza de vida (eje horizontal) y PIB per cápita (eje vertical) en Sudáfrica (1996–2016): se aprecia que primero la esperanza de vida cayó mientras la economía crecía, y que hacia 2006 la esperanza de vida volvió a subir mientras el crecimiento se aplanaba. Al ser un tipo poco habitual, el lector necesita más tiempo y anotación (etiquetas de eje, flechas, el año en el primer y último punto). También sirve para más grupos: comparar niveles para diez países (destaca EE. UU. por su alto PIB) o el crecimiento porcentual desde 1996 (donde EE. UU. casi desaparece y resaltan China y Etiopía). Cuál es mejor depende de la audiencia y del argumento.

## Ideas clave

- Los gráficos de línea y área son la base para mostrar cambios en el tiempo; no hay límite de líneas, pero con muchas usa color y grosor ("Start with Gray") para enfocar la atención.
- El eje de una línea no necesita empezar en cero; el rango elegido depende de los datos y del objetivo, y altera la percepción del cambio.
- Cuidado con ilusiones perceptuales: la de anchura de línea (grafica la diferencia directamente) y el cruce engañoso de los gráficos de doble eje (evítalos; usa small multiples, índices o connected scatterplots).
- Señaliza siempre los datos faltantes (línea discontinua, sin conectar o nota); nunca aparentes una serie continua.
- Para muchos datos, prueba sparklines, cycle charts, horizon charts o small multiples: priorizan tendencias generales sobre valores exactos.
- En el área apilada, el orden de apilado guía la percepción; solo la serie en la base se compara con precisión, y la ilusión de anchura exagera cambios bruscos.
- Bump charts muestran rangos; slope charts, dos momentos; Gantt, duraciones; streamgraphs, series volátiles con forma orgánica.
- Flow charts, timelines y connected scatterplots admiten infinitas variantes; ajusta el detalle y el diseño (horizontal, vertical, compacto) a las necesidades y plataforma del lector.
