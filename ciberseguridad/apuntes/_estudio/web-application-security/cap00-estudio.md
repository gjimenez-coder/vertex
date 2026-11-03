# Prólogo — Preface (Prólogo) — Estudio

## Tarjetas de repaso

P: ¿Cuál es la tesis central del libro según el prólogo? / R: Para asegurar una aplicación web primero hay que entender cómo piensan y actúan los hackers; por eso recorre técnicas ofensivas y defensivas con proporción casi 1:1.

P: ¿Qué añade la segunda edición respecto a la primera? / R: Más de cien páginas de contenido nuevo, contenido avanzado por capítulo y tecnologías recientes como GraphQL y bases de datos NoSQL.

P: ¿Por qué el libro enseña conceptos a bajo nivel en lugar de depender de herramientas? / R: La dependencia de herramientas impide usar ataques o mitigaciones avanzadas y las herramientas quedan obsoletas con frecuencia.

P: ¿Por qué la mayoría de los ejemplos están en JavaScript? / R: Porque es el único lenguaje que corre en el cliente dentro del navegador; usarlo también en el servidor mantiene cliente y servidor en el mismo lenguaje, y los conceptos son transferibles a otros lenguajes.

P: ¿Qué herramientas usa el libro? / R: Solo scripts propios, peticiones de red y el utillaje estándar de sistemas Unix y de los tres navegadores principales (Chrome, Firefox y Edge); no usa herramientas especializadas de seguridad.

P: ¿En qué tres partes se divide el contenido principal? / R: Recon (Parte I), Offense (Parte II) y Defense (Parte III), tras una breve lección de historia.

P: ¿Qué es el recon y por qué importa? / R: Obtener información sobre una aplicación sin intentar hackearla aún; es lo que diferencia a los grandes hackers y sirve para priorizar exploits, siendo clave en pruebas black box.

P: ¿Cómo se organiza la Parte de Offense? / R: Exploit por exploit; cada capítulo explica el mecanismo del exploit, cómo buscar vulnerabilidades y cómo crear un payload contra una app demo.

P: ¿Qué principio rige los trade-offs de la seguridad? / R: Toda mejora de seguridad tiene un coste fuera de la seguridad: rendimiento, más código y mantenimiento, más logging/monitorización o menor usabilidad.

P: ¿Qué diferencia a una vulnerability de un exploit y de un payload? / R: Vulnerability es un bug que permite acciones no previstas; exploit es el código o comandos que la aprovechan; payload es el exploit formateado para enviarse al servidor.

P: ¿Qué es un threat/attack vector frente a un attack surface? / R: El threat/attack vector es una subsección insegura y buen objetivo; el attack surface es la lista de vulnerabilidades.

P: ¿Qué distingue a un white hat, un black hat y un grey hat? / R: El white hat es hacker ético; el black hat rompe sistemas para lucrarse o causar caos; el grey hat es intermedio, a veces ilegal pero por descubrimiento o reconocimiento.

P: ¿Qué nivel previo requiere el libro? / R: Nivel intermedio: CRUD, código backend, algo de frontend, saber qué es HTTP (GET/POST), comunicación cliente-servidor y familiaridad con una base de datos popular.

P: ¿Qué relación tienen TLS y SSL según los acrónimos? / R: TLS reemplaza a SSL, que ya está deprecado.

## Preguntas de autoevaluación

P: ¿Qué deberías poder hacer al terminar el libro? / R: Hacer recon sin acceso al código, identificar threat vectors y vulnerabilidades, construir payloads para comprometer datos o alterar el flujo de ejecución, y escribir código que defienda la aplicación y a sus usuarios. (Sección "Lo que necesitas saber")

P: ¿Por qué buscar XSS sinks a mano en lugar de usar una herramienta como XSS-Sniper? / R: Porque enseña las técnicas a bajo nivel; depender de herramientas impide ataques y mitigaciones avanzadas y las herramientas se vuelven obsoletas. (Sección "Por qué JavaScript y por qué conceptos en lugar de herramientas")

P: ¿Cuáles son las dos audiencias del libro? / R: La principal son ingenieros de software y desarrolladores web (frontend, backend, full stack) de carrera temprana o media; la segunda, ingenieros de seguridad, pen testers y bug bounty hunters que quieren profundizar en el sistema y el código detrás de las herramientas. (Sección "Conocimientos previos y audiencia")

P: ¿Cómo aborda la Parte III (Defense) los exploits de la Parte II? / R: Los revisa desde el punto de vista contrario, con protecciones específicas y generales ("secure by default", buenas prácticas de código, tests, linters), e introduce los trade-offs de la seguridad. (Sección "Cómo está organizado el libro")

P: Con el ejemplo del formulario de login, ¿por qué conviene dar mensajes de error genéricos? / R: Porque un mensaje que confirma un usuario inválido facilita el brute force y permite descubrir direcciones válidas y deducir el esquema de correos corporativos para phishing; el coste es menor usabilidad. (Sección "Los trade-offs de la seguridad")

P: ¿Qué advertencia legal establece el prólogo? / R: Probar las técnicas solo contra una aplicación propia o con permiso escrito explícito, porque el uso indebido puede conllevar multas o cárcel. (Sección "Advertencia legal y convenciones")

P: ¿Para qué sirven las tres tablas de referencia del prólogo? / R: Reúnen el vocabulario común del libro: ocupaciones (P-1), términos (P-2) y acrónimos (P-3), a las que conviene volver. (Sección "Lenguaje y terminología")

## Puntos a dominar

- Entender que el libro combina ofensiva y defensiva en proporción casi 1:1 y se recomienda leerlo de principio a fin.
- Dominar el vocabulario de las tres tablas: ocupaciones (P-1), términos (P-2) y acrónimos (P-3).
- Distinguir vulnerability, threat/attack vector, attack surface, exploit y payload.
- Comprender el propósito de las tres partes: Recon, Offense y Defense, y el papel del recon en pruebas black box.
- Interiorizar el principio de los trade-offs de la seguridad (rendimiento, código, logging, usabilidad) con el ejemplo del formulario de login.
- Verificar que cumples el nivel previo requerido: CRUD, backend, frontend básico, HTTP (GET/POST), cliente-servidor y una base de datos popular.
- Recordar que TLS reemplaza a SSL (deprecado).
- Probar técnicas solo contra sistemas propios o con permiso escrito explícito.
