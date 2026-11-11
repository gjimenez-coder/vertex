# Vector autoregressions (Autorregresiones vectoriales) — Estudio

## Tarjetas de repaso

P: ¿Cuál es la diferencia clave entre la regresión dinámica y un VAR?
R: La regresión dinámica supone una relación unidireccional (las predictoras influyen en la variable a pronosticar pero no al revés); el VAR permite relaciones de retroalimentación y trata todas las variables de forma simétrica.

P: ¿Qué significa que en un VAR todas las variables sean "endógenas"?
R: Que todas las variables se tratan simétricamente y cada una se modela en función de los rezagos de todas las variables del sistema, admitiendo influencia mutua.

P: ¿Cómo se modela cada variable en un VAR?
R: Como función de los valores rezagados de todas las variables del sistema, incluyendo el rezago de la propia variable y el de las demás.

P: ¿Cómo se escribe un VAR(1) bivariado?
R: Con una ecuación por variable: y1,t = c1 + φ11,1·y1,t−1 + φ12,1·y2,t−1 + e1,t, y análogamente y2,t = c2 + φ21,1·y1,t−1 + φ22,1·y2,t−1 + e2,t.

P: ¿Cómo se generan los pronósticos en un VAR?
R: De forma iterativa: a un paso se usan los últimos valores observados y a dos o más pasos se sustituyen los valores futuros desconocidos por sus propios pronósticos.

P: ¿Qué ejemplo ilustra la retroalimentación entre variables en el capítulo?
R: La relación entre consumo personal e ingreso disponible: el consumo puede verse afectado por el ingreso y viceversa.

P: ¿Qué ejemplo real de influencia mutua se cita?
R: El paquete de estímulo del gobierno de diciembre de 2008, que aumentó el gasto navideño y con ello los ingresos.

P: ¿En qué cuatro situaciones resultan útiles los VAR?
R: Pronóstico conjunto de variables relacionadas sin interpretación explícita, pruebas de causalidad de Granger, análisis de respuesta al impulso y descomposición de la varianza del error de pronóstico.

P: ¿Qué es la causalidad de Granger en este contexto?
R: Probar si una variable sirve para pronosticar otra.

P: ¿Qué es el análisis de respuesta al impulso?
R: Analizar la respuesta de una variable ante un cambio repentino pero temporal en otra.

P: ¿Qué es la descomposición de la varianza del error de pronóstico?
R: Atribuir la proporción de la varianza del pronóstico de una variable al efecto de las demás variables.

P: ¿Qué funciones del paquete `vars` se usan para ajustar y diagnosticar un VAR?
R: `VARselect` (seleccionar rezagos), `VAR` (ajustar), `serial.test` (diagnóstico de residuos), `summary` y `forecast`.

P: ¿Para qué sirve la prueba de Portmanteau en un VAR?
R: Para evaluar la autocorrelación de los residuos del modelo.

P: ¿Por qué puede diferir el número de rezagos seleccionado?
R: Porque los criterios no coinciden: AIC y FPE pueden sugerir un número de rezagos y HQ y SC otro distinto.

## Preguntas de autoevaluación

1. ¿Por qué se dice que en un VAR no hay distinción entre variables dependientes e independientes?
R: Porque todas las variables se consideran endógenas y se modelan simétricamente con los rezagos de todas las variables, permitiendo retroalimentación. (Sección: "Lo que necesitas saber")

2. Escribe la estructura de un VAR(1) con dos variables y explica qué capta cada término.
R: y1,t = c1 + φ11,1·y1,t−1 + φ12,1·y2,t−1 + e1,t y y2,t = c2 + φ21,1·y1,t−1 + φ22,1·y2,t−1 + e2,t; cada ecuación incluye el rezago propio y el de la otra variable, captando la retroalimentación. (Sección: "El modelo VAR")

3. ¿Cómo se obtiene un pronóstico a dos pasos en un VAR?
R: Sustituyendo los valores futuros desconocidos (de T+1) por sus propios pronósticos, de forma iterativa. (Sección: "Pronósticos")

4. ¿Cuál de los usos de los VAR se asocia a probar si una variable ayuda a pronosticar otra?
R: Las pruebas de causalidad de Granger. (Sección: "Cuándo son útiles los VAR")

5. En el ejemplo en R, ¿qué modelo se ajusta y sobre qué datos?
R: Un VAR(3) con término constante sobre los datos `usconsumption` (consumo e ingreso de EE. UU.), con 161 observaciones y dos variables endógenas. (Sección: "Ejemplo en R con `vars`")

6. ¿Qué indica el p-valor de 0.2219 de la prueba de Portmanteau?
R: Que no se rechaza la ausencia de autocorrelación residual, es decir, los residuos no muestran autocorrelación significativa. (Sección: "Ejemplo en R con `vars`")

7. ¿Qué refleja la correlación de 0.3639 entre los residuos de consumo e ingreso?
R: La relación contemporánea entre ambas series. (Sección: "Ejemplo en R con `vars`")

8. ¿Qué rezagos resultan significativos en las ecuaciones del ejemplo?
R: En la ecuación del consumo, los rezagos del propio consumo (l1, l2, l3); en la del ingreso, el consumo rezagado un periodo y el ingreso rezagado un periodo. (Sección: "Ejemplo en R con `vars`")

## Puntos a dominar

- Distinguir la regresión dinámica (unidireccional) de los VAR (retroalimentación, todas las variables endógenas).
- Escribir y leer un VAR(1) bivariado con sus dos ecuaciones y términos de rezago cruzado.
- Explicar el cálculo iterativo de pronósticos y la sustitución de valores futuros por sus pronósticos.
- Enumerar los cuatro usos de los VAR: pronóstico conjunto, causalidad de Granger, respuesta al impulso y descomposición de la varianza.
- Conocer el flujo en R con `vars`: `VARselect`, `VAR`, `serial.test`, `summary`, `forecast`.
- Interpretar la selección de rezagos según criterios (AIC/FPE frente a HQ/SC), la prueba de Portmanteau y la correlación de residuos.
