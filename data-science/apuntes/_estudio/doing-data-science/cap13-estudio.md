# Capítulo 13 — Lessons Learned from Data Competitions: Data Leakage and Model Evaluation — Estudio

## Tarjetas de repaso

P: Según Perlich, ¿cuál es la habilidad más importante y difícil de enseñar de un data scientist? / R: Entender los datos y el dominio, es decir, saber cómo se generaron los datos (el *data generating process*).

P: ¿Qué es la *data leakage* (fuga de datos)? / R: Información que ayuda a predecir pero cuyo uso no es legítimo porque no estaría disponible en el momento real de la predicción; a menudo es un artefacto de invertir causa y efecto.

P: ¿Qué señal inequívoca de leakage mencionan Pyle y Perlich? / R: Un rendimiento "too good to be true" (por ejemplo, un AUC cercano a 1), como el AUC de 0.999 en la predicción del S&P.

P: ¿Por qué "Free Shipping = True" produjo leakage en el caso de Amazon? / R: El envío gratis es un *efecto* de gastar mucho (se ofrece tras superar cierto umbral) y es simultáneo a la venta, no un dato previo legítimo.

P: ¿Qué provocó que `sum(revenue) = 0` predijera perfectamente a los compradores de joyas? / R: Un problema de muestreo: al preparar los datos se quitaron las compras de joyería pero solo se incluyó a quien había comprado algo, y esos clientes solo habían comprado joyas.

P: ¿Por qué el *patient ID* tenía poder predictivo en el caso de cáncer de mama? / R: Porque se mezclaron bases de datos de distintos centros, algunos con pacientes más enfermos; renumerar y aleatorizar no basta, hay que saber para qué se usará el modelo.

P: ¿Qué diferencia una competición "sterile" de una "real world"? / R: La "sterile" entrega una matriz limpia y un error estándar (problema puro de ML donde ganan algoritmos y ensembles); la "real world" da datos crudos en varias tablas y exige montar el modelo y definir evaluaciones de la tarea.

P: ¿Qué cuatro consejos da Perlich para evitar la fuga de datos? / R: Aplicar un corte temporal estricto, poner timestamp del momento en que aprendiste el dato, evitar quitar columnas y filas (empezar de cero con datos crudos) y saber cómo se crearon los datos.

P: ¿Por qué la accuracy es una mala métrica? / R: No sirve para regresión y, con clases desbalanceadas, un modelo tonto ("di siempre 1") puede ser muy accurate y a la vez malo.

P: ¿Qué dos aspectos propone Perlich evaluar por separado y con qué herramientas? / R: El *ranking* (curva ROC/AUC y lift curve) y la *calibración* (buckets de probabilidad predicha frente a la empírica).

P: ¿Por qué los árboles de decisión calibran mal y la regresión logística mejor? / R: Los árboles optimizan la *pureza* y dan predicciones más extremas que la realidad; la regresión logística calibra mejor.

P: ¿Qué es el overfitting y cómo se combate? / R: Encontrar patrones que no generalizan ("si buscas lo suficiente, encontrarás algo"); se combate con cross-validation y reduciendo la complejidad del modelo (p. ej. árboles podados).

P: ¿Cómo se descompone el valor esperado de donación en el ejemplo de la campaña de caridad? / R: E[$ | person] = P(response = "yes" | person) · E[$ | response = "yes", person], modelando por separado si la persona dona y cuánto dona.

P: ¿Cómo se elige la métrica según los datos? / R: La suma de errores al cuadrado es la pérdida de máxima verosimilitud si los datos son normales; para la mediana se usan errores absolutos; para un cuantil, error absoluto ponderado.

## Preguntas de autoevaluación

P: ¿Por qué un AUC de 0.999 al predecir el S&P delata fuga de datos en lugar de un buen modelo? / R: Porque los mercados son casi aleatorios, así que ese valor indica que alguna variable del dataset era muy predictiva pero no estaría disponible en tiempo real. (Sección "Data Leakage")

P: Explica el warning sobre el muestreo de un solo día de tráfico. / R: Sobrerepresenta a los usuarios frecuentes: en el ejemplo de 80 usuarios, los 10 diarios aparecen siempre y suponen el 50% de la muestra diaria siendo solo el 12.5% de la base. (Sección "Data Leakage")

P: ¿Qué significa "Leakage happens" y por qué es peligroso aunque no la busques? / R: Aunque no explotes la fuga a propósito, el modelo lo hará por ti, y ganar por leakage es más fácil que construir buenos modelos. (Sección "Data Leakage")

P: ¿Por qué importan las probabilidades y no los 0 y 1 en la evaluación? / R: Porque nadie decide sobre el resultado binario; se quiere la probabilidad (p. ej. de tener cáncer) y no un sí/no, por lo que se evalúa ranking y calibración por separado. (Sección "Evaluación de modelos")

P: ¿Por qué probar algoritmos en datasets pequeños puede engañar? / R: Porque el mejor algoritmo puede cambiar al aumentar el tamaño de la muestra; por ejemplo, los árboles rinden bien solo con datos suficientes. (Sección "Elegir algoritmo y métrica")

P: En el ejemplo de la campaña de caridad, ¿por qué el modelo descompuesto supera al árbol podado y a la red neuronal? / R: El árbol podado da $0 (nunca halla una hoja con mayoría de positivos) y la red neuronal $7,500; descomponer en "si dona" y "cuánto dona" logra $15,000. (Sección "Un ejemplo final")

P: ¿Qué metodología en dos fases propone el paper para evitar la fuga? / R: Etiquetar cada observación con *legitimacy tags* durante la recolección y luego aplicar una *learn-predict separation*. (Sección "Cómo evitar la fuga")

P: ¿Por qué modelar personas en el futuro es más difícil que etiquetar lo ya ocurrido? / R: Porque los humanos no estamos hechos para entender datos ni la incertidumbre (por nuestros sesgos), sino el lenguaje; la predicción futura es intrínsecamente más incierta. (Sección "Parting Thoughts")

## Puntos a dominar

- Reconocer la *data leakage* como información no disponible en el momento real de la predicción, frecuentemente causa y efecto invertidos o artefactos de preparación.
- Identificar los casos típicos del capítulo: free shipping (Amazon), `sum(revenue)=0` (joyería), "websphere" (IBM), patient ID (cáncer de mama), código 486 (neumonía) y AUC 0.999 (S&P).
- Interiorizar que un rendimiento "too good to be true" es señal de fuga, no de calidad.
- Dominar las medidas de prevención: corte temporal estricto, timestamp del momento en que se supo el dato, partir de datos crudos sin borrar columnas/filas y conocer cómo se crearon.
- Distinguir competiciones "sterile" frente a "real world" y qué habilidades exige cada una.
- Explicar por qué la accuracy es mala métrica y evaluar ranking (ROC/AUC, lift) y calibración (buckets) por separado.
- Relacionar overfitting con cross-validation y complejidad del modelo, y saber que los árboles sin podar sobreajustan y calibran mal.
- Elegir algoritmo y métrica según el tamaño y la naturaleza de los datos (MSE para normales, errores absolutos para la mediana, ponderados para cuantiles).
