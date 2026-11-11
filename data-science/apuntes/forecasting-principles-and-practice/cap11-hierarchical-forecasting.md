# Forecasting: Principles and Practice — Rob J. Hyndman (material de taller, University of Western Australia, septiembre 2014)
## Capítulo 11 — Hierarchical forecasting (Pronóstico jerárquico)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF (material de taller con sesiones de laboratorio en R, del que se conserva solo el código esencial); las citas usan la página del PDF `(PDF p. N)`.

## Lo que necesitas saber
El capítulo trata de cómo pronosticar colecciones de series temporales que están relacionadas entre sí por una estructura de agregación. En una *hierarchical time series* las series se enlazan en una jerarquía (un total que se desagrega en niveles anidados), como la clasificación ATC de productos farmacéuticos. En una *grouped time series* las series se agregan de varias formas no jerárquicas y cruzadas, como la demanda turística australiana agrupada por región y por propósito del viaje.

La tesis central es que todos los métodos de pronóstico jerárquico pueden escribirse como una combinación lineal de pronósticos base, y que conviene reconciliar esos pronósticos para que los niveles sumen de forma coherente. El marco unificado `Ỹn(h) = S P Ŷn(h)` cubre bottom-up, top-down, middle-out y los métodos de reconciliación óptima (OLS y WLS).

Sales sabiendo cómo representar la jerarquía con la matriz de sumas `S`, cómo cada método elige la matriz `P`, cuándo los pronósticos reconciliados son insesgados, y qué método funciona mejor según las aplicaciones (turismo y mercado laboral australiano). También conoces el paquete `hts` de R para aplicarlo en la práctica.

## Series jerárquicas y agrupadas
Notación básica: `Yt` es el agregado observado de todas las series en el tiempo `t`; `YX,t` es la observación de la serie `X`; `Bt` es el vector de todas las series del nivel más bajo (bottom level). La estructura se captura con la ecuación matricial:

```
Yt = S Bt
```

donde `S` es la *summing matrix*: cada fila indica qué series del nivel inferior se suman para formar cada serie de la jerarquía. Para una jerarquía simple Total → A, B, C, la primera fila de `S` es `[1 1 1]` (el total) y las siguientes son filas identidad. En jerarquías de dos niveles o en datos agrupados (cruzando grupos A/B con X/Y), `S` crece pero mantiene la misma idea: las filas superiores agregan, las inferiores son la identidad del bottom level.

- **Ejemplos de jerarquías**: jerarquías de productos de manufactura, rotación neta de personal, ventas farmacéuticas, demanda turística por región y propósito.
- **Jerárquica**: productos farmacéuticos bajo la Anatomical Therapeutic Chemical (ATC) Classification System.
- **Agrupada**: turismo australiano agrupado por región y por propósito de viaje (agregaciones no jerárquicas y cruzadas).

## El marco de pronóstico
Sea `Ŷn(h)` el vector de pronósticos base iniciales a `h` pasos, hechos en el tiempo `n` y apilados en el mismo orden que `Yt` (pueden no sumar de forma coherente). Todos los métodos de pronóstico jerárquico tienen la forma:

```
Ỹn(h) = S P Ŷn(h)
```

para alguna matriz `P`. Aquí `P` extrae y combina los pronósticos base para obtener pronósticos del bottom level, `S` los suma hacia arriba, y `Ỹn(h)` son los pronósticos revisados y reconciliados.

- **Bottom-up**: `P = [0 | I]` (matriz nula y matriz identidad). `P` extrae solo los pronósticos del nivel inferior y `S` los suma para dar los pronósticos bottom-up.
- **Top-down**: `P = [p | 0]`, con `p = [p1, p2, …, pmK]′` un vector de proporciones que suman uno. `P` distribuye el pronóstico del agregado a las series del nivel más bajo. Distintos métodos top-down llevan a distintos vectores de proporciones `p`.

**Sesgo (bias)**: si los pronósticos base son insesgados y `βn(h) = E[B̂n(h)]`, entonces `E[Ŷn(h)] = S βn(h)`. Queremos que los revisados también sean insesgados, lo que se cumple siempre que `S P S = S`. Esto es cierto para bottom-up, pero **no** para ningún método top-down ni middle-out.

**Varianza**: si `Σh = Var[Ŷn(h)]` es la varianza de los pronósticos base, la varianza de los revisados es `Var[Ỹn(h)] = S P Σh P′ S′`. Es un resultado general para todos los métodos existentes.

## Pronósticos óptimos: reconciliación
La idea clave de la *forecast reconciliation* es: ignorar las restricciones estructurales y pronosticar cada serie de interés de forma independiente, y luego ajustar esos pronósticos para imponer las restricciones. Como `Yt = S Bt`, se escribe `Ŷn(h) = S βn(h) + εh`, donde `εh` tiene media cero y covarianza `Σh`. Estimando `βn(h)` por mínimos cuadrados generalizados (GLS):

```
Ỹn(h) = S (S′ Σ†h S)⁻¹ S′ Σ†h Ŷn(h)
```

con `Σ†h` la inversa generalizada de `Σh`. El problema práctico es que `Σh` es difícil de estimar.

## Pronósticos reconciliados por OLS
Se aproxima `Σ†1` por `cI`, o se asume `εh ≈ S εB,h` (con `εB,h` el error de pronóstico del bottom level), de modo que `Σh ≈ S Ωh S′`. Usando la inversa generalizada de Moore-Penrose, `(S′Σ†h S)⁻¹ S′Σ†h = (S′S)⁻¹ S′`, y los pronósticos reconciliados quedan:

```
Ỹn(h) = S (S′S)⁻¹ S′ Ŷn(h)
```

Características: admite covariables en los pronósticos iniciales; permite ajustes a cualquier nivel; es muy simple y flexible y sirve para cualquier serie jerárquica o agrupada; cumple `S P S = S`, así que es insesgado; es conceptualmente fácil (OLS sobre los pronósticos base); y los pesos son independientes de los datos y de la estructura de covarianza.

Desafíos: dificultades computacionales en jerarquías grandes por el tamaño de `S` y el comportamiento singular de `(S′S)`; necesidad de estimar la matriz de covarianza para producir intervalos de pronóstico; e ignora la matriz de covarianza al calcular los pronósticos puntuales.

## Pronósticos reconciliados por WLS
Se aproxima `Σ1` por su diagonal y se toma `Λ = [diag(Σ1)]⁻¹`, que contiene las inversas de las varianzas de pronóstico a un paso:

```
Ỹn(h) = S (S′ΛS)⁻¹ S′Λ Ŷn(h)
```

Es fácil de estimar y pone peso donde tenemos los mejores pronósticos, pero ignora las covarianzas. Para muchas series, el cálculo debe hacerse sin formar explícitamente `S`, `(S′ΛS)⁻¹` ni `S′Λ`.

## Aplicación: turismo australiano
Datos trimestrales 1998–2006 del National Visitor Survey (entrevistas anuales a 120.000 australianos de 15+ años, recogidas por Tourism Research Australia). La jerarquía va de Total → estados (NSW, VIC, QLD, Other) → zonas → regiones.

Evaluación: se seleccionan modelos con todas las observaciones; se reestiman con las primeras 12 y se generan pronósticos de 1 a 8 pasos; se aumenta la muestra de una en una reestimando hasta el final (24 pronósticos a 1 paso, 23 a 2 pasos, hasta 17 a 8 pasos). Medido por MAPE, el método *Scaling (st. dev.)* tiende a ganar en niveles inferiores (estados, zonas, regiones), mientras que OLS es competitivo en el nivel superior (Australia). El error crece notablemente al bajar en la jerarquía (del ~4% en el total al ~32% en regiones).

## Aplicación: mercado laboral australiano
La jerarquía ocupacional sigue la ANZSCO (Australian and New Zealand Standard Classification of Occupations): 8 grupos mayores, 43 submayores, 97 menores, 359 grupos de unidad y 1023 ocupaciones (ejemplo: 2 Professionals → 22 → 224 → 2241 → 224113 Statistician). Los pronósticos base se obtienen con `auto.arima()` y se muestran los cambios mayores por nivel entre base y reconciliados.

Evaluación por rolling origin (RMSE, h de 1 a 8): **WLS** consigue el mejor promedio en casi todos los niveles (p. ej. nivel 1, nivel 2, nivel 3 y bottom level), seguido de cerca por bottom-up; **OLS** destaca en el nivel superior frente a bottom-up pero pierde en los niveles intermedios. El patrón general es que WLS equilibra bien precisión y coherencia a lo largo de toda la jerarquía.

## El paquete hts para R
`hts` (versión 4.3, publicado 2014-06-10; autores Rob J Hyndman, Earo Wang y Alan Lee; licencia GPL ≥ 2) ofrece métodos para analizar y pronosticar series jerárquicas y agrupadas. Depende de `forecast (≥ 5.0)`. Uso básico:

```r
library(hts)
# bts: matriz con las series del bottom level; nodes describe la estructura
y <- hts(bts, nodes=list(2, c(3,2)))
# Pronóstico a 10 pasos con método de combinación WLS; ETS por serie por defecto
fc <- forecast(y, h=10)
```

La función `forecast.gts` acepta `method = c("comb","bu","mo","tdgsf","tdgsa","tdfp")`, `fmethod = c("ets","rw","arima")`, `weights = c("sd","none","nseries")`, además de `positive`, `parallel` y `num.cores`. Con `weights = "sd"` se tiene en cuenta la desviación estándar de los pronósticos para la combinación óptima.

## Lab Session 11
Antes de los ejercicios se carga `library(fpp)`. El objetivo es reconciliar los pronósticos de los datos `infantgts` (muertes infantiles). Código esencial:

```r
library(hts)
smatrix(infantgts)                       # ver la matriz S
infantforecast <- forecast(infantgts, h=10)
plot(infantforecast, include=10)
# Pronosticar todas las series agregadas con ARIMA y recombinar
allts_infant <- aggts(infantgts)
y.f <- combinef(allf, groups = infantgts$groups)
# Entrenamiento/prueba y evaluación
forecast <- forecast(window(infantgts, start=1933, end=1993), h=10)
accuracy.gts(forecast, test)
```

Los ejercicios piden medir la precisión global de toda la colección, repetir el análisis con `method="bu"` (bottom-up) y top-down, y valorar si la reconciliación "óptima" funciona mejor en este caso.

## Ideas clave
- Una serie jerárquica se agrega en niveles anidados; una agrupada se agrega de formas cruzadas no jerárquicas.
- La estructura se resume en `Yt = S Bt`, con `S` la summing matrix.
- Todo método jerárquico es `Ỹn(h) = S P Ŷn(h)`; la elección de `P` define el método.
- Bottom-up usa `P = [0|I]`; top-down usa `P = [p|0]` con proporciones que suman uno.
- Los pronósticos reconciliados son insesgados si `S P S = S`: lo cumple bottom-up, no top-down ni middle-out.
- La reconciliación óptima pronostica cada serie por separado y luego ajusta; OLS usa `S(S′S)⁻¹S′` y WLS pondera por la inversa de las varianzas.
- OLS es simple e insesgado pero ignora covarianzas; WLS pone peso donde hay mejores pronósticos.
- En las aplicaciones (turismo y mercado laboral), WLS/scaling suele rendir mejor que OLS en los niveles inferiores; el paquete `hts` de R implementa todos estos métodos.
