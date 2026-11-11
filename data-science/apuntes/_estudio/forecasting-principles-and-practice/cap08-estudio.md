# Seasonal ARIMA models (Modelos ARIMA estacionales) — Estudio

## Tarjetas de repaso

P: ¿Qué representa cada componente de la notación ARIMA(p,d,q)(P,D,Q)ₘ?
R: La primera terna es la parte no estacional, la segunda la parte estacional y m el número de periodos por estación (p. ej. 4 trimestral, 12 mensual).

P: ¿Cómo se construye un modelo ARIMA estacional a partir de sus componentes?
R: Multiplicando los factores AR, de diferenciación y MA de ambas partes (no estacional y estacional), lo que genera un polinomio con rezagos alrededor de los múltiplos de m.

P: ¿Sobre qué rezagos operan los términos estacionales?
R: Sobre rezagos múltiplos de m, usando el operador de retardo elevado a potencias de m.

P: En un ARIMA(1,1,1)(1,1,1)₄, ¿qué significan los seis factores de la ecuación?
R: En orden: AR(1) no estacional, AR(1) estacional, diferencia no estacional, diferencia estacional, MA(1) no estacional y MA(1) estacional.

P: ¿Cómo se identifica un término MA estacional frente a uno AR estacional en ACF/PACF?
R: Un término MA estacional deja picos en los rezagos estacionales de la ACF; un término AR estacional deja picos en los rezagos estacionales de la PACF.

P: ¿Qué patrón muestra un ARIMA(0,0,0)(0,0,1)₁₂ en la ACF y la PACF?
R: Un pico en el rezago 12 de la ACF (sin otros picos significativos) y decaimiento exponencial en los rezagos estacionales (12, 24, 36…) de la PACF.

P: ¿Qué patrón muestra un ARIMA(0,0,0)(1,0,0)₁₂ en la ACF y la PACF?
R: Decaimiento exponencial en los rezagos estacionales de la ACF y un único pico significativo en el rezago 12 de la PACF.

P: ¿Qué requisito impone la comparación de modelos por AICc?
R: Exige el mismo orden de diferenciación en todos los modelos comparados; las comparaciones de RMSE en prueba pueden involucrar cualquier modelo.

P: ¿Qué prueba se usa para validar los residuos de un modelo ARIMA estacional?
R: La prueba de Ljung-Box (Box.test con type="Ljung").

P: ¿Qué se hace si ningún modelo pasa todas las pruebas de residuos?
R: Se usa el mejor modelo disponible aunque no las supere todas.

P: ¿Cuál es la relación entre los modelos de suavizado exponencial lineales y ARIMA?
R: Todos los modelos de suavizado exponencial lineales son casos especiales de ARIMA, pero los no lineales no tienen contraparte ARIMA y muchos modelos ARIMA no tienen equivalente en suavizado exponencial.

P: ¿Qué equivalencias ARIMA tienen el suavizado exponencial simple y el método de Holt?
R: Suavizado exponencial simple ≡ ARIMA(0,1,1); método de Holt ≡ ARIMA(0,2,2); Holt amortiguado ≡ ARIMA(1,1,2).

P: ¿Qué propiedad de estacionariedad tienen todos los modelos ETS?
R: Son todos no estacionarios: los que tienen estacionalidad o tendencia no amortiguada (o ambas) tienen dos raíces unitarias; el resto, una.

## Preguntas de autoevaluación

P: ¿Por qué un ARIMA(1,1,1)(1,1,1)₄ genera términos en rezagos como yₜ₋₅ o yₜ₋₆ y no solo en rezagos contiguos o múltiplos de 4?
R: Porque al multiplicar los factores de la parte no estacional y estacional aparecen productos cruzados que combinan rezagos, produciendo términos alrededor de los múltiplos de m (yₜ₋₁, yₜ₋₂, yₜ₋₄, yₜ₋₅, yₜ₋₆…). (Sección "El modelo estacional y su notación")

P: En el ejemplo del comercio minorista trimestral europeo, ¿qué llevó a proponer ARIMA(0,1,1)(0,1,1)₄ como candidato inicial?
R: Se concluyó que d=1 y D=1 eran necesarios; un pico en el rezago 1 de la ACF sugirió MA(1) no estacional y un pico en el rezago 4 sugirió MA(1) estacional. (Sección 8.3)

P: ¿Cómo se supo que el ARIMA(0,1,1)(0,1,1)₄ inicial no era adecuado y qué modelo lo mejoró?
R: Los residuos mostraban picos significativos en el rezago 2 (y quizá el 3); comparando por AICc, el ARIMA(0,1,3)(0,1,1)₄ (68.53) mejoró frente al (0,1,2)(0,1,1)₄ (74.36). (Sección 8.3)

P: ¿Qué diferencia hubo entre auto.arima por defecto y la búsqueda exhaustiva en euretail?
R: `auto.arima(euretail)` eligió ARIMA(1,1,1)(0,1,1)₄ (AICc 69.11), mientras que `auto.arima(euretail, stepwise=FALSE, approximation=FALSE)` encontró ARIMA(0,1,3)(0,1,1)₄ (AICc 68.53), coherente con la identificación manual. (Sección 8.3)

P: En la serie H02, ¿qué decisiones de diferenciación e identificación llevaron al candidato ARIMA(3,0,0)(2,1,0)₁₂?
R: Se eligió D=1 y d=0; picos en la PACF en los rezagos 12 y 24 sugirieron AR(2) estacional y otros picos de la PACF sugirieron un posible AR(3) no estacional. (Sección 8.4)

P: ¿Por qué se eligió finalmente el ARIMA(3,0,1)(0,1,2)₁₂ para pronosticar H02?
R: Tiene el menor RMSE fuera de muestra (0.0622) y el mejor AICc entre modelos con menos de 6 parámetros. (Sección 8.4)

P: ¿Por qué la comparación por RMSE fuera de muestra requiere un esquema de entrenamiento y prueba como el de la función getrmse?
R: Porque permite evaluar el desempeño predictivo sobre datos no usados en el ajuste; en H02 se usó entrenamiento jul 91 – jun 06 y prueba jul 06 – jun 08. (Sección 8.4)

P: ¿Es correcto afirmar que ARIMA es más general que el suavizado exponencial?
R: No; es un mito. Los ETS lineales son casos especiales de ARIMA, pero los ETS no lineales no tienen contraparte ARIMA y Holt-Winters multiplicativo no tiene equivalencia ARIMA. (Sección 8.5)

## Puntos a dominar

- Leer y expandir la notación ARIMA(p,d,q)(P,D,Q)ₘ identificando cada factor de la ecuación.
- Distinguir en ACF/PACF los picos estacionales: MA estacional en la ACF, AR estacional en la PACF.
- Elegir d y D para lograr estacionariedad antes de identificar p, q, P, Q.
- Comparar candidatos por AICc (con igual diferenciación) y por RMSE fuera de muestra.
- Validar residuos con la prueba de Ljung-Box y reconocer cuándo usar el mejor modelo aunque no pase todas las pruebas.
- Apoyarse en auto.arima y en búsquedas exhaustivas (stepwise=FALSE, approximation=FALSE).
- Conocer las equivalencias entre ETS y ARIMA y los límites de cada enfoque.
