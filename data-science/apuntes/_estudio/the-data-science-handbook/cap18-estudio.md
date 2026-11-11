# Capítulo 18 — Probability (Probabilidad) — Estudio

## Tarjetas de repaso

P: ¿En qué se diferencian probabilidad y estadística según el capítulo? / R: La probabilidad asume un modelo matemático con aleatoriedad y deduce sus consecuencias; la estadística trabaja hacia atrás, infiriendo el proceso real a partir de los datos.

P: ¿Qué es una variable de Bernoulli y cómo se codifican sus resultados? / R: Es el lanzamiento de una moneda (posiblemente sesgada) con probabilidad p de cara y 1−p de cruz, denotada Bernoulli(p); por convención cara = 1 y cruz = 0.

P: ¿Qué restricciones debe cumplir una función de masa de probabilidad válida? / R: Que todos los p_i sean no negativos y que sumen 1.0.

P: ¿Qué distingue a una RV discreta de una continua? / R: La discreta tiene un número finito de resultados o todos listables; la continua puede tomar cualquier valor dentro de un rango y cada resultado exacto tiene probabilidad 0.

P: ¿Qué restricciones debe cumplir una función de densidad (PDF) válida? / R: Que f(x) nunca sea negativa y que el área total bajo la curva sea 1.0.

P: ¿Qué es la CDF y qué propiedades tiene? / R: F(x) da la probabilidad de que la RV sea ≤ x; es no decreciente, tiende a 0 cuando x→−∞ y a 1.0 cuando x crece, y funciona tanto para RV discretas como continuas.

P: ¿Por qué Uniform(0,1) es la distribución más fundamental? / R: Es la base para simular cualquier otra distribución: si se conoce la CDF F_X y su inversa, F_X⁻¹(u) con u de Uniform(0,1) es una muestra de X.

P: ¿Qué son los números pseudoaleatorios y para qué sirve la semilla (seed)? / R: Secuencias deterministas que imitan la aleatoriedad verdadera; fijar la semilla hace el programa reproducible, útil para depurar bugs intermitentes, tests deterministas y comparar implementaciones.

P: ¿Cómo se definen esperanza, varianza y desviación estándar? / R: E[X] (μ_X) es la media; var[X] = E[(X−μ_X)²]; σ_X = √var[X], que mide cuán lejos típicamente está X de su media.

P: ¿Qué significa que dos RV sean independientes y cómo se relaciona con la correlación? / R: Son independientes si conocer una no dice nada de la otra, equivalente a p_xy = p_x·p_y; la independencia es un criterio mucho más fuerte que tener correlación cero.

P: ¿Qué es una distribución de cola pesada (heavy-tailed) y por qué importa? / R: Aquella en la que aparecen valores extremadamente grandes con cierta frecuencia (p. ej. patrimonio neto, tráfico web); rompe la estimación de la media, que puede no converger o no ser un valor típico.

P: ¿Qué modelan la binomial y la Poisson? / R: Binomial(n, p) es el número de caras en n lanzamientos independientes (media np); Poisson modela pocos eventos entre muchísimos posibles e independientes, como límite de una binomial con n grande y p pequeño y np = λ.

P: ¿Por qué es tan importante la distribución normal? / R: Su densidad se concentra en torno a la media con colas muy ligeras, y muchas distribuciones convergen a ella al promediar muestras, según el teorema central del límite.

P: ¿Qué propiedad caracteriza a la distribución exponencial? / R: Es sin memoria (memoryless): por mucho que lleves esperando, el tiempo restante sigue la misma distribución; se usa para el tiempo entre eventos y marca la frontera con las colas pesadas.

P: ¿Cómo se define la entropía y para qué se usa? / R: Mide cuán aleatoria es una RV como E[−ln(p)]; se usa para elegir de forma rigurosa distribuciones de máxima ignorancia bajo restricciones (p. ej. 1/N sobre 1..N, o Uniform(a,b) en un intervalo).

## Preguntas de autoevaluación

P: Con un pago de $5 por cara y −$2 por cruz y p=0.7, ¿cuánto esperas ganar en N lanzamientos? / R: E[payout] = 0.7·5 + 0.3·(−2) = 2.9, es decir, alrededor de 2.9·N dólares. (Sección: Monedas: variables de Bernoulli)

P: ¿Por qué es problemática la visualización de una distribución híbrida y cuál es la mejor solución? / R: Porque un histograma muestra un pico enorme (p. ej. en 0) que aplasta el resto; la mejor solución son dos gráficos: un diagrama de sectores (cuántos valores son 0 vs >0) y un histograma solo de los valores no nulos. (Sección: Variables ni discretas ni continuas)

P: ¿Cómo se obtienen la probabilidad marginal y la condicional a partir de p_xy? / R: La marginal de X se obtiene sumando p_xy sobre todos los y; la condicional de y dado X=x es p_xy dividida por la marginal de x. (Sección: Dependencia, probabilidad marginal y condicional)

P: ¿Por qué la media no es fiable en distribuciones de cola pesada, y qué alternativas hay? / R: Un único outlier enorme puede disparar el promedio y la media puede no converger ni ser un valor típico; la mediana y los cuantiles son robustos, pero a menudo inútiles porque los outliers grandes son lo que interesa. (Sección: Entender las colas)

P: ¿Cómo cambia la binomial al aumentar n? / R: Su media es np y su desviación estándar crece como √n, por lo que la distribución se concentra cada vez más alrededor de np. (Sección: Distribución binomial)

P: ¿Cómo se simula una variable log-normal y por qué la prefiere el autor? / R: Se muestrea x de Normal(μ, σ²) y se toma eˣ; la prefiere porque es fácil de entender y simular y siempre tiene media y desviación finitas, permitiendo outliers grandes con regularidad. (Sección: Distribución log-normal)

P: ¿Por qué el logaritmo aparece en la definición de sorpresa/entropía? / R: Porque se busca una función f de la probabilidad con tres propiedades (f(1.0)=0, f(p)→∞ cuando p→0, y sorpresa conjunta de independientes igual a la suma de sorpresas), que juntas obligan a usar un logaritmo. (Sección: Entropía)

P: ¿Qué parametriza a la Gaussiana multivariante y qué representa su matriz Σ? / R: Un vector μ de dimensión d y una matriz de covarianza Σ de d×d, cuyo componente (i,j) es Cov[X_i, X_j]. (Sección: Gaussiana multivariante)

## Puntos a dominar

- Distinguir el enfoque de la probabilidad (modelo → consecuencias) del de la estadística (datos → modelo).
- Identificar cuándo una RV es discreta, continua o híbrida y describirla con función de masa, PDF o CDF.
- Explicar por qué Uniform(0,1) permite simular otras distribuciones vía la inversa de la CDF, y el papel de la semilla en la reproducibilidad.
- Calcular e interpretar esperanza, varianza y desviación estándar, y distinguir independencia (p_xy = p_x·p_y) de correlación cero.
- Reconocer una distribución de cola pesada y las precauciones al estimar su media.
- Saber cuándo aplicar binomial, Poisson, normal, exponencial y log-normal, y las fortalezas y debilidades de la normal (colas finas, sensibilidad a outliers).
- Relacionar binomial, Poisson y normal con el teorema central del límite.
- Entender la entropía como E[−ln(p)] y su uso para elegir distribuciones de máxima ignorancia bajo restricciones.
