# Dive Into Design Patterns — Alexander Shvets (Refactoring.Guru, 2021)
## Capítulo 31 — Observer (Observador)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF (que presenta palabras pegadas por la justificación) y las citas usan la página del PDF.

## Lo que necesitas saber

Observer es un patrón de diseño de comportamiento que permite definir un mecanismo de suscripción para notificar a varios objetos sobre cualquier evento que le suceda al objeto que están observando (PDF p. 359). También se le conoce como Observador, Publicación-Suscripción, Modelo-patrón, Event-Subscriber o Listener.

El patrón resuelve el conflicto entre dos extremos indeseables: o el objeto interesado sondea continuamente a otro para detectar cambios (desperdiciando su tiempo), o el objeto observado notifica indiscriminadamente a todos (desperdiciando recursos y molestando a quienes no les interesa). La solución es un mecanismo de suscripción por el que solo los objetos interesados reciben notificaciones.

Sales sabiendo cómo separar la funcionalidad central (el notificador) de los objetos que reaccionan a sus cambios (los suscriptores), comunicándolos únicamente a través de una interfaz común para evitar el acoplamiento a clases concretas, y cómo construir y modificar esas relaciones dinámicamente durante el tiempo de ejecución.

## El ejemplo que recorre el capítulo

El problema se plantea con un objeto Cliente y un objeto Tienda (PDF p. 360). El cliente quiere un producto concreto (un nuevo modelo de iPhone) que llegará pronto a la tienda. Si el cliente visita la tienda cada día, la mayoría de los viajes serán en vano mientras el producto está en camino. Si, en cambio, la tienda envía cientos de correos a todos los clientes ante cada novedad, se parece a spam y molesta a quienes no están interesados. El patrón Observer resuelve el conflicto permitiendo que solo los clientes interesados se suscriban a las notificaciones de la tienda.

## Problema y solución

El objeto que tiene un estado interesante suele llamarse sujeto, pero como va a notificar a otros objetos sus cambios de estado, el libro lo llama notificador (también publicador). Los objetos que quieren conocer esos cambios son los suscriptores (PDF p. 361).

El patrón sugiere añadir un mecanismo de suscripción a la clase notificadora que consiste en: 1) un campo matriz para almacenar una lista de referencias a objetos suscriptores y 2) varios métodos públicos para añadir y eliminar suscriptores de esa lista (PDF p. 361). Cuando le sucede un evento importante, el notificador recorre sus suscriptores y llama al método de notificación de cada uno.

Como puede haber decenas de clases suscriptoras —algunas desconocidas de antemano si otros usan tu notificador—, es fundamental que todas implementen la misma interfaz y que el notificador solo se comunique a través de ella (PDF p. 362). Esa interfaz declara el método de notificación junto con parámetros para pasar información contextual. Si hay varios tipos de notificadores, se puede hacer que todos sigan una interfaz común de suscripción para que los suscriptores los observen sin acoplarse a sus clases concretas (PDF p. 363).

## Analogía en el mundo real

Suscripciones a revistas y periódicos (PDF p. 363). Al suscribirte, ya no vas a la tienda a comprobar si salió el siguiente número: el notificador envía los nuevos números directamente a tu buzón tras la publicación. El notificador mantiene la lista de suscriptores y sabe qué revistas les interesan, y los suscriptores pueden abandonar la lista cuando quieran dejar de recibirlos.

## Estructura

1. El **Notificador** envía eventos de interés, que ocurren cuando cambia su estado o ejecuta ciertos comportamientos. Contiene la infraestructura de suscripción para que nuevos y antiguos suscriptores se unan o abandonen la lista.
2. Cuando sucede un nuevo evento, el notificador recorre la lista de suscripción e invoca el método de notificación declarado en la interfaz suscriptora de cada objeto.
3. La **interfaz Suscriptora** declara la interfaz de notificación; en la mayoría de los casos consiste en un único método `actualizar`, que puede recibir parámetros con detalles del evento (PDF p. 364-365).
4. Los **Suscriptores Concretos** realizan acciones en respuesta a las notificaciones. Todos implementan la misma interfaz para que el notificador no se acople a clases concretas.
5. Los suscriptores suelen necesitar información contextual, por lo que el notificador la pasa como argumento del método de notificación; incluso puede pasarse a sí mismo para que el suscriptor extraiga lo que necesite.
6. El **Cliente** crea objetos notificador y suscriptor por separado y registra los suscriptores en el notificador.

## Pseudocódigo

El ejemplo muestra un editor de texto que notifica a objetos tipo servicio los cambios de estado (PDF p. 365-369). La clase editora no mantiene la lista de suscripción por sí misma: delega ese trabajo a un objeto ayudante dedicado (`EventManager`), que puede actualizarse para servir como despachador centralizado de eventos.

```
// Clase notificadora base con la gestión de suscripciones.
class EventManager is
    private field listeners: hash map of event types and listeners
    method subscribe(eventType, listener) is
        listeners.add(eventType, listener)
    method unsubscribe(eventType, listener) is
        listeners.remove(eventType, listener)
    method notify(eventType, data) is
        foreach (listener in listeners.of(eventType)) do
            listener.update(data)
```

El `Editor` tiene un campo público `events: EventManager` y, en sus métodos de negocio (`openFile`, `saveFile`), invoca `events.notify(...)`. La interfaz `EventListener` declara `update(filename)`. Los suscriptores concretos `LoggingListener` (escribe en un log) y `EmailAlertsListener` (envía correo) la implementan. La clase `Application` configura notificadores y suscriptores en tiempo de ejecución y suscribe cada listener a los eventos que le interesan (`"open"`, `"save"`). Añadir nuevos suscriptores no requiere cambios en las clases notificadoras existentes, siempre que trabajen con la misma interfaz.

El libro nota que la clase notificadora concreta puede derivar de la base, pero a menudo eso no es posible (ya es subclase de otra cosa), y entonces se usa composición. Si el lenguaje soporta tipos funcionales, se puede sustituir toda la jerarquía suscriptora por un grupo de funciones.

## Aplicabilidad

- Cuando los cambios en el estado de un objeto puedan necesitar cambiar otros objetos y el grupo de objetos sea desconocido de antemano o cambie dinámicamente (PDF p. 370). Es común en clases de GUI: por ejemplo, permitir que el cliente cuelgue su código en tus botones para que se active al pulsarlos.
- Cuando algunos objetos deban observar a otros solo durante un tiempo limitado o en casos específicos, ya que la lista de suscripción es dinámica y los suscriptores pueden unirse o salir cuando lo deseen.

## Cómo implementarlo

1. Divide la lógica de negocio en dos partes: la funcionalidad central será el notificador y el resto, las clases suscriptoras (PDF p. 371).
2. Declara la interfaz suscriptora con al menos un método `actualizar`.
3. Declara la interfaz notificadora con métodos para añadir y eliminar suscriptores, trabajando con ellos solo a través de la interfaz suscriptora.
4. Decide dónde colocar la lista y los métodos de suscripción: normalmente en una clase abstracta derivada de la interfaz notificadora; si aplicas el patrón a una jerarquía existente, usa composición colocando la lógica de suscripción en un objeto separado.
5. Crea las clases notificadoras concretas, que notifican a todos sus suscriptores ante cada evento importante.
6. Implementa los métodos de notificación en las suscriptoras concretas. El contexto puede pasarse como argumento; alternativamente el suscriptor lo extrae de la propia notificación (el notificador se pasa a sí mismo). La opción menos flexible es vincular notificador y suscriptor de forma permanente en el constructor.
7. El cliente crea los suscriptores y los registra con los notificadores adecuados.

## Pros y contras

- **Pro:** respeta el principio de abierto/cerrado: puedes introducir nuevas clases suscriptoras sin cambiar el código de la notificadora (y viceversa si hay interfaz notificadora).
- **Pro:** puedes establecer relaciones entre objetos durante el tiempo de ejecución.
- **Contra:** los suscriptores son notificados en un orden aleatorio.

## Relaciones con otros patrones

Chain of Responsibility, Command, Mediator y Observer abordan distintas formas de conectar emisores y receptores de solicitudes (PDF p. 373): Chain of Responsibility pasa una solicitud secuencialmente por una cadena dinámica hasta que alguien la gestiona; Command establece conexiones unidireccionales entre emisor y receptor; Mediator elimina las conexiones directas forzando la comunicación a través de un mediador; Observer permite a los receptores suscribirse o darse de baja dinámicamente.

La diferencia entre Mediator y Observer suele ser difusa. La meta de Mediator es eliminar dependencias mutuas entre componentes haciéndolos depender de un único mediador; la de Observer es establecer conexiones dinámicas de un solo sentido donde unos objetos son subordinados de otros (PDF p. 373-374). Existe una implementación popular de Mediator basada en Observer, donde el mediador es el notificador y los componentes son suscriptores; así ambos se parecen mucho. Pero Mediator puede implementarse de otras formas (vinculando permanentemente los componentes al mediador), y si todos los componentes se vuelven notificadores con conexiones dinámicas entre sí, se tiene un grupo distribuido de observadores sin mediador centralizado.

## Ideas clave

- Observer define un mecanismo de suscripción: un notificador avisa a sus suscriptores de los eventos que le suceden.
- El notificador y los suscriptores se comunican solo a través de una interfaz común, evitando el acoplamiento a clases concretas.
- La lista de suscripción es dinámica: los objetos se unen o salen en tiempo de ejecución.
- El método de notificación suele ser un único `actualizar`, al que se pasa el contexto del evento como argumento.
- La lógica de suscripción puede ir en una clase base por herencia o en un objeto separado por composición (útil con jerarquías existentes).
- Cumple el principio de abierto/cerrado; su contrapartida es que el orden de notificación es aleatorio.
- Mediator y Observer se parecen cuando el mediador se implementa como notificador, pero persiguen metas distintas.
