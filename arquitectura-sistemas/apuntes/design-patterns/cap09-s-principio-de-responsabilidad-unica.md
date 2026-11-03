# Dive Into Design Patterns — Alexander Shvets (Refactoring.Guru, 2021)
## Capítulo 9 — S: Single Responsibility Principle (S: Principio de responsabilidad única)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF (con muchas palabras pegadas por la justificación de párrafos) y las citas usan la página del PDF.

## Lo que necesitas saber

Este capítulo presenta la primera letra del acrónimo SOLID: el principio de responsabilidad única (Single Responsibility Principle). Su enunciado es breve: una clase sólo debe tener una razón para cambiar. La idea es hacer a cada clase responsable de una única parte de la funcionalidad del software y lograr que esa responsabilidad quede totalmente encapsulada —escondida— dentro de la clase.

El objetivo principal del principio es reducir la complejidad. El autor aclara que no hace falta un diseño sofisticado para un programa de unas 200 líneas de código: con un puñado de buenos métodos basta. Los verdaderos problemas aparecen cuando el programa crece y cambia constantemente, y las clases se vuelven tan grandes que ya no puedes recordar sus detalles.

Sales sabiendo cuándo y por qué conviene dividir una clase: cuando hace demasiadas cosas, cada cambio en una de esas cosas te obliga a modificarla, y al hacerlo te arriesgas a descomponer otras partes de la clase que no pretendías tocar. Si te cuesta centrarte en un aspecto específico del programa cada vez, es señal de que puede ser el momento de aplicar el principio.

## Por qué importa: la complejidad al crecer

Cuando el programa crece, las clases se vuelven tan grandes que ya no recuerdas sus detalles. La navegación del código se ralentiza "hasta ir a paso de tortuga" (PDF p. 56) y tienes que recorrer clases enteras o incluso un programa completo para encontrar algo específico. El número de entidades del programa supera tu capacidad cerebral y sientes que pierdes el control sobre el código.

Hay un segundo problema: si una clase hace demasiadas cosas, tienes que cambiarla cada vez que una de esas cosas cambia, con el riesgo de romper partes que no pretendías modificar. El síntoma práctico es la dificultad recurrente para concentrarte en un único aspecto del programa; ante ese síntoma, conviene recordar el principio y comprobar si toca dividir algunas clases en partes.

## El ejemplo que recorre el capítulo

El ejemplo usa una clase `Empleado` que tiene varias razones para cambiar:

- La primera razón está ligada al trabajo principal de la clase: gestionar información de los empleados.
- La segunda razón es que el formato del informe de horas de trabajo puede cambiar con el tiempo, lo que te obliga a cambiar el código de la clase.

Progresión del refactor:

- ANTES: la clase contiene varios comportamientos diferentes mezclados.
- Solución: mover el comportamiento relacionado con la impresión de informes de horas de trabajo a una clase separada. Este cambio permite además mover otros elementos relacionados con el informe a la nueva clase.
- DESPUÉS: el comportamiento adicional queda en su propia clase, y cada clase tiene una sola razón para cambiar.

## Ideas clave

- Una clase sólo debe tener una razón para cambiar (PDF p. 56).
- Cada clase debe ser responsable de una única parte de la funcionalidad, totalmente encapsulada dentro de ella.
- El objetivo del principio es reducir la complejidad.
- Para programas pequeños (unas 200 líneas) no hace falta un diseño sofisticado; el problema surge al crecer y cambiar constantemente.
- Una clase que hace demasiadas cosas debe cambiarse ante cada cambio, con riesgo de romper partes no previstas.
- Síntoma de alerta: que te cueste centrarte en un aspecto específico del programa.
- En el ejemplo, la clase `Empleado` cambia por dos motivos (gestión de datos e informe de horas); la solución es extraer la impresión del informe a una clase separada.
