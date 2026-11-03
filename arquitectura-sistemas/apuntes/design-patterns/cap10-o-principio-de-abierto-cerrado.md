# Dive Into Design Patterns — Alexander Shvets (Refactoring.Guru, 2021)
## Capítulo 10 — O: Principio de abierto/cerrado (Open/Closed Principle)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF (el original tiene muchas palabras pegadas por la justificación de párrafos) y las citas usan la página del PDF.

## Lo que necesitas saber

Este capítulo presenta la "O" de los principios SOLID: el principio de abierto/cerrado. Su enunciado es que las clases deben estar abiertas a la extensión pero cerradas a la modificación (PDF p. 58). La idea de fondo es evitar que el código existente se descomponga cuando implementas nuevas funciones.

Sales sabiendo qué significa cada mitad del principio. Una clase está abierta si puedes extenderla: crear una subclase, añadir métodos o campos, o sobrescribir el comportamiento base. Algunos lenguajes permiten restringir la extensión con palabras clave como `final`, y tras eso la clase ya no está abierta. Una clase está cerrada si está lista al 100 % para que otras clases la utilicen; su interfaz está claramente definida y no se cambiará en el futuro.

El autor señala que los términos abierta y cerrada suenan mutuamente excluyentes, pero no lo son: respecto a este principio una clase puede estar al mismo tiempo abierta (para la extensión) y cerrada (para la modificación).

## Por qué extender en lugar de modificar

Cuando una clase ya se ha desarrollado, probado, revisado e incluido en un framework o utilizado en una aplicación, es arriesgado juguetear con su código. En lugar de cambiar directamente el código de la clase, puedes crear una subclase y sobrescribir las partes que quieras que se comporten de otra forma, logrando tu objetivo sin descomponer los clientes existentes de la clase original (PDF p. 58-59).

El principio tiene un límite importante: no está pensado para aplicarse a todos los cambios de una clase. Si sabes que hay un error, debes arreglarlo; no crees una subclase para ello. Una clase hija no debe ser responsable de los problemas de la clase padre (PDF p. 59).

## El ejemplo que recorre el capítulo

El ejemplo es una aplicación de comercio electrónico con una clase `Pedido` que calcula los costos de envío, con todos los métodos de envío incrustados dentro de la clase.

- ANTES: si necesitas añadir un nuevo método de envío, tienes que cambiar el código de la clase `Pedido`, arriesgándote a descomponerla. Es decir, hay que modificar `Pedido` cada vez que se añade un método de envío (PDF p. 59).
- DESPUÉS: el problema se resuelve aplicando el patrón Strategy. Se extraen los métodos de envío y se colocan en clases separadas con una interfaz común (`Envíos`). Añadir un nuevo método de envío ya no requiere cambiar clases existentes (PDF p. 60).

Con esta solución, cuando necesitas implementar un nuevo método de envío, derivas una nueva clase de la interfaz `Envíos` sin tocar el código de la clase `Pedido`. El código cliente de `Pedido` vinculará los pedidos con un objeto de envío de la nueva clase cuando el usuario seleccione esos métodos de envío en la UI (PDF p. 60-61).

## Ventaja adicional

La solución tiene una ventaja extra: permite mover el cálculo del tiempo de entrega a clases más relevantes, de acuerdo con el principio de responsabilidad única (PDF p. 61). Así, el refactor que satisface abierto/cerrado también mejora la cohesión según el principio anterior de SOLID.

## Ideas clave

- Abierto/cerrado: las clases deben estar abiertas a la extensión y cerradas a la modificación (PDF p. 58).
- La meta es evitar descomponer el código existente al implementar nuevas funciones.
- Abierta = extensible (subclases, nuevos métodos/campos, sobrescribir); palabras clave como `final` cierran la extensión.
- Cerrada = interfaz lista al 100 %, definida y estable, que no cambiará en el futuro.
- Una misma clase puede ser abierta y cerrada a la vez; los términos no son excluyentes aquí.
- El principio no aplica a corregir errores: un bug se arregla, no se "parchea" con una subclase.
- El ejemplo de `Pedido` muestra cómo el patrón Strategy extrae los métodos de envío a clases con interfaz común, evitando modificar clases existentes.
- La solución además habilita cumplir el principio de responsabilidad única moviendo el cálculo del tiempo de entrega a clases más relevantes.
