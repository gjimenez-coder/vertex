# Singleton (Singleton) — Estudio

## Tarjetas de repaso

P: ¿Qué es el patrón Singleton y a qué familia pertenece? / R: Es un patrón de diseño creacional que asegura que una clase tenga una única instancia y proporciona un punto de acceso global a esa instancia. También se le llama "Instancia única".

P: ¿Qué dos problemas resuelve Singleton a la vez? / R: Garantizar que una clase tenga una sola instancia y ofrecer un punto de acceso global a esa instancia.

P: ¿Por qué Singleton vulnera, de entrada, el Principio de responsabilidad única? / R: Porque resuelve dos problemas a la vez en una misma clase.

P: ¿Cuáles son los dos pasos comunes a todas las implementaciones de Singleton? / R: Hacer privado el constructor por defecto para impedir el uso de `new`, y crear un método de creación estático que invoca al constructor privado, guarda el objeto en un campo estático y devuelve el objeto en caché en las llamadas siguientes.

P: ¿Qué hace el método `obtenerInstancia` (`getInstance`)? / R: Almacena en caché el primer objeto creado y lo devuelve en todas las llamadas siguientes, siendo la única manera de obtener el objeto.

P: ¿Qué es la inicialización diferida en Singleton? / R: Crear el objeto en la primera llamada al método de creación y devolver el objeto almacenado en las siguientes; la instancia solo se inicializa cuando se requiere por primera vez.

P: ¿Por qué Singleton es más seguro que una variable global? / R: Permite acceder al objeto desde cualquier parte del programa y, a la vez, evita que otro código sobrescriba la instancia en caché; nada salvo la propia clase puede sustituirla.

P: ¿Qué tratamiento especial exige Singleton en entornos multihilo? / R: Requiere bloqueo de hilo (acquireThreadLock) con una segunda comprobación de la instancia para evitar que varios hilos creen el objeto más de una vez.

P: ¿Cuáles son los pros del patrón Singleton? / R: Certeza de que una clase tiene una única instancia, punto de acceso global a dicha instancia, e inicialización de la instancia solo cuando se requiere por primera vez.

P: ¿Cuáles son los contras del patrón Singleton? / R: Vulnera el Principio de responsabilidad única, puede enmascarar un mal diseño (componentes que saben demasiado entre sí), requiere tratamiento especial en multihilo y dificulta las pruebas unitarias del código cliente.

P: ¿Por qué Singleton dificulta las pruebas unitarias? / R: Muchos frameworks dependen de la herencia para crear mock objects, pero el constructor es privado y en la mayoría de lenguajes no se pueden sobrescribir métodos estáticos, así que hay que idear una forma original de simular el Singleton.

P: ¿En qué se diferencian Singleton y Flyweight? / R: Solo debe existir una instancia de Singleton (Flyweight puede tener varias con distintos estados intrínsecos), y el Singleton puede ser mutable mientras que los flyweight son inmutables.

P: ¿Qué relación tienen Facade, Abstract Factory, Builder y Prototype con Singleton? / R: Una Facade suele poder transformarse en Singleton porque basta un único objeto fachada; Abstract Factory, Builder y Prototype pueden implementarse como Singletons.

## Preguntas de autoevaluación

P: ¿Por qué no se puede implementar el comportamiento de "una sola instancia" con un constructor normal? / R: Porque por diseño una llamada al constructor siempre devuelve un objeto nuevo. (sección "Problema")

P: ¿Cuál es el ejemplo hilo conductor del capítulo y cómo se obtiene su objeto? / R: Una clase de conexión a base de datos sin constructor público; la única manera de obtener su objeto es invocar `obtenerInstancia` (`getInstance`). (sección "El ejemplo que recorre el capítulo")

P: ¿Qué analogía del mundo real usa el capítulo para explicar Singleton? / R: El gobierno: un país solo tiene un gobierno oficial, y el título "Gobierno de X" actúa como punto de acceso global independientemente de quién lo integre. (sección "El ejemplo que recorre el capítulo")

P: En el pseudocódigo, ¿por qué `bar` contiene el mismo objeto que `foo`? / R: Porque ambas variables se obtienen con `Database.getInstance()`, que devuelve siempre la misma instancia en caché. (sección "Pseudocódigo")

P: ¿Cuándo conviene usar Singleton según la aplicabilidad? / R: Cuando una clase deba tener una sola instancia disponible para todos los clientes, y cuando se necesite un control más estricto que el de las variables globales. (sección "Aplicabilidad")

P: ¿Cómo se podría permitir cierto número de instancias en lugar de solo una? / R: Ajustando la limitación cambiando solo el cuerpo de `getInstance`. (sección "Aplicabilidad")

P: ¿Para qué sirve que toda consulta pase por el método `query` del ejemplo? / R: Es el lugar donde se puede aplicar throttling o caché. (sección "Pseudocódigo")

## Checklist

Puntos a dominar:

- Reconocer Singleton como patrón creacional de instancia única con punto de acceso global.
- Explicar por qué vulnera el Principio de responsabilidad única al resolver dos problemas.
- Implementar los pasos: campo estático privado, método de creación estático público, inicialización diferida, constructor privado y sustitución de llamadas directas al constructor por el método estático.
- Justificar el bloqueo de hilo con doble comprobación en entornos multihilo.
- Argumentar las ventajas frente a variables globales y los contras (acoplamiento oculto, dificultad para pruebas unitarias).
- Distinguir Singleton de Flyweight y relacionarlo con Facade, Abstract Factory, Builder y Prototype.
