# 08 · Visualización y Comunicación de Datos

Cómo convertir datos y modelos en comunicación que mueve a decidir. Mientras el documento 04 cubre la visualización **exploratoria** (entender los datos para uno mismo), este documento cubre la visualización **explicativa**: elegir el gráfico correcto, eliminar el desorden, dirigir la atención, diseñar con intención y envolver todo en una narrativa para una audiencia concreta.

> **Idea rectora:** *el éxito de una visualización empieza fuera de la visualización.* Una buena gráfica no es la más técnicamente precisa, sino la que comunica el mensaje correcto a la audiencia correcta. "Data visualization is a mix of science (percepción exacta) and art (atención y engagement)."

> Fuentes: *Storytelling with Data* (Cole Nussbaumer Knaflic) y *Better Data Visualizations* (Jonathan Schwabish).

---

## 1. Primero el contexto: a quién, qué y cómo

Antes de abrir cualquier herramienta, responde en orden:

1. **¿Quién?** — la audiencia específica (un comité, un VP, ingeniería…). Un mismo dato cuenta historias distintas según quién lo recibe. Si no puedes nombrar la audiencia, no estás listo para construir.
2. **¿Qué?** — qué necesitas que **sepa o haga**. Toda comunicación de datos debería pedir (o al menos sugerir) una **acción**. "Si solo presentas datos, es fácil que digan 'qué interesante' y sigan; si pides acción, tienen que decidir."
3. **¿Cómo?** — con qué datos y por qué **mecanismo**, que va en un continuo:
   - **Presentación en vivo** (izquierda): tú controlas, respondes señales, puedes mostrar menos detalle.
   - **Documento / email** (derecha): la audiencia controla, necesita todo el detalle explícito porque no estarás ahí.

### Exploratorio vs. explicativo
> Exploratorio = abrir 100 ostras para encontrar 2 perlas. Explicativo = mostrar solo las 2 perlas. El error típico es "hacer que la audiencia reabra todas las ostras". Al comunicar, destila.

### Herramientas para destilar antes de diseñar
- **The 3-minute story:** si tuvieras 3 minutos y sin slides, ¿qué contarías? Si no puedes contarlo claro sin tecnología, aún no entiendes tu historia.
- **The Big Idea** (Nancy Duarte): reducir el mensaje a **una sola oración** que (1) exprese tu punto de vista único, (2) transmita qué está en juego y (3) sea una oración completa.
- **Storyboarding:** bosquejar la estructura con post-its/pizarra **antes** de abrir el software, para no apegarse emocionalmente a lo ya construido. *"Don't start with presentation software."*

---

## 2. Elegir el gráfico correcto

Deja que **la relación que quieres mostrar guíe el tipo de gráfico**, no al revés. Con ~una docena de tipos bien usados se cubre casi todo. Elige por **función**, no por costumbre.

| Función | Gráficos recomendados |
| --- | --- |
| **Uno o dos números** | **Simple text** (el número en grande; meterlo en un gráfico le quita fuerza) |
| **Cambio en el tiempo (continuo)** | Línea, área, slopegraph, sparkline |
| **Comparar categorías** | Barras (vertical/horizontal), dot plot |
| **Distribución** | Histograma, boxplot, violín, ridgeline |
| **Relación / correlación** | Scatterplot, bubble |
| **Parte-todo** | Barras apiladas, treemap (pie solo con cuidado) |
| **Geográfico** | Choropleth, cartograma, símbolo proporcional |
| **Cualitativo (texto)** | Citas, coloreo de frases, iconos, word tree |
| **Valor exacto** | **Tabla** (sí, es una forma de visualización) |

### Reglas duras y sus excepciones
- **Baseline en cero: obligatorio en barras** (el ojo compara los extremos; un baseline falso exagera y destruye credibilidad — caso Fox News: un alza real del 13% parecía 460%). **No obligatorio en líneas ni scatter** si el cero no es un valor posible.
- **Doble eje (eje y secundario): evitar** — crea correlaciones falsas. Única excepción legítima: el **Pareto** (misma métrica: marginal + acumulada).
- **Pie chart: desaconsejado** (el ojo compara mal ángulos/áreas) salvo pocas categorías (3-4) con ángulos familiares (25/50/75%) y una audiencia que lo lee al instante.
- **Evitar siempre:** 3D (distorsiona), donut.
- **Ordena las categorías** de forma intencional (natural o por valor descendente) para aprovechar el recorrido en "z" de la mirada.
- **¿Debería ser un mapa?** No hagas un mapa solo porque tienes datos geográficos; a veces un scatter revela mejor la relación.

---

## 3. Reducir el desorden (clutter)

El cerebro tiene procesamiento finito: **cada elemento en pantalla cobra carga cognitiva**. El clutter son elementos que ocupan espacio **sin aumentar la comprensión**; hacen que el visual *parezca* más complicado de lo que es y la audiencia se rinde ("ugh").

- **Data-ink ratio / señal-ruido:** maximiza la proporción de tinta dedicada a los datos; quita el resto.
- **Regla práctica:** *"¿Eliminar esto cambiaría algo? ¿No? Fuera."* Lo necesario-pero-no-clave, empújalo al fondo (gris claro).

### Los 6 principios Gestalt (para quitar, no agregar)
| Principio | Idea | Uso para declutter |
| --- | --- | --- |
| **Proximidad** | Objetos cercanos = grupo | Etiquetar datos *junto* a ellos; agrupar por espaciado |
| **Similitud** | Mismo color/forma = relacionados | Color consistente entre etiqueta y serie → elimina bordes y leyendas |
| **Enclosure** | Objetos encerrados = grupo | Sombreado leve para separar (ej. zona de pronóstico) |
| **Closure** | La mente completa formas | Quitar bordes y fondos del gráfico; sigue viéndose completo |
| **Continuity** | El ojo busca el camino más suave | Quitar la línea del eje; el espacio en blanco mantiene la alineación |
| **Connection** | Objetos conectados = grupo | La línea de un line chart conecta y ordena los puntos |

**Declutter típico:** redondear decimales, quitar bordes y gridlines, eliminar marcadores innecesarios, etiquetar directo (fuera la leyenda separada), color consistente. Conserva siempre `$`, `%`, comas. Cuida alineación, espacio en blanco y contraste estratégico. *"When design is thoughtful, it fades into the background."*

---

## 4. Enfocar la atención

No vemos con los ojos sino con el cerebro. Los **atributos preatentivos** (tamaño, color, posición, orientación, longitud…) se detectan en una fracción de segundo, antes del pensamiento consciente (memoria icónica). Úsalos **con moderación y estrategia** para (1) dirigir la mirada y (2) crear jerarquía visual.

- **Codificación cuantitativa vs. categórica:** la longitud y la posición se leen como *cantidad* (por eso las barras funcionan); el color **no** significa "más" o "menos" → úsalo para distinguir categorías o resaltar, no para magnitud.
- **Los tres más potentes:**
  - **Tamaño** — el tamaño relativo denota importancia relativa.
  - **Color** — un cambio de color señala *un cambio*; úsalo con moderación y consistencia, nunca por novedad. Base en **gris** + un único color de acento.
  - **Posición** — la esquina **superior izquierda** es la más valiosa (inicio del recorrido en "z"); pon ahí el mensaje o call to action.
- **Etiquetado selectivo:** marca y etiqueta solo los puntos/series clave; etiquetar todo crea un "cluttered mess" y mata la señal.
- **Test "¿a dónde van tus ojos?":** mira el visual con ojos frescos (o pide a un colega que narre dónde mira primero). Si la vista no aterriza donde quieres, rediseña.

---

## 5. Pensar como diseñador

**Form follows function:** primero decide qué quieres que la audiencia *pueda hacer* con los datos, luego crea la forma que lo permita. El buen diseño se desvanece: no se nota porque funciona.

- **Affordances:** rasgos que hacen obvio cómo "usar" el gráfico. Tres tácticas: resaltar lo importante (máximo ~**10%** del visual), eliminar distracciones, crear jerarquía visual clara. Jerarquía de énfasis: **negrita > itálica > subrayado**.
- **Accesibilidad:** *"If it's hard to read, it's hard to do."* No sobrecompliques (lenguaje directo, define jerga, deletrea siglas), apóyate en el texto. Considera daltonismo (CVD): evita la **paleta arcoíris** (no mapea al sistema numérico, falla en CVD y en blanco y negro); usa paletas apropiadas (ver §6). Añade **alt text** que resuma la conclusión.
- **El texto es tu amigo — títulos activos:** todo gráfico necesita título y cada eje su título. El título debe decir el **"so what"** (el takeaway), no una descripción neutra. *"Estimated 2015 spending is above budget"* en vez de *"2015 Budget"*. Si no logras un título activo conciso, puede que el gráfico no tenga un mensaje claro.
- **Estética:** un diseño cuidado genera un "contrato" — la audiencia invierte tiempo porque ve que tú lo invertiste; además tolera mejor los fallos menores.
- **Aceptación:** un gran diseño rechazado no comunica. Para ganar buy-in: articula los beneficios, muestra el **antes/después** lado a lado, ofrece opciones y pide input, y gana primero a un miembro influyente. Ante resistencia, distingue si el problema es el cambio en sí o un fallo real del diseño (pide opinión a un tercero sin interés).

---

## 6. Color, tablas y estandarización

### Los 5 esquemas de color (elegir según el dato)
| Esquema | Para | Ejemplo |
| --- | --- | --- |
| **Binary** | Dos categorías nominales | urbano / rural |
| **Sequential** | Valores ordenados (claro→oscuro) | choropleth de pobreza |
| **Diverging** | Dos secuenciales desde un medio claro | desviaciones respecto a cero |
| **Categorical** | Diferencias nominales | grupos de producto |
| **Highlighting** | Resaltar un valor/grupo (caso especial de categorical) | la serie que importa en color, el resto gris |

### Diseño de tablas (sí, son visualización)
Para cuando importa el **valor exacto**. Reglas clave: separa encabezados del cuerpo, divisores sutiles (no gridlines pesadas), **números alineados a la derecha**, **texto a la izquierda**, precisión adecuada (sin exceso de decimales), elimina repetición de unidades, resalta outliers, agrupa datos similares, y añade mini-visualizaciones (sparklines, barras en celda) cuando aporten.

### Style guide (consistencia)
Un *style guide* hace por los gráficos lo que un manual de estilo por la gramática: automatiza las decisiones (muchas subjetivas pero no arbitrarias) y da consistencia, eficiencia y marca. Documento vivo; secciones típicas: anatomía del gráfico, paleta de color, fuente, tipos de gráfico, exportación, accesibilidad/inclusión.

### Formatos de exportación
- **Bitmap/raster** (PNG, JPEG): píxeles; pierde nitidez al escalar.
- **Vector** (PDF, SVG, EPS): independiente de resolución; archivos más pesados.
Elige según destino (web, impresión, slide) y **verifica siempre la nitidez del producto final**.

---

## 7. Narrativa: contar una historia con datos

*"La gente no se inspira a actuar solo con la razón."* Los bullets de hechos persuaden solo en lo intelectual; la **historia** une idea + emoción y mueve a la acción. *"Nirvana se alcanza cuando los visuales efectivos se combinan con una narrativa poderosa."*

### Estructura de tres actos (inicio – medio – fin)
- **Inicio (setup):** contexto y protagonista = **tu audiencia**.
- **Medio (tensión):** el conflicto **"what is vs. what could be"** — el contraste entre el estado actual (problema) y lo que podría ser (solución). Sin conflicto no hay historia que enganche. Enmárcalo como el problema *de la audiencia*.
- **Fin:** resolución + **call to action** claro (qué quieres que hagan). Un cierre clásico "ata con el inicio".

### Flujo narrativo
El orden depende de la audiencia: **cronológico** (seguir el análisis) para construir credibilidad con una audiencia técnica; **empezar por el "ask"** para una audiencia ocupada.

### Tácticas para que la historia quede clara
- **Bing-Bang-Bongo:** diles lo que les vas a decir → díselo → resume lo que les dijiste (la repetición cementa en memoria).
- **Lógica horizontal:** leer solo los **títulos activos** de las slides en orden debe contar toda la historia.
- **Lógica vertical:** todo en una slide se auto-refuerza (texto ↔ visual), sin info extraña.
- **Reverse storyboarding:** anota el punto principal de cada página del deck final; la lista debe parecerse a tu storyboard original.
- **Fresh perspective:** pide a un colega ojos frescos; tú ya no ves como la audiencia.
- Keep it simple, **edita sin piedad**, sé auténtico. *"The story is not for you; the story is for them."*

---

## 8. Los principios universales (checklist pre-publicación)

Destilado de todo el documento. Antes de compartir cualquier visual:

1. **Show the data** — resalta los valores que importan a tu argumento (no todos).
2. **Reduce the clutter** — quita todo lo que distrae o distorsiona.
3. **Integrate graphics and text** — etiqueta directo, elimina leyendas, usa títulos activos y anotaciones.
4. **Avoid the spaghetti chart** — usa *small multiples* (paneles con la misma escala) en vez de amontonar series.
5. **Start with gray** — empieza todo en gris y justifica deliberadamente cada color y énfasis.
6. **Consider your audience** — diseña para quién lo recibe y qué necesita.

> El conjunto de gráficos posibles es infinito; cualquiera puede comunicar datos eficazmente pensando críticamente en su audiencia y practicando el rediseño.

---

## Conexión con el resto del flujo

- **Visualización exploratoria** (histogramas, boxplots, scatter para *entender* los datos) → `04_analisis_exploratorio_datos.md` §7.
- **Visualizar el desempeño de modelos** (ROC, lift, profit, matriz de confusión) → `06_modelado_y_evaluacion.md` §6c.
- **Reporte final** orientado a decisión → `06_modelado_y_evaluacion.md` §10.
- **Dashboards sobre vistas limpias** (no tablas crudas) y herramientas de BI/mapas → `02_arquitectura_e_ingenieria_datos.md` §8.

> **Regla de oro compartida con el modelado:** cada tabla, gráfico o métrica debe responder *¿qué decisión ayuda a tomar?* Si no ayuda a decidir, no debería estar.
