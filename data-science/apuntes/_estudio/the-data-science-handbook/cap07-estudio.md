# Interlude: Feature Extraction Ideas (Interludio: ideas para extracción de características) — Estudio

## Tarjetas de repaso

P: ¿Cuál es la tesis central del interludio sobre extracción de características?
R: Un análisis de machine learning solo será tan bueno como las características que le introduzcas; las mejores características reflejan con cuidado aquello que estudias, por lo que hace falta mucha experiencia de dominio.

P: ¿Qué es la característica `Is_null` y por qué es útil?
R: Registra si la entrada original falta. Es simple y sorprendentemente efectiva, porque a menudo el valor es nulo por una razón importante (datos no recogidos de ciertos widgets, o grupos demográficos que reportan menos).

P: ¿Qué es una dummy variable y por qué se llama también one-hot encoding?
R: Es una variable binaria que indica si una columna categórica tiene un valor concreto. Se llama one-hot encoding porque cada fila tendrá un 1 en exactamente una de las dummy variables.

P: ¿Cuáles son los dos problemas grandes de las dummy variables?
R: (a) Puede haber muchísimas categorías, algunas muy raras; lo típico es fijar un umbral, crear dummies para los valores comunes y una adicional para todo lo demás. (b) Solo conoces los valores posibles mirando el entrenamiento, así que necesitas un protocolo para entradas no vistas.

P: ¿Qué son los ranks y para qué sirven?
R: Son una forma contundente de corregir outliers: se ordenan los valores de una columna y se usan sus rangos ordinales.

P: ¿Cuáles son los dos problemas grandes de los ranks?
R: (a) Son costosos porque hay que ordenar toda la lista y no se paralelizan bien en un clúster. (b) Si se clasifican todos los puntos antes de dividir, la información del conjunto de prueba se filtra al de entrenamiento; el apaño de asignar a cada punto de prueba el rango que habría tenido es computacionalmente caro.

P: ¿Qué es el binning y qué inconveniente tiene frente a los ranks?
R: Consiste en colocar los datos en varios bins de histograma de tamaño parecido (por ejemplo por percentiles) y decir solo en qué bin cae cada punto. Aborda los dos problemas de los ranks pero pierde la resolución fina de los rangos percentiles.

P: ¿Qué efecto tiene tomar el logaritmo de un valor y qué hacer si hay ceros?
R: Amortigua los grandes outliers y realza los valores pequeños. Si los datos contienen ceros, lo habitual es sumar 1 antes de tomar el logaritmo.

P: Cuando hay varias filas por entidad, ¿qué métricas agregadas de fuerza bruta se pueden extraer?
R: El número de filas; la media, mínimo, máximo, mediana, etc. de una columna; para columnas no numéricas, el número de entradas distintas o el número de entradas iguales a la más común; y la correlación entre dos columnas distintas.

P: ¿Qué características más sofisticadas se adelantan para imágenes y series temporales?
R: Medir cuánto se parece una imagen a otra, clásicamente con Principal Component Analysis (PCA), que también sirve para arrays numéricos de series temporales o mediciones de sensores.

P: ¿Cómo se pueden usar el clustering y el texto como fuente de características?
R: El clustering permite usar el cluster de cada punto como característica categórica; en texto se puede extraer la frecuencia de cada palabra, aunque suele dar demasiadas características y hacer falta un método adicional para condensarlas.

P: ¿Qué quiere decir que a veces la característica más importante es la que intentas predecir?
R: Que definir la variable objetivo puede ser un problema de extracción en sí mismo, porque la "ground truth" (tráfico humano real, lealtad del cliente, inminencia de un evento) hay que estimarla a partir de datos contaminados o indirectos.

## Preguntas de autoevaluación

P: ¿Por qué el autor insiste en la experiencia de dominio antes de las técnicas de machine learning?
R: Porque el análisis solo es tan bueno como las características que le das, y las mejores reflejan con cuidado el fenómeno estudiado, lo que exige aportar experiencia de dominio al problema. (Lo que necesitas saber)

P: ¿Qué protocolo se recomienda para las dummy variables cuando aparece un valor categórico no visto en el entrenamiento?
R: Fijar un umbral y crear dummies solo para los valores más comunes, más una dummy adicional que valga 1 para todo lo demás, y disponer de un protocolo para entradas no presentes en el entrenamiento. (Standard Features)

P: ¿Por qué los ranks pueden filtrar información del conjunto de prueba al de entrenamiento y cómo se mitiga?
R: Si se clasifican todos los puntos antes de dividir, los rangos del entrenamiento ya contienen información del conjunto de prueba. Se mitiga asignando a cada punto de prueba el rango que habría tenido en el entrenamiento, aunque es caro. (Standard Features)

P: ¿En qué situación conviene agrupar filas para extraer características y por qué?
R: Cuando el dataset tiene varias filas por una sola entidad (por ejemplo una fila por transacción con una columna de cliente) pero queremos características sobre la entidad; hay que agregar las filas de cada entidad. (Features That Involve Grouping)

P: ¿Qué problema plantea extraer la frecuencia de palabras en texto?
R: Que suele generar demasiadas características, por lo que puede hacer falta un método adicional para condensarlas. (Preview of More Sophisticated Features)

P: ¿Cómo resolvió el autor la estimación de tráfico humano contaminado por bots?
R: Filtrando ese tráfico y estimando su correspondencia con humanos reales como problema aparte, comparando su estimación con la de Google en unos pocos sitios; a veces quedaba por encima y a veces por debajo, pero concluyeron que coincidía lo suficiente. (Defining the Feature You Want to Predict)

P: Al predecir eventos a partir de series temporales, ¿qué decisiones hay que tomar sobre la variable objetivo?
R: Decidir cuán lejos en el futuro puede estar un evento antes de considerarse "imminent", o bien usar un valor continuo del tiempo hasta el próximo evento, topándolo en un máximo o tomando su logaritmo para amortiguar outliers. (Defining the Feature You Want to Predict)

## Puntos a dominar

- Entender que la calidad de las características limita la calidad del análisis y que la experiencia de dominio es decisiva.
- Reconocer cuándo aplicar `Is_null` y por qué un valor faltante puede ser informativo.
- Saber construir dummy variables (one-hot encoding) gestionando categorías raras y valores no vistos en el entrenamiento.
- Distinguir ranks de binning: cuándo corrigen outliers, su coste y el riesgo de fuga de información prueba/entrenamiento.
- Aplicar el logaritmo para amortiguar outliers y recordar sumar 1 cuando hay ceros.
- Identificar las métricas de agregación disponibles cuando hay varias filas por entidad.
- Conocer el papel de PCA, clustering y frecuencia de palabras como características más sofisticadas.
- Asumir que definir la variable a predecir puede ser el propio problema de extracción de características.
