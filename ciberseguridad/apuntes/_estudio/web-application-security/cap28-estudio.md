# Defending Against XSS Attacks (Defensa contra ataques XSS) — Estudio

## Tarjetas de repaso

P: ¿Cuál es la regla principal de codificación anti-XSS?
R: Nunca permitir que datos de usuario sin sanitizar lleguen al DOM; poblar el DOM con datos de usuario debe ser la opción de último recurso.

P: ¿Por qué el cliente es casi siempre el punto ideal para mitigar XSS?
R: Porque un XSS requiere ejecución del lado del cliente para ser un XSS, aunque pueda mitigarse también en red, base de datos o cliente.

P: ¿Cuándo surge la verdadera dificultad para defenderse del XSS?
R: Cuando un requisito de funcionalidad obliga a mostrar datos enviados por el usuario como DOM en lugar de como texto.

P: ¿Qué diferencia hay entre `innerText` e `innerHTML` para inyectar datos de usuario?
R: `innerText` es mucho más seguro porque sanea lo que parezca una etiqueta HTML representándolo como string; `innerHTML` interpreta las etiquetas como DOM.

P: ¿Qué es el pseudoesquema JavaScript y por qué es peligroso?
R: Es el uso de `javascript:` en atributos como `href` para ejecutar código; permite XSS aunque se bloqueen comillas y etiquetas `<script>`, y debe evitarse siempre.

P: ¿Cómo evita el filtrado de comillas `String.fromCharCode()`?
R: Construye strings a partir de códigos de carácter numéricos (p. ej. `String.fromCharCode(88,83,83)`), evitando escribir comillas en el payload.

P: ¿Qué APIs/sinks del DOM conviene evitar por ser vectores potenciales de XSS?
R: `innerHTML`/`outerHTML`, `Blob`, `SVG`, `document.write`/`writeln`, `DOMParser.parseFromString` y `document.implementation`.

P: ¿Por qué `createElement()` + `appendChild()` es menos arriesgado que `DOMParser.parseFromString`?
R: Porque controlas la estructura y los nombres de etiqueta, y el payload solo controla el contenido, no la estructura DOM.

P: ¿Por qué los SVG son más peligrosos que una etiqueta `<img>`?
R: Se basan en la spec XML que permite ejecución de script; pueden lanzar cualquier JavaScript `onload`.

P: ¿Cómo se puede sanear un hipervínculo aprovechando el navegador?
R: Creando un elemento `<a>` ficticio con `document.createElement('a')` y asignando la URL a su `href`, usando el filtrado nativo del navegador para `<a>`.

P: ¿Por qué `encodeURIComponent()` no sirve para una URL completa?
R: Porque el origen (scheme + :// + hostname + : + port) no puede interpretarse codificado; al codificarlo se convierte en otro origen.

P: ¿Cuáles son los "big five" del HTML entity encoding?
R: `&`→`&amp;`, `<`→`&lt;`, `>`→`&gt;`, `"`→`&#034;`, `'`→`&#039;`.

P: ¿Qué contenido NO protege el HTML entity encoding?
R: No protege contenido inyectado dentro de `<script></script>`, CSS ni una URL; solo protege nodos tipo `<div></div>`.

P: ¿Cómo puede el CSS filtrar datos de usuario?
R: Con `background:url` se emite una petición GET a un dominio (con query params), y el estilado selectivo según el estado de un formulario filtra datos.

P: ¿Qué es una CSP y qué controla?
R: Es una herramienta de configuración de seguridad que relaja o endurece qué código puede ejecutarse: qué scripts externos se cargan, desde dónde, y qué APIs del DOM pueden ejecutarlos.

## Preguntas de autoevaluación

P: ¿Por qué el XSS común es fácil de defender pero puede volverse difícil?
R: La mayoría del XSS se mitiga con buenas prácticas de codificación segura; la dificultad aparece cuando hay que mostrar datos de usuario como DOM en lugar de como texto. (Lo que necesitas saber)

P: Si debes permitir algunas etiquetas HTML (`<strong>`, `<i>`) pero no otras (`<script>`), ¿qué hay que hacer y cuál es el matiz?
R: Hay que sanear exhaustivamente y bloquear intentos de escape del sanitizador, teniendo en cuenta que la sanitización completa es extremadamente difícil. (Sanitizar la entrada del usuario)

P: ¿Por qué es preferible crear nodos manualmente en lugar de usar `DOMParser.parseFromString`?
R: Porque `parseFromString` carga el string en nodos DOM que reflejan su estructura, mientras que crear cada nodo con `createElement()`/`appendChild()` te da control de estructura y nombres de etiqueta, dejando al payload solo el contenido. (DOMParser Sink)

P: ¿En qué nodos protege el entity encoding y en cuáles no?
R: Protege contenido inyectado en nodos tipo `<div></div>`, pero no dentro de `<script>`, CSS ni una URL. (HTML Entity Encoding)

P: ¿Cuáles son las tres formas de evitar ataques XSS vía CSS y su dificultad?
R: Prohibir CSS subido por usuarios (fácil); permitir solo campos específicos y generar la hoja de estilos en el servidor (medio); sanear cualquier atributo CSS que inicie HTTP como `background:url` (difícil). (CSS XSS)

P: ¿Qué hace la CSP con los scripts inline y con `eval()` por defecto?
R: Por defecto, con CSP habilitada, la ejecución de scripts inline está deshabilitada (se reactiva con `unsafe-inline`) y `eval()` y métodos string→code también (se reactiva con `unsafe-eval`). (Unsafe Eval y Unsafe Inline)

P: ¿Por qué `script-src` no basta por sí solo y qué limitación tiene la CSP frente al XSS?
R: Porque no protege contra scripts cargados desde tus propios servidores de confianza si un atacante logra almacenar o reflejar uno, y la CSP no protege contra DOM XSS. (Unsafe Eval y Unsafe Inline; Ideas clave)

P: ¿Cuándo conviene aplicar una CSP y por qué?
R: Como primer paso de mitigación si ya sabes qué construcciones y APIs usará la aplicación, porque es un string de configuración que puede cambiarse fácilmente después. (Implementar una CSP)

## Checklist

- Tratar los datos de usuario como string siempre que no se requiera HTML/DOM y usar `innerText` en vez de `innerHTML`.
- Nunca permitir que datos de usuario sin sanitizar lleguen al DOM.
- Evitar el pseudoesquema `javascript:` en atributos como `href`.
- Evitar los sinks de DOM XSS: `innerHTML`/`outerHTML`, `Blob`, `SVG`, `document.write`/`writeln`, `DOMParser.parseFromString`, `document.implementation`.
- Preferir `document.createElement()` + `appendChild()` frente a `DOMParser.parseFromString`.
- Sanear hipervínculos con un elemento `<a>` ficticio y/o `encodeURIComponent()` (sin usarlo sobre una URL completa).
- Aplicar HTML entity encoding de los "big five" en contenido inyectado en nodos tipo `<div>`.
- Prohibir el CSS subido por usuarios o generar la hoja de estilos tú mismo en el servidor con campos permitidos.
- Reescribir funciones que dependan de `eval` para que no se interpreten como string.
- Configurar una CSP con `script-src` restringido, usar `"self"`, evitar wildcards y mantener deshabilitados `unsafe-inline` y `unsafe-eval`.
- Entregar la CSP vía cabecera `Content-Security-Policy` o etiqueta `<meta>`.
