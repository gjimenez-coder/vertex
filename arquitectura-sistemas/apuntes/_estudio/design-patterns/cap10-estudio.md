# Capítulo 10 — O: Principio de abierto/cerrado (Open/Closed Principle) — Estudio

## Tarjetas de repaso

P: ¿Qué enuncia el principio de abierto/cerrado? / R: Que las clases deben estar abiertas a la extensión pero cerradas a la modificación (PDF p. 58).

P: ¿Cuál es la idea de fondo del principio? / R: Evitar que el código existente se descomponga cuando implementas nuevas funciones.

P: ¿Qué significa que una clase esté "abierta"? / R: Que puedes extenderla: crear una subclase, añadir métodos o campos, o sobrescribir el comportamiento base.

P: ¿Cómo se puede restringir la extensión de una clase? / R: Con palabras clave como `final`, tras lo cual la clase ya no está abierta.

P: ¿Qué significa que una clase esté "cerrada"? / R: Que está lista al 100 % para que otras clases la usen; su interfaz está claramente definida y no se cambiará en el futuro.

P: ¿Son excluyentes los términos "abierta" y "cerrada"? / R: No; respecto a este principio una clase puede estar a la vez abierta (para la extensión) y cerrada (para la modificación).

P: ¿Por qué es arriesgado modificar directamente una clase ya desarrollada? / R: Porque ya fue probada, revisada e incluida en un framework o aplicación, y juguetear con su código puede descomponer a sus clientes existentes.

P: ¿Cuál es la alternativa a modificar el código de una clase? / R: Crear una subclase y sobrescribir las partes que quieras que se comporten distinto, sin descomponer los clientes existentes (PDF p. 58-59).

P: ¿Aplica el principio a la corrección de errores? / R: No; si sabes que hay un error debes arreglarlo, no crear una subclase. Una clase hija no debe ser responsable de los problemas de la padre (PDF p. 59).

P: En el ejemplo, ¿qué problema tenía la clase `Pedido` antes del refactor? / R: Los métodos de envío estaban incrustados en la clase, así que había que modificar `Pedido` cada vez que se añadía un método de envío (PDF p. 59).

P: ¿Qué patrón resuelve el problema del ejemplo `Pedido`? / R: El patrón Strategy: se extraen los métodos de envío a clases separadas con una interfaz común (`Envíos`) (PDF p. 60).

P: Tras el refactor, ¿cómo se añade un nuevo método de envío? / R: Derivando una nueva clase de la interfaz `Envíos`, sin tocar el código de la clase `Pedido` (PDF p. 60-61).

P: ¿Qué ventaja adicional aporta la solución del ejemplo? / R: Permite mover el cálculo del tiempo de entrega a clases más relevantes, cumpliendo el principio de responsabilidad única (PDF p. 61).

## Preguntas de autoevaluación

P: Explica con tus palabras las dos mitades del principio abierto/cerrado. / R: Abierta a la extensión (puedes añadir comportamiento mediante subclases, nuevos métodos/campos o sobrescritura) y cerrada a la modificación (su interfaz está definida y estable y no se cambia). (Sección: Lo que necesitas saber)

P: ¿Por qué no contradice el principio que una clase sea abierta y cerrada al mismo tiempo? / R: Porque "abierta" se refiere a poder extenderla y "cerrada" a no modificar su código ni interfaz; son dimensiones distintas, no opuestas. (Sección: Lo que necesitas saber)

P: ¿Qué riesgo concreto se corre al modificar una clase ya integrada en un framework o aplicación? / R: Descomponer a los clientes existentes que dependen de esa clase, porque ya estaba probada y en uso. (Sección: Por qué extender en lugar de modificar)

P: ¿Cuál es el límite del principio y por qué existe? / R: No aplica a corregir errores; un bug se arregla en la clase, no se parchea con una subclase, porque una clase hija no debe cargar con los problemas de la padre. (Sección: Por qué extender en lugar de modificar)

P: Describe el cambio entre el ANTES y el DESPUÉS del ejemplo de `Pedido`. / R: Antes los métodos de envío estaban dentro de `Pedido` y añadir uno exigía modificarla; después se extraen a clases con la interfaz común `Envíos`, de modo que añadir un método ya no requiere cambiar clases existentes. (Sección: El ejemplo que recorre el capítulo)

P: ¿Cómo vincula el código cliente un pedido con un nuevo método de envío tras el refactor? / R: El código cliente de `Pedido` vincula el pedido con un objeto de envío de la nueva clase cuando el usuario selecciona ese método en la UI. (Sección: El ejemplo que recorre el capítulo)

P: ¿De qué manera el refactor que satisface abierto/cerrado también mejora otro principio SOLID? / R: Al extraer el cálculo del tiempo de entrega a clases más relevantes, mejora la cohesión según el principio de responsabilidad única. (Sección: Ventaja adicional)

## Puntos a dominar

- Enunciar el principio: abierto a la extensión, cerrado a la modificación (PDF p. 58).
- Distinguir qué hace a una clase "abierta" (extensible) frente a "cerrada" (interfaz estable y completa).
- Reconocer que `final` cierra la extensión de una clase.
- Argumentar por qué extender vía subclase es más seguro que modificar código ya probado y en uso.
- Identificar el límite del principio: los errores se corrigen, no se subclasifican.
- Explicar cómo el patrón Strategy aplica el principio en el ejemplo de `Pedido` y la interfaz `Envíos`.
- Relacionar la solución con el principio de responsabilidad única mediante el cálculo del tiempo de entrega.
