# Web Application Security (2nd Edition) — Andrew Hoffman (O'Reilly Media, 2024)
## Capítulo 16 — Client-Side Attacks (Ataques del lado del cliente)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF y las citas usan la página del PDF.

## Lo que necesitas saber

El capítulo trata de los ataques que tienen como objetivo el cliente (el navegador) en lugar del servidor. En la Web 1.0 se asumía que el cliente no era un vector común de ataque, por lo que las empresas invertían poco en asegurar sus clientes de navegador. Con la Web 2.0, cada vez más funcionalidad que antes residía en el servidor (operaciones complejas, almacenamiento de datos, estado) se trasladó al cliente mediante JavaScript, local/session storage, IndexedDB y AJAX. La arquitectura pasó de un modelo donde el servidor hacía todo el cómputo y el cliente solo renderizaba, a uno en que ambos realizan tareas de cómputo complejas.

La tesis central es que los profesionales de seguridad deben actualizar sus habilidades para entregar software seguro tanto del lado del servidor COMO del cliente. Un ataque del lado del cliente es cualquier ataque que no requiere un servidor web vulnerable ni llamadas de red al servidor del cliente.

Sales sabiendo cómo pensar en ataques de cliente (empezando por eliminar el servidor), por qué son difíciles de detectar, y el funcionamiento de tres técnicas concretas: prototype pollution, clickjacking y tabnabbing (tradicional e inverso).

## Métodos para atacar un cliente de navegador

Hay dos formas principales de atacar un cliente de navegador:

- Client-targeted attacks: vulnerabilidades generales que pueden afectar tanto al cliente como al servidor. Ejemplo: regular expression denial of service (ReDoS). Las expresiones regulares existen en lenguajes de servidor (Java, C#, Python) y también en el navegador (JavaScript). ReDoS es un ataque de cliente cuando el código JavaScript está estructurado de modo que el cliente es vulnerable sin llamadas de red ni interacción con el servidor.
- Client-specific attacks: ataques que existen solo en el cliente y casi nunca aparecen en el servidor. El ejemplo principal es DOM-based cross-site scripting (DOM XSS), cubierto en el Capítulo 10: tanto el sink como el source ocurren en el navegador (p. ej., una cadena de `window.location.hash` renderizada vía `eval()`).

### Ventajas de los ataques de cliente

Como en DOM XSS tanto el sink como el source existen solo en el DOM del navegador, el ataque puede explotarse sin que ningún servidor web se entere. Los payloads se entregan directamente al cliente, evitando servidores que registran tráfico y buscan peticiones malformadas. Por eso "client-side attacks are often categorically one of the most difficult types of exploit for a mature corporation to detect" (PDF p. 246).

Además, desarrollar estos exploits es más fácil sin ser identificado: se puede descargar la aplicación HTML/CSS/JS completa, apagar la red, y realizar millones de intentos localmente sin enviar datos a los servidores de producción. Esto evita la detección que generan los múltiples intentos de payload contra un servidor (por humanos, firewalls o escáneres de red).

## Prototype Pollution Attacks

Con el auge de npm y otros gestores de paquetes de JavaScript, los ataques de prototype pollution han aumentado. Solo funcionan contra lenguajes con sistemas de herencia prototípica (p. ej., JavaScript), distintos de la herencia OOP tradicional de Java o C#. Permiten comprometer un objeto al que no tienes acceso a través de otro objeto al que sí tienes acceso y que comparte una relación de herencia prototípica.

### Entender prototype pollution

Partiendo de una pseudo-clase `Technician` y una instancia `Bob`:

```javascript
const Technician = function(name, birthdate, paymentId) {
    this.name = name;
    this.birthdate = birthdate;
    this.paymentId = paymentId; // for paying for jobs
}
const Bob = new Technician("Bob", "12/01/1970", 12345);
```

Los datos se guardan en una prototype chain. `Bob.__proto__` apunta a un objeto prototipo real, mientras que `Technician.prototype` apunta a un blueprint para construir prototipos. Por eso `Bob.__proto__ == Technician.prototype; // true`. Se puede recorrer la cadena manualmente (`Bob.__proto__.__proto__ == Object.prototype; // true`) o usar `instanceof` como atajo.

La jerarquía de herencia es `(Object) -> (Technician) -> (Bob)`. Cuando se llama una función no definida en el objeto actual, el intérprete sube por la cadena hasta encontrarla (p. ej., `toString()` no está en Bob ni en Technician, pero sí en Object — ver Tabla 16-1). Si no se encuentra, se lanza un error.

Esto permite contaminar a Bob sin acceder a él, modificando el prototipo de Technician u Object:

```javascript
const addTechnicianFunctionality = function(obj) {
  Technician.prototype[obj.name] = obj.data
}
// user input payload
{ name: "toString", data: `function() { console.log("polluted!"); }` }
Bob.toString(); // prints "polluted!"
```

El ataque aprovecha que la herencia prototípica recorre la cadena, de modo que contaminar un objeto "spreads" a objetos relacionados que quizá no sean directamente atacables.

### Atacar con prototype pollution

Cuando no hay ejecución completa de script (XSS), los puntos donde los prototipos se fusionan o actualizan son la superficie de ataque. El paquete npm `merge v2.0` es conocido por ser vulnerable. Su función `merge()` combina dos objetos:

```javascript
merge(Object, { isAdmin: true });
console.log(Bob.isAdmin); // undefined

merge(Object, { "__proto__.isAdmin": true });
console.log(Bob.isAdmin); // true
```

Esta librería también es vulnerable a constructor pollution:

```javascript
merge(Object, { "constructor.prototype.isAdmin": true });
console.log(Bob.isAdmin); // true
```

### Arquetipos de prototype pollution

- Denial of service: interferir con la ejecución normal del script (p. ej., cambiar un valor a float en vez de integer), causando bugs posteriores.
- Property injection: modificar un valor del que depende una llamada de función, provocando llamadas de red o funcionalidad no esperada.
- Remote code execution: el peor caso. En el cliente eleva el ataque a XSS; en Node.js (servidor) a ejecución de código del lado del servidor. Normalmente requiere un sink de ejecución como `eval()` o una función de generación de nodos DOM como `DOMParser.parseFromString()`.

## Clickjacking Attacks

Ataques sutiles pero de alto impacto contra el usuario dentro del navegador. Fusionan elementos de UI maliciosos con no maliciosos, o engañan al navegador para enviar input a un servidor o función maliciosa. Pueden implementarse con JavaScript, HTML y CSS. Es factible considerarlos "a form of user-interface keylogger" (PDF p. 252).

### Camera and Microphone Exploit

Uno de los ejemplos tempranos más conocidos es el hijack de micrófono y cámara de Adobe Flash, divulgado en 2008 por Robert Hansen y Jeremiah Grossman. Un juego o página aparentemente inofensiva tenía debajo un iframe con la página de ajustes de Adobe Flash con opacidad cero (invisible). Cada clic del usuario pasaba a esos ajustes privilegiados, otorgando al atacante control de cámara y micrófono. Destacó porque usó un plug-in para escapar del sandbox del navegador y acceder al hardware.

### Crear exploits de clickjacking

El método más común es una web de aspecto legítimo con un iframe invisible debajo apuntando a la web objetivo:

```html
<div id="clickjacker">
  <span id="fake_button">click me</span>
</div>
<iframe id="target_website" src="target-website.com"></iframe>
```

```css
#target_website { opacity: 0; }
#fake_button {
  position: relative; right: 25px; top: 25px;
  pointer-events: none; background-color: blue;
}
```

El atributo `pointer-events: none` hace que los clics sobre `#fake_button` pasen al elemento de debajo (dentro del iframe). Como el iframe suele tener acceso a las session cookies de la web enmarcada, el clic puede iniciar peticiones privilegiadas (hacer público un perfil, iniciar una transacción financiera). Las apps sin controles de framing adecuados son de las más fáciles de atacar así.

## Tabnabbing and Reverse Tabnabbing

Combinan elementos de phishing (engañar al usuario para interactuar con una web maliciosa) y de redirección (redirigir la página actual a una maliciosa). Abusan de las APIs del DOM del navegador para redirigir la página actual o sobrescribir su contenido.

### Tabnabbing tradicional

Abusa del objeto `window` (especificación DOM del WHATWG). Cuando se abre una pestaña con `window.open()`, la función devuelve una referencia al objeto window que abrió la nueva pestaña. Aquí el atacante es la web que lanza la pestaña:

```javascript
const goToLegitWebsite = function() {
 const windowObj = window.open("https://website-b.com");
 setTimeout(() => {
  windowObj.location.replace("https://website-c.com");
 }, 1000 * 60 * 5);
};
```

La web A abre la web B legítima en otra pestaña; tras un tiempo (una vez que el usuario ya verificó que era legítima), A usa `windowObj.location.replace()` para redirigir esa pestaña a la web C, idéntica en apariencia a B. Cuando el usuario reintroduce credenciales, C las copia, las envía al servidor del hacker y redirige a una página de error en B. Es más eficaz que el phishing convencional porque el usuario ya había verificado la pestaña.

### Reverse tabnabbing

Opera en sentido inverso: el atacante es la web abierta en la nueva pestaña y ataca la pestaña inicial. Se apoya en mecanismos para que una pestaña haga llamadas al DOM de la pestaña que la abrió.

- DOM API attack: al invocar `window.open()`, el opener pasa por defecto una referencia a su objeto window a la nueva pestaña. Usando la propiedad `opener`, la nueva pestaña controla la original:

```javascript
// Script for legit website
window.open("https://malicious-website.com")
// Script for malicious website
window.opener.location.replace("https://get-hacked.com")
```

  Limitación: no todas las formas de abrir pestañas/redirigir producen pestañas con referencia `window.opener`, así que no todas las webs son vulnerables.

- HTML link attack: si `window.opener` no está disponible, se puede atacar si se genera (o se engaña a la web para generar) un enlace HTML con `target=_blank`, que también fuerza una nueva pestaña con referencia `opener`:

```html
<a href="https://malicious-website.com" target="_blank">click me</a>
```

- Iframe attack: si ninguno de los anteriores es posible y el iframe no implementa mitigación (p. ej., atributo `sandbox` o política CSP), se accede al window padre vía `window.parent`:

```javascript
window.parent.location.replace("https://get-hacked.com");
```

En resumen, el tabnabbing se basa en que una pestaña obtenga acceso al objeto window que controla a otra mediante llamadas inseguras a la API del DOM.

## Ideas clave

- Un ataque de cliente es cualquiera que no requiere un servidor web vulnerable ni llamadas de red; se divide en client-targeted (p. ej., ReDoS) y client-specific (p. ej., DOM XSS).
- Son de los más difíciles de detectar para una corporación madura porque no generan tráfico de red hacia el servidor.
- Prototype pollution funciona en lenguajes con herencia prototípica (JavaScript): contaminar `Object.prototype` o el constructor propaga el cambio a objetos relacionados no atacables directamente.
- `merge v2.0` de npm es vulnerable a prototype pollution (`__proto__.isAdmin`) y a constructor pollution (`constructor.prototype.isAdmin`).
- Los arquetipos de prototype pollution son DoS, property injection y RCE (eleva a XSS en cliente o a ejecución de código en Node.js, vía sinks como `eval()`).
- Clickjacking superpone un iframe invisible (`opacity: 0`) con `pointer-events: none` para que los clics pasen a funcionalidad privilegiada; actúa como un keylogger de UI.
- El exploit de cámara y micrófono de Adobe Flash (2008, Hansen y Grossman) usó un plug-in para escapar del sandbox del navegador.
- El tabnabbing tradicional ataca desde la pestaña que abre; el reverse tabnabbing ataca desde la pestaña abierta vía `window.opener`, enlaces `target=_blank` o `window.parent` en iframes.
