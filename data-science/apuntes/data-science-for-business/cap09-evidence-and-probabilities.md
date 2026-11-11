# Data Science for Business — Foster Provost & Tom Fawcett (O'Reilly, 2013)
## Capítulo 9 — Evidence and Probabilities (Evidencia y probabilidades)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas usan la página del PDF `(PDF p. N)`.

## Lo que necesitas saber
Este capítulo ofrece una manera distinta de llegar a una conclusión sobre el valor del target de una instancia: tratar lo que sabemos de ella (sus features) como evidencia a favor o en contra de cada valor posible del target. Si conocemos la fuerza de la evidencia que aporta cada feature, podemos combinarla de forma probabilística para estimar la probabilidad de pertenencia a una clase. Esa fuerza se estima a partir de los datos de entrenamiento.

La tesis central es la Regla de Bayes: permite calcular la probabilidad de una hipótesis dada la evidencia a partir de cantidades más fáciles de estimar (la verosimilitud de la evidencia dada la clase, y las probabilidades a priori de la clase y de la evidencia). Aplicada a clasificación, y combinada con una fuerte suposición de independencia condicional, da lugar al clasificador Naive Bayes.

Sales sabiendo qué son probabilidad conjunta, independencia e independencia condicional; cómo se deriva y qué significa cada término de la Regla de Bayes; cómo Naive Bayes convierte un problema intratable (estimar la probabilidad de un vector completo de features) en un simple conteo de proporciones; sus ventajas (eficiencia, aprendizaje incremental) y riesgos (no fiarse de los valores de probabilidad para decisiones con costes/beneficios); y cómo modelar el "lift" de cada pieza de evidencia.

## El ejemplo que recorre el capítulo
El hilo conductor es targetizar anuncios de display online a consumidores según las páginas que han visitado. Se trabaja para un gran publisher con una campaña del hotel de lujo **Luxhote**. La instancia es un consumidor; el target es binario: ¿reservó una habitación en la semana siguiente a ver el anuncio? Las features son el conjunto de content pieces que el consumidor vio o "Likeó" (registrado vía cookies). Se busca estimar la probabilidad de reserva para targetizar a los consumidores con mayor probabilidad. El problema encaja en una familia amplia: instancias descritas por un conjunto de piezas de evidencia tomadas de una colección potencialmente enorme (clasificación de documentos, detección de spam).

## Combinar evidencia probabilísticamente
Interesa `p(C)`, la probabilidad de que un consumidor cualquiera reserve (p. ej. `p(C) = 0.0001`, 1 de cada 10.000), y sobre todo `p(C|E)`, la probabilidad de C **condicionada** a una evidencia E (el conjunto de sitios visitados). El problema: para un E concreto y específico probablemente no hayamos visto en los datos suficientes casos con esa misma combinación exacta (o ninguno). La solución es considerar las piezas de evidencia por separado y luego combinarlas.

## Probabilidad conjunta e independencia
La **probabilidad conjunta** `p(AB)` es la de que ocurran A y B. Solo cuando A y B son **independientes** (saber uno no dice nada sobre el otro) se cumple `p(AB) = p(A) · p(B)`; ejemplo: dos tiradas de un dado justo, `p(AB) = 1/36`. En general no es así: con dados trucados (cada cara igual) sacados al azar, `p(A) = p(B) = 1/6` pero `p(AB) = 1/6` porque los eventos son totalmente dependientes. La fórmula general que maneja las dependencias es:

```
p(AB) = p(A) · p(B | A)
```

En el caso independiente `p(B|A) = p(B)` y se recupera el producto; en el totalmente dependiente `p(B|A) = 1.0`. La fórmula combina las probabilidades correctamente en todos los casos, y es la base de la Regla de Bayes.

## Regla de Bayes
Como el orden de A y B es arbitrario, `p(A)·p(B|A) = p(AB) = p(B)·p(A|B)`. Dividiendo se obtiene, renombrando B como hipótesis H y A como evidencia E:

```
p(H | E) = p(E | H) · p(H) / p(E)
```

Bayes permite calcular la probabilidad de la hipótesis dada la evidencia mirando la probabilidad de la evidencia dada la hipótesis, más las probabilidades incondicionales de hipótesis y evidencia. En el ejemplo médico (H = sarampión, E = manchas rojas), estimar directamente `p(sarampión|manchas)` exigiría razonar sobre todas las causas de manchas; en cambio `p(E|H)` (probabilidad de manchas dado sarampión), `p(H)` (prevalencia de sarampión) y `p(E)` (prevalencia de manchas) son mucho más fáciles de estimar observando y contando. A menudo `p(E)` ni siquiera hay que calcularla, porque se comparan hipótesis distintas ante la misma evidencia. Bayes es la base de una gran familia de métodos (redes bayesianas, modelos de tópicos probabilísticos, HMM, campos aleatorios de Markov, etc.).

## Aplicar Bayes a la ciencia de datos
Reescrita para clasificación, Bayes estima la **probabilidad posterior** `p(C=c|E)` a partir de tres cantidades calculables de los datos: `p(C=c)`, la probabilidad **a priori** o base rate de la clase (porcentaje de ejemplos de clase c); `p(E|C=c)`, la **verosimilitud** de ver la evidencia dentro de la clase c (una pregunta "generativa": si el proceso generó una instancia de clase c, ¿con qué frecuencia se vería como E?); y `p(E)`, la frecuencia de E en todos los ejemplos. La prior puede ser subjetiva, venir de una aplicación previa de Bayes, o inferirse de los datos como base rate (enfoque que usa este método). El posterior puede usarse como estimación de probabilidad, como score para rankear, o eligiendo el `c` de máxima probabilidad.

El problema persiste: aplicar Bayes directamente exige `p(e1 ∧ e2 ∧ ⋯ ∧ ek | c)`, muy específico y difícil de medir; puede que nunca veamos ese E exacto en entrenamiento. Los métodos bayesianos lo resuelven con suposiciones de independencia probabilística.

## Independencia condicional y Naive Bayes
La **independencia condicional** es la independencia pero usando probabilidades condicionadas (aquí, a la clase). Sin suponerla, `p(AB|C) = p(A|C) · p(B|AC)`. Si se asume que A y B son condicionalmente independientes dada C, se simplifica a `p(AB|C) = p(A|C) · p(B|C)`. Suponiendo que todos los atributos son condicionalmente independientes dada la clase:

```
p(E | c) = p(e1 | c) · p(e2 | c) ⋯ p(ek | c)
```

Cada `p(ei|c)` se calcula contando la proporción de veces que aparece el feature ei en las instancias de clase c (y hay muchas ocurrencias de ei). Esto da la ecuación de **Naive Bayes**:

```
p(c | E) = [ p(e1|c) · p(e2|c) ⋯ p(ek|c) · p(c) ] / p(E)
```

Clasifica estimando la probabilidad de cada clase y reporta la de mayor probabilidad. El `p(E)` del denominador no hace falta calcularlo: para clasificar basta comparar numeradores (E es igual para todas las clases); y si se quieren las probabilidades reales, como las clases suelen ser mutuamente excluyentes y exhaustivas (reserva o no reserva), `p(E)` se expresa como suma de los numeradores de cada clase.

## Ventajas e inconvenientes de Naive Bayes
Es muy simple pero usa toda la evidencia, y es eficiente en espacio y cómputo: entrenar consiste solo en almacenar conteos de clases y ocurrencias de features. Pese a su estricta suposición de independencia, funciona sorprendentemente bien en clasificación: cuando dos evidencias son dependientes se produce un doble conteo, pero mientras apunten en la dirección correcta, para clasificar no daña; solo hace las estimaciones más extremas en la dirección correcta. Esto **sí** es un problema si se usan los valores de probabilidad en sí, por lo que Naive Bayes debe usarse con cautela para decisiones con costes y beneficios; los profesionales lo usan mucho para ranking, donde solo importan los valores relativos. Otra ventaja: es un **aprendiz incremental**, actualiza su modelo un ejemplo a la vez sin reprocesar el pasado (útil, p. ej., en filtros de spam personalizados; es la base del de Thunderbird de Mozilla). Está en casi todos los toolkits y sirve de baseline. Se extiende de atributos binarios a categóricos multivaluados y numéricos.

## Un modelo de "lift" de la evidencia
El lift mide cuánto concentra un clasificador los positivos sobre la prevalencia de la población (si la base rate de reservas es 0.01% y en la subpoblación seleccionada 0.02%, el lift es 2). Asumiendo independencia **total** de features (no solo condicional) —lo que los autores llaman Naive-Naive Bayes— la ecuación se reordena como un producto de lifts:

```
p(C=c | E) = p(C=c) · liftc(e1) · liftc(e2) ⋯     con   liftc(x) = p(x|c) / p(x)
```

Se parte de z = prior de la clase y, por cada pieza de evidencia, se multiplica z por su lift: >1 sube la probabilidad, <1 la baja. En Luxhote z se inicializa a 0.0001; visitar un sitio de finanzas multiplica por 2, un sitio de tractor-pull por 0.25. Como se tratan las evidencias como independientes, cualquier dependencia distorsiona el valor final: útil para entender datos y comparar instancias, pero el valor absoluto hay que tomarlo con cautela.

## Ejemplo: lifts de evidencia de los "Likes" de Facebook
Kosinski, Stillwell y Graepel (2013, PNAS) mostraron que los "Likes" de Facebook predicen rasgos no evidentes (tests de inteligencia, rasgos psicométricos, orientación sexual, consumo de alcohol/tabaco, religión y opiniones políticas). Con target IQ>130 (~14% de la muestra es positiva), los Likes con mayor lift incluyen Lord Of The Rings (1.69), Wikileaks (1.59), One Manga (1.57), Beethoven (1.52), Science (1.49), Star Trek (1.39) y Sheldon Cooper (1.30). Si no "Likeo" nada, mi probabilidad es la base rate (14%). Con Sheldon Cooper sube a 0.14 × 1.3 = 18%. Con Sheldon Cooper, Star Trek y Lord of the Rings: 0.14 × 1.3 × 1.39 × 1.69 = 43%. Clave: no significa que *gustar* algo indique alto IQ, sino que *declarar públicamente* el "Like" lo hace; el dato representa el acto de declarar, no el gusto.

## Evidencia en acción
Los cálculos son tan simples (contar, calcular proporciones, multiplicar y dividir) que caben en una hoja de cálculo; los autores proveen una con un ejemplo numérico de juguete del targeting de anuncios.

## Ideas clave
- Tratar cada feature como evidencia a favor/en contra de una clase y combinarla probabilísticamente; la fuerza se estima de los datos.
- Probabilidad conjunta general: `p(AB) = p(A)·p(B|A)`; solo si hay independencia se reduce a `p(A)·p(B)`.
- Regla de Bayes: `p(H|E) = p(E|H)·p(H) / p(E)`; convierte una cantidad difícil en tres fáciles de estimar y contar.
- Para clasificar suele bastar comparar numeradores; `p(E)` normalmente no se calcula.
- Naive Bayes asume independencia condicional dada la clase, reduciendo `p(E|c)` a un producto de `p(ei|c)` calculables por conteo.
- Es eficiente, incremental y un baseline habitual; efectivo para clasificación pese a su naïveté.
- Precaución: sus valores de probabilidad no son fiables para decisiones con costes/beneficios por el doble conteo de evidencias dependientes; mejor para ranking.
- El lift de cada evidencia, `p(x|c)/p(x)`, permite partir del prior y multiplicar; útil para interpretar y comparar, con el valor final tomado con cautela.
- Métodos generativos (modelan cómo cada clase genera las features) frente a discriminativos (árboles, ecuaciones lineales); Bayes es la base de la familia de métodos bayesianos.
