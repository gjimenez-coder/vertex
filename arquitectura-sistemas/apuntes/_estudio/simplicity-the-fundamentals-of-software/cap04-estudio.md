# The Future (El futuro) — Estudio

## Tarjetas de repaso

P: ¿Cuál es la pregunta central del diseñador de software según el capítulo?
R: Cómo tomar decisiones sobre el software; no qué decisión es absolutamente correcta, sino cómo ordenar las opciones posibles y elegir la mejor entre muchas.

P: ¿Qué representan las variables D, V y E en la Ecuación del Diseño de Software?
R: D es la deseabilidad de un cambio, V su valor y E el esfuerzo que implica realizarlo.

P: ¿Cómo se relaciona la deseabilidad con el valor y el esfuerzo?
R: La deseabilidad es directamente proporcional al valor e inversamente proporcional al esfuerzo.

P: ¿Cuál es la definición más simple de valor?
R: El grado en que un cambio ayuda a alguien en cualquier lugar; lo más importante es ayudar a los usuarios, aunque sostenerte financieramente también es valor.

P: ¿Cuáles son los dos factores que componen el valor?
R: La probabilidad de valor (qué tan probable es que ayude, a cuántos y con qué frecuencia) y el valor potencial (cuánto ayuda cuando sí ayuda).

P: ¿Qué es el "balance del daño" al calcular el valor?
R: Algunos cambios causan daño además de ayudar (p. ej., anuncios que molestan), y calcular el valor incluye restar ese daño.

P: ¿Por qué las funciones sin usuarios no tienen valor inmediato?
R: Porque no se encuentran, son difíciles de usar o no ayudan a nadie; por eso casi siempre hay que liberar el software a tiempo para que tenga valor.

P: ¿Qué incluye el esfuerzo además de programar?
R: Todo el tiempo conectado con el cambio: investigación, comunicación entre desarrolladores y tiempo de reflexión, más costos ocultos como arreglar los bugs que el cambio introduce.

P: ¿Cuáles son los cuatro componentes de la ecuación completa?
R: Esfuerzo de implementación (Ei), esfuerzo de mantenimiento (Em), valor ahora (Vn) y valor futuro (Vf).

P: Enuncia la ley primaria del diseño de software.
R: La deseabilidad de un cambio es directamente proporcional al valor ahora más el valor futuro, e inversamente proporcional al esfuerzo de implementación más el de mantenimiento.

P: ¿A qué se reduce la ecuación cuando se razona sobre plazos largos?
R: A comparar el valor futuro frente al esfuerzo de mantenimiento, porque el valor ahora y el esfuerzo de implementación suelen volverse insignificantes.

P: ¿Cuál es la solución ideal y única garantía de éxito respecto al mantenimiento?
R: Diseñar sistemas cuyo esfuerzo de mantenimiento disminuya con el tiempo hasta acercarse a cero; entonces no importa cuán grande sea el valor futuro.

P: ¿Qué es más importante reducir: el esfuerzo de mantenimiento o el de implementación?
R: Es más importante reducir el esfuerzo de mantenimiento que el de implementación.

P: ¿A qué debe ser proporcional el nivel de calidad del diseño?
R: Al tiempo futuro durante el cual el sistema seguirá ayudando a la gente; en la duda, diseña como si fuera a usarse muchísimo tiempo.

P: ¿Cuál es el error más común y desastroso de los programadores?
R: Predecir algo del futuro cuando no pueden conocerlo; lo seguro es diseñar permitiendo el cambio futuro sin adivinar sus detalles.

## Preguntas de autoevaluación

1. ¿Para qué sirve la Ecuación del Diseño de Software y para qué no sirve?
R: Sirve para ordenar las opciones posibles comparando valor y esfuerzo, no para declarar si un cambio es absolutamente correcto o incorrecto. (Sección "La Ecuación del Diseño de Software")

2. Un cambio tiene probabilidad de valor de uno en un millón de salvar una vida. ¿Cómo se describe su valor?
R: Tiene alto valor potencial aunque baja probabilidad de valor, porque cuando ayuda lo hace enormemente. (Sección "Valor")

3. ¿Por qué un cambio que tarda demasiado puede acabar con valor cero?
R: Porque sin usuarios no hay valor inmediato y, si no llega a tiempo, puede no alcanzar a nadie; por eso hay que considerar los calendarios de lanzamiento. (Sección "Valor")

4. En el ejemplo del cambio de $1.000 con $1.000 diarios de valor futuro y $100 diarios de mantenimiento, ¿qué ocurre con el tiempo?
R: A los 10 días los acumulados igualan a los iniciales y a los 1.000 días llegan a $1.000.000 y $100.000, de modo que el valor ahora y el esfuerzo de implementación se vuelven insignificantes. (Sección "Reducción de la ecuación")

5. ¿Por qué es terrible un cambio cuyo esfuerzo de mantenimiento crece mientras el valor cae?
R: Porque el sistema se vuelve infinitamente caro; cualquier situación donde el mantenimiento crezca más rápido que el valor da problemas, aunque al principio parezca aceptable. (Sección "Lo que quieres y lo que no quieres")

6. ¿Qué diferencia hay entre diseñar permitiendo el cambio futuro y predecir el futuro?
R: Diseñar para el cambio usa información conocida del presente para lograr un futuro mejor sin especificar detalles; predecir el futuro es afirmar algo del largo plazo que no se puede conocer. (Sección "Consecuencias imprevisibles")

7. ¿Qué enseña el ejemplo del software de 1985 que arreglaba disquetes?
R: Que depender por completo de un supuesto del futuro ("siempre se usarán disquetes") lleva a la obsolescencia; el largo plazo es mayormente desconocido. (Sección "Consecuencias imprevisibles")

8. ¿Qué son los "principios guía" y qué papel cumplen las leyes del libro?
R: Son reglas que mantienen las cosas funcionando pase lo que pase en un futuro impredecible; las leyes y reglas del libro son esos principios guía. (Sección "Consecuencias imprevisibles")

## Puntos a dominar

- La deseabilidad ordena opciones: valor (ahora + futuro) frente a esfuerzo (implementación + mantenimiento), no verdades absolutas.
- El valor = probabilidad de valor × valor potencial, restando el daño; sin usuarios no hay valor inmediato.
- El esfuerzo abarca todo el tiempo conectado al cambio, no solo programar.
- En plazos largos la ecuación se reduce a valor futuro vs. esfuerzo de mantenimiento.
- Reducir el esfuerzo de mantenimiento importa más que el de implementación; lo ideal es que tienda a cero.
- La calidad del diseño debe ser proporcional al tiempo futuro de utilidad del sistema; en la duda, diseña para el largo plazo y mantén la flexibilidad.
- Nunca predigas el futuro que no puedes conocer; diseña permitiendo el cambio y apóyate en los principios guía del libro.
