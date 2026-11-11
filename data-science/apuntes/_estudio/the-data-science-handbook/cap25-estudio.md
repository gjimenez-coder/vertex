# Stochastic Modeling (Modelado estocástico) — Estudio

## Tarjetas de repaso

P: ¿Qué estudia el modelado estocástico?
R: Un proceso que ocurre de forma aleatoria a lo largo de algo secuencial (tiempo, palabras, generaciones, posición), no una sola variable aleatoria.

P: ¿Qué dice la propiedad de Markov?
R: La distribución de Xᵢ₊₁ puede depender de Xᵢ, pero es independiente de todos los estados anteriores si se conoce Xᵢ: Pr(Xᵢ₊₁ | X₁…Xᵢ) = Pr(Xᵢ₊₁ | Xᵢ).

P: ¿Cómo se representan las transiciones de una cadena de Markov de k estados?
R: Con una matriz k×k donde la fila i es "estar en i" y la entrada j es la probabilidad de saltar a j; cada entrada ≥ 0 y cada fila suma 1.0.

P: Dado el vector de estado p, ¿cómo se obtiene la distribución tras m pasos?
R: p_{i+m} = p_i·Tᵐ (un paso: p_{i+1} = p_i·T).

P: ¿A qué equivale una cadena de Markov de orden m?
R: A una cadena de orden 1 con kᵐ estados; con m grande el número de estados se vuelve astronómico e inviable.

P: ¿Qué caracteriza a una cadena irreducible aperiódica?
R: Se puede ir de cualquier estado a cualquier otro en pasos finitos y ningún estado es periódico; tiene una distribución de equilibrio única π.

P: ¿Cómo se halla la distribución de equilibrio π?
R: Resolviendo π = π·T con Σπᵢ = 1, o aproximándola iterando Tᵐ hasta que sus filas converjan a π.

P: ¿Qué es una cadena absorbente y qué modela?
R: Una cadena con al menos un estado que va a sí mismo con probabilidad 1.0; modela procesos que terminan (visitante que compra o abandona, máquina que se avería).

P: ¿Para qué sirve MCMC y cuándo se usa?
R: Genera muestras θᵢ cuya distribución estacionaria es la distribución objetivo π; se usa cuando solo se conoce una función de puntuación S(θ) proporcional a π, no la constante de proporcionalidad.

P: ¿Qué es un modelo oculto de Markov (HMM)?
R: Una cadena de Markov subyacente de estados ocultos Xᵢ más observaciones Yᵢ que dependen solo de su Xᵢ; se caracteriza por la distribución inicial, la matriz de transición y Pr(Y|X).

P: ¿Qué hace el algoritmo de Viterbi?
R: Halla la secuencia más probable de estados ocultos recorriendo un trellis capa a capa, maximizando la suma de log-scores y guardando el "padre" de cada nodo para reconstruir el camino.

P: ¿Qué diferencia a un random walk del movimiento browniano?
R: El random walk sube/baja 1 entero por paso (Bernoulli); el browniano generaliza a los reales con Xᵢ₊₁ − Xᵢ = Normal(0, σ²).

P: ¿Qué aporta ARIMA frente al movimiento browniano?
R: Reversión a la media: X_{i+1} = c + φ·X_i + Normal(0, σ²) con 0 < φ < 1 y media a largo plazo E[X] = c/(1 − φ).

P: ¿Qué mide π en cadenas discretas frente a procesos de Markov en tiempo continuo?
R: En discretas, la frecuencia con que se transiciona a cada estado; en continuas, la fracción del tiempo total que se pasa en cada estado.

P: ¿Qué supone un proceso de Poisson?
R: Eventos independientes con tiempos entre eventos exponenciales de media θ = 1/λ; el número de eventos en un intervalo T sigue una Poisson de media λT.

## Preguntas de autoevaluación

P: ¿Por qué la propiedad de Markov hace que las cadenas sean tratables?
R: Porque la distribución del siguiente estado depende solo del actual, lo que permite caracterizar toda la cadena con la matriz de transición T y la distribución inicial y calcular pasos futuros con potencias de T. (Sección 25.1)

P: ¿Por qué modelar lenguaje natural con m = 6 es problemático pese a capturar más contexto?
R: Una cadena de orden m equivale a una de orden 1 con kᵐ estados; con m = 6 el número de estados es astronómico, no hay datos suficientes para ajustar la matriz ni es viable explorarlos, por lo que se recurre a heurísticas. (Sección 25.1)

P: ¿Qué tipo de preguntas se hacen sobre una cadena absorbente frente a una irreducible?
R: En absorbentes: cuánto hasta entrar en un estado absorbente, con qué probabilidad se acaba en cada uno y cuántas visitas a A antes de ser absorbido; en irreducibles: cuál es π, cuántos pasos para aproximarse a π, pasos promedio de A a B y distribución dentro de 5 pasos. (Sección 25.2)

P: ¿Por qué la secuencia más probable de estados ocultos no equivale a elegir el estado más probable en cada instante?
R: Porque la masa de probabilidad puede repartirse entre muchas secuencias, de modo que el óptimo global de la secuencia no coincide con la suma de óptimos individuales de cada Xᵢ. (Sección 25.4–25.5)

P: ¿Por qué Viterbi maximiza el logaritmo de las probabilidades en lugar de las probabilidades directamente?
R: Porque las probabilidades de los caminos son diminutas e indistinguibles de 0 para el computador; usar log convierte el producto en una suma de scores de aristas y nodos. (Sección 25.4–25.5)

P: ¿Por qué en finanzas se modela el logaritmo del precio como movimiento browniano?
R: Para que una caída del 10% pese igual en cualquier precio y para que el precio nunca sea negativo; sirve como modelo nulo sin tendencias ni precio "correcto". (Sección 25.6–25.7)

P: ¿Qué significa que ARIMA sea "mean reverting"?
R: Que existe una fuerza elástica que empuja la variable hacia su media a largo plazo E[X] = c/(1 − φ), de modo que fluctúa alrededor de una línea base en vez de vagar sin rumbo como el browniano. (Sección 25.8–25.10)

P: ¿En qué situaciones un flujo de eventos no es un proceso de Poisson?
R: Cuando un evento precipita otros (contagio), cuando una fuerza externa provoca ráfagas, cuando hay tendencia a espaciado uniforme o cuando hay una población pequeña de eventos que ocurren una sola vez por periodo; los dos primeros (eventos no independientes) son los más problemáticos. (Sección 25.8–25.10)

## Puntos a dominar

- Enunciar la propiedad de Markov y explicar por qué hace tratables las cadenas.
- Construir e interpretar una matriz de transición (entradas ≥ 0, filas suman 1.0) y calcular pasos futuros con p_i·Tᵐ.
- Distinguir cadenas irreducibles aperiódicas (distribución de equilibrio π única) de cadenas absorbentes (procesos que terminan).
- Hallar π resolviendo π = π·T con Σπᵢ = 1, o iterando Tᵐ.
- Reconocer cuándo aplicar MCMC: solo se conoce una puntuación S(θ) proporcional a π.
- Describir la estructura de un HMM y por qué la secuencia más probable no es el máximo estado a estado.
- Explicar la lógica de Viterbi: trellis, log-scores, condicionar sobre el estado anterior y reconstrucción hacia atrás.
- Diferenciar random walk, movimiento browniano y ARIMA, y cuándo cada uno es apropiado.
- Contrastar el significado de π en cadenas discretas (frecuencia de transición) y en tiempo continuo (fracción de tiempo).
- Enumerar las propiedades de un proceso de Poisson y los casos en que no aplica.
