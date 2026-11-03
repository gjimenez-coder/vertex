# Capítulo 9 — Testing (Pruebas) — Estudio

## Tarjetas de repaso

- P: ¿Qué enuncia la Ley de las Pruebas (Law of Testing)? / R: El grado en el que sabes cómo se comporta tu software es el grado en el que lo has probado con precisión.
- P: ¿De qué sí hay certeza y de qué no, respecto a que un programa funcione? / R: Solo hay certeza de que funciona ahora; no hay certeza de que vaya a funcionar en el futuro.
- P: ¿Qué regla práctica se deriva de la Ley de las Pruebas? / R: A menos que lo hayas probado, no sabes que funciona.
- P: ¿Qué aspectos combina el "grado" de prueba? / R: Cuántos aspectos del software has probado, qué tan recientemente y en cuántos entornos distintos.
- P: ¿Qué efecto tiene la antigüedad de una prueba sobre la certeza? / R: Cuanto más reciente sea la prueba, más probable es que el software siga funcionando.
- P: ¿Qué significa realmente que el software "funciona"? / R: Que se comporta como lo pretendías, por lo que antes debes saber qué comportamiento pretendías.
- P: ¿Cómo describe el autor la naturaleza de cada prueba? / R: Cada prueba es una pregunta muy precisa que espera una respuesta muy específica.
- P: ¿Qué información mínima puede dar una prueba cuando un comportamiento es muy difícil de probar? / R: Preguntar "si el usuario hace esto, ¿se cae el programa?" y esperar la respuesta "No".
- P: ¿Qué significa que una prueba sea precisa (accurate)? / R: Que no diga que el programa se comporta bien cuando no es así, ni que está roto cuando en realidad funciona.
- P: ¿Qué requisito, además de la precisión, debe cumplir una buena prueba? / R: Observar los resultados: si falla, debe haber forma de saber que falló y específicamente cómo falló.
- P: ¿Por qué es fácil olvidar probar? / R: Escribimos código, lo guardamos y olvidamos comprobar si de verdad funciona.
- P: ¿Bastan las demostraciones matemáticas de corrección para saber que el código funciona? / R: No; no sabes que funciona hasta que realmente has intentado usarlo.
- P: ¿Qué ocurre con tu conocimiento de una pieza cuando la cambias? / R: Dejas de saber que esa pieza funciona y que las piezas conectadas siguen funcionando; hay que volver a probar.
- P: ¿Cuál es la respuesta moderna para no probar todo manualmente tras cada cambio? / R: Crear pruebas automatizadas para cada pieza de código y ejecutarlas tras cada cambio.
- P: ¿Qué explica exactamente la Ley de las Pruebas y qué no? / R: Explica por qué, cuándo y qué información dan las pruebas; no explica cómo escribir pruebas automatizadas.

## Preguntas de autoevaluación

- P: ¿Por qué el autor afirma que no puedes estar seguro de que un programa funcionará en el futuro? / R: Porque aunque lo hayas ejecutado una vez puede no volver a ejecutarse: el entorno puede cambiar a su alrededor o puede que lo corras en otra máquina y ya no funcione. (Sección "Lo que necesitas saber")
- P: ¿Por qué decir simplemente que el software "funciona" es insuficiente para una prueba? / R: Porque "funciona" es vago; lo que realmente sabes es que se comporta como pretendías, así que debes definir el comportamiento pretendido. (Sección "Qué significa 'funciona'")
- P: Da un ejemplo del capítulo de pregunta precisa y respuesta específica de una prueba. / R: "¿Qué pasa cuando un usuario pulsa este botón como primera acción tras arrancar la aplicación por primera vez?" con respuesta esperada "La aplicación muestra una ventana que dice 'Hello, World!'". (Sección "Qué significa 'funciona'")
- P: ¿Cuáles son los dos requisitos de una buena prueba según el capítulo? / R: Que sea precisa (accurate) y que sus resultados se observen, de modo que si falla sepas que falló y cómo. (Sección "Requisitos de una buena prueba")
- P: ¿Por qué un cambio pequeño puede obligar a volver a probar todo el programa? / R: Porque al cambiar una pieza dejas de saber que funciona, y como está conectada con muchas otras tampoco sabes si esas siguen funcionando; si el cambio es grande, hay que reprobar todo. (Sección "Por qué se olvida probar")
- P: ¿Qué ventaja ofrecen las pruebas automatizadas frente a la prueba manual? / R: Permiten ejecutarse justo después de cualquier cambio y comprueban cada pieza del sistema para asegurar que todo sigue funcionando tras cada cambio individual. (Sección "Pruebas automatizadas")
- P: ¿Qué alcance tiene la Ley de las Pruebas respecto a la técnica de pruebas? / R: Solo explica por qué, cuándo y qué información dan las pruebas; el cómo escribirlas está muy bien cubierto en Internet y libros. (Sección "Pruebas automatizadas")

## Checklist

- Antes de probar, define qué comportamiento pretendías para la pieza de código.
- Formula cada prueba como una pregunta precisa con una respuesta específica esperada.
- Asegúrate de que la prueba sea precisa (no dé falsos positivos ni falsos negativos).
- Observa y registra los resultados: si falla, confirma que puedes saber que falló y cómo.
- Evalúa el "grado" de prueba: cuántos aspectos, qué tan reciente y en cuántos entornos.
- Tras cada cambio, vuelve a probar la pieza modificada y las piezas conectadas.
- Crea pruebas automatizadas para cada pieza de código y ejecútalas después de cada cambio.
