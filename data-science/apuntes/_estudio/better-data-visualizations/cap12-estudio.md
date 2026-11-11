# Developing a Data Visualization Style Guide — Estudio

## Tarjetas de repaso

P: ¿Qué hace una guía de estilo de visualización de datos y con qué se compara en el apunte?
R: Define las partes de un gráfico y su uso correcto y consistente; se compara con lo que el *Chicago Manual of Style* hace por la gramática inglesa.

P: ¿Por qué muchas decisiones de estilo son subjetivas?
R: Porque no existe, por ejemplo, un grosor de línea objetivamente correcto; hay principios a considerar, pero los estilos reflejan las preferencias tuyas y de tu organización.

P: ¿Qué tres propósitos cumple la guía en una organización?
R: Dar a los miembros estilos y expectativas detalladas; guiar y automatizar decisiones para quienes no conocen las reglas de marca; y fijar el tono de que la visualización es tan importante como el resto de materiales de marca.

P: ¿Cuáles son las seis secciones básicas que debería cubrir una guía?
R: Graph Anatomy, Color Palette, Font, Graph Types, Exporting Images y Accessibility, Diversity, and Inclusion.

P: ¿En cuántos elementos descompone el gráfico la plantilla del Urban Institute y cita algunos?
R: En catorce, desde Overall Dimensions, Figure Number, Title y Subtitle hasta Data Markers, Data Labels y Data Series.

P: ¿Cuáles son los cinco esquemas de color principales?
R: Binary (dos categorías nominales), Sequential (bajo a alto), Diverging (hacia fuera desde un punto medio), Categorical (diferencias nominales) y Highlighting (resaltar un valor o grupo).

P: ¿Qué es la transparency y por qué no es un esquema más?
R: Es una técnica, no un esquema: usar colores transparentes deja ver el objeto que hay detrás y hace visibles los solapamientos.

P: ¿Por tres razones es mala elección el arcoíris (avoid the rainbow)?
R: No es lógico decir que "morado" es más que "naranja"; no se corresponde con el sistema numérico (franjas de distinto ancho); y no es consistente con CVD ni al imprimir en blanco y negro.

P: ¿Qué es la deficiencia de visión del color (CVD) y a cuántas personas afecta?
R: Dificultad para distinguir colores, sobre todo rojos y verdes; afecta a unos 300 millones de personas en el mundo, en su mayoría hombres.

P: ¿Cuántas fuentes suelen bastar y cómo se varía su aspecto?
R: Rara vez hacen falta más de dos y a menudo basta una; se varía cambiando grosor (fina, negrita), ángulo (cursiva) y color.

P: ¿Cuál es el riesgo de las fuentes personalizadas?
R: Deben estar instaladas en toda máquina que muestre el gráfico, lo que da problemas al compartir archivos o presentar desde otro portátil.

P: ¿Cuál es la diferencia entre formato bitmap y vector al exportar?
R: El bitmap (raster) se almacena como píxeles y pierde nitidez al ampliar; el vector guarda la forma, es resolution-independent y se amplía sin perder calidad, a costa de archivos grandes.

P: ¿Qué es el alt text y qué debe comunicar en un gráfico?
R: Una descripción concisa; en un gráfico debe comunicar su conclusión o mensaje en una sola frase.

P: ¿Cuáles son las cuatro áreas que definen las WCAG?
R: Perceivable, Operable, Understandable y Robust.

## Preguntas de autoevaluación

P: ¿Por qué conviene probar los componentes de una guía antes de adoptarlos? (Lo que necesitas saber)
R: Porque colores que lucen en un logo pueden no funcionar en un gráfico de líneas o de barras; la guía es además un documento vivo que debe evolucionar con la estética, las publicaciones y las herramientas.

P: ¿Qué papel juega el Urban Institute en el capítulo? (El ejemplo que recorre el capítulo)
R: Su guía de estilo es el hilo conductor usado como plantilla para definir cada parte de un gráfico, apoyada en otras guías publicadas (Economist, Financial Times, London Datastore, etc.).

P: En la anatomía del gráfico, ¿qué recomendaciones da sobre las líneas de eje y los tick marks? (La anatomía de un gráfico)
R: Definir color y grosor y si los tick marks van dentro o fuera; a veces se omite la línea del eje vertical conservando la horizontal como ancla; el autor prefiere oscurecer la línea del cero, sobre todo con valores negativos.

P: ¿Qué cinco consejos encabezan la guía del Urban Institute? (Guías por tipo de gráfico)
R: Mantener alta la densidad de datos (gráficos de 685px de ancho), referenciar siempre la figura en el texto, mantener el título corto y simple, reservar la información técnica para Source and Notes, y extender las leyendas por arriba o a la derecha en orden lógico.

P: ¿Por qué el par rosa-azul es problemático y qué alternativas se sugieren? (Paletas de color — Colors and culture)
R: Arrastra un bagaje de género (rosa=debilidad, azul=fuerza), aunque antes de mediados del siglo XX era al revés; se sugiere usar morados y verdes (Telegraph) o azules y naranjas (Guardian).

P: ¿Qué formato de imagen conviene según el destino, según la tabla adaptada de Claus O. Wilke? (Exportar imágenes)
R: Vectoriales pdf y eps (uso general) y svg (online); de bitmap png (dibujos de líneas), jpeg (fotografías), tiff (impresión, mejor color) y gif (animaciones).

P: ¿Qué estándar legal y qué buenas prácticas de lenguaje menciona la sección de accesibilidad? (Accesibilidad, diversidad e inclusión)
R: La Sección 508 de la Rehabilitation Act de 1973, que obliga a las agencias federales de EE. UU. a que su ICT sea accesible; y usar el lenguaje aceptado por cada comunidad, prefiriendo el "people-first" ("personas con discapacidad").

P: Según "Juntarlo todo", ¿cuál es el objetivo al decidir detalles estilísticos como el grosor de las gridlines? (Juntarlo todo)
R: Muchas decisiones no tienen respuesta correcta; son estilísticas pero funcionales, y el objetivo es enfatizar los datos sobre gridlines, tick marks y marcadores.

## Checklist

- [ ] Cubrir las seis secciones básicas: Graph Anatomy, Color Palette, Font, Graph Types, Exporting Images y Accessibility, Diversity, and Inclusion.
- [ ] Definir cada parte del gráfico (hasta los 14 elementos del Urban Institute: dimensiones, número de figura, título, subtítulo, títulos y etiquetas de eje, líneas y tick marks, gridlines, fuentes y notas, logo, leyenda, data markers, data labels y data series).
- [ ] Elegir el esquema de color adecuado al dato (binary, sequential, diverging, categorical o highlighting) y considerar la transparency para solapamientos.
- [ ] Evitar el arcoíris y comprobar los colores para CVD con herramientas como Vischeck.com o WebAIM; definir tintes y sombras.
- [ ] Limitar las fuentes a una o dos y verificar que estén instaladas en toda máquina que muestre el gráfico antes de usar fuentes personalizadas.
- [ ] Fijar reglas por tipo de gráfico empezando por los más usados en la organización.
- [ ] Exportar con suficiente resolución eligiendo entre bitmap y vector según herramienta, sistema operativo y destino; revisar siempre el resultado final.
- [ ] Añadir alt text con la conclusión en una frase, nombrar los archivos de imagen de forma descriptiva y revisar las cuatro áreas WCAG (Perceivable, Operable, Understandable, Robust).
- [ ] Usar lenguaje "people-first" y el aceptado por cada comunidad, y decidir con cuidado el orden de barras o líneas.
- [ ] Tratar la guía como documento vivo y revisarla según cambian tecnologías y tendencias.
