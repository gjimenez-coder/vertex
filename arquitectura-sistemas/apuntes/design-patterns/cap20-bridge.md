# Dive Into Design Patterns — Alexander Shvets (Refactoring.Guru, 2021)
## Capítulo 20 — Bridge (Puente)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas usan la página del PDF.

## Lo que necesitas saber

Bridge es un patrón de diseño estructural que te permite dividir una clase grande, o un grupo de clases estrechamente relacionadas, en dos jerarquías separadas —abstracción e implementación— que pueden desarrollarse independientemente la una de la otra (PDF p. 176).

El patrón ataca la explosión combinatoria que aparece cuando una jerarquía de clases intenta crecer en dos dimensiones independientes a la vez. La idea central es pasar de la herencia a la composición del objeto: se extrae una de las dimensiones a una jerarquía de clases separada, de modo que las clases originales referencian un objeto de la nueva jerarquía en lugar de contener todo el estado y la funcionalidad dentro de una sola clase.

Sales sabiendo cómo reconocer dimensiones ortogonales en un diseño, cómo separar la capa de control de alto nivel (abstracción) de la capa que hace el trabajo real (implementación), y cómo vincularlas mediante una referencia que actúa de "puente".

## El ejemplo que recorre el capítulo

El problema se ilustra con una clase geométrica `Forma` con subclases `Círculo` y `Cuadrado`. Si se quiere incorporar colores (`Rojo`, `Azul`), surgen combinaciones como `CírculoAzul` y `CuadradoRojo`. El número de combinaciones crece en progresión geométrica: añadir un tipo de forma obliga a crear una subclase por cada color, y añadir un color obliga a crear una subclase por cada forma (PDF p. 177-178).

La solución extrae el color a su propia jerarquía (`Rojo`, `Azul`). La clase `Forma` obtiene un campo de referencia que apunta a un objeto de color y delega en él todo el trabajo relacionado con el color. Esa referencia actúa como puente entre `Forma` y `Color`; añadir nuevos colores ya no exige cambiar la jerarquía de forma, ni viceversa (PDF p. 179).

## Problema

El problema se presenta porque se intenta extender las clases en dos dimensiones independientes (por forma y por color), algo muy habitual en la herencia de clases. Cuanto más se avanza, peor: cada nueva variante en una dimensión multiplica las clases necesarias en la otra (PDF p. 178).

## Solución: abstracción e implementación

El libro de la GoF introduce los términos Abstracción e Implementación como parte de la definición del patrón; el autor advierte que suenan demasiado académicos y hacen parecer el patrón más complicado de lo que es (PDF p. 179).

- La **Abstracción** (también llamada interfaz) es una capa de control de alto nivel. No hace trabajo real por su cuenta, sino que delega en la capa de implementación.
- La **Implementación** (también llamada plataforma) hace el trabajo de bajo nivel.

No se trata de las interfaces o clases abstractas del lenguaje de programación; son cosas diferentes (PDF p. 180). En una aplicación real, la abstracción puede ser una interfaz gráfica de usuario (GUI) y la implementación el código del sistema operativo subyacente (API) al que la GUI llama. Así, la aplicación puede extenderse en dos direcciones independientes: varias GUI (clientes regulares, administradores) y varias API (Windows, Linux, macOS). Sin Bridge, esto degenera en un "plato gigante de espagueti" con cientos de condicionales conectando GUI con API (PDF p. 180-181).

Aplicando Bridge, la GUI es la abstracción y las API de los sistemas operativos la implementación. Las implementaciones son intercambiables mientras sigan una interfaz común, así que la misma GUI funciona con Windows y Linux; añadir soporte para otro sistema operativo solo requiere una subclase nueva en la jerarquía de implementación (PDF p. 182).

## Estructura

1. La **Abstracción** ofrece lógica de control de alto nivel y depende del objeto de implementación para el trabajo de bajo nivel.
2. La **Implementación** declara la interfaz común a todas las implementaciones concretas. La abstracción solo se comunica con ella a través de estos métodos; normalmente la abstracción define funcionalidades complejas basadas en operaciones primitivas declaradas por la implementación.
3. Las **Implementaciones Concretas** contienen código específico de plataforma.
4. Las **Abstracciones Refinadas** proporcionan variantes de lógica de control y trabajan con distintas implementaciones a través de la interfaz general.
5. El **Cliente** solo trabaja con la abstracción, pero debe vincular el objeto de abstracción con uno de implementación (PDF p. 183-184).

## Pseudocódigo

El ejemplo divide una aplicación que gestiona dispositivos y sus controles remotos. Las clases `Dispositivo` actúan como implementación y las clases `Remoto` como abstracción. El control remoto base declara un campo de referencia que lo vincula a un dispositivo y opera a través de la interfaz general de dispositivos, lo que permite a un mismo remoto soportar varios tipos de dispositivo (PDF p. 184-185).

```
class RemoteControl is
    protected field device: Device
    constructor RemoteControl(device: Device) is
        this.device = device
    method togglePower() is
        if (device.isEnabled()) then device.disable()
        else device.enable()
    method volumeUp() is
        device.setVolume(device.getVolume() + 10)

class AdvancedRemoteControl extends RemoteControl is
    method mute() is
        device.setVolume(0)

interface Device is
    method isEnabled()
    method enable()
    method disable()
    method getVolume()
    method setVolume(percent)
    method getChannel()
    method setChannel(channel)

class Tv implements Device is // ...
class Radio implements Device is // ...

// Código cliente
tv = new Tv()
remote = new RemoteControl(tv)
radio = new Radio()
remote = new AdvancedRemoteControl(radio)
```

La interfaz de implementación no tiene por qué coincidir con la de la abstracción; de hecho pueden ser completamente diferentes (PDF p. 186-188).

## Aplicabilidad

- Cuando quieras dividir y organizar una clase monolítica con muchas variantes de una sola funcionalidad (por ejemplo, trabajar con diversos servidores de bases de datos).
- Cuando necesites extender una clase en varias dimensiones ortogonales (independientes): Bridge sugiere extraer una jerarquía de clase separada para cada dimensión.
- Cuando necesites poder cambiar implementaciones durante el tiempo de ejecución; sustituir el objeto de implementación es tan sencillo como asignar un nuevo valor a un campo. Este punto es la razón principal por la que mucha gente confunde Bridge con Strategy (PDF p. 188-189).

## Cómo implementarlo

1. Identifica las dimensiones ortogonales (abstracción/plataforma, dominio/infraestructura, front end/back end, interfaz/implementación).
2. Define las operaciones que necesita el cliente en la clase base de abstracción.
3. Declara en la interfaz general de implementación las operaciones que la abstracción necesita de todas las plataformas.
4. Crea clases concretas de implementación para cada plataforma, siguiendo la interfaz.
5. Añade en la abstracción un campo de referencia al tipo de implementación y delega en él la mayor parte del trabajo.
6. Si hay muchas variantes de lógica de alto nivel, crea abstracciones refinadas extendiendo la clase base.
7. El cliente pasa un objeto de implementación al constructor de la abstracción y luego trabaja solo con la abstracción (PDF p. 189-190).

## Pros y contras

- Puedes crear clases y aplicaciones independientes de plataforma.
- El código cliente trabaja con abstracciones de alto nivel y no queda expuesto a los detalles de la plataforma.
- Principio de abierto/cerrado: puedes introducir nuevas abstracciones e implementaciones independientes entre sí.
- Principio de responsabilidad única: la lógica de alto nivel queda en la abstracción y los detalles de plataforma en la implementación.
- Contra: el código puede complicarse si aplicas el patrón a una clase muy cohesionada (PDF p. 190-191).

## Relaciones con otros patrones

- Bridge suele diseñarse por anticipado; Adapter se usa con una aplicación existente para hacer trabajar juntas clases incompatibles.
- Bridge, State, Strategy (y en cierto punto Adapter) tienen estructuras similares basadas en composición, pero resuelven problemas diferentes.
- Abstract Factory puede usarse con Bridge cuando ciertas abstracciones solo funcionan con implementaciones específicas, encapsulando esas relaciones.
- Builder se puede combinar con Bridge: el director hace de abstracción y las constructoras de implementaciones (PDF p. 191-192).

## Ideas clave

- Bridge separa una clase en dos jerarquías independientes: abstracción (control de alto nivel) e implementación (trabajo de bajo nivel).
- Sustituye herencia por composición para evitar la explosión combinatoria de clases cuando hay dos dimensiones independientes.
- La abstracción delega el trabajo real en un objeto de implementación al que referencia.
- Abstracción e implementación pueden tener interfaces completamente diferentes y evolucionar por separado.
- Permite cambiar la implementación en tiempo de ejecución; esto lo hace confundible con Strategy, aunque la intención difiere.
- Úsalo ante dimensiones ortogonales o clases monolíticas con muchas variantes (p. ej., múltiples GUI y múltiples API).
- Favorece los principios de abierto/cerrado y de responsabilidad única.
- A diferencia de Adapter, Bridge se planifica desde el inicio del diseño.
