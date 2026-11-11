# Visualizing Model Performance (Visualización del rendimiento de modelos) — Estudio

## Tarjetas de repaso

P: ¿Qué alternativa a decidir caso por caso propone el capítulo para actuar sobre los casos? / R: Rankear los casos por score y actuar sobre los `n` primeros (o los que superen un umbral), lo que es útil con presupuesto fijo o cuando no hay probabilidades fiables.

P: ¿Qué produce un clasificador de ranking combinado con un umbral? / R: Una única matriz de confusión; al variar el umbral cambian los true positives y false positives, generando una familia de matrices.

P: ¿Qué ocurre con las instancias al bajar el umbral? / R: Suben de la fila N a la fila Y: las positivas se vuelven true positives (Y,p) y las negativas, false positives (Y,n).

P: ¿Qué es una profit curve y qué grafica? / R: El barrido del umbral sobre la lista ordenada por score decreciente, registrando en cada corte el porcentaje de la lista predicho como positivo y el beneficio esperado correspondiente.

P: ¿Cuándo son apropiadas las profit curves? / R: Cuando los class priors (base rate) y los costes y beneficios se conocen con certeza y son estables.

P: ¿Cómo afecta una restricción de presupuesto a la elección de clasificador? / R: Cambia el punto de operación (por ejemplo del 50% al 8% de la base) y puede cambiar qué clasificador conviene usar para rankear.

P: ¿Qué representan los ejes de un gráfico ROC? / R: La false positive rate (false alarm rate) en el eje x y la true positive rate (hit rate) en el eje y, mostrando el trade-off entre costes y beneficios.

P: ¿Qué significan los puntos (0,0), (1,1), (0,1) y la diagonal en el espacio ROC? / R: (0,0) nunca clasifica positivo; (1,1) siempre clasifica positivo; (0,1) es clasificación perfecta; la diagonal de (0,0) a (1,1) es adivinar al azar.

P: ¿Cuál es la ventaja principal del gráfico ROC? / R: Desacopla el rendimiento del clasificador de las condiciones de uso: es independiente de las proporciones de clase y de los costes y beneficios.

P: ¿Qué es el AUC y qué rango tiene? / R: El área bajo la curva ROC como fracción del cuadrado unidad, de 0 a 1 (0,5 = azar); equivale a la probabilidad de que un positivo al azar quede rankeado por delante de un negativo al azar.

P: ¿A qué medidas equivale técnicamente el AUC? / R: A la medida Mann-Whitney-Wilcoxon y, con una transformación algebraica menor, al coeficiente de Gini.

P: ¿Qué grafica una cumulative response curve? / R: El hit rate (tp rate, eje y) frente al porcentaje de la población apuntada (eje x); la diagonal x=y representa el azar.

P: ¿Qué significa un "2X lift"? / R: Que en el umbral elegido el modelo apunta el doble de bien que el azar; el lift es el valor de la cumulative response dividido por la diagonal y=x.

P: ¿Qué supuesto limita a las cumulative response y lift curves frente a las ROC? / R: Asumen que el test conserva exactamente los mismos priors que la población real, por lo que el down-sampling de negativos las distorsiona (a las ROC no).

P: ¿Por qué el k-NN alcanzaba 93% de accuracy en el churn pese a ser pobre? / R: Porque casi nunca predecía churn, comportándose como clasificador de base rate (el base rate era 93%); la accuracy engaña en datasets sesgados.

## Preguntas de autoevaluación

P: ¿Por qué el capítulo propone visualizaciones en lugar de confiar en un único número de beneficio esperado? / R: Porque los cálculos aislados dependen de supuestos muy estrictos (conocimiento preciso de costes, beneficios y probabilidades), mientras que las visualizaciones comunican mejor a los stakeholders y exponen el comportamiento del modelo bajo incertidumbre. (Sección "Lo que necesitas saber")

P: ¿Qué cuatro técnicas presenta el capítulo y bajo qué condiciones conviene cada una? / R: Profit curves (priors, costes y beneficios conocidos y estables), ROC curves y su AUC (condiciones inciertas o cambiantes), y cumulative response y lift curves (costes inciertos pero proporción de clases estable). (Sección "Lo que necesitas saber" y "Resumen del capítulo")

P: En el ejemplo de presupuesto limitado, ¿por qué el mejor clasificador pasa a ser el Classifier 1? / R: Con 100.000 clientes y $40.000 a $5 por oferta solo se pueden hacer 8.000 ofertas (8% de la base); mirando las curvas en x=8% el Classifier 1 es superior, aunque con recursos ilimitados el Classifier 2 maximizaba el beneficio apuntando al 50%. (Sección "Profit curves")

P: ¿Por qué ningún clasificador debería caer en el triángulo inferior derecho del espacio ROC? / R: Porque esa región corresponde a un rendimiento peor que el azar; para separarse de la diagonal hacia el triángulo superior el clasificador debe explotar información de los datos. (Sección "ROC graphs y curvas")

P: ¿Por qué una evaluación ingenua del churn (entrenar y testear sobre el mismo set) da resultados engañosos? / R: Porque con base rate del 93% cualquier clasificador debería alcanzar ese mínimo, por lo que el 100% del k-NN y el 76% de Naive Bayes resultan sospechosos; esos números reflejan memorización (overfitting). (Sección "Ejemplo: analítica de rendimiento para modelos de churn")

P: ¿Cómo se explica que Naive Bayes tenga la accuracy más baja pero el AUC más alto? / R: El k-NN casi nunca predice churn y actúa como clasificador de base rate, mientras Naive Bayes comete más errores pero identifica a muchos más churners, lo que eleva su AUC. (Sección "Ejemplo: analítica de rendimiento para modelos de churn")

P: ¿Por qué no se puede tomar el top 25% del Tree y continuar con Naive Bayes esperando el resultado óptimo? / R: Porque los órdenes de ranking de los dos clasificadores son distintos; combinarlos bien requiere métodos principiados (ensembles). (Sección "Ejemplo: analítica de rendimiento para modelos de churn")

P: ¿Qué ilustra la comparación entre los dos escenarios de costes de las profit curves de churn? / R: La sensibilidad de las profit curves a los supuestos de costes y beneficios: con ratio 9 a 1 hay un máximo hacia el 20%, y con ratio 12 a 1 el beneficio máximo es mayor y aparecen dos máximos (Tree ~20%, NB ~35%). (Sección "Ejemplo: analítica de rendimiento para modelos de churn")

## Puntos a dominar

- Entender que un clasificador de ranking más un umbral equivale a una matriz de confusión, y cómo el barrido del umbral genera curvas de rendimiento.
- Saber elegir la visualización según qué condiciones son estables: profit curves (priors y costes conocidos), ROC/AUC (condiciones inciertas), cumulative response/lift (costes inciertos, priors estables).
- Leer un gráfico ROC: ejes (fp rate vs tp rate), puntos clave, diagonal del azar, región noroeste como mejor rendimiento y zonas conservadora/permisiva.
- Interpretar el AUC como número resumen (0 a 1, 0,5 = azar) y como probabilidad de rankear un positivo por delante de un negativo.
- Reconocer que la accuracy engaña en datasets sesgados y que el comportamiento de base rate puede inflarla sin valor predictivo.
- Recordar la limitación de priors de las lift/cumulative response curves frente a la robustez de las ROC ante el down-sampling.
- Validar con cross-validation y fitting curves para no confiar en resultados de entrenamiento inflados por overfitting.
- Tener presente que combinar segmentos de distintos clasificadores no da lo óptimo y que para ello existen los ensembles.
