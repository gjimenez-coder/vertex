# Exponential smoothing (Suavizado exponencial) — Estudio

## Tarjetas de repaso

P: ¿Qué idea básica define al suavizado exponencial?
R: Ponderar las observaciones pasadas con pesos que decaen geométricamente, de modo que lo más reciente pesa más.

P: ¿Qué papel cumple el parámetro α en SES?
R: Controla la velocidad de decaimiento de los pesos; con α mayor (p. ej. 0.8) lo reciente pesa más, con α menor (0.2) el decaimiento es más lento. Rango: 0 ≤ α ≤ 1.

P: ¿Cómo son las ecuaciones de SES en forma de componentes?
R: Pronóstico ŷ_{t+h|t} = ℓ_t y suavizado ℓ_t = α y_t + (1−α) ℓ_{t−1}.

P: ¿Por qué los pronósticos de SES a varios pasos son constantes?
R: Sin tendencia ni estacionalidad el pronóstico es una media constante, por lo que la función de pronóstico es plana.

P: ¿Qué añade el método de Holt (1957) respecto a SES?
R: Una segunda ecuación y un segundo parámetro β* para modelar la tendencia: ŷ_{t+h|t} = ℓ_t + h b_t, con ℓ_t el nivel y b_t la pendiente.

P: ¿Qué hace la tendencia amortiguada (damped) y qué parámetro la gobierna?
R: Un parámetro 0 < φ < 1 amortigua la tendencia para ser más conservador; el corto plazo tiene tendencia y el largo plazo es constante. Con φ=1 coincide con Holt lineal.

P: ¿Qué añaden los métodos de Holt-Winters?
R: Una tercera ecuación de suavizado para la estacionalidad (parámetro γ, periodo m), en versiones aditiva y multiplicativa, y con variante amortiguada.

P: ¿Qué significa la notación ETS(Error, Trend, Seasonal)?
R: Error = {A, M}, Trend = {N, A, Ad, M, Md}, Seasonal = {N, A, M}; clasifica los métodos de suavizado como modelos de espacio de estados con innovaciones.

P: ¿Cuántos métodos y cuántos modelos ETS existen?
R: 15 métodos de suavizado (por Trend × Seasonal) y 30 modelos ETS al distinguir error aditivo y multiplicativo.

P: ¿Qué diferencia hay entre error aditivo y multiplicativo en ETS?
R: Dan los mismos pronósticos puntuales pero distintos intervalos de pronóstico; la única diferencia está en la ecuación de observación.

P: ¿Qué es un modelo de "fuente única de error" (innovaciones)?
R: Un modelo donde el mismo proceso ε_t ~ NID(0,σ²) alimenta tanto la ecuación de observación como las de los estados (en ETS(A,N,N) el error e_t coincide con la innovación ε_t).

P: ¿Cómo se estiman los parámetros y estados iniciales en ETS?
R: Por MLE, minimizando la función de verosimilitud L* (equivalente a −2 log(verosimilitud) + constante); no hay solución cerrada y se usa optimización numérica.

P: ¿Qué criterios se usan para seleccionar modelo y cómo interpretarlos?
R: AIC = −2 log(Likelihood) + 2p, su corrección AICc para muestras pequeñas, y BIC; se minimiza el AIC. Solo tiene sentido comparando modelos sobre los mismos datos y diferencias ≤ 2 no son sustanciales.

P: ¿Cuándo no se pueden usar modelos con error multiplicativo?
R: Con datos que contienen ceros o valores negativos; exigen datos estrictamente positivos, y en caso contrario solo valen los seis modelos totalmente aditivos.

P: ¿Qué hace la función `ets()` en R?
R: Elige automáticamente un modelo por AIC/AICc/BIC, maneja cualquier combinación de tendencia, estacionalidad y amortiguamiento, asegura parámetros admisibles y produce intervalos de pronóstico.

## Preguntas de autoevaluación

P: ¿Qué representa el pronóstico ŷ_{T+h|T} en la perspectiva de espacio de estados y por qué se distingue de los datos observados?
R: Es la esperanza condicional E(y_{T+h}|x_T); el marco separa los datos observados (y₁,…,y_T) del estado no observado (x₁,…,x_T), y define la varianza del pronóstico como Var(y_{T+h}|x_T). (Sección: La perspectiva de espacio de estados)

P: ¿Por qué Holt casi siempre tiene mejor RMSE dentro de muestra que SES y por qué eso no basta para preferirlo?
R: Porque se optimiza con un parámetro más, pero un mejor ajuste dentro de muestra no garantiza mejor desempeño; la comparación útil es el RMSE fuera de muestra con un conjunto de prueba. (Sección: Métodos con tendencia)

P: ¿Cómo se comporta el pronóstico de la tendencia amortiguada cuando h→∞?
R: Tiende a ŷ_{T+h|T} → ℓ_T + φ b_T/(1−φ), de modo que el corto plazo conserva tendencia y el largo plazo se vuelve constante. (Sección: Métodos con tendencia)

P: ¿Por qué el marco ETS resuelve el problema de elegir entre tantos métodos?
R: Porque los modelos de espacio de estados con innovaciones son procesos generadores de datos estocásticos que describen toda la distribución de pronóstico, lo que permite una selección "propia" de modelo por criterio de información (y se desarrolló para pronosticar automáticamente miles de productos farmacéuticos). (Sección: Taxonomía y modelos ETS)

P: ¿Cuál es la diferencia estructural entre un modelo ETS con error aditivo y uno con error multiplicativo?
R: Con error aditivo k(x)=1 e y_t = μ_t + ε_t; con error multiplicativo k(x_{t−1})=μ_t e y_t = μ_t(1+ε_t). La única diferencia está en la ecuación de observación. (Sección: Taxonomía y modelos ETS)

P: ¿Qué diferencias de región de parámetros existen entre la restricción "usual" y la "admisible"?
R: La usual interpreta medias ponderadas (0<α<1, 0<β<α, 0<γ<1−α, 0.8<φ<0.98); la admisible evita que el pasado lejano siga influyendo y suele ser menos restrictiva (p. ej. ETS(A,N,N) admite 0<α<2). (Sección: Estimación y selección de modelo)

P: ¿Cómo se obtienen los pronósticos puntuales con ETS y cuándo equivalen a E(y_{t+h}|x_t)?
R: Iterando las ecuaciones para t = T+1,…,T+h fijando ε_t = 0 para t > T; solo equivalen a la esperanza condicional cuando tendencia y estacionalidad son ambas aditivas. (Sección: ETS y pronóstico en R)

P: ¿Qué modelo eligió la selección automática sobre `ausbeer` y cómo se evalúa la bondad de ajuste?
R: Eligió ETS(M,Md,M) con α=0.1776, β=0.0454, γ=0.1947, φ=0.9549; la bondad de ajuste se evalúa con `accuracy()` (ME, RMSE, MAE, MPE, MAPE, MASE). (Sección: ETS y pronóstico en R)

## Checklist

- [ ] Formular SES en forma de componentes y de espacio de estados, identificando α y ℓ₀.
- [ ] Ajustar SES, Holt y Holt-Winters en R con `ses()`, `holt()` y `hw()`, incluyendo las variantes `exponential=TRUE`, `damped=TRUE` y `seasonal="mult"`.
- [ ] Decidir entre tendencia lineal y amortiguada según el horizonte y el objetivo de ser conservador en el largo plazo.
- [ ] Comparar métodos por RMSE fuera de muestra con un conjunto de prueba, no solo por ajuste dentro de muestra.
- [ ] Verificar que los datos sean estrictamente positivos antes de usar modelos con error multiplicativo; en caso contrario, limitarse a los seis modelos totalmente aditivos.
- [ ] Usar `ets()` con `model="ZZZ"` para selección automática y revisar los componentes elegidos con `plot(fit)`.
- [ ] Controlar los argumentos de `ets()` relevantes: `damped`, `additive.only`, `lambda` (Box-Cox), `opt.crit`, `bounds`, `ic` y `restrict`.
- [ ] Generar pronósticos e intervalos con `forecast(fit, h=...)` y recordar que los intervalos pueden ser exactos o por simulación.
- [ ] Evaluar la bondad de ajuste con `accuracy()` y, si procede, reajustar un modelo previo a datos nuevos con `ets(serie, model=ajuste_previo)`.
