# 03 · Estadística Aplicada

Fundamentos estadísticos para describir datos y hacer inferencia: clasificación de variables, medidas descriptivas (con fórmula, justificación y origen), forma de la distribución, normalidad, correlación, asociación entre categóricas, comparación de medias e intervalos de confianza.

---

## 1. Clasificación de variables

Antes de cualquier análisis o modelo hay que identificar la naturaleza del dato.

### Cualitativas (categóricas)
Atributos que se clasifican en categorías, no se miden numéricamente.
- **Nominales:** sin orden jerárquico. *Ej.:* sexo, estado civil, color de ojos.
- **Ordinales:** con orden lógico. *Ej.:* nivel socioeconómico, calidad de servicio, tallas de ropa.

### Cuantitativas (numéricas)
Cantidades sobre las que se pueden hacer operaciones aritméticas.
- **Discretas:** valores enteros o conteos. *Ej.:* número de asistentes, cantidad de hijos.
- **Continuas:** cualquier valor en un rango, con decimales. *Ej.:* peso, ingresos, diámetros.

### Métrica de resumen recomendada por tipo

| Tipo | Subtipo | Métrica recomendada | Justificación |
| --- | --- | --- | --- |
| Cualitativa | Nominal | **Moda** | Única válida: no hay orden ni valor para promediar |
| Cualitativa | Ordinal | **Mediana** | Respeta la jerarquía de las categorías |
| Cuantitativa | Discreta | **Mediana / Moda** | Mediana si hay extremos; moda si el conteo se repite mucho |
| Cuantitativa | Continua | **Media** | La más precisa, si la distribución es simétrica |
| Cualquiera con outliers | Numérica | **Mediana** | Ignora extremos, da un centro más real |

---

## 2. Medidas descriptivas

Para cada medida: definición, fórmula, justificación, ejemplo y origen histórico.

### Tendencia central

**Media (promedio)** — centro de gravedad de los datos.
$$\bar{x} = \frac{1}{n} \sum_{i=1}^n x_i$$
Es el único valor que minimiza la suma de errores cuadrados $E(m) = \sum (x_i - m)^2$. *Ej.:* rendimientos [5,7,6,8,4]% → media 6%. *Origen:* Pitágoras (~500 a.C.), formalizado por Laplace (s. XVIII).

**Mediana** — valor central de los datos ordenados.
$$\text{Mediana} = x_{\frac{n+1}{2}} \ (n\text{ impar}); \quad \frac{x_{n/2} + x_{n/2+1}}{2}\ (n\text{ par})$$
Minimiza $\sum |x_i - m|$. *Ej.:* ingresos ordenados [1800…2500] → 2200. *Origen:* Lorenz (1905), Gini (1912).

**Moda** — valor más frecuente.
$$\text{moda} = \arg\max_v \#\{i: x_i = v\}$$
Indica el pico de densidad empírica. *Ej.:* tallas [S,S,M,L,M,M,S,M] → M. *Origen:* Edgeworth (1885).

### Dispersión

**Varianza** — promedio de los cuadrados de las desviaciones.
$$s^2 = \frac{1}{n-1} \sum_{i=1}^n (x_i - \bar{x})^2$$
El divisor $n-1$ corrige el sesgo (segundo momento central). *Origen:* R.A. Fisher (1922).

**Desviación estándar** — raíz de la varianza, vuelve a las unidades originales.
$$s = \sqrt{s^2}$$
*Origen:* Pearson (1895).

**Rango intercuartílico (IQR)** — dispersión del 50% central.
$$IQR = Q_3 - Q_1$$
Base para detectar outliers (ver documento 04). *Origen:* Wilks (1932).

**Coeficiente de variación** — compara dispersión entre escalas distintas.
$$CV = \frac{s}{\bar{x}} \times 100\%$$
*Ej.:* acciones A (CV 5%) vs. B (CV 15%). *Origen:* Pearson (1895).

### Posición y organización

**Percentiles y cuartiles** — dividen la muestra en partes iguales.
$$k = \left\lceil \frac{p}{100}(n+1) \right\rceil, \quad P_p = x_{(k)}$$
*Origen:* Galton (1884), Wilks (1928).

**Distribución de frecuencias** — conteo por intervalos.
$$n_k = \#\{x_i \in [a_k, b_k)\}, \quad f_k = \frac{n_k}{n}$$
*Origen:* Karl Pearson (1895).

---

## 3. Forma de la distribución

**Sesgo (skewness)** — asimetría de la distribución (tercer momento).
$$\gamma_1 = \frac{\frac{1}{n}\sum (x_i-\bar{x})^3}{\left(\frac{1}{n}\sum (x_i-\bar{x})^2\right)^{3/2}}$$
*Ej.:* ingresos con sesgo a la derecha ($\gamma_1 > 0$). *Origen:* Pearson (1895).

**Curtosis** — comportamiento de las colas / qué tan puntiaguda es (cuarto momento).
$$\gamma_2 = \frac{\frac{1}{n}\sum (x_i-\bar{x})^4}{\left(\frac{1}{n}\sum (x_i-\bar{x})^2\right)^2} - 3$$
*Ej.:* retornos financieros con alta curtosis. *Origen:* Fisher (1929).

> La detección y el tratamiento de outliers, el boxplot y el binning de histogramas están en `04_analisis_exploratorio_datos.md`.

---

## 4. Distribuciones y normalidad

Muchos métodos clásicos asumen normalidad de forma directa o indirecta.

- **Distribución normal:** forma de campana, simétrica, descrita por media, varianza y desviación estándar.
- **Histograma:** muestra la forma general (¿simétrica? ¿sesgada? ¿multimodal? ¿colas largas?).
- **Q-Q plot:** compara cuantiles observados vs. esperados de una normal. Si siguen una recta, la normalidad es razonable; desviaciones en las colas indican asimetría o extremos.
- **Shapiro-Wilk:** test formal de normalidad (H₀: los datos son normales). *Precaución:* con muestras grandes rechaza normalidad por desviaciones mínimas sin relevancia práctica, por eso combínalo con histogramas, Q-Q plots y asimetría.
- **Asimetría y curtosis** complementan los gráficos.

---

## 5. Correlación

Mide **asociación, no causalidad**.

### Pearson
Relación **lineal** entre dos variables numéricas. Úsalo cuando ambas son numéricas, la relación es aproximadamente lineal y no hay outliers extremos.
```
|r| < 0.3     asociación débil
0.3 a 0.5     asociación moderada
>= 0.5        asociación fuerte
```
*Limitaciones:* no detecta bien relaciones curvas, es sensible a outliers, no implica causalidad.

### Spearman
Asociación basada en **rangos**. Úsalo cuando hay outliers, las variables son ordinales, la relación es monótona no lineal o la distribución es asimétrica. *Limitaciones:* no implica causalidad; los empates afectan la precisión.

---

## 6. Asociación entre variables categóricas

**Tabla de contingencia** — conteos cruzados entre categorías; permite ver diferencias de proporciones.

| Variable A | Clase 0 | Clase 1 |
| --- | --- | --- |
| Grupo 1 | 80 | 20 |
| Grupo 2 | 50 | 50 |

**Chi-cuadrado** — evalúa independencia (H₀: las variables son independientes). Un p-valor bajo indica asociación. *Limitaciones:* requiere frecuencias esperadas suficientes; con muestras grandes detecta diferencias pequeñas; no mide la fuerza.

**Cramér's V** — mide la **fuerza** de la asociación (0 = ninguna, 1 = perfecta). Se reporta junto al chi-cuadrado.

---

## 7. Comparación de medias

**Prueba t de Student** — compara medias de **dos** grupos.
$$t = \frac{\bar{x}_A - \bar{x}_B}{s_p \sqrt{\frac{1}{n_A} + \frac{1}{n_B}}}, \quad s_p^2 = \frac{(n_A-1)s_A^2 + (n_B-1)s_B^2}{n_A + n_B - 2}$$
Normaliza la diferencia por el error estándar. Revisa independencia, varianzas y normalidad aproximada (o tamaño muestral suficiente). *Origen:* Student (1908).

**ANOVA** — compara medias de **dos o más** grupos (H₀: todas las medias son iguales). Si es significativa, al menos un grupo difiere, pero no dice cuál: para eso se usan pruebas post-hoc como **Tukey**.

**Eta cuadrado (η²)** — proporción de varianza de la variable numérica explicada por el grupo.
```
0.01  efecto pequeño
0.06  efecto moderado
0.14  efecto grande
```

---

## 8. Intervalos de confianza y p-valores

Un p-valor **no mide la importancia** de un efecto, solo qué tan compatible es la evidencia con la hipótesis nula. Complétalo con tamaño del efecto, intervalo de confianza, contexto y tamaño muestral.

**Intervalo de confianza** — expresa incertidumbre.
```
Diferencia media estimada: 5.2
IC 95%: [2.1, 8.3]
```
Como el intervalo no incluye cero, hay evidencia de una diferencia relevante.

**Tamaño del efecto** — responde *¿qué tan grande es la diferencia o asociación?* Clave porque significancia estadística no implica relevancia práctica.
