# Web Application Security (2nd Edition) — Andrew Hoffman (O'Reilly Media, 2024)
## Prólogo — Preface (Prólogo)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas indican la página del PDF.

## Lo que necesitas saber

El prólogo presenta el libro *Web Application Security: Exploitation and Countermeasures for Modern Web Applications* y sirve para que decidas si es para ti. Su tesis es que para asegurar una aplicación web primero hay que entender cómo piensan y actúan los hackers: el libro recorre tanto las técnicas ofensivas como las defensivas, con una proporción casi 1:1 de capítulos de ataque y de defensa.

Respecto a la primera edición, esta segunda añade más de cien páginas de contenido nuevo, contenido avanzado por capítulo (para profesionales senior además de ingenieros junior/intermedios) y tecnologías recientes como GraphQL y bases de datos NoSQL. El enfoque es enseñar conceptos a bajo nivel —qué ocurre "bajo el capó" de las herramientas— en lugar de depender de herramientas concretas, que son efímeras en la industria.

Al terminar, deberías poder: hacer recon contra aplicaciones sin acceso al código, identificar threat vectors y vulnerabilidades, construir payloads para comprometer datos o alterar el flujo de ejecución, y escribir código que defienda la aplicación y a sus usuarios. El contenido sube de dificultad de forma progresiva y define cualquier tecnología nueva antes de usarla.

## Por qué JavaScript y por qué conceptos en lugar de herramientas

La mayoría de los ejemplos están en JavaScript porque es el único lenguaje que corre en el cliente dentro del navegador; usarlo también en el servidor mantiene cliente y servidor en el mismo lenguaje. Los lenguajes son en gran parte intercambiables, así que los ataques y mitigaciones del lado servidor se pueden aplicar a otros lenguajes.

El libro explica técnicas a bajo nivel: por ejemplo, desarrollarás payloads de XSS y buscarás XSS sinks a mano en lugar de usar una herramienta automática como XSS-Sniper. La dependencia de herramientas impide usar ataques o mitigaciones avanzadas, y las herramientas quedan obsoletas con frecuencia. No se usan herramientas especializadas de seguridad; solo scripts propios, peticiones de red y el utillaje estándar de sistemas Unix y de los tres navegadores principales (Chrome, Firefox y Edge).

## Conocimientos previos y audiencia

El nivel requerido es "intermedio" en ingeniería de software, no principiante absoluto. Las habilidades mínimas (PDF p. 9):

- Escribir programas CRUD básicos (create, read, update, delete) en al menos un lenguaje.
- Escribir código de servidor (backend).
- Escribir algo de código de navegador (frontend, normalmente JavaScript).
- Saber qué es HTTP y poder hacer o al menos leer llamadas GET/POST.
- Entender aplicaciones que combinan código cliente y servidor comunicándose por HTTP.
- Estar familiarizado con al menos una base de datos popular (MySQL, MongoDB, etc.).

Audiencias principales: ingenieros de software y desarrolladores web (frontend, backend y full stack) de carrera temprana o media; y, como segunda audiencia, ingenieros de seguridad, pen testers y bug bounty hunters que entienden los ataques conceptualmente pero quieren profundizar en el sistema y el código detrás de las herramientas.

## Cómo está organizado el libro

Tras una breve lección de historia, el contenido principal se divide en tres partes:

- **Recon** (Parte I): obtener información sobre una aplicación sin intentar hackearla aún. El recon experto es lo que diferencia a los grandes hackers de los buenos y sirve para priorizar exploits, porque contra objetivos bien defendidos quizá solo tengas una oportunidad. Clave para pruebas "black box", donde el tester no conoce la estructura ni el código y debe construir su entendimiento mediante análisis.
- **Offense** (Parte II): organizada exploit por exploit. Cada capítulo explica el mecanismo del exploit, cómo buscar vulnerabilidades y cómo crear un payload contra una app demo, empezando por defensas rutinarias y avanzando hacia mecanismos más sofisticados.
- **Defense** (Parte III): revisa cada exploit de la Parte II desde el punto de vista contrario, con protecciones específicas y generales ("secure by default", buenas prácticas de código, tests, linters). Introduce los *trade-offs* de la seguridad.

> "most software systems are easy to break into" sin defensas (PDF p. 15).

### Los trade-offs de la seguridad

Toda mejora de seguridad tiene un coste fuera de la seguridad: suele ser rendimiento (más operaciones para leer y sanear datos), más código (más mantenimiento, tests y tiempo de ingeniería), más logging/monitorización, o menor usabilidad.

Ejemplo del formulario de login: mostrar un mensaje de error que confirma un usuario inválido facilita el brute force, porque el hacker ya no necesita adivinar la combinación usuario:contraseña, solo la contraseña. Con esquemas de email + contraseña, además, se pueden descubrir direcciones válidas y deducir el esquema de correos corporativos (por ejemplo `first.last@company.com`, `firstlast@company.com`, `firstl@company.com`) para phishing. Por eso es buena práctica dar mensajes de error genéricos, a costa de la usabilidad.

## Lenguaje y terminología

El libro deletrea cada acrónimo la primera vez (como hizo con XSS) y reúne los términos en tres tablas de referencia a las que conviene volver.

- **Ocupaciones (Tabla P-1):** hacker; white hat (hacker ético); black hat (rompe sistemas para lucrarse o causar caos); grey hat (intermedio, a veces ilegal pero por descubrimiento o reconocimiento); penetration tester (pagado por reportar fallos); bug bounty hunter (pen tester freelance en programas de divulgación responsable); application/product security engineer; software security engineer; admin; scrum master; security champion.
- **Términos (Tabla P-2):** vulnerability (bug que permite acciones no previstas); threat/attack vector (subsección insegura y buen objetivo); attack surface (lista de vulnerabilidades); exploit (código o comandos que aprovechan una vulnerabilidad); payload (exploit formateado para enviarse al servidor); red team, blue team, purple team; website, web application, hybrid application (móvil sobre tecnología web, p. ej. Apache Cordova).
- **Acrónimos (Tabla P-3):** API, CSRF, CSS, DDoS, DOM, DoS, HTML, HTTP, HTTPS, JSON, OOP, OSS, REST, RTC, SOAP, SOP (Same Origin Policy), SPA, SSDL, SSL, TLS (reemplaza a SSL, ya deprecado), VCS, XML, XSS, XXE.

## Advertencia legal y convenciones

> Prueba las técnicas solo contra una aplicación propia o con permiso escrito explícito; el uso indebido puede conllevar multas o cárcel (PDF p. 14).

Convenciones tipográficas: *italic* para términos nuevos, URLs y nombres de archivo; `constant width` para código y elementos de programa; `constant width bold` para lo que el usuario teclea literalmente; `constant width italic` para valores que el usuario debe sustituir. Se usan los elementos TIP, NOTE y WARNING.

## Ideas clave

- El libro enseña ofensiva y defensiva con proporción casi 1:1; se recomienda leerlo de principio a fin, aunque sirve como referencia por mitades.
- La segunda edición añade +100 páginas, contenido avanzado por capítulo y tecnologías nuevas (GraphQL, NoSQL).
- Enseña conceptos a bajo nivel en vez de herramientas; solo usa scripts propios, peticiones de red y utillaje estándar de Unix y de Chrome/Firefox/Edge.
- Los ejemplos están en JavaScript porque es el único lenguaje del cliente, pero los conceptos son transferibles a otros lenguajes.
- Requiere nivel intermedio: CRUD, backend, algo de frontend, HTTP (GET/POST), comunicación cliente-servidor y una base de datos popular.
- Estructura en tres partes: Recon, Offense y Defense; el recon es decisivo para priorizar exploits y para pruebas black box.
- Toda mejora de seguridad implica trade-offs en rendimiento, mantenimiento, logging o usabilidad (ejemplo del formulario de login y los mensajes de error genéricos).
- Las tres tablas (P-1 ocupaciones, P-2 términos, P-3 acrónimos) son la referencia de vocabulario común del libro.
- Solo pruebas técnicas contra sistemas propios o con permiso escrito; el mal uso puede tener consecuencias legales.
