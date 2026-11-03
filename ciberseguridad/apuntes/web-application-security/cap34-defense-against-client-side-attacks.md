# Web Application Security (2nd Edition) — Andrew Hoffman (O'Reilly Media, 2024)
## Capítulo 34 — Defense Against Client-Side Attacks (Defensa contra ataques del lado del cliente)

> Nota de extracción: el texto se obtuvo de la capa de texto del PDF; las citas usan la página del PDF.

## Lo que necesitas saber
Este capítulo es el complemento defensivo del Capítulo 16, donde se cubrieron tres formas de ataque del lado del cliente: prototype pollution, clickjacking y tabnabbing. En esos ataques se explota al usuario a través de su navegador cliente en lugar de pasar por un servidor para atacar al usuario final. El autor señala que los ataques del lado del cliente van en aumento a medida que los navegadores se vuelven más sofisticados cada año.

La tesis central es práctica: como detectar ataques del lado del cliente tiene limitaciones, lo imperativo es configurar la aplicación de forma que estos ataques sean difíciles de ejecutar con éxito. El capítulo recorre las técnicas de mitigación para cada uno de los tres ataques.

Sales sabiendo cómo mitigar prototype pollution (sanitización de claves, congelado de prototipos, prototipos nulos), cómo frenar clickjacking (directiva `frame-ancestors` de CSP y scripts framebuster) y cómo prevenir tabnabbing (Cross-Origin-Opener Policy, atributos de enlace y políticas de aislamiento con fetch metadata). El mensaje de cierre es que la mayoría de estos ataques se detienen, al menos en parte, en el propio navegador mediante cambios simples de configuración, por lo que aprender estas mitigaciones es de los métodos más rentables y que más tiempo ahorran para mejorar la postura de seguridad.

## Defensa contra prototype pollution
Estos ataques dependen del sistema de herencia prototipal de JavaScript. Por cómo el intérprete recorre la cadena de prototipos buscando funciones y datos, un atacante puede contaminar un objeto sin acceso directo, contaminando un objeto relacionado en la jerarquía de herencia. Son difíciles de encontrar al principio por apoyarse en características específicas del lenguaje, pero las mitigaciones se entienden con facilidad una vez dominadas.

### Key Sanitization (sanitización de claves)
Una de las formas más fáciles de prevenirlos es asegurar que el código JavaScript sanitiza todas las claves provistas por el usuario antes de fusionar o manipular objetos. La clave `__proto__` es la parte del objeto que explota la cadena de prototipos al fusionarse en otro objeto:

```javascript
// submitted via address collection form
const obj = { 
  "__proto__": { "role": "admin" }
}
```

Con una allowlist de claves disponibles se puede iterar sobre las entradas del usuario y prevenir el ataque:

```javascript
const allowedKeys = ["street", "city", "state", "firstName", "lastName"];
```

El allowlisting no siempre es aceptable, ya que algunas aplicaciones necesitan aceptar entradas flexibles y no pueden depender de un conjunto estático de claves. Donde sea posible, es "one of the best first-line solutions" (PDF p. 423) contra estos ataques.

### Prototype Freezing (congelado de prototipos)
La función `Object.freeze()` convierte los objetos en inmutables en lugar de mutables. Un objeto congelado no puede tener claves, valores ni propiedades actualizadas durante el resto de la sesión; al cerrar y reabrir la pestaña vuelve a ser mutable hasta que se vuelva a llamar a `Object.freeze()`.

Limitaciones importantes: un objeto congelado no puede modificarse ni para fines maliciosos ni legítimos, lo que reduce la funcionalidad para el código de primera parte y complica el desarrollo. Además, congelar en bloque APIs de JavaScript o del DOM tiene consecuencias graves, porque docenas de APIs dependen de la mutabilidad de otros objetos; un freeze masivo o accidental sobre APIs integradas rompe amplias porciones de funcionalidad. Por eso debe usarse con moderación.

### Null Prototypes (prototipos nulos)
Como mitigación final, se puede cortar la cadena de prototipos de un objeto durante su instanciación usando directamente el constructor de objetos y pasando `null`:

```javascript
// traditional object creation
const myObj1 = { username: "testUser1" }

// manual object constructor invocation inheriting from null
const myObj2 = Object.create(null);
myObj2["username"] = "testUser2";
Object.getPrototypeOf(myObj2); // null
```

Al crearse sin prototipo, el objeto no puede recorrer la cadena ni ser contaminado vía objetos padre, porque no existe ningún padre.

## Defensa contra clickjacking
Hay múltiples defensas, pero solo dos son muy efectivas: una a nivel de CSP y otra en JavaScript. Las defensas legacy con cabeceras como `X-Frame-Options` se consideran obsoletas por la mayoría de navegadores y no deben considerarse una línea de defensa efectiva.

### Frame Ancestors
La forma más fácil y efectiva de detener la mayoría de ataques de clickjacking es cambiar la política CSP del sitio con la directiva `frame-ancestors`, aplicable en cabecera o meta tag:

```
Content-Security-Policy: frame-ancestors 'none';
```

Esto indica al navegador que impida cargar la página dentro de un iframe. Más del 95% de los navegadores modernos soportan esta directiva, así que detiene casi todos los intentos de clickjacking. Si la aplicación necesita ser enmarcada en otro sitio, se puede relajar con una allowlist:

```
Content-Security-Policy: frame-ancestors subdomain.my-website.com
```

También existe la opción `self` para el caso raro de que la aplicación necesite contener una copia de sí misma en un iframe.

### Framebusting
Para los pocos navegadores que no soportan `frame-ancestors`, o casos de enmarcado especiales, existen los scripts framebuster (también llamados framekillers): funciones JavaScript que detectan si el sitio está siendo enmarcado donde no se permite y detienen o descargan el código.

```javascript
html { 
  display:none;
}
if (self == top) { 
    document.documentElement.style.display = 'block';
}
```

El CSS debe ir en el bloque `head` para cargarse antes del `body`, y el JavaScript en el `body` para cargarse después. El contenido arranca con `display: none` (invisible y sin interacción), lo que impide que los clics secuestrados interactúen con la página. El script compara los objetos integrados `self` y `top`: si es la ventana superior, cambia a `display: block`, volviendo el contenido visible e interactivo; si no lo es, los scripts siguen ejecutándose pero sin renderizar contenido visible ni interactivo. Las formas legacy que permiten cargar la página antes de ejecutar el framebuster no son ideales: dejan una ventana de tiempo para secuestrar clics y un atacante puede detener o retrasar la ejecución del script.

## Defensa contra tabnabbing
Los ataques de tabnabbing son fáciles de prevenir con planificación gracias a las mitigaciones integradas del navegador. Al ser soluciones simples, deberían implementarse por defecto en cualquier aplicación nueva, aunque muchas las omiten y quedan vulnerables.

### Cross-Origin-Opener Policy (COOP)
CSP soporta la política COOP, que determina qué sitios reciben una referencia al objeto window al abrirse en un hiperenlace. Por defecto debería estar en:

```
Cross-Origin-Opener-Policy: same-origin
```

Esto impide que los enlaces abiertos puedan referenciar el sitio del que se originaron. Es la solución de primera línea para la mayoría de casos de tabnabbing; solo se vuelve problemática en sitios grandes con múltiples dominios, donde conviene un COOP más relajado combinado con otras técnicas.

### Link Blockers (bloqueadores de enlaces)
Como los hiperenlaces permiten por defecto referenciar la página que los abre, dejar que los usuarios generen enlaces es arriesgado. El atributo `noopener` cambia la referencia `window.opener` del sitio destino a `null`:

```html
<a href="malicious-website.com rel="noopener">click me</a>
```

Conviene acompañarlo de su atributo hermano `noreferrer`, que impide que el sitio destino acceda a la información de referrer:

```html
<a href="malicious-website.com rel="noopener noreferrer">click me</a>
```

Con ambas políticas mejora la seguridad y la privacidad, y el tabnabbing vía enlaces dinámicos se vuelve imposible.

### Isolation Policies (políticas de aislamiento)
Una función nueva del navegador, fetch metadata, soporta políticas de aislamiento flexibles que mitigan múltiples ataques del lado del cliente. Están disponibles solo en los builds recientes de Firefox y Chrome; no en Safari de escritorio ni iOS, ni en la mayoría de navegadores internacionales. Por eso hoy deben considerarse defense in depth, implementadas junto a otras mitigaciones.

Como parte de fetch metadata, los navegadores envían cabeceras en cada petición:

- `Sec-Fetch-Site`: indica desde dónde se solicita el sitio. Valores: `same-origin`, `same-site`, `cross-site`, `none`.
- `Sec-Fetch-Mode`: el modo de la petición. Valores: `same-origin`, `no-cors`, `cors`, `navigate`.
- `Sec-Fetch-Dest`: dónde se cargará el contenido. Valores: `audio`, `audioworklet`, `embed`, `font`, `frame`, `manifest`, `object`, `paintworklet`, `report`, `script`, `serviceworker`, `sharedworker`, `style`, `track`, `video`, `xslt`.
- `Sec-Fetch-User`: `1` si el navegador cree que el usuario inició la petición; `null` si cree que fue un script o plug-in.

Combinando estas cabeceras en el servidor se crean mitigaciones potentes. Ejemplo para impedir que un sitio sea enmarcado (bloqueando la mayoría del clickjacking):

```javascript
app.get('/index.html', function(req, res, next) { 
  if (req.headers["Sec-Fetch-Dest"]) { 
    const dest = req.headers["Sec-Fetch-Dest"]; 
    if (dest === "frame") { 
      return res.sendStatus(400); 
    } else { 
      return res.sendFile("/index.html")); 
    } 
  }
});
```

## Ideas clave
- Los ataques del lado del cliente explotan al usuario a través del navegador sin pasar por el servidor; como detectarlos es limitado, hay que configurar la app para dificultarlos.
- Prototype pollution se mitiga con sanitización de claves (allowlist), `Object.freeze()` y objetos sin prototipo con `Object.create(null)`.
- `Object.freeze()` es potente pero debe usarse con moderación: inmoviliza el objeto para todo uso y un freeze masivo rompe APIs del DOM y de JavaScript.
- Contra clickjacking, la directiva CSP `frame-ancestors 'none'` es la defensa principal (soporte >95%); `X-Frame-Options` es obsoleta.
- Los scripts framebuster son la alternativa cuando no hay soporte de `frame-ancestors`; los framebusters legacy dejan una ventana vulnerable.
- Contra tabnabbing: `Cross-Origin-Opener-Policy: same-origin` por defecto, y en enlaces dinámicos los atributos `noopener` y `noreferrer`.
- Las políticas de aislamiento vía fetch metadata (`Sec-Fetch-Site`, `-Mode`, `-Dest`, `-User`) son defense in depth, hoy solo en Firefox y Chrome recientes.
- La mayoría de los ataques del lado del cliente se frenan en parte en el navegador con cambios simples de configuración, lo que hace estas mitigaciones muy rentables.
