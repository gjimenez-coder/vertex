# 07 · Series Temporales y Pronóstico

Análisis y pronóstico de datos ordenados en el tiempo. El flujo general (EDA, preparación, modelado, evaluación) aplica igual, pero con particularidades: **el orden importa**, el split es cronológico, nunca se usa el futuro para predecir el pasado, y aparecen patrones propios (tendencia, estacionalidad, ciclo). Este documento consolida el marco completo de pronóstico: desde graficar y clasificar patrones hasta ETS, ARIMA/SARIMA, regresión dinámica, modelos jerárquicos, VAR, redes neuronales y estacionalidad compleja.

> **Idea rectora (Hyndman & Athanasopoulos):** *un pronóstico no es adivinar el futuro, es estimar la media de un valor futuro con su incertidumbre.* Por eso todo pronóstico puntual debe acompañarse de un **intervalo de predicción**, y todo modelo serio debe superar un **benchmark** simple.

> **Nota de herramientas:** la fuente original (*Forecasting: Principles and Practice*) usa R (`forecast`/`fable`). Aquí se conservan esas funciones como referencia y se añade el **equivalente en Python** (`statsmodels`, `pmdarima`, `statsforecast`, `sktime`, `prophet`), para alinear con el stack Python del resto de dominios.

---

## 1. Qué responde el análisis de una serie temporal

- ¿Qué patrón tiene la serie? ¿Hay **tendencia**, **estacionalidad**, **ciclos**?
- ¿Hay cambios estructurales o anomalías?
- ¿La varianza cambia con el tiempo?
- ¿Puedo explicar la serie con variables externas?
- ¿Puedo **predecir** valores futuros y con qué incertidumbre?
- ¿Puedo detectar el **impacto de una intervención**?

### Predictibilidad: ¿qué se puede pronosticar?
Antes de modelar, evalúa qué tan pronosticable es el fenómeno. Depende de tres cosas:
1. Cuánto **entendemos** los factores que contribuyen.
2. Cuántos **datos** hay disponibles.
3. Si el pronóstico mismo **puede alterar** lo que intenta pronosticar (profecía autocumplida).

> *Ej.:* la demanda eléctrica es muy pronosticable (depende de temperatura y calendario); el tipo de cambio a largo plazo casi no lo es. Evita invertir esfuerzo en pronosticar lo esencialmente impredecible.

---

## 2. Patrones: tendencia, estacionalidad y ciclo

| Patrón | Definición | Clave |
| --- | --- | --- |
| **Tendencia** | Aumento o disminución de largo plazo | No tiene por qué ser lineal |
| **Estacionalidad** | Influida por factores de calendario (trimestre, mes, día de semana) | Periodo **fijo** y conocido (`m` periodos por estación) |
| **Ciclo** | Subidas y bajadas que **no** son de periodo fijo | Duración variable, usualmente ≥ 2 años |

**Estacional vs. cíclico** (el error de clasificación más común): lo estacional tiene longitud constante y *timing* predecible; lo cíclico tiene longitud variable, es más largo en promedio y de *timing* impredecible. De esta distinción depende si usas un método estacional o no.

> *Ej.:* ventas de abrigos = estacional (invierno, periodo fijo). Demanda inmobiliaria = cíclica (sube y baja con la economía, sin periodo fijo).

La **frecuencia** `m` define qué patrones esperar: anual (`m=1`), trimestral (`m=4`), mensual (`m=12`), diario con estacionalidad semanal (`m=7`), horario (`m=24`, 168, 8766…).

---

## 3. EDA de series temporales

Preguntas que guían la exploración:

- ¿La serie crece? (tendencia)
- ¿Tiene patrones semanales, mensuales o anuales? (estacionalidad)
- ¿La varianza cambia con el tiempo? (¿amplitud creciente → transformación?)
- ¿Hay outliers, fechas faltantes, cortes o cambios estructurales?

### Autocorrelación (ACF)
Mide la relación lineal entre `yₜ` y sus rezagos `yₜ₋ₖ`. Revela la estructura:
- **Tendencia:** ACF alta que decae **lento**.
- **Estacionalidad:** picos en los rezagos estacionales (`m, 2m, 3m…`).

El **PACF** (autocorrelación parcial) mide la relación entre `yₜ` y `yₜ₋ₖ` **quitando** los rezagos intermedios; es clave para identificar el orden AR (ver §7).

### Visualización temporal básica
```python
# df.set_index('fecha')['valor'].plot()  (ver 04_analisis_exploratorio_datos.md)
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
plot_acf(serie); plot_pacf(serie)
```

---

## 4. Descomposición de la serie

Toda serie puede separarse en componentes interpretables y tratarse cada uno por separado:

- **Aditiva:** `Yₜ = Tₜ + Sₜ + Eₜ` (tendencia-ciclo + estacional + resto).
- **Multiplicativa:** `Yₜ = Tₜ × Sₜ × Eₜ` — cuando la amplitud estacional **crece con el nivel**.

**STL** (*Seasonal and Trend decomposition using Loess*) es el método por defecto: versátil, **robusto a outliers**, permite que la estacionalidad **cambie con el tiempo**. Solo aditivo (para varianza no constante, aplicar Box-Cox antes).

**Ajuste estacional (desestacionalizar):** `Yₜ − Sₜ` muestra el movimiento subyacente. Útil para comparar periodo a periodo (ej. desempleo de enero vs. febrero) sin confundir estacionalidad con tendencia real.

```python
from statsmodels.tsa.seasonal import STL
res = STL(serie, period=12, robust=True).fit()   # res.trend, res.seasonal, res.resid
```

**Pronóstico vía descomposición:** descomponer → pronosticar el estacional repitiendo el último ciclo (naïve estacional) → pronosticar la parte desestacionalizada con un método no estacional (ETS/RW) → recombinar. *Limitación:* los intervalos resultantes ignoran la incertidumbre del componente estacional.

---

## 5. Benchmarks (métodos de referencia)

**Todo método sofisticado debe superar un benchmark simple** para justificar su complejidad.

| Método | Pronóstico | R / Python |
| --- | --- | --- |
| **Media** | Promedio de todos los datos | `meanf()` / media |
| **Naïve** | Último valor observado | `naive()` / `rwf()` |
| **Naïve estacional** | Último valor del mismo periodo estacional | `snaive()` |
| **Drift** | Naïve + pendiente promedio (primera↔última obs.) | `rwf(drift=TRUE)` |

Elegir según el patrón: serie estable → media; con tendencia → drift; estacional → naïve estacional. El modelo **random walk** `yₜ = yₜ₋₁ + eₜ` es lo que está detrás del naïve.

---

## 6. Suavizamiento exponencial (ETS)

Pronóstico por **promedios ponderados** donde lo reciente pesa más (los pesos decaen exponencialmente). Escala desde series planas hasta series con tendencia y estacionalidad.

| Método | Captura | Parámetros |
| --- | --- | --- |
| **SES** (simple) | Solo nivel → pronóstico **plano** | `α` (nivel) |
| **Holt** (tendencia lineal) | Nivel + tendencia | `α`, `β*` |
| **Holt amortiguado** | Tendencia que se aplana a largo plazo | `+ φ` (0<φ<1) |
| **Holt-Winters** | Nivel + tendencia + estacionalidad | `+ γ` (estacional) |

- La **tendencia amortiguada** (`φ`) evita extrapolaciones demasiado optimistas en horizontes largos.
- Toda la familia se escribe como **modelo de espacio de estados** (ver §11), lo que permite generar intervalos de predicción.

### Marco ETS(Error, Trend, Seasonal)
Taxonomía que clasifica los 15 métodos (Trend ∈ {N, A, Ad, M, Md} × Seasonal ∈ {N, A, M}) y, con errores aditivos/multiplicativos, da 30 modelos. Las versiones aditiva y multiplicativa dan **el mismo pronóstico puntual pero distintos intervalos**.

**Selección automática:** se elige el mejor modelo minimizando **AICc**. Nació para pronosticar automáticamente miles de series (ventas farmacéuticas) a escala.

```python
from statsmodels.tsa.holtwinters import ExponentialSmoothing
fit = ExponentialSmoothing(serie, trend="add", seasonal="add",
                           seasonal_periods=12, damped_trend=True).fit()
# Selección automática tipo ets(): statsforecast.models.AutoETS
```

---

## 7. ARIMA

Combina **AR** (valores pasados), **I** (diferenciación) y **MA** (errores pasados). Requiere una serie **estacionaria**.

### 7.1 Estacionariedad (prerrequisito)
Serie estacionaria = aproximadamente horizontal, **varianza constante**, sin patrones predecibles a largo plazo. Dos problemas, dos herramientas:

- **Varianza no constante** → **transformación Box-Cox** (`λ=0` es log, interpretable como cambios relativos; `λ=0` además fuerza pronósticos positivos).
- **Media no constante / tendencia** → **diferenciación**:
  - Ordinaria: `y'ₜ = yₜ − yₜ₋₁` (estabiliza la media).
  - Estacional: `yₜ − yₜ₋ₘ` (quita la estacionalidad).

**¿Cuánto diferenciar?** Tests de raíz unitaria:
- **ADF** (H₀: no estacionaria) y **KPSS** (H₀: estacionaria).
- Automatizar con `ndiffs()` / `nsdiffs()`.
- Si la estacionalidad es fuerte, diferenciar **estacionalmente primero**. Mantener las diferencias **interpretables** y no sobre-diferenciar.

```python
from statsmodels.tsa.stattools import adfuller, kpss
from pmdarima.arima import ndiffs, nsdiffs
```

### 7.2 Identificación del orden (p, d, q)
`ARIMA(p,d,q)`: `p` = orden AR, `d` = grado de diferenciación, `q` = orden MA. Casos particulares: ruido blanco = (0,0,0); random walk = (0,1,0) sin constante; con drift = (0,1,0) con constante.

**Lectura de ACF/PACF:**
- `ARIMA(p,d,0)`: el ACF decae exponencial/sinusoidal y el PACF tiene un **pico en el lag p** (nada después).
- `ARIMA(0,d,q)`: el PACF decae y el ACF tiene un **pico en el lag q**.

### 7.3 Selección y procedimiento completo (7 pasos)
Selección objetiva por **AICc** (las comparaciones por AICc exigen el **mismo `d`**). Algoritmo `auto.arima` (Hyndman-Khandakar) para automatizar, pero sin renunciar al juicio humano:

1. Graficar; identificar observaciones inusuales.
2. Transformar (Box-Cox) si la varianza no es constante.
3. Diferenciar hasta estacionariedad.
4. Examinar ACF/PACF → candidatos AR(p)/MA(q).
5. Probar modelos y elegir el de mejor AICc.
6. Revisar residuales (ACF + Ljung-Box). Si no son ruido blanco, modificar.
7. Cuando los residuales sean ruido blanco → pronosticar.

> **No pronostiques hasta que los residuales parezcan ruido blanco.** La automatización cubre los pasos 3-5; graficar y verificar residuales sigue siendo humano.

```python
import pmdarima as pm
modelo = pm.auto_arima(serie, seasonal=False, stepwise=True)  # ~ auto.arima()
```

### 7.4 SARIMA (ARIMA estacional)
`ARIMA(p,d,q)(P,D,Q)ₘ`: añade una parte estacional en los rezagos múltiplos de `m`. Se lee en los rezagos estacionales del ACF/PACF igual que la parte no estacional. Modelos comunes: el *airline model* `ARIMA(0,1,1)(0,1,1)₁₂` con log. En el Ljung-Box usar `lag = 2m`.

```python
from statsmodels.tsa.statespace.sarimax import SARIMAX
SARIMAX(serie, order=(2,1,0), seasonal_order=(0,1,1,12)).fit()
```

### 7.5 ARIMA vs. ETS
No hay ganador universal. **Comparar por error out-of-sample (RMSE)** en test set / validación cruzada. A veces **ningún** modelo pasa todos los tests de residuales → *usa el mejor modelo disponible aunque no sea perfecto* (pragmatismo sobre perfeccionismo paralizante).

---

## 8. Regresión dinámica (predictores externos)

Para usar covariables (publicidad, ingreso, clima) cuando los errores de la regresión están **autocorrelacionados**:

$$y_t = \beta_0 + \sum \beta_i x_{i,t} + n_t, \quad n_t \sim \text{ARIMA}$$

- Solo los errores finales `eₜ` (dentro de `nₜ`) se asumen ruido blanco.
- **Estimar por verosimilitud (minimizar Σe²), nunca OLS directo**: un OLS con errores autocorrelacionados da p-values engañosamente pequeños → **regresión espuria**.
- Todas las variables deben ser estacionarias antes de estimar.
- Para pronosticar hace falta conocer/estimar los **predictores futuros** (o usar los conocidos de antemano: tiempo, dummies de calendario).

**Tendencia determinista vs. estocástica:** dan pronósticos puntuales casi iguales pero **intervalos muy distintos** (los estocásticos, con `d≥1`, son más anchos y honestos a largo plazo).

**Estacionalidad con términos de Fourier:** pares seno/coseno `sin(2πkt/m)`, `cos(2πkt/m)`; manejan estacionalidad de periodo largo o múltiple con pocos términos (`K` por AICc). `nₜ` queda como ARIMA no estacional.

**Función de transferencia:** incluir predictores rezagados `xₜ, xₜ₋₁,…` cuando el efecto se propaga con retraso (campaña → ventas semanas después).

---

## 9. Pronóstico jerárquico

Cuando las series se organizan en jerarquías (Total → Regiones → Tiendas), los pronósticos independientes **no suman** (la suma de regiones ≠ total). La estructura se codifica en la matriz de sumas `S` (`Yₜ = S·Bₜ`).

| Enfoque | Idea | Insesgado |
| --- | --- | --- |
| **Bottom-up** | Pronosticar el nivel más bajo y agregar hacia arriba | ✅ Sí |
| **Top-down** | Pronosticar el total y repartir con proporciones | ❌ No |
| **Reconciliación óptima** | Pronosticar todos los niveles y ajustar para imponer coherencia | ✅ Sí |

La **reconciliación óptima** combina los pronósticos base de todos los niveles minimizando la varianza. Aproximaciones prácticas: **OLS** (robusto, ignora covarianzas) y **WLS** (pondera por calidad del pronóstico, suele dar menor MAPE). En R: paquete `hts` (`method="comb"`); en Python: `hierarchicalforecast` (Nixtla). Evaluar precisión **por nivel y horizonte**, no solo el total.

---

## 10. VAR (autorregresiones vectoriales)

Cuando varias variables se influyen **mutuamente** (retroalimentación), se tratan todas como **endógenas** y cada una depende de los rezagos de todas. Supera la limitación unidireccional (x→y) de la regresión dinámica.

$$y_{1,t} = c_1 + \phi_{11}y_{1,t-1} + \phi_{12}y_{2,t-1} + e_{1,t} \quad (\text{y análogo para } y_2)$$

**Usos:** pronóstico conjunto de variables relacionadas, **causalidad de Granger** (¿una variable ayuda a pronosticar otra?), respuesta al impulso, descomposición de varianza. Elegir el orden `p` con criterios (AIC/BIC/HQ/FPE); validar residuales con un test portmanteau. Reservarlo para **pocas** variables realmente interdependientes (explota en nº de parámetros).

```python
from statsmodels.tsa.api import VAR
res = VAR(data).fit(maxlags=8, ic="aic")   # res.test_causality(...) para Granger
```

---

## 11. Modelos de espacio de estados y filtro de Kalman

Casi cualquier modelo (ETS, ARIMA, estructurales) se escribe como un **espacio de estados** —una ecuación de observación y otra de estado— donde hay **estados ocultos** (nivel, pendiente, estacional) observados con ruido:

$$y_t = f' x_t + \varepsilon_t \qquad x_t = G x_{t-1} + w_t$$

El **filtro de Kalman** da entonces, con una sola maquinaria: pronósticos óptimos (MSE), la verosimilitud, y manejo natural de **datos faltantes** (ciclo predecir → actualizar).

- **Modelos estructurales (BSM):** ponen explícitamente nivel + pendiente + estacional como estados con sus varianzas; fáciles de generalizar (covariables) y de manejar con faltantes.
- Los **ETS aditivos** son casi equivalentes a los modelos estructurales correspondientes.
- Permite **parámetros variables en el tiempo** (ej. una elasticidad que cambia).

```python
from statsmodels.tsa.statespace.structural import UnobservedComponents
UnobservedComponents(serie, level="local linear trend", seasonal=12).fit()
```

---

## 12. Modelos no lineales: redes neuronales (NNAR)

Una red sin capa oculta = regresión lineal; la **capa oculta** introduce la no linealidad. Para series, usa valores rezagados como entradas: **NNAR(p, P, k)ₘ** = autorregresión no lineal.

- `NNAR(p, P, 0)ₘ` equivale a `ARIMA(p,0,0)(P,0,0)ₘ` pero **sin restricciones de estacionariedad**.
- Selección automática: `p` por analogía con el mejor AR lineal (AIC), `P=1` por defecto, `k = (p+P+1)/2`.
- Útil para dinámica no lineal (ej. ciclos de manchas solares). Riesgo de **sobreajuste**; comparar siempre contra ETS/ARIMA por validación cruzada antes de adoptarlo.

En R: `nnetar()` (`lambda=0` para pronósticos positivos). En Python: `sktime`/`darts` (NBEATS, RNN, LSTM, GRU) o `statsforecast`/`neuralforecast` (Nixtla).

---

## 13. Estacionalidad compleja: TBATS

Para estacionalidad **múltiple, de periodo largo o no entera** (demanda eléctrica horaria con ciclos diario+semanal+anual; llamadas cada 5 min), los métodos clásicos (SARIMA, Holt-Winters) fallan. **TBATS** ensambla:

- **T**rigonometric: términos de Fourier para la estacionalidad (periodos múltiples/no enteros, pocos parámetros).
- **B**ox-Cox: estabiliza la varianza.
- **A**RMA: dinámica de corto plazo (errores).
- **T**rend (posiblemente amortiguada) + **S**easonal.

Los términos de Fourier **ahorran grados de libertad** frente a la diferenciación estacional en periodos largos. En R: `tbats()`; en Python: `sktime.forecasting.tbats.TBATS` o Prophet (estacionalidades múltiples). La elección final entre TBATS / Fourier-regresión / NNAR / SARIMA se decide por **validación cruzada**.

---

## 14. Evaluación: residuales y precisión out-of-sample

### Diagnóstico de residuales
Un buen modelo deja residuales que parecen **ruido blanco**: no correlacionados, media cero, varianza constante (idealmente normales, para intervalos). El error de pronóstico de un paso: `eₜ = yₜ − ŷₜ|ₜ₋₁`.

- **Límites del ACF:** para ruido blanco, el 95% de las autocorrelaciones caen dentro de **±1.96/√T**. Si se superan, queda información sin usar.
- **Test portmanteau (Ljung-Box, preferido sobre Box-Pierce):** evalúa el *conjunto* de autocorrelaciones. Usar `h=10` (no estacional), `h=2m` (estacional). p-value alto → residuales ≈ ruido blanco (bien).

```python
from statsmodels.stats.diagnostic import acorr_ljungbox
acorr_ljungbox(residuales, lags=[10])
```

### Precisión fuera de muestra
> *Un modelo que ajusta bien los datos no necesariamente pronostica bien.* El sobreajuste es tan malo como no identificar el patrón.

- Dividir **cronológicamente**: train (~80%) y test (~20%). **El test no se usa para ninguna parte del desarrollo del modelo.** (ver regla anti-leakage en `05_preparacion_de_datos.md`).
- Métricas: ME, RMSE, MAE, MPE, MAPE y **MASE** (escalada, comparable entre series).

### Validación cruzada temporal (origen rodante)
No se puede barajar datos temporales. El **rolling forecasting origin** avanza el origen paso a paso: entrena con `1…i`, pronostica `i+1` (o hasta `i+h`), mide el error, avanza. Promedia los errores **por horizonte** (un modelo puede ser mejor a 1 paso y peor a 12). Se corresponde con **TimeSeriesSplit** (ver `06_modelado_y_evaluacion.md`). La ventana puede ser **expansiva** (crece) o **fija** (deslizante).

```python
from sklearn.model_selection import TimeSeriesSplit   # respeta el orden
# o sktime: ExpandingWindowSplitter / SlidingWindowSplitter
```

---

## 15. Flujo de trabajo de pronóstico

```
Graficar y clasificar patrones (tendencia/estacional/ciclo)
      ↓
Evaluar predictibilidad + correr benchmarks (naïve, snaive, drift, media)
      ↓
¿Estabilizar? → Box-Cox (varianza) + diferenciación (media)
      ↓
Elegir familia:  ETS · ARIMA/SARIMA · Regresión dinámica · VAR · NNAR · TBATS
      ↓
Ajustar y seleccionar por AICc (dentro de la familia)
      ↓
Diagnóstico de residuales (ACF ±1.96/√T + Ljung-Box)
      ↓
Comparar familias por error out-of-sample (RMSE/MAE con validación cruzada temporal)
      ↓
Pronóstico puntual + intervalo de predicción
```

### Elección rápida del método

| Situación | Método recomendado |
| --- | --- |
| Serie plana, sin tendencia ni estacionalidad | SES / naïve |
| Tendencia, sin estacionalidad | Holt (amortiguado en horizontes largos) / drift |
| Estacionalidad simple entera y corta | ETS estacional (Holt-Winters) / SARIMA |
| Predictores externos | Regresión dinámica con errores ARIMA |
| Varias variables con retroalimentación | VAR |
| Dinámica no lineal | NNAR / modelos de deep learning |
| Estacionalidad múltiple, larga o no entera | TBATS / Fourier-regresión / Prophet |
| Series jerárquicas que deben cuadrar | Reconciliación (bottom-up / WLS óptima) |
| Datos faltantes o parámetros variables | Espacio de estados (filtro de Kalman) |

---

## Conexión con el resto del flujo

- **Visualización temporal:** `df.set_index('fecha')['valor'].plot()` → `04_analisis_exploratorio_datos.md`.
- **Split cronológico y regla anti-leakage** → `05_preparacion_de_datos.md`.
- **Validación cruzada (TimeSeriesSplit)** y métricas de error (RMSE, MAE) → `06_modelado_y_evaluacion.md`.
- **Correlación y comparación de medias** (base de ACF e inferencia) → `03_estadistica_aplicada.md`.

> Este documento sintetiza los 14 capítulos de *Forecasting: Principles and Practice* (Hyndman & Athanasopoulos). Las fórmulas estadísticas base (media, varianza, correlación) viven en el documento 03; las reglas de split y validación compartidas con el modelado general viven en 05 y 06, y aquí solo se enlazan para no duplicarlas.
