# The Data Science Handbook — Field Cady (Wiley, 2017)
## Capítulo 17 — Time Series Analysis (Análisis de series temporales)

> Nota de extracción: el texto se obtuvo de la capa de texto del PDF; las citas usan la página del PDF `(PDF p. N)`. Se conservan solo los fragmentos de código esenciales.

## Lo que necesitas saber
El capítulo sostiene que el análisis de series temporales es menos común en data science de lo que cabría esperar, pero que ganará peso a medida que proliferen las redes de sensores; los ingenieros eléctricos llevan décadas de ventaja en ello. Las aplicaciones típicas son predecir cuándo ocurrirá un evento (p. ej. el fallo de una máquina), proyectar el valor futuro de la serie (p. ej. el precio de una acción) e identificar patrones en corpus demasiado grandes para revisar a mano.

La tesis central es que casi todos estos problemas de negocio se reformulan como problemas de machine learning: predecir un fallo es clasificación, predecir el valor futuro es regresión, y buscar patrones suele resolverse con clustering o reducción de dimensionalidad. El grueso del capítulo trata de las técnicas para convertir una serie temporal en un problema de ML y de los retos propios de ese paso.

Sales sabiendo el flujo de trabajo habitual (remuestreo, suavizado, ventaneo, extracción de características) y las herramientas conceptuales para cada etapa: interpolación, medias y medianas móviles, descomposición estacional, tratar ventanas como vectores y, de forma destacada, el análisis de Fourier.

## El ejemplo que recorre el capítulo
El hilo conductor es un script que predice las visitas diarias a una página de Wikipedia. Descarga la serie de vistas, la grafica, recorta los outliers fijando todo lo que supere el percentil 95 a ese valor (método tosco pero útil), descompone la señal con `statsmodels` en componentes periódico, de tendencia y de ruido, y luego parte la serie en ventanas deslizantes de una semana de las que extrae características para entrenar un modelo de regresión que predice el tráfico de la semana siguiente.

Los pasos clave del tratamiento de outliers y descomposición:

```python
# Forma tosca de quitar outliers
max_views = df['views'].quantile(0.95)
df.views[df.views > max_views] = max_views

# Descomposición estacional
decomp = sm.tsa.seasonal_decompose(df['views'].values, freq=7)
```

Sobre los datos de prueba, el modelo alcanza una correlación de 0,78864 (PDF p. 249). Cady lo describe como «no es nada sofisticado», pero es lo típico de un primer intento con series temporales.

## Flujo de trabajo típico
Un flujo habitual encadena varias etapas (PDF p. 249-250): remuestreo e interpolación para pasar de datos con huecos o muestreo no uniforme a una serie uniforme (la mayoría de algoritmos lo exigen); condensación de eventos con marca de tiempo en series (p. ej. contando eventos por día); preprocesado y eliminación de ruido a nivel de serie; ventaneo (dividir la serie en ventanas); y extracción de características de cada ventana para alimentar un modelo. A veces, en lugar de proyectar su valor, se construye un modelo de la serie como proceso aleatorio, algo superficialmente parecido pero distinto.

## Series temporales frente a eventos con marca de tiempo
Se llaman «series temporales» a dos cosas muy distintas: (1) series reales, una secuencia de números asociados a instantes (precio de una acción, temperatura de un sensor), y (2) eventos discretos con una marca de tiempo. El capítulo se centra casi siempre en las primeras, por dos razones: las técnicas están pensadas para datos numéricos de medida y generalizan poco sobre eventos; y aun teniendo eventos, lo que solemos querer es algo continuo. En el tráfico de Internet, por ejemplo, importa cuántas personas visitarán el sitio el martes, no los milisegundos hasta la siguiente llegada: existe una «densidad de tráfico» continua de la que las visitas son muestras. Lo normal es convertir registros de eventos en series contando los eventos en ventanas de tamaño fijo (eventos por día, por hora, etc.).

## Remuestreo e interpolación
Con marcas de tiempo t₁…tₙ y medidas f(tᵢ) de espaciado desigual, casi todo algoritmo requiere espaciado regular, así que hay que estimar la señal en nuevos puntos Tᵢ₊₁ = Tᵢ + δ, siendo δ un parámetro que se ajusta. Las opciones, de más simple a más sofisticada:

- Interpolación por vecino más cercano (función constante a trozos), o backfill/forward fill, llevando el valor hacia adelante o atrás. Son toscas pero están integradas en casi todas las librerías; es el método «de primera mano» de Cady si los tᵢ son densos.
- Interpolación lineal a trozos.
- Splines: en vez de ajustar una recta a dos puntos, se ajusta un polinomio a tres o más; la opción común es el spline cúbico, que da una función suave y continuamente diferenciable.

En Pandas, el relleno es trivial con `df.asfreq('1min', method='backfill')`; para interpolar en puntos arbitrarios se usa `scipy.interpolate.interp1d` (lineal por defecto, o `kind="cubic"`). La extrapolación (estimar fuera del rango de datos) es «dicey business»: `interp1d` lanza error salvo que se pase `bounds_error=False`, y aun así devuelve nulos en vez de extrapolar.

## Suavizado de señales
Lo más simple es la media móvil: sustituir cada medida por la media de k medidas previas (o algunas antes y algunas después, variando solo la marca temporal). También es común usar una media ponderada, pues tiene sentido que f_smooth(tᵢ) dependa más de f(tᵢ) que de f(tᵢ₋₁). Una variante elegante es el suavizado exponencial, media ponderada con pesos que decrecen exponencialmente. La media móvil es muy popular, pero sufre con picos de ruido grandes, que acaba «embadurnando» en vez de eliminar; por eso Cady prefiere la mediana móvil (reemplazar cada punto por la mediana de los k previos): más costosa pero más robusta. Otra opción es recortar los valores para quitar outliers groseros, como en el script inicial.

## Logaritmos y otras transformaciones
A menudo conviene analizar no los datos crudos sino una función de ellos; la más importante es la transformación logarítmica, típica en finanzas, por dos razones: hace que un movimiento en el eje Y tenga el mismo impacto sea cual sea el punto de partida, y muchas veces los modelos de regresión estándar funcionan mal sobre los datos crudos pero bien sobre la transformación.

## Tendencias y periodicidad
La descomposición estacional (`seasonal_decompose`) separa una señal con comportamiento cíclico conocido en componente periódico, tendencia suave y ruido. Mirar solo la tendencia da una versión ajustada por estacionalidad (p. ej. comparar sábado con miércoles sin preocuparse del fin de semana). Las limitaciones: solo funciona si la periodicidad es exacta (bien para el tráfico web diario, mal para procesos de duración variable) y asume que ruido, estacionalidad y tendencia son aditivos (modela cambios de tamaño fijo, no proporcionales). El componente estacional se calcula promediando los días correspondientes de toda la serie; la curva de tendencia, mediante LOESS, que ajusta polinomios locales y los une sin pasar por todos los puntos.

## Ventaneo (windowing)
Aquí empieza la transición de las series hacia el ML. A diferencia de los problemas habituales con «entidades» claras (anuncios, clientes), una serie es solo una lista de medidas, y dividirla en entidades es delicado. El enfoque típico es el ventaneo: seleccionar ventanas de igual tamaño, extraer características de cada una y etiquetarlas (p. ej. ventanas de 1 hora, excluyendo aquellas en que la máquina falló, etiquetadas según si falló en la hora siguiente). Ventanear equivale a decidir con los datos disponibles al final de la ventana.

Con N medidas y ventana de longitud W hay N − W + 1 ventanas posibles. Usarlas todas (como en el script) suele ser mala idea: hay demasiados puntos y las ventanas se solapan mucho, lo que invita al overfitting y alimenta datos casi duplicados. La alternativa son las «covering windows» (ventanas contiguas sin solape), a menudo la mejor opción si la longitud es natural para el dominio (p. ej. periodos de 24 h). Sus dos riesgos: si hay periodicidad igual a la longitud de la ventana, todas parecen artificialmente similares; y se pierde la capacidad de alinear eventos conocidos (como fallos) dentro de las ventanas de forma útil. Un fallo se desaprovecha si queda en mitad de una ventana.

## Características: desde lo simple hasta tratar la ventana como vector
Entre las características simples por ventana: media, mediana y cuartiles; desviación típica; pendiente e intercepto de una recta ajustada (por mínimos cuadrados, penalización L1, etc.); o los parámetros de una curva de crecimiento/decaimiento exponencial ajustada. Pero hay más allá de la ventana: conviene extraer también características de toda la vida de la serie, como cuánto tiempo lleva (edad del dispositivo), la fecha de inicio, las estadísticas aplicadas a una ventana inicial (para comparar con el estado actual), o los parámetros de una curva ajustada a la serie entera.

Una ventana es un array de floats, es decir, un vector numérico. Esto permite medir la distancia a una ventana de referencia con la métrica euclídea o la «taxicab» (L1); si solo interesa la forma, se normaliza antes. También se pueden agrupar las ventanas con k-means y usar el clúster como característica, o —lo más frecuente— usar el producto escalar con ventanas de referencia, por ejemplo las componentes principales dominantes obtenidas por PCA. Todos estos métodos dependen críticamente de una buena selección de ventanas: si un patrón clave aparece al inicio de unas y al final de otras, clustering y PCA se verán muy perjudicados.

## Análisis de Fourier: a veces una bala mágica
El análisis de Fourier descompone la señal entera en una combinación lineal de señales periódicas (p. ej. temperatura con periodo anual de estaciones y periodo de 24 h día/noche). El teorema clave: un array de N números se expresa como un offset constante a₀ más términos sinusoidales con coeficientes aₘ y bₘ (el «espectro»); versión equivalente usa una amplitud cₘ = √(aₘ² + bₘ²) y un desfase φₘ. Si la señal es ruido, el espectro es anodino; si es periódica, unos pocos coeficientes grandes bastan para reconstruirla, y en sistemas físicos cada frecuencia suele corresponder a un fenómeno real. Es conceptualmente pariente del PCA: ambos son un «cambio de base».

El algoritmo es la transformada rápida de Fourier (FFT), «uno de los algoritmos más importantes de la historia» y pilar de la era de la información. En SciPy:

```python
from scipy.fftpack import fft, ifft
spec = fft(x)          # espectro, números complejos: componente m = am + j*bm
cm = np.abs(spec)      # magnitud
x_again = ifft(spec)   # reconstrucción
```

El espectro es un único array de números complejos (la componente m es aₘ + j·bₘ); en data science se suele volver a números reales cuanto antes. Usos habituales: identificar periodicidad (la frecuencia dominante del pulso es la frecuencia cardiaca), usar la magnitud de los coeficientes como característica de las ventanas, suavizar eliminando alta frecuencia (filtro paso bajo: poner a 0 los coeficientes altos y reconstruir) y quitar tendencias de largo plazo (filtro paso alto: poner a 0 los bajos).

## Series temporales en contexto: todo el conjunto de características
En una aplicación real se combinan datos de tipos distintos. Para predecir fallos de máquinas tendrás medidas continuas de sensores, pero también especificaciones físicas, tiempo de funcionamiento, condiciones de operación y registros de mantenimiento. Las características de la ventana previa a T dicen el estado en T, pero la máquina tiene toda una vida que mirar: su edad, cuántas reparaciones ha tenido, o cuántas horas ha pasado en cierto estado (medido por clustering sobre las ventanas de entrenamiento). Como en toda data science, la clave es extraer las características correctas, y para ello hay que entender qué fenómenos del mundo real son relevantes.

## Ideas clave
- Casi todo problema de series temporales se reformula como clasificación, regresión o clustering de ML.
- El flujo típico: remuestreo/interpolación → suavizado → ventaneo → extracción de características.
- Distingue series reales (medidas numéricas) de eventos con marca de tiempo; estos se condensan contando por ventana.
- Interpolar va de simple a sofisticado (vecino más cercano, lineal, spline cúbico); extrapolar es arriesgado.
- La mediana móvil es más robusta que la media móvil ante picos de ruido.
- La descomposición estacional separa periodicidad, tendencia (LOESS) y ruido, pero exige periodicidad exacta y es aditiva.
- El ventaneo con solape invita al overfitting; las ventanas contiguas suelen ser mejores salvo problemas de periodicidad o alineación de eventos.
- Una ventana es un vector: admite distancias, clustering, PCA y, sobre todo, el análisis de Fourier (FFT) para hallar periodicidad, extraer características y filtrar.
