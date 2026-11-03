# Dive Into Design Patterns — Alexander Shvets (Refactoring.Guru, 2021)
## Capítulo 7 — Programa a una interfaz, no a una implementación (Program to an interface, not an implementation)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF (algunas palabras aparecían pegadas por la justificación) y las citas usan la página del PDF.

## Lo que necesitas saber

Este principio de diseño se resume en una frase: "Programa a una interfaz, no a una implementación. Depende de abstracciones, no de clases concretas" (PDF p. 46). La idea central es que un diseño es suficientemente flexible cuando puedes extenderlo con facilidad sin descomponer el código existente. El capítulo lo ilustra primero con una analogía y luego con un ejemplo de código más elaborado.

La tesis es que depender de abstracciones hace que la colaboración entre objetos sea más flexible que hacer que una clase dependa directamente de otra clase concreta. A cambio de esa flexibilidad, el código se vuelve algo más complicado, por lo que la decisión de extraer una interfaz debe tomarse cuando hay una razón real: un punto de extensión previsible o la posibilidad de que otras personas quieran extender tu código.

Sales sabiendo cómo convertir una dependencia concreta en una dependencia sobre una interfaz paso a paso, y entiendes que aplicar bien este principio puede llevarte, casi sin darte cuenta, a un patrón de diseño (aquí, Factory Method).

## La analogía del gato

Un gato que puede comer cualquier comida es más flexible que uno que solo puede comer salchichas. Al primer gato puedes darle salchichas, porque son un subgrupo de "cualquier comida", pero además puedes extender su menú con cualquier otra comida (PDF p. 46). La abstracción ("cualquier comida") admite más casos que la implementación concreta ("salchichas").

## Cómo establecer una colaboración flexible

Cuando quieres que dos clases colaboren, lo habitual es empezar haciendo una dependiente de la otra; el propio autor admite que suele empezar así (PDF p. 46). Pero hay una forma más flexible de establecer la colaboración entre objetos, en cuatro pasos:

1. Determina qué necesita exactamente un objeto del otro: ¿qué métodos ejecuta?
2. Describe esos métodos en una nueva interfaz o clase abstracta.
3. Haz que la clase que es una dependencia implemente esa interfaz.
4. Haz que la segunda clase dependa de esa interfaz en lugar de la clase concreta. Todavía puedes hacerla funcionar con objetos de la clase original, pero ahora la conexión es mucho más flexible (PDF p. 47).

Tras este cambio probablemente no notes un beneficio inmediato; al contrario, el código se vuelve más complicado que antes. Merece la pena solo si prevés que ese punto puede ser un buen lugar de extensión para funcionalidad adicional, o si otras personas que usan tu código podrían querer extenderlo ahí (PDF p. 47).

## El ejemplo que recorre el capítulo: el simulador de empresa

El capítulo desarrolla un simulador de una empresa de desarrollo de software, con distintas clases que representan varios tipos de empleados. El ejemplo evoluciona en tres etapas:

### ANTES: clases fuertemente acopladas

Al principio, la clase `Empresa` está fuertemente acoplada a clases de empleados concretos. A pesar de las diferencias en sus implementaciones, es posible generalizar varios métodos relacionados con el trabajo y extraer después una interfaz común para todas las clases de empleado (PDF p. 48–49).

### MEJOR: polimorfismo con la interfaz Empleado

Después de extraer la interfaz `Empleado`, se puede aplicar polimorfismo dentro de la clase `Empresa`, tratando los distintos objetos de empleado a través de esa interfaz. El polimorfismo simplifica el código, pero el resto de la clase `Empresa` aún depende de las clases de empleado concretas (PDF p. 49).

Esto no es bueno: si introducimos nuevos tipos de empresas que funcionan con otros tipos de empleados, tendríamos que sobrescribir la mayor parte de la clase `Empresa` en lugar de reutilizar ese código (PDF p. 49).

### DESPUÉS: método para obtener empleados declarado como abstracto

La solución es declarar como abstracto el método que obtiene los empleados. Cada empresa concreta implementará ese método de forma diferente, creando únicamente los empleados que necesita (PDF p. 49–50). Así, el método primario de la clase `Empresa` queda independiente de las clases de empleado concretas, y los objetos de empleado se crean en las subclases de empresa concretas.

Tras el cambio, la clase `Empresa` se vuelve independiente de las distintas clases de empleado. Puedes extenderla e introducir nuevos tipos de empresas y empleados reutilizando parte de la clase base `Empresa`, y extender esa clase base no descompone el código existente que ya se apoya en ella (PDF p. 50).

El autor señala que, al hacer esto, acabamos de ver la aplicación de un patrón de diseño en acción: es un ejemplo del patrón **Factory Method**, que se explicará en detalle más adelante (PDF p. 50).

## Ideas clave

- Programa a una interfaz, no a una implementación: depende de abstracciones, no de clases concretas (PDF p. 46).
- Un diseño es flexible si puedes extenderlo con facilidad sin descomponer el código existente.
- Una abstracción ("cualquier comida") admite más casos que una implementación concreta ("salchichas").
- Pasos para colaborar de forma flexible: identificar los métodos necesarios, describirlos en una interfaz, implementarla en la dependencia y depender de la interfaz, no de la clase concreta.
- Extraer una interfaz añade complejidad; hazlo solo cuando prevés un punto de extensión real.
- Aplicar polimorfismo reduce acoplamiento, pero la creación de objetos concretos puede seguir acoplando las clases.
- Declarar abstracto el método de creación y delegarlo a las subclases elimina ese acoplamiento restante.
- Ese patrón de creación delegado a subclases es el **Factory Method** (PDF p. 50).
