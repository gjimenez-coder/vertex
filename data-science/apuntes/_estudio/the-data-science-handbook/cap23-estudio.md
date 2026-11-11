# Maximum Likelihood Estimation and Optimization (Estimación por máxima verosimilitud y optimización) — Estudio

## Tarjetas de repaso

P: ¿Qué busca la estimación por máxima verosimilitud (MLE)?
R: El valor de los parámetros θ que maximiza P(X|θ), asumiendo que un proceso real sigue alguna distribución de una familia descrita por θ y que X procede de ese proceso.

P: ¿Por qué en MLE la probabilidad del conjunto es el producto de las probabilidades de cada punto?
R: Porque casi siempre se asume que los puntos de datos de X son independientes entre sí, de modo que P(X|θ) = ∏ P(Xi|θ).

P: ¿Por qué suele maximizarse el log-verosimilitud en lugar de la verosimilitud?
R: Porque el logaritmo convierte el producto en una suma: log P(X|θ) = Σ log P(Xi|θ), lo que es más fácil de maximizar.

P: ¿Cuáles son los dos problemas significativos de la MLE?
R: El overfitting (sobre todo con conjuntos pequeños) y el problema logístico de calcular realmente el θ óptimo.

P: ¿Cuál es la alternativa más popular a la MLE frente al overfitting y qué desventajas tiene?
R: El enfoque bayesiano: más difícil de entender, más complicado de implementar, más lento y con la espinosa cuestión de cómo elegir el prior.

P: ¿Cuándo son los mínimos cuadrados la técnica correcta según la MLE?
R: Cuando se cumple la suposición de que y es una función lineal de x más ruido con distribución normal; entonces existe solución cerrada para la pendiente m y la ordenada b.

P: ¿Qué calcula la regresión logística y cómo?
R: La probabilidad p(x) = σ(w·x + b) = 1 / (1 + exp(w·x + b)) de que un punto en x sea un 1; el entrenamiento busca el w y el b que maximizan la verosimilitud de las etiquetas observadas.

P: ¿Qué problema general resuelve la optimización?
R: Dada f(θ) con θ de d dimensiones y posibles restricciones gi(θ) ≤ 0, encontrar el θ que minimiza f(θ) cumpliendo todas las restricciones.

P: ¿Qué diferencia a la regresión LASSO de la regularización elastic net?
R: LASSO resta un término λ·Σ|wi| (penaliza pesos grandes y pequeños moderadamente); elastic net añade además un término que penaliza el cuadrado de los pesos para castigar con dureza los pesos grandes.

P: ¿Cuáles son las dos formas típicas de fallo de un optimizador tratado como caja negra?
R: Que la secuencia de conjeturas se dispare al infinito en alguna dirección (reiniciar con otra conjetura inicial) o que converja a un óptimo local.

P: ¿Qué es un óptimo local?
R: Un punto mejor que todo lo cercano pero peor que algún punto lejano.

P: ¿Qué dirección toma el descenso de gradiente y por qué?
R: La dirección −∇f(x), porque multiplicar el gradiente por −1 da la dirección más empinada cuesta abajo.

P: ¿Para qué sirve el Hessiano en la optimización?
R: Como matriz de segundas derivadas permite aproximar f localmente como un paraboloide y moverse hacia su centro; muchos algoritmos pasan a él cerca del óptimo porque converge más rápido.

P: ¿Qué condiciones definen un problema convexo?
R: La función objetivo tiene forma de "cuenco" (sin mínimos locales salvo el global) y la región factible es convexa (una recta entre dos puntos cualesquiera queda dentro). Formalmente, f(αx + (1−α)y) ≤ αf(x) + (1−α)f(y) para α entre 0 y 1.

P: ¿Qué idea sostiene el descenso de gradiente estocástico (SGD) y su variante mini batch?
R: Aproximar el gradiente usando un único índice i (SGD) o una selección de varios puntos (mini batch), haciendo viable la optimización cuando N es enorme; el mini batch tiende a converger más rápido que el SGD puro.

## Preguntas de autoevaluación

P: ¿Qué significa, bajo el marco de la MLE, "entrenar el modelo"?
R: Calcular θ, es decir, hallar los parámetros que maximizan P(X|θ); muchos modelos de clasificación y regresión caen bajo este paraguas. (Sección: Lo que necesitas saber)

P: ¿Por qué un cambio en las suposiciones sobre el ruido puede hacer que los mínimos cuadrados dejen de ser adecuados? Da un ejemplo del apunte.
R: Porque los mínimos cuadrados solo son correctos si el ruido es normal y constante; si x es el ingreso e y el precio de la vivienda, conviene que la desviación típica del ruido sea proporcional a x (β·x), porque 20.000 $ pesan distinto según el ingreso. Esa variante probablemente no tiene solución cerrada. (Sección: Un ejemplo simple: ajustar una recta)

P: ¿Cómo se construye la verosimilitud de las etiquetas en regresión logística?
R: Como el producto de p(x) sobre los puntos con y=1 por el producto de (1 − p(x)) sobre los puntos con y=0. (Sección: Otro ejemplo: regresión logística)

P: ¿Por qué añadir un término de penalización a la MLE deja de ser una MLE válida pero sigue siendo útil?
R: Porque ya no maximiza P(X|θ), pero se convierte en un problema de optimización que mitiga el overfitting; así se obtienen LASSO o elastic net. (Sección: Optimización)

P: ¿Qué se puede hacer cuando un optimizador converge a un óptimo local y qué limitación persiste?
R: Probar varias conjeturas iniciales y ver si las mejores convergen al mismo sitio; aun así no puedes estar seguro de haber hallado el óptimo global. (Sección: Optimización)

P: En el descenso de gradiente, ¿cómo se ajusta el tamaño de paso y qué dos problemas hay que evitar?
R: Usar el gradiente como paso inicial y multiplicarlo por α > 1 mientras f baje, o dividirlo por α si no bajó. Hay que evitar reducir el paso tan rápido que se tarde mucho o se converja antes del mínimo, y sobrepasar el mínimo repetidamente (que puede hacer aumentar f). (Sección: Descenso de gradiente y optimización convexa)

P: ¿Por qué importa tanto que un problema sea convexo?
R: Porque casi no hay término medio: si es convexo, cualquier algoritmo decente converge al óptimo global; si no, no hay garantías. Por eso se reformulan problemas no convexos en equivalentes convexos o se demuestra que lo son. (Sección: Optimización convexa)

P: ¿Por qué el SGD es necesario en problemas MLE con datasets grandes?
R: Porque la función objetivo es una suma sobre N puntos (Σ log P(Xi|θ)) y, con N enorme, calcular el gradiente completo es computacionalmente prohibitivo; el SGD aproxima el gradiente con uno o pocos puntos. (Sección: Descenso de gradiente estocástico (SGD))

## Puntos a dominar

- Plantear un problema como MLE: identificar la familia de distribuciones, los parámetros θ y la expresión P(X|θ) = ∏ P(Xi|θ), y pasar al log-verosimilitud (suma) para maximizar.
- Reconocer cuándo una técnica estándar (mínimos cuadrados) es la MLE correcta según sus suposiciones y cuándo cambiarlas (ruido proporcional a x, distribuciones con más outliers).
- Distinguir overfitting y cálculo del óptimo como los dos problemas de la MLE, y situar el enfoque bayesiano como alternativa frente al primero.
- Diferenciar LASSO (penaliza |w|) de elastic net (penaliza |w| y w²) como regularizaciones vía optimización.
- Explicar el descenso de gradiente: dirección −∇f, alternativas sin gradiente, uso del Hessiano y ajuste del tamaño de paso con α.
- Enunciar las dos condiciones de convexidad (cuenco y región factible convexa) y su desigualdad formal, y por qué garantizan convergencia al óptimo global.
- Describir SGD y mini batch SGD como aproximaciones del gradiente que hacen viable la optimización con muchos datos.
