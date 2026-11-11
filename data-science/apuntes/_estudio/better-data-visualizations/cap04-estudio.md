# Comparing Categories (Comparando categorías) — Estudio

## Tarjetas de repaso

P: ¿Qué debes decidir antes de elegir un gráfico para comparar categorías?
R: El argumento principal y la comparación más importante, porque mostrar todas las barras o puntos puede ocultar el mensaje.

P: ¿Por qué el gráfico de barras está en la cima del ranking perceptual?
R: Porque con rectángulos sobre un mismo eje recto es fácil comparar valores rápida y exactamente; además son fáciles de hacer, incluso con lápiz y papel.

P: ¿Por qué debe empezar en cero el eje de un gráfico de barras?
R: Porque percibimos el valor por la longitud de la barra; empezar en otro punto sobreenfatiza las diferencias y sesga la percepción.

P: ¿Qué significa "don't break the bar" y qué alternativa hay con outliers?
R: No usar una línea ondulada para recortar barras, pues distorsiona los valores relativos; mejor usar un "zoom out" con todos los datos y un "zoom in" que omite los extremos, con etiquetas y título activo.

P: ¿Qué es un outlier y qué método estándar ayuda a detectarlo?
R: Un punto alejado del resto (por variabilidad aleatoria, error de medición o anomalía real); se detecta inspeccionando visualmente y comparando con 1,5 veces el rango intercuartílico (IQR).

P: ¿Qué es un lollipop chart y qué lo distingue de la barra?
R: Sustituye la barra por una línea con un punto al final; queda justo por debajo de la barra en el ranking, pero reduce tinta y deja espacio para anotar.

P: ¿Por qué se recomienda evitar el circular bar chart?
R: Porque dos barras de igual valor terminan alineadas pero no miden lo mismo al recorrer circunferencias distintas; Andy Kirk lo compara con una carrera con salidas escalonadas.

P: ¿Para qué sirve un paired bar y cuál es su problema principal?
R: Comparar entre categorías y dentro de ellas, dirigiendo la atención a niveles y diferencia; su problema principal es el clutter cuando hay demasiadas barras por categoría.

P: ¿Cuál es el reto del stacked bar y una de sus soluciones?
R: Las series interiores no comparten línea base, lo que dificulta compararlas; una solución es separar cada serie en su propia línea base con small multiples (perdiendo el total).

P: ¿Cuál es la diferencia entre percent change y percentage point change?
R: El cambio porcentual es ((NEW−OLD)/OLD)×100; el cambio en puntos porcentuales es NEW−OLD cuando ambos ya son porcentajes.

P: ¿Qué es un diverging bar y cuándo funciona mejor?
R: Un stacked bar cuyas pilas divergen desde una línea base central; funciona cuando interesa el sentimiento total de cada lado más que la comparación de cada componente (típico en escalas Likert).

P: ¿Qué ventaja tiene el dot plot sobre las barras y qué oculta?
R: Usa menos tinta y deja más espacio para anotar al comparar muchas categorías; al ser un gráfico resumen oculta los valores intermedios y la variación brusca entre los dos puntos.

P: ¿Qué compara un Marimekko y qué lo diferencia del mosaic?
R: Compara dos variables escalando el ancho de cada barra según una segunda variable; en el mosaic tanto alturas como anchos suman 100 %, llenando todo el espacio (part-to-whole en ambas dimensiones).

P: ¿Por qué hay que escalar los círculos de un bubble chart por área y no por diámetro?
R: Porque el diámetro escala linealmente y el área cuadráticamente (A = πr²); usar el radio para doblar un valor cuadriplica el área.

P: ¿Qué muestran un Sankey diagram y un waterfall chart?
R: El Sankey muestra cómo las categorías fluyen de un estado a otro con el ancho de las líneas como magnitud; el waterfall muestra una ecuación sumando o restando valores desde un inicial hasta un total.

## Preguntas de autoevaluación

P: Con datos de población donde ningún país baja de 50 millones, ¿qué problema causa empezar el eje en 50 millones?
R: Hace que Brasil parezca mucho mayor que Italia cuando solo es unas 3,5 veces mayor; empezar en 100 millones haría parecer que la mitad de los países no tiene habitantes. (Sección: El gráfico de barras)

P: ¿Por qué el caso Buzzfeed/Pornhub (2014) con Kansas como gran outlier era un artefacto?
R: Porque la metodología asignaba la geolocalización ausente al centro geográfico de EE. UU., que es Kansas. (Sección: El gráfico de barras)

P: ¿Cuál es la solución más elegante para etiquetas de categoría demasiado largas en barras verticales?
R: Girar todo el gráfico a barras horizontales: se mantiene la longitud como atributo preatentivo, pero las etiquetas quedan horizontales y legibles. (Sección: El gráfico de barras)

P: ¿Cuándo prefiere el autor barras sobre líneas para cambios en el tiempo?
R: Cuando hay pocos puntos (p. ej. cinco años, donde la tinta da peso visual) y con intervalos temporales discretos y pocas observaciones. (Sección: Paired bar)

P: ¿Qué problema plantea colocar la categoría "neutral" en el centro de un diverging bar y qué alternativas hay?
R: Implica erróneamente que se reparte entre ambos lados y rompe las líneas base; mejor colocarla a un lado o usar un stacked bar que sume 100 % marcando el 50 % como guía. (Sección: Diverging bar)

P: ¿Qué riesgo tiene escalar los iconos de un isotype chart por valor?
R: Cuesta saber si escala por altura, ancho o área; Bertin y Few advierten que el área crece más rápido que la altura y obliga al lector a estimar áreas, algo que hacemos mal. (Sección: Unit, isotype y waffle)

P: En un heatmap de composición de ingresos, ¿qué diferencia hay entre usar la misma escala de color para todo o una escala por columna?
R: La misma escala permite comparar entre todas las categorías; dar a cada columna su propia escala facilita comparar dentro de cada categoría. (Sección: Heatmap)

P: ¿Por qué Stephen Few inventó el bullet chart frente al gauge chart?
R: Porque medimos mal los ángulos del gauge; el bullet es lineal y compacto, con valor observado, valor objetivo y rango de fondo con bandas de éxito, y permite apilar varios para comparar. (Sección: Gauge y bullet)

## Puntos a dominar

- Decidir el argumento principal y la comparación más importante antes de elegir cualquier gráfico.
- Reglas de la barra: empezar el eje en cero, no romper la barra, ordenar los datos cuando ayude y usar tick marks/gridlines con mesura.
- Cuándo usar paired, stacked y diverging bar, y reconocer que su reto común es el clutter y las series sin línea base compartida.
- Distinguir percent change de percentage point change al interpretar o reportar cambios.
- Saber que el dot plot aligera la tinta pero oculta la variación intermedia por ser un gráfico resumen.
- Reconocer las distorsiones perceptuales: ángulos en gauge, áreas en bubble/isotype (escalar por área, no por diámetro) y circunferencias en circular bar.
- Elegir heatmap para datos densos o de alta frecuencia, y Sankey/waterfall como alternativas compactas según el objetivo comunicativo.
