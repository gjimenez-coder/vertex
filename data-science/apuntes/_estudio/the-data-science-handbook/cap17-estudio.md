# Time Series Analysis (Análisis de series temporales) — Estudio

## Tarjetas de repaso

P: ¿En qué tipos de problema de ML se reformulan los problemas de series temporales?
R: Predecir un fallo es clasificación, predecir el valor futuro es regresión y buscar patrones suele resolverse con clustering o reducción de dimensionalidad.

P: ¿Cuál es el flujo de trabajo típico para convertir una serie temporal en un problema de ML?
R: Remuestreo e interpolación → preprocesado/eliminación de ruido → ventaneo → extracción de características de cada ventana para alimentar un modelo.

P: ¿Qué dos cosas distintas se llaman «series temporales» y en cuál se centra el capítulo?
R: Series reales (secuencia de números asociados a instantes) y eventos discretos con marca de tiempo; el capítulo se centra casi siempre en las primeras.

P: ¿Cómo se convierten los registros de eventos con marca de tiempo en series?
R: Contando los eventos en ventanas de tamaño fijo (eventos por día, por hora, etc.).

P: ¿Por qué se necesita el remuestreo e interpolación?
R: Porque las medidas suelen tener espaciado desigual o huecos y casi todo algoritmo requiere una serie con espaciado regular.

P: Ordena las opciones de interpolación de más simple a más sofisticada.
R: Vecino más cercano (backfill/forward fill), interpolación lineal a trozos y splines (habitualmente el spline cúbico, suave y continuamente diferenciable).

P: ¿Por qué Cady prefiere la mediana móvil frente a la media móvil?
R: La media móvil «embadurna» los picos de ruido grandes en vez de eliminarlos; la mediana móvil es más costosa pero más robusta.

P: ¿Para qué sirve la transformación logarítmica y por qué se usa en finanzas?
R: Hace que un movimiento en el eje Y tenga el mismo impacto sea cual sea el punto de partida, y muchos modelos de regresión funcionan mejor sobre la transformación que sobre los datos crudos.

P: ¿Qué componentes separa la descomposición estacional y cuáles son sus limitaciones?
R: Separa componente periódico, tendencia (calculada con LOESS) y ruido; solo funciona con periodicidad exacta y asume que los componentes son aditivos (cambios de tamaño fijo, no proporcionales).

P: ¿Qué es el ventaneo y por qué usar todas las ventanas posibles suele ser mala idea?
R: Es dividir la serie en ventanas de igual tamaño de las que se extraen características; usarlas todas genera demasiados puntos y ventanas muy solapadas, lo que invita al overfitting y alimenta datos casi duplicados.

P: ¿Qué son las «covering windows» y qué dos riesgos tienen?
R: Son ventanas contiguas sin solape; sus riesgos son que una periodicidad igual a la longitud de la ventana las haga parecer similares y que se pierda la capacidad de alinear eventos conocidos (como fallos) dentro de ellas.

P: ¿Qué significa tratar una ventana como un vector y qué permite?
R: Una ventana es un array de floats, es decir un vector numérico; permite medir distancias (euclídea o L1), agrupar con k-means, aplicar PCA y usar el producto escalar con ventanas de referencia.

P: ¿Qué hace el análisis de Fourier y con qué otra técnica es pariente conceptual?
R: Descompone la señal entera en una combinación lineal de señales periódicas; es conceptualmente pariente del PCA porque ambos son un «cambio de base».

P: ¿Qué es la FFT y cómo se obtiene el espectro en SciPy?
R: La transformada rápida de Fourier, el algoritmo para calcular el espectro; en SciPy `fft(x)` devuelve un array de números complejos (componente m = aₘ + j·bₘ) e `ifft` reconstruye la señal.

P: ¿Cómo se usa Fourier para filtrar una señal?
R: Filtro paso bajo (poner a 0 los coeficientes de alta frecuencia y reconstruir) para suavizar, y filtro paso alto (poner a 0 los de baja frecuencia) para quitar tendencias de largo plazo.

## Preguntas de autoevaluación

1. ¿Por qué el capítulo se centra en las series reales y no en los eventos con marca de tiempo?
   R: Porque las técnicas están pensadas para datos numéricos de medida y generalizan poco sobre eventos, y porque aun teniendo eventos lo que solemos querer es algo continuo (p. ej. cuántas personas visitarán el sitio el martes, no los milisegundos hasta la siguiente llegada). (Sección «Series temporales frente a eventos con marca de tiempo»)

2. ¿Qué pasos sigue el script del hilo conductor para predecir las visitas a una página de Wikipedia?
   R: Descarga la serie de vistas, la grafica, recorta outliers fijando lo que supera el percentil 95 a ese valor, descompone la señal con `statsmodels` en periódico, tendencia y ruido, y parte la serie en ventanas deslizantes de una semana para entrenar un modelo de regresión; alcanza una correlación de 0,78864. (Sección «El ejemplo que recorre el capítulo», PDF p. 249)

3. ¿Por qué es arriesgada la extrapolación al interpolar?
   R: Estimar fuera del rango de datos es «dicey business»: `interp1d` lanza error salvo que se pase `bounds_error=False`, y aun así devuelve nulos en vez de extrapolar. (Sección «Remuestreo e interpolación»)

4. ¿Qué características simples se pueden extraer de cada ventana?
   R: Media, mediana y cuartiles; desviación típica; pendiente e intercepto de una recta ajustada; o los parámetros de una curva de crecimiento/decaimiento exponencial ajustada. (Sección «Características: desde lo simple hasta tratar la ventana como vector»)

5. ¿Por qué la selección de ventanas es crítica para clustering y PCA?
   R: Porque si un patrón clave aparece al inicio de unas ventanas y al final de otras, clustering y PCA se verán muy perjudicados; todos estos métodos dependen de una buena selección de ventanas. (Sección «Características: desde lo simple hasta tratar la ventana como vector»)

6. ¿Qué indica el espectro de Fourier sobre una señal y para qué usos sirve?
   R: Si la señal es ruido el espectro es anodino; si es periódica, unos pocos coeficientes grandes bastan para reconstruirla y en sistemas físicos cada frecuencia suele corresponder a un fenómeno real. Usos: identificar periodicidad, usar la magnitud de los coeficientes como característica y filtrar (paso bajo/paso alto). (Sección «Análisis de Fourier: a veces una bala mágica»)

7. En una aplicación real como predecir fallos de máquinas, ¿por qué no bastan las características de la ventana previa a T?
   R: Esas características dicen el estado en T, pero la máquina tiene toda una vida que mirar: su edad, cuántas reparaciones ha tenido o cuántas horas ha pasado en cierto estado; además se combinan datos de tipos distintos (especificaciones físicas, tiempo de funcionamiento, condiciones de operación, registros de mantenimiento). (Sección «Series temporales en contexto: todo el conjunto de características»)

## Puntos a dominar

- Reconocer cómo cada problema de series temporales se reformula en clasificación, regresión o clustering de ML.
- Reproducir mentalmente el flujo típico: remuestreo/interpolación → suavizado → ventaneo → extracción de características.
- Distinguir series reales de eventos con marca de tiempo y saber condensar eventos contando por ventana.
- Elegir el método de interpolación según la densidad de los datos y evitar la extrapolación.
- Saber cuándo preferir la mediana móvil sobre la media móvil y cuándo aplicar la transformación logarítmica.
- Interpretar los tres componentes de la descomposición estacional y sus limitaciones (periodicidad exacta, aditividad).
- Valorar el compromiso entre ventanas solapadas (overfitting) y «covering windows» (periodicidad y alineación de eventos).
- Entender la ventana como vector y las técnicas asociadas: distancias, k-means, PCA y análisis de Fourier (FFT) con sus filtros paso bajo/paso alto.
