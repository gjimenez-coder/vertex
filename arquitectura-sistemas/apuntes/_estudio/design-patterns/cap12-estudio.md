# I: Interface Segregation Principle (Principio de segregación de la interfaz) — Estudio

## Tarjetas de repaso

P: ¿Qué enuncia el principio de segregación de la interfaz (ISP)?
R: No se debe forzar a los clientes a depender de métodos que no utilizan.

P: ¿A qué letra de SOLID corresponde este capítulo?
R: A la "I" de SOLID.

P: ¿Cómo deben ser las interfaces según el ISP?
R: Lo bastante estrechas como para que las clases cliente no implementen comportamientos que no necesitan.

P: ¿Qué hay que hacer con las interfaces "gruesas"?
R: Desintegrarlas en interfaces más detalladas y específicas, para que cada cliente implemente solo los métodos que de verdad necesita.

P: ¿Qué riesgo tiene un cambio en una interfaz gruesa?
R: Puede descomponer incluso a clientes que no utilizan los métodos cambiados.

P: ¿Por qué no hace falta amontonar métodos no relacionados en una sola interfaz?
R: Porque una clase hereda de una única superclase, pero puede implementar múltiples interfaces a la vez.

P: ¿Qué ejemplo recorre el capítulo?
R: Una biblioteca para integrar aplicaciones con varios proveedores de computación en la nube.

P: ¿Cómo era la versión inicial de esa biblioteca?
R: Solo soportaba Amazon Cloud, pero cubría todos sus servicios y funciones.

P: ¿Qué supuesto equivocado se hizo en el diseño inicial?
R: Que todos los proveedores de nube tendrían la misma amplitud de funciones que Amazon.

P: ¿Qué problema apareció al dar soporte a otro proveedor?
R: La mayoría de las interfaces eran demasiado amplias: describían funciones que otros proveedores no incluyen.

P: ¿Cuál es la solución que propone el capítulo?
R: Dividir la interfaz en partes, de modo que cada clase implemente solo las interfaces cuyos métodos le tienen sentido.

P: ¿Por qué colocar maquetas en los métodos sobrantes no es buena solución?
R: Porque no es una solución limpia frente a dividir la interfaz.

P: ¿Cuál es el límite o equilibrio del ISP?
R: No dividir una interfaz que ya es bastante específica, porque más interfaces complican el código.

## Preguntas de autoevaluación

1. ¿Qué significa "interfaz gruesa" y por qué es un problema?
R: Una interfaz que reúne demasiados métodos, incluidos algunos no relacionados; un cambio en ella puede descomponer a clientes que ni siquiera usan los métodos modificados. (El principio)

2. ¿Qué característica del lenguaje aprovecha el ISP para evitar interfaces sobredimensionadas?
R: Que una clase puede implementar varias interfaces simultáneamente, aunque solo pueda heredar de una superclase; así se dividen los métodos sin amontonarlos. (El principio)

3. En el ejemplo de la nube, ¿por qué fallaron las interfaces al añadir un segundo proveedor?
R: Porque se diseñaron asumiendo la amplitud de funciones de Amazon, y resultaron demasiado amplias: incluían métodos de funciones que otros proveedores no ofrecen. (El ejemplo que recorre el capítulo)

4. ¿Qué resultado concreto produce dividir la interfaz abotargada?
R: Se obtiene un grupo de interfaces más detalladas, y cada proveedor implementa solo las que corresponden a las funciones que realmente ofrece. (La solución: dividir la interfaz)

5. ¿Cómo se puede ir "demasiado lejos" al aplicar el ISP?
R: Fragmentando interfaces que ya son suficientemente específicas, lo que aumenta el número de interfaces y complica el código. (El equilibrio)

6. ¿Cuál es la recomendación final del capítulo respecto a la segregación de interfaces?
R: Mantener el equilibrio: dividir lo necesario sin crear interfaces de más. (El equilibrio)

## Puntos a dominar

- El enunciado del ISP: no forzar a los clientes a depender de métodos que no usan.
- Reconocer interfaces "gruesas" o abotargadas y el riesgo de acoplar clientes a métodos que no utilizan.
- Entender que implementar múltiples interfaces evita amontonar métodos no relacionados.
- Saber que la solución es dividir la interfaz en interfaces más específicas y que cada clase implemente solo las que le tienen sentido.
- Interpretar el ejemplo de la biblioteca de proveedores de nube como caso de interfaz demasiado amplia.
- Conocer el límite: no sobre-fragmentar interfaces ya específicas; mantener el equilibrio.
