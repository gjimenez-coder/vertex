# Decision Analytic Thinking II: Toward Analytical Engineering (Pensamiento analítico para la decisión II: hacia la ingeniería analítica) — Estudio

## Tarjetas de repaso

P: ¿Qué es la ingeniería analítica? / R: Diseñar una solución analítica a un problema de negocio a partir de los datos, las herramientas y las técnicas disponibles.

P: ¿Por qué los problemas de negocio no llegan como problemas limpios de clasificación, regresión o clustering? / R: Son simplemente problemas de negocio; el equipo de datos debe traducirlos a algo que las técnicas conocidas puedan atacar.

P: ¿Cuál es la tesis central del capítulo? / R: El marco de valor esperado descompone un problema de negocio en subproblemas tratables y luego recompone los resultados en la solución del problema original.

P: ¿Cómo se expresa el beneficio esperado de dirigirse a un consumidor x en el mailing benéfico? / R: p(R | x) · vR(x) + (1 − p(R | x)) · vNR(x), donde vR(x) es el valor de responder y vNR(x) el de no responder.

P: ¿Por qué no basta con maximizar el número de donaciones? / R: Porque las donaciones varían (unos \$100, otros \$1); lo que se busca es maximizar el beneficio neto tras costes, no la cantidad de respuestas.

P: ¿Cuál es la regla óptima de targeting en el mailing benéfico? / R: Enviar la solicitud cuando la donación esperada supera el coste: p(R | x) · dR(x) > c.

P: ¿Por qué vR(x) se estima con un modelo entrenado solo con quienes respondieron? / R: Porque la mayoría no responde; así se evita confundir un valor cero por no-respuesta con uno pequeño debido a las características del consumidor.

P: ¿Qué es el sesgo de selección en este contexto? / R: Que los datos no son una muestra aleatoria de la población objetivo, sino de quienes respondieron o fueron seleccionados antes.

P: ¿Cuál es la pregunta clave ante un posible sesgo de selección? / R: Si el procedimiento que sesga los datos influye también en el valor de la variable objetivo.

P: En churn, ¿por qué es un error targetear a quienes tienen mayor p(S | x) · vS(x)? / R: Porque apunta a quienes más probablemente se quedan; se quiere targetear a aquellos donde se perdería más valor si se fueran.

P: ¿Qué expresa la Ecuación 11-1, VT = Δ(p) · uS(x) − c? / R: El valor de targeting: targetear a clientes con mayor cambio en su probabilidad de quedarse ponderado por su valor si se quedan, menos el coste del incentivo.

P: ¿Qué dos modelos de estimación de probabilidad indica construir la descomposición del churn? / R: p(S | x, T) y p(S | x, notT): probabilidad de quedarse si se contacta y si no se contacta.

P: ¿Con qué análisis conecta comparar contactar vs. no contactar (EB_T vs. EB_notT)? / R: Con el análisis causal, que crea una situación contrafactual entre casos tratado y no tratado (ampliado en el Capítulo 12).

P: ¿Qué tres opciones ofrece el marco cuando faltan datos para p(S | x, T)? / R: Simplificar (asumir p = 1), usar una etiqueta proxy, o invertir en datos para generarlos.

P: ¿Qué ejemplo ilustra "invertir en datos" y cómo se gestiona esa inversión? / R: Signet Bank, que asumió pérdidas con ofertas amplias y se convirtió en Capital One; se gestiona con la curva de aprendizaje, abortando si no compensa.

## Preguntas de autoevaluación

P: ¿Por qué el marketing dirigido es un caso de estudio ideal para la ingeniería analítica? / R: Porque muchos negocios comparten su forma (marketing de base de datos, cupones personalizados, ad targeting) y su estructura reaparece en problemas como el churn. (Sección: Targeting the Best Prospects for a Charity Mailing)

P: ¿Cómo permite el marco de valor esperado estimar el beneficio si no hay un método directo para estimarlo? / R: Descomponiendo el beneficio en probabilidad de respuesta (estimación de probabilidad de clase) y valores vR(x)/vNR(x) estimables por regresión, y recomponiendo las piezas. (Sección: El marco de valor esperado: descomponer y recomponer)

P: ¿Por qué la muestra de donantes pasados podría sesgarse hacia quienes donan menos? / R: Porque es razonable pensar que quien dona sumas grandes dona con menos frecuencia, ignorando varias campañas, de modo que aparece poco en los datos. (Sección: Un breve inciso sobre el sesgo de selección)

P: ¿Cuál es el verdadero problema de negocio en churn y qué implica para el modelado? / R: No es retener al máximo de clientes sino perder menos dinero, lo que obliga a incorporar el valor del cliente al razonamiento. (Sección: El ejemplo de churn revisitado con más sofisticación)

P: ¿Qué aporta de nuevo la formulación de churn con EB_T(x) y EB_notT(x)? / R: Considerar qué pasaría si no se contactara (comparar ambos) y la influencia real del incentivo, que es su diferencia. (Sección: Evaluando la influencia del incentivo)

P: ¿Por qué p(S | x, T) plantea un problema de datos y cómo lo hace visible el marco? / R: Es una oferta nueva que nadie ha visto, por lo que no hay datos; el marco hace explícitas las opciones de simplificar, usar proxy o invertir en datos. (Sección: De la descomposición del valor esperado a la solución de data science)

P: ¿Cuál es el objetivo de la ingeniería analítica según el resumen? / R: No cubrir cada contingencia, sino pensar los problemas de forma analítica para que el papel del data mining sea claro y las simplificaciones se hagan consciente y explícitamente. (Sección: Summary)

## Puntos a dominar

- Entender la ingeniería analítica como traducción de un problema de negocio a técnicas conocidas usando datos, herramientas y métodos disponibles.
- Dominar el marco de valor esperado como herramienta para descomponer en subproblemas y recomponer la solución.
- Saber escribir y justificar la regla de targeting del mailing benéfico: p(R | x) · dR(x) > c.
- Explicar por qué vR(x) se entrena solo con quienes respondieron.
- Identificar el sesgo de selección y evaluar si afecta a la variable objetivo.
- Formular el valor de targeting en churn (Ecuación 11-1) y explicar por qué se targetea el mayor cambio en valor esperado, no la mayor retención.
- Relacionar la comparación contactar vs. no contactar con el análisis causal y el Capítulo 12.
- Reconocer las tres estrategias ante falta de datos (simplificar, proxy, invertir) y el papel de la curva de aprendizaje.
- Asumir que las simplificaciones son legítimas solo si se toman consciente y explícitamente.
