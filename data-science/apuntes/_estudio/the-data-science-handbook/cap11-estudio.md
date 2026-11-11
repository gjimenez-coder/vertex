# Regression (Regresión) — Estudio

## Tarjetas de repaso

P: ¿En qué se diferencia la regresión de la clasificación?
R: La regresión produce una salida que es un número real en lugar de una categoría.

P: ¿Por qué el autor dice que ajustar curvas (curve fitting) y la regresión de machine learning son matemáticamente lo mismo?
R: En ambos se asume una forma funcional de la salida en función de las entradas y se eligen los parámetros para ajustar lo mejor posible los datos de entrenamiento; la diferencia es un accidente histórico.

P: ¿Qué minimiza el método de least squares (mínimos cuadrados)?
R: La suma del cuadrado del error en cada punto: L = Σ (y_i − (m·x_i + b))².

P: ¿Por qué least squares es muy sensible a outliers?
R: Al elevar el error al cuadrado, una sola desviación grande (p. ej. de 10, penalización 100) pesa más que varias pequeñas (tres de 5, penalización 75), y el modelo dobla sus parámetros para evitarla.

P: ¿Qué es la penalización L1 y qué ventaja/inconveniente tiene frente a least squares?
R: Suma los valores absolutos de los errores (L = Σ |y_i − (m·x_i + b)|); es más robusta a outliers, pero castiga más las desviaciones pequeñas y es más complicada de implementar computacionalmente.

P: ¿Qué función de SciPy se usa para ajustes no lineales y qué recibe/devuelve?
R: `curve_fit`; recibe una función definida por el usuario (toma x y parámetros) junto con los x e y de los datos, y devuelve una tupla con los mejores parámetros y una matriz de su varianza.

P: ¿Qué recomienda el autor ante ajustes no lineales lentos o que fallan?
R: Transformar el problema en uno lineal (por ejemplo ajustando el logaritmo de los datos) o, si no se puede, aportar una conjetura inicial con el parámetro `p0`.

P: ¿Cómo se define R² y qué representa?
R: R² = 1 − (RV/TV), donde TV = Σ (y_i − ȳ)² y RV = Σ (y_i − f(x_i))²; es la fracción de la varianza total explicada por el modelo.

P: ¿Qué significan R² = 1, R² = 0 y un R² negativo?
R: 1 es ajuste perfecto; 0 equivale a predecir siempre la media `f(x) = ȳ`; valores negativos indican un ajuste peor que predecir la media.

P: ¿Qué limitación tiene usar la correlación entre predicho y real como medida de bondad?
R: Mide si predicciones y objetivos están relacionados, pero no si realmente coinciden.

P: ¿Qué detecta la correlación de residuos y cómo se calcula?
R: Detecta si la forma funcional supuesta era correcta; se ordenan los puntos por x y se calcula la correlación entre residuos consecutivos: cercana a 0 indica buena forma (el error viene del ruido, no de una forma equivocada).

P: ¿Cómo se evalúa visualmente la regresión lineal cuando ya no se puede dibujar la curva sobre los datos?
R: Con un scatterplot entre los valores reales del test y los predichos, que muestra si el modelo rinde mejor para valores grandes o pequeños y si sufre outliers.

P: ¿Por qué el tamaño de los coeficientes revela qué variables importan en la regresión lineal del ejemplo?
R: Porque las características se normalizaron a media 0 y desviación 1 con `normalize()`, así que el tamaño relativo de los pesos indica su relación con la salida.

P: ¿En qué consiste LASSO y qué papel juega su parámetro `alpha`?
R: Ajusta un modelo lineal penalizando los pesos distintos de cero; `alpha` indica cuán severamente se castigan (alpha = 0 lo reduce a regresión lineal; el script usa 1.0 por defecto).

P: ¿Por qué LASSO sirve como selección de variables?
R: Porque lleva muchos coeficientes exactamente a 0 (cuatro en el ejemplo), dejando claras las características relevantes y combatiendo el sobreajuste de la regresión lineal.

## Preguntas de autoevaluación

P: ¿Cuál es el dataset hilo conductor del capítulo y qué objetivo se predice?
R: Mediciones fisiológicas de 442 pacientes de diabetes, cuyo objetivo es un indicador de la progresión de la enfermedad. (Sección "El ejemplo que recorre el capítulo" / "Ejemplo: predicción de la progresión de la diabetes")

P: Compara los resultados de regresión lineal y LASSO en el ejemplo. ¿Qué indican?
R: Regresión lineal: Corr = 0.660, Rsq = 0.396; LASSO: Corr = 0.677, Rsq = 0.445. Los mejores valores de LASSO confirman que el modelo lineal estaba sobreajustando. (Sección "Ejemplo: predicción de la progresión de la diabetes" / "Regresión LASSO y selección de variables")

P: ¿Para qué recuerda el autor el quartet de Anscombe?
R: Son cuatro datasets con la misma recta de mejor ajuste y misma calidad según los métodos estándar; subraya que el ojo humano detecta outliers y patologías que los números esconden, aunque se necesita un método objetivo para el computador. (Sección "Mínimos cuadrados")

P: ¿Qué dos preguntas hay que responder al evaluar una curva ajustada y con qué se abordan?
R: Con qué precisión predecimos valores (se mide con R² y con la correlación predicho-real) y si la suposición sobre la forma funcional fue buena (se evalúa con la correlación de residuos). (Secciones "Bondad del ajuste: R² y correlación" y "Correlación de residuos")

P: ¿Qué problema de la regresión lineal motiva el uso de LASSO?
R: Casi todos los coeficientes son grandes y pueden compensarse entre sí, mejorando un poco el ajuste de entrenamiento pero generalizando muy mal (sobreajuste) y dificultando saber qué variables importan. (Sección "Regresión LASSO y selección de variables")

P: En el ejemplo de la diabetes, ¿qué características destacan según cada modelo?
R: Con regresión lineal (`linear.coef_`) destacan la tercera y la cuarta; con LASSO (`lasso.coef_`) cuatro características quedan en peso 0 y la más relevante es la tercera, seguida de la cuarta y la novena. (Secciones "Regresión lineal" y "Regresión LASSO y selección de variables")

P: ¿Qué observaciones hace el autor sobre el scatterplot predicho-real de la regresión lineal?
R: La correlación es clara pero tenue; hay puntos cuyo valor real está muy por debajo de lo predicho (diabetes menos dañina de lo esperado) y la recta de ajuste parece más plana que los datos por puntos anómalamente bajos que tiran las predicciones hacia abajo. (Sección "Regresión lineal")

## Puntos a dominar

- Entender que la regresión predice un valor real y que curve fitting y regresión de ML comparten el mismo fundamento matemático.
- Saber qué minimiza least squares y por qué es sensible a outliers, y cuándo preferir la penalización L1.
- Reconocer las formas funcionales no lineales habituales (decaimiento/crecimiento exponencial, logístico, polinomios) y el uso de `curve_fit` con `p0`.
- Calcular e interpretar R² = 1 − (RV/TV), incluidos los casos R² = 0 y negativo.
- Distinguir bondad predictiva (R², correlación predicho-real) de validez de la forma funcional (correlación de residuos ordenados por x).
- Interpretar los coeficientes de un modelo lineal con características normalizadas para identificar variables importantes.
- Explicar cómo LASSO (parámetro `alpha`) combate el sobreajuste y realiza selección de variables llevando coeficientes a 0.
