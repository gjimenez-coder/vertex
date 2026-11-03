# Code Simplicity: The Fundamentals of Software — Max Kanat-Alexander (O'Reilly Media, 2012)
## Capítulo 4 — The Future (El futuro)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas usan la página del PDF `(PDF p. N)`.

## Lo que necesitas saber

La pregunta central del diseñador de software es cómo tomar decisiones sobre su software. No se trata de qué decisión es absolutamente correcta o incorrecta, sino de ordenar las opciones posibles y elegir la mejor entre muchas. Un diseñador puede tener 100 funcionalidades posibles y capacidad para solo 2: debe saber cuáles priorizar.

El capítulo responde a esa pregunta con la Ecuación del Diseño de Software, que relaciona la deseabilidad de un cambio con su valor y su esfuerzo. Luego introduce el elemento tiempo: todo cambio hay que mantenerlo y su valor se proyecta al futuro. Al razonar sobre plazos largos, la ecuación se reduce prácticamente a comparar el valor futuro frente al esfuerzo de mantenimiento.

Sales sabiendo que es más importante reducir el esfuerzo de mantenimiento que el de implementación, que la calidad del diseño debe ser proporcional al tiempo durante el cual el sistema seguirá ayudando a la gente, y que el error más común y desastroso es predecir el futuro cuando no se puede conocer. La salida es diseñar permitiendo el cambio futuro sin intentar adivinar sus detalles.

## La Ecuación del Diseño de Software

Toda pregunta de este tipo se responde con una ecuación donde:

- **D** = deseabilidad de un cambio (cuánto queremos hacerlo).
- **V** = valor del cambio (cuánto ayuda, normalmente a los usuarios).
- **E** = esfuerzo que implica realizar el cambio.

La deseabilidad es directamente proporcional al valor e inversamente proporcional al esfuerzo. No dice si un cambio es correcto o incorrecto, sino cómo ordenar las opciones: cambios de mucho valor y poco esfuerzo son "mejores" que los de poco valor y mucho esfuerzo. Incluso la pregunta "¿deberíamos quedarnos igual?" se responde comparando el valor y el esfuerzo de no cambiar frente a los de cambiar.

## Valor

La definición más simple de valor es el grado en que un cambio ayuda a alguien en cualquier lugar. Lo más importante es ayudar a los usuarios, pero también es valor sostenerte financieramente como desarrollador. Medir el valor numérico exacto suele ser difícil (ejemplo: cuánto vale ayudar a alguien a perder peso), pero aun así se pueden ordenar los cambios por su valor, apoyándose en la experiencia y en investigar a los usuarios.

El valor se compone de dos factores:

- **Probabilidad de valor**: qué tan probable es que el cambio ayude a un usuario (a cuántos usuarios y con qué frecuencia).
- **Valor potencial**: cuánto ayuda cuando sí ayuda.

Ejemplos: una función que podría salvar una vida con probabilidad de uno en un millón tiene alto valor potencial aunque baja probabilidad; una función que permite a personas ciegas introducir números en una hoja de cálculo afecta a pocos usuarios pero su valor potencial es muy alto; una función que hace sonreír al 100% de los usuarios tiene alta probabilidad de valor con bajo potencial; una con una entre un millón de hacer sonreír tiene ambos factores bajos.

**Balance del daño**: algunos cambios causan daño además de ayudar (p. ej., anuncios que molestan aunque te sostengan). Calcular el valor incluye restar ese daño.

**El valor de tener usuarios**: las funciones sin usuarios no tienen valor inmediato (no se encuentran, son difíciles de usar o no ayudan a nadie). Por eso casi siempre hay que liberar el software para que tenga valor, y un cambio que tarda demasiado puede acabar con valor cero por no llegar a tiempo. Hay que tener en cuenta los calendarios de lanzamiento.

## Esfuerzo

El esfuerzo es más fácil de cuantificar que el valor: suele describirse como cierto número de horas por cierto número de personas (p. ej., "cien persona-años"). Aun así, medirlo en la práctica es muy difícil o imposible, por los costos ocultos como arreglar los bugs que el cambio introduce. Un desarrollador experimentado puede ordenar los cambios por esfuerzo aunque no conozca las cifras exactas. Hay que contar todo el esfuerzo: investigación, comunicación entre desarrolladores y tiempo de reflexión, no solo programar. Todo el tiempo conectado con un cambio es parte de su costo de esfuerzo.

## Mantenimiento y la ecuación completa

Falta el tiempo. Todo cambio requiere mantenimiento (un programa de impuestos debe actualizarse cada año por leyes nuevas), y el valor existe ahora y en el futuro. Algunas funciones pierden valor con el tiempo (entender las leyes fiscales de 2009) y otras lo ganan. Así, el esfuerzo tiene dos componentes y el valor otros dos:

- **Ei**: esfuerzo de implementación.
- **Em**: esfuerzo de mantenimiento.
- **Vn**: valor ahora.
- **Vf**: valor futuro.

La ecuación completa: la deseabilidad de un cambio es directamente proporcional al valor ahora más el valor futuro, e inversamente proporcional al esfuerzo de implementación más el de mantenimiento. Esta es la ley primaria del diseño de software.

## Reducción de la ecuación

Valor futuro y esfuerzo de mantenimiento dependen del tiempo. Con un ejemplo (no usar así en la realidad) de un cambio que cuesta $1.000 implementar, genera $10.000 de inmediato, luego $1.000 diarios de valor futuro y $100 diarios de mantenimiento: a los 10 días el valor futuro y el mantenimiento acumulados ya igualan a los iniciales; a los 1.000 días llegan a $1.000.000 y $100.000, y el valor ahora y el esfuerzo de implementación quedan insignificantes. Con el tiempo la ecuación se reduce a comparar valor futuro contra esfuerzo de mantenimiento. Los sistemas se mantienen tanto tiempo que el valor ahora y el esfuerzo de implementación casi siempre se vuelven insignificantes. (Nota opcional para matemáticos: debe pensarse como una serie infinita con un límite cuando el tiempo tiende a infinito, no como una ecuación estática.)

## Lo que quieres y lo que no quieres

Hay que evitar que el esfuerzo de mantenimiento acabe superando al valor futuro. Un cambio cuyo esfuerzo crece ($10 → $100.000) mientras el valor cae es terrible: el sistema se vuelve infinitamente caro. Cualquier situación donde el mantenimiento crezca más rápido que el valor da problemas, aunque al principio parezca aceptable.

La solución ideal y única garantía de éxito es diseñar sistemas cuyo esfuerzo de mantenimiento disminuya con el tiempo hasta acercarse a cero; entonces no importa cuán grande sea el valor futuro. Un cambio con mantenimiento decreciente se vuelve cada vez más deseable. Teóricamente un cambio es deseable mientras el valor futuro supere siempre al mantenimiento, pero es mejor que el mantenimiento decrezca. Lograrlo suele exigir bastante más esfuerzo de implementación (más diseño y planificación), pero ese esfuerzo casi siempre es insignificante y debe ignorarse en su mayoría. En resumen: es más importante reducir el esfuerzo de mantenimiento que el de implementación. Qué causa el esfuerzo de mantenimiento es el tema de casi todo el resto del libro.

## La calidad del diseño

Es fácil escribir software que ayude a una persona ahora; es mucho más difícil ayudar a millones ahora y durante décadas. Habrá mucho más trabajo de programación y muchos más usuarios en el futuro que en el presente. Ignorar el futuro y hacer cosas que "solo funcionan" ahora produce software difícil de mantener, y por tanto "software malo", lleno de bugs que deja de ayudar.

De ahí la regla: el nivel de calidad del diseño debe ser proporcional al tiempo futuro durante el cual el sistema seguirá ayudando a la gente. Si durará horas, poco diseño; si durará 10 años (ocurre más de lo que uno cree), mucho diseño. En la duda, diseña como si fuera a usarse muchísimo tiempo: no te encierres en un solo método, mantenlo flexible, no tomes decisiones irreversibles y presta mucha atención al diseño.

## Consecuencias imprevisibles

El futuro debe ser el foco principal, pero hay cosas del futuro que no se pueden conocer. El error más común y desastroso de los programadores es predecir algo del futuro cuando no pueden saberlo. Ejemplo: un software de 1985 que arreglaba disquetes y dependía por completo de cómo funcionaban los disquetes quedó obsoleto; el programador predijo "siempre se usarán disquetes". El corto plazo puede ser predecible; el largo plazo es mayormente desconocido y, a la vez, más importante.

Estás más seguro si no intentas predecir el futuro y tomas las decisiones con información conocida del presente. Esto no contradice lo anterior: hay diferencia entre diseñar permitiendo el cambio futuro y predecir el futuro. Analogía: elegir comer en vez de morir de hambre no requiere predecir el futuro; sabes que comer ahora da un mejor mañana sin especificar qué pasará. Igual en diseño: decidimos con información presente para un futuro mejor (menos mantenimiento, más valor) sin predecir detalles. Hay excepciones limitadas para futuros muy cercanos y muy ciertos, pero no es posible predecir el largo plazo. Ejemplo de los CD (1979): nadie pudo prever los DVD del mismo tamaño ni el problema de girar un CD 50 veces más rápido en un CD-ROM. Por eso en toda ingeniería existen "principios guía": reglas que mantienen las cosas funcionando pase lo que pase. Las leyes y reglas de este libro son esos principios. Puedes discrepar y sacar tus propias conclusiones, pero si no las sigues probablemente acabarás en problemas en un futuro que no puedes predecir.

## Ideas clave

- La deseabilidad de un cambio es directamente proporcional a su valor (ahora + futuro) e inversamente proporcional al esfuerzo (implementación + mantenimiento); sirve para ordenar opciones, no para declarar verdades absolutas.
- El valor combina probabilidad de valor (a cuántos y con qué frecuencia) y valor potencial (cuánto cuando ayuda), restando el daño; sin usuarios no hay valor inmediato, así que hay que liberar a tiempo.
- El esfuerzo incluye todo el tiempo conectado con el cambio (investigar, comunicar, pensar), no solo programar, y es difícil de medir aunque se pueda ordenar.
- Con plazos largos la ecuación se reduce a valor futuro frente a esfuerzo de mantenimiento; el valor ahora y el esfuerzo de implementación suelen volverse insignificantes.
- Es más importante reducir el esfuerzo de mantenimiento que el de implementación; lo ideal es que el mantenimiento tienda a cero con el tiempo.
- La calidad del diseño debe ser proporcional al tiempo futuro en que el sistema seguirá ayudando; en la duda, diseña para el largo plazo y mantén la flexibilidad.
- El error más común y desastroso es predecir el futuro cuando no se puede conocer; diseña permitiendo el cambio, no adivinando sus detalles.
- Las leyes y reglas del libro son "principios guía" que producen buen software futuro sin necesidad de predecir ese futuro.
