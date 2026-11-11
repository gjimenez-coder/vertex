# Hierarchical forecasting (Pronóstico jerárquico) — Estudio

## Tarjetas de repaso

P: ¿Qué es una *hierarchical time series*? / R: Una colección de series enlazadas en una jerarquía: un total que se desagrega en niveles anidados (por ejemplo, la clasificación ATC de productos farmacéuticos).

P: ¿Qué es una *grouped time series*? / R: Una colección de series que se agregan de varias formas no jerárquicas y cruzadas, como la demanda turística australiana agrupada por región y por propósito del viaje.

P: ¿Qué expresa la ecuación `Yt = S Bt`? / R: Que el conjunto de series se obtiene aplicando la summing matrix `S` al vector `Bt` de las series del nivel más bajo (bottom level).

P: ¿Qué es la summing matrix `S`? / R: Una matriz cuyas filas indican qué series del nivel inferior se suman para formar cada serie de la jerarquía; las filas superiores agregan y las inferiores son la identidad del bottom level.

P: ¿Cuál es el marco unificado de todos los métodos de pronóstico jerárquico? / R: `Ỹn(h) = S P Ŷn(h)`, donde `P` extrae y combina los pronósticos base, `S` los suma hacia arriba y `Ỹn(h)` son los pronósticos reconciliados.

P: ¿Cómo se define `P` en el método bottom-up? / R: `P = [0 | I]`: extrae solo los pronósticos del nivel inferior y `S` los suma.

P: ¿Cómo se define `P` en el método top-down? / R: `P = [p | 0]`, con `p` un vector de proporciones que suman uno que distribuye el pronóstico del agregado hacia las series del nivel más bajo.

P: ¿Cuándo son insesgados los pronósticos revisados? / R: Siempre que `S P S = S`; lo cumple bottom-up, pero no ningún método top-down ni middle-out.

P: ¿Cuál es la varianza de los pronósticos revisados? / R: `Var[Ỹn(h)] = S P Σh P′ S′`, resultado general válido para todos los métodos existentes.

P: ¿En qué consiste la *forecast reconciliation*? / R: Ignorar las restricciones estructurales y pronosticar cada serie de forma independiente, y luego ajustar esos pronósticos para imponer las restricciones.

P: ¿Cuál es la fórmula de los pronósticos reconciliados por OLS? / R: `Ỹn(h) = S (S′S)⁻¹ S′ Ŷn(h)`, obtenida con la inversa generalizada de Moore-Penrose.

P: ¿Cuál es la fórmula de los pronósticos reconciliados por WLS? / R: `Ỹn(h) = S (S′ΛS)⁻¹ S′Λ Ŷn(h)`, con `Λ = [diag(Σ1)]⁻¹`, las inversas de las varianzas de pronóstico a un paso.

P: ¿Qué ventaja y qué limitación tiene OLS? / R: Es simple, flexible e insesgado (`S P S = S`) y sirve para cualquier serie jerárquica o agrupada, pero ignora la matriz de covarianza al calcular los pronósticos puntuales.

P: ¿Qué ventaja y qué limitación tiene WLS? / R: Es fácil de estimar y pone peso donde hay mejores pronósticos, pero ignora las covarianzas.

P: ¿Qué paquete de R implementa estos métodos y de qué depende? / R: El paquete `hts` (v4.3, 2014), que depende de `forecast (≥ 5.0)` y permite analizar y pronosticar series jerárquicas y agrupadas.

## Preguntas de autoevaluación

P1: ¿Qué diferencia a una serie jerárquica de una agrupada?
R: La jerárquica se agrega en niveles anidados (un total desagregado), mientras que la agrupada se agrega de formas cruzadas no jerárquicas. (Sección "Series jerárquicas y agrupadas")

P2: ¿Por qué todos los métodos pueden escribirse como `Ỹn(h) = S P Ŷn(h)` y qué papel juega `P`?
R: Porque todos son combinaciones lineales de los pronósticos base; `P` extrae y combina esos pronósticos para obtener los del bottom level, y la elección de `P` define el método. (Sección "El marco de pronóstico")

P3: ¿Por qué los métodos top-down y middle-out no son insesgados?
R: Porque la condición de insesgadez es `S P S = S`, que no se cumple para ningún método top-down ni middle-out; solo la cumple bottom-up. (Sección "El marco de pronóstico", apartado Sesgo)

P4: ¿Cuál es la idea central de la reconciliación óptima y qué dificultad práctica tiene?
R: Pronosticar cada serie de forma independiente y luego ajustar para imponer las restricciones, estimando `βn(h)` por GLS; la dificultad práctica es que `Σh` es difícil de estimar. (Sección "Pronósticos óptimos: reconciliación")

P5: En la aplicación del turismo australiano, ¿qué método rinde mejor según el nivel y cómo evoluciona el error?
R: *Scaling (st. dev.)* tiende a ganar en niveles inferiores (estados, zonas, regiones) y OLS es competitivo en el nivel superior (Australia); el error crece al bajar, del ~4% en el total al ~32% en regiones (MAPE). (Sección "Aplicación: turismo australiano")

P6: En la aplicación del mercado laboral australiano, ¿qué método obtiene el mejor promedio y cómo se evalúa?
R: WLS consigue el mejor promedio en casi todos los niveles, seguido de cerca por bottom-up, mientras OLS destaca solo en el nivel superior; se evalúa por rolling origin con RMSE para h de 1 a 8. (Sección "Aplicación: mercado laboral australiano")

P7: ¿Cómo se define en la práctica una serie jerárquica con el paquete `hts`?
R: Con `hts(bts, nodes=list(...))`, donde `bts` es la matriz de las series del bottom level y `nodes` describe la estructura; luego se pronostica con `forecast(y, h=...)`. (Sección "El paquete hts para R")

## Checklist

Puntos a dominar:

- [ ] Representar una jerarquía con `Yt = S Bt` e identificar qué filas de `S` agregan y cuáles son la identidad del bottom level.
- [ ] Reconocer el marco `Ỹn(h) = S P Ŷn(h)` y derivar `P` para bottom-up (`[0|I]`) y top-down (`[p|0]`).
- [ ] Aplicar la condición de insesgadez `S P S = S` y saber qué métodos la cumplen (bottom-up) y cuáles no (top-down, middle-out).
- [ ] Distinguir las fórmulas de reconciliación por OLS `S(S′S)⁻¹S′` y por WLS `S(S′ΛS)⁻¹S′Λ`, con `Λ` las inversas de las varianzas a un paso.
- [ ] Explicar los compromisos de cada método: OLS simple pero ignora covarianzas; WLS pondera por calidad pero ignora covarianzas.
- [ ] Relacionar las aplicaciones (turismo y mercado laboral) con el método que rinde mejor por nivel (scaling/WLS en niveles inferiores, OLS en el superior).
- [ ] Usar el paquete `hts`: definir la estructura con `nodes`, pronosticar con `forecast`, y conocer opciones `method`, `fmethod` y `weights`.
- [ ] Reproducir el flujo de la Lab Session 11 con `infantgts`: `smatrix`, `forecast`, `aggts`, `combinef` y `accuracy.gts`.
