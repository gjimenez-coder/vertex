# Dive Into Design Patterns — Alexander Shvets (Refactoring.Guru, 2021)
## Capítulo 2 — Los pilares de la POO (The Pillars of OOP)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas usan la página del PDF.

## Lo que necesitas saber

Este capítulo breve presenta los cuatro pilares sobre los que se asienta la programación orientada a objetos (POO): abstracción, encapsulación, herencia y polimorfismo. Son los conceptos que, según el autor, diferencian a la POO de otros paradigmas de programación.

La idea central es que estos cuatro principios permiten modelar objetos del mundo real dentro de un programa de forma limitada y útil, ocultar la complejidad tras interfaces sencillas, reutilizar código entre clases y escribir programas que respondan al tipo real de un objeto aunque ese tipo no se conozca de antemano. Al terminar, sales sabiendo qué significa cada pilar, con ejemplos concretos (aviones, autos, animales) que el libro usa para ilustrarlos.

## Abstracción

Cuando programas con POO, modelas los objetos del programa a partir de objetos del mundo real, pero los objetos del programa no los representan con precisión del 100 % (y rara vez hace falta). Tus objetos solo copian los atributos y comportamientos relevantes para un contexto específico e ignoran el resto.

El ejemplo es una clase `Avión`: podría existir tanto en un simulador de vuelo como en una aplicación de reserva de vuelos. En el primer caso contendría información relacionada con el propio vuelo; en el segundo solo haría falta preocuparse del mapa de asientos y de los asientos disponibles. Es el mismo objeto del mundo real modelado de forma distinta según el contexto.

> La Abstracción es el modelo de un objeto o fenómeno del mundo real, limitado a un contexto específico (PDF p. 15).

## Encapsulación

Para arrancar un auto solo giras una llave o pulsas un botón; no necesitas conectar cables, rotar el cigüeñal ni iniciar el ciclo de potencia del motor. Esos detalles se esconden bajo el capó. Solo dispones de una interfaz simple: interruptor de encendido, volante y pedales. Así, cada objeto cuenta con una **interfaz**: la parte pública abierta a interacciones con otros objetos.

La encapsulación es la capacidad de un objeto de esconder partes de su estado y comportamiento, exponiendo únicamente una interfaz limitada al resto del programa. Encapsular algo significa hacerlo **privado**, accesible solo desde los métodos de su propia clase. Existe un modelo menos restrictivo, **protegido**, que hace que el miembro también esté disponible para las subclases.

Las interfaces y las clases y métodos abstractos de la mayoría de los lenguajes se basan en abstracción y encapsulación. En los lenguajes modernos, el mecanismo de interfaz (declarado con `interface` o `protocol`) permite definir contratos de interacción entre objetos. Por eso las interfaces solo se interesan por los comportamientos de los objetos, y por eso no puedes declarar un campo en una interfaz.

El autor señala la confusión del término: *interfaz* se refiere a la parte pública de un objeto, pero también existe el tipo `interface` en la mayoría de los lenguajes.

El ejemplo: una interfaz `TransporteAéreo` con un método `vuelo(origen, destino, pasajeros)`. Al diseñar un simulador de transporte aéreo puedes restringir la clase `Aeropuerto` para que solo funcione con objetos que implementen `TransporteAéreo`. Así, cualquier objeto pasado al aeropuerto —un `Avión`, un `Helicóptero` o incluso un `GrifoDomesticado`— podrá aterrizar o despegar. Puedes cambiar la implementación del método `volar` como quieras; mientras la firma coincida con la declarada en la interfaz, todas las instancias de `Aeropuerto` funcionarán con tus objetos voladores.

## Herencia

La herencia es la capacidad de crear nuevas clases sobre otras existentes. Su principal ventaja es la **reutilización de código**: si quieres una clase ligeramente distinta de una ya existente, no duplicas código; extiendes la clase existente y colocas la funcionalidad adicional en una subclase que hereda los campos y métodos de la superclase.

La consecuencia es que las subclases tienen la misma interfaz que su clase padre. No puedes esconder en una subclase un método declarado en la superclase, y debes implementar todos los métodos abstractos aunque no tengan sentido en tu subclase.

En la mayoría de los lenguajes una subclase puede extender una única superclase, pero cualquier clase puede implementar varias interfaces al mismo tiempo. Si una superclase implementa una interfaz, todas sus subclases deben implementarla también.

## Polimorfismo

Con un ejemplo de animales: la mayoría de los `Animal` puede emitir sonidos. Como todas las subclases necesitarán sobrescribir el método base `emitirSonido` para emitir el sonido correcto, conviene declararlo abstracto directamente. Esto permite omitir cualquier implementación por defecto en la superclase, pero fuerza a cada subclase a definir la suya.

Imagina gatos y perros dentro de una bolsa: con los ojos tapados, vas sacando los animales de uno en uno. Al sacar un animal no sabes qué es, pero si lo abrazas lo suficiente emitirá un sonido específico según su clase concreta.

El programa no conoce el tipo concreto del objeto contenido en la variable, pero gracias al **polimorfismo** puede rastrear la subclase del objeto cuyo método se ejecuta y ejecutar el comportamiento adecuado.

> El polimorfismo es la capacidad de un programa de detectar la verdadera clase de un objeto e invocar su implementación, incluso aunque su tipo real sea desconocido en el contexto actual (PDF p. 21).

También puede pensarse en el polimorfismo como la capacidad de un objeto de "fingir" ser otra cosa, normalmente una clase que extiende o una interfaz que implementa. En el ejemplo, los perros y gatos de la bolsa fingen ser animales genéricos.

```
bag = [new Cat(), new Dog()];

foreach (Animal a : bag)
    a.makeSound()

// ¡Miau!
// ¡Guau!
```

## Ideas clave

- La POO se apoya en cuatro pilares: abstracción, encapsulación, herencia y polimorfismo.
- Abstracción: modelar un objeto real limitado a un contexto específico, copiando solo los atributos y comportamientos relevantes.
- Un mismo objeto real (p. ej. `Avión`) se modela distinto según el contexto (simulador vs. reserva de vuelos).
- Encapsulación: ocultar estado y comportamiento internos, exponiendo solo una interfaz limitada; miembros privados (solo la clase) o protegidos (también subclases).
- Las interfaces definen contratos de comportamiento; por eso no pueden declarar campos.
- Herencia: crear clases sobre otras existentes para reutilizar código; la subclase hereda la interfaz de la superclase y debe implementar sus métodos abstractos.
- Una subclase extiende una sola superclase, pero una clase puede implementar varias interfaces.
- Polimorfismo: el programa invoca la implementación de la clase real de un objeto aunque su tipo concreto sea desconocido en el contexto actual.
