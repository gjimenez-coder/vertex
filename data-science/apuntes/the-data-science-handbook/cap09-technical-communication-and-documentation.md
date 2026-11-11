# The Data Science Handbook — Field Cady (Wiley, 2017)
## Capítulo 9 — Technical Communication and Documentation (Comunicación técnica y documentación)

> Nota de extracción: el texto se obtuvo de la capa de texto del PDF; las citas usan la página del PDF. Contiene fragmentos de código, de los que se conservan solo los esenciales.

## Lo que necesitas saber
El capítulo defiende que el trabajo técnico de primera calidad puede quedar infravalorado si no se comunica bien, y que unos pocos principios sencillos marcan la diferencia entre ser incomprensible y ofrecer una presentación brillante. El autor admite que no se considera especialmente dotado para comunicar, pero precisamente por eso insiste en el valor de interiorizar unas pocas pautas.

El científico de datos ocupa un nicho inusualmente intensivo en comunicación: su trabajo es tender puentes entre los mundos del negocio, la analítica y el software. Mientras que los ingenieros hablan sobre todo con ingenieros y los analistas de negocio con otros analistas, el data scientist debe hacerse entender por todos ellos. El objetivo único de todo el capítulo es transmitir ideas a la audiencia de forma que (1) la entiendan de verdad y (2) les resulte fácil entenderla.

Sales sabiendo varios principios generales de comunicación técnica y luego consejos concretos para tres medios —presentaciones con diapositivas, informes escritos y exposiciones habladas— más una sección sobre documentación de código, que el autor describe como el medio de comunicación de último recurso.

## Principios generales (9.1)
Cady propone seis principios que, a su juicio, sustentan casi toda buena comunicación técnica:

- Conoce a tu audiencia. Es el principio más básico y de los más difíciles de dominar. Un data scientist habla con cuatro perfiles: expertos de dominio (saben del problema pero poco de software y analítica, y son muy útiles para detectar defectos en el trabajo o dar sentido a los datos); personas analíticas (quieren el detalle fino de la metodología estadística y las decisiones de modelado); ingenieros de software (tienden a tratar el código como caja negra, pero les importa mucho su rendimiento en el mundo real); y gente de negocio (desde exingenieros que preguntan detalles hasta gestores no técnicos que quieren todo traducido a "business speak"). Conocer a la audiencia incluye saber cuánto detalle incluir y cuánta "historia" del trabajo contar: a un ejecutivo le bastan unos pocos puntos clave; los pares quieren más metodología, sobre todo si los hallazgos sorprenden o cambiaron el rumbo del proyecto.

- Muestra por qué importa. Enmarca siempre la analítica en algo que a la gente ya le preocupe, normalmente un problema de negocio, y explica cómo se conecta con los resultados económicos. No hace falta insistir en exceso, pero sí dar un motivo para interesarse. Es también un buen ejercicio propio: si no sabes explicar en términos simples por qué un proyecto vale la pena, quizá deberías trabajar en otro problema.

- Hazlo concreto. El cerebro humano no maneja bien los conceptos abstractos, ni siquiera el de personas con formación. Dar unos cuantos "ganchos mentales" concretos ayuda enormemente. A menudo el propio caso de negocio aporta los ejemplos; cuando es demasiado enrevesado, conviene un problema de juguete simple.

- Una imagen vale más que mil palabras. El corazón de una presentación son una o pocas figuras clave; el resto del trabajo es, en esencia, un pie de foto extenso que explica cómo se generaron y cómo interpretarlas. La falta de imágenes suele ser señal de pereza, porque elaborar buenas figuras exige planificación y trabajo.

- No seas arrogante con tu conocimiento técnico. Menospreciar a quien sabe menos matemáticas arruina la relación y levanta barreras a la comunicación; además, dominar las ecuaciones no equivale a pensar con claridad. El autor recuerda a una gestora sin formación estadística que, por ser lista y sensata, hacía siempre las preguntas correctas, mejor que muchos data scientists.

- Haz que se vea decente. La estética no es periférica: el diseño gráfico es una forma pragmática de asegurar que la comunicación sea clara y convincente, igual que usar ejes logarítmicos ayuda a transmitir una idea.

## Presentaciones con diapositivas (9.2)
Las diapositivas son el medio más común y el de mayor impacto para comunicar resultados de ciencia de datos, porque es más probable que la gente escuche una charla que lea un informe. El mayor error es tratarlas como un informe escrito —incluso copiando y pegando texto de un documento—: son un medio distinto, regido por otras reglas. Dan control total sobre el aspecto, pero la audiencia espera recorrerlas mucho más rápido que un informe, así que deben ser nítidas y al grano, sustituyendo texto por contenido gráfico siempre que se pueda. El segundo error es pasarse: formas raras, imágenes en movimiento y fotos de gatos deben usarse con mucha mesura.

Regla práctica: el 75 % de las diapositivas debería consistir en una imagen (un gráfico de datos, un diagrama de flujo, etc.) y, como mucho, dos frases que den el mensaje para llevar de esa imagen.

### Diseño C.R.A.P. (9.2.1)
Muchos principios de buen diseño se resumen en el acrónimo C.R.A.P.: contrast, repetition, alignment, proximity.

- Contrast (contraste): lo que es distinto debe parecer distinto —distintas fuentes para código, texto y pies de figura; distintos colores para distintos segmentos de cliente; distintos tamaños de fuente para enfatizar.
- Repetition (repetición): los puntos o motivos clave deben repetirse a lo largo del trabajo, de forma obvia para que calen pero sutil para no molestar. Es en parte el dual del contraste.
- Alignment (alineación): es lo más puramente estético; las partes del campo visual deben alinearse de forma natural (o estar claramente desalineadas si se contrastan), para que nadie se distraiga preguntándose si dos bloques están ligeramente torcidos.
- Proximity (proximidad): usa la distancia entre elementos para indicar sus relaciones y aprovecha la disposición del campo visual.

El autor muestra una diapositiva propia mal diseñada (todo en la misma fuente, el propósito con el mismo rango que los temas, exceso de espacio en blanco, todo alineado con todo) y su versión corregida aplicando C.R.A.P. El contenido es idéntico: el diseño gráfico no suplementa el contenido, sino que hace que se note.

### Consejos y reglas prácticas (9.2.2)
Entre los que el autor destaca: evitar frases largas (sustituirlas por expresiones cortas); no más de cuatro viñetas por sección; partir una diapositiva en dos si hay demasiado; preferir llamadas con flechas sobre una figura antes que listas; si una imagen se repite en diapositivas consecutivas, colocarla exactamente en la misma posición (nada más molesto que un salto de unos píxeles); evitar la fuente Comic Sans salvo que conozcas bien a tu audiencia; usar PNG con fondo transparente; etiquetar siempre los ejes; poner un fondo de diapositiva sencillo; incluir color, evitando combinar rojo y verde por el daltonismo; permitirse un tono más informal que en un informe, sin excederse; calcular unos 2 minutos por diapositiva; e incluir números de diapositiva, fechas o logotipo como puntos de referencia.

## Informes escritos (9.3)
Primer consejo del autor: no usar LaTeX salvo que vayas a publicar en una revista científica o quieras dar aspecto académico; su sintaxis idiosincrásica impide la edición colaborativa, y su control fino rara vez es necesario y a menudo se abusa de él. Recomienda Microsoft Word, Google Docs u otro editor WYSIWYG (escribió el libro en Word).

La estructura varía según la audiencia y el problema, pero la mayoría de informes técnicos tendrán un subconjunto de estas secciones:

- Resumen ejecutivo: hasta una página con el problema, lo que hiciste y qué puede hacerse con ello, con énfasis en el negocio.
- Antecedentes y motivación: cómo encaja el trabajo en un contexto mayor.
- Datasets usados: cuáles, de dónde salen, qué describen y sus limitaciones; breve, con los detalles en un apéndice.
- Visión analítica general: la analítica o el algoritmo a alto nivel, centrada en el modelo matemático abstracto más que en su implementación, idealmente con algún diagrama.
- Resultados: a menudo la parte más importante; presentarlos de forma gráfica, nítida y convincente, ligados al contexto; incluir solo los más interesantes y dejar el resto en un apéndice.
- Visión general del software: muchas veces innecesaria y, si se incluye, breve; relevante si el código se integra en otro sistema o se reejecutará; explica cómo ejecutarlo (pocas líneas; si no, refactoriza) y da una arquitectura de alto nivel.
- Trabajo futuro: a veces un relleno que puede omitirse, pero también una oportunidad para señalar nuevos proyectos o descartarlos.
- Conclusiones.
- Apéndices con detalles técnicos: para el autor, hasta la mitad del informe.

## Hablar: lo que me ha funcionado (9.4)
El autor rechaza el truco clásico de imaginar desnuda a la audiencia. Hay estilos muy distintos; a él no le funciona guionizar al detalle. Su método: tener un buen deck, practicar mucho explicando en voz alta cada diapositiva sin guion, y el día de la charla improvisar vigilando el tiempo. Habla bien de forma espontánea y se vuelve aburrido cuando sigue un plan.

El estándar de oro es que la exposición parezca una conversación con alguien bien preparado y bueno explicando, no un discurso formal. En ello influyen el tono, la cadencia, las expresiones faciales y el movimiento corporal, independientes de las palabras; como es demasiado para controlarlo a la vez, la única solución es practicar hasta que sea segunda naturaleza. Recomienda entrenar una "personalidad al hablar" y practicar explicaciones improvisadas de temas de tu trabajo (ante un espejo, amigos o en tu cabeza). Pautas al explicar: ser claro y vocalizar; hablar algo más despacio de lo normal porque la gente también atiende a las diapositivas; incluir una anécdota, broma u opinión breve para humanizar sin excederse; preferir una pausa corta a un "um"; ser animado para mostrar entusiasmo; adoptar una cadencia natural y relajada (el nerviosismo se nota); cuidar la postura (erguido, hombros atrás y abajo, lo que según investigación aumenta la confianza real); y vigilar los gestos de las manos, que en dosis moderadas dan énfasis. A quien sufra ansiedad profunda ante hablar en público le sugiere Toastmasters o grupos similares.

## Documentación de código (9.5)
Siempre que entregues una pieza de código significativa, acompáñala de documentación de qué hace y cómo usarla. Puede tomar varias formas: un comentario largo al inicio del archivo, un runbook o manual de usuario aparte (típico en software grande o para clientes/otros equipos), páginas en una wiki de empresa, o tests unitarios ejecutables.

Lo más importante es explicar cómo ejecutar el código y reproducir su funcionalidad, para que el usuario lo use y verifique que funciona. Explicar su funcionamiento interno es secundario y entrar en demasiado detalle puede ser contraproducente: si entregas el fuente, es razonable esperar que lo lean; basta con indicar por dónde empezar y dar un breve resumen de arquitectura señalando qué hace cada módulo. Muy recomendable incluir una sección de solución de problemas (troubleshooting) con los fallos raros o las partes frágiles específicas de tu software, que ahorra horas de depuración.

## Ideas clave
- El objetivo de toda comunicación técnica es que la audiencia entienda tus ideas y le resulte fácil hacerlo; el data scientist debe puentear negocio, analítica y software.
- Seis principios guía: conoce a tu audiencia, muestra por qué importa, hazlo concreto, usa imágenes, no seas arrogante y cuida la estética.
- Las diapositivas no son informes: deben ser nítidas y gráficas (regla del 75 % imagen) y aplicar el diseño C.R.A.P. (contraste, repetición, alineación, proximidad).
- El diseño gráfico no suplementa el contenido: hace que la audiencia lo note.
- En informes escritos, evita LaTeX fuera del ámbito académico y estructura en secciones (resumen ejecutivo, antecedentes, datasets, visión analítica, resultados, software, trabajo futuro, conclusiones, apéndices).
- Para hablar bien, practica hasta que tono, cadencia y postura sean segunda naturaleza y la charla parezca una conversación.
- La documentación de código debe priorizar cómo ejecutarlo y reproducirlo, con un breve mapa de arquitectura y una sección de troubleshooting.
