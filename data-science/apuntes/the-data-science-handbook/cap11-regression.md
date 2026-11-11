# The Data Science Handbook — Field Cady (Wiley, 2017)
## Capítulo 11 — Regression (Regresión)

> Nota de extracción: texto obtenido de la capa de texto del PDF; las citas indican la página como (PDF p. N).

## Lo que necesitas saber

La regresión es como la clasificación, pero la variable de salida es un número real en lugar de una categoría. El capítulo presenta las técnicas de regresión más habituales en machine learning y cómo evaluar su rendimiento. Cady distingue dos familias: modelar la salida como una combinación lineal de las entradas, con mucha matemática elegante y formas principiadas de tratar patologías de los datos, y una serie de "ugly hacks" para lo no lineal.

Una decisión poco convencional del autor es incluir el ajuste de una línea o curva a datos bidimensionales dentro del capítulo de regresión. Aunque el curve fitting no suele presentarse en el contexto de machine learning, matemáticamente es lo mismo: se asume una forma funcional de la salida en función de las entradas (p. ej. `y = m1·x1 + m2·x2`) y se eligen los parámetros para que se ajusten lo mejor posible a los datos de entrenamiento. La diferencia es un accidente histórico: ajustar curvas se desarrolló mucho antes del machine learning e incluso de los computadores.

Al terminar el capítulo sabrás ajustar líneas y curvas por mínimos cuadrados, cuándo usar la penalización L1 frente a los cuadrados, cómo medir la bondad del ajuste con R² y correlación, cómo detectar si la forma funcional elegida fue acertada mediante la correlación de residuos, y cómo LASSO ayuda a seleccionar variables penalizando pesos distintos de cero.

## El ejemplo que recorre el capítulo

El hilo conductor es un dataset con mediciones fisiológicas de 442 pacientes de diabetes, cuyo objetivo es un indicador de la progresión de la enfermedad. Un script en Python entrena dos modelos sobre los mismos datos —regresión lineal y LASSO— y compara sus resultados mediante scatterplots de predicho frente a real, además de la correlación y el R². Este ejemplo reaparece en varias secciones para ilustrar los coeficientes, el sobreajuste y la selección de variables.

## Ejemplo: predicción de la progresión de la diabetes

El script carga el dataset con `sklearn.datasets.load_diabetes()`, normaliza las entradas, separa entrenamiento y test, y ajusta `LinearRegression` y `Lasso`. Para cada modelo calcula la correlación entre predicciones y valores reales y el R² con `r2_score`, y dibuja un scatterplot con la recta `x = y` de referencia. Los resultados reportados fueron: regresión lineal Corr = 0.660, Rsq = 0.396; LASSO Corr = 0.677, Rsq = 0.445.

## Mínimos cuadrados (Least Squares)

El ejemplo más simple de regresión es ajustar una línea `y = m·x + b` a pares x/y. El autor recuerda el quartet de Anscombe, cuatro datasets con la misma recta de mejor ajuste y la misma calidad de ajuste según los métodos estándar, para subrayar que el ojo humano detecta outliers y patologías que los números esconden. Pero se necesita un método objetivo que un computador pueda aplicar sin intervención humana.

El método estándar es least squares, disponible en la clase `LinearRegression`, cuyos coeficientes se obtienen con `lm.coef_` (m) y `lm.intercept_` (b). Minimiza una función de penalización que suma el cuadrado del error en cada punto:

```
L = Σ (y_i − (m·x_i + b))²
```

Elevar al cuadrado hace a least squares extremadamente sensible a outliers: tres desviaciones de tamaño 5 dan una penalización de 75, pero una sola desviación de tamaño 10 da 100. El modelo doblará los parámetros para evitar grandes desviaciones de un único punto, lo que lo hace inadecuado cuando se esperan unas pocas desviaciones grandes.

La alternativa es la penalización L1, que suma los valores absolutos de los errores:

```
L = Σ |y_i − (m·x_i + b)|
```

Los outliers siguen influyendo, pero menos que en least squares. A cambio, L1 castiga más las desviaciones pequeñas y es bastante más complicada de implementar computacionalmente.

## Ajuste de curvas no lineales

Ajustar una curva a datos es ubicuo en ciencia e ingeniería; a menudo hay razones a priori para esperar una forma funcional concreta, y extraer los parámetros de mejor ajuste dice algo significativo sobre el sistema. Formas habituales que menciona: decaimiento exponencial hacia una línea base (`y = a·e^(−bx) + c`), crecimiento exponencial (`y = a·e^(bx)`), crecimiento logístico (útil en biología para poblaciones en entornos limitados) y polinomios de distintos grados.

El enfoque típico sigue siendo mínimos cuadrados, minimizando `L = Σ (y_i − f(x_i))²`. En Python se usa `curve_fit` de SciPy, que recibe una función definida por el usuario (toma x y parámetros y devuelve el valor), junto con los x e y de los datos; mediante optimización por prueba y error busca los parámetros que minimizan el error, y devuelve una tupla con los mejores parámetros y una matriz de su varianza.

```python
from scipy.optimize import curve_fit
def calc(x, a, b):
    return a + b*x*x
cf = curve_fit(calc, xs, ys)
best_fit_params = cf[0]
```

Ajustando datos de la forma `y = 2 + 3x²`, el autor recupera a ≈ 2.34 y b = 3, buen resultado. Advierte que los ajustes no lineales son muy lentos y que los algoritmos numéricos a veces fallan dando resultados incorrectos. Lo mejor, si se puede, es transformar el problema en uno lineal (por ejemplo ajustando el logaritmo de los datos); si no, conviene aportar una conjetura inicial mediante el parámetro opcional `p0`.

## Bondad del ajuste: R² y correlación

Al evaluar una curva ajustada hay dos preguntas: ¿con qué precisión predecimos valores? y ¿fue buena la suposición sobre la forma funcional? Para la primera, la medida estándar es R², descrito a menudo como la fracción de la varianza explicada por el modelo. Un valor de 1.0 es ajuste perfecto y 0 significa que no se captó nada de la variación; incluso puede ser negativo en algunas definiciones.

R² se basa en dos conceptos: la variación total `TV = Σ (y_i − ȳ)²`, donde ȳ es la media de los valores y, y la variación residual `RV = Σ (y_i − f(x_i))²`. La definición es:

```
R² = 1 − (RV / TV)
```

Es decir, la fracción de toda la variación capturada por el modelo. R² = 0 corresponde a definir la función ajustada como la media constante de y, `f(x) = ȳ`, la forma más burda de ajustar; hacerlo peor que eso vuelve R² negativo. En el script se calcula con `r2_score(Y_test, preds_linear)`.

Otra vía es tomar directamente la correlación entre valores predichos y conocidos del test, con la ventaja de poder elegir Pearson, Spearman o Kendall según cómo tratar los outliers. Su límite: la correlación mide si predicciones y objetivos están relacionados, pero no si realmente coinciden.

## Correlación de residuos

Normalmente no se cuestiona si la forma funcional supuesta era la "correcta", pero en datos bidimensionales sí puede evaluarse. La forma más simple es dibujar los datos conocidos frente a la curva de valores predichos y ver si encajan: en el quartet de Anscombe se ve claro que un modelo lineal es adecuado para el primer dataset y equivocado para el segundo.

Para cuantificarlo está la correlación de residuos. Si la forma del modelo es correcta, los datos observados deberían ser la fórmula de mejor ajuste más ruido aleatorio, cayendo al azar por encima o por debajo de la curva. Si la forma es mala, aparecen tramos largos donde los datos están sistemáticamente por encima o por debajo. Por ello se ordenan los puntos por x y se calcula la correlación entre residuos consecutivos: una correlación cercana a 0 indica que la forma era buena y que el fallo predictivo viene del ruido real, no de una forma funcional equivocada.

## Regresión lineal

La regresión lineal es el mismo proceso que ajustar una línea, pero generalizado a d características de entrada: `y = b + m1·x1 + m2·x2 + … + md·xd`. Casi todo lo anterior se traslada directamente: se ajusta por mínimos cuadrados y se evalúa con R² y con la correlación entre predicho y real.

La diferencia práctica es que ya no es viable dibujar la curva predicha sobre los datos; en su lugar se hace un scatterplot entre los valores reales del test y los predichos. Esto permite ver si el modelo rinde mejor para valores grandes o pequeños y si sufre outliers. En el ejemplo, la correlación entre predicho y real es clara pero tenue: hay varios puntos cuyo valor real está muy por debajo de lo predicho (diabetes menos dañina de lo esperado), y la recta de ajuste parece algo más plana que los datos, lo que sugiere puntos anómalamente bajos que tiran de las predicciones hacia abajo.

La regresión lineal también sirve para identificar variables interesantes. Como el script usó `normalize()` para escalar las características a media 0 y desviación 1, el tamaño relativo de los pesos indica su relación con la progresión de la diabetes. Al imprimir `linear.coef_`, la tercera y la cuarta características destacan como las más interesantes para examinar más de cerca.

## Regresión LASSO y selección de variables

El problema de la regresión lineal es que casi todos los coeficientes son grandes, lo que dificulta precisar qué variables importan y, sobre todo, apunta a sobreajuste: muchos coeficientes moderados pueden compensarse entre sí, mejorando ligeramente el ajuste sobre el entrenamiento pero generalizando muy mal.

La idea de LASSO es ajustar igualmente un modelo lineal pero penalizando los pesos distintos de cero. Recibe un parámetro `alpha` que indica cuán severamente se castigan esos pesos; con `alpha = 0` se reduce a regresión lineal, y el valor por defecto usado en el script es 1.0. El scatterplot de LASSO se pega más a la línea central, lo que, junto con un R² y una correlación mayores (0.445 y 0.677 frente a 0.396 y 0.660), confirma que el modelo lineal estaba sobreajustando.

La diferencia salta al mirar `lasso.coef_`: cuatro de las características tienen peso exactamente 0, y de las restantes queda claro que la tercera es la más relevante para la progresión de la diabetes, seguida de la cuarta y la novena.

## Ideas clave

- La regresión predice una salida real; ajustar curvas y la regresión de ML son matemáticamente lo mismo: asumir una forma funcional y elegir parámetros que ajusten "lo mejor posible".
- Least squares minimiza la suma de cuadrados de los residuos y es muy sensible a outliers; la penalización L1 (suma de valores absolutos) es más robusta pero más costosa.
- Para ajustes no lineales se usa `curve_fit`; son lentos y frágiles, así que conviene linealizar el problema o dar una conjetura inicial `p0`.
- R² = 1 − (RV/TV) es la fracción de varianza explicada; puede ser negativo y R² = 0 equivale a predecir siempre la media.
- La correlación entre predicho y real es otra medida de bondad, pero indica relación, no coincidencia exacta.
- La correlación de residuos (ordenados por x) detecta si la forma funcional supuesta era la correcta: cercana a 0 es buena señal.
- En regresión lineal con características normalizadas, el tamaño de los coeficientes revela qué variables importan más.
- LASSO penaliza pesos no nulos (parámetro `alpha`), combate el sobreajuste y lleva muchos coeficientes a 0, sirviendo como selección de variables.
