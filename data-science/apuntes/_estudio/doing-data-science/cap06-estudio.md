# Time Stamps and Financial Modeling (Marcas de tiempo y modelado financiero) — Estudio

## Tarjetas de repaso

P: ¿Qué nexo une la parte de GetGlue y la parte de finanzas del capítulo?
R: El dato con timestamp: tanto los eventos de usuarios como los precios de mercado son datos ordenados en el tiempo, y ese orden es lo que permite ver causa y efecto.

P: ¿Cómo almacena GetGlue las acciones de los usuarios y cómo se visualiza?
R: En tripletes {user, action, item} (con timestamp forma {user, action, item, timestamp}), visualizados como un grafo bipartito con nodos "users" e "items" y aristas que solo van de un usuario a un item.

P: ¿Qué tipos de aristas adicionales enriquecen el grafo de GetGlue?
R: Aristas dirigidas de amistad/seguimiento entre usuarios, conexiones de gustos similares (normalmente no dirigidas) y conexiones de similitud entre programas creadas por evaluadores humanos (a veces dirigidas).

P: ¿Cuál es la regla del modelado causal en finanzas?
R: Nunca usar información del futuro para predecir el presente; solo datos del pasado hasta el momento actual, distinguiendo timestamps de disponibilidad y de referencia.

P: ¿Qué diferencia hay entre datos out-of-sample y datos de prueba (testing)?
R: El testing ocurre dentro del in-sample; el out-of-sample son datos que se usan tras finalizar el modelo para estimar su rendimiento en producción, y conviene limitar cuántas veces se usan.

P: ¿Por qué no se debe normalizar con la media calculada sobre todo el training set?
R: Porque es acausal: usar una estimación global equivale a anticipar eventos (como un crash) antes de que ocurran, y esa interferencia puede hacer que un modelo malo o puro ruido parezca bueno.

P: ¿Qué es un log return y cómo se calcula?
R: El retorno logarítmico de cierre a cierre: si Ft es el cierre del día t, es log(Ft/Ft−1).

P: ¿Por qué se prefieren log returns frente a retornos porcentuales?
R: Son aditivos (el log return de cinco días es la suma de los diarios) y simétricos ante ganancias y pérdidas, mientras que el porcentual está sesgado hacia las ganancias.

P: ¿Qué es el lookback window y qué compromiso implica?
R: La ventana de pasado de donde se toma información para estimar volatilidad: cuanto más larga, más información; cuanto más corta, más rápido responde a lo nuevo.

P: ¿Cuál es la fórmula de actualización de la varianza con exponential downweighting?
R: Vnew = s·Vold + (1−s)·r0², donde s es el decay; comprime los datos en un único valor actualizable sin guardar todo el histórico.

P: ¿Qué significa que el mercado "aprende con el tiempo"?
R: Que si encuentras una forma de ganar dinero acaba desapareciendo, porque tu propia compra cambia el proceso (market impact) y reduce la señal; las señales existentes quedan muy débiles.

P: ¿Cómo se evalúa un modelo financiero en lugar de usar accuracy?
R: Dibujando el PnL (Profit and Loss) acumulado día a día (diferencia, no ratio): la suma acumulada del producto de forecast demeaned por realized demeaned, comparando contra el modelo "más tonto" (asumir que todo es la media).

P: ¿Por qué se prefiere la regresión lineal y no la logística en finanzas?
R: Porque la señal es muy débil y conviene quedarse solo con términos lineales; la logística obliga a un interruptor on/off e ignora el tamaño, que sí importa (no es igual subir 2% que 0.01%).

P: ¿Qué es un prior y para qué sirve en este modelado?
R: Una opinión formulada matemáticamente e incorporada al modelo (p. ej. "el dato nuevo importa más" o "los coeficientes varían suavemente"); reduce grados de libertad sumando una matriz a la de covarianza en la regresión.

## Preguntas de autoevaluación

P: ¿Por qué es típico (y causa) del Big Data el dato de eventos con timestamp?
R: Porque un solo usuario puede generar miles de puntos de datos al día: cada acción en web o app se registra con hora exacta y naturaleza, y ese registro es parte del producto. (Sección "Timestamps y análisis exploratorio")

P: ¿Qué decisiones afectan la interpretación al agregar datos de eventos en el tiempo?
R: Contar usuarios únicos o logins totales; acciones o usuarios con al menos una acción; qué horizonte temporal usar (segundo, minuto, hora, día, semana); y cómo tratar la estacionalidad y las zonas horarias. (Sección "Timestamps y análisis exploratorio")

P: En el experimento mental de Cathy, ¿qué se pierde al ignorar los timestamps?
R: No se puede separar causa y efecto; y si solo se guardan diferenciales relativos sin timestamps absolutos, se ignoran tendencias y estacionalidad, vitales dado lo pequeñas que son las señales financieras. (Sección "Cathy O'Neil: experimento mental y causalidad")

P: ¿Por qué los coeficientes de una regresión se consideran "organismos vivos"?
R: Porque no se conocen los "mejores coeficientes" hasta el último timestamp; al avanzar en el tiempo cada coeficiente evoluciona, y su estabilidad informa la estimación (si cambia de signo diez veces, quizá lo mejor sea cero). (Sección "In-sample, out-of-sample y modelado causal")

P: ¿Qué problema tiene la ventana estrictamente rodante (rolling window) y cómo se resuelve?
R: Un retorno grande cuenta pleno hasta que de repente desaparece al salir de la ventana, lo que no encaja con cómo olvidamos; se resuelve con una ventana continua que downweightea exponencialmente los datos antiguos, con un half-life. (Sección "Medir la volatilidad")

P: ¿Por qué se guarda la varianza corriente y no la desviación típica en el exponential downweighting?
R: Porque las estimaciones deben ser aditivas para poder mantener un total corriente actualizable; la varianza lo es y la desviación típica no. (Sección "Exponential downweighting")

P: ¿Cómo se implementa el prior de suavidad en la regresión?
R: Añadiendo un término a la función de penalización con el operador de desplazamiento M (I−M como derivada discreta): β2 = (xᵀx + N·λ²I + N·μ²·(I−M)ᵀ(I−M))⁻¹xᵀy, ajustando λ al cambiar μ. (Sección "Por qué regresión y priors")

P: ¿Qué hace nuevo al análisis de datos con timestamp hoy, si no es nuevo el dato en sí?
R: La escala: es fácil medir el comportamiento humano todo el día con dispositivos, los timestamps son precisos (no dependen del autorreporte) y la capacidad de cómputo permite almacenar y procesar mucho rápido. (Sección "Métricas, pasos siguientes y perspectiva histórica")

## Checklist

- Al hacer EDA, empezar por gráficas de usuarios individuales en el tiempo con una muestra pequeña antes de agregar.
- Codificar con color los distintos tipos de acción y revisar anomalías (si todos hacen lo mismo a la vez, distinguir evento real de bug).
- Al agregar, decidir y justificar: unicidad de usuarios vs logins, horizonte temporal, estacionalidad y desplazamiento a hora local por zonas horarias.
- Convertir timestamps a segundos desde epoch cuando los cambios de hora compliquen el modelado.
- Separar in-sample antes de out-of-sample en orden temporal y limitar el número de análisis out-of-sample.
- Distinguir timestamps de disponibilidad y de referencia al usar datos públicos retrasados.
- Normalizar/preparar con estimaciones corrientes conocidas en cada momento, nunca con la media o varianza global.
- Construir la serie de log returns diarios (de cierre a cierre) en lugar de retornos porcentuales.
- Estimar la volatilidad con exponential downweighting usando Vnew = s·Vold + (1−s)·r0² y elegir el decay/half-life con intuición del mercado.
- Evaluar con el PnL acumulado (forecast demeaned × realized demeaned) y comprobar que deriva al alza frente al modelo "más tonto".
- Ejercicio GetGlue: cargar 1.000 filas con R (fromJSON, ldply), mirarlas, agregar y contar (acciones únicas y por tipo, usuarios únicos, 10 películas más populares, eventos en 2011) y proponer y responder cinco preguntas propias con una visualización.
- Ejercicio financiero: descargar de Yahoo! Finance 8+ años diarios de una acción (de antiguo a reciente), crear log returns, montar una regresión lineal con los dos últimos retornos para predecir el siguiente, hacerla causal, normalizar por volatilidad o meter decay, y dibujar el PnL acumulado.
