# Forecasting: Principles and Practice — Rob J. Hyndman (material de taller, University of Western Australia, septiembre 2014)
## Capítulo 12 — Vector autoregressions (Autorregresiones vectoriales)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; es material de taller con sesiones de laboratorio en R (se conserva solo el código esencial) y las citas usan la página del PDF.

## Lo que necesitas saber

Este capítulo introduce los modelos de autorregresión vectorial (VAR) como alternativa a la regresión dinámica. La diferencia clave es la direccionalidad: la regresión dinámica supone una relación unidireccional, en la que la variable a pronosticar está influida por las variables predictoras pero no al revés. Los VAR, en cambio, permiten relaciones de retroalimentación y tratan todas las variables de forma simétrica, es decir, todas pasan a considerarse "endógenas" (PDF p. 128).

La idea se ilustra con la relación entre consumo personal e ingreso disponible: el consumo puede verse afectado por el ingreso disponible y viceversa. El texto cita el paquete de estímulo del gobierno de diciembre de 2008, que aumentó el gasto navideño y con ello los ingresos, como ejemplo de esa influencia mutua.

Al terminar el capítulo sabrás qué es un VAR, cómo se escribe un VAR(1) con dos variables, cómo se generan pronósticos iterativos, para qué casos resultan útiles estos modelos y cómo ajustarlos y diagnosticarlos en R con el paquete `vars`.

## El modelo VAR

En un VAR cada variable se modela como función de los valores rezagados de todas las variables del sistema. Para dos variables con un rezago, el VAR(1) es (PDF p. 128):

```
y1,t = c1 + φ11,1·y1,t−1 + φ12,1·y2,t−1 + e1,t
y2,t = c2 + φ21,1·y1,t−1 + φ22,1·y2,t−1 + e2,t
```

Cada ecuación incluye tanto el rezago de la propia variable como el rezago de la otra, lo que capta la retroalimentación entre ambas.

## Pronósticos

Los pronósticos se generan de forma iterativa, igual que en otros modelos autorregresivos. A un paso se usan los últimos valores observados; a dos o más pasos se sustituyen los valores futuros desconocidos por sus propios pronósticos (PDF p. 128):

```
ŷ1,T+1|T = ĉ1 + φ̂11,1·y1,T + φ̂12,1·y2,T
ŷ2,T+1|T = ĉ2 + φ̂21,1·y1,T + φ̂22,1·y2,T
ŷ1,T+2|T = ĉ1 + φ̂11,1·ŷ1,T+1 + φ̂12,1·ŷ2,T+1
ŷ2,T+2|T = ĉ2 + φ̂21,1·ŷ1,T+1 + φ̂22,1·ŷ2,T+1
```

## Cuándo son útiles los VAR

El texto enumera cuatro situaciones en las que los VAR resultan útiles (PDF p. 128):

- Pronosticar un conjunto de variables relacionadas cuando no se requiere una interpretación explícita.
- Probar si una variable sirve para pronosticar otra, que es la base de las pruebas de causalidad de Granger.
- Análisis de respuesta al impulso, donde se analiza la respuesta de una variable ante un cambio repentino pero temporal en otra.
- Descomposición de la varianza del error de pronóstico, donde la proporción de la varianza del pronóstico de una variable se atribuye al efecto de las demás variables.

## Ejemplo en R con `vars`

El capítulo desarrolla un ejemplo con los datos `usconsumption` (consumo e ingreso de EE. UU.) usando el paquete `vars`. El flujo esencial es: seleccionar el número de rezagos, ajustar el VAR, diagnosticar los residuos y pronosticar (PDF p. 129–130).

```r
library(vars)
VARselect(usconsumption, lag.max=8, type="const")$selection
var <- VAR(usconsumption, p=3, type="const")
serial.test(var, lags.pt=10, type="PT.asymptotic")
summary(var)
fcst <- forecast(var)
plot(fcst, xlab="Year")
```

La selección de rezagos no es unánime entre criterios: AIC y FPE sugieren 5 rezagos, mientras que HQ y SC sugieren 1 (PDF p. 129). En el ejemplo se ajusta un VAR(3) con término constante sobre una muestra de 161 observaciones y dos variables endógenas (consumo e ingreso).

La prueba de Portmanteau sobre los residuos da un p-valor de 0.2219, por lo que no se rechaza la ausencia de autocorrelación residual (PDF p. 129). En la ecuación del consumo, los rezagos del propio consumo (l1, l2, l3) resultan significativos; en la ecuación del ingreso son significativos el consumo rezagado un periodo y el ingreso rezagado un periodo (PDF p. 129–130). La matriz de correlación de los residuos muestra una correlación de 0.3639 entre consumo e ingreso, señal de la relación contemporánea entre ambas series. El resultado final es un gráfico de pronósticos a partir del VAR(3).

## Ideas clave

- La regresión dinámica es unidireccional; los VAR permiten retroalimentación y tratan todas las variables como endógenas.
- Un VAR modela cada variable con los rezagos de todas las variables del sistema; el VAR(1) bivariado tiene una ecuación por variable.
- Los pronósticos se calculan iterativamente, reemplazando valores futuros desconocidos por sus pronósticos.
- Los VAR sirven para pronóstico conjunto sin interpretación, causalidad de Granger, respuesta al impulso y descomposición de la varianza del error.
- En R, el paquete `vars` ajusta y diagnostica VAR: `VARselect`, `VAR`, `serial.test`, `summary` y `forecast`.
- La elección de rezagos puede diferir según el criterio (AIC/FPE frente a HQ/SC).
- La prueba de Portmanteau evalúa la autocorrelación de los residuos del VAR.
