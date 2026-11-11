# The Data Science Handbook — Field Cady (Wiley, 2017)
## Capítulo 25 — Stochastic Modeling (Modelado estocástico)

> Nota de extracción: el texto se obtuvo de la capa de texto del PDF y las citas usan la página del PDF `(PDF p. N)`.

## Lo que necesitas saber
El modelado estocástico agrupa herramientas de probabilidad para estudiar no una sola variable aleatoria, sino un proceso que ocurre de forma aleatoria a lo largo del tiempo: el precio de una acción, las visitas a una página web o una máquina que cambia de estado durante su operación. No hace falta que la variable sea el tiempo; sirve cualquier cosa secuencial, como qué palabras siguen a otras en un texto, los cambios de una generación a la siguiente o la variación de temperatura en un terreno.

El capítulo es un recorrido por los principales modelos probabilísticos, empezando por el más importante: la cadena de Markov. Explica cómo se relacionan entre sí, qué situaciones describen y qué problemas permiten resolver. A partir de las cadenas de Markov se construyen modelos más avanzados (MCMC, HMM con el algoritmo de Viterbi) y se presentan procesos complementarios: random walks, movimiento browniano, ARIMA, procesos de Markov en tiempo continuo y procesos de Poisson.

Sales sabiendo qué es la propiedad de Markov, la diferencia entre cadenas irreducibles aperiódicas y absorbentes, cómo hallar la distribución de equilibrio, cómo inferir estados ocultos y qué proceso usar según el fenómeno que modelas.

## Cadenas de Markov (25.1)
Una cadena de Markov es una secuencia de variables aleatorias X₁, X₂, … interpretadas como el estado de un sistema en instantes sucesivos. Inicialmente se asume que las Xᵢ son discretas con un número finito de valores. La propiedad definitoria —la "propiedad de Markov"— es que la distribución de Xᵢ₊₁ puede depender de Xᵢ, pero es independiente de todas las anteriores si se conoce Xᵢ:

Pr(Xᵢ₊₁ | X₁, X₂, …, Xᵢ) = Pr(Xᵢ₊₁ | Xᵢ)

La imagen mental del autor es una rana amnésica que salta entre nenúfares: sabe en cuál está (eso determina las probabilidades de su próximo salto), pero no recuerda dónde estuvo antes ni cuánto lleva saltando.

Con k estados, las probabilidades de transición se ordenan en una matriz k×k: la fila i es "estar en el estado i" y la entrada j de esa fila es la probabilidad de saltar a j. Toda entrada es ≥ 0 y cada fila suma 1.0. Conocer la matriz de transición T y la distribución inicial de X₁ caracteriza por completo la cadena. El ejemplo del clima: un día soleado tiene 80% de probabilidad de ser seguido por otro soleado; tras lluvia es 50/50.

Si p es el vector de estado (fila k×1), la distribución del siguiente paso es p_{i+1} = p_i·T, y en general p_{i+m} = p_i·Tᵐ. La propiedad de Markov es la clave de que las cadenas sean tratables matemática y computacionalmente.

Cuando la propiedad no se cumple —por ejemplo, modelar lenguaje natural con un solo contexto de palabra es insuficiente— se usa una cadena de orden m: Xᵢ₊₁ depende de varios valores previos. Una cadena de orden m equivale a una de orden 1 con kᵐ estados. En lenguaje natural a escala industrial es común m = 6, lo que da un número de estados astronómico: con tantos estados no hay datos suficientes para ajustar la matriz ni es computacionalmente viable explorarlos, y se recurre a heurísticas y optimizaciones.

## Dos tipos de cadenas, dos tipos de preguntas (25.2)
La mayoría de cadenas prácticas son de dos tipos. Una cadena **irreducible aperiódica** cumple que: (1) se puede llegar de cualquier estado a cualquier otro en un número finito de pasos; y (2) ningún estado es periódico. Esto garantiza un comportamiento de estado estacionario único, la "distribución de equilibrio" π, un vector de k probabilidades donde la componente i es la probabilidad de estar en el estado i. El clima y el lenguaje natural son ejemplos: a largo plazo, el estado de hoy deja de importar.

Para hallar π se resuelve la ecuación de álgebra lineal π = π·T con la restricción Σπᵢ = 1. Una forma aproximada y conceptualmente simple (aunque costosa) es multiplicar T por sí misma repetidamente: en el límite de m grande, p_{i+m} converge a π sin importar p_i, de modo que las filas de Tᵐ terminan siendo aproximadamente iguales a π.

En una cadena **absorbente** existe al menos un estado que va a sí mismo con probabilidad 1.0 (si la rana cae ahí, se queda para siempre). Modela procesos que terminan: un visitante web que acaba en "compró" o "abandonó el sitio", la vida de una máquina que se avería o un paciente. A veces se añade un estado absorbente "el mensaje terminó" al modelar textos cortos como correos o mensajes.

Con cadenas irreducibles se pregunta: ¿cuál es la distribución de equilibrio π?, ¿cuántos pasos hasta aproximarse a π?, ¿cuántos pasos en promedio de A a B?, ¿cuál es la distribución dentro de 5 pasos? Con cadenas absorbentes: ¿cuánto hasta entrar en un estado absorbente?, ¿con qué probabilidad acabo en cada uno?, ¿cuántas veces visito A antes de ser absorbido?

## Markov Chain Monte Carlo (25.3)
MCMC es una aplicación avanzada de las cadenas de Markov, ya vista al estimar los parámetros θ de una red bayesiana. Se dispone de una función de puntuación S(θ) = Pr(θ)·Pr(Datos|θ) que no define una distribución (no suma 1), pero que es proporcional a la distribución objetivo π sobre los valores de θ. Conocemos S(θ), no la constante de proporcionalidad.

La solución general es una simulación MCMC: genera una secuencia de muestras θᵢ que forman una cadena de Markov cuya distribución estacionaria es π. Con suficientes muestras se obtiene un muestreo representativo de π para estimar promedios u otros estadísticos. A grandes rasgos: a partir de θᵢ se añade una perturbación aleatoria Δ y se forma un candidato Φ = θᵢ + Δ; usando Score(θᵢ) y Score(Φ) se acepta Φ como θᵢ₊₁ probabilísticamente o se prueba otro Δ. Así θᵢ₊₁ depende solo de θᵢ. Si se acepta/rechaza de forma adecuada y Δ permite alcanzar cualquier θ desde cualquier otro, el estado estacionario está garantizado que es π; un muestreo inteligente de Δ acelera la convergencia y hace las muestras más independientes.

## Modelos ocultos de Markov y Viterbi (25.4–25.5)
Un modelo oculto de Markov (HMM) tiene una cadena de Markov subyacente Xᵢ (los "estados ocultos") y observaciones Yᵢ que dependen solo de su Xᵢ asociado. Ejemplo de texto borroso: los Xᵢ son las palabras correctas y los Yᵢ las imágenes difusas; aunque un trozo se parezca más a "quick", el contexto ("the duck said…") hace más probable "quack". Otro ejemplo: dos monedas (una justa, otra sesgada a 90% caras) con 10% de probabilidad de cambiar de moneda tras cada lanzamiento; Xᵢ indica qué moneda se usó e Yᵢ si salió cara.

Un HMM se caracteriza por: la distribución inicial de X₁, la matriz de transición de los Xᵢ y la probabilidad condicional Pr(Y|X). La pregunta más habitual es cuál es la **secuencia más probable** de los Xᵢ dadas las observaciones Yᵢ. Ojo: no es lo mismo que elegir el valor más probable de cada Xᵢ por separado; la masa de probabilidad puede repartirse entre muchas secuencias. Los HMM brillan cuando las observaciones son muy ambiguas pero los Xᵢ cambian rara vez; implícitamente asumen que el tiempo que X mantiene un valor sigue una distribución geométrica, suposición fuerte que suele no molestar si las permanencias son largas.

El **algoritmo de Viterbi** halla esa secuencia óptima. Se visualiza con un "trellis diagram" que muestra todos los estados ocultos y sus transiciones; una secuencia es un camino por el grafo. Como las probabilidades de los caminos son diminutas (indistinguibles de 0 para el computador), se maximiza el logaritmo: el score de un camino es la suma de los scores de sus aristas (log de la transición) y nodos (log de la observación).

Se definen P(i, x) como el camino de mayor score que termina en Xᵢ = x, y S(i, x) su score. La idea clave es condicionar sobre el estado anterior: P(i, Fair) es, entre venir de Fair o de Biased, el que tenga mayor score. Así el problema en la capa i se reduce a la capa i−1. El algoritmo recorre el trellis capa a capa rellenando todos los S(i, x) y guardando el "padre" de cada nodo; al final reconstruye la secuencia hacia atrás desde el nodo de mayor score. El autor lo describe como el algoritmo más complicado del libro.

## Random walks y movimiento browniano (25.6–25.7)
Un **random walk** (o "paseo del borracho") parte de X₁ (normalmente 0) y en cada paso sube 1 con probabilidad p o baja 1 con probabilidad 1 − p. Con p = 0.5 es "unbiased": el caminante deambula sin rumbo, pasa por el origen infinitas veces, su posición media es 0 y su distancia media al origen crece como la raíz cuadrada del número de pasos (cada paso es Bernoulli(p)).

El **movimiento browniano** generaliza el random walk de los enteros a los reales: Xᵢ₊₁ − Xᵢ = Normal(0, σ²), con σ como único parámetro. Fue el primer proceso estocástico estudiado a fondo (una partícula suspendida en un líquido). Su rasgo notable es que la diferencia entre posiciones no consecutivas sigue siendo browniano, solo que más disperso: Xᵢ₊ₜ − Xᵢ = Normal(0, t·σ²). Por el Teorema Central del Límite, casi cualquier movimiento aleatorio no sesgado a escala pequeña da lugar a browniano a gran escala. En finanzas se usa como hipótesis nula: para que una caída del 10% pese igual a cualquier precio y el precio nunca sea negativo, se toma X como el logaritmo del precio. No es un modelo preciso de precios reales, pero es un modelo nulo común sin tendencias ni precio "correcto".

## ARIMA, procesos en tiempo continuo y procesos de Poisson (25.8–25.10)
El problema del browniano para ciencia de datos es que vaga sin un valor "normal", pero los procesos reales suelen tener una línea base alrededor de la cual oscilan (el precio de un valor fluctúa pero no demasiado). Este comportamiento es "mean reverting": una fuerza elástica que empuja la variable hacia su media. El modelo clásico es **ARIMA** (autoregressive moving average). Su forma habitual con un solo término es:

X_{i+1} = c + φ·X_i + Normal(0, σ²), con 0 < φ < 1

que tiene valor medio a largo plazo E[X] = c/(1 − φ): X fluctúa a su alrededor y siempre es devuelto a la media.

Los **procesos de Markov en tiempo continuo** levantan la limitación de los pasos discretos: el sistema puede cambiar de estado en cualquier momento (un servidor web recibe o pierde visitantes en cualquier instante). Se describen con tasas λᵢⱼ de i a j: en un intervalo pequeño Δ, Pr(X_{t+Δ} = j | X_t = i) = λᵢⱼ·Δ. La evolución es d/dt p(t) = p(t)·Λ, con Λ la matriz de tasas (0 en la diagonal), y π se obtiene de π·Λ = 0 con Σπᵢ = 1. Diferencia crítica: en cadenas discretas π mide con qué frecuencia se transiciona a cada estado; en continuas mide la fracción del tiempo total en cada estado (no es lo mismo, porque mucha masa puede entrar y salir rápido). Ambas matrices requieren entradas no negativas, pero en las discretas cada fila suma 1 y en las continuas las sumas son irrelevantes mientras la diagonal sea 0.

Un **proceso de Poisson** modela un flujo de eventos a intervalos aleatorios, caracterizado por λ (eventos promedio por unidad de tiempo) o θ = 1/λ (tiempo medio entre eventos). Propiedades: los tiempos entre eventos son exponenciales con media θ; los tiempos consecutivos son independientes; en un intervalo de longitud T el número de eventos sigue una Poisson de media λT; e intervalos no solapados tienen cuentas independientes. No son Poisson los sistemas donde un evento precipita otros (contagio), donde una fuerza externa provoca ráfagas, donde hay tendencia a espaciado uniforme (reemplazo de piezas desgastadas) o donde hay una población pequeña de eventos que ocurren una sola vez por periodo. Los dos primeros casos, cuya clave es que los eventos no son independientes, suelen ser los más problemáticos en la práctica.

## Ideas clave
- La propiedad de Markov: Xᵢ₊₁ depende solo de Xᵢ; es lo que hace tratables las cadenas. Una cadena de orden m equivale a una de orden 1 con kᵐ estados.
- Las cadenas irreducibles aperiódicas tienen una distribución de equilibrio única π, que se halla con π = π·T (o iterando Tᵐ); las absorbentes modelan procesos que terminan.
- MCMC genera muestras θᵢ cuya distribución estacionaria es la distribución objetivo π, útil cuando solo se conoce una función de puntuación proporcional a ella.
- Un HMM infiere estados ocultos Xᵢ a partir de observaciones Yᵢ; la secuencia más probable no coincide con el valor más probable de cada estado por separado.
- El algoritmo de Viterbi recorre un trellis capa a capa maximizando log-scores y reconstruye la secuencia óptima guardando el "padre" de cada nodo.
- Random walk, movimiento browniano y ARIMA modelan trayectorias numéricas; ARIMA añade reversión a la media (E[X] = c/(1 − φ)).
- En cadenas discretas π mide frecuencia de transición; en procesos de tiempo continuo mide fracción de tiempo en cada estado.
- Un proceso de Poisson supone eventos independientes con tiempos entre eventos exponenciales; no sirve cuando hay contagio, ráfagas, espaciado uniforme o poblaciones finitas de eventos.
