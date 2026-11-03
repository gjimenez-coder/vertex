# Code Simplicity: The Fundamentals of Software — Max Kanat-Alexander (O'Reilly Media, 2012)
## Capítulo 9 — Testing (Pruebas)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas usan la página del PDF.

## Lo que necesitas saber

Este capítulo corto defiende por qué, cuándo y qué información nos dan las pruebas. El punto de partida es que no existe certeza de que un programa vaya a funcionar en el futuro: solo hay certeza de que está funcionando ahora. Aunque lo hayas ejecutado una vez, puede que no vuelva a ejecutarse; el entorno puede cambiar a su alrededor o puede que lo corras en otra máquina y ya no funcione.

Frente a esa incertidumbre, el autor propone la Ley de las Pruebas (Law of Testing): «El grado en el que sabes cómo se comporta tu software es el grado en el que lo has probado con precisión» (PDF p. 81). De ahí sale una regla práctica: a menos que lo hayas probado, no sabes que funciona. Sales sabiendo que probar no es un trámite opcional, sino la única fuente real de conocimiento sobre el comportamiento del software, y entendiendo qué significa realmente ese "grado" de prueba.

## El "grado" de prueba

El "grado" de prueba combina varios aspectos: cuántos aspectos del software has probado, qué tan recientemente lo has hecho y en cuántos entornos distintos. Cuanto más reciente sea la prueba, más probable es que el software siga funcionando. Cuantos más entornos hayas probado, más certeza tienes de que funciona en esas circunstancias.

## Qué significa "funciona"

Decir que el software "funciona" es vago. Lo que realmente sabes al probar es que el software se comporta como pretendías. Por tanto, debes saber qué comportamiento pretendías, algo que puede parecer obvio pero es crítico en las pruebas.

Cada prueba exige una pregunta muy precisa y espera una respuesta muy específica. El ejemplo del capítulo: "¿Qué pasa cuando un usuario pulsa este botón como primera acción tras arrancar la aplicación, cuando nunca se había arrancado antes?", con una respuesta concreta esperada, como "La aplicación muestra una ventana que dice 'Hello, World!'". Si obtienes otra respuesta, el software "no funciona".

A veces un comportamiento es muy difícil de probar y solo puedes preguntar "si el usuario hace esto, ¿se cae el programa?" y esperar la respuesta "No". Pero con software bien diseñado, en la mayoría de situaciones, puedes obtener información mucho más específica que eso.

## Requisitos de una buena prueba

- Las pruebas deben ser precisas (accurate). Si te dicen que el programa se comporta bien cuando no es así, o que está roto cuando en realidad funciona, son pruebas inexactas.
- Debes observar los resultados para que las pruebas sean válidas. Si fallan, tiene que haber alguna forma de que sepas que fallaron y específicamente cómo fallaron.

## Por qué se olvida probar

Probar es fácil de pasar por alto: escribimos código, lo guardamos y olvidamos comprobar si de verdad funciona. Pero por muy brillante que seas como programador, y por muchas demostraciones matemáticas que hagas de que tu código es correcto, no sabes que funciona hasta que realmente has intentado usarlo.

Además, en cuanto cambias una pieza del software, dejas de saber que esa pieza funciona: hay que probarla de nuevo. Y como esa pieza suele estar conectada con muchas otras, tampoco sabes si esas otras siguen funcionando. Si el cambio es suficientemente grande, puede que tengas que volver a probar todo el programa.

## Pruebas automatizadas

Obviamente no quieres probar manualmente todo el programa cada vez que haces un cambio diminuto. Por eso, en la actualidad, los desarrolladores suelen aplicar esta ley creando pruebas automatizadas para cada pieza de código que escriben. La ventaja es que pueden ejecutar las pruebas justo después de cualquier cambio, y esas pruebas automatizadas comprueban cada pieza del sistema para asegurar que todo sigue funcionando tras cada cambio individual.

El autor señala que hay mucha información en Internet y en libros sobre cómo escribir pruebas automatizadas y sobre pruebas en general: es un área muy bien cubierta y vale la pena leer sobre ella. La Ley de las Pruebas solo explica por qué debemos probar, cuándo debemos probar y qué información nos dan realmente las pruebas.

## Ideas clave

- Ley de las Pruebas: el grado en que conoces el comportamiento de tu software es el grado en que lo has probado con precisión.
- No hay certeza de que un programa funcione en el futuro, solo de que funciona ahora; a menos que lo pruebes, no sabes que funciona.
- El "grado" de prueba combina cuántos aspectos, qué tan reciente y en cuántos entornos has probado.
- "Funciona" significa que el software se comporta como lo pretendías; cada prueba es una pregunta precisa con una respuesta específica esperada.
- Las pruebas deben ser precisas y sus resultados deben observarse (saber si fallaron y cómo).
- Cambiar una pieza invalida lo que sabías de ella y de las piezas conectadas; hay que volver a probar.
- La respuesta moderna es crear pruebas automatizadas para cada pieza y ejecutarlas tras cada cambio.
