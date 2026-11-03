# Mediator (Mediador) — Estudio

## Tarjetas de repaso

P: ¿Qué tipo de patrón es Mediator y qué permite? / R: Es un patrón de comportamiento que reduce las dependencias caóticas entre objetos restringiendo la comunicación directa y forzándolos a colaborar a través de un objeto mediador.

P: ¿Qué otros nombres recibe Mediator? / R: Mediador, Intermediary y Controller.

P: ¿Cuál es la tesis central del patrón? / R: Cortar la comunicación directa entre objetos fuertemente acoplados y encaminarla por un único intermediario, de modo que cada componente dependa solo de la clase mediadora.

P: En el ejemplo del diálogo de perfil, ¿qué problema surge al poner la lógica en cada elemento? / R: Las clases se vuelven difíciles de reutilizar: la casilla queda acoplada al campo del perro, así que o reutilizas todas las clases del formulario o ninguna.

P: ¿Quién actúa como mediador en el ejemplo del formulario y por qué? / R: La propia clase de diálogo, porque ya conoce a todos sus subelementos y no hace falta introducir nuevas dependencias.

P: ¿Qué cambio sufre el botón de envío al aplicar Mediator? / R: Deja de validar todos los campos y solo notifica el clic al diálogo, que realiza las validaciones o delega la tarea.

P: ¿Cuáles son los cuatro elementos de la estructura del patrón? / R: Los Componentes, la interfaz Mediadora, los Mediadores Concretos y la regla de que los componentes no conozcan a otros componentes, notificando solo a la interfaz mediadora.

P: ¿Qué conoce un componente sobre el mediador y qué ventaja aporta? / R: Conoce solo el tipo de la interfaz mediadora, no la clase concreta, por lo que puede reutilizarse vinculándolo a otra mediadora.

P: ¿Qué significa que para un componente todo sea una "caja negra"? / R: Que el emisor no sabe quién gestionará su solicitud y el receptor no sabe quién la envió.

P: ¿Cuántos métodos suele necesitar la comunicación en Mediator y cuál es su firma típica? / R: Normalmente basta un único método de notificación, como `notify(sender, event)`.

P: ¿Qué hace el mediador al recibir una notificación? / R: Identifica al emisor y decide qué componente debe activarse, redirigiendo la llamada al componente adecuado.

P: ¿Qué principios de diseño favorece Mediator? / R: El de responsabilidad única (las comunicaciones quedan en un solo sitio) y el de abierto/cerrado (nuevas mediadoras sin tocar los componentes).

P: ¿Cuál es el riesgo principal del patrón? / R: Que con el tiempo el mediador evolucione hacia un objeto todopoderoso.

P: ¿Qué analogía del mundo real ilustra el patrón? / R: La torre de control de tráfico aéreo: los pilotos no hablan entre sí, toda la comunicación pasa por el controlador, que impone límites en el área de la terminal.

## Preguntas de autoevaluación

P: ¿Por qué un grupo de clases fuertemente acopladas es difícil de mantener y reutilizar? / R: Porque forman una red de relaciones donde cada clase se conoce y se llama entre sí directamente; cambiar o reutilizar una obliga a arrastrar a las demás. (Sección "Lo que necesitas saber" y "El ejemplo que recorre el capítulo")

P: ¿Cómo logra el patrón que los componentes sean independientes sin eliminar su colaboración? / R: Detiene la comunicación directa y la hace indirecta a través de un mediador que redirige las llamadas, de modo que cada componente depende solo de la clase mediadora. (Sección "Solución")

P: ¿Qué se gana al extraer una interfaz común de notificación para los diálogos? / R: Que un componente como el botón funcione con cualquier diálogo que implemente esa interfaz, aumentando su reutilización. (Sección "Solución")

P: Según la analogía, ¿la torre de control gestiona todo el vuelo? / R: No; solo impone límites en el área de la terminal, donde el número de actores es difícil de gestionar para un piloto. (Sección "Analogía en el mundo real")

P: ¿En qué casos conviene aplicar Mediator? / R: Cuando sea difícil cambiar clases fuertemente acopladas, cuando no puedas reutilizar un componente por depender demasiado de otros, y cuando crees muchas subclases solo para reutilizar un comportamiento básico en varios contextos. (Sección "Aplicabilidad")

P: ¿Por qué la clase de diálogo es una mediadora natural en interfaces de usuario? / R: Porque ya conoce a todos sus subelementos, por lo que no introduce nuevas dependencias al asumir el rol de mediador. (Sección "Solución" y "Ideas clave")

P: ¿Qué relación tienen los componentes concretos entre sí en el pseudocódigo? / R: Ninguna directa: no hablan entre sí y su único canal es el envío de notificaciones al mediador. (Sección "Pseudocódigo")

## Puntos a dominar

- Reconocer un grupo de clases fuertemente acopladas que se beneficiarían de ser más independientes.
- Entender que la comunicación directa se sustituye por notificaciones a una interfaz mediadora.
- Saber declarar la interfaz mediadora y su protocolo, normalmente un único método de notificación.
- Comprender que el mediador concreto almacena referencias a los componentes y encapsula sus relaciones.
- Mover la lógica de coordinación desde los componentes hacia el mediador, dejando que estos solo notifiquen eventos.
- Tener presentes las ventajas (menor acoplamiento, reutilización, SRP y OCP) y el riesgo del mediador todopoderoso.
