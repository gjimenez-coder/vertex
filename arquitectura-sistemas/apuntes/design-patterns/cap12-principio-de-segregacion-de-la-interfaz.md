# Dive Into Design Patterns — Alexander Shvets (Refactoring.Guru, 2021)
## Capítulo 12 — I: Interface Segregation Principle (Principio de segregación de la interfaz)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF (con palabras pegadas por la justificación); las citas usan la página del PDF.

## Lo que necesitas saber

Este capítulo corresponde a la "I" de SOLID: el principio de segregación de la interfaz (Interface Segregation Principle). La idea central se resume en una frase: no se debe forzar a los clientes a depender de métodos que no utilizan. El objetivo es diseñar interfaces lo bastante estrechas como para que las clases cliente no tengan que implementar comportamientos que no necesitan.

La tesis es que las interfaces "gruesas" deben desintegrarse en otras más detalladas y específicas, de modo que cada cliente implemente únicamente los métodos que realmente necesita. Si no se hace así, un cambio en una interfaz gruesa puede descomponer incluso a clientes que no usan los métodos modificados.

Sales sabiendo cómo detectar interfaces sobredimensionadas, por qué la posibilidad de implementar varias interfaces (a diferencia de la herencia de una sola superclase) hace innecesario amontonar métodos no relacionados, y cuál es el límite: no conviene fragmentar interfaces que ya son suficientemente específicas.

## El principio

Según el principio, debes desintegrar las interfaces "gruesas" hasta crear otras más detalladas y específicas. Los clientes deben implementar únicamente aquellos métodos que necesitan de verdad; de lo contrario, un cambio en una interfaz gruesa descompondrá incluso clientes que no utilizan los métodos cambiados.

La herencia de clases permite a una clase tener una única superclase, pero no limita el número de interfaces que la clase puede implementar al mismo tiempo. Por eso no hay necesidad de amontonar toneladas de métodos no relacionados en una única interfaz: conviene dividirla en varias interfaces más refinadas, que pueden implementarse todas en una misma clase si es necesario. Algunas clases, en cambio, solo necesitarán implementar una de ellas.

## El ejemplo que recorre el capítulo

Imagina una biblioteca que facilita la integración de aplicaciones con varios proveedores de computación en la nube. En su versión inicial solo soportaba Amazon Cloud, pero cubría todos los servicios y funciones de esa nube. En aquel momento se asumió que todos los proveedores tendrían la misma amplitud de funciones que Amazon.

Cuando hubo que dar soporte a otro proveedor, se descubrió que la mayoría de las interfaces de la biblioteca eran demasiado amplias: algunos métodos describen funciones que otros proveedores de la nube no incluyen. Como lo resume el texto, "ANTES: no todos los clientes pueden satisfacer los requisitos de la abotargada interfaz" (PDF p. 70).

## La solución: dividir la interfaz

Se podrían implementar esos métodos sobrantes colocando algunas maquetas, pero no sería una solución muy limpia. La mejor solución es dividir la interfaz en partes. Así, las clases capaces de implementar la interfaz original pueden ahora implementar varias interfaces refinadas, mientras que otras clases implementan únicamente aquellas interfaces cuyos métodos tienen sentido para ellas.

El resultado es que una interfaz "abotargada" se divide en un grupo de interfaces más detalladas (PDF p. 71): cada proveedor de nube implementa solo las interfaces correspondientes a las funciones que realmente ofrece.

## El equilibrio

Como sucede con otros principios SOLID, con este también puedes ir demasiado lejos. No se debe dividir una interfaz que ya es bastante específica. Hay que recordar que, cuantas más interfaces crees, más se complicará tu código. La recomendación final es mantener el equilibrio.

## Ideas clave

- El principio: no se debe forzar a los clientes a depender de métodos que no utilizan.
- Haz las interfaces lo bastante estrechas para que las clases cliente no implementen comportamientos innecesarios.
- Desintegra las interfaces "gruesas" en interfaces más detalladas y específicas.
- Un cambio en una interfaz gruesa descompone incluso a clientes que no usan los métodos cambiados.
- Una clase hereda de una sola superclase, pero puede implementar múltiples interfaces: aprovéchalo para no amontonar métodos no relacionados.
- En el ejemplo de la nube, las interfaces pensadas para Amazon resultaron demasiado amplias para otros proveedores.
- La solución es dividir la interfaz en partes; cada clase implementa solo las que le tienen sentido.
- Cuidado con el exceso: no dividas interfaces ya específicas, porque más interfaces complican el código. Mantén el equilibrio.
