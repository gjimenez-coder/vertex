# Refactoring: Improving the Design of Existing Code — Martin Fowler (con Kent Beck, John Brant, William Opdyke y Don Roberts) (Addison-Wesley, 1999)
## Prólogo — Preface (Prefacio)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas indican la página como `(PDF p. N)`.

## Lo que necesitas saber

El prólogo presenta la refactorización (refactoring) como el hilo conductor de todo el libro y explica por qué Fowler decidió escribirlo. Arranca con una anécdota personal sobre un proyecto que fracasó por tener un código demasiado complejo de depurar y ajustar, y cómo Kent Beck lo relanzó insistiendo en una limpieza continua del código mediante refactorización. De ahí surge la motivación: transmitir el conocimiento que Kent y otros aprendieron usando refactoring para mejorar la calidad del software.

La tesis central es que el diseño no tiene por qué ocurrir todo por adelantado: con refactorización, el diseño sucede de forma continua durante el desarrollo, de modo que el programa mantiene un buen diseño a medida que crece. Es la inversión de la noción habitual de decaimiento del software.

Sales sabiendo qué es refactoring, cómo está organizado el libro, para quién está escrito, qué recorrido de lectura seguir según tu objetivo, y a quiénes reconoce Fowler como fundadores del campo.

## El ejemplo que recorre el capítulo

La historia del consultor que visita un proyecto con una jerarquía de clases desordenada. Las clases de nivel superior hacían suposiciones embebidas en código heredado que no encajaba con todas las subclases y se sobrescribía en exceso; en otros lugares se duplicaba comportamiento o había código que podía subir en la jerarquía. Los programadores dedicaron un día o dos a limpiarla y eliminaron la mitad del código sin reducir funcionalidad, volviéndola más rápida y fácil de extender. La dirección no quedó contenta por las presiones de calendario. Fowler revela que él era ese consultor: seis meses después el proyecto fracasó por el exceso de complejidad del código. Kent Beck fue traído para reiniciarlo, reescribiéndolo casi por completo e insistiendo en la limpieza continua mediante refactorización.

## What Is Refactoring? (¿Qué es refactoring?)

Refactoring es el proceso de cambiar un sistema de software de modo que no altere el comportamiento externo del código pero mejore su estructura interna. Es una forma disciplinada de limpiar el código que minimiza las probabilidades de introducir errores; en esencia, mejorar el diseño del código después de haberlo escrito.

Esa frase —"mejorar el diseño después de escrito"— es contraintuitiva: la concepción habitual es diseñar primero y codificar después, y con el tiempo la integridad del sistema se desvanece y el código "se hunde de la ingeniería al hacking". Refactoring es lo opuesto: partiendo de un mal diseño, incluso del caos, se reelabora hasta un código bien diseñado. Cada paso es simple —mover un campo de una clase a otra, extraer código de un método para convertirlo en su propio método, subir o bajar código por la jerarquía—, pero el efecto acumulado de estos pequeños cambios puede mejorar radicalmente el diseño.

## What's in This Book? (¿Qué hay en este libro?)

Es una guía de refactoring para el programador profesional, cuyo objetivo es mostrar cómo refactorizar de forma controlada y eficiente sin introducir errores. Estructura:

- Capítulo 1: toma un programa pequeño con defectos de diseño comunes y lo refactoriza a un programa orientado a objetos más aceptable. Es el capítulo clave para entender de qué va realmente el refactoring.
- Capítulo 2: principios generales, definiciones, razones para refactorizar y algunos de sus problemas.
- Capítulo 3: con Kent Beck, cómo detectar "bad smells" (malos olores) en el código y limpiarlos con refactorizaciones.
- Capítulo 4: cómo integrar tests en el código con un framework de pruebas de Java simple y open-source, dado el papel crucial de las pruebas.
- Capítulos 5 a 12: el corazón del libro, el catálogo de refactorizaciones. No es exhaustivo, sino el comienzo de un catálogo; recuerda cómo ejecutar cada refactorización (por ejemplo, Replace Conditional with Polymorphism) de forma segura y paso a paso.
- Capítulo 13: Bill Opdyke, sobre la adopción de refactoring en desarrollo comercial.
- Capítulo 14: Don Roberts y John Brant, sobre el futuro real del refactoring, las herramientas automatizadas.
- Capítulo 15: la última palabra, a cargo de Kent Beck.

## Refactoring in Java (Refactoring en Java)

Todos los ejemplos están en Java porque es el lenguaje que Fowler conoce mejor, aunque el refactoring aplica a otros lenguajes y hay notas ocasionales para ellos. Para comunicar mejor las ideas, evita áreas complejas de Java (inner classes, reflection, threads y otras características potentes) y se centra en las refactorizaciones esenciales. Advierte que estas refactorizaciones no están pensadas para programación concurrente ni distribuida, temas fuera del alcance del libro.

## Who Should Read This Book? (¿Quién debería leer este libro?)

Dirigido al programador profesional que vive de escribir software; incluye mucho código que leer y entender, todo en Java (elegido por ser cada vez más conocido, comprensible para quien tiene base en C y orientado a objetos, lo que ayuda al refactoring). Aunque está centrado en el código, el refactoring impacta fuertemente en el diseño del sistema, por lo que es vital que diseñadores senior y arquitectos entiendan sus principios. Se introduce mejor de la mano de un desarrollador respetado y experimentado, capaz de adaptar los principios al entorno concreto, sobre todo con lenguajes distintos de Java.

Recorridos de lectura según el objetivo:

- Entender qué es refactoring: leer el Capítulo 1.
- Entender por qué refactorizar: leer los dos primeros capítulos.
- Encontrar dónde refactorizar: leer el Capítulo 3.
- Hacer refactoring de verdad: leer completos los cuatro primeros capítulos, luego hojear el catálogo para saber qué contiene, y leer en detalle cada refactorización cuando se vaya a aplicar; también leer los capítulos invitados, especialmente el 15.

## Building on the Foundations Laid by Others (Sobre los cimientos de otros)

Fowler reconoce una gran deuda con quienes desarrollaron el campo en la década previa. Ward Cunningham y Kent Beck fueron de los principales proponentes y lo usaron como parte central de su proceso; la colaboración con Kent le mostró la importancia del refactoring. Ralph Johnson lidera en la Universidad de Illinois en Urbana-Champaign un grupo notable por sus contribuciones prácticas a la tecnología de objetos. Bill Opdyke desarrolló el primer trabajo escrito detallado sobre refactoring en su tesis doctoral. John Brant y Don Roberts fueron más allá y escribieron una herramienta, el Refactoring Browser, para refactorizar programas Smalltalk.

## Acknowledgments (Agradecimientos)

Kent Beck fue la mayor ayuda: de una conversación suya sobre un artículo para el Smalltalk Report surgió la semilla del Capítulo 1 y el hábito de anotar refactorizaciones, además de aportar la idea de los "code smells". Kent Beck, John Brant, William Opdyke y Don Roberts escribieron o coescribieron capítulos; Rich Garzaniti y Ron Jeffries añadieron recuadros. Carter Shanklin y su equipo en Addison-Wesley reunieron un panel de revisores técnicos (entre ellos Ken Auer, Joshua Bloch, Ward Cunningham, Erich Gamma, Ralph Johnson, Doug Lea y otros). Ward y Ron sugirieron el estilo side-by-side del Capítulo 1 y Joshua Kerievsky la idea de los "code sketches" del catálogo. El refactoring se probó en producción en el sistema Chrysler Comprehensive Compensation (C3), cuyo equipo cita extensamente. Cierra agradeciendo a su esposa Cindy. Firma: Martin Fowler, Melrose, Massachusetts.

## Ideas clave

- Refactoring cambia la estructura interna del código sin alterar su comportamiento externo (PDF p. 9).
- Es una forma disciplinada de limpiar código que minimiza el riesgo de introducir errores.
- El diseño deja de ocurrir todo por adelantado y pasa a suceder de forma continua durante el desarrollo.
- Cada refactorización es un paso pequeño y simple; su efecto acumulado mejora radicalmente el diseño.
- La anécdota del proyecto fallido muestra el coste real de no limpiar el código; Kent Beck lo relanzó con refactorización continua.
- El libro combina un ejemplo inicial (cap. 1), principios (cap. 2), malos olores (cap. 3), pruebas (cap. 4) y un catálogo de referencia (caps. 5-12).
- Los ejemplos están en Java y evitan rasgos complejos; no cubren programación concurrente ni distribuida.
- El campo se cimienta en el trabajo de Cunningham, Beck, Johnson, Opdyke, Brant y Roberts, con probado impacto en el sistema C3.
