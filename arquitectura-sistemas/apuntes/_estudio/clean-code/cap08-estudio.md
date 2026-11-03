# Boundaries (Límites) — Estudio

## Tarjetas de repaso

P: ¿Qué son los "límites" (*boundaries*) en este capítulo?
R: Los puntos de contacto donde integramos en nuestro sistema software que no controlamos: paquetes de terceros, código open source o subsistemas producidos por otros equipos.

P: ¿Cuál es la tesis central del capítulo?
R: Debemos aislar nuestro código de las particularidades del código ajeno; es mejor depender de algo que controlamos que de algo que no controlamos, no sea que acabe controlándonos.

P: ¿Qué tensión natural existe en los límites?
R: Los proveedores de una interfaz buscan amplia aplicabilidad para muchos entornos y audiencias, mientras que los usuarios quieren una interfaz enfocada a sus necesidades concretas.

P: ¿Por qué `java.util.Map` ilustra el riesgo de una interfaz de límite?
R: Es una interfaz muy amplia: cualquier receptor puede llamar a `clear()` y vaciarla, y no restringe de forma fiable los tipos almacenados, así que cualquier usuario decidido puede añadir elementos de cualquier tipo.

P: ¿Cuál es la forma más limpia de usar `Map` según el capítulo?
R: Encapsularla dentro de una clase (como `Sensors`), ocultando la interfaz del límite para que evolucione con poco impacto y quede ajustada a las necesidades de la aplicación.

P: ¿Cuál es el consejo real sobre `Map`? ¿Encapsular todo `Map`?
R: No; el consejo es no pasar `Map` (ni otra interfaz de límite) por el sistema: mantenerla dentro de una clase o familia cercana y evitar devolverla o aceptarla como argumento en APIs públicas.

P: ¿Qué beneficios aporta encapsular la interfaz externa?
R: Hace que evolucione con poco impacto, la ajusta a las necesidades, la hace más difícil de usar mal y permite a la clase imponer reglas de diseño y de negocio.

P: ¿Qué son los *learning tests* y quién acuñó el nombre?
R: Pruebas que exploran nuestra comprensión de una API externa llamándola como esperamos usarla, como experimentos controlados; el nombre lo acuñó Jim Newkirk.

P: ¿Por qué conviene escribir *learning tests* en vez de experimentar en el código de producción?
R: Aprender e integrar una librería a la vez es doblemente difícil; separar el aprendizaje evita largas sesiones de depuración sin saber si el fallo es nuestro o del tercero.

P: ¿Qué enseñó el ejemplo de log4j sobre `ConsoleAppender`?
R: Su constructor por defecto queda "unconfigured"; quitar `ConsoleAppender.SystemOut` sigue imprimiendo, pero quitar `PatternLayout` vuelve a fallar por falta de *output stream*.

P: ¿Por qué los *learning tests* "salen gratis o mejor"?
R: De todos modos había que aprender la API, y además tienen retorno positivo: al salir una nueva versión se ejecutan y detectan de inmediato diferencias de comportamiento incompatibles.

P: ¿Cómo se trabaja con código del otro lado que aún no existe?
R: Se define "la interfaz que desearías tener", bajo nuestro control, como la interfaz `Transmitter` con su método `transmit` que recibe una frecuencia y un *data stream*.

P: ¿Qué papel juega el patrón ADAPTER en los límites?
R: Puentea entre nuestra interfaz ideal y la API real cuando esta queda definida (p. ej. `TransmitterAdapter`), concentrando en un único lugar los cambios cuando la API evoluciona.

P: ¿Cómo favorece este diseño a las pruebas?
R: Crea una *seam* conveniente: con un `FakeTransmitter` se prueba `CommunicationsController`, y se pueden crear pruebas de límite una vez exista la API real.

P: ¿Qué caracteriza a un límite limpio?
R: Separación clara, pruebas que definen las expectativas y muy pocos lugares que referencien el detalle del tercero, envolviéndolo o usando un ADAPTER.

## Preguntas de autoevaluación

P: ¿Por qué pasar una instancia de `Map<Sensor>` por todo el sistema es problemático aunque los *generics* mejoren la legibilidad?
R: Porque sigue ofreciendo más capacidad de la necesaria y crea muchos lugares que arreglar si la interfaz de `Map` cambia, como ocurrió al añadirse *generics* en Java 5. (Sección "Using Third-Party Code")

P: ¿Qué responsabilidad carga el cliente al usar un `Map` sin *generics* y cómo lo alivian estos?
R: El cliente debe obtener un `Object` y castearlo repetidamente; los *generics* permiten obtener directamente el `Sensor` y mejoran la legibilidad. (Sección "Using Third-Party Code")

P: ¿Qué quedó codificado tras explorar log4j y para qué sirvió después?
R: El conocimiento adquirido quedó en un conjunto de pruebas unitarias simples (`LogTest.java`), que luego permitió encapsular la inicialización en una clase propia aislada del límite de log4j. (Sección "Learning log4j")

P: ¿Qué valor de mantenimiento aportan los *learning tests* ante una nueva versión del paquete de terceros?
R: Se ejecutan para detectar diferencias de comportamiento; si un cambio es incompatible con nuestras pruebas, lo sabremos de inmediato, lo que facilita la migración. (Sección "Learning Tests Are Better Than Free")

P: En el sistema de comunicaciones por radio, ¿cómo evitó el equipo quedar bloqueado por un "Transmitter" indefinido?
R: Empezaron a trabajar lejos de la parte desconocida y, al toparse con el límite, definieron su propia interfaz `Transmitter` con lo que deseaban obtener de ella. (Sección "Using Code That Does Not Yet Exist")

P: ¿Por qué es ventajoso definir "la interfaz que desearías tener"?
R: Porque está bajo nuestro control y mantiene el código cliente legible y enfocado. (Sección "Using Code That Does Not Yet Exist")

P: ¿Qué ocurre en los límites que obliga a un buen diseño y cómo debe responder este?
R: Ocurre sobre todo el cambio; un buen diseño lo acomoda sin grandes inversiones ni retrabajo, con separación clara y pruebas que definen expectativas. (Sección "Clean Boundaries")

## Puntos a dominar

- Identificar los límites del sistema: código de terceros, open source y subsistemas de otros equipos, y reconocer la tensión proveedor-usuario.
- Explicar por qué no debe pasarse una interfaz de límite como `Map` por todo el sistema y cómo encapsularla en una clase o familia de clases.
- Enumerar los beneficios de encapsular una interfaz externa: evolución con bajo impacto, interfaz ajustada, más difícil de usar mal y capaz de imponer reglas de negocio.
- Describir qué son los *learning tests*, su propósito (explorar la API con experimentos controlados) y por qué salen gratis o con retorno positivo.
- Aplicar la técnica de "la interfaz que desearías tener" cuando el código del otro lado aún no existe.
- Reconocer el patrón ADAPTER como puente entre la interfaz ideal y la API real, y su papel al concentrar cambios y crear *seams* para pruebas.
- Sostener el principio de depender de lo que controlas y limitar los lugares que conocen los detalles del tercero.
