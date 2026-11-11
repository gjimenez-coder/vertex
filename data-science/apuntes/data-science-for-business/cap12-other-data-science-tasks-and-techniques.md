# Data Science for Business — Foster Provost & Tom Fawcett (O'Reilly, 2013)
## Capítulo 12 — Other Data Science Tasks and Techniques (Otras tareas y técnicas de ciencia de datos)

> Nota de extracción: el texto se obtuvo de la capa de texto del PDF; las citas indican la página como (PDF p. N).

## Lo que necesitas saber
El capítulo cierra el recorrido mostrando que los conceptos fundamentales ya presentados (control de complejidad, similitud, ajuste de funciones numéricas a un objetivo, supervisado vs. no supervisado, lift) son la base de muchas otras técnicas que el libro no trató en detalle. La tesis central es que la ciencia de datos se entiende mejor desde los principios, no desde algoritmos sueltos: ante un problema nuevo conviene reformularlo como una de las tareas para las que ya existen buenas herramientas (ingeniería analítica), en lugar de construir soluciones a medida desde cero.

Los autores encuadran estas tareas dentro de la "ingeniería analítica": el problema de negocio aporta el objetivo y las restricciones, los datos y el conocimiento del dominio son la materia prima, y la ciencia de datos ofrece marcos para descomponer el problema y herramientas para resolverlo. Sobre esa idea se repasan seis tareas adicionales.

Sales sabiendo reconocer y encuadrar: asociaciones y co-ocurrencias (con lift y leverage), profiling o perfilado de comportamiento típico, predicción de enlaces y recomendación social, reducción de datos e información latente (recomendación de películas), métodos de ensemble con la descomposición sesgo-varianza del error, y la explicación causal a partir de datos. En todos los casos el mensaje es el mismo: son instancias o combinaciones de los fundamentos.

## Co-ocurrencias y asociaciones: encontrar ítems que van juntos
La agrupación por co-ocurrencia o descubrimiento de asociaciones busca relaciones entre entidades a partir de las transacciones que las involucran. Aplicaciones típicas: venta cruzada en retail online ("los clientes que compraron el eWatch también compraron el eBracelet") y optimización de operaciones, como decidir qué ítems menos populares conviene almacenar en centros de distribución regionales porque co-ocurren con los más populares, reduciendo costes de envío.

La asociación se piensa como una regla: "si ocurre A, es probable que ocurra B también". Las estadísticas de lo "interesante" siguen los principios fundamentales:

- Support (soporte): porcentaje mínimo de transacciones a las que aplica la regla; es un control de complejidad contra co-ocurrencias debidas al azar (por ejemplo, exigir que aplique al menos al 0,01% de las transacciones).
- Confidence o strength (fuerza): es p(B|A), la probabilidad de que B ocurra cuando ocurre A; se exige por encima de un umbral (p. ej. 5%).

### Medir la sorpresa: lift y leverage
Además queremos que la asociación sea "sorprendente". La sorpresa fuerte (contradecir el conocimiento previo) es difícil de automatizar; en la práctica los científicos de datos y usuarios de negocio revisan listas largas descartando lo obvio. Pero hay una noción más débil y computable solo con los datos: cuánto más frecuente es la asociación de lo esperado por azar.

Lift: cociente entre la probabilidad de ver A y B juntos y la que habría si fueran independientes.

```
Lift(A, B) = p(A, B) / ( p(A) · p(B) )
```

Un lift mayor que 1 es el factor por el que ver A "aumenta" la probabilidad de ver B. Una alternativa es mirar la diferencia en lugar del cociente, llamada leverage:

```
Leverage(A, B) = p(B, A) − p(A) · p(B)
```

### Ejemplo: cerveza y billetes de lotería
En una tienda de conveniencia se observa que mucha gente compra cerveza y lotería juntas. Con p(cerveza)=0,3, p(lotería)=0,4 y p(cerveza y lotería)=0,2: si fueran independientes esperaríamos 0,3 × 0,4 = 0,12. El lift es 0,2 / 0,12 ≈ 1,67 (unas 1⅔ veces más probable que por azar). El leverage es 0,2 − 0,12 = 0,08: un aumento de ocho puntos porcentuales sobre lo esperado por ser ítems populares. Para esta asociación el support es 20% y el strength (p(lotería|cerveza)) es 67%. Conclusión: hay algo de relación, pero buena parte de la co-ocurrencia se debe a que ambos son muy populares.

### Asociaciones entre "Likes" de Facebook
La técnica es más general que el análisis de cesta de la compra. Usando los Likes de Facebook (Kosinski, Stillwell & Graepel, 2013), cada usuario tiene una "cesta" de Likes y se buscan Likes que co-ocurren más de lo esperado. Pueden añadirse virtual items (ítems virtuales), como la ubicación del usuario o datos psicométricos (extroversión, afabilidad, IQ), para hallar asociaciones con esas características. Las asociaciones se obtuvieron con el sistema Magnum Opus, filtrando las que cubren muy pocos casos; en el ejemplo, todas con lift por encima de 20 y cubriendo al menos el 1% de los usuarios (p. ej. "Family Guy & The Daily Show -> The Colbert Report", support=0,010, strength=0,793, lift=31,32).

Conviene recordar la distinción supervisado vs. no supervisado: si queremos entender qué correlaciona con una variable concreta (afabilidad, gustar de nuestra marca), lo formulamos como problema supervisado; si exploramos sin objetivo específico, la búsqueda de asociaciones es más apropiada. Un uso práctico del minado de asociaciones es explorar datos poco conocidos (p. ej. al entrar en un trabajo nuevo) para tener una visión amplia de las relaciones de gustos en la base de clientes.

## Profiling: encontrar el comportamiento típico
El profiling caracteriza el comportamiento típico de un individuo, grupo o población (p. ej. el uso típico de tarjeta de crédito de un segmento). La detección de fraude lo usa para describir el comportamiento normal y detectar desviaciones; el perfil puede ser por población, por grupos pequeños o individual (perfilar el uso internacional de cada usuario evita falsas alarmas con quien viaja a menudo).

El profiling combina conceptos previos: puede implicar clustering si hay subgrupos con comportamientos distintos, y en esencia es una instancia del concepto del Capítulo 4: definir una función numérica con parámetros, definir un objetivo y encontrar los parámetros que mejor lo cumplen. Ejemplo: perfilar el tiempo de espera en un call center calculando media y desviación típica equivale a un ajuste de modelo si asumimos distribución Normal (gaussiana); la media y la desviación son el modelo de máxima verosimilitud bajo esa suposición.

Si al visualizar la distribución no parece una campana simétrica, hay que desconfiar de reportar media y desviación: la cola larga sesga la media al alza (en el ejemplo, la media de 100 no representa la espera normal). Puede reportarse la mediana o ajustar otra distribución. Un truco común para datos sesgados es tomar el logaritmo: los logaritmos de los tiempos de espera sí parecen una campana (una distribución log-normal), lo que justifica reportar media y desviación de los log-tiempos.

La idea se extiende: para perfilar dos variables correlacionadas (gasto y tiempo en el sitio web) se ajusta una gaussiana bidimensional (una "campana ovalada"). Si creemos que hay subgrupos, ajustamos varias gaussianas con un Gaussian Mixture Model (GMM); con k=2 el ajuste identifica dos grupos de clientes. El GMM produce un clustering distinto del Capítulo 6: un clustering "suave" o probabilístico, donde cada punto tiene un grado o probabilidad de pertenencia a cada cluster en lugar de pertenecer estrictamente a uno. Esto muestra que son los principios, no las tareas o algoritmos concretos, la base de la ciencia de datos.

## Predicción de enlaces y recomendación social
A veces es más útil predecir conexiones entre ítems que una propiedad de un ítem. La predicción de enlaces (link prediction) es común en redes sociales ("como tú y Karen compartís 10 amigos, ¿quieres ser su amiga?") y puede estimar la fuerza del enlace, como en la recomendación de películas (buscar enlaces usuario–película que aún no existen pero deberían ser fuertes).

Dos formas de encuadrarlo con los fundamentos:

- Como similitud: suponer que los enlaces se dan entre individuos similares y definir una medida de similitud (número de amigos compartidos, ponderada por comunicación, proximidad geográfica, intereses o demografía compartidos). Es aplicar "encontrar ítems similares" a personas representadas como datos.
- Como modelado predictivo: una instancia es un par de personas; la variable objetivo es si la relación existe (o se formaría si se recomienda); es una tarea supervisada porque podemos obtener datos de entrenamiento con enlaces que existen o no; los atributos son características del par (amigos en común, similitud de intereses, etc.). Una vez planteado así, se decide qué modelos aplicar y cómo evaluarlos, igual que en cualquier tarea predictiva.

## Reducción de datos, información latente y recomendación de películas
A veces queremos sustituir un conjunto grande de datos por uno más pequeño que preserve la información importante: más manejable y que puede revelar mejor lo que contiene. Normalmente implica sacrificar algo de información; lo clave es el trade-off entre el insight o manejabilidad ganados y la información perdida.

El caso guía es el Netflix Challenge: Netflix ofreció un millón de dólares a quien mejor predijera cómo valorarían los clientes las películas. El equipo ganador (Bellkor's Pragmatic Chaos) combinó dos ideas: ensembles de modelos y reducción de datos. El problema es de predicción de enlaces (predecir la fuerza del enlace usuario–película).

El enfoque popular (Koren, Bell & Volinsky, 2009) se basa en dimensiones latentes de las preferencias. "Latente" significa "relevante pero no observado explícitamente en los datos" (como los topic models del Capítulo 10). Las dimensiones latentes de preferencia de películas podrían ser serio vs. escapista, comedia vs. drama, orientación infantil, etc., o rasgos mal definidos como profundidad del personaje o rareza; emergen de los datos. Cada película y cada usuario se representan como vectores de atributos sobre esas dimensiones, y se recomienda calculando la similitud usuario–película: las más similares a las preferencias del usuario.

La Figura 12-5 muestra un espacio de gustos de dos dimensiones latentes minado de los datos de Netflix; la interpretación de los ejes la imponen las personas aplicando conocimiento del dominio (p. ej. un eje separa drama de acción) y es subjetiva. Para hallar las dimensiones se aplica el concepto del Capítulo 4: representar la similitud usuario–película como una fórmula con d dimensiones desconocidas, donde cada dimensión son pesos (coeficientes) sobre películas y clientes; el significado queda implícito en esos pesos. Se define una función objetivo (predecir mejor las valoraciones observadas, con regularización, o explicar mejor su variación) y se ajustan los parámetros: esto suele llamarse matrix factorization (factorización de matrices). Intuitivamente, el minado determina a la vez cuán "rara" es una película y cuánto le gustan al usuario las películas raras.

## Sesgo, varianza y métodos de ensemble
Los ganadores de Netflix también construyeron muchos modelos de recomendación y los combinaron en un "supermodelo": un ensemble model. Los ensembles mejoran la generalización en muchas situaciones (clasificación, regresión, estimación de probabilidad). La intuición: cada modelo es un "experto"; en vez de preguntar a uno solo, se combina a un grupo (votando o promediando). El k-NN es un ensemble simple (expertos muy sencillos); los ensembles suelen usar modelos más complejos (p. ej. promediar varios árboles).

Los ensembles ayudan cuando los expertos cometen errores distintos e idealmente independientes: al promediar, los errores tienden a cancelarse. Los errores de un modelo se caracterizan por tres factores:

1. Aleatoriedad inherente: la predicción no es determinista; la máxima exactitud teórica alcanzable es la Bayes rate (tasa de Bayes), generalmente desconocida.
2. Sesgo (bias): un procedimiento es sesgado si, por mucha data de entrenamiento que reciba, su curva de aprendizaje nunca alcanza la exactitud perfecta (p. ej. una regresión logística lineal ante una respuesta realmente más compleja).
3. Varianza (variance): como el entrenamiento usa una muestra finita, muestras ligeramente distintas dan modelos distintos; cuánto varía la exactitud entre conjuntos de entrenamiento del mismo tamaño es la varianza.

Hay un trade-off: menor varianza suele implicar mayor sesgo y viceversa. Predecir solo la tasa media de compra es baja varianza pero alto sesgo; usar mil variables da potencial de mayor exactitud pero mucha varianza (overfitting). El control de complejidad (p. ej. selección de variables) gestiona ese trade-off buscando el "punto dulce" donde la suma de ambos errores es mínima. Los ensembles funcionan porque, con métodos de alta varianza, promediar reduce la varianza de las predicciones; por eso se usan mucho con árboles (que tienen alta varianza): random forests, bagging y boosting.

## Explicación causal a partir de datos y el ejemplo del marketing viral
El modelado predictivo visto hasta aquí se basa en correlaciones, no en causación. A veces queremos saber qué influye en qué, para entender mejor el negocio o para decidir cómo intervenir y provocar un resultado deseado.

Ejemplo: el marketing viral. La idea es que "sembrar" ciertos consumidores (p. ej. dándoles el producto gratis) los convierte en influencers que aumentan la probabilidad de compra de sus conocidos. El supuesto crítico es que los consumidores realmente se influyen entre sí. Un análisis ingenuo engaña: por razones sociológicas (McPherson, Smith-Lovin & Cook, 2001), la gente se agrupa en redes con personas similares, así que los vecinos de quien compra tienden a tener preferencias parecidas y también comprarían aun sin ninguna influencia causal. Con análisis causal cuidadoso (Aral, Muchnik & Sundararajan, 2009) se mostró que los métodos tradicionales sobreestimaban la influencia en al menos un 700%.

Existen varios métodos de explicación causal, todos comprensibles dentro del marco común de la ciencia de datos: requieren entender inversiones en adquisición de datos, medidas de similitud, cálculos de valor esperado, correlación y variables informativas, y ajuste de ecuaciones. El Capítulo 11 lo anticipó con el problema de churn (a quién influye más la oferta). Otros métodos usan emparejamiento por similitud (Capítulo 6) para simular el "contrafactual", y otros ajustan funciones numéricas e interpretan sus coeficientes (con cautela: insista en entender por qué un coeficiente admite interpretación causal). El mensaje final: no se puede entender la ciencia de datos causal sin los principios fundamentales.

## Ideas clave
- Conviene reformular un problema nuevo como una tarea conocida (ingeniería analítica); los principios fundamentales sostienen casi todas las técnicas.
- Asociaciones: support (prevalencia conjunta), strength = p(B|A), lift (cociente frente a la independencia) y leverage (diferencia) miden cuán interesante es una co-ocurrencia.
- El profiling caracteriza el comportamiento típico y suele ser un ajuste de modelo (media/desviación como máxima verosimilitud bajo una gaussiana); visualizar la distribución evita resumir mal datos sesgados.
- El GMM ajusta varias gaussianas y produce un clustering "suave" (pertenencia probabilística), distinto del clustering del Capítulo 6.
- La predicción de enlaces se encuadra como similitud entre personas o como modelado predictivo donde la instancia es un par de personas.
- La reducción de datos revela información latente; la recomendación de películas (Netflix) usa dimensiones latentes y matrix factorization, interpretables solo a posteriori.
- Los ensembles reducen error combinando modelos cuyos errores son distintos; ayudan sobre todo con métodos de alta varianza como los árboles (random forests, bagging, boosting).
- El error se descompone en aleatoriedad inherente (tasa de Bayes), sesgo y varianza, con un trade-off que el control de complejidad intenta equilibrar.
- La explicación causal exige cuidado: la homofilia social puede inflar enormemente la influencia estimada en marketing viral.
