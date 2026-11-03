# Observer (Observador) — Estudio

## Tarjetas de repaso

P: ¿Qué tipo de patrón es Observer y qué permite definir?
R: Es un patrón de comportamiento que permite definir un mecanismo de suscripción para notificar a varios objetos sobre cualquier evento que le suceda al objeto que observan.

P: ¿Qué otros nombres recibe Observer?
R: Observador, Publicación-Suscripción, Modelo-patrón, Event-Subscriber o Listener.

P: ¿Qué dos extremos indeseables resuelve el patrón?
R: Que el objeto interesado sondee continuamente a otro para detectar cambios (desperdicia su tiempo) o que el objeto observado notifique indiscriminadamente a todos (desperdicia recursos y molesta a los no interesados).

P: ¿Cómo se llaman los dos roles principales del patrón?
R: El notificador (o publicador/sujeto), que tiene el estado interesante y notifica sus cambios, y los suscriptores, que quieren conocer esos cambios.

P: ¿Qué dos elementos componen el mecanismo de suscripción que se añade a la clase notificadora?
R: Un campo matriz para almacenar referencias a objetos suscriptores y varios métodos públicos para añadir y eliminar suscriptores de esa lista.

P: ¿Por qué todos los suscriptores deben implementar la misma interfaz?
R: Porque puede haber decenas de clases suscriptoras, algunas desconocidas de antemano, y el notificador debe comunicarse solo a través de esa interfaz para no acoplarse a clases concretas.

P: ¿En qué consiste normalmente la interfaz suscriptora?
R: En un único método `actualizar`, que puede recibir parámetros con detalles del evento.

P: ¿Cómo recibe el suscriptor la información contextual del evento?
R: El notificador la pasa como argumento del método de notificación; incluso puede pasarse a sí mismo para que el suscriptor extraiga lo que necesite.

P: ¿Cuáles son las dos formas de colocar la lista y los métodos de suscripción?
R: En una clase abstracta/base derivada de la interfaz notificadora (herencia) o en un objeto separado (composición), útil al aplicar el patrón a una jerarquía existente.

P: En el pseudocódigo, ¿qué objeto gestiona la lista de suscripción en lugar del editor de texto?
R: Un objeto ayudante dedicado llamado `EventManager`, al que el editor delega esa tarea y que puede servir como despachador centralizado de eventos.

P: ¿Qué principio de diseño respeta Observer?
R: El principio de abierto/cerrado: pueden introducirse nuevas clases suscriptoras sin cambiar el código de la notificadora (y viceversa si hay interfaz notificadora).

P: ¿Cuál es la principal contrapartida (contra) del patrón?
R: Los suscriptores son notificados en un orden aleatorio.

P: ¿Cuándo es adecuado aplicar Observer según su aplicabilidad?
R: Cuando los cambios en el estado de un objeto puedan requerir cambiar otros objetos cuyo grupo es desconocido de antemano o cambia dinámicamente, o cuando algunos objetos deban observar a otros solo durante un tiempo limitado.

P: ¿Cuál es la diferencia de meta entre Mediator y Observer?
R: Mediator busca eliminar dependencias mutuas haciendo que los componentes dependan de un único mediador; Observer busca establecer conexiones dinámicas de un solo sentido donde unos objetos son subordinados de otros.

## Preguntas de autoevaluación

P: Explica el conflicto que ilustra el ejemplo del Cliente y la Tienda.
R: Si el cliente visita la tienda cada día esperando el producto, la mayoría de viajes serán en vano; si la tienda envía correos a todos ante cada novedad, es como spam y molesta a los no interesados. Observer permite que solo los clientes interesados se suscriban. (Sección: "El ejemplo que recorre el capítulo")

P: ¿Qué hace el notificador cuando le sucede un evento importante?
R: Recorre su lista de suscriptores e invoca el método de notificación (declarado en la interfaz suscriptora) de cada objeto. (Secciones: "Problema y solución" y "Estructura")

P: ¿Cómo ilustra la analogía de las revistas el funcionamiento del patrón?
R: Al suscribirte dejas de ir a la tienda a comprobar si salió el número; el notificador envía los nuevos números a tu buzón tras publicarlos, mantiene la lista de suscriptores y permite abandonarla cuando se desee. (Sección: "Analogía en el mundo real")

P: ¿Qué papel cumple la clase `Application`/cliente en el pseudocódigo?
R: Crea los objetos notificador y suscriptor por separado, los configura en tiempo de ejecución y suscribe cada listener a los eventos que le interesan (como "open" y "save"). (Secciones: "Pseudocódigo" y "Estructura")

P: ¿Por qué a veces se usa composición en lugar de herencia para la lógica de suscripción?
R: Porque la clase notificadora concreta a menudo ya es subclase de otra cosa y no puede derivar de la base; entonces se coloca la lógica de suscripción en un objeto separado. (Secciones: "Pseudocódigo" y "Cómo implementarlo")

P: ¿Por qué añadir nuevos suscriptores no exige cambiar las clases notificadoras existentes?
R: Porque notificador y suscriptores trabajan con la misma interfaz común, de modo que basta implementar esa interfaz; esto cumple el principio de abierto/cerrado. (Secciones: "Pseudocódigo" y "Pros y contras")

P: ¿Por qué suele ser difusa la distinción entre Mediator y Observer?
R: Porque existe una implementación popular de Mediator basada en Observer, donde el mediador es el notificador y los componentes son suscriptores, lo que hace que ambos se parezcan mucho. (Sección: "Relaciones con otros patrones")

## Puntos a dominar

- Identificar Observer como patrón de comportamiento y su mecanismo de suscripción notificador–suscriptor.
- Reconocer los dos extremos indeseables que resuelve (sondeo continuo vs. notificación indiscriminada).
- Distinguir los roles: notificador (publicador/sujeto) y suscriptores, y el flujo de notificación.
- Entender por qué la comunicación debe pasar solo por la interfaz común para evitar acoplamiento a clases concretas.
- Comprender la interfaz suscriptora con el método `actualizar` y cómo se pasa el contexto del evento.
- Diferenciar las dos ubicaciones de la lógica de suscripción: herencia (clase base) vs. composición (objeto separado como `EventManager`).
- Relacionar el patrón con el principio de abierto/cerrado y su contra (orden de notificación aleatorio).
- Diferenciar Observer de Chain of Responsibility, Command y Mediator según cómo conectan emisores y receptores.
