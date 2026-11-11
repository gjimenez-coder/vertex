# The Data Science Handbook — Field Cady (Wiley, 2017)
## Capítulo 5 — Visualizations and Simple Metrics (Visualizaciones y métricas simples)

> Nota de extracción: el texto se obtuvo de la capa de texto del PDF; las citas usan la página del PDF `(PDF p. N)`. El capítulo incluye fragmentos de código en Python; aquí se conservan solo los esenciales.

## Lo que necesitas saber
La tesis del capítulo es contundente: en ciencia de datos, "si no hay una imagen, lo estás haciendo mal" (PDF p. 71). Un buen proyecto analítico empieza con visualizaciones exploratorias que ayudan a formular hipótesis y a ganar familiaridad con los datos, y termina con figuras cuidadas que hacen visualmente obvios los resultados. El verdadero procesamiento numérico queda escondido en medio, a veces casi como un detalle secundario. Cady cuenta que en varios proyectos nunca hubo machine learning: bastó con gráficos para mostrar dónde había señal.

El objetivo de las visualizaciones no es transmitir información sin más, sino transmitirla de una forma que el cerebro humano entienda y le importe. Aun así, a veces hace falta un número: los ojos nos engañan y conviene tener una estadística fría, y además los ordenadores necesitan cifras para automatizar decisiones (aunque solo sea elegir qué imágenes merecen tu atención).

Sales sabiendo cuándo y cómo usar las visualizaciones centrales (pie charts, bar charts, histogramas, boxplots, scatterplots, scatter matrices, heatmaps y series temporales) y las métricas que resumen un dato en forma numérica (media, desviación estándar, mediana, cuantiles y correlaciones). El autor recomienda memorizar la sintaxis básica de tu lenguaje para iterar sin consultar referencias.

## El ejemplo que recorre el capítulo
El hilo conductor es el famoso dataset Iris (incluido en scikit-learn): 150 especímenes de flor, 50 de cada una de tres especies, con longitud y anchura de pétalos y sépalos. El código base importa Pandas, matplotlib y sklearn, y construye un DataFrame con una columna `species`:

```python
import pandas as pd
from matplotlib import pyplot as plt
import sklearn.datasets

def get_iris_df():
    ds = sklearn.datasets.load_iris()
    df = pd.DataFrame(ds['data'], columns=ds['feature_names'])
    code_species_map = dict(zip(range(3), ds['target_names']))
    df['species'] = [code_species_map[c] for c in ds['target']]
    return df

df = get_iris_df()
```

## Herramientas de visualización en Python
La herramienta principal es matplotlib: potente y flexible, pero el eslabón más débil de la pila técnica de Python. Los gráficos pueden verse caricaturescos, la sintaxis a veces no es intuitiva y la interactividad deja que desear; casi todo se arregla ajustando la configuración, porque los valores por defecto no son buenos. Cady se queda con matplotlib por ser el estándar y por integrarse bien con las demás librerías, pero menciona alternativas que ganan terreno, sobre todo basadas en navegador como Bokeh y Plot.ly.

El código usa Pandas siempre que se puede. Las visualizaciones de Pandas son un envoltorio sobre matplotlib: normalmente generas la imagen llamando al método `plot()` de un objeto Pandas y luego usas el módulo `pyplot` de matplotlib para título, mostrar o guardar el archivo.

## Pie charts
Cady defiende el pie chart, a menudo menospreciado por "simple". Todo lo que da un pie chart se podría leer en una lista de números, pero interpretar números exige esfuerzo cognitivo, mientras que los circuitos neuronales de bajo nivel entienden un pie chart al instante. Es la ilustración más clara del principio rector: importa cómo se transmite la información. Le saca más partido en análisis exploratorio (¿cuántos clientes son mayores? ¿qué fracción de visitas viene de EE. UU.?) o al comunicar resultados de un clasificador binario. Con `kind='pie'` sobre una Series se genera uno; sobre un DataFrame con `subplots=True` se obtiene uno por columna. El texto advierte que con los ajustes por defecto el texto puede solaparse.

## Bar charts
La misma información de un pie chart puede ir en un bar chart, y a veces es más sensato (interesan los tamaños relativos de las flores, no su "porción del pastel"). Se usa `kind='bar'`. El capítulo destaca argumentos de formato: `fontsize` (suele ser demasiado pequeño por defecto), `rot` (rota el texto de las etiquetas) y `suptitle()` para el título global de la figura; Pandas etiqueta cada subplot con su columna.

## Histogramas
Es la visualización favorita del autor porque casi siempre contiene algo interesante: bultos distintos que pueden corresponder a clases reales, outliers, variación de la población. Funciona con solo un campo numérico (floats o enteros), a diferencia del scatterplot. Con `df.plot(kind='hist', subplots=True, layout=(2,2))` se ven todas las columnas. En Iris salta a la vista que `petal length` tiene distribución bimodal; al dibujar cada especie por separado (con `alpha` y `label`) se confirma que el pico de la izquierda es solo la especie setosa.

Dos grandes problemas de los histogramas:

- Número y tamaño de los bins. Bins demasiado grandes ocultan patrones dentro de un cubo; demasiado pequeños dejan muchos cubos vacíos y convierten la campana en barras de una unidad.
- Los datos pueden estropear la imagen: un cubo con muchísimos puntos aplasta a los demás (por ejemplo, un pico enorme en 0.0 que hay que filtrar).

Los outliers son el otro problema visual. A veces basta con filtrar unos pocos puntos aberrantes, pero con frecuencia lo que hay es una cola gruesa (fat tail) que representa un fenómeno real: recortarla aclara la imagen, pero elimina señal significativa eligiendo un umbral más o menos arbitrario.

## Medias, desviaciones estándar, medianas y cuantiles
Para resumir una distribución en pocos números, hay dos opciones, pensadas asumiendo una distribución acampanada: dar media y desviación estándar (históricamente populares y fáciles de calcular), o dar mediana, percentil 25 y percentil 75 (más robustas a patologías, pero más costosas porque exigen ordenar). En Pandas: `col.mean()`, `col.std()`, `col.quantile(0.5)`, `col.quantile(0.25)`, `col.quantile(0.75)`.

Si la distribución tiene varios picos, estas cifras siguen existiendo pero pierden su interpretación intuitiva. Los outliers apenas afectan a mediana y cuantiles, pero pueden ser decisivos para media y desviación estándar: con outliers grandes (p. ej. una log-normal) la media se desplaza lejos del bulto, y un solo punto puede dominarla, por lo que hace falta mucha más data incluso para estimarla. Una solución común es descartar antes los outliers (p. ej. lo que cae bajo el percentil 25 o sobre el 75):

```python
Clean_Avg = col[(col > Perc25) & (col < Perc75)].mean()
```

Esto vale si los outliers son patológicos (fallo de un sensor), pero no si son datos clave (importes de transacciones). La mediana tampoco es perfecta: con datos sesgados se aleja del bulto y no cambia aunque alteres los valores extremos, pero conserva su significado claro: la mitad de los valores está por encima y la mitad por debajo. Cady usa la mediana para lo "típico" y la media cuando el comportamiento promedio es lo que importa de negocio.

## Boxplots
Resumen un dataset mostrando mediana, cuantiles y min/máx de cada variable (`kind='box'`). En Iris deja patente que las tres especies difieren. Su ventaja es que los outliers grandes se ven de inmediato: donde el cuantil superior queda mucho más lejos de la mediana que el inferior, un histograma solo mostraría un leve engrosamiento de las colas.

## Scatterplots
Son de las formas más simples y potentes de visualizar relaciones, ideales como primer paso con un proyecto nuevo (`kind='scatter'` con `x` e `y`). Permiten meter más dimensiones mediante: color coding (categorías o mezcla continua), tamaño (`s`, también para destacar puntos) y opacidad (`alpha`, útil cuando los puntos se solapan). Argumentos de `scatter()`: `c` (color), `s` (tamaño en píxeles), `marker` (tipo de marcador) y `alpha` (transparencia). En Iris, con colores y marcadores por especie, se ve que setosa destaca por sépalos más largos y estrechos.

## Scatterplots con ejes logarítmicos
Cuando los valores son positivos pero varían en órdenes de magnitud (tráfico web, ingresos), casi todos los puntos se aplastan a un lado y el gráfico es ilegible. Con `logx=True` (o `logy=True`) el eje se vuelve logarítmico: las marcas quedan equiespaciadas en la figura pero representan incrementos pequeños a la izquierda y grandes a la derecha. En el ejemplo de Boston (criminalidad vs. valor mediano de vivienda) el eje log revela una relación inversa clara en todos los niveles de criminalidad. Solo funcionan con valores mayores que 0; si la data puede ser 0 es común sumar 1, pero con valores negativos no sirven.

## Scatter matrices y heatmaps
Como la visualización humana se agota en tres dimensiones, una solución parcial es la "scatter matrix": un scatterplot para cada par de variables (`scatter_matrix(df)`), con histogramas de cada variable en la diagonal. Otro problema de los scatterplots es el amontonamiento cuando hay muchos puntos (especialmente con enteros que caen unos sobre otros); reducir el tamaño o usar `alpha` ayuda solo hasta cierto punto. Cuando lo que importa es la densidad y no los puntos concretos, se usa un heatmap que colorea las regiones por densidad; en Pandas con `kind='hexbin'` las regiones son hexágonos ("hexbin").

## Correlaciones
La correlación mide cuán ligadas están dos variables. Dos tipos principales: Pearson (la habitual, mide cuán buena aproximación es Y = mX + b; cerca de 1 o −1 según el signo de m, pero asumir linealidad es muy restrictivo) y correlaciones ordinales (no asumen linealidad, solo relación monótona): Spearman y Kendall. En Pandas: `df[col1].corr(df[col2], method="pearson"/"spearman")`.

Ninguna correlación capta relaciones no monótonas (si Y = sin(X) sobre un rango amplio, la correlación ronda 0; lo mejor es graficar). Kendall es más robusta a datos aberrantes pero muy sensible a pequeños cambios de orden; si hay que elegir, el autor usa Spearman. ¿Qué tan fuerte es "suficiente"? Depende del contexto: a Cady le empieza a importar por encima de 0.4; hacia 0.7 se puede estimar de forma defendible una variable con la otra; por encima de 0.95 una variable es casi sinónimo de la otra (y probablemente hay algo raro en la data).

"Correlación no es causalidad": el estándar de oro son los experimentos controlados, a menudo imposibles en sociología o economía. Cady propone su regla práctica: "Si A y B están correlacionadas, ninguna causa a la otra; hay un factor C que causa ambas" (PDF p. 89), un buen generador de hipótesis. Aun así a veces sí hay causalidad (tabaco y cáncer de pulmón), pero inferirla requiere apoyarse en el conocimiento del dominio.

## Anscombe's Quartet y los límites de los números
El cuarteto de Anscombe es un dataset inventado famoso: sus cuatro conjuntos tienen idénticos media, desviación estándar, correlación y recta de mejor ajuste, pero relaciones muy distintas (lineal con ruido, no lineal pero limpia, y dos dominados por outliers). Demuestra que las métricas resumen pueden enmascarar rasgos importantes.

## Series temporales
Son uno de los tipos de dato más importantes (precios de acciones, tráfico web, glucemia) y, sin embargo, un punto débil de la ciencia de datos frente a la ingeniería. Aquí la visualización es insustituible: no existe una "suposición por defecto" que funcione como la campana, así que siempre hay que mirar los datos para saber qué es normal. Si el índice del DataFrame es de tipo datetime, Pandas formatea el eje X de forma amigable; en el ejemplo del CO2 se ve un ciclo anual y una tendencia creciente.

Recomendaciones del autor: poder hacer zoom (un pico agudo puede resultar ser una meseta); usar escala logarítmica (`logy=True`) cuando importan los cambios proporcionales, como el precio de una acción a largo plazo; al comparar muchas series, graficarlas juntas (normalizadas) o mostrar mediana y cuantiles, quizá con una muestra pequeña superpuesta; y considerar transformaciones al dominio de la frecuencia (transformada de Fourier) cuando se espera periodicidad. La visualización suele ser un medio para extraer features útiles (p. ej. la mediana del periodo) para un modelo.

## Ideas clave
- Si no hay imagen, lo estás haciendo mal: las visualizaciones son plan A–C salvo en la validación estadística final; importa transmitir la información como la entiende el cerebro.
- Elige la visualización según la pregunta: pie/bar para proporciones y resultados binarios; histograma para una variable (ideal para detectar bimodalidad y outliers); scatterplot para relaciones entre dos variables.
- Media y desviación son fáciles pero frágiles ante outliers; mediana y cuantiles son robustos. Usa mediana para lo "típico" y media para el comportamiento promedio de negocio.
- Los boxplots muestran mediana, cuantiles y extremos, y delatan outliers que un histograma disimularía.
- Los ejes logarítmicos rescatan datos que varían en órdenes de magnitud; solo con valores positivos.
- Scatter matrices, heatmaps (hexbin) y scatterplots con color/tamaño/opacidad empaquetan más dimensiones o resuelven el amontonamiento.
- Pearson asume linealidad; Spearman y Kendall solo monotonicidad. Correlación no es causalidad: busca el factor C común.
- Anscombe's quartet prueba que los números resumen engañan; en series temporales no hay sustituto para graficar.
