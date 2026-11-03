# Refactoring, Reuse, and Reality (Refactorización, reutilización y realidad) — Estudio

## Tarjetas de repaso

P: ¿Quién escribió el capítulo 13 y por qué es relevante su figura?
R: William Opdyke, cuya tesis doctoral en la Universidad de Illinois fue el primer trabajo escrito mayor sobre refactorización.

P: ¿Cuál es la tesis central del capítulo?
R: Hacer la refactorización "real" exige atender las preocupaciones prácticas de desarrolladores y gerentes, no solo demostrar su valor teórico.

P: Según Opdyke, ¿dónde está la mayor parte del coste de los sistemas de larga vida?
R: En cambiarlos y adaptarlos durante décadas, no en construir la versión inicial.

P: ¿Cuáles son los tres caminos ante el software existente y qué los distingue?
R: Reescribir (caro y arriesgado), copiar-y-modificar (corrompe el diseño con el tiempo) y refactorizar (el punto medio que hace explícitas las ideas de diseño).

P: ¿Cuáles son las cuatro razones por las que los desarrolladores se resisten a refactorizar?
R: No entender cómo hacerlo, que el beneficio sea solo a largo plazo, que sea overhead frente a escribir features nuevas, y el riesgo de romper el programa.

P: ¿Cómo se relacionan las refactorizaciones de alto nivel con las de bajo nivel?
R: Las de alto nivel (crear superclase abstracta, extraer componente reutilizable) se definen en términos de las de bajo nivel, de modo que la seguridad se conoce por construcción.

P: ¿Qué rasgos de C++ favorecen la refactorización?
R: El tipado estático acota las referencias a renombrar, el control de acceso (public/protected/private) limita dónde existen referencias, la herencia facilita generalizar o especializar, y el compilador suele señalar bugs introducidos.

P: ¿Qué rasgos de C++ complican la refactorización?
R: La compatibilidad con C: punteros, casts y `sizeof(object)` introducen aliasing y exponen la representación interna, pudiendo alterar el comportamiento tras un cambio.

P: ¿Qué ilustra el caso del framework Choices?
R: Beneficios a corto plazo de refactorizar BSD → System V: errores corregidos en un solo sitio, menos código y separación de lo específico frente a lo común.

P: ¿Qué define una refactorización segura?
R: La que no rompe el programa: debe comportarse igual antes y después del cambio.

P: ¿Cómo garantiza seguridad la herramienta de Opdyke?
R: Con un analizador que verifica precondiciones (propiedades de scoping y typing); solo aplica la refactorización si todo es seguro y, ante la duda, avisa en vez de actuar.

P: ¿La refactorización segura detecta errores previos?
R: No; evita introducir errores nuevos, pero no detecta los que ya existían, aunque puede facilitar verlos.

P: ¿Qué modelo invoca Opdyke para la adopción tecnológica?
R: El modelo de Geoffrey Moore (Crossing the Chasm): una idea debe cruzar el "abismo" desde innovadores y early adopters hacia la early y late majority.

P: ¿Qué lección de Ralph Johnson atraviesa el capítulo?
R: Si alguien "no lo entiende", la culpa es del que comunica; es su responsabilidad desarrollar y transmitir bien las ideas.

## Preguntas de autoevaluación

P: ¿Por qué la refactorización tardó en ser adoptada por los profesionales de la industria?
R: Por la novedad de la tecnología orientada a objetos (pocos habían llegado a los problemas de evolución que resuelve) y por razones de sentido común por las que los desarrolladores se resisten a refactorizar. (Sección "Lo que necesitas saber")

P: ¿Cómo se refactorizó el sistema de archivos Choices para pasar de BSD a System V?
R: Primero se clonó y modificó la implementación BSD; luego se crearon superclases abstractas con el comportamiento común, se movieron variables y funciones comunes, y donde las funciones eran casi idénticas se extrajeron las diferencias a funciones por subclase hasta que lo idéntico pudo subir a la superclase. (Sección "El ejemplo que recorre el capítulo")

P: ¿Por qué se compara una herramienta de refactorización con aplicar lint a un programa C/C++?
R: Porque la herramienta no entiende el significado del programa: identifica debilidades estructurales y similitudes redundantes y solo sugiere; el programador decide qué aplicar. (Sección "Entender cómo y dónde refactorizar")

P: ¿Por qué refactorizar en C++ es más costoso por iteración que en Smalltalk o CLOS?
R: Porque C++ resuelve referencias en tiempo de compilación, así que cada iteración exige recompilar y relincar, mientras Smalltalk y CLOS permiten interpretación y compilación incremental. (Recuadro "Refactorizar programas C++")

P: ¿Qué límites tienen confiar en el programador, el compilador, las pruebas o la revisión de código para refactorizar con seguridad?
R: Los programadores son falibles; el compilador no atrapa ciertos errores (sobre todo de scoping ligados a herencia); probar todos los caminos es indecidible; y los revisores también son falibles y están ocupados. (Sección "Refactorizar con seguridad")

P: ¿Cómo se responde a la objeción de que refactorizar es overhead frente a escribir features?
R: Hay herramientas y técnicas que lo hacen rápido, el overhead se compensa con menor esfuerzo en otras fases, y al volverse rutina deja de sentirse como overhead y pasa a sentirse esencial. (Sección "Reducir el overhead")

P: ¿Por qué las cuatro preocupaciones aplican también a la reutilización y la transferencia de tecnología?
R: Porque en todas el personal puede no saber qué o cómo hacerlo, necesita beneficios a corto plazo, hay que atender overhead y curva de aprendizaje, y la adopción no debe ser disruptiva; son cuestiones genéricas de transferencia de tecnología. (Sección "Implicaciones para la reutilización y la transferencia de tecnología")

## Puntos a dominar

- Explicar por qué la refactorización es el punto medio entre reescribir y copiar-y-modificar.
- Enumerar y rebatir las cuatro objeciones típicas a refactorizar.
- Distinguir las refactorizaciones de bajo nivel de las de alto nivel y su relación de composición.
- Identificar qué rasgos de C++ ayudan y cuáles complican la refactorización, con el ejemplo del V-table.
- Definir qué es una refactorización segura y cómo las precondiciones verificables la garantizan.
- Relacionar las lecciones de refactorización con la reutilización y el modelo de Moore de cruce del abismo.
