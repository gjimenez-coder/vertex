# The Data Science Handbook — Field Cady (Wiley, 2017)
## Capítulo 18 — Probability (Probabilidad)

> Nota de extracción: texto obtenido de la capa de texto del PDF; las citas usan la página del PDF (PDF p. N). Se conservan solo los fragmentos de código esenciales.

## Lo que necesitas saber

El capítulo da el trasfondo teórico de probabilidad que un data scientist necesita para su trabajo diario: poco en cantidad, pero crucial, porque es la base de casi todo el machine learning y de la mayor parte de la analítica. Cady distingue probabilidad de estadística: la probabilidad describe el mundo con modelos matemáticos que incluyen aleatoriedad y deduce consecuencias asumiendo que el modelo es correcto; la estadística trabaja hacia atrás, infiriendo el proceso real a partir de los datos.

El desarrollo es deliberadamente intuitivo. Arranca con los dos modelos más simples (la moneda de Bernoulli y la uniforme), los usa como motivación para formalizar conceptos (función de masa, densidad, CDF, esperanza, desviación estándar, dependencia y condicionalidad) y termina con un recorrido por las distribuciones clave: binomial, Poisson, normal, normal multivariante, exponencial y log-normal, más una introducción a la entropía.

Sales sabiendo cuándo cada distribución aplica, qué significa que una distribución sea de cola pesada (heavy-tailed) y por qué eso rompe muchos supuestos habituales, y cómo simular variables aleatorias a partir de números pseudoaleatorios y la distribución uniforme.

## Monedas: variables de Bernoulli

El modelo probabilístico más simple es lanzar una moneda (posiblemente sesgada): probabilidad p de cara y 1−p de cruz. Ese lanzamiento es una variable aleatoria (RV) de Bernoulli, denotada Bernoulli(p). La asignación de probabilidades a cada resultado es la función de masa de probabilidad (probability mass function). Por convención, cara = 1 y cruz = 0.

Cuando hay un pago asociado a cada resultado, el pago medio es la esperanza. Con $5 por cara y −$2 por cruz y p=0.7: E[payout] = 0.7·5 + 0.3·(−2) = 2.9; interpretado como que en N lanzamientos (N grande) ganarás alrededor de 2.9·N dólares (PDF p. 264).

Bernoulli generaliza a casos como el dado, donde p_i es la probabilidad del i-ésimo resultado. Las únicas restricciones de una función de masa válida son que todos los p_i sean no negativos y que sumen 1.0. Bernoulli es una RV discreta: tiene un número finito de resultados o todos pueden listarse (incluso si asigna masa a cada entero positivo). La altura humana con precisión arbitraria no es discreta.

## Dardos: variables uniformes

Lo opuesto a lo discreto son las RV continuas, que pueden tomar cualquier valor dentro de un rango. La más simple es la uniforme, Uniform(a,b): siempre está entre a y b y es igualmente probable en cualquier punto del rango. En RV continuas, cada resultado exacto tiene probabilidad 0, pero ciertos rangos son más probables; esa verosimilitud relativa es la función de densidad de probabilidad (PDF). Restricciones de una PDF f válida: f(x) nunca negativa y área total bajo la curva igual a 1.0.

La función de distribución acumulada (CDF), denotada F() frente a la PDF f(), da F(x) = probabilidad de que la RV sea ≤ x. Es no decreciente, tiende a 0 cuando x→−∞ y a 1.0 cuando x crece; sube con fuerza donde f(x) es grande y es plana donde f(x) es 0. La PDF suele ser más fácil de visualizar, pero hay problemas que se resuelven mejor con la CDF.

## La uniforme y los números pseudoaleatorios

Uniform(0,1) es la distribución más fundamental: la más simple y la base para construir otras, tanto en teoría como en la práctica. Si conoces la CDF F_X de X y puedes calcular su inversa F_X⁻¹, entonces F_X⁻¹(u) con u extraído de Uniform(0,1) es una muestra de X. Por eso las librerías de simulación parten del muestreo uniforme. Ejemplos: simular Bernoulli(p) extrayendo u y poniendo cara si u<p; simular un dado sesgado dividiendo [0,1] en seis regiones proporcionales a cada cara; simular una exponencial tomando −log(u).

Técnicamente un computador no puede generar aleatoriedad (es determinista), así que se usan números pseudoaleatorios: se parte de una secuencia de bytes interpretada como un número binario en [0,1] y una función determinista la transforma en otra secuencia sin correlación aparente con la anterior (cambiar un bit puede alterar cualquier bit de salida). Bien diseñados, imitan todas las propiedades de la aleatoriedad verdadera. Su gran ventaja es la semilla (seed): fijar el array inicial hace el programa totalmente reproducible, lo que sirve para depurar bugs intermitentes, reproducir resultados ante escrutinio, escribir tests deterministas y comparar dos implementaciones (prueba de concepto y producción) con la misma entrada.

## Variables ni discretas ni continuas

Existen RV híbridas: por ejemplo, la altura de árboles plantados tiene una masa finita en 0 (los no germinados) y un rango continuo para el resto. En la práctica no supone problema, porque trabajas con datasets finitos; media, mediana u otras métricas se calculan igual. El problema aparece en la visualización: un histograma muestra un pico enorme en 0 que aplasta la campana. La mejor solución son dos gráficos: un diagrama de sectores (cuántos valores son 0 y cuántos >0) más un histograma solo de los valores no nulos. Conceptualmente, una distribución híbrida tiene un pico "infinitamente alto" en la PDF; lo riguroso es la CDF, que salta en cada pico.

## Notación, esperanza y desviación estándar

Se usa mayúscula X para la RV y minúscula x para un valor concreto. Una RV unidimensional se describe con función de masa (discreta) o de densidad (continua), y el concepto generaliza a vectores de d dimensiones. E[X] es la media o valor esperado (μ_X): suma de i·p_i en el caso discreto e integral de x·f(x)·dx en el continuo. Más en general, E[g(X)] = ∫ g(x)·f(x)·dx.

La varianza se define como var[X] = E[(X−μ_X)²] y la desviación estándar σ_X = √var[X], que mide cuán lejos "típicamente" está X de su media. Usar la notación E[g(X)] permite tratar RV discretas y continuas con la misma notación.

## Dependencia, probabilidad marginal y condicional

Con dos RV discretas X e Y y p_xy = Pr[X=x, Y=y], la probabilidad marginal de X se obtiene sumando p_xy sobre todos los y (e igual para Y sobre x): es la distribución al ignorar la otra variable. La probabilidad condicional de y dado X=x es p_xy dividida por la marginal de x; tiene un papel central y explícito en la estadística bayesiana. También se usa E[Y | X=x], estadísticas de Y "condicionadas" al valor de X.

La correlación de X e Y mide el grado de relación lineal (Y=mX+b). X e Y son independientes si conocer una no dice nada sobre la otra, lo que equivale a p_xy = p_x·p_y. La independencia es un criterio mucho más fuerte que tener correlación cero.

## Entender las colas (heavy-tailed)

Una propiedad clave de una distribución es cuán "pesada" es su cola, es decir, con qué frecuencia aparecen valores extremadamente grandes. La altura humana no es de cola pesada (nadie mide más de 10 pies); el patrimonio neto sí lo es (hay algún Bill Gates). Las distribuciones de cola pesada son muy comunes en data science, sobre todo en aplicaciones web (tráfico, pujas en subastas online).

Importan porque rompen muchas operaciones habituales. La media es difícil de estimar: con 100 personas al azar, un multimillonario puede disparar el promedio. Una simulación de muestras Pareto muestra que el promedio de las primeras N muestras no converge: salta al aparecer un outlier enorme y luego decae; si se simulara infinitamente, crecería hacia infinito. Muchas distribuciones reales acaban estabilizándose en una media finita, pero tardan muchísimo. Peor aún: aunque calcules la media, no es un valor "típico" (la mayoría de muestras están por debajo). La mediana y los cuantiles son robustos a colas pesadas, pero a menudo no sirven porque los outliers grandes son precisamente lo que interesa. Conclusión: si un proceso puede ser de cola pesada, modélalo con distribuciones apropiadas y trátalo con cautela.

## Distribución binomial

Binomial(n, p) es el número de caras en n lanzamientos independientes con probabilidad p de cara. Toma valores de 0 a n; su media es np y la masa se concentra allí; su desviación estándar crece como √n, por lo que al aumentar n la distribución se concentra cada vez más alrededor de np. Para una secuencia concreta con k caras, la probabilidad es pᵏ·(1−p)ⁿ⁻ᵏ; falta contar cuántas secuencias dan k caras, que es "n sobre k" = n! / (k!·(n−k)!), donde x! es el factorial. En NumPy:

```python
import numpy as np
sample = np.random.binomial(200, 0.3)
```

## Distribución de Poisson

Modela sistemas con muchísimos eventos posibles e independientes, de los que en promedio solo ocurren unos pocos (p. ej., visitas diarias a una web: miles de millones de personas podrían entrar, pero solo entran unos cientos). Surge como límite de una Binomial(n, p) con n muy grande y p pequeño manteniendo np = λ constante; su función de masa es p_k = e⁻λ·λᵏ/k!. En NumPy: `np.random.poisson(200)`.

## Distribución normal (Gaussiana)

Si hay una distribución que conocer, es la normal o Gaussiana: la clásica campana, parametrizada por media μ y desviación σ, denotada N(μ, σ²). Su propiedad práctica más importante es que la densidad se concentra fuertemente en torno a la media, con colas muy ligeras y outliers extremadamente improbables; por eso puede ser peligroso ajustar una normal ingenuamente, y es común identificar y eliminar outliers antes de ajustarla.

Es famosa porque muchas distribuciones convergen a ella al promediar suficientes muestras (binomial, Poisson y casi cualquier otra con media y desviación finitas). Esto lo recoge el teorema central del límite: para X con media μ y desviación σ finitas y muestras independientes X₁…Xₙ, la media de n muestras se distribuye normalmente alrededor de μ cuando n→∞.

## Gaussiana multivariante

La mayoría de distribuciones del capítulo son univariantes y no generalizan de forma destacable, pero la normal sí: se define para cualquier número d de dimensiones, con densidad en forma de "colina" elipsoidal que pica en la media, y los elipsoides pueden estirarse en cualquier dirección (no solo a lo largo de los ejes). Se parametriza con un vector μ de dimensión d y una matriz Σ de d×d, la matriz de covarianza, cuyo componente (i,j) es Cov[X_i, X_j]. Tiene las mismas fortalezas (conveniencia matemática, convergencia) y debilidades (colas muy finas, sin outliers grandes) que la univariante.

## Distribución exponencial

Aparece en muchos sitios, pero es más útil para modelar el tiempo hasta que ocurre un evento o el tiempo entre eventos. Si en cada instante hay una probabilidad fija y pequeña de que llegue alguien a una tienda, independiente de los demás instantes, el tiempo entre llegadas es exponencial. Se parametriza por su media θ (tiempo medio entre eventos) o, a veces, por la tasa λ = 1/θ. En NumPy: `np.random.exponential(10)`.

Su propiedad clave es que es sin memoria (memoryless): por mucho que lleves esperando, el tiempo restante sigue la misma distribución exponencial. La exponencial suele tomarse como la línea divisoria entre distribuciones de cola pesada y las que no lo son. En contraste, la edad no es de cola pesada (alguien de 20 probablemente viva 20 años más, uno de 90 no), mientras que el patrimonio neto sí lo es (si alguien tiene al menos $10 millones, es probable que tenga muchos más).

## Distribución log-normal

Es la distribución de cola pesada preferida del autor: fácil de entender y simular, y siempre con media y desviación finitas (cierto para casi todos los fenómenos reales). Tiene un pico definido por encima de 0; a la izquierda cae rápido hasta 0 en x=0, y a la derecha decae gradualmente, permitiendo outliers grandes con regularidad. Se entiende así: muestrea un valor x de Normal(μ, σ²); entonces eˣ es log-normal. En NumPy: `np.random.lognormal(mu, sigma)`.

## Entropía

La entropía mide "cuán aleatoria" es una RV; viene de la teoría de la información. Una moneda justa es más aleatoria que una que sale cara el 99% de las veces, y una normal con σ pequeña es menos aleatoria que una con σ grande. La intuición: algunos resultados son más "sorprendentes" que otros, y la entropía es E[Surprise[X]]. La sorpresa de X=x se define como −ln(p_x), de modo que para una RV discreta H[X] = −Σ p_x·ln(p_x), y para una continua H[X] = −∫ f(x)·ln(f(x))·dx.

El logaritmo no es arbitrario: se busca una función f de la probabilidad con tres propiedades: f(1.0)=0, f(p)→∞ cuando p→0, y para variables independientes la sorpresa conjunta es la suma de sorpresas; juntas obligan a usar un logaritmo. La entropía se usa sobre todo para elegir, de forma rigurosa, una distribución que refleje gran ignorancia: sobre los números 1 a N, la de máxima entropía asigna 1/N a cada uno; sobre un intervalo [a,b], es Uniform(a,b). La maximización siempre requiere restricciones. Además, las definiciones discreta y continua no son equivalentes: aplicar la discreta a una uniforme dividiéndola en n intervalos da ln(n), que diverge, porque nunca podrías acertar el valor exacto de una RV continua. Rara vez calcularás entropía en el trabajo diario, pero es ubicua en la construcción y las propiedades teóricas de las herramientas.

## Ideas clave

- La probabilidad asume un modelo y deduce consecuencias; la estadística infiere el modelo a partir de los datos.
- Las RV discretas se describen con función de masa y las continuas con PDF; la CDF, F(x)=Pr[X≤x], funciona para ambas.
- Uniform(0,1) es la base para simular cualquier otra distribución vía la inversa de la CDF; los computadores usan números pseudoaleatorios, reproducibles fijando la semilla.
- E[X] es la media; var[X]=E[(X−μ)²] y σ=√var miden la dispersión típica.
- La independencia (p_xy = p_x·p_y) es mucho más fuerte que correlación cero.
- Las distribuciones de cola pesada (patrimonio, tráfico web) rompen la media; la mediana y los cuantiles son robustos pero a veces inútiles.
- Binomial (número de caras en n tiradas), Poisson (eventos raros entre muchos posibles, límite de la binomial) y normal (campana con colas finas, meta del teorema central del límite) son las distribuciones esenciales.
- La exponencial es sin memoria y marca el límite con las colas pesadas; la log-normal (eˣ con x normal) es una cola pesada manejable con media finita.
- La entropía mide la aleatoriedad como E[−ln(p)] y guía la elección de distribuciones de máxima ignorancia bajo restricciones.
