# Mitigating Business Logic Vulnerabilities (Mitigación de vulnerabilidades de lógica de negocio) — Estudio

## Tarjetas de repaso

P: ¿Por qué las business logic vulnerabilities son difíciles de detectar con automatización o penetration testing? / R: Porque requieren conocimiento profundo de la lógica de negocio de la aplicación, lo que también las hace difíciles de atacar.

P: ¿Cuál es la tesis optimista del capítulo sobre estas vulnerabilidades? / R: Como atacarlas exige profundo conocimiento de ingeniería, defenderse es más fácil que atacarlas, sobre todo si seguridad e ingeniería colaboran estrechamente.

P: ¿Cuáles son los tres enfoques de mitigación que presenta el capítulo? / R: Mitigaciones a nivel de arquitectura (worst-case design), modelado estadístico, y el análisis de los resultados de ese modelado para localizar errores.

P: ¿Cuál es la idea rectora que atraviesa todo el capítulo? / R: Empezar a pensar cómo la funcionalidad programada puede usarse de formas no intencionadas o inesperadas.

P: ¿Qué es el worst-case scenario design y por qué es la mitigación más importante? / R: Diseñar considerando desde el inicio el uso malicioso de cada componente; ocurre en la fase de arquitectura, antes de escribir código, y evita la mayoría de las business logic vulnerabilities.

P: ¿Qué muestra el ejemplo de los algoritmos A1 y A2? / R: Que evaluar por la mediana engaña: A1 (mediana 5) parece mejor que A2 (constante 6), pero por sus edge cases A1 tiende a un promedio de 7, volviéndose menos eficiente; elegir A1 es best-case design.

P: ¿Qué es el modelado estadístico (statistical modeling)? / R: Combinar fuzzing (probar con entradas aleatorias) con data science y automatización de navegador para podar, seleccionar e iterar mucho más rápido que con fuzzing aleatorio solo.

P: ¿Qué dos componentes debe incluir el modelo de uso de la aplicación? / R: Las entradas (inputs) y los flujos de página direccionales (acciones).

P: ¿Cómo se modelan las entradas según su tipo? / R: Dropdown ordenando los ítems por frecuencia de elección, texto libre ordenando las entradas más comunes, y radio button considerando cuál se selecciona más a menudo.

P: ¿Por qué importan los edge cases al modelar entradas? / R: Porque tienen más probabilidad de evidenciar vulnerabilidades de lógica donde el código no contempló adecuadamente un valor poco común, con caracteres o longitudes inusuales.

P: ¿Qué son los headless browsers y para qué se usan aquí? / R: Navegadores que implementan el DOM, ejecutan JavaScript y hacen peticiones de red, pero se controlan programáticamente; se usan para automatizar la traversía de la app en un entorno de pruebas local seguro.

P: ¿Qué herramientas se mencionan para el control de navegador? / R: Google's Headless Chrome (con API similar a Phantom.js y Slimer.js) controlado mediante la librería wrapper Puppeteer.

P: ¿Qué debe registrarse en el análisis del modelo? / R: Cada petición de red en términos de payload, respuesta y código de estado HTTP, para hallar fácilmente errores inesperados del servidor.

P: ¿Qué valor tiene un error encontrado que no puede explotarse? / R: Revela bugs no relacionados con seguridad cuya resolución mejora la experiencia de usuario.

P: ¿En qué formatos se almacenan entradas y acciones modeladas? / R: JSON, YAML, CSV o XML, para facilitar el procesamiento programático y la automatización.

## Preguntas de autoevaluación

P: ¿Por qué es la fase de arquitectura el mejor momento para mitigar estas vulnerabilidades? / R: Porque considerar el uso malicioso de cada componente antes de escribir código evita la mayoría de las vulnerabilidades; después de la arquitectura son mucho más caras y lentas de resolver, según la máxima de que 1 minuto arreglando bugs de arquitectura ahorra 10 de bugs de implementación. (sección "Mitigaciones a nivel de arquitectura")

P: Según el ejemplo de la Tabla 36-1, ¿cuál es el promedio de A1 sobre 10 corridas y por qué A2 termina siendo mejor? / R: El promedio de A1 es (9 × 5 + 25)/10 = 7; A2 corre siempre a velocidad constante de 6, así que al analizar edge cases A1 se vuelve menos eficiente que A2. (sección "Mitigaciones a nivel de arquitectura")

P: ¿Qué aporta el modelado estadístico frente al fuzzing aleatorio por sí solo? / R: Al sumar data science y automatización de navegador al fuzzing, permite podar, seleccionar e iterar mucho más rápido. (sección "Modelado estadístico")

P: ¿En qué se diferencian las acciones en aplicaciones legacy y en aplicaciones modernas? / R: En legacy son típicamente flujos de página direccionales; en modernas incluyen además clics que generan peticiones AJAX, modales, llamadas websocket o RTC e invocaciones directas de funciones JavaScript. (sección "Modelado de acciones")

P: ¿Por qué es sencillo poblar la base de datos con usuarios modelo pero complejo el desarrollo del modelo? / R: Porque técnicamente un usuario es solo un conjunto de bits en una base de datos, pero lo complejo es simular la traversía de la app y el uso de acciones. (sección "Desarrollo del modelo")

P: ¿Por qué las acciones de un usuario suelen ser datos fáciles de obtener? / R: Porque las rutas de acción se obtienen con herramientas de analytics que muchas empresas ya usan, así que es probable que el dato ya exista. (sección "Modelado de acciones")

P: ¿Por qué estas vulnerabilidades difieren tanto entre aplicaciones? / R: Porque dependen de la lógica de negocio específica; aunque haya similitudes entre apps de una misma industria, las formas de atacarlas suelen diferir, lo que las hace difíciles de atacar, detectar, mitigar y remediar. (sección "Resumen")

P: ¿Por qué no deben descuidarse aunque parezcan bugs de programación y no fallos de seguridad? / R: Porque la lógica de negocio suele ser el activo digital más crítico del negocio. (sección "Resumen")

## Checklist

- [ ] En la fase de arquitectura, aplicar worst-case design y descartar el best-case design para cada componente funcional.
- [ ] Para cada componente, pensar cómo la funcionalidad puede usarse de formas no intencionadas o inesperadas.
- [ ] Integrar analytics o formular una hipótesis sobre cómo los usuarios usan la aplicación.
- [ ] Modelar las entradas por frecuencia según su tipo (dropdown, texto libre, radio button) e incluir edge cases poco comunes.
- [ ] Modelar las acciones (flujos de página, clics, AJAX, modales, websocket/RTC, llamadas JavaScript).
- [ ] Almacenar entradas y acciones en un formato procesable programáticamente (JSON, YAML, CSV o XML).
- [ ] Automatizar los flujos de usuario con un headless browser (Google's Headless Chrome vía Puppeteer) en un entorno de pruebas local seguro.
- [ ] Registrar de cada petición el payload, la respuesta y el código de estado HTTP.
- [ ] Tras una muestra significativa, revisar los errores o fallos inesperados del servidor como posibles business logic vulnerabilities.
- [ ] Derivar a ingeniería la remediación de los errores hallados, incluidos los no explotables que mejoran la experiencia de usuario.
