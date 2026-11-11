# Data Science for Business — Foster Provost & Tom Fawcett (O'Reilly, 2013)
## Capítulo 16 — Appendix B. Another Sample Proposal (Apéndice B. Otra propuesta de ejemplo)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas usan la página del PDF `(PDF p. N)`.

## Lo que necesitas saber
Este apéndice es el complemento práctico del Apéndice A (guía de revisión de propuestas) y retoma el ejercicio del Capítulo 13, donde se analizaba una propuesta de "migración de clientes" con sus defectos. Aquí se presenta una segunda propuesta de ejemplo, esta vez construida sobre el problema de la fuga de clientes (churn) en telecomunicaciones, el caso que ha servido de hilo conductor a todo el libro.

La idea es ponerte en el papel de quien revisa una propuesta de ciencia de datos antes de presentarla al cliente. Se expone un escenario ficticio, el texto íntegro de la propuesta y, a continuación, una crítica numerada que identifica sus errores más graves. Cada fallo remite a los capítulos del libro donde se tratan los principios que lo explican.

Lo que sales sabiendo: aplicar los fundamentos de la ciencia de datos como lista de comprobación para detectar debilidades en un plan analítico —desde cómo se definen los datos de entrenamiento hasta cómo se evalúa la generalización, se mide el valor esperado y se atiende a la comprensibilidad del modelo frente a las necesidades del negocio.

## Escenario y propuesta
Trabajas como responsable de un equipo analítico en Green Giant Consulting (GGC), que apenas empieza a desarrollar sus capacidades de ciencia de datos. GGC propone un proyecto a TelCo, el segundo mayor proveedor de comunicaciones inalámbricas del país, para atacar su problema de churn. Tu equipo ha producido una propuesta y tú debes revisarla antes de presentarla al cliente, buscando fallos y mejoras.

La propuesta, titulada "Churn Reduction via Targeted Incentives — A GGC Proposal", plantea lo siguiente:

- Idea central: TelCo puede usar datos de comportamiento de clientes para predecir cuándo se irán y así dirigirles incentivos especiales para que se queden.
- Problema de modelado: estimar la probabilidad de que un cliente abandone (o no) en los 90 días siguientes a la expiración del contrato. Se reconoce que retener a clientes que siguen mes a mes tras la expiración es un problema aparte, y que esta ventana de 90 días es un punto de partida apropiado.
- El modelo se construiría sobre una base de datos de casos históricos de clientes que han dejado la compañía. La probabilidad de churn se predeciría con datos de 45 días antes de la expiración del contrato, para dar a TelCo tiempo suficiente de influir con una oferta de incentivo.
- Técnica elegida: un ensemble de árboles (random forest), "conocido por tener alta precisión para una amplia variedad de problemas de estimación".
- Afirmación de rendimiento: se estima poder identificar el 70% de los clientes que se irán en la ventana de 90 días, verificándolo ejecutando el modelo sobre la propia base de datos.
- Validación: la V.P. de Retención de Clientes debe dar el visto bueno; decidirá según su propia valoración de que el procedimiento tiene sentido y según la opinión de expertos de la firma, a quienes se dará acceso al modelo.
- Operación: cada semana se ejecutaría el modelo para estimar la probabilidad de churn de los clientes cuyo contrato expira en 45 días (más o menos una semana), se les ordenaría por probabilidad y se seleccionaría el top N para recibir el incentivo, con N según el coste del incentivo y el presupuesto semanal de retención.

## Fallos en la propuesta de GGC
La crítica usa los principios fundamentales de la ciencia de datos para detectar los errores. El Apéndice A sirve de guía inicial, pero el libro entero puede verse como una guía de revisión de propuestas. Los fallos más graves, con sus remisiones a capítulos:

1. La propuesta solo menciona modelar a partir de "clientes que han dejado la compañía". Para entrenar (y probar) también se necesitan clientes que no se fueron, de modo que el modelado encuentre información discriminativa. (Cap. 2, 3, 4, 7)

2. ¿Por qué ordenar a los clientes por mayor probabilidad de churn? ¿Por qué no ordenarlos por pérdida esperada, mediante un cálculo estándar de valor esperado? (Cap. 7, 11)

3. Mejor aún: ¿no deberíamos modelar a los clientes con más probabilidad de ser influidos positivamente por el incentivo? (Cap. 11, 12)

4. Si se procede como en (3), aparece el problema de no disponer de los datos de entrenamiento necesarios: habría que invertir en obtenerlos. (Cap. 3, 11)

La propuesta actual podría ser solo un primer paso hacia el objetivo de negocio, pero esto debería explicitarse: ver si se pueden estimar bien las probabilidades; si se logra, tiene sentido continuar, y si no, convendría replantear la inversión en el proyecto.

5. No dice nada sobre evaluar el rendimiento de generalización (una evaluación con datos reservados, holdout). Suena a que van a probar sobre el conjunto de entrenamiento ("ejecutar el modelo sobre la base de datos"). (Cap. 5)

6. No define ni menciona qué atributos se van a usar. ¿Es una omisión? ¿O es que el equipo ni lo ha pensado? ¿Cuál es el plan? (Cap. 2, 3)

7. ¿Cómo estima el equipo que el modelo identificará el 70% de los clientes que se irán? No se menciona ningún estudio piloto previo, ni curvas de aprendizaje sobre muestras de datos, ni ningún otro respaldo. Parece una conjetura. (Cap. 2, 5, 7)

8. Además, sin hablar de la tasa de error ni de los falsos positivos y falsos negativos, no queda claro qué significa "identificar el 70% de los que se irán". Si no digo nada sobre la tasa de falsos positivos, puedo identificar el 100% simplemente diciendo que todos se irán. Hablar de la tasa de verdaderos positivos solo tiene sentido si también se habla de la de falsos positivos. (Cap. 7, 8)

9. ¿Por qué elegir un único modelo? Con las herramientas modernas es fácil comparar varios modelos sobre los mismos datos. (Cap. 4, 7, 8)

10. La V.P. de Retención debe aprobar el procedimiento y examinará si "tiene sentido" (validación con conocimiento del dominio). Pero los ensembles de árboles son modelos de caja negra, y la propuesta no explica cómo va a entender ella cómo toma sus decisiones. Dado su deseo, sería mejor sacrificar algo de precisión por un modelo más comprensible; una vez que esté convencida, podrían usarse técnicas menos comprensibles para lograr mayor precisión. (Cap. 3, 7, 12)

## Ideas clave
- Entrenar solo con clientes que se fueron impide hallar información discriminativa: hacen falta también ejemplos negativos (clientes que se quedaron).
- Ordenar por probabilidad de churn es inferior a ordenar por pérdida esperada, y lo ideal es modelar a quién influye positivamente el incentivo (no solo quién se irá).
- Pasar a modelar la respuesta al incentivo exige datos de entrenamiento que probablemente haya que obtener invirtiendo en ello.
- Sin evaluación con datos reservados (holdout), probar sobre el conjunto de entrenamiento no mide la generalización; la cifra del 70% carece de respaldo (piloto o curvas de aprendizaje).
- Una tasa de verdaderos positivos solo es interpretable junto a la de falsos positivos: sin ella, "identificar el 70%" es ambiguo.
- Conviene comparar varios modelos en lugar de fijar uno de antemano; las herramientas modernas lo facilitan.
- Si quien valida necesita comprender el procedimiento, un modelo de caja negra (random forest) choca con esa necesidad: a veces compensa sacrificar precisión por comprensibilidad.
- El libro entero funciona como guía de revisión de propuestas: cada fallo remite a los capítulos que explican el principio incumplido.
