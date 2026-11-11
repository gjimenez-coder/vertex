# Capítulo 7 — Geospatial (Datos geoespaciales) — Estudio

## Tarjetas de repaso

P: ¿Cuál es la gran ventaja de un mapa frente a otras visualizaciones?
R: Que la gente puede encontrarse a sí misma en los datos, una conexión que otras visualizaciones no logran.

P: ¿Cuál es el gran riesgo o problema central de los mapas basados en datos?
R: Que el tamaño de un área geográfica puede no corresponder a la importancia del valor del dato (p. ej. Rusia y Alaska ocupan mucho; Luxemburgo o Massachusetts, muy poco pese a cifras altas).

P: ¿Qué es un choropleth map?
R: El mapa de datos más familiar; usa colores, tonos o patrones sobre unidades geográficas para mostrar cantidades y magnitudes proporcionales.

P: ¿Cuándo es un error usar una paleta divergente en un choropleth?
R: Cuando no comparamos valores por encima y por debajo de un punto medio (como el promedio); en ese caso la paleta divergente es mala elección.

P: ¿Qué hace una proyección y qué implica siempre?
R: Transforma la esfera de la Tierra en un plano; toda proyección distorsiona en algún grado.

P: ¿Qué caracteriza a la proyección Mercator?
R: Es la más familiar (Gerardus Mercator, 1569), estándar náutico y opción por defecto en herramientas como Tableau y PowerBI; permite trazar una rhumb line, pero distorsiona el tamaño al aumentar la latitud (Groenlandia parece tan grande como Sudamérica).

P: ¿Cuáles son las tres categorías principales de proyecciones?
R: Cónica (buena para geografías largas este-oeste), cilíndrica (como Mercator, infla áreas lejanas del centro) y planar o azimutal (proyecta sobre una superficie plana, con distorsión creciente desde el centro).

P: ¿Cuáles son los cuatro métodos de binning (intervalos) descritos?
R: Sin bins (paleta continua/ramp), intervalos iguales, distribución de datos (cuartiles, quintiles, deciles o varianza) y bins arbitrarios.

P: ¿Qué es un cartograma y cuál es su tradeoff?
R: Reescala las áreas geográficas según sus valores para corregir la distorsión del choropleth; el tradeoff es que deja de parecerse al mapa conocido.

P: ¿Cuáles son los cuatro tipos principales de cartograma?
R: Contiguo, no contiguo, gráfico (p. ej. mapa Dorling) y en cuadrícula/gridded (p. ej. tile grid map).

P: ¿Qué ventaja y desventaja tiene el tile grid map?
R: Ventaja: todos los estados quedan del mismo tamaño (abstrae la distorsión) y se puede construir en Excel; desventaja: las unidades quedan fuera de su sitio (p. ej. California sin tocar Arizona).

P: ¿Qué diferencia a un proportional symbol map de un dot density map?
R: El proportional symbol map dimensiona símbolos según el dato; el dot density map usa puntos (relación uno-a-uno o uno-a-muchos) para mostrar la presencia de un valor y revelar densidades y clusters.

P: ¿Por qué se reconoce la forma del país en un dot density map sin fronteras ni etiquetas?
R: Porque la gente se agrupa en ciudades, fronteras y costas, aplicando el principio Gestalt de "similitud".

P: ¿Qué muestran los flow maps y qué subtipos existen?
R: Muestran movimiento entre lugares (dirección con flechas/líneas, valor con el ancho); subtipos radiales (origen-destino, de una fuente a muchos destinos) y distributivos (el flujo se bifurca en muchas líneas).

P: ¿Por qué es célebre el flow map de Minard (1869) sobre Napoleón en Rusia?
R: Integra seis variables en una vista (tropas, distancia, temperatura, tiempo, dirección y geografía) y concentra el mensaje en el declive del número de tropas (420.000 a 10.000).

## Preguntas de autoevaluación

P: ¿Qué dos preguntas guían la decisión de qué tipo de mapa usar?
R: ¿Qué importancia tienen los patrones geográficos? y ¿qué importancia tiene que el lector vea un mapa familiar? (Sección "Lo que necesitas saber").

P: Según el capítulo, ¿qué actitud recomienda Schwabish ante el deseo de hacer un mapa y por qué?
R: Más escepticismo y pensamiento crítico: no se trata de no hacer mapas nunca, sino de dar un paso atrás y considerar si es la elección correcta, porque el tamaño geográfico puede distorsionar la percepción de los valores. (Sección "Los retos de los mapas").

P: En el ejemplo del PIB per cápita mundial de 2017, ¿cómo ilustra el choropleth el problema de la distorsión geográfica?
R: Luxemburgo tuvo el PIB per cápita más alto (más de 104.000 dólares; EE. UU., 59.500) pero resulta casi invisible por su pequeño tamaño. (Sección "Choropleth map").

P: ¿Por qué el binning se describe como un problema de agregación y cómo ayuda mostrar la distribución?
R: Porque al combinar varios estados o países en un mismo bin se pierden las diferencias internas; siguiendo a Monmonier, añadir un gráfico de columnas junto al mapa hace visibles los cortes y las diferencias. (Sección "Elegir los bins").

P: En el ejemplo del Washington Post (2016) sobre suicidio y armas, ¿por qué funciona mejor un bubble plot que dos choropleths?
R: Con dos choropleths cuesta ver la relación positiva porque el lector salta de un mapa a otro; el bubble plot (tasa de suicidio en Y, posesión de armas en X, tamaño por población) muestra claramente que los estados del cuadrante superior derecho tienden a ser del oeste y el sur. (Sección "¿Debería ser un mapa?").

P: ¿Cómo resume Kenneth Field el propósito de un cartograma?
R: Como casi siempre la geografía es inapropiada para comparar, en vez de cambiar los datos y mantener la geografía, se conservan los valores y se modifica la geografía. (Sección "Cartogram").

P: ¿Qué es un cartograma no basado en área y qué ejemplo lo ilustra?
R: Uno que distorsiona la geografía física para mostrar tiempo o distancia relativos; el ejemplo es el mapa del metro de Washington, DC, con distancias casi constantes entre paradas para una vista compacta del viaje. (Sección "Cartogram").

P: ¿Qué recomienda el capítulo como solución frecuentemente óptima ante datos geográficos?
R: Combinar tipos: un mapa con una tabla o un gráfico de barras, para dar al lector una vista familiar donde ubicarse y, a la vez, un detalle más preciso de los datos. (Sección "Conclusión").

## Checklist

- [ ] Antes de mapear, preguntarte si el mapa comunica tu argumento o solo muestra dónde vive la gente.
- [ ] Evaluar si un scatter o bubble plot comunica mejor la relación que un (o dos) choropleth.
- [ ] En un choropleth, usar paletas secuenciales (claro a oscuro); reservar las divergentes para comparaciones respecto a un punto medio.
- [ ] Elegir la proyección según la geografía y sus tradeoffs (p. ej. cónica para geografías largas este-oeste; evitar Mercator salvo áreas pequeñas).
- [ ] Decidir el método de binning (sin bins, intervalos iguales, distribución de datos o arbitrario) y mostrar la distribución real junto al mapa.
- [ ] Revisar el etiquetado de los bins sopesando precisión (decimales), número de bins y suavidad de los datos; considerar incluir el número de observaciones por bin.
- [ ] Si la distorsión geográfica estorba, valorar un cartograma (contiguo, no contiguo, gráfico o en cuadrícula) asumiendo la pérdida de familiaridad.
- [ ] En proportional symbol maps, usar color transparente para ver formas superpuestas en racimos densos.
- [ ] Recordar a la audiencia real del mapa (p. ej. mapas de tránsito pensados para sus usuarios, no para un público general).
