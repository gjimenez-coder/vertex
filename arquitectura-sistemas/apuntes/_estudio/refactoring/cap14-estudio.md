# Capítulo 14 — Refactoring Tools (Herramientas de refactorización) — Estudio

## Tarjetas de repaso

P: Según el capítulo, ¿cuál ha sido uno de los mayores obstáculos a la refactorización?
R: La falta de soporte de herramientas; Smalltalk es la excepción cultural donde existen entornos potentes que la apoyan.

P: ¿Cuál es la tesis central del capítulo escrito por Don Roberts y John Brant?
R: Refactorizar con soporte automático de herramientas se siente distinto de hacerlo a mano: al abaratar la refactorización y el ajuste del formato, la limpieza mejora la mantenibilidad, reutilización y comprensibilidad.

P: ¿Qué tipo de criterios consideran los autores más importantes, los técnicos o los prácticos?
R: Los prácticos, porque la herramienta se crea para apoyar a una persona en una tarea y, si no encaja con su forma de trabajar, no se usará.

P: ¿Cuánto tarda Extract Method con el Refactoring Browser y qué hace la herramienta?
R: Unos 15 segundos; valida si la selección es legal, calcula los parámetros, pide un nombre, permite ordenar parámetros, extrae el código, lo reemplaza por una llamada y crea el método en la misma clase.

P: ¿Cuál es el propósito principal de una herramienta de refactorización?
R: Permitir refactorizar sin tener que volver a probar el programa, transformándolo mientras se preserva su comportamiento.

P: ¿Qué es la Program Database (base de datos del programa)?
R: La capacidad de buscar entidades del programa en todo el código (llamadas a un método, métodos que leen o escriben una variable de instancia); requiere análisis semántico, no `grep`.

P: ¿Por qué un enfoque con `grep` falla para construir la base de datos del programa?
R: Porque no distingue una variable `foo` de una función `foo`; hace falta parsing para determinar la «parte del discurso» de cada token.

P: ¿Para qué sirven los Parse Trees (árboles de análisis)?
R: Para manipular la estructura interna de un método, ya que muchas refactorizaciones operan por debajo del nivel de método (por ejemplo extraer parte de un método).

P: ¿Por qué es imposible la preservación total del comportamiento (Accuracy)?
R: Porque, por ejemplo, un cambio de milisegundos rompe un programa de tiempo real estricto, o renombrar un método invocado vía Java Reflection API por su nombre en un string lanzaría una excepción.

P: ¿Qué relación hay entre el abaratamiento de la refactorización y el diseño inicial?
R: Al abaratarse, los errores de diseño cuestan menos y se necesita menos diseño por adelantado; se diseña para el problema actual sabiendo que se puede extender después.

P: ¿Por qué la función de deshacer (Undo) habilita un diseño exploratorio?
R: Porque la inversa de una refactorización también preserva el comportamiento; con deshacer se puede crear clases, mover métodos y cambiar de rumbo sin miedo y muy rápido.

P: ¿Qué enseñó la implementación temprana del Refactoring Browser como herramienta separada?
R: Que nadie la usaba, ni siquiera sus autores; al integrarla en el Smalltalk Browser pasaron a usarla intensamente. La integración en el IDE fue decisiva.

P: Según los autores, ¿cómo afecta la refactorización asistida a las pruebas?
R: Se prueba menos porque muchas refactorizaciones son automáticas, pero el paso de pruebas no se elimina (hay refactorizaciones no automatizables). Empíricamente las pruebas se ejecutan las mismas veces al día, pero se refactoriza más.

## Preguntas de autoevaluación

P: ¿Cómo describe Kent Beck el cambio en su forma de programar con el Refactoring Browser?
R: Desaparecen los pensamientos del tipo «debería cambiar este nombre, pero…» porque siempre hay una opción de menú; tuvo que aprender a pensar refactorizaciones más grandes y rápidas, y ahora usa mitad refactorización y mitad código nuevo a la misma velocidad. (Sección: Refactoring with a Tool)

P: ¿Por qué refactorizar deja de ser una actividad separada de programar con soporte automático?
R: Porque no hay que probar tras las refactorizaciones automáticas, así que las actividades fluyen entre sí y el cambio de sombrero se hace menos evidente, aunque siga ocurriendo. (Sección: Refactoring with a Tool)

P: ¿En qué se diferencia el mantenimiento de la base de datos del programa entre Smalltalk y Java?
R: En Smalltalk la compilación dinámica actualiza la base de datos al cambiar una clase; en entornos estáticos como Java el código se escribe en archivos de texto y actualizarla requiere procesarlos, similar a compilar (VisualAge for Java imita la actualización dinámica). (Sección: Technical Criteria)

P: ¿Qué compensación (trade-off) plantea el criterio de velocidad y cómo se puede resolver un análisis demasiado lento?
R: Siempre se sopesa tiempo frente a precisión; si tarda demasiado, el programador lo hará a mano. Una opción es pedir la información al programador: no es demostrablemente seguro, pero traslada la responsabilidad a quien suele conocer el dato y aumenta el uso de la herramienta. (Sección: Practical Criteria)

P: ¿Por qué los autores dicen que no hace falta obsesionarse con los casos límite?
R: Porque la mayoría de los programas no son casos límite, y enfoques más simples y rápidos funcionan asombrosamente bien, aunque los informáticos tiendan a fijarse en los casos límite. (Sección: Practical Criteria)

P: ¿A qué atribuyen los autores el éxito del Refactoring Browser?
R: A que, siendo programadores, intentaron que encajara con su forma de trabajar: implementaban refactorizaciones manuales generales, aceleraban lo lento y mejoraban lo poco preciso. (Sección: Wrap Up)

P: ¿Por qué creen los autores que es más fácil desarrollar herramientas de refactorización para Java?
R: Porque Java es mucho más simple que el lenguaje con el que comparte sintaxis, y esperan evitar «los pecados de C++». (Sección: Wrap Up)

## Puntos a dominar

- Distinguir los criterios técnicos (base de datos del programa, árboles de análisis, precisión razonable) de los prácticos (velocidad, deshacer, integración con herramientas) y saber por qué los prácticos pesan más.
- Explicar el propósito principal de una herramienta de refactorización: refactorizar sin tener que volver a probar.
- Argumentar por qué `grep` es insuficiente y por qué hace falta análisis semántico para la base de datos del programa.
- Entender que la preservación total del comportamiento es imposible y conocer los casos que la rompen (tiempo real estricto, Java Reflection API).
- Reconocer el efecto de abaratar la refactorización sobre el diseño inicial y sobre la frecuencia de pruebas.
- Justificar por qué una herramienta separada del IDE no se usa y por qué la integración fue decisiva.
