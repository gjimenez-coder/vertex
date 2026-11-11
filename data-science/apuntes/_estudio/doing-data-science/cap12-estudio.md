# Epidemiology (Epidemiología) — Estudio

## Tarjetas de repaso

P: ¿Quién expone el capítulo 12 y cuál es su especialidad? / R: David Madigan, catedrático y director de estadística en Columbia, con trabajo en estadística bayesiana, text mining, métodos de Monte Carlo, farmacovigilancia y modelos gráficos probabilísticos.

P: ¿Cuál es la tesis central del capítulo? / R: Que los métodos habituales de la epidemiología (estratificación y ajustes por confusores) no son fiables, porque según cómo se elijan base de datos, confusores o ventana temporal, un mismo par fármaco-efecto puede salir significativo en direcciones opuestas: "puedes obtener lo que quieras".

P: ¿Qué es la estratificación en epidemiología? / R: Partir los casos en subcasos y mirarlos por separado (por ejemplo, ajustar por género mediante una media ponderada) para intentar controlar posibles confusores.

P: ¿Por qué la estratificación no resuelve el problema del confusor? / R: Porque puede empeorar las estimaciones del efecto causal, sobre todo con números pequeños o poblaciones que no son realmente comparables.

P: ¿Qué muestra el ejemplo de la Tabla 12-1 y su división por género? / R: Un efecto causal agregado de 0,1 (0,3 − 0,2) que, al dividir por género con cifras pequeñas, pasa a 0,05 en hombres y 0,1125 en mujeres, permitiendo un titular engañoso de efectos "dos veces más fuertes" en mujeres.

P: ¿Qué es el proyecto OMOP? / R: Observational Medical Outcomes Partnership, colaboración público-privada (Foundation for the NIH, PhRMA y FDA) para identificar los métodos más fiables de analizar grandes volúmenes de datos de fuentes heterogéneas.

P: ¿Qué escala tuvo el experimento de OMOP? / R: 10 grandes bases de datos con registros de 200 millones de personas, 14 diseños epidemiológicos y unas 5.000 configuraciones, sobre 10 clases de fármacos y 10 resultados.

P: ¿Cómo se diseñó la evaluación de "casos conocidos" en OMOP? / R: Con 9 efectos nocivos conocidos (p. ej., la warfarina causa sangrado) y 44 casos "negativos" conocidos sin daño, para ver si los métodos discriminaban entre ellos, como un filtro de spam.

P: ¿Qué es la "curva ROC de 25 millones de dólares"? / R: Una curva de sensibilidad frente a tasa de falsos positivos construida variando el umbral de riesgo relativo; costó unos 25 millones de dólares producir los análisis que la sustentan.

P: ¿Qué AUC se obtuvo con un único método para todo y qué significa? / R: AUC de 0,64, apenas mejor que adivinar al azar (0,5), siendo el mejor de los 5.000 análisis si se aplica un solo método.

P: ¿Qué AUC se logró al especializar el análisis? / R: 0,92 en la base de datos de Medicare para lesión renal aguda (80% de sensibilidad con 10% de falsos positivos), mediante validación cruzada.

P: ¿Qué es el método "OS" mencionado en el capítulo? / R: Un método ganador que compara dentro del historial de un mismo paciente (periodos con y sin fármaco), hoy poco usado.

P: Según Madigan, ¿qué crítica hace al machine learning actual? / R: Que recuerda a la estadística de hace 20 años (inventar un método y probarlo en datasets), con poca implicación con el dominio.

P: ¿Qué riesgos éticos señala Madigan en el dataset de 80 millones de personas? / R: Que los modelos podrían usarse para cobrar primas abusivas a los enfermos o excluirlos del seguro, en lugar de ayudar a la gente a estar sana.

## Preguntas de autoevaluación

P: ¿Por qué afirma Madigan que con los estudios observacionales "puedes obtener lo que quieras"? / R: Porque en 20 de los 50 pares fármaco-resultado podía pasarse de significativo en una dirección a la contraria según la base de datos elegida, y lo mismo ocurría al variar confusores y ventana temporal. (Sección "¿Hay una forma mejor?")

P: ¿Qué problema ilustra el ejemplo de los bifosfonatos orales respecto a la fidelidad de los estudios? / R: Que un estudio concluyó que causan cáncer de esófago y dos semanas después JAMA publicó lo contrario usando la misma base de datos; además estudios posteriores contradijeron el hallazgo original. (Secciones "Literatura médica y estudios observacionales" y "¿Hay una forma mejor?")

P: ¿Qué cuestiona Madigan sobre la elección de confusores en la práctica? / R: Que no está claro por qué se eligen unos confusores y no otros (aspirina, antecedentes de coágulos, tabaco, alcohol, IMC), y que equipos distintos tomaron decisiones radicalmente distintas en estudios paralelos. (Sección "Qué hace la gente con los confusores en la práctica")

P: ¿Qué potencial y qué tensión plantea el experimento mental de partida? / R: El potencial de aprovechar datos longitudinales de decenas de millones de pacientes para mejorar la atención (p. ej., evitar hospitalizaciones), frente a la tensión ética de que esos modelos sirvan para primas abusivas o exclusión del seguro. (Sección "El experimento mental de partida")

P: ¿Por qué no se había hecho antes una evaluación empírica como OMOP? / R: Por conflicto de interés (no interesa demostrar que los propios métodos no funcionan) y por el coste: 25 millones de dólares. (Sección "Por qué no se había hecho antes")

P: ¿Qué significan los valores de AUC 0,5, 1 y menos de 0,5? / R: 1 es el modelo ideal, 0,5 equivale a adivinar al azar y menos de 0,5 es un modelo "perverso". (Sección "La curva ROC de 25 millones de dólares")

P: ¿Qué diferencia hay entre aplicar un método único y especializar por base de datos y resultado? / R: El método único alcanza AUC 0,64 (apenas mejor que el azar), mientras que especializar por base de datos y resultado llega hasta AUC 0,92. (Sección "La curva ROC de 25 millones de dólares")

## Puntos a dominar

- Entender por qué la estratificación no garantiza mejores estimaciones del efecto causal y cómo las cifras pequeñas distorsionan el resultado (ejemplo del 10% agregado dividido por género).
- Explicar el argumento "puedes obtener lo que quieras" en función de las tres decisiones clave: base de datos, confusores y ventana temporal.
- Describir el diseño del experimento OMOP: 10 bases, 200 millones de personas, 14 diseños, ~5.000 configuraciones, 9 casos nocivos y 44 negativos conocidos.
- Interpretar la curva ROC y el AUC, distinguiendo el 0,64 del método único frente al 0,92 especializado.
- Reconocer las implicaciones éticas del uso de datos médicos masivos señaladas por Madigan.
- Situar la crítica de Madigan al machine learning actual frente a la estadística aplicada moderna.
