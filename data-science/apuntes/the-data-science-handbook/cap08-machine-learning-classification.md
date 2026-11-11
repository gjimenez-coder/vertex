# The Data Science Handbook — Field Cady (Wiley, 2017)
## Capítulo 8 — Machine Learning Classification (Clasificación con aprendizaje automático)

> Nota de extracción: texto obtenido de la capa de texto del PDF; las citas indican la página como (PDF p. N).

## Lo que necesitas saber

Los clasificadores de machine learning son una pieza central del kit del data scientist, pero Cady insiste en desmitificarlos: no son la "caja negra mágica" que se suele vender. La mayor parte del trabajo está en preparar los datos, apuntar el clasificador a la pregunta correcta y dar sentido a los resultados. Entrenar un clasificador básico "no es ciencia de cohetes".

El capítulo tiene dos mitades. La primera es una serie de tutoriales rápidos sobre los clasificadores más útiles (árboles de decisión, random forests, SVM, regresión logística, lasso, naive Bayes y redes neuronales). La segunda trata cómo medir su precisión (matrices de confusión, curvas ROC, AUC, elección de umbrales y otras métricas).

Sales sabiendo para qué sirve un clasificador, los dos grandes usos (clasificar en producción y extraer insights del negocio), las ideas de fondo de cada algoritmo con sus fortalezas y debilidades, y cómo evaluar el rendimiento equilibrando falsos positivos y falsos negativos.

## ¿Qué es un clasificador y para qué sirve? (8.1–8.3)

Un clasificador tiene dos etapas: se *entrena* con datos etiquetados (puntos con su etiqueta correcta) para aprender un patrón, y luego actúa como una función que recibe puntos nuevos y predice su clasificación. La predicción puede ser una etiqueta concreta o un número continuo interpretable como puntuación de confianza (PDF p. 105).

Hay dos usos principales. El obvio: tener cosas que clasificar, ya sea de forma autónoma (qué anuncio mostrar) o marcando casos para que los revise un humano (posible fraude con tarjeta). El segundo, que para Cady ha sido el más común en su carrera: obtener *insights* sobre los datos subyacentes. A los clientes a menudo no les interesa predecir que una máquina fallará, sino los patrones que predicen el fallo, para diagnosticar y corregir. Esto crea un dilema: a veces los clasificadores más precisos son los más difíciles de interpretar.

Preocupaciones prácticas (8.2): todo se basa en tener datos etiquetados correctamente y en cantidad suficiente, un lujo que el mundo real rara vez ofrece. En detección de fraude sueles tener un conjunto modesto de casos etiquetados a mano y una enorme masa de datos sin etiquetar que presumes no fraudulentos, por lo que una fracción desconocida del entrenamiento está mal etiquetada. Además, ¿qué *es* "fraude"? Definir la verdad de base (ground truth) es un problema en sí mismo. Un truco de Cady cuando busca patrones es eliminar los casos límite del entrenamiento: con un cliente que estudiaba la "lealtad", definió criterios de "claramente leal" y "claramente no leal" y descartó la zona gris (un tercio de los clientes); el clasificador funcionó sorprendentemente bien. Junto a esto está el problema perenne: la extracción de características (feature extraction). Cualquier clasificador fallará si le das características sin señal.

Binario vs. multiclase (8.3): la mayoría de problemas son binarios (1 o 0), pero a veces la etiqueta es categórica con varios valores. Algunos algoritmos lo manejan de forma nativa; otros son estrictamente binarios. La solución estándar para k etiquetas con un clasificador binario es entrenar k clasificadores, uno por etiqueta (X o no-X). Estos detalles suelen quedar ocultos dentro de las librerías; el capítulo asume que todos los clasificadores son binarios.

## El ejemplo que recorre el capítulo (8.4)

Un script con el dataset iris entrena varios clasificadores para distinguir *iris virginica* del resto y dibuja sus curvas ROC para compararlos. El núcleo:

```python
CLASS_MAP = {
    'LogisticRegression': ('-', LogisticRegression()),
    'Naive Bayes': ('--', GaussianNB()),
    'Decision Tree': ('.-', DecisionTreeClassifier(max_depth=5)),
    'Random Forest': (':', RandomForestClassifier(
        max_depth=5, n_estimators=10, max_features=1)),
}
X, Y = df[df.columns[:3]], (df['species']=='virginica')
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=.8)
for name, (line_fmt, model) in CLASS_MAP.items():
    model.fit(X_train, Y_train)
    preds = model.predict_proba(X_test)
    fpr, tpr, thresholds = roc_curve(Y_test, pd.Series(preds[:,1]))
    auc_score = auc(fpr, tpr)
```

Los AUC resultantes: regresión logística 0.989, random forest 0.901, naive Bayes 0.897, árbol de decisión 0.830 (PDF p. 109).

## Clasificadores específicos (8.5)

Árboles de decisión. Conceptualmente los más simples: clasificar equivale a seguir un diagrama de flujo. Cada nodo pregunta por una característica (umbral si es numérica, un hijo por valor si es categórica) y las hojas dan las puntuaciones. Entrenarlo es otra historia: hallar el árbol óptimo es computacionalmente intratable, así que se usa una heurística: en cada paso se busca la característica/corte que mejor particiona los datos (medida con "information gain" o "Gini impurity"), se recursiona en los hijos y se para cuando todos los puntos comparten etiqueta o se alcanza la profundidad máxima. El gran problema es el *overfitting*: si la profundidad es excesiva, cada hoja contiene pocos puntos y da puntuaciones muy seguras que son accidentes de números pequeños. Hay que ajustar los árboles porque los valores por defecto suelen dejarlos sobreajustar. Son muy legibles (útil con gente recelosa de las cajas negras) y rápidos, pero sorprendentemente difíciles de interpretar en profundidad. Cady no los usa mucho salvo como bloque para random forests.

```python
clf = DecisionTreeClassifier(max_depth=5)
clf.fit(train[indep_cols], train.breed)
```

Random forests. Si solo pudiera llevarse un clasificador a una isla desierta, sería este: consistentemente de los más precisos y robustos. Es una colección de árboles, cada uno entrenado sobre un subconjunto aleatorio de filas y de características, sin coordinación. La puntuación final es el promedio (o la fracción de votos) de todos los árboles. Cada árbol capta patrones distintos y da predicciones confiadas solo cuando su patrón está presente; los sobreajustes individuales, aleatorios y distintos, tienden a cancelarse. El inconveniente: son imposibles de interpretar en términos de negocio; su potencia es justamente ser demasiado complejos. Lo único extraíble es la *feature importance*, calculada barajando aleatoriamente la k-ésima característica entre puntos y midiendo cuánto empeora el rendimiento.

Clasificadores de ensemble (8.5.3). Los random forests son el ejemplo más conocido: se entrenan muchos clasificadores bajo condiciones aleatorias distintas y se agregan sus resultados. Si cada uno es al menos marginalmente bueno y están poco correlacionados, el conjunto converge con fiabilidad a la respuesta correcta. Es usar fuerza bruta computacional y la ley de los grandes números en lugar de conocimiento del dominio.

Support vector machines (SVM). Famosas, pero Cady las detesta. Asumen *separabilidad lineal*: ven cada punto en un espacio d-dimensional y buscan el hiperplano que separa las dos clases. Entrenar consiste en hallar el hiperplano que separa los datos y queda "en medio" del hueco, maximizando el *margin* (distancia mínima a los puntos de cada clase). El hiperplano es f(x) = w·x + b = 0; se clasifica según el signo de f(x). La versión "hard margin" supone separación perfecta; en la práctica se usa "soft margin", que penaliza los puntos del lado equivocado. Problemas: si hay tantas características como puntos, siempre existe un hiperplano separador y el sobreajuste es casi seguro; y son fundamentalmente binarias, sin puntuaciones continuas de confianza. La separabilidad lineal falla en casos como una clase cerca del origen y otra lejos. La solución es el *kernel SVM*: mapear los puntos a otro espacio donde la frontera sí sea lineal. La clave computacional es el "kernel trick": nunca se calcula el mapeo ϕ directamente, solo la función kernel k(x,y) = ϕ(x)·ϕ(y), que suele ser simple y no lineal. Kernels habituales: polinómico, gaussiano y sigmoide. No toda función es un kernel válido: debe ser simétrica y "definida positiva".

Regresión logística. Un excelente clasificador de propósito general, con buen equilibrio entre precisión e interpretabilidad. Es como una versión no binaria del SVM: puntúa los puntos con probabilidades según su distancia al hiperplano mediante la función sigmoide σ(z) = 1/(1 + exp[−z]), donde σ(0)=0.5 y tiende a 1 o 0 en los extremos. El hiperplano w·x + b = 0 es ahora la línea donde p(x) = ½. Interpretar el modelo es fácil: si el componente k-ésimo de w es grande y positivo, esa característica alta empuja hacia la etiqueta 1; si es grande y negativo, hacia 0; cuanto mayores los elementos de w, más se aproxima a un SVM. Requiere escalar todas las características a la misma escala para que los coeficientes sean comparables. Además es muy eficiente: el modelo son solo d+1 números en coma flotante.

Lasso regression. Variante de la logística. Un problema de la logística es tener muchas características con pesos modestos en vez de pocas con pesos grandes, lo que dificulta la interpretación y es una forma solapada de overfitting. Lasso entrena penalizando los pesos modestos; el resultado tiende a llevar la mayoría de los pesos a 0 dejando solo las pocas características más significativas.

Naive Bayes. Versión drásticamente simplificada de la estadística bayesiana. Intuición: partes de una confianza inicial en cada etiqueta y la ajustas con cada nueva información según su verosimilitud condicionada a cada etiqueta. En el entrenamiento aprende cuán común es cada etiqueta y la distribución de probabilidad de cada característica condicionada a cada etiqueta (probabilidades condicionales). Al clasificar, parte de la proporción de cada etiqueta y va multiplicando por las probabilidades condicionales, renormalizando con γ para que sumen 1. Su gran defecto: trata cada característica como independiente de las demás (si X5 es copia de X4, la cuenta dos veces). Aun así suelen ser muy potentes: duplicar una variable predictiva fuerte puede volverte sobreconfiado, pero rara vez te hace equivocarte.

Redes neuronales. Fueron la oveja negra y hoy viven un renacimiento, sobre todo el *deep learning*. La analogía con el cerebro humano es falsa; una red básica es "solo otro clasificador". La más simple es el perceptrón: una red de "neuronas" organizadas en capas; las capas intermedias son "hidden" y la última produce las salidas (una puntuación por categoría). Cada neurona calcula su salida con una *activation function*, típicamente la sigmoide sobre una combinación ponderada de sus entradas: en efecto, cada neurona es una pequeña regresión logística, y una red sin capas ocultas es un conjunto de regresores logísticos. Se entrenan con *backpropagation*: se propagan los ajustes de la capa final hacia atrás, y la sigmoide hace el proceso más tratable. Su virtud distintiva es identificar *características agregadas* (una neurona oculta puede detectar segmentos de recta o curvas al reconocer letras manuscritas), a menudo más interesantes que las entradas crudas.

## Evaluación de clasificadores (8.6)

En aplicaciones de negocio buscas más una clase que otra (acciones prometedoras, pacientes con cáncer). Hay dos aspectos: marcar lo que buscas y no marcar lo que no buscas. Marcar agresivamente da muchos falsos positivos; marcar con cautela deja fuera cosas que debían marcarse. El equilibrio entre falsos positivos y negativos es una cuestión de negocio, no analítica. Las dos métricas que dan la imagen completa:

- True positive rate (TPR): de todo lo que debía marcarse, la fracción que se marca. Ideal 1.0.
- False positive rate (FPR): de todo lo que NO debía marcarse, la fracción que se marca igualmente. Ideal 0.0.

Otras equivalentes: precision (fracción de lo marcado que realmente es un hit) y recall (fracción de todos los hits que se marcan).

Matrices de confusión (8.6.1): tabla 2×2 con lo clasificado frente a lo que debía ser. En el ejemplo, TPR = 10/(10+1) = 0.91 y FPR = 4/(4+35) = 0.10 (PDF p. 123).

Curvas ROC (8.6.2): con FPR en el eje x y TPR en el eje y, la esquina superior izquierda (0.0, 1.0) es el clasificador perfecto; por debajo de la línea y = x es "peor que inútil". Como casi ningún clasificador es realmente binario (dan puntuaciones), cada umbral posible es un clasificador distinto y todos juntos trazan la curva ROC. Subiendo desde (0,0) al aflojar el criterio, un buen clasificador sube abruptamente; la "rodilla" apuntando a la esquina superior izquierda es la firma de un clasificador fuerte.

Área bajo la curva (8.6.3): el AUC resume la ROC en un número; cercano a 1.0 es bueno, cercano a 0.5 es pobre. No depende de dónde se ponga el corte y tiene un significado claro: la probabilidad de que un hit aleatorio tenga mayor predicción que un no-hit aleatorio. Cady lo usa para decidir entre clasificadores y configuraciones.

## Selección de umbrales y otras métricas (8.7)

Queremos un umbral cerca de la "rodilla". Dos formas elegantes: (1) donde la ROC corta la línea y = 1−x, lo que iguala la precisión en hits y en no-hits (permite responder "cómo de preciso es" con un solo número); (2) donde la ROC tiene pendiente paralela a y = x, un punto de inflexión que equivale a decir que un épsilon más de TPR vale el coste de un épsilon más de FPR; esta segunda generaliza a otras ponderaciones.

Otras métricas (8.7.1): para un clasificador binario, el clásico es el **F1 score**, media armónica de precision y recall (1.0 perfecto, 0.0 el peor caso). No hay nada mágico en la media armónica: a veces se usa la geométrica (G-score). La aritmética sería mala porque marcarlo todo (o nada) daría una puntuación mejor que 0.

Curvas lift–reach (8.7.2): información equivalente a la ROC pero presentada distinto. *Reach* es la fracción de puntos marcados; *lift* es la fracción de marcados que son hits dividida por la proporción de hits en la población (lift 1 = marcar al azar; mayor = buen rendimiento). El lift suele empezar alto y decaer a 1.0 cuando el reach se acerca a 1.

## Ideas clave

- Un clasificador se entrena con datos etiquetados y luego predice; sus dos usos son clasificar en producción y extraer insights del negocio.
- El trabajo duro está en los datos y la extracción de características: sin señal en las features, ningún clasificador funciona. Definir el ground truth es parte del problema.
- Árboles de decisión: simples y legibles pero propensos al overfitting; base de los random forests.
- Random forests y ensembles: muy precisos y robustos por la ley de los grandes números, pero casi imposibles de interpretar salvo la feature importance.
- SVM asume separabilidad lineal y es binario; el kernel trick (k(x,y) = ϕ(x)·ϕ(y)) resuelve datos no lineales sin calcular ϕ.
- Regresión logística: equilibrio entre precisión e interpretabilidad vía la sigmoide; lasso lleva pesos a 0 para quedarse con pocas features relevantes.
- Naive Bayes asume independencia entre características y aun así suele ser potente; las redes neuronales encadenan regresiones logísticas y destacan por hallar características agregadas.
- Se evalúa con TPR/FPR, matrices de confusión, curvas ROC y AUC; los umbrales se eligen cerca de la "rodilla", y F1 resume el rendimiento de un clasificador binario.
