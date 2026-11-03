# Web Application Security (2nd Edition) — Andrew Hoffman (O'Reilly Media, 2024)
## Capítulo 38 — Conclusion (Conclusión)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF y las citas usan la página del PDF.

## Lo que necesitas saber
La conclusión repasa los puntos clave de cada parte del libro: recon (reconocimiento), ofensiva y defensa de aplicaciones web. No introduce material nuevo, sino que sintetiza las ideas centrales de cada capítulo para que el lector pueda revisarlas y volver a los temas que necesite refrescar.

La tesis que atraviesa el repaso es que las aplicaciones web modernas son grandes, distribuidas y dependen fuertemente de terceros, lo que ha desplazado el foco de los atacantes desde las vulnerabilidades en servidores, protocolos de red o navegadores hacia las vulnerabilidades lógicas del código de aplicación. Por eso la colaboración entre desarrolladores y expertos en seguridad es hoy más valiosa que la contribución individual.

Al terminar sales sabiendo cómo encajan recon, ataque y defensa como un ciclo, y qué técnicas defensivas corresponden a cada familia de ataques. El autor cierra recordando que la seguridad web es un campo de aprendizaje continuo y que quien no refresca su conocimiento corre el riesgo de quedar obsoleto.

## Historia de la seguridad del software
Repaso del Capítulo 1 y la evolución del campo:
- Phreaking telefónico: los "phreakers" imitaban las frecuencias que automatizaban las conexiones para llamar gratis. Bell Labs respondió con el sistema DTMF (dual-tone multifrequency), más difícil de reproducir; con el tiempo apareció hardware que imitaba los tonos DTMF y, finalmente, las centrales digitales eliminaron el riesgo (el DTMF permaneció por retrocompatibilidad).
- Hacking de computadoras: el Commodore 64 impulsó la adopción masiva del PC. Fred Cohen demostró el primer virus capaz de autocopiarse vía disquete; Robert Morris fue el primero en desplegar un virus fuera del laboratorio: el Morris Worm se propagó a unas 15.000 computadoras en un día. Morris fue el primer hacker condenado, con una multa de $10.500 y 400 horas de servicio comunitario.
- World Wide Web: la Web 1.0 abrió ataques contra servidores y redes; la Web 2.0 (colaboración usuario-a-usuario sobre HTTP) convirtió al navegador en nuevo vector de ataque.
- Aplicaciones modernas: con la mejora de la seguridad del navegador, los atacantes pasaron a atacar vulnerabilidades lógicas en el código, donde además reside hoy data mucho más valiosa (banca, seguros, medicina).

## Recon (reconocimiento)
El primer paso para atacar es mapear la aplicación y evaluar cada componente en busca de riesgos arquitectónicos o lógicos. Un buen recon da comprensión profunda del objetivo, útil para priorizar ataques y evitar detección. Para el dueño de la aplicación, las mismas habilidades sirven para priorizar defensas.
- Estructura moderna: muchas capas de tecnología, persistencia tanto en servidor como en cliente, lo que amplía la superficie de ataque.
- Subdominios, APIs y HTTP: hay que mapear toda la superficie; las apps están más distribuidas y pueden usar sockets o RTC además de HTTP.
- Dependencias de terceros: tan presentes como el código propio o más, y no auditadas al mismo estándar; mediante fingerprinting se detectan versiones vulnerables de servidores, frameworks cliente, frameworks CSS y bases de datos.
- Arquitectura: evaluar la arquitectura revela vulnerabilidades generalizadas por controles inconsistentes y sirve como señal de la calidad del código.

## Offense (ofensiva)
Puntos clave de la Parte II:
- XSS: posible cuando la app usa indebidamente inputs del usuario permitiendo ejecución de scripts. Incluso con sanitización en DOM o API pueden quedar XSS sinks por bugs del DOM o integraciones de terceros.
- CSRF: explota la relación de confianza entre navegador y usuario; si las peticiones GET que cambian estado ya están filtradas, considerar web forms.
- XXE: una debilidad de la especificación XML permite filtrar archivos del servidor; puede ser directo o indirecto (el servidor construye el XML a partir del payload del usuario).
- Injection: SQL injection es la más conocida, pero cualquier utilidad CLI invocada por una API es un objetivo (compresores de imágenes, utilidades de backup, etc.).
- DoS: desde reducción de rendimiento hasta interrupción total; puede atacar motores de regex, procesos que consumen recursos o saturar con tráfico.
- Ataques a data y objetos: explotar las reglas de memoria del lenguaje; mass assignment o serialization attacks rompen los límites de formatos comunes.
- Ataques de cliente: tabnabbing, clickjacking y prototype pollution solo tocan el navegador, son difíciles de detectar y pueden desarrollarse offline.
- Explotar dependencias de terceros: usar bases de datos de CVE para encontrar vulnerabilidades conocidas.
- Vulnerabilidades de lógica de negocio: específicas de cada app, difíciles de hallar con herramientas automáticas (SAST, DAST, SCA).

## Defense (defensa)
Puntos clave de la Parte III:
- Arquitectura segura: empieza en la fase de diseño; una vulnerabilidad descubierta aquí puede costar hasta 60 veces menos que en producción, y habilita mitigaciones consistentes para toda la app.
- Configuración segura: aprovechar las funciones de seguridad del stack (JavaScript, DOM, navegador) que solo requieren activarse.
- UX segura: la UI debe fomentar buenas prácticas como MFA y políticas de contraseñas fuertes.
- Threat modeling: estándar de la industria para documentar brechas antes del desarrollo; los problemas hallados aquí son más baratos de resolver.
- Revisión de código: proceso de secure code review similar a un code review normal, pero buscando otro tipo de bugs y priorizando archivos/módulos.
- Descubrimiento de vulnerabilidades: pipeline propio más especialistas externos (bug bounty, pentesters) que incentivan el reporte en vez de la venta en el mercado negro.
- Gestión de vulnerabilidades: reproducir, triar y puntuar por impacto. Existen varios algoritmos de scoring, siendo CVSS el más conocido; lo importante es usar uno de forma consistente.

Defensas por familia de ataque:
- XSS: mitigar en API (sanitización), base de datos y, sobre todo, en el cliente, que es la superficie más importante.
- CSRF: reglas adicionales para peticiones que cambian estado — eliminar GET state-changing, CSRF tokens y confirmación MFA en peticiones de privilegio elevado.
- XXE: los parsers XML modernos permiten desactivar la external entity; considerar también formatos XML-like como SVG, PDF, RTF.
- Injection: en SQL, configuración correcta y prepared statements; en CLI, principio de mínima autoridad (principle of least authority) y separación de concerns.
- DoS: escanear regex por backtracing, limitar acceso a funciones costosas y rate limiting; contra DDoS, empezar en el firewall, blackholing o servicios de gestión de ancho de banda.
- Data y objetos: validación fuerte y especificación de estructura; elegir formatos de datos según sus pros y contras de seguridad.
- Cliente: primero mitigaciones del navegador como CSP; luego JavaScript y DOM con `Object.freeze()` o framebuster scripts.
- Dependencias de terceros: limitar permisos y scope, escanear y revisar antes de integrar, consultar bases de CVE.
- Lógica de negocio: no se hallan con tooling común; ayuda modelar los workflows de usuario y automatizar pruebas de inputs y flujos.

## More to Learn (más por aprender)
El autor cierra recordando que siempre hay más que aprender y que en esta industria "life-long learners excel the most" (PDF p. 458). Los temas de esta segunda edición se eligieron por tres criterios: aplicabilidad a un amplio rango de aplicaciones web, dificultad que escala linealmente con el conocimiento previo del libro, y relación entre temas para que el libro fluya de principio a fin sin saltos ni consultas externas. Su deseo final es que el libro ayude a encontrar y resolver fallos de seguridad y que sea una lectura a la que volver como referencia.

## Ideas clave
- El foco del ataque moderno está en las vulnerabilidades lógicas del código, no tanto en servidores, red o navegador.
- Recon es el primer paso: mapear toda la superficie, incluidas dependencias de terceros, que suelen ser el vector más fácil.
- El libro estructura el conocimiento como ciclo recon → ofensiva → defensa, con una defensa específica para cada familia de ataque.
- Las vulnerabilidades de lógica de negocio escapan a SAST/DAST/SCA y requieren enfoque manual y modelado de workflows.
- La seguridad empieza en la arquitectura: corregir en diseño puede costar hasta 60 veces menos que en producción.
- El cliente (navegador) es la superficie más importante para mitigar XSS y ataques de cliente; CSP es primera línea de defensa.
- Lo esencial de la gestión de vulnerabilidades es usar algún algoritmo de scoring consistente (CVSS es el más conocido), no cuál.
- La seguridad web exige aprendizaje continuo para no quedar obsoleto frente a la evolución de las aplicaciones.
