# Doing Data Science — Cathy O'Neil & Rachel Schutt (O'Reilly, 2013)
## Capítulo 13 — Lessons Learned from Data Competitions: Data Leakage and Model Evaluation (Lecciones aprendidas de las competiciones de datos: fuga de datos y evaluación de modelos)

> Nota de extracción: texto obtenido de la capa de texto del PDF; las citas usan la página del PDF `(PDF p. N)`.

## Lo que necesitas saber
Este capítulo recoge la charla invitada de Claudia Perlich, Chief Scientist en Media 6 Degrees (M6D), ganadora repetida del KDD Cup y de otras competiciones (ILP 2005, INFORMS 2008, Kaggle HIV 2010) y después organizadora (INFORMS 2009, Heritage Health Prize 2011). A partir de su experiencia compitiendo, explica dos lecciones que considera descuidadas en la academia: la *data leakage* (fuga de datos) y la evaluación de modelos.

La tesis central de Perlich es que la habilidad más importante y difícil de enseñar de un data scientist es entender los datos y el dominio: saber cómo se generaron los datos. La fuga de datos —información que no estaría disponible en el momento real de la predicción— permite ganar competiciones pero produce modelos inútiles en producción. Evitarla exige un corte temporal estricto y conocer cómo se creó cada dato.

Sales sabiendo reconocer casos típicos de fuga (efectos confundidos con causas, problemas de muestreo, artefactos de preparación de datos), cómo prevenirla, y por qué la accuracy es una mala métrica. Perlich defiende evaluar por separado el *ranking* (curva ROC, lift) y la *calibración* (buckets de probabilidad predicha frente a observada), y elegir algoritmo y métrica según el tamaño y la naturaleza de los datos.

## El perfil de Claudia Perlich y la vida de una Chief Data Scientist
Perlich arranca preguntando con qué referencia se evalúa uno su propio perfil de data scientist. En su tabla de perfil se califica fuerte en Machine Learning y Data, sólida en Computer Science (dos másteres, "I can hack, not production code"), pasable o débil en Visualization, Math, Stats y Presentation, y ante Domain responde que es la pregunta equivocada. Sostiene que la habilidad clave ausente del perfil del Capítulo 1 es precisamente *Data*, y que es la más difícil de describir.

Con 15 años trabajando con datos, su intuición nace de meterse en el *data generating process* (proceso de generación de los datos), su parte favorita del trabajo. Sus herramientas principales son Unix, sed, awk, Perl y SQL, y modela con regresión logística, k-nearest neighbors y otros métodos, dedicando mucho tiempo a montar bien el problema. Reparte su tiempo en 40% "contributor" (trabajo directo con datos), 40% "ambassador" (escribir, dar charlas, comunicación externa de M6D) y 20% "leadership" de su grupo.

Sobre ser mujer en el campo, comenta que la intuición es útil y que a las mujeres se las recuerda; cita un paper de 2003 de Shawndra Hill y Foster Provost que muestra que se puede adivinar quién escribió un artículo con un 40% de acierto solo por las citas, de modo que hacer los papers "blind" no garantiza eliminar el sesgo.

## Tipos de competición y cómo ser buen modelador
Perlich distingue dos clases de competición. La "sterile" te entrega una matriz limpia y preparada, una medida de error estándar y features a menudo anonimizadas: es un problema puro de machine learning donde ganan los algoritmos, las máquinas potentes y los grandes ensembles (ejemplos: KDD Cup 2009, el Netflix Prize y muchas competiciones de Kaggle). La "real world" te da datos crudos repartidos en varias tablas difíciles de unir; tú montas el modelo y defines evaluaciones específicas de la tarea (ejemplos: KDD Cup 2007, 2008 y 2010). Esta segunda, que ella prefiere, simula mejor la vida real y exige practicar con el desorden.

Para Perlich, entender los datos y el dominio es la habilidad más importante, y no se enseña: se cultiva. Señala tres lecciones poco tratadas en la academia:

- **Leakage**: el mejor amigo del concursante y la peor pesadilla del organizador y del profesional; siempre hay algo mal en los datos.
- **Medidas de rendimiento reales**: ir más allá de MSE, tasa de error de clasificación o AUC; por ejemplo, el beneficio (profit).
- **Construcción/transformación de features**: los datos reales rara vez llegan en una matriz perfecta.

## Data Leakage
En el paper del KDD 2011 "Leakage in Data Mining: Formulation, Detection, and Avoidance", Perlich con Shachar Kaufman y Saharon Rosset retoman a Dorian Pyle, que habla de *anachronisms* (algo fuera de lugar en el tiempo) y dice que un rendimiento "too good to be true" es una señal inequívoca. Ellos lo llaman *data leakage* en el contexto del modelado predictivo. La leakage es información que ayuda a predecir pero cuyo uso no es legítimo; a menudo es un artefacto de invertir causa y efecto. Es un problema enorme, no solo en competiciones.

Los ejemplos que recorren esta sección ilustran cómo aparece la fuga:

- **Predicción de mercado (S&P)**: una entrada ganadora alcanzó un AUC de 0.999. Como los mercados son casi aleatorios, ese valor delata leakage: alguna variable del dataset era muy predictiva del S&P pero no estaría disponible en tiempo real.
- **Amazon, grandes compradores**: el modelo descubrió que "Free Shipping = True" predecía muy bien el gasto alto. Pero el envío gratis es un *efecto* de gastar mucho (se ofrece tras superar, p. ej., $50) y es simultáneo a la venta. Hay que usar solo datos previos y eliminar esa variable manualmente.
- **Joyería (muestreo)**: `sum(revenue) = 0` predecía perfectamente a los compradores de joyas, porque al preparar los datos se quitaron las compras de joyería pero solo se incluyó a quien había comprado algo; esos clientes solo habían comprado joyas. Es un problema de muestreo común.
- **IBM, websphere**: tener la palabra "websphere" en la web de la empresa predecía la compra. Pero un cliente potencial, por definición, aún no lo había comprado; el dato de hoy contiene la información filtrada de que acabaron comprándolo. No se puede rastrear la Web del pasado.
- **Cáncer de mama**: el *patient ID* tenía poder predictivo porque se mezclaron bases de datos de distintos centros, algunos con pacientes más enfermos. Esto abrió un debate: renumerar y aleatorizar no basta; lo clave es saber para qué se usará el modelo.
- **INFORMS, neumonía**: incluir el número de códigos de diagnóstico como feature categórica (AUC 0.90) superaba a usarlo como numérica (0.80). El preparador había retirado el código 486 (neumonía) sustituyéndolo por "–1" y desplazando los demás a la izquierda; eso revelaba quién tenía solo neumonía o ninguna, lo bastante para ganar.

**Warning sobre muestreo de usuarios**: analizar un solo día de tráfico sobrerepresenta a los usuarios frecuentes. En el ejemplo de 80 usuarios, 10 vienen a diario y 70 una vez por semana; cualquier día ves 20, de los que 10 son los diarios: representan el 50% de la muestra siendo solo el 12.5% de la base.

**Leakage happens**: aunque no explotes la fuga a propósito, tu modelo lo hará por ti. Ganar por leakage es más fácil que construir buenos modelos.

## Cómo evitar la fuga
El riesgo de leakage aparece siempre que preparas, limpias, imputas valores faltantes o eliminas outliers: puedes distorsionar los datos hasta que el modelo funcione sobre tu dataset "limpio" pero fracase en el mundo real. Consejos de Perlich:

- Aplicar un **corte temporal estricto**: eliminar toda la información inmediatamente anterior al evento de interés (p. ej., lo que sabes antes de que ingrese un paciente).
- Poner un **timestamp** en cada dato que corresponda al momento en que lo aprendiste, no al momento en que ocurrió.
- Evitar quitar columnas y filas (genera inconsistencias rastreables); mejor empezar de cero con datos crudos y limpios tras pensarlo bien.
- Saber **cómo se crearon los datos**.

El paper propone una metodología en dos fases: etiquetar cada observación con *legitimacy tags* durante la recolección y luego aplicar una *learn-predict separation*.

## Evaluación de modelos
Con algoritmos potentes buscando patrones, el peligro es el **overfitting**: "si buscas lo suficiente, encontrarás algo" aunque no generalice. Se combate con cross-validation y reduciendo la complejidad del modelo. La imagen clásica de Hastie y Tibshirani (*Elements of Statistical Learning*) muestra regresión lineal (underfit), 15-NN (buen ajuste) y 1-NN (overfit). El modelo importa: los árboles de decisión sin podar son los que más sobreajustan, por eso se usan árboles podados.

**Accuracy: meh.** Perlich la descarta como mala métrica: no sirve para regresión y, en clasificación con clases desbalanceadas, un modelo tonto ("di siempre 1") puede ser muy accurate y a la vez malo.

**Importan las probabilidades, no los 0 y 1.** Nadie decide sobre el resultado binario: quieres la *probabilidad* de tener cáncer, no un sí/no. Perlich propone evaluar por separado:

- **Ranking**: con la curva ROC y su área (AUC, típicamente de 0.5 a 1.0), independiente de escala y calibración. También la *lift curve*, calculada respecto a un baseline (un lift de 3 es 3 veces mejor que mostrar anuncios al azar).
- **Calibración**: ¿son exactas las probabilidades? Como no se mide directamente, se agrupan predicciones en buckets (p. ej. 0.50–0.55) y se compara la probabilidad predicha con la empírica. Un buen modelo cae sobre la recta x = y. Los árboles de decisión calibran mal porque optimizan la *pureza* y dan predicciones más extremas que la realidad; la regresión logística calibra mejor.

## Elegir algoritmo y métrica
No es trivial: probar en datasets pequeños puede engañar, porque el mejor algoritmo puede cambiar al aumentar el tamaño de la muestra (los árboles rinden bien solo con datos suficientes). Elige el algoritmo según el tamaño y la naturaleza de los datos, y la métrica según los datos y aquello en lo que quieras ser bueno: la suma de errores al cuadrado es la pérdida de máxima verosimilitud si los datos son normales; para la mediana usa errores absolutos; para un cuantil, error absoluto ponderado. En una competición de predecir el número de ratings de una película en el próximo año asumieron una distribución de Poisson y buscaron en la literatura una métrica específica dependiente del parámetro λ.

## Un ejemplo final
Para una campaña de caridad: enviar la carta a toda la lista recauda unos $9,000, pero solo da ~5% de la gente y se quiere ahorrar. Un árbol podado da $0 de beneficio (nunca halla una hoja con mayoría de positivos); una red neuronal solo $7,500. Descomponiendo la decisión en dos —si la persona dona y cuánto dona— se modela:

```
E[$ | person] = P(response = "yes" | person) · E[$ | response = "yes", person]
```

El primer modelo debe estar bien calibrado (importa el número, no solo el ranking), así que se usa regresión logística; el segundo se entrena con ejemplos de donaciones. El modelo descompuesto logra $15,000 de beneficio. Con datos infinitos no haría falta descomponer; además se multiplican errores, lo que es problemático si están correlacionados.

## Parting Thoughts
Según Perlich, los humanos no estamos hechos para entender datos —están fuera de nuestros sentidos— sino el lenguaje, y tampoco entendemos bien la incertidumbre por nuestros sesgos. Por eso modelar personas en el futuro es más difícil que etiquetar lo ya ocurrido. Aun así, lo hacemos lo mejor posible: generando datos con cuidado, pensando bien cuál es el problema, modelándolo con datos cercanos a cómo se usará, optimizando lo que realmente deseamos y conociendo qué algoritmos encajan con cada tarea.

## Ideas clave
- La habilidad más valiosa y menos enseñable del data scientist es entender los datos, el dominio y su proceso de generación.
- La *data leakage* es información no disponible en el momento real de la predicción; suele ser causa y efecto invertidos o artefactos de preparación.
- Un rendimiento "too good to be true" (AUC cercano a 1) delata fuga, no un buen modelo.
- Casos típicos: free shipping en Amazon, `sum(revenue)=0` en joyería, "websphere" en IBM, patient ID en cáncer, código 486 en neumonía.
- El muestreo mal pensado (un solo día de tráfico) sobrerepresenta a los usuarios frecuentes.
- Para evitar leakage: corte temporal estricto, timestamps de cuándo lo supiste, datos crudos desde cero y saber cómo se crearon.
- Evalúa ranking (ROC/AUC, lift) y calibración (buckets) por separado; la accuracy es mala métrica y lo que importa son las probabilidades.
- Los árboles sin podar sobreajustan y calibran mal (optimizan pureza); elige algoritmo y métrica según el tamaño y la naturaleza de los datos.
