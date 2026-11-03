# Dive Into Design Patterns — Alexander Shvets (Refactoring.Guru, 2021)
## Capítulo 29 — Mediator (Mediador)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF (que contiene palabras pegadas por la justificación) y las citas usan la página del PDF.

## Lo que necesitas saber

Mediator es un patrón de diseño de comportamiento que permite reducir las dependencias caóticas entre objetos. El patrón restringe las comunicaciones directas entre los objetos, forzándolos a colaborar únicamente a través de un objeto mediador (PDF p. 327). También se le conoce como Mediador, Intermediary o Controller.

La tesis central es que, cuando muchos objetos se conocen y se llaman entre sí directamente, surge una red de relaciones difícil de mantener y reutilizar. El patrón propone cortar esa comunicación directa y encaminarla a través de un único intermediario. De este modo, cada componente depende solo de la clase mediadora en lugar de estar acoplado a decenas de sus colegas.

Sales sabiendo cómo identificar grupos de clases fuertemente acopladas, cómo extraer sus relaciones a un mediador mediante una interfaz común de notificación, y qué ventajas (menor acoplamiento, reutilización) y qué riesgo (que el mediador se convierta en un objeto todopoderoso) conlleva.

## El ejemplo que recorre el capítulo

El caso hilo conductor es un diálogo para crear y editar perfiles de cliente, compuesto por varios controles de formulario: campos de texto, casillas, botones, etc. (PDF p. 328). Algunos elementos interactúan: al marcar la casilla "tengo un perro" aparece un campo de texto oculto para el nombre del perro; el botón de envío debe validar todos los campos antes de guardar.

El problema es que, al implementar esa lógica directamente en el código de cada elemento, las clases se vuelven difíciles de reutilizar en otros formularios: la casilla queda acoplada al campo del perro, así que o reutilizas todas las clases del formulario o ninguna (PDF p. 329).

## Solución

El patrón sugiere detener toda comunicación directa entre los componentes que quieres hacer independientes; en su lugar colaboran indirectamente invocando un objeto mediador que redirige las llamadas a los componentes adecuados. Así los componentes dependen de una sola clase mediadora (PDF p. 329).

En el ejemplo, la propia clase de diálogo actúa como mediadora: ya conoce a todos sus subelementos, por lo que no hace falta introducir nuevas dependencias (PDF p. 330). El cambio más significativo lo sufren los elementos del formulario: el botón de envío ya no valida todos los campos, sino que solo notifica el clic al diálogo, y es el diálogo quien realiza las validaciones o delega la tarea.

Se puede ir más lejos extrayendo una interfaz común para todos los tipos de diálogo que declare el método de notificación. Así el botón funciona con cualquier diálogo que implemente esa interfaz (PDF p. 331). El patrón encapsula una red compleja de relaciones dentro de un único objeto mediador: cuantas menos dependencias tiene una clase, más fácil es modificarla, extenderla o reutilizarla.

## Analogía en el mundo real

Los pilotos de aviones no hablan directamente entre sí para decidir quién aterriza primero; toda la comunicación pasa por la torre de control (PDF p. 330). Hablan con un controlador de tráfico aéreo. Sin él, cada piloto tendría que conocer todos los aviones próximos y negociar prioridades con decenas de colegas, disparando las estadísticas de accidentes. La torre no controla el vuelo completo; solo impone límites en el área de la terminal, donde el número de actores es difícil de gestionar para un piloto (PDF p. 332).

## Estructura

1. Los **Componentes** son clases con cierta lógica de negocio. Cada uno tiene una referencia a una interfaz mediadora, declarada con su tipo; no conoce la clase concreta, por lo que se puede reutilizar vinculándolo a otra mediadora (PDF p. 333).
2. La **interfaz Mediadora** declara métodos de comunicación con los componentes, normalmente un único método de notificación. Los componentes pueden pasar cualquier contexto como argumento, pero sin que haya acoplamiento entre el receptor y el emisor.
3. Los **Mediadores Concretos** encapsulan las relaciones entre componentes; suelen mantener referencias a todos los que gestionan y a veces gestionan su ciclo de vida.
4. Los componentes no deben conocer a otros componentes: si les sucede algo importante, solo notifican a la interfaz mediadora. Al recibir la notificación, la mediadora identifica al emisor y decide qué componente activar.

Desde la perspectiva de un componente, todo parece una caja negra: el emisor no sabe quién gestionará su solicitud y el receptor no sabe quién la envió (PDF p. 333).

## Pseudocódigo

El ejemplo elimina dependencias mutuas entre varias clases UI: botones, casillas y etiquetas de texto. El diálogo de autenticación actúa como mediador: sabe cómo deben colaborar los elementos concretos y facilita su comunicación indirecta; al recibir una notificación decide qué elemento debe encargarse del evento y redirige la llamada (PDF p. 335).

```
// La interfaz mediadora declara un método que usan los
// componentes para notificar al mediador sobre eventos.
interface Mediator is
    method notify(sender: Component, event: string)

class AuthenticationDialog implements Mediator is
    private field title: string
    private field loginOrRegisterChkBx: Checkbox
    private field loginUsername, loginPassword: Textbox
    private field registrationUsername, registrationPassword,
                  registrationEmail: Textbox
    private field okBtn, cancelBtn: Button

    constructor AuthenticationDialog() is
        // Crea los componentes y les pasa el mediador actual.

    method notify(sender, event) is
        if (sender == loginOrRegisterChkBx and event == "check")
            if (loginOrRegisterChkBx.checked)
                title = "Log in"
                // Muestra el formulario de inicio de sesión y oculta el de registro.
            else
                title = "Register"
                // Muestra el formulario de registro y oculta el de inicio de sesión.
        if (sender == okBtn && event == "click")
            // Valida credenciales o crea la cuenta según el modo.

// Los componentes se comunican con el mediador por la interfaz.
class Component is
    field dialog: Mediator
    constructor Component(dialog) is
        this.dialog = dialog
    method click() is
        dialog.notify(this, "click")
    method keypress() is
        dialog.notify(this, "keypress")

class Button extends Component is // ...
class Textbox extends Component is // ...
class Checkbox extends Component is
    method check() is
        dialog.notify(this, "check")
```

Los componentes concretos no hablan entre sí: su único canal es el envío de notificaciones al mediador (PDF p. 337).

## Aplicabilidad

- Cuando resulte difícil cambiar algunas clases porque están fuertemente acopladas a un puñado de otras: el patrón extrae esas relaciones a una clase separada, aislando los cambios (PDF p. 338).
- Cuando no puedas reutilizar un componente en otro programa porque depende demasiado de otros; basta con darle una nueva clase mediadora.
- Cuando te encuentres creando cientos de subclases de componente solo para reutilizar un comportamiento básico en varios contextos: defines nuevas colaboraciones introduciendo nuevas mediadoras, sin cambiar los componentes.

## Cómo implementarlo

1. Identifica un grupo de clases fuertemente acopladas que se beneficiarían de ser más independientes (PDF p. 339).
2. Declara la interfaz mediadora y el protocolo de comunicación; suele bastar un único método para recibir notificaciones.
3. Implementa la clase concreta mediadora, que se beneficia de almacenar referencias a todos los componentes que gestiona.
4. Opcionalmente, haz la interfaz mediadora responsable de crear y destruir componentes; así puede parecerse a una fábrica o una fachada.
5. Los componentes almacenan una referencia al mediador, establecida normalmente en el constructor (PDF p. 340).
6. Cambia el código de los componentes para que invoquen el método de notificación del mediador en lugar de los métodos de otros componentes, y mueve ese código a la mediadora.

## Ideas clave

- Mediator reduce las dependencias caóticas forzando la comunicación indirecta a través de un objeto mediador.
- Los componentes solo conocen la interfaz mediadora, no a otros componentes: todo parece una caja negra.
- Suele bastar un único método `notify(sender, event)` para toda la comunicación.
- En la UI, la clase de diálogo es candidata natural a mediadora porque ya conoce a sus subelementos.
- Favorece el Principio de responsabilidad única (comunicaciones en un solo sitio) y el de abierto/cerrado (nuevas mediadoras sin tocar componentes).
- Reduce el acoplamiento y facilita la reutilización de componentes individuales.
- Riesgo principal: con el tiempo el mediador puede evolucionar hacia un objeto todopoderoso (PDF p. 339).
- Analogía: la torre de control de tráfico aéreo que coordina a los pilotos sin que estos hablen entre sí.
