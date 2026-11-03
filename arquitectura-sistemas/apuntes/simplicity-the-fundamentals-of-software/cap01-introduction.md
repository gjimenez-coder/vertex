# Code Simplicity: The Fundamentals of Software — Max Kanat-Alexander (O'Reilly Media, 2012)
## Capítulo 1 — Introduction (Introducción)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas usan la página del PDF.

## Lo que necesitas saber

El capítulo abre planteando una paradoja: los computadores aportan un valor enorme porque hacen mucho trabajo muy rápido con menos personas, pero fallan constantemente, hasta el punto de que la mayoría de la gente vive un fallo o mal funcionamiento al menos una vez al día. La tesis central es que, en el software, los fallos tienen una única causa de raíz: la mala programación, y que la mala programación gira en torno a un solo concepto, la complejidad.

De aquí se deriva la idea que vertebra todo el libro: programar es, en esencia, el acto de reducir la complejidad a simplicidad. Un programa es tan complejo que ninguna persona puede comprenderlo entero; por eso sus piezas complejas deben organizarse de forma simple, para que un programador pueda trabajar sin necesitar habilidades mentales sobrehumanas. Ese es el arte y el talento de programar.

Sales sabiendo qué significa realmente un "buen" y un "mal" programador en estos términos, por qué el código desorganizado es mucho más dañino que una lista de la compra desordenada, y por qué el foco del libro será la calidad del código. También queda clara la motivación última: el código importa solo porque buscamos un mejor resultado.

## El ejemplo que recorre el capítulo

El hilo conductor es la analogía del ingeniero que, necesitando clavar un clavo en el suelo, inventa un artefacto con poleas, cuerdas y un imán grande. Resulta ridículo. Kanat-Alexander traslada esa imagen al software: ante una tarea difícil (por ejemplo, "código que comunique dos computadores cualesquiera por cualquier medio imaginable"), muchos programadores producen el equivalente a cuerdas, poleas y un imán: una solución que funciona pero que apenas es comprensible para los demás. No son irracionales ni están mal; simplemente, con poco tiempo, hacen lo que pueden y entregan algo que "funciona". El problema es que pasan ese artefacto a otro programador, que lo usa como parte del suyo y añade más complejidad. Cuantos más eslabones no reducen la complejidad, más incomprensible se vuelve el programa.

## What's Wrong with Computers? (¿Qué va mal con los computadores?)

- Para el software, la causa única de los fallos es la mala programación; la investigación muestra que la raíz está siempre en la propia programación, no en la gestión ni en los clientes.
- "Mala programación" es un término ambiguo; los programadores suelen ser gente inteligente y racional. Todo se reduce a la complejidad.
- Un computador es quizá el dispositivo más complejo que se fabrica hoy: miles de millones de cálculos por segundo y cientos de millones de piezas electrónicas que deben funcionar correctamente.
- Un programa es igual de complejo. Microsoft Windows 2000, al escribirse, fue uno de los programas más grandes jamás creados, con alrededor de 30 millones de líneas de código, comparable a escribir un libro de 200.000.000 de palabras (más de cinco veces el tamaño de la Encyclopedia Britannica).
- La complejidad del software desconcierta porque es abstracta: cuando se rompe, no hay nada físico que abrir y mirar por dentro. Nadie comprende por completo cómo funciona todo el código de un programa medio, y cuanto más grande, más cierto es.
- Un "mal programador" es simplemente alguien que no logra reducir la complejidad. A menudo ocurre porque cree estar reduciéndola para sí mismo (al escribir código que "funciona sin más") sin pensar en reducirla para otros programadores.
- A medida que un programa se acerca a la complejidad infinita, se vuelve imposible encontrar todos sus problemas. Los aviones a reacción cuestan millones o miles de millones porque son casi así de complejos y fueron depurados; pero el software suele costar al cliente unos $50–$100, y a ese precio nadie dedica los recursos para sacar todos los fallos.
- Un "buen programador" debe hacer todo lo posible por que lo que escribe sea lo más simple posible para otros programadores; crea cosas fáciles de entender, lo que facilita eliminar los bugs.

Malentendidos sobre la simplicidad que el autor corrige:

- Simplicidad no significa poco código ni evitar tecnologías avanzadas. A veces mucho código conduce a la simplicidad (más escritura y lectura, lo cual está bien), siempre que exista un documento breve que explique esa gran masa de código. Las tecnologías avanzadas suelen llevar a más simplicidad, aunque haya que aprenderlas primero.
- Escribir de forma simple parece tardar más que escribir rápido algo que "hace el trabajo", pero dedicar algo más de tiempo a código simple resulta ser más rápido que escribir mucho código deprisa y luego gastar tiempo intentando entenderlo. La historia de la industria lo ha demostrado: muchos grandes programas se estancaron porque añadir funciones a las bestias complejas en que se convirtieron tomaba demasiado tiempo.

## What Is a Program, Really? (¿Qué es realmente un programa?)

La frase "un programa de computador" tiene dos definiciones muy distintas:

1. Una secuencia de instrucciones dadas al computador.
2. Las acciones que toma el computador como resultado de recibir esas instrucciones.

La primera es lo que ve el programador al escribir; la segunda, lo que ve el usuario al usarlo. El programador dice "muestra un cerdo en la pantalla" (definición 1); el computador mueve mucha electricidad que hace aparecer el cerdo (definición 2). Ambos dirían que trabajan con "un programa", pero su experiencia es muy distinta: el programador maneja palabras y símbolos, el usuario solo ve el resultado final, las acciones. En última instancia, un programa es ambas cosas, y todo el propósito de escribir las instrucciones es provocar las acciones; sin las acciones no habría razón para escribir las instrucciones.

Analogía de la lista de la compra: una lista es un conjunto de instrucciones sobre qué comprar; escribirla sin ir nunca a la tienda sería inútil. Pero hay diferencias clave con el software:

- Una lista desorganizada solo ralentiza un poco la compra; el código desorganizado puede convertir el logro de los objetivos en un laberinto de dificultad.
- Las listas son cortas, simples y se tiran al terminar; los programas son grandes, complejos y a menudo se mantienen durante años o décadas.

Además, en ningún otro campo están tan estrechamente ligados un conjunto de instrucciones y su resultado como en el desarrollo de software. Una arquitecta escribe planos (instrucciones) que pasan por muchas personas durante mucho tiempo hasta convertirse en un edificio, resultado de todas esas interpretaciones. Al escribir código, en cambio, no hay nadie entre nosotros y el computador: el resultado es exactamente lo que dicen las instrucciones. La calidad del resultado depende de tres factores: la calidad de la máquina, la calidad de nuestras ideas y la calidad de nuestro código.

De esos tres, la calidad del código es hoy el mayor problema de los proyectos de software, y por eso la mayor parte del libro trata de mejorarla (se tocan las ideas y las máquinas solo en algunos puntos). Al hablar tanto de código es fácil olvidar que lo hacemos porque deseamos un mejor resultado: nada en el libro justifica un resultado pobre; nos centramos en mejorar el código porque es el problema más importante a resolver para mejorar el resultado. Lo que más se necesita, concluye, es una ciencia para mejorar la calidad del código.

## Ideas clave

- En el software, la causa única de los fallos es la mala programación, y su núcleo es la complejidad.
- Programar es el acto de reducir la complejidad a simplicidad; ese es el arte del oficio.
- Un "mal programador" no reduce la complejidad; un "buen programador" hace su código lo más simple posible para otros, facilitando eliminar bugs.
- Simplicidad no equivale a poco código ni a evitar tecnología avanzada; a veces más código o tecnología más avanzada producen más simplicidad.
- Escribir código simple parece más lento, pero resulta más rápido que escribir deprisa y luego pelear por entenderlo; la complejidad estanca la evolución de los programas.
- Un programa es a la vez las instrucciones que escribe el programador y las acciones que ejecuta el computador; el fin de las instrucciones es provocar las acciones.
- El código desorganizado es mucho más dañino que una lista de la compra desordenada, porque los programas son grandes y se mantienen durante años o décadas.
- La calidad del resultado depende de la máquina, las ideas y el código; el código es hoy el mayor problema, de ahí la necesidad de una ciencia para mejorar su calidad.
