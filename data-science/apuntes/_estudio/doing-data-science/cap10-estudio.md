# Social Networks and Data Journalism (Redes sociales y periodismo de datos) — Estudio

## Tarjetas de repaso

P: ¿Cuál es la tesis central del capítulo sobre cómo entender el mundo?
R: El mundo es más una red que un conjunto de casos con atributos; no basta con entender individuos aislados, hay que mirar las relaciones y los patrones de nivel meso.

P: ¿Qué diferencia hay entre datos caso-atributo y datos de red?
R: Los datos caso-atributo describen cada caso (persona o evento) por atributos (edad, SO, historial de búsquedas); los datos de red se centran en las relaciones entre las personas, no solo en las personas.

P: ¿De qué dos orígenes nace el análisis de redes sociales (SNA)?
R: De la teoría de grafos (Euler y el problema de los siete puentes de Königsberg) y de la sociometría, iniciada por Jacob Moreno.

P: ¿Qué son nodos y aristas en terminología de redes?
R: Los actores o nodos (personas, webs, etc.) son los puntos; las relaciones son los lazos relacionales o aristas (edges).

P: ¿Qué es el cierre triádico?
R: La existencia de una arista entre A y C cuando ya existen las aristas A–B y B–C.

P: ¿Qué son los grafos bipartitos y las ego networks?
R: Los grafos bipartitos conectan solo dos clases distintas (p. ej. personas y empresas unidas si alguien está en el consejo); una ego network es la parte de la red que rodea a una sola persona.

P: ¿Qué cuatro medidas de centralidad se presentan y qué noción de importancia captan?
R: Grado (cuántas conexiones tienes), cercanía (estar cerca de todos), intermediación (cuántos caminos más cortos pasan por ti) y vector propio (ser popular entre los populares, p. ej. PageRank).

P: ¿Por qué falla buscar un bloguero influyente de los Hermanos Musulmanes partiendo del top 100 del gran grafo?
R: Porque encontrarías a alguien influyente en la red grande (élites transnacionales), no dentro del grupo local; lo clave es mirar la red o subred correcta.

P: ¿Qué moraleja resume la metáfora de los "bancos de peces"?
R: Los peces individuales importan menos que los bancos de peces; hay que centrarse en patrones de nivel meso, no en el micro ni el macro.

P: ¿Qué consejo clave da Kelly sobre el orden entre preguntas y datos?
R: Invertir la dirección del pensamiento: primero preguntar qué significaría predecir algo y qué datos harían falta, y luego elegir la fuente. Primero las preguntas, luego los datos.

P: ¿Qué es el modelo de grafo aleatorio de Erdős–Rényi (red de Bernoulli)?
R: Un modelo con N nodos y D = C(N,2) dyads en el que cada arista existe de forma independiente con probabilidad p; no todas las redes resultan igual de probables.

P: ¿Qué modelan los ERGM y por qué se usan frente a Bernoulli?
R: Las redes reales no son de Bernoulli: exhiben transitividad, clustering, reciprocidad e intermediación; los ERGM eligen estadísticas de grafo (triángulos, aristas, k-stars) como variables y ajustan coeficientes para modelar el comportamiento observado.

P: ¿Qué problema de inferencia sufren los ERGM?
R: En la práctica se observa una sola red (tamaño muestral de uno); la pseudo-verosimilitud puede dar valores infinitos y los métodos MCMC sufren degeneración inferencial (convergen a grafos completos o vacíos, o no convergen), como documenta Mark Handcock (2003).

P: Según Bruner, ¿qué comparten el periodismo de datos y la ciencia de datos?
R: Las habilidades fundamentales: hacer buenas preguntas, responderlas con datos y comunicar los hallazgos; la traducción y la visualización son centrales.

P: ¿Cuál dice Bruner que es su habilidad fundamental?
R: La traducción: convertir historias complejas en significado que el lector entienda, anticipar preguntas y responderlas de forma persuasiva.

## Preguntas de autoevaluación

P: ¿Por qué sostiene Kelly que existe un sesgo hacia los datos caso-atributo y qué se pierde con ellos? (sección "Datos caso-atributo frente a datos de red")
R: Porque son fáciles de almacenar y recopilar, pero pierden el sentido de muchas preguntas; centrarse en ellos es como buscar "bajo la farola", un sesgo observacional, ya que el mundo es más una red.

P: ¿Cómo distingue el SNA el dilema micro frente a macro y por qué importa conocer la red real? (sección "Análisis de redes sociales: orígenes y terminología")
R: El dilema es individual frente a sistémico; en EE. UU. hay mecanismos formales que salvan la brecha (mercados y elecciones), pero gran parte del mundo no los tiene, así que hay que conocer la red real para saber quién tiene poder e influencia para provocar cambios.

P: ¿Por qué el análisis solo con NLP del texto es insuficiente para entender la blogosfera? (sección "Mapas de la blogosfera y bancos de peces")
R: Porque tratar el texto como un río solo muestra el nivel micro o macro y pierde la historia más importante; falta el SNA, que mapea los patrones de interacción entre los nodos.

P: ¿Cómo distingue la visualización una viralidad real de una fabricada, según el ejemplo de los vídeos? (sección "Mapas de la blogosfera y bancos de peces")
R: El discurso "I Have a Dream" aparece en picos espontáneos por toda la blogosfera, mientras que el vídeo de la campaña de Romney muestra un esfuerzo concertado de blogueros conservadores al unísono; un histograma simple lo haría parecer viral, pero la segmentación revela una operación planificada.

P: En el experimento de predecir la política de Egipto, ¿por qué podrían ser más útiles los registros telefónicos que las redes sociales? (sección "Experimento mental: predecir el futuro político de Egipto")
R: Porque las cosas cambian: la gente migra de plataforma y las discusiones pueden volverse clandestinas, y los registros telefónicos pueden representar mejor a quienes intentan pasar desapercibidos.

P: ¿Cómo se representa una red no dirigida y qué ventajas tiene la lista de incidencia? (sección "El SNA desde la estadística: representaciones y grafos aleatorios")
R: Se representa con una matriz N×N de unos y ceros (matriz de adyacencia), simétrica para redes no dirigidas; la lista de incidencia (para cada nodo, los nodos a los que se conecta) ahorra espacio y permite guardar atributos.

P: ¿Qué cambió para que el periodismo de datos dejara de ser dominio de usuarios avanzados de Excel? (sección "Periodismo de datos")
R: La aparición de más datos vía APIs, nuevas herramientas y computación barata, y el que coincidieran en más gente la buena escritura y la programación.

P: ¿Qué consejo da Bruner al iniciar un proyecto y a qué se parece? (sección "Periodismo de datos")
R: No tener una tesis fuerte antes de entrevistar a los expertos; entrar con una idea laxa y dispuesto a pivotar. Suena al análisis exploratorio de datos.

## Puntos a dominar

- Explicar por qué el mundo se entiende mejor como una red que como casos con atributos y qué se pierde con el enfoque caso-atributo.
- Reconocer los orígenes del SNA (teoría de grafos y sociometría) y su terminología: nodos, aristas, dyads, triads, cierre triádico, subredes, grafos bipartitos y ego networks.
- Distinguir las cuatro medidas de centralidad (grado, cercanía, intermediación, vector propio) y la noción de importancia que capta cada una.
- Elegir la red o subred correcta y reconocer que las medidas de centralidad se manipulan (p. ej. bots de Twitter que se siguen entre sí).
- Interpretar un mapa de blogosfera (fuerzas de repulsión/atracción, colores por clúster, tamaño por grado, Fruchterman-Reingold) y detectar viralidad fabricada.
- Aplicar el principio "primero las preguntas, luego los datos" al diseñar un estudio predictivo.
- Diferenciar los modelos de grafos aleatorios: Erdős–Rényi/Bernoulli, ERGM (transitividad, clustering, reciprocidad, k-stars) y sus problemas de inferencia (degeneración, un solo grafo observado).
- Describir el perfil del periodista de datos según Bruner: visualización, informática para datos sucios y plazos, experiencia de dominio y la traducción como habilidad central.
