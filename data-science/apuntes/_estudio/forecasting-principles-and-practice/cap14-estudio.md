# Forecasting complex seasonality (Pronóstico de estacionalidad compleja) — Estudio

## Tarjetas de repaso

P: ¿Qué problema aborda el capítulo 14?
R: El pronóstico de series con estacionalidad compleja: patrones estacionales múltiples, no enteros y de periodo largo que los modelos clásicos no manejan bien.

P: ¿Qué cuatro ideas reúne el modelo TBATS?
R: Términos trigonométricos para la estacionalidad, transformación de Box-Cox para la heterogeneidad, errores ARMA para la dinámica de corto plazo y tendencia (posiblemente amortiguada).

P: ¿Qué característica del componente estacional de TBATS lo distingue?
R: Admite periodos estacionales múltiples y no enteros.

P: ¿Para qué sirve la transformación de Box-Cox en TBATS?
R: Para controlar la heterogeneidad (varianza no constante); con ω = 0 equivale al logaritmo.

P: ¿Qué ventaja aportan los términos trigonométricos (armónicos de Fourier) frente a la diferenciación estacional?
R: Permiten periodos no enteros y ahorran (reducen el número de) parámetros/grados de libertad.

P: ¿Qué proceso sigue el término de error d_t en TBATS?
R: Un proceso ARMA(p, q).

P: ¿Qué representa cada estacionalidad i en el modelo?
R: Una suma de k_i armónicos trigonométricos.

P: ¿Qué significan los elementos de la notación TBATS(ω, {p,q}, φ, {<periodo, k>,...})?
R: ω es la potencia de Box-Cox, {p,q} el orden ARMA, φ el amortiguamiento de la tendencia y cada <periodo, k> una estacionalidad con su número de armónicos.

P: ¿Cuáles son los tres conjuntos de datos que ilustran el capítulo?
R: Productos de gasolina terminada de EE. UU. (semanal), llamadas a un gran banco americano en intervalos de 5 minutos y la demanda eléctrica turca (diaria).

P: ¿Cuál es el flujo de trabajo de TBATS en R?
R: Ajustar con `tbats()`, pronosticar con `forecast()` y visualizar con `plot()`; antes debe cargarse el paquete fpp.

P: ¿Cuántas estacionalidades se identificaron para las llamadas al centro de atención y cuáles?
R: Dos: diaria y semanal.

P: ¿Cuántas estacionalidades se identificaron para la demanda eléctrica turca y cuáles?
R: Tres: semanal, anual aproximada (354.37) y anual de 365.25 días.

P: ¿Cómo se actualizan el nivel y la tendencia en TBATS?
R: ℓ_t = ℓ_{t-1} + φ b_{t-1} + α d_t y b_t = (1−φ) b + φ b_{t-1} + β d_t.

P: ¿Qué método permite comparar objetivamente TBATS con los demás modelos del curso?
R: La validación cruzada, calculando el MAE validado por cruzamiento de cada modelo.

## Preguntas de autoevaluación

P: ¿Por qué los métodos clásicos no bastan para los ejemplos del capítulo?
R: Porque presentan estacionalidad compleja: patrones múltiples, no enteros y de periodo largo que esos métodos no capturan bien. (Sección: Lo que necesitas saber)

P: ¿Qué modelo elegido se reporta para la gasolina y qué indica su estacionalidad?
R: TBATS(0.999, {2,2}, 1, {<52.1785714285714,8>}), una única estacionalidad anual no entera de 52.18 semanas con 8 armónicos. (Sección: Ejemplos y uso en R)

P: Interpreta la notación TBATS(1, {3,1}, 0.987, {<169,5>, <845,3>}) de las llamadas.
R: Box-Cox ω=1, ARMA de orden {3,1}, amortiguamiento φ=0.987 y dos estacionalidades: <169,5> (diaria, 5 armónicos) y <845,3> (semanal, 3 armónicos). (Sección: Ejemplos y uso en R)

P: ¿Qué hay que hacer antes de cualquier ejercicio en R del laboratorio?
R: Cargar el paquete fpp con `library(fpp)`. (Sección: 14.2 Lab Session 12)

P: ¿Qué se pide comprobar al modelar la serie `visitors` con tbats?
R: Revisar los residuos, producir pronósticos, valorar si el enfoque automático funciona y comprobar si se ahorran grados de libertad usando términos de Fourier en lugar de diferenciación estacional. (Sección: 14.2 Lab Session 12)

P: ¿Qué función se propone experimentar como alternativa basada en redes neuronales?
R: `nnetar()`. (Sección: 14.2 Lab Session 12 / Ideas clave)

P: ¿Cuál es el ejercicio final del laboratorio y qué precaución se menciona?
R: Usar validación cruzada para comparar todos los modelos de los datos de comercio minorista (`retail`) con el MAE validado; como la ejecución es lenta, conviene dejarla corriendo durante la noche. (Sección: 14.2 Lab Session 12)

## Checklist

- Cargar el paquete fpp con `library(fpp)` antes de los ejercicios en R.
- Ajustar el modelo con `tbats()`, pronosticar con `forecast()` y visualizar con `plot()`.
- Revisar los residuos del modelo ajustado antes de dar por buenos los pronósticos.
- Comprobar si se ahorran grados de libertad usando términos de Fourier en lugar de diferenciación estacional.
- Leer los datos de gasolina con `read.csv` y definir la serie con `ts(..., frequency = 365.25/7)` antes de ajustar TBATS.
- Interpretar la notación TBATS(ω, {p,q}, φ, {<periodo, k>}) para entender los parámetros estimados.
- Comparar TBATS con los otros modelos mediante validación cruzada (MAE), dejando la ejecución correr durante la noche por su lentitud.
