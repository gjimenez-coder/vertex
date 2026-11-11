# Verificación de fidelidad — forecasting-principles-and-practice

Reporte generado por el agente `notes-verifier`: contrasta cada apunte con el texto fuente del capítulo.

| Capítulo | Hallazgos | Alta | Media | Baja |
|---|---|---|---|---|
| cap01 | 1 | 1 | 0 | 0 |
| cap02 | 0 | 0 | 0 | 0 |
| cap03 | 1 | 0 | 0 | 1 |
| cap04 | 0 | 0 | 0 | 0 |
| cap05 | 0 | 0 | 0 | 0 |
| cap06 | 0 | 0 | 0 | 0 |
| cap07 | 1 | 0 | 1 | 0 |
| cap08 | 1 | 0 | 0 | 1 |
| cap09 | 1 | 0 | 0 | 1 |
| cap10 | 0 | 0 | 0 | 0 |
| cap11 | 1 | 1 | 0 | 0 |
| cap12 | 1 | 0 | 1 | 0 |
| cap13 | 0 | 0 | 0 | 0 |
| cap14 | 0 | 0 | 0 | 0 |

**Total:** 7 hallazgos (alta 2, media 2, baja 3) en 14 capítulos.

## Detalle

## cap01 — Introduction to forecasting
Hallazgos: 1 (alta 1, media 0, baja 0)
- [alta] «University of Western Australia (taller), 2014» → editorial y año inventados; la fuente no menciona esa institución ni ese año, y sitúa al autor en Monash University; evidencia: «Director of Monash University's Business & Economic Forecasting Unit» (PDF p. 5)

## cap02 — The forecaster's toolbox
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap03 — Exponential smoothing (Suavizado exponencial)
Hallazgos: 1 (alta 0, media 0, baja 1)
- [baja] «Rob J. Hyndman (University of Western Australia, 2014)» → la afiliación/editorial y el año no aparecen en el texto fuente del capítulo; el libro se titula «Forecasting: principles and practice» sin indicar universidad ni año; evidencia: «Forecasting: principles and practice» (PDF p. 35)

## cap04 — Time series decomposition
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap05 — Time series cross-validation
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap06 — Making time series stationary
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap07 — Non-seasonal ARIMA models
Hallazgos: 1 (alta 0, media 1, baja 0)
- [media] «Rob J. Hyndman (University of Western Australia, 2014)» → afiliación sin respaldo en la fuente del capítulo; el texto no menciona autor, editorial, año ni universidad; evidencia: el encabezado de página solo indica «Forecasting: principles and practice» (PDF p. 73)

## cap08 — Seasonal ARIMA models
Hallazgos: 1 (alta 0, media 0, baja 1)
- [baja] «Rob J. Hyndman (University of Western Australia, 2014)» → afiliación y año no respaldados por el texto fuente del capítulo; evidencia: la fuente no menciona autor, editorial ni año (PDF p. 84)

## cap09 — State space models (Modelos de espacio de estados)
Hallazgos: 1 (alta 0, media 0, baja 1)
- [baja] «programar un filtro de Kalman propio para actualizar coeficientes de regresión del consumo personal (`y`) frente a la renta disponible (`z`)» → omite que las series son tasas de crecimiento trimestral, no los niveles; evidencia: «quarterly growth rates in US personal consumption expenditure (y) against quarterly growth rates in US real personal disposable income (z)» (PDF p. 104)

## cap10 — Dynamic regression models
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap11 — Hierarchical forecasting
Hallazgos: 1 (alta 1, media 0, baja 0)
- [alta] «Rob J. Hyndman (University of Western Australia (taller), 2014)» → afiliación sin respaldo y contradicha por la fuente, que asocia al autor con Monash; evidencia: «Maintainer: Rob J Hyndman <Rob.Hyndman at monash.edu>» (PDF p. 125)

## cap12 — Vector autoregressions
Hallazgos: 1 (alta 0, media 1, baja 0)
- [media] «en la ecuación del ingreso son significativos el consumo rezagado un periodo y el ingreso rezagado un periodo» → lista incompleta de términos significativos: la fuente también muestra el consumo rezagado tres periodos como significativo; evidencia: «consumption.l3 0.40297 ... 3.367 0.000959 ***» (PDF p. 130)

## cap13 — Neural network models
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap14 — Forecasting complex seasonality
Hallazgos: 0 (alta 0, media 0, baja 0)
