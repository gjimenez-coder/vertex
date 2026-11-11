# The Data Science Handbook — Field Cady (Wiley, 2017)
## Capítulo 1 — Introduction: Becoming a Unicorn (Introducción: Convertirse en un unicornio)

> Nota de extracción: texto obtenido de la capa de texto del PDF; las citas indican la página como (PDF p. N).

## Lo que necesitas saber

El capítulo abre el libro con una definición propia de data science: hacer trabajo analítico que, por un motivo u otro, exige una cantidad sustancial de habilidades de ingeniería de software (PDF p. 17). A veces el entregable final es el mismo que daría un estadístico o un analista de negocio, pero alcanzarlo requiere destrezas de software que un analista típico no tiene: datos tan grandes que obligan a computación distribuida, formatos tan enrevesados que necesitan muchas líneas de código para parsearlos, o software de producción que implementa las ideas analíticas en tiempo real.

La tesis central es que las personas capaces de construir buenos modelos estadísticos, programar software de calidad y conectar todo con problemas de negocio son tan raras que los reclutadores las llaman "unicornios". Cady sostiene que convertirse en unicornio no solo es posible sino relativamente sencillo: es cuestión de adquirir el equilibrio concreto de habilidades. Son raros por un accidente histórico —pocos programas educativos enseñan todas esas destrezas—, no porque una sola persona no pueda dominarlas.

Al terminar el capítulo sabes qué entiende el autor por data science, en qué se distingue de la estadística, cómo está organizado el libro, cómo usarlo, por qué todo el código está en Python y qué datasets y código de ejemplo vas a encontrar. El libro no pretende ser exhaustivo —el campo es demasiado grande y cambia demasiado rápido—, sino dar una base sólida del panorama general y un conjunto de habilidades "completo" para salir a trabajar.

## ¿Acaso los data scientists no son solo estadísticos sobrepagados?

Cady recoge la frase de Nate Silver: "I think data scientist is a sexed-up term for statistician" (PDF p. 18) y admite que tiene parte de razón, pero solo parte. La estadística se ocupa sobre todo de métodos matemáticos rigurosos para problemas bien definidos. El data scientist pasa la mayor parte del tiempo llevando los datos a una forma donde esos métodos siquiera puedan aplicarse: asegurar que el problema analítico encaje con los objetivos de negocio, extraer features significativas de los datos crudos y lidiar con patologías y casos borde raros. Una vez hecho ese trabajo pesado se aplican las herramientas estadísticas —aunque muchas veces ni siquiera hacen falta.

Históricamente, el data science surgió de forma independiente de la estadística. Los primeros data scientists eran programadores o expertos en machine learning que trabajaban con problemas de Big Data y analizaban conjuntos que los estadísticos no tocaban: páginas HTML, imágenes, correos, logs crudos de servidores web. Esos datos no encajan en bases de datos relacionales ni en herramientas estadísticas, así que durante décadas se acumularon sin analizar; el data science nació para exprimirles valor. Cady predice que en 20 años estadística, data science y machine learning se fundirán en una sola disciplina, porque sus diferencias son de grado o de accidente histórico. Pero de momento resolver problemas de data science exige habilidades que el estadístico normal no tiene —ingeniería de software extensa y extracción de features específica del dominio—, y ese trabajo constituye la abrumadora mayoría de la tarea: la estadística juega un papel secundario.

## ¿Cómo está organizado este libro?

El libro se divide en tres secciones:

- The Stuff You'll Always Use: temas que se usan en casi cualquier proyecto; habilidades core indispensables a cualquier nivel. Esta parte sirve también a quien solo necesita data science para responder una pregunta concreta sin aspirar a ser data scientist completo; para ellos, la Parte I probablemente baste.
- Stuff You Still Need to Know: habilidades core adicionales. Algunas, como clustering, son tan comunes que casi entran en la primera sección; otras, como el procesamiento de lenguaje natural, son especializadas, críticas en ciertos dominios y superfluas en otros. El autor considera que un data scientist debe manejar todas, aunque no las use siempre.
- Stuff That's Good to Know: temas opcionales. Algunos amplían temas de las secciones anteriores con más fondo teórico; otros son material nuevo que aparece en data science pero con el que se puede pasar una carrera sin toparse.

## ¿Cómo usar este libro?

El libro se escribió pensando en tres usos (PDF p. 19-20): leerlo de principio a fin como un curso autocontenido que te deja listo para problemas reales (quien tenga base fuerte en programación o matemáticas encontrará parte como repaso); usarlo para ponerse al día rápido en un tema concreto, ya que los capítulos son bastante autocontenidos, sobre todo tras la primera sección; y aprovechar el abundante código de ejemplo, en piezas lo bastante grandes como para servir de punto de partida de tus propios proyectos.

## ¿Por qué todo está en Python?

Todo el código de ejemplo está en Python, salvo algunos lenguajes específicos de dominio como SQL. El objetivo no es empujar a nadie a usar Python —hay muchas buenas herramientas—, sino usar un solo lenguaje en todos los ejemplos para mantener el libro legible y permitir seguirlo conociendo uno solo. Cady elige Python por dos razones: es el lenguaje más popular entre data scientists, con R como único gran competidor libre, y él lo considera directamente mejor (salvo algunos paquetes estadísticos oscuros de R rara vez necesarios); y porque "para cualquier tarea, Python es el segundo mejor lenguaje" (PDF p. 20): un todoterreno. Si solo necesitas estadística, cálculo numérico o parsing web hay opciones mejores, pero si debes hacer todo eso dentro de un mismo proyecto —como ocurre en el data science, inherentemente multidisciplinar— Python es la mejor opción. Consejo del autor: es mucho mejor dominar un lenguaje hasta producir código fiable y de calidad que ser mediocre en varios.

## Código de ejemplo y datasets

El libro es rico en código de ejemplo, en bloques bastante largos, por dos razones: como data scientist necesitas saber leer piezas largas de código —habilidad no opcional—, y para facilitar que reutilices el código del libro. El autor libera el código al dominio público (con o sin atribución) y lo publica en su página de GitHub, www.github.com/field-cady. Los datos de ejemplo vienen en dos formas: datasets de prueba incluidos en las librerías científicas de Python, y datos extraídos de Internet (fuentes como Yahoo y Wikipedia), en cuyo caso los scripts de ejemplo incluyen el código que descarga los datos.

## Palabras de despedida

El autor espera que el libro no solo enseñe a hacer data science práctico, sino que transmita lo emocionante de esta disciplina profundamente interdisciplinar, e invita a escribirle con comentarios o erratas a través de www.fieldcady.com.

## Ideas clave

- Data science = trabajo analítico que exige una cantidad sustancial de ingeniería de software.
- El "unicornio" combina modelos estadísticos, software de calidad y conexión con el negocio; es alcanzable, no un don raro.
- Frente a la estadística, el grueso del trabajo es preparar datos, extraer features y encajar el problema con el negocio; la estadística es secundaria.
- El data science nació para analizar datos no estructurados (HTML, imágenes, correos, logs) que las herramientas estadísticas ignoraban.
- Cady prevé que estadística, data science y machine learning se fundirán en 20 años.
- Tres secciones: lo que siempre usarás, lo que aún debes saber y lo bueno de conocer.
- Tres modos de uso: curso completo, consulta puntual por tema o fuente de código reutilizable.
- Python se usa por ser el más popular y el mejor "segundo mejor" para proyectos multidisciplinares; mejor dominar un lenguaje que ser mediocre en varios.
