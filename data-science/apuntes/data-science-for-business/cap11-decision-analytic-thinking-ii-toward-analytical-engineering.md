# Data Science for Business — Foster Provost & Tom Fawcett (O'Reilly, 2013)
## Capítulo 11 — Decision Analytic Thinking II: Toward Analytical Engineering (Pensamiento analítico para la decisión II: hacia la ingeniería analítica)

> Nota de extracción: texto obtenido de la capa de texto del PDF; las citas indican la página como (PDF p. N).

## Lo que necesitas saber

Resolver problemas de negocio con data science empieza por la *ingeniería analítica*: diseñar una solución analítica a partir de los datos, las herramientas y las técnicas disponibles. El capítulo insiste en que la realidad es desordenada: los problemas de negocio rara vez vienen envueltos como un problema limpio de clasificación, regresión o clustering. Son simplemente problemas de negocio, y es tarea del equipo de datos traducirlos a algo que las técnicas conocidas puedan atacar.

La tesis central es que el *marco de valor esperado* (del Capítulo 7) sirve para descomponer un problema de negocio en subproblemas tratables con técnicas probadas, y luego recomponer los resultados en una solución del problema original. El valor esperado es una suma de productos de probabilidades por valores, y data science ofrece métodos para estimar ambos.

Se desarrolla con dos casos de estudio —una campaña de recaudación benéfica y el ejemplo recurrente de *churn*— que muestran cómo el mismo marco guía el entendimiento del negocio, la formulación de datos, el modelado y la evaluación. Sales sabiendo que el objetivo de la ingeniería analítica no es modelar cada contingencia, sino hacer explícito el papel del data mining y tomar las simplificaciones de forma consciente.

## El ejemplo que recorre el capítulo

Dos casos hilan el capítulo: (1) seleccionar los mejores prospectos para un *mailing* benéfico, y (2) el problema de churn en una operadora inalámbrica, retomado con más sofisticación. Ambos se estructuran con el marco de valor esperado.

## Targeting the Best Prospects for a Charity Mailing

El marketing dirigido es un caso de estudio ideal: muchos negocios tienen problemas con esa misma forma (marketing de base de datos, cupones personalizados, *ad targeting* online) y su estructura reaparece en otros problemas como el churn. Una organización de recaudación quiere solicitar donaciones a un "buen" subconjunto de donantes, cuidando su presupuesto y la paciencia de los prospectos.

Un *data miner* pensaría de inmediato en modelar la probabilidad de que cada prospecto responda a la oferta. Pero pensando en el problema de negocio real, la respuesta varía: unos donan \$100 y otros \$1. Maximizar el número de donaciones no sirve si cada una deja \$1 y cuesta \$1 captarla. Lo que se quiere es maximizar el *beneficio* de las donaciones (el neto tras costes). Tenemos métodos para estimar la probabilidad de respuesta (estimación de probabilidad de clase sobre un resultado binario), pero no está claro que tengamos métodos para estimar el beneficio directamente.

## El marco de valor esperado: descomponer y recomponer

El beneficio esperado de dirigirse al consumidor x se escribe como:

```
Beneficio esperado de targeting = p(R | x) · vR(x) + (1 - p(R | x)) · vNR(x)
```

donde p(R | x) es la probabilidad de respuesta, vR(x) el valor de una respuesta (donación menos coste de la solicitud) y vNR(x) el valor de no responder (cero menos el coste). El beneficio esperado de no dirigirse es cero (se asume que nadie dona espontáneamente). La clave: vR(x) y vNR(x) también se pueden estimar de los datos mediante regresión. Además, vR(x) debe estimarse con un modelo entrenado *solo con quienes respondieron*, lo que resulta más útil que estimar la respuesta de un consumidor en general, porque la gran mayoría no responde y el modelo no sabría distinguir un valor cero por no-respuesta de uno pequeño por las características del consumidor.

El marco descompone el problema en subproblemas (estimar probabilidades y estimar valores) y muestra cómo recomponer las piezas. Para este caso el resultado es intuitivo: enviar el correo a quienes su donación esperada supere el coste del envío. Siendo dR(x) la donación estimada si responde y c el coste:

```
p(R | x) · dR(x) > c
```

es decir, la donación esperada debe superar el coste de la solicitud.

## Un breve inciso sobre el sesgo de selección

Los datos de donaciones pasadas pueden estar sesgados: no son una muestra aleatoria de toda la población, sino de quienes respondieron antes. Es análogo a modelar solvencia crediticia a partir de clientes a los que ya se les concedió crédito. La pregunta clave para el científico de datos es: ¿se espera que el procedimiento de selección que sesga los datos influya también en el valor de la variable objetivo? En la solvencia, claramente sí. En las donaciones es menos directo, pero es razonable pensar que quien dona sumas grandes dona con menos frecuencia (alguien da \$100 e ignora varias campañas), de modo que la muestra de donantes pasados se sesga hacia quienes donan menos. Existen técnicas para manejar el sesgo de selección —fuera del alcance del libro—; se remite a Zadrozny & Elkan (2001) y Zadrozny (2004) para este caso concreto.

## El ejemplo de churn revisitado con más sofisticación

El problema de negocio real no es retener al máximo de clientes, sino perder menos dinero. Por eso hay que incorporar el valor del cliente. En churn ese valor es más fácil de estimar: con los registros de facturación se puede extrapolar el valor futuro (condicionado a que se quede). Representar el beneficio esperado de dirigirse a un cliente como en el caso de donaciones:

```
Beneficio esperado de targeting = p(S | x) · vS(x) + (1 - p(S | x)) · vNS(x)
```

donde p(S | x) es la probabilidad de que el cliente *se quede* (Stay) tras ser contactado. Pero si se simplifica asumiendo vNS(x) = 0, el beneficio queda p(S | x) · vS(x): ¡eso apunta a quienes tienen mayor probabilidad de quedarse, no de irse! El error es que no queremos targetear a quien más valor daría si se queda, sino a aquellos donde *perderíamos más valor si se fueran*. El marco del valor esperado permite trabajar ese razonamiento sistemáticamente.

## Evaluando la influencia del incentivo

Hay que calcular por separado el beneficio de contactar y de no contactar, haciendo explícito el coste c del incentivo (que, por simplicidad, se asume que se incurre tanto si el cliente se queda como si se va). Siendo uS(x) y uNS(x) los beneficios si se queda o se va, sin contar el incentivo, y condicionando la probabilidad de quedarse a contactar (T) o no (notT):

```
EB_T(x)    = p(S | x, T)    · (uS(x) - c) + (1 - p(S | x, T))    · (uNS(x) - c)
EB_notT(x) = p(S | x, notT) · (uS(x))     + (1 - p(S | x, notT)) · (uNS(x))
```

Queremos targetear a los clientes con mayor EB_T(x) − EB_notT(x). Es una formulación bastante más compleja que las anteriores, pero el marco la estructura. Lo nuevo aquí es que hay que considerar qué pasaría si no contactáramos (comparar EB_T y EB_notT) y la influencia real del incentivo (su diferencia). Esto conecta con el *análisis causal*: crear una situación contrafactual que compara los casos "tratado" y "no tratado" (se amplía en el Capítulo 12).

Asumiendo cero valor si el cliente no se queda, el *valor de targeting* se descompone (Ecuación 11-1):

```
VT = Δ(p) · uS(x) - c
```

donde Δ(p) es el cambio en la probabilidad de quedarse según se contacte o no. Resultado intuitivo: targetear a los clientes con mayor cambio en su probabilidad de quedarse, ponderado por su valor si se quedan; es decir, los de mayor cambio en valor esperado por el contacto.

## De la descomposición del valor esperado a la solución de data science

La Ecuación 11-1 indica exactamente qué modelos construir: dos modelos separados de estimación de probabilidad, p(S | x, T) y p(S | x, notT) —probabilidad de quedarse si se contacta y si no—, con los que luego se calcula el valor esperado del targeting. También enfoca el *entendimiento de los datos*: hacen falta muestras de clientes cuyo contrato haya vencido lo suficiente como para saber si se quedaron o se fueron, una muestra de contactados (para el primer modelo) y otra de no contactados (para el segundo), cuidando que sean representativas (sesgo de selección) y que no haya cambiado nada sustancial en el entorno (ejemplo: el iPhone exclusivo de AT&T).

El problema surge con p(S | x, T): es una oferta nueva, nadie la ha visto, no hay datos. Opciones que el marco hace visibles:

- **Simplificar**: asumir p(S | x, T) = 1 (todos se quedan con la oferta). Entonces se targetea a los de mayor (1 − p(S | x, notT)) · uS(x), es decir, la mayor pérdida esperada si se fueran.
- **Usar una etiqueta *proxy***: p. ej. una oferta pasada similar, o eventos distintos como visitar el sitio de la marca en lugar de la conversión real (Dalessandro et al., 2012).
- **Invertir en datos**: targetear para generar datos, aplicando el primer principio: los datos son un activo. Es el caso de Signet Bank, que asumió pérdidas haciendo ofertas amplias y con esos datos se convirtió en Capital One. La inversión se gestiona con la *curva de aprendizaje* (Capítulo 8), midiendo mejora sobre una línea base (el modelo simple de churn) y abortando si no compensa. Aun si se aborta, no fue un desperdicio: se invirtió en información.

El marco también permite extensiones: comparar múltiples ofertas o parametrizar el descuento para optimizar el valor esperado por cliente.

## Summary

Los ejemplos de donaciones y churn muestran cómo el marco de valor esperado articula el verdadero problema de negocio y el papel del data mining. Siempre se puede elaborar el problema con más detalle, pero el modelado exige simplificaciones para ser tratable. Habrá puntos donde haya que concluir: no hay datos para este evento, modelarlo con precisión sería demasiado caro, el evento es tan improbable que se ignora, o la formulación es suficiente por ahora. El objetivo de la ingeniería analítica no es cubrir cada contingencia, sino pensar los problemas de forma analítica para que el papel del data mining sea claro, se consideren restricciones, costes y beneficios, y las simplificaciones se hagan consciente y explícitamente: así aumenta la probabilidad de éxito y se reduce el riesgo de sorpresas en el despliegue.

## Ideas clave

- La ingeniería analítica diseña la solución a partir de datos, herramientas y técnicas; los problemas de negocio no vienen como problemas limpios de ML.
- El marco de valor esperado descompone un problema en subproblemas (estimar probabilidades y valores) y recompone las piezas en la solución.
- En el mailing benéfico la regla óptima es simple: enviar si la donación esperada supera el coste, p(R | x) · dR(x) > c.
- vR(x) se estima con un modelo entrenado solo sobre quienes respondieron, evitando el ruido de los muchos ceros por no-respuesta.
- El sesgo de selección aparece cuando los datos no son una muestra aleatoria de la población objetivo; importa si afecta a la variable objetivo.
- En churn el objetivo es minimizar pérdida de valor, no maximizar retención: targetear donde Δ(p) · uS(x) es mayor.
- Hay que comparar contactar vs. no contactar (contrafactual), base del análisis causal del Capítulo 12.
- Ante la falta de datos: simplificar, usar etiquetas proxy o invertir en datos (Signet Bank → Capital One), gestionando la inversión con la curva de aprendizaje.
- Las simplificaciones son legítimas si se toman consciente y explícitamente.
