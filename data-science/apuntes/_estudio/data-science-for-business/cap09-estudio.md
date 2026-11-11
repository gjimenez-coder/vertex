# Evidence and Probabilities (Evidencia y probabilidades) — Estudio

## Tarjetas de repaso

P: ¿En qué consiste la idea central del capítulo para estimar el valor del target de una instancia?
R: Tratar lo que sabemos de ella (sus features) como evidencia a favor o en contra de cada valor posible del target, y combinarla de forma probabilística; la fuerza de cada pieza se estima de los datos de entrenamiento.

P: ¿Qué es la probabilidad conjunta `p(AB)`?
R: La probabilidad de que ocurran A y B a la vez.

P: ¿Cuándo se cumple que `p(AB) = p(A) · p(B)`?
R: Solo cuando A y B son independientes, es decir, cuando saber uno no dice nada sobre el otro (ejemplo: dos tiradas de un dado justo, `p(AB) = 1/36`).

P: ¿Cuál es la fórmula general de la probabilidad conjunta que maneja dependencias?
R: `p(AB) = p(A) · p(B|A)`; en el caso independiente `p(B|A) = p(B)` y en el totalmente dependiente `p(B|A) = 1.0`.

P: ¿Cómo se enuncia la Regla de Bayes?
R: `p(H|E) = p(E|H) · p(H) / p(E)`: la probabilidad de la hipótesis dada la evidencia a partir de la verosimilitud de la evidencia dada la hipótesis y las probabilidades incondicionales de hipótesis y evidencia.

P: ¿Por qué Bayes resulta útil frente a estimar `p(H|E)` directamente?
R: Convierte una cantidad difícil en tres fáciles de estimar observando y contando; p. ej. `p(sarampión|manchas)` exigiría razonar sobre todas las causas de manchas, mientras que `p(E|H)`, `p(H)` y `p(E)` se cuentan.

P: ¿Qué tres cantidades calculables de los datos usa Bayes para la probabilidad posterior `p(C=c|E)`?
R: La prior o base rate `p(C=c)`, la verosimilitud `p(E|C=c)` y la frecuencia de la evidencia `p(E)`.

P: ¿Qué es la verosimilitud `p(E|C=c)` y por qué se la llama pregunta "generativa"?
R: Es la probabilidad de ver la evidencia dentro de la clase c; es generativa porque pregunta: si el proceso generó una instancia de clase c, ¿con qué frecuencia se vería como E?

P: ¿Qué es la independencia condicional y cómo simplifica `p(AB|C)`?
R: Es la independencia usando probabilidades condicionadas (a la clase); si A y B son condicionalmente independientes dada C, `p(AB|C) = p(A|C) · p(B|C)` en lugar de `p(A|C) · p(B|AC)`.

P: ¿Cuál es la ecuación de Naive Bayes?
R: `p(c|E) = [ p(e1|c) · p(e2|c) ⋯ p(ek|c) · p(c) ] / p(E)`, asumiendo que todos los atributos son condicionalmente independientes dada la clase.

P: ¿Por qué no hace falta calcular `p(E)` para clasificar con Naive Bayes?
R: Porque E es igual para todas las clases y basta comparar numeradores; si se quieren las probabilidades reales, `p(E)` se expresa como suma de los numeradores de cada clase (clases mutuamente excluyentes y exhaustivas).

P: ¿Por qué Naive Bayes es eficiente y qué lo hace un aprendiz incremental?
R: Entrenar consiste solo en almacenar conteos de clases y ocurrencias de features; es incremental porque actualiza su modelo un ejemplo a la vez sin reprocesar el pasado (base del filtro de spam de Thunderbird de Mozilla).

P: ¿Por qué debe usarse Naive Bayes con cautela para decisiones con costes y beneficios?
R: Porque la dependencia entre evidencias produce doble conteo que vuelve las estimaciones más extremas; no daña la clasificación ni el ranking, pero sí los valores de probabilidad en sí.

P: ¿Cómo se define el lift de una pieza de evidencia y cómo se usa el modelo "Naive-Naive Bayes"?
R: `liftc(x) = p(x|c) / p(x)`; asumiendo independencia total se parte del prior de la clase y se multiplica por el lift de cada evidencia: `p(C=c|E) = p(C=c) · liftc(e1) · liftc(e2) ⋯`.

P: En el ejemplo de los "Likes" de Facebook, ¿qué representa realmente el dato predictor?
R: El acto de *declarar públicamente* el "Like", no el gusto; declarar un Like como Sheldon Cooper, Star Trek y Lord of the Rings sube la probabilidad de IQ>130 de 14% a 43%.

## Preguntas de autoevaluación

P: ¿Por qué no se puede estimar directamente `p(C|E)` para una evidencia E concreta a partir de los datos?
R: Porque para un E específico (la combinación exacta de sitios visitados) probablemente no haya suficientes casos iguales en los datos, o ninguno; por eso se consideran las piezas de evidencia por separado y luego se combinan. (Sección: Combinar evidencia probabilísticamente)

P: Con dados trucados (cada uno con todas las caras iguales) sacados al azar, ¿por qué `p(AB) ≠ p(A)·p(B)`?
R: Porque los eventos son totalmente dependientes: `p(A) = p(B) = 1/6` pero `p(AB) = 1/6`, ya que `p(B|A) = 1.0`. (Sección: Probabilidad conjunta e independencia)

P: ¿Cómo se deriva la Regla de Bayes a partir de la probabilidad conjunta?
R: Como el orden es arbitrario, `p(A)·p(B|A) = p(AB) = p(B)·p(A|B)`; dividiendo y renombrando H como hipótesis y E como evidencia se obtiene `p(H|E) = p(E|H)·p(H)/p(E)`. (Sección: Regla de Bayes)

P: ¿Qué fuentes puede tener la probabilidad a priori `p(C=c)` y cuál usa este método?
R: Puede ser subjetiva, venir de una aplicación previa de Bayes o inferirse de los datos como base rate; este método usa el enfoque del base rate (porcentaje de ejemplos de clase c). (Sección: Aplicar Bayes a la ciencia de datos)

P: ¿Qué suposición convierte el intratable `p(e1 ∧ ⋯ ∧ ek | c)` en un simple conteo de proporciones?
R: La independencia condicional de todos los atributos dada la clase, que reduce `p(E|c)` al producto `p(e1|c) · p(e2|c) ⋯ p(ek|c)`, calculando cada `p(ei|c)` por conteo. (Sección: Independencia condicional y Naive Bayes)

P: ¿Por qué Naive Bayes funciona bien para clasificación pese a que su suposición de independencia casi nunca se cumple?
R: Porque cuando dos evidencias son dependientes se produce doble conteo, pero mientras apunten en la dirección correcta solo hace las estimaciones más extremas en esa dirección, sin dañar la decisión de clasificar. (Sección: Ventajas e inconvenientes de Naive Bayes)

P: ¿Qué significa un lift de 2 y cómo se interpreta en el modelo de lift de la evidencia?
R: Significa que la subpoblación seleccionada concentra el doble de positivos que la base rate de la población (p. ej. de 0.01% a 0.02%); en el modelo, un lift >1 sube la probabilidad y uno <1 la baja al multiplicar el prior. (Sección: Un modelo de "lift" de la evidencia)

P: ¿Qué diferencia a los métodos generativos de los discriminativos según el capítulo?
R: Los generativos modelan cómo cada clase genera las features (Bayes es su base); los discriminativos (árboles, ecuaciones lineales) modelan directamente la distinción entre clases. (Sección: Ideas clave)

## Puntos a dominar

- Distinguir probabilidad conjunta, independencia e independencia condicional, y saber cuándo aplica `p(AB) = p(A)·p(B)` frente a `p(AB) = p(A)·p(B|A)`.
- Reproducir y explicar cada término de la Regla de Bayes: posterior, verosimilitud, prior y `p(E)`.
- Entender por qué `p(E)` no se calcula para clasificar y cómo obtenerlo como suma de numeradores si se necesitan probabilidades reales.
- Derivar la ecuación de Naive Bayes a partir de la suposición de independencia condicional dada la clase.
- Saber estimar cada `p(ei|c)` como proporción de ocurrencias del feature en la clase.
- Reconocer cuándo usar Naive Bayes para ranking y no para decisiones con costes/beneficios por el doble conteo.
- Calcular la probabilidad con el modelo de lift partiendo del prior y multiplicando por `liftc(x) = p(x|c)/p(x)`.
- Interpretar que en los "Likes" de Facebook el predictor es el acto de declarar públicamente, no el gusto.
