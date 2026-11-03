# Cross-Site Scripting (Scripting entre sitios) — Estudio

## Tarjetas de repaso

P: ¿Qué explota en esencia un ataque XSS?
R: Que las aplicaciones web ejecutan scripts en los navegadores de los usuarios; cualquier script creado dinámicamente que un usuario final pueda contaminar o modificar pone en riesgo a la aplicación.

P: ¿Cuáles son los tres grandes tipos de XSS reconocidos por comités como OWASP?
R: Stored (el código se almacena en una base de datos antes de ejecutarse), reflected (el servidor lo refleja sin almacenarlo) y DOM-based (se almacena y ejecuta en el navegador).

P: ¿Cuál es el fallo arquitectónico del ejemplo del banco mega-bank.com?
R: Aplicar literalmente el resultado de una petición HTTP al DOM, típicamente con `innerHTML`, de modo que el texto se interpreta como marcado en lugar de texto.

P: ¿Por qué el stored XSS es fácil de detectar pero a menudo el más peligroso?
R: Porque se almacena como texto en el servidor (fácil de escanear), pero un objeto almacenado o global infectado puede ser visto por muchos usuarios, ampliando el alcance.

P: ¿Qué requisito único define a un XSS como "stored"?
R: Que el payload se almacene en la base de datos de la aplicación; no necesita ser JavaScript válido ni que el cliente sea un navegador.

P: ¿En qué se diferencia el reflected XSS del stored?
R: Opera igual pero no se almacena en base de datos: el servidor refleja el payload directamente de vuelta al cliente.

P: Según la regla general del capítulo, ¿cuál es el trade-off del reflected XSS?
R: Evade mejor la detección (nunca se almacena, suele atacar a un usuario directo) pero generalmente es más difícil de distribuir a muchos usuarios.

P: ¿Qué dos componentes necesita un DOM-based XSS para ejecutarse?
R: Un source (objeto DOM que almacena texto) y un sink (API DOM capaz de ejecutar un script almacenado como texto); nunca requiere interacción con un servidor.

P: ¿Por qué el DOM-based XSS es casi imposible de detectar con análisis estático o escáneres?
R: Porque no toca el servidor y depende de las diferencias de implementación entre navegadores y versiones (un navegador de 2015 puede ser vulnerable y uno moderno no).

P: ¿En qué consiste el mutation-based XSS (mXSS)?
R: Usa payloads seguros para el filtro que mutan en payloads inseguros tras pasar la filtración, aprovechando cómo el navegador optimiza y renderiza nodos DOM; ha burlado DOMPurify, OWASP AntiSamy y Google Caja.

P: ¿Qué es un polyglot payload?
R: Un payload capaz de ejecutar script en muchos contextos distintos del navegador (atributos, comentarios HTML, etiquetas, cadenas JS), lo que ahorra trabajo al atacante.

P: ¿Cómo burla filtros la técnica de Protocol-Relative URLs (PRURLs)?
R: Quitando `http`/`https` y usando `//` para que el navegador elija el protocolo, evadiendo filtros que ocurren antes de instanciar los nodos DOM.

P: Define sink y source en el contexto de XSS.
R: El sink es el método del navegador capaz de ejecutar script (p. ej. `eval()`, `document.write()`, `innerHTML`); el source es el lugar que acepta un payload de texto que luego lee y ejecuta el sink (p. ej. `window.location.hash`, `localStorage`).

P: ¿Cuál es la causa raíz del XSS y qué mitigaciones cita el capítulo?
R: Inyectar entrada no saneada en la UI; mitigaciones citadas: regex contra etiquetas script, reglas CSP que impidan script inline y sanitizadores como DOMPurify.

## Preguntas de autoevaluación

P: Describe el flujo completo del fallo XSS en el portal de soporte del banco.
R: El usuario envía un comentario por formulario → se almacena en base de datos → otros usuarios lo solicitan por HTTP → se inyecta en la página → el comentario inyectado se interpreta como DOM en lugar de texto. (Sección "Descubrimiento y explotación de XSS", PDF p. 160-161)

P: ¿Qué puede lograr un atacante una vez que su `<script>` llega al DOM y se ejecuta?
R: Ejecutar un script no escrito por el dueño de la app sin visibilidad ni interacción, obtener cualquier dato de la app, enviar/recibir datos de un servidor malicioso, robar tokens de sesión (account takeover) y dibujar objetos DOM sobre la UI para phishing perfecto. (Sección "Descubrimiento y explotación de XSS", PDF p. 163-164)

P: ¿Por qué escanear las entradas de la base de datos no es una mitigación definitiva contra el stored XSS?
R: Porque los payloads avanzados pueden no estar en texto plano (base64, binario) o almacenarse en varias partes y concatenarse al usarse en el cliente. (Sección "Stored XSS")

P: En el ejemplo de reflected XSS, ¿cómo se dispara el ataque y cómo se distribuye?
R: La búsqueda del portal correlaciona el query param con el encabezado de resultados; al inyectar `<script>alert(test);</script>` en la URL se dispara un modal. El atacante distribuye el enlace malicioso por email, anuncios u otros medios, disfrazándolo de enlace legítimo. (Sección "Reflected XSS")

P: En el ejemplo de DOM-based XSS del portal de inversiones, ¿cuáles son el source y el sink?
R: `window.location.hash` es la fuente (source) y `document.write()` el sumidero (sink); el enlace con `#<script>alert(document.cookie);</script>` hace que `document.write()` ejecute el hash como script. (Sección "DOM-Based XSS")

P: ¿Por qué el payload de mXSS de Masato Kinugawa en la librería Closure pasó por DOMPurify?
R: Porque técnicamente debería ser DOM-safe: DOMPurify usa un elemento raíz `<template>` con scripting deshabilitado, donde `<noscript>` representa sus hijos; en el navegador real, con scripting habilitado, el `<p title="` se ignora y el `img onerror` se activa tras las optimizaciones del navegador. (Sección "Mutation-Based XSS (mXSS)")

P: Enumera las técnicas de evasión de filtros descritas en el capítulo.
R: Self-closing HTML tags, Protocol-Relative URLs (PRURLs), malformed tags, encoding escapes (Unicode con `\u`) y polyglot payloads. (Sección "Bypassing Filters (Evasión de filtros)")

P: ¿En qué specs abiertas se basan JavaScript y el DOM, y por qué importa para el XSS?
R: En las specs de TC39 (ECMAScript) y WHATWG (DOM), pero cada navegador las implementa distinto, lo que hace que la vulnerabilidad DOM-based dependa del navegador y versión. El autor recomienda leer esas specs para encontrar más sinks y sources. (Secciones "DOM-Based XSS" y "XSS Sinks and Sources")

## Puntos a dominar

- Distinguir los tres tipos de XSS (stored, reflected, DOM-based) y el trade-off detección/alcance/distribución de cada uno.
- Explicar el fallo raíz: inyectar entrada no saneada en el DOM (p. ej. vía `innerHTML`) hace que el texto se interprete como marcado.
- Reconocer el modelo sink/source y citar ejemplos (sinks: `eval()`, `document.write()`, `innerHTML`, `setTimeout()`; sources: `window.location.hash`, `document.referrer`, `localStorage`).
- Entender por qué el DOM-based XSS evade análisis estático y depende de la implementación de cada navegador.
- Describir el mecanismo de mXSS: payload seguro que muta en inseguro tras la sanitización, burlando DOMPurify, OWASP AntiSamy y Google Caja.
- Identificar las cinco técnicas de evasión de filtros y cómo el navegador "corrige" payloads para activarlos.
- Enumerar las mitigaciones citadas: regex contra etiquetas script, reglas CSP contra script inline y sanitizadores como DOMPurify.
