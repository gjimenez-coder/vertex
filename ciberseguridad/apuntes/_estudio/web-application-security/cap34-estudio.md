# Defense Against Client-Side Attacks — Estudio

## Tarjetas de repaso

P: ¿Qué son los ataques del lado del cliente y por qué importa configurar la app contra ellos?
R: Explotan al usuario a través de su navegador cliente sin pasar por un servidor; como detectarlos tiene limitaciones, lo imperativo es configurar la aplicación para dificultar su ejecución exitosa.

P: ¿Qué tres ataques del lado del cliente cubre este capítulo como complemento defensivo del Capítulo 16?
R: Prototype pollution, clickjacking y tabnabbing.

P: ¿En qué característica de JavaScript se apoya prototype pollution?
R: En el sistema de herencia prototipal: el intérprete recorre la cadena de prototipos buscando funciones y datos, lo que permite contaminar un objeto relacionado en la jerarquía sin acceso directo.

P: ¿En qué consiste la sanitización de claves (key sanitization) y qué clave es la crítica?
R: En sanitizar todas las claves provistas por el usuario antes de fusionar o manipular objetos, típicamente con una allowlist; la clave `__proto__` es la que explota la cadena de prototipos al fusionarse.

P: ¿Qué hace `Object.freeze()` y cuál es su principal limitación?
R: Convierte un objeto en inmutable (no admite actualizar claves, valores ni propiedades); limita tanto el uso malicioso como el legítimo y debe usarse con moderación porque un freeze masivo rompe APIs del DOM y de JavaScript.

P: ¿Cómo se crea un objeto con prototipo nulo y por qué protege?
R: Con `Object.create(null)`, invocando el constructor con `null`; al no tener padre, el objeto no puede recorrer la cadena ni ser contaminado vía objetos padre.

P: ¿Cuál es la defensa principal contra clickjacking y qué soporte tiene?
R: La directiva CSP `frame-ancestors` (por ejemplo `'none'`), soportada por más del 95% de los navegadores modernos, que impide cargar la página dentro de un iframe.

P: ¿Por qué `X-Frame-Options` no se considera defensa efectiva contra clickjacking?
R: Porque las cabeceras legacy como `X-Frame-Options` están obsoletas para la mayoría de navegadores y no deben considerarse una línea de defensa efectiva.

P: ¿Qué es un script framebuster (framekiller) y cuándo se usa?
R: Una función JavaScript que detecta si el sitio está siendo enmarcado donde no se permite y detiene o descarga el código; se usa para los pocos navegadores sin soporte de `frame-ancestors` o enmarcados especiales.

P: ¿Cómo evita el framebuster del capítulo el secuestro de clics?
R: El contenido arranca con `display: none`; el script compara `self` y `top`, y solo si es la ventana superior cambia a `display: block`, dejando el contenido visible e interactivo únicamente cuando no está enmarcado.

P: ¿Cuál es el valor recomendado por defecto de Cross-Origin-Opener-Policy (COOP) y qué logra?
R: `Cross-Origin-Opener-Policy: same-origin`, que impide que los enlaces abiertos puedan referenciar el sitio del que se originaron; es la solución de primera línea para la mayoría de casos de tabnabbing.

P: ¿Qué hacen los atributos `noopener` y `noreferrer` en los enlaces?
R: `noopener` cambia la referencia `window.opener` del sitio destino a `null`; `noreferrer` impide que el destino acceda a la información de referrer. Juntos mejoran seguridad y privacidad y hacen imposible el tabnabbing vía enlaces dinámicos.

P: ¿Qué son las políticas de aislamiento basadas en fetch metadata y qué estatus tienen hoy?
R: Políticas flexibles que mitigan varios ataques del lado del cliente usando cabeceras `Sec-Fetch-*`; solo están en builds recientes de Firefox y Chrome, por lo que hoy deben considerarse defense in depth.

P: ¿Qué indican las cabeceras `Sec-Fetch-Site`, `Sec-Fetch-Mode`, `Sec-Fetch-Dest` y `Sec-Fetch-User`?
R: `Sec-Fetch-Site`: desde dónde se solicita el sitio; `Sec-Fetch-Mode`: el modo de la petición; `Sec-Fetch-Dest`: dónde se cargará el contenido; `Sec-Fetch-User`: `1` si el usuario inició la petición, `null` si fue un script o plug-in.

## Preguntas de autoevaluación

P: ¿Cuál es la tesis central del capítulo sobre cómo enfrentar los ataques del lado del cliente?
R: Que, dado que la detección tiene limitaciones, lo imperativo es configurar la aplicación para que estos ataques sean difíciles de ejecutar con éxito; la mayoría se frena en parte en el propio navegador con cambios simples de configuración. (Lo que necesitas saber)

P: Enumera las tres mitigaciones de prototype pollution y una característica de cada una.
R: Key sanitization (allowlist de claves, una de las mejores primeras líneas pero no siempre aceptable por entradas flexibles), `Object.freeze()` (inmoviliza el objeto, usar con moderación) y null prototypes con `Object.create(null)` (corta la cadena de prototipos). (Defensa contra prototype pollution)

P: ¿Por qué hay que usar `Object.freeze()` con moderación en APIs integradas?
R: Porque docenas de APIs dependen de la mutabilidad de otros objetos; un freeze masivo o accidental sobre APIs de JavaScript o del DOM rompe amplias porciones de funcionalidad, además de complicar el desarrollo legítimo. (Prototype Freezing)

P: Compara `frame-ancestors` con los scripts framebuster como defensas contra clickjacking.
R: `frame-ancestors` es la defensa CSP más fácil y efectiva, con soporte >95%, y detiene casi todos los intentos; los framebusters son la alternativa JavaScript para navegadores sin ese soporte, pero los framebusters legacy dejan una ventana vulnerable al cargar la página antes de ejecutarse. (Defensa contra clickjacking)

P: ¿Cómo se relaja `frame-ancestors` cuando la aplicación sí necesita ser enmarcada?
R: Con una allowlist de orígenes (por ejemplo `frame-ancestors subdomain.my-website.com`) o con la opción `self` para el caso raro de que la app necesite contener una copia de sí misma en un iframe. (Frame Ancestors)

P: ¿Cuándo deja de ser suficiente COOP `same-origin` y qué se recomienda en ese caso?
R: En sitios grandes con múltiples dominios; ahí conviene un COOP más relajado combinado con otras técnicas. (Cross-Origin-Opener Policy (COOP))

P: ¿Por qué las políticas de aislamiento con fetch metadata se consideran defense in depth y no una defensa única?
R: Porque solo están disponibles en builds recientes de Firefox y Chrome, no en Safari de escritorio ni iOS ni en la mayoría de navegadores internacionales, por lo que deben implementarse junto a otras mitigaciones. (Isolation Policies)

P: En el ejemplo de servidor con fetch metadata, ¿qué cabecera y valor se usan para bloquear el enmarcado?
R: Se inspecciona `Sec-Fetch-Dest`; si su valor es `frame`, el servidor responde con estado 400, bloqueando así la mayoría del clickjacking. (Isolation Policies)

## Puntos a dominar

- Explicar por qué, al tener la detección limitaciones, la estrategia es configurar la app para dificultar los ataques del lado del cliente.
- Distinguir las tres mitigaciones de prototype pollution (key sanitization, `Object.freeze()`, null prototypes) y sus limitaciones.
- Reconocer el rol de la clave `__proto__` y cómo una allowlist de claves la neutraliza.
- Justificar el uso moderado de `Object.freeze()` por su impacto sobre APIs del DOM y de JavaScript.
- Identificar `frame-ancestors` como defensa principal contra clickjacking y `X-Frame-Options` como obsoleta.
- Describir cómo un framebuster usa `display:none` y la comparación `self`/`top`, y por qué los framebusters legacy son débiles.
- Recordar `Cross-Origin-Opener-Policy: same-origin` y los atributos `noopener` y `noreferrer` como defensas de tabnabbing.
- Situar las políticas de aislamiento con cabeceras `Sec-Fetch-*` como defense in depth por su soporte limitado.
