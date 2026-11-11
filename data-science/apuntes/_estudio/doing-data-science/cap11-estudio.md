# Capítulo 11 — Causality (Causalidad) — Estudio

## Tarjetas de repaso

- P: ¿En qué se diferencia el objetivo de este capítulo del resto del libro? / R: El resto se centra en la predicción (precisión, sin importar el significado de las variables); aquí el objetivo es aislar causas y afirmar que un comportamiento provoca un resultado.
- P: ¿Qué significa que correlación no implica causalidad? / R: Que dos variables estén asociadas (p. ej. helado y bañadores) no implica que una cause la otra; puede haber un tercer factor (el calor) que cause ambas.
- P: ¿Cómo se formula la forma natural de una pregunta causal? / R: ¿Cuál es el efecto de x sobre y?, es decir, el efecto del tratamiento (treatment) sobre el resultado (outcome).
- P: ¿Qué es un confusor (confounder)? / R: Una variable que tiene efecto causal a la vez sobre el tratamiento y sobre el resultado; es la raíz de confundir correlación con causalidad.
- P: En el ejemplo de OK Cupid, ¿por qué la mujer guapa es un confusor? / R: Porque afecta a la vez al tratamiento (que Frank use "beautiful") y al resultado (que ella responda).
- P: ¿Por qué el gráfico de OK Cupid no respalda el consejo "evita los cumplidos físicos"? / R: Es un estudio observacional, no un experimento; además la palabra puede decir más de quien la usa, la gente puede autodescribirse y las destinatarias pueden ser especiales (reciben muchos emails y responden a pocos).
- P: ¿Cuál es el patrón oro para establecer causalidad y por qué funciona? / R: El experimento aleatorizado: asigna al azar tratamiento y control, creando poblaciones estadísticamente idénticas que equilibran confusores conocidos y los "50 millones de cosas en las que no pensamos".
- P: ¿Qué es el equilibrio clínico (clinical equipoise)? / R: La condición ética para un ensayo aleatorizado: la comunidad médica no sabe qué tratamiento es mejor.
- P: ¿Qué son las pruebas A/B? / R: El nombre de los experimentos aleatorizados en empresas de software: se muestran versiones distintas del producto (color, diseño o algoritmo) para medir el impacto con métricas.
- P: ¿Qué es la paradoja de Simpson? / R: Que una tendencia presente en subgrupos puede desaparecer o invertirse al combinarlos, como en el ejemplo del "mal fármaco" al separar por consumo de aspirina.
- P: En el modelo causal de Rubin, ¿qué representan Zi, Yi1 e Yi0? / R: Zi es el tratamiento de la unidad i (0 = control, 1 = tratamiento), Yi1 la respuesta si Zi = 1 e Yi0 la respuesta si Zi = 0.
- P: ¿Cuál es el problema fundamental de la inferencia causal? / R: El efecto causal individual Yi1 − Yi0 es incognoscible porque solo observamos uno de los dos resultados por unidad; a nivel poblacional sí se puede inferir.
- P: ¿Qué son W, A e Y en un grafo causal? / R: W es el conjunto de posibles confusores, A el tratamiento (binario 0/1) e Y el resultado binario; las aristas dirigidas indican causalidad.
- P: ¿En qué consiste el emparejamiento por puntaje de propensión (propensity score matching)? / R: Crear un grupo de control sintético con personas que tenían la misma probabilidad de recibir el tratamiento pero no lo recibieron, usando regresión logística para estimar esa probabilidad (puntaje de propensión).
- P: ¿Qué limitación inherente tiene el puntaje de propensión? / R: Nunca sabremos si ajustamos por todos los confusores necesarios.

## Preguntas de autoevaluación

- P: ¿Por qué la eficacia de la publicidad suele considerarse imposible de medir y qué mala práctica provoca? / R: Porque estimar parámetros causales es muy difícil; la gente elige métricas fáciles de estimar que no miden lo que quieren y decide con ellas igualmente, p. ej. premiar a los marketers por vender a quien iba a comprar de todos modos. (Sección "Correlación no implica causalidad")
- P: ¿Qué cifras dio OK Cupid sobre la palabra "beautiful" y qué regla dedujo? / R: La tasa media de respuesta era ~32%, pero P(respuesta | "beautiful") = 0,22 frente a P(respuesta) = 0,32; de ahí dedujeron "evita los cumplidos físicos". (Sección "Confusores: el ejemplo de las citas (Frank)")
- P: ¿Por qué se aleatoriza al azar y no buscando algorítmicamente la mejor partición? / R: Porque la aleatorización equilibra no solo los confusores que se nos ocurren, sino también todos los que no pensamos; buscar la mejor partición solo equilibraría los conocidos. (Sección "El patrón oro: ensayos clínicos aleatorizados")
- P: ¿Qué riesgo aparece cuando varios equipos lanzan pruebas A/B a la vez sin coordinarse? / R: Un mismo usuario puede acabar en varios tratamientos simultáneos y atribuir el efecto a uno solo. (Sección "El promedio frente al individuo y las pruebas A/B")
- P: ¿Qué supuesto clave de la aleatorización se rompe en la era de las redes sociales? / R: El supuesto de que los usuarios son independientes; hay que tener en cuenta la estructura de red, y es un problema abierto. (Sección "El promedio frente al individuo y las pruebas A/B")
- P: En el ejemplo del "mal fármaco", ¿por qué la recta original sigue siendo útil pese a la paradoja de Simpson? / R: Como modelo predictivo sigue siendo lo mejor sin conocer la aspirina; el problema surge solo al querer asignar causalidad. (Sección "Segundo mejor: estudios observacionales y la paradoja de Simpson")
- P: ¿Cómo se define el efecto causal en el ejemplo de las 100 personas y el cáncer? / R: Si 30 de 100 desarrollan cáncer (0,30) y "jugando a ser Dios" sin fármaco habrían sido 20 (0,20), el efecto causal es la diferencia: 10% (a veces se define como el cociente). (Sección "Definir el efecto causal y el puntaje de propensión")
- P: ¿Cuáles son los tres consejos de Ori Stitelman? / R: (1) Entender cómo se generaron los datos y sus distribuciones, lo que exige conocimiento del dominio; (2) dar un paso atrás y escribir con cuidado qué quieres saber, y comprobar cuánto te acercaste; (3) no ignorar la intuición de datos: que un método converja no significa que el resultado sea significativo. (Sección "Tres consejos de Ori Stitelman")

## Puntos a dominar

- Distinguir el objetivo de predecir del de entender causalidad, aunque usen herramientas parecidas (regresión).
- Reconocer un confusor e identificar por qué invalida pasar de correlación a causalidad.
- Explicar por qué el experimento aleatorizado es el patrón oro y qué lo limita (equilibrio clínico, coste, viabilidad).
- Entender las pruebas A/B como experimentos aleatorizados en software y sus dificultades prácticas (coordinación, independencia de usuarios).
- Detectar la paradoja de Simpson con el ejemplo del "mal fármaco" y la aspirina.
- Manejar el modelo causal de Rubin (Zi, Yi1, Yi0) y el problema fundamental de la inferencia causal.
- Describir los grafos causales (W, A, Y) y el emparejamiento por puntaje de propensión con su limitación inherente.
