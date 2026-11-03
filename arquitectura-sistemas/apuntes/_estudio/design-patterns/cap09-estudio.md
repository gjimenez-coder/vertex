# S: Single Responsibility Principle (S: Principio de responsabilidad única) — Estudio

## Tarjetas de repaso

P: ¿Qué enuncia el principio de responsabilidad única? / R: Que una clase sólo debe tener una razón para cambiar (PDF p. 56).

P: ¿A qué letra y acrónimo corresponde este principio? / R: A la letra S del acrónimo SOLID.

P: ¿De qué debe ser responsable cada clase según el principio? / R: De una única parte de la funcionalidad del software.

P: ¿Dónde debe quedar esa responsabilidad? / R: Totalmente encapsulada, escondida dentro de la clase.

P: ¿Cuál es el objetivo principal del principio? / R: Reducir la complejidad.

P: ¿Hace falta un diseño sofisticado para un programa de unas 200 líneas? / R: No; con un puñado de buenos métodos basta.

P: ¿Cuándo aparecen los verdaderos problemas de diseño? / R: Cuando el programa crece y cambia constantemente, y las clases se vuelven tan grandes que no recuerdas sus detalles.

P: ¿Qué pasa con la navegación del código al crecer el programa? / R: Se ralentiza "hasta ir a paso de tortuga" (PDF p. 56) y tienes que recorrer clases o el programa entero para hallar algo.

P: ¿Qué riesgo implica una clase que hace demasiadas cosas? / R: Debe cambiarse ante cada cambio de alguna de esas cosas, con riesgo de romper partes que no pretendías tocar.

P: ¿Cuál es el síntoma de alerta para aplicar el principio? / R: Que te cueste centrarte en un aspecto específico del programa.

P: ¿Por qué dos razones cambia la clase `Empleado` del ejemplo? / R: Por gestionar la información de los empleados y porque el formato del informe de horas puede cambiar.

P: ¿Cuál es la solución propuesta en el ejemplo `Empleado`? / R: Mover el comportamiento de impresión del informe de horas a una clase separada.

P: ¿Qué se logra tras extraer el informe a su propia clase? / R: Que cada clase tenga una sola razón para cambiar.

## Preguntas de autoevaluación

P: ¿Cómo se relaciona el principio de responsabilidad única con la encapsulación?
R: La responsabilidad única de cada clase debe quedar totalmente encapsulada (escondida) dentro de ella. (Sección: Lo que necesitas saber)

P: ¿Por qué el autor dice que un programa pequeño no necesita este principio de forma estricta?
R: Porque para unas 200 líneas basta un puñado de buenos métodos; la complejidad problemática surge al crecer y cambiar constantemente. (Sección: Lo que necesitas saber)

P: ¿Qué dos problemas provoca que las clases crezcan demasiado?
R: Que la navegación del código se ralentiza y pierdes el control, y que cualquier cambio obliga a modificar la clase con riesgo de romper partes no previstas. (Sección: Por qué importa: la complejidad al crecer)

P: ¿Qué señal práctica indica que podría ser momento de dividir una clase?
R: La dificultad recurrente para concentrarte en un único aspecto del programa. (Sección: Por qué importa: la complejidad al crecer)

P: En el ejemplo, ¿cuál es la razón de cambio ligada al trabajo principal de la clase `Empleado`?
R: Gestionar la información de los empleados. (Sección: El ejemplo que recorre el capítulo)

P: ¿Qué beneficio adicional aporta mover el informe de horas a una clase separada?
R: Permite mover también otros elementos relacionados con el informe a la nueva clase. (Sección: El ejemplo que recorre el capítulo)

P: ¿Cuál es el objetivo último que persigue dividir responsabilidades entre clases?
R: Reducir la complejidad del software. (Sección: Lo que necesitas saber / Ideas clave)

## Checklist — Puntos a dominar

- El enunciado: una clase sólo debe tener una razón para cambiar.
- La relación entre responsabilidad única, encapsulación y reducción de complejidad.
- Reconocer cuándo NO hace falta aplicarlo con rigor (programas pequeños, ~200 líneas).
- Identificar el síntoma de alerta: no poder centrarte en un aspecto específico del programa.
- Detectar clases con varias razones para cambiar (como `Empleado`).
- Aplicar el refactor: extraer a una clase separada el comportamiento que cambia por otra razón (p. ej. la impresión del informe de horas).
- Verificar el resultado: cada clase con una sola razón para cambiar.
