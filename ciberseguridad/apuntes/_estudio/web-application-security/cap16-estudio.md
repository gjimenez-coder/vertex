# Client-Side Attacks (Ataques del lado del cliente) — Estudio

## Tarjetas de repaso

P: ¿Qué es un ataque del lado del cliente?
R: Cualquier ataque que no requiere un servidor web vulnerable ni llamadas de red al servidor del cliente; tiene como objetivo el navegador en lugar del servidor.

P: ¿En qué dos tipos se dividen los métodos para atacar un cliente de navegador?
R: Client-targeted attacks (vulnerabilidades generales que afectan a cliente y servidor, p. ej. ReDoS) y client-specific attacks (ataques que existen solo en el cliente, p. ej. DOM-based XSS).

P: ¿Por qué ReDoS puede ser un ataque de cliente?
R: Porque las expresiones regulares existen también en JavaScript; cuando el código está estructurado de modo que el cliente es vulnerable sin llamadas de red ni interacción con el servidor, ReDoS es un ataque de cliente.

P: ¿Por qué los ataques de cliente son difíciles de detectar para una corporación madura?
R: Porque no generan tráfico de red hacia el servidor; en DOM XSS tanto el sink como el source existen solo en el DOM del navegador, evitando los servidores que registran tráfico y buscan peticiones malformadas.

P: ¿Qué ventaja tiene desarrollar exploits de cliente sin ser identificado?
R: Se puede descargar la aplicación HTML/CSS/JS completa, apagar la red y realizar millones de intentos localmente sin enviar datos a los servidores de producción.

P: ¿En qué lenguajes funciona prototype pollution y qué permite?
R: Solo en lenguajes con herencia prototípica (p. ej. JavaScript); permite comprometer un objeto al que no tienes acceso a través de otro al que sí tienes acceso y que comparte una relación de herencia prototípica.

P: ¿Qué relación verifica `Bob.__proto__ == Technician.prototype`?
R: Es `true`: `__proto__` apunta al objeto prototipo real y `Technician.prototype` apunta al blueprint para construir prototipos; por eso la instancia hereda de su pseudo-clase.

P: ¿Qué hace el intérprete cuando se llama una función no definida en el objeto actual?
R: Sube por la prototype chain hasta encontrarla (p. ej. `toString()` se encuentra en Object); si no la encuentra, lanza un error.

P: ¿Qué paquete npm es conocido por ser vulnerable a prototype pollution y cómo se explota?
R: `merge v2.0`; con `merge(Object, { "__proto__.isAdmin": true })` (prototype pollution) y con `merge(Object, { "constructor.prototype.isAdmin": true })` (constructor pollution).

P: ¿Cuáles son los tres arquetipos de prototype pollution?
R: Denial of service (interferir con la ejecución normal del script), property injection (modificar un valor del que depende una función) y remote code execution (eleva a XSS en cliente o a ejecución de código en Node.js).

P: ¿Qué sinks suele requerir el prototype pollution que llega a RCE?
R: Un sink de ejecución como `eval()` o una función de generación de nodos DOM como `DOMParser.parseFromString()`.

P: ¿Cómo funciona un exploit de clickjacking típico?
R: Una web de aspecto legítimo con un iframe invisible debajo (`opacity: 0`) apuntando a la web objetivo; `pointer-events: none` hace que los clics pasen al iframe, que suele tener acceso a las session cookies.

P: ¿Qué fue el exploit de cámara y micrófono de Adobe Flash?
R: Divulgado en 2008 por Robert Hansen y Jeremiah Grossman; un iframe invisible con la página de ajustes de Adobe Flash capturaba los clics y usaba un plug-in para escapar del sandbox del navegador y acceder al hardware.

P: ¿Qué diferencia al tabnabbing tradicional del reverse tabnabbing?
R: En el tradicional el atacante es la web que abre la pestaña y redirige la pestaña abierta; en el reverse el atacante es la web abierta y ataca la pestaña inicial vía `window.opener` o `window.parent`.

P: ¿Qué tres vías puede usar el reverse tabnabbing para acceder a la pestaña original?
R: DOM API attack (propiedad `window.opener`), HTML link attack (enlace con `target=_blank`) e iframe attack (`window.parent` cuando el iframe no implementa mitigación).

## Preguntas de autoevaluación

P: ¿Por qué cambió la relevancia de la seguridad del cliente entre la Web 1.0 y la Web 2.0?
R: En la Web 1.0 se asumía que el cliente no era un vector común y se invertía poco en asegurarlo; con la Web 2.0 se trasladó al cliente mucha funcionalidad (JavaScript, local/session storage, IndexedDB, AJAX), de modo que ambos realizan cómputo complejo. (Sección: Lo que necesitas saber)

P: ¿Qué distingue a un client-specific attack de un client-targeted attack, con un ejemplo de cada uno?
R: El client-targeted es una vulnerabilidad general que afecta a cliente y servidor (ReDoS); el client-specific existe solo en el cliente y casi nunca en el servidor (DOM-based XSS, con sink y source en el navegador). (Sección: Métodos para atacar un cliente de navegador)

P: ¿Cómo se contamina a Bob sin acceder directamente a él mediante prototype pollution?
R: Modificando el prototipo de Technician u Object (p. ej. `Technician.prototype[obj.name] = obj.data`); como la herencia recorre la cadena, el cambio se propaga a los objetos relacionados. (Sección: Prototype Pollution Attacks — Entender prototype pollution)

P: ¿Cuál es el peor caso de un ataque de prototype pollution y cómo se comporta según el entorno?
R: Remote code execution: en el cliente eleva el ataque a XSS y en Node.js (servidor) a ejecución de código del lado del servidor; normalmente requiere un sink como `eval()` o `DOMParser.parseFromString()`. (Sección: Arquetipos de prototype pollution)

P: ¿Por qué el atributo `pointer-events: none` es clave en el clickjacking?
R: Hace que los clics sobre el botón falso pasen al elemento de debajo (el iframe de la web objetivo), de modo que el clic puede iniciar peticiones privilegiadas usando las session cookies del iframe. (Sección: Clickjacking Attacks — Crear exploits de clickjacking)

P: ¿Por qué el tabnabbing tradicional es más eficaz que el phishing convencional?
R: Porque la web A abre la web B legítima, el usuario la verifica y solo después A redirige esa pestaña a la web C idéntica; el usuario reintroduce credenciales sobre una pestaña que ya había validado. (Sección: Tabnabbing and Reverse Tabnabbing — Tabnabbing tradicional)

P: ¿Qué limitación tiene el DOM API attack del reverse tabnabbing y cómo se sortea?
R: No todas las formas de abrir pestañas o redirigir producen una referencia `window.opener`, así que no todas las webs son vulnerables; si no está disponible, se recurre al HTML link attack (`target=_blank`) o al iframe attack (`window.parent`). (Sección: Reverse tabnabbing)

## Puntos a dominar

- Definir ataque de cliente y diferenciar client-targeted (ReDoS) de client-specific (DOM XSS).
- Explicar por qué estos ataques evaden la detección basada en tráfico de red al servidor.
- Describir la prototype chain (`__proto__`, `prototype`, jerarquía Object → Technician → Bob) y cómo se recorre.
- Reconocer vectores de prototype pollution en `merge v2.0` (`__proto__.isAdmin`, `constructor.prototype.isAdmin`).
- Clasificar los arquetipos de prototype pollution: DoS, property injection y RCE, y sus sinks (`eval()`, `DOMParser.parseFromString()`).
- Identificar la estructura de un clickjacking: iframe invisible (`opacity: 0`) + `pointer-events: none` como keylogger de UI.
- Distinguir tabnabbing tradicional de reverse tabnabbing y sus tres vías (`window.opener`, `target=_blank`, `window.parent`).
