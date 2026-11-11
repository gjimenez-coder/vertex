# Appendix B. Another Sample Proposal (Apéndice B. Otra propuesta de ejemplo) — Estudio

## Tarjetas de repaso

P: ¿Qué papel asume el lector en el escenario del apéndice? / R: El de responsable de un equipo analítico en Green Giant Consulting (GGC) que revisa una propuesta de ciencia de datos antes de presentarla al cliente, buscando fallos y mejoras.

P: ¿Qué empresa es el cliente y cuál es su problema? / R: TelCo, el segundo mayor proveedor de comunicaciones inalámbricas del país, con un problema de fuga de clientes (churn).

P: ¿Cuál es el problema de modelado planteado en la propuesta? / R: Estimar la probabilidad de que un cliente abandone (o no) en los 90 días siguientes a la expiración del contrato.

P: ¿Con qué antelación se predeciría la probabilidad de churn y por qué? / R: Con datos de 45 días antes de la expiración del contrato, para dar a TelCo tiempo suficiente de influir con una oferta de incentivo.

P: ¿Qué técnica elige la propuesta y cómo la justifica? / R: Un ensemble de árboles (random forest), "conocido por tener alta precisión para una amplia variedad de problemas de estimación".

P: ¿Por qué es un error entrenar solo con "clientes que han dejado la compañía"? / R: Porque también se necesitan clientes que no se fueron (ejemplos negativos) para que el modelado encuentre información discriminativa.

P: ¿Por qué es preferible ordenar por pérdida esperada en vez de por probabilidad de churn? / R: Porque un cálculo estándar de valor esperado prioriza mejor a los clientes según su impacto económico, no solo según su probabilidad de irse.

P: ¿A quién sería ideal modelar según la crítica, más allá de quién se irá? / R: A los clientes con más probabilidad de ser influidos positivamente por el incentivo.

P: ¿Qué problema de datos aparece si se modela la respuesta al incentivo? / R: Que no se dispone de los datos de entrenamiento necesarios y habría que invertir en obtenerlos.

P: ¿Por qué no basta "ejecutar el modelo sobre la base de datos" para medir el rendimiento? / R: Porque probar sobre el conjunto de entrenamiento no mide la generalización; hace falta una evaluación con datos reservados (holdout).

P: ¿Por qué una tasa de verdaderos positivos del 70% es ambigua por sí sola? / R: Porque sin la tasa de falsos positivos se podría identificar el 100% diciendo que todos se irán; la de verdaderos positivos solo tiene sentido junto a la de falsos positivos.

P: ¿Qué defecto presenta elegir un único modelo de antemano? / R: Que con las herramientas modernas es fácil comparar varios modelos sobre los mismos datos, y conviene hacerlo en lugar de fijar uno.

P: ¿Qué conflicto genera el random forest frente a la validación de la V.P. de Retención? / R: Es un modelo de caja negra, y ella necesita entender si el procedimiento "tiene sentido"; a veces compensa sacrificar precisión por comprensibilidad.

P: ¿Cómo funciona la operación semanal propuesta? / R: Cada semana se ejecuta el modelo para clientes cuyo contrato expira en 45 días (±1 semana), se ordenan por probabilidad y se selecciona el top N para el incentivo, según coste y presupuesto.

P: ¿Cómo plantea el apéndice el uso del libro completo? / R: Como una guía de revisión de propuestas: cada fallo remite a los capítulos que explican el principio incumplido.

## Preguntas de autoevaluación

P: ¿Por qué entrenar únicamente con clientes que se marcharon invalida el modelado? / R: Porque sin ejemplos de clientes que se quedaron no hay con qué contrastar, y el modelo no puede hallar la información discriminativa que separa a quienes se van de quienes no. (Sección "Fallos en la propuesta de GGC", punto 1)

P: ¿Qué secuencia de mejoras propone la crítica para decidir a quién dirigir el incentivo? / R: Pasar de ordenar por probabilidad de churn, a ordenar por pérdida esperada (valor esperado), y finalmente a modelar a quién influye positivamente el incentivo, lo que exigiría obtener nuevos datos de entrenamiento. (Sección "Fallos en la propuesta de GGC", puntos 2, 3 y 4)

P: ¿Qué falla en cómo la propuesta pretende verificar su rendimiento? / R: No evalúa la generalización con datos reservados (holdout) y sugiere probar sobre el conjunto de entrenamiento, por lo que la cifra no sería fiable. (Sección "Fallos en la propuesta de GGC", punto 5)

P: ¿Qué respaldo falta para la afirmación de identificar el 70% de los clientes que se irán? / R: No se menciona ningún estudio piloto previo, ni curvas de aprendizaje sobre muestras de datos, ni otro respaldo; parece una conjetura. (Sección "Fallos en la propuesta de GGC", punto 7)

P: ¿Por qué no se puede interpretar "identificar el 70%" sin la tasa de falsos positivos? / R: Porque sin hablar de falsos positivos y falsos negativos se podría identificar el 100% diciendo que todos se irán; la tasa de verdaderos positivos solo tiene sentido junto a la de falsos positivos. (Sección "Fallos en la propuesta de GGC", punto 8)

P: ¿Qué omisión hay respecto a los atributos del modelo y por qué importa? / R: La propuesta no define ni menciona qué atributos se usarán, lo que sugiere que podría ser una omisión o que el equipo no lo ha pensado ni tiene plan. (Sección "Fallos en la propuesta de GGC", punto 6)

P: ¿Por qué el random forest entra en conflicto con la validación de la V.P. de Retención? / R: Porque ella aprobará el procedimiento examinando si "tiene sentido" (validación con conocimiento del dominio), pero los ensembles de árboles son cajas negras; sería mejor sacrificar algo de precisión por comprensibilidad y, una vez convencida, usar modelos menos comprensibles para mayor precisión. (Sección "Fallos en la propuesta de GGC", punto 10)

P: ¿Cómo se relaciona este apéndice con el Apéndice A y el Capítulo 13? / R: Es el complemento práctico del Apéndice A (guía de revisión de propuestas) y retoma el ejercicio del Capítulo 13, aplicando ahora los fundamentos al caso de churn en telecomunicaciones. (Sección "Lo que necesitas saber")

## Puntos a dominar

- Reconocer que todo modelo de clasificación necesita ejemplos positivos y negativos para hallar información discriminativa (Cap. 2, 3, 4, 7).
- Distinguir entre ordenar por probabilidad, ordenar por pérdida/valor esperado y modelar la respuesta al incentivo (Cap. 7, 11, 12).
- Exigir evaluación de generalización con datos reservados (holdout) y no probar sobre el conjunto de entrenamiento (Cap. 5).
- Interpretar la tasa de verdaderos positivos siempre junto a la de falsos positivos (Cap. 7, 8).
- Pedir respaldo empírico (piloto, curvas de aprendizaje) para cualquier cifra de rendimiento prometida (Cap. 2, 5, 7).
- Comparar varios modelos en vez de fijar uno de antemano (Cap. 4, 7, 8).
- Equilibrar precisión y comprensibilidad según las necesidades de validación del negocio; evitar cajas negras cuando el dominio exige entender el modelo (Cap. 3, 7, 12).
- Usar los fundamentos de la ciencia de datos como lista de comprobación para revisar propuestas analíticas.
