# Storytelling with Data — Cole Nussbaumer Knaflic (Wiley, 2015)
## Capítulo 5 — Think Like a Designer (Piensa como un diseñador)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas usan la página del PDF. Libro muy visual: las figuras se describen con palabras.

## Lo que necesitas saber
El capítulo aplica conceptos tradicionales del diseño a la comunicación con datos, partiendo del lema "la forma sigue a la función": primero decide qué quieres que tu audiencia pueda hacer con los datos (función) y luego crea la visualización (forma) que lo permita con facilidad. La tesis es que no hace falta ser diseñador profesional para reconocer y crear buen diseño; basta con conocer algunos principios y aprender a confiar en el propio ojo.

Se recorren cuatro grandes ideas: *affordances* (señales que indican cómo usar la visualización), *accesibilidad* (que sea comprensible por personas de habilidades diversas), *estética* (que resulte agradable), y *aceptación* (lograr que la audiencia adopte el nuevo diseño). Al terminar sabrás resaltar lo importante, eliminar distracciones, crear una jerarquía visual, no complicar en exceso, usar el texto como aliado y manejar la resistencia al cambio.

## El ejemplo que recorre el capítulo
Varios ejemplos se encadenan. El principal es un gráfico del Pew Research Center (2014) sobre la "Tasa de nuevos matrimonios por nivel educativo": se transforma paso a paso para ilustrar resaltado y eliminación de distracciones. También reaparece el ejemplo de los tickets (de los capítulos 3 y 4) para mostrar el poder del texto.

## Affordances
En diseño, las *affordances* son aspectos inherentes al objeto que hacen evidente cómo se usa: un pomo invita a girarlo, un botón a pulsarlo, un cordón a tirar de él. Cuando hay suficientes affordances, el buen diseño se vuelve invisible. El autor cita la marca OXO y su "diseño universal": sus utensilios de cocina solo se pueden sujetar de la forma correcta (Figura 5.1). Llevado a los datos, podemos usar affordances visuales para indicar a la audiencia cómo leer e interactuar con la visualización. Tres lecciones: (1) resaltar lo importante, (2) eliminar distracciones y (3) crear una jerarquía clara de la información.

### Resaltar lo importante
Los atributos preatentivos dirigen la atención, pero solo funcionan si se aplican a una fracción del total; según *Universal Principles of Design* (Lidwell, Holden y Butler, 2003) conviene resaltar como máximo el 10% del diseño. Pautas:

- **Negrita, cursiva y subrayado**: para títulos, etiquetas, pies y secuencias cortas. Se prefiere la negrita (añade poco ruido y destaca bien); la cursiva destaca menos y es menos legible; el subrayado añade ruido y compromete la legibilidad (usar poco o nada).
- **MAYÚSCULAS y tipografía**: las mayúsculas en secuencias cortas se escanean fácil (títulos, etiquetas, palabras clave). Evitar cambiar de fuente para resaltar.
- **Color**: eficaz si se usa con moderación y en combinación con otras técnicas (p. ej., negrita).
- **Invertir elementos**: atrae la atención pero añade bastante ruido; usar poco.
- **Tamaño**: también señala importancia.

El autor descarta el parpadeo (que Lidwell reserva para información crítica urgente) por molesto. Los atributos pueden combinarse: algo muy importante puede ser grande, de color y en negrita a la vez.

En el ejemplo Pew (Figura 5.2), un gráfico de barras agrupadas por nivel educativo; el color más oscuro de las barras de 2012 desvía la atención sin apoyar el mensaje. En la Figura 5.3 se usa el naranja solo para "Bachelor's degree or more" y gris para todo lo demás, señalando dónde mirar.

### Eliminar distracciones
Citando a Saint‐Exupéry, "sabes que has alcanzado la perfección no cuando no tienes nada más que añadir, sino cuando no tienes nada más que quitar" (PDF p. 148). Lo que se recorta puede importar más que lo que se destaca. Para detectar distracciones, piensa en *desorden* (elementos que ocupan espacio sin aportar información) y *contexto* (lo necesario para que el mensaje tenga sentido: ni demasiado ni demasiado poco). Consideraciones:

- No todos los datos importan igual: elimina datos o componentes no críticos.
- Cuando no se necesita el detalle, resume.
- Pregúntate: ¿eliminar esto cambiaría algo? Si no, quítalo.
- Empuja al fondo lo necesario pero sin impacto en el mensaje (el gris claro funciona bien para restar énfasis).

Cada reducción hace destacar más lo que queda. Si dudas del detalle, busca incluirlo sin diluir el mensaje (p. ej., llevarlo a un apéndice en una presentación).

En la Figura 5.4 se aplican varios cambios al gráfico Pew: el mayor es pasar de barras a un gráfico de líneas (mejor para tendencias temporales), reduciendo de 25 barras a 4 líneas con los extremos destacados y un único eje x compartido. Se elimina la categoría "All" (agregado redundante), se redondean los decimales de las etiquetas, se quita la cursiva del subtítulo y su espaciado, y se extiende el resaltado de "Bachelor's degree or more" al nombre de la categoría. La Figura 5.5 muestra el antes y el después.

### Crear una jerarquía visual de la información
Los mismos atributos preatentivos que resaltan sirven para ordenar: traer unos elementos al frente y empujar otros al fondo, indicando el orden de lectura. Un recurso útil son las *supercategorías*: agrupar y etiquetar (p. ej., edad, raza, nivel de ingresos, educación) para dar una estructura jerárquica que facilite la lectura de tablas o gráficos con muchos desgloses.

El ejemplo es un diagrama de dispersión de un fabricante de coches (Figura 5.6): compara modelos según satisfacción del cliente y frecuencia de problemas frente a la media del año anterior. La autora describe el orden en que lee: primero el título (con "Issues" y "Satisfaction" en negrita), luego los ejes ("Things Gone Wrong" de pocos arriba a muchos abajo; satisfacción de baja a alta), después el punto gris oscuro "Prior Year Average" (~900 problemas por 1.000 y 72% satisfechos), y por último el rojo del cuadrante inferior derecho (alta satisfacción pero muchos problemas, peor que la media). Las etiquetas de cuadrante funcionan como supercategorías; los cuadrantes izquierdos no se etiquetan porque no hay datos. Su marido, daltónico rojo‐verde, fue directo al rojo porque destacaba lo suficiente. En cualquier orden, la jerarquía ordena un visual complejo sin que se sienta complicado.

## Accessibility (Accesibilidad)
La accesibilidad dice que los diseños deben ser usables por personas de habilidades diversas. Aplicado a datos: debe entenderlo gente de muy distinta destreza técnica; aunque seas ingeniero, no debería hacer falta un título de ingeniería para leer tu gráfico. La responsabilidad recae en ti, el diseñador. Ejemplo: el mapa del metro de Londres de Harry Beck (1933), que descartó la geografía real y se volvió una guía esencial y plantilla mundial. Dos estrategias: (1) no complicar en exceso y (2) el texto es tu amigo.

### No complicar en exceso
"Si es difícil de leer, es difícil de hacer": Song y Schwarz (Universidad de Michigan, 2008) dieron a unos estudiantes instrucciones de ejercicio en fuente legible (Arial) y a otros en una fuente cursiva (Brushstroke). Los de la fuente recargada juzgaron la rutina más difícil y fueron menos proclives a intentarla; un segundo estudio con una receta de sushi lo confirmó. Traducido a datos: cuanto más complicado parece un visual, más tiempo cree la audiencia que costará entenderlo y menos lo intentará. Consejos: hacerlo legible (tipografía y tamaño consistentes y fáciles), mantenerlo limpio con affordances, usar lenguaje directo (palabras sencillas, menos palabras, definir tecnicismos y desplegar siglas) y eliminar la complejidad innecesaria. No se trata de simplificar en exceso, sino de no complicar más de lo necesario. Un recuadro aparte ("¿de quién es la culpa del mal diseño?") recuerda que cuando la gente no entiende un gráfico suele culparse a sí misma, pero casi siempre la culpa es del diseño.

### El texto es tu amigo
El texto etiqueta, introduce, explica, refuerza, resalta, recomienda y cuenta una historia. Algunos textos son obligatorios: todo gráfico necesita título y todo eje necesita título (las excepciones son rarísimas); su ausencia obliga a la audiencia a detenerse a descifrar qué está viendo. No supongas que dos personas llegarán a la misma conclusión: si quieres que lleguen a una, escríbela y hazla destacar con atributos preatentivos. Un recuadro sobre *action titles* recomienda usar la barra de título de las diapositivas para una conclusión accionable ("El gasto estimado de 2015 supera el presupuesto") en vez de un título descriptivo redundante ("Presupuesto 2015").

También puede anotarse directamente sobre el gráfico. Un ejemplo favorito es "Peak Break‐up Times" de David McCandless (Figura 5.7), que anota las rupturas en Facebook: subida en San Valentín, picos en Spring Break ("¿limpieza de primavera?"), pico en los Inocentes (April Fool's), tendencia de rupturas los lunes, subida y bajada en verano y un gran aumento antes de las fiestas con caída brusca en Navidad ("demasiado cruel"). Ahí, deliberadamente, el eje vertical no se etiqueta: interesan los picos y valles relativos, y no etiquetarlo evita debates sobre la métrica; es una excepción consciente y rara.

Se retoma el ejemplo de los tickets: la Figura 5.8 muestra un gráfico limpio con marcadores y etiquetas pero sin palabras. La Figura 5.9 añade lo imprescindible (título "Ticket volume over time", títulos de eje, nota de fuente). La Figura 5.10 va más allá con un *action title* ("Please approve the hire of 2 FTEs...") y una anotación que explica que dos empleados se fueron en mayo y desde agosto no se ha podido recuperar el ritmo.

## Aesthetics (Estética)
¿Hace falta "hacerlo bonito"? Un rotundo sí. La gente percibe los diseños más estéticos como más fáciles de usar, lo sean o no; además se aceptan y usan más, fomentan el pensamiento creativo y hacen a las personas más tolerantes con los problemas del diseño. Ejemplo: el jabón líquido Method (Figura 5.11), cuyo frasco antropomórfico era una pieza de arte para exhibir; su atractivo hacía que la gente tolerara que goteara. En datos, dedicar tiempo a la estética gana paciencia de la audiencia y aumenta las probabilidades de que el mensaje llegue. Si no confías en tu ojo, colecciona visualizaciones que te gusten e imita lo que funciona.

Tres puntos a cuidar:
1. **Sé inteligente con el color**: siempre intencional, escaso y estratégico, solo donde quieras resaltar.
2. **Cuida la alineación**: organiza los elementos creando líneas verticales y horizontales limpias para dar unidad.
3. **Aprovecha el espacio en blanco**: conserva márgenes; no estires los gráficos ni añadas cosas solo porque sobra espacio.

Bien hechos, estos elementos no se notan; mal hechos (colores arcoíris, falta de alineación y de espacio) resultan incómodos y denotan descuido y falta de respeto por los datos y la audiencia. En el ejemplo de segmentos de clientes de un minorista (Figura 5.12), el color está sobreutilizado (demasiados colores compiten; el recuadro rojo sobre los segmentos 3–5 cuesta verse), los elementos no están alineados (título centrado, títulos de segmento sin línea limpia) y el espacio en blanco está mal usado (demasiado entre títulos y datos, y columnas demasiado juntas con líneas de puntos innecesarias). La Figura 5.13 corrige todo: color estratégico, alineación y buen uso del espacio en blanco crean organización visual y transmiten respeto por el trabajo y la audiencia, animando a dedicarle tiempo.

## Acceptance (Aceptación)
Para ser efectivo, un diseño debe ser aceptado por su audiencia. Es natural que la gente sienta incomodidad ante el cambio: Lidwell et al. describen esa tendencia a resistirse a lo nuevo por familiaridad con lo viejo, así que cambiar "como siempre se ha hecho" exige más esfuerzo que simplemente sustituir. Estrategias para ganar aceptación:

- **Articula los beneficios** del enfoque nuevo: dar transparencia sobre por qué cambia ayuda; señala qué observaciones nuevas o mejores permite.
- **Muestra el lado a lado**: si lo nuevo es claramente superior, el antes‐y‐después lo demuestra, explicando por qué quieres cambiar.
- **Ofrece varias opciones y pide opinión**: en vez de imponer, crea alternativas y recoge feedback.
- **Gana a un miembro influyente** de la audiencia: háblale uno a uno, incorpora su feedback; si se suma, otros seguirán.

Ante la resistencia, pregúntate si el problema es la aversión al cambio o fallos reales de tu diseño. Pruébalo con alguien sin interés en juego: que piense en voz alta al revisar el visual (y los históricos, si procede), qué le gusta, qué dudas tiene y cuál prefiere. Un tercero imparcial puede revelar problemas de diseño o ayudarte a formular argumentos.

## Ideas clave
- La forma sigue a la función: primero define qué debe hacer la audiencia con los datos, luego diseña la forma que lo permita.
- Usa affordances visuales: resalta solo lo importante (≤10% del visual), elimina distracciones y crea una jerarquía con atributos preatentivos.
- Lo que quitas o atenúas (gris claro) puede importar más que lo que destacas; cada reducción hace brillar lo que queda.
- Accesibilidad: no compliques en exceso (fuentes legibles, lenguaje simple) porque lo complicado ahuyenta a la audiencia.
- El texto es imprescindible: titula gráfico y ejes, escribe la conclusión que quieres que se entienda y usa action titles y anotaciones.
- La estética importa: el buen aspecto aumenta la percepción de usabilidad y la tolerancia a los problemas del diseño.
- Color intencional, alineación limpia y espacio en blanco cuidado transmiten organización y respeto por la audiencia.
- Para que un diseño se adopte hay que gestionar la resistencia al cambio: explica beneficios, muestra el antes‐y‐después, ofrece opciones y gana a aliados influyentes.
