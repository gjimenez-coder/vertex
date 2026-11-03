# Web Application Security (2nd Edition) — Andrew Hoffman (O'Reilly Media, 2024)

Libro de seguridad de aplicaciones web que enseña tanto las técnicas ofensivas como las defensivas, con una proporción casi 1:1 de capítulos de ataque y de defensa. Su tesis es que para asegurar una aplicación web primero hay que entender cómo piensan y actúan los hackers. Prioriza conceptos a bajo nivel ("bajo el capó") frente a herramientas concretas, usa JavaScript en los ejemplos por ser el único lenguaje del cliente, y se organiza en tres partes: reconocimiento (recon), ofensiva (offense) y defensa (defense). Recorre la aplicación web moderna como un conjunto de aplicaciones simbióticas comunicadas por red, cada capa de las cuales amplía la superficie de ataque, y usa el banco ficticio MegaBank como ejemplo hilo conductor.

## Capítulos

- [Capítulo 0 — Prólogo (Preface)](cap00-preface.md): presenta el libro, su enfoque ofensiva/defensa 1:1 y los requisitos de nivel para decidir si es para ti.
- [Capítulo 1 — La historia de la seguridad del software](cap01-the-history-of-software-security.md): recorre un siglo de la relación cíclica entre hackers e ingenieros, del Enigma a la Web 2.0.
- [Capítulo 2 — Introducción al reconocimiento de aplicaciones web](cap02-introduction-to-web-application-reconnaissance.md): el recon como fase previa al hackeo para mapear una aplicación más allá de su UI pública.
- [Capítulo 3 — La estructura de una aplicación web moderna](cap03-the-structure-of-a-modern-web-application.md): las tecnologías del stack moderno y por qué cada capa amplía la superficie de ataque.
- [Capítulo 4 — Encontrar subdominios](cap04-finding-subdomains.md): técnicas para descubrir los subdominios que dan vida a una aplicación, de las simples a la fuerza bruta.
- [Capítulo 5 — Análisis de APIs](cap05-api-analysis.md): descubrir endpoints, enumerar verbos HTTP, reconocer autenticación y deducir la forma del payload.
- [Capítulo 6 — Identificando dependencias de terceros](cap06-identifying-third-party-dependencies.md): detectar frameworks de cliente/servidor y la base de datos para ligarlos a CVE conocidos.
- [Capítulo 7 — Identificación de puntos débiles en la arquitectura de la aplicación](cap07-identifying-weak-points-in-application-architecture.md): unir el recon para priorizar ataques, partiendo de que la mala arquitectura origina más vulnerabilidades.
- [Capítulo 8 — Resumen de la Parte I](cap08-part-i-summary.md): cierre de síntesis del recon como disciplina viva que evoluciona constantemente.
- [Capítulo 9 — Introducción al hacking de aplicaciones web](cap09-introduction-to-hacking-web-applications.md): abre la Parte II con la mentalidad del hacker y el puente entre recon y ofensiva.
- [Capítulo 10 — Cross-Site Scripting](cap10-cross-site-scripting.md): el XSS (stored, reflected y DOM-based) y sus variantes avanzadas como mXSS y la evasión de filtros.
- [Capítulo 11 — Cross-Site Request Forgery](cap11-cross-site-request-forgery.md): CSRF explota la confianza navegador-usuario-servidor para ejecutar acciones privilegiadas sin que la víctima lo note.
- [Capítulo 12 — Entidad externa XML](cap12-xml-external-entity.md): XXE explota parsers XML mal configurados para comprometer archivos del servidor y llegar al account takeover.
- [Capítulo 13 — Inyección](cap13-injection.md): todo ataque de inyección necesita un intérprete y un payload sin sanear; de SQL injection a command injection.
- [Capítulo 14 — Denegación de servicio](cap14-denial-of-service.md): el DoS como cualquier esfuerzo automatizado que degrada la usabilidad, del regex DoS al DDoS.
- [Capítulo 15 — Atacando datos y objetos](cap15-attacking-data-and-objects.md): abusar de los objetos como first-class citizens mediante mass assignment, IDOR y ataques de serialización.
- [Capítulo 16 — Ataques del lado del cliente](cap16-client-side-attacks.md): ataques que no requieren servidor vulnerable: prototype pollution, clickjacking y tabnabbing.
- [Capítulo 17 — Explotación de dependencias de terceros](cap17-exploiting-third-party-dependencies.md): el OSS como vector preferente y el uso de bases NVD/CVE para localizar fallos conocidos sin parchear.
- [Capítulo 18 — Vulnerabilidades de lógica de negocio](cap18-business-logic-vulnerabilities.md): fallos únicos de cada aplicación en la implementación de sus reglas de negocio, difíciles de detectar pero de alto impacto.
- [Capítulo 19 — Resumen de la Parte II](cap19-part-ii-summary.md): cierre de la ofensiva: arquetipos + pensamiento crítico + conocimiento del dominio.
- [Capítulo 20 — Asegurando aplicaciones web modernas](cap20-securing-modern-web-applications.md): abre la defensa con el proceso continuo y por etapas, análogo a fortificar un castillo.
- [Capítulo 21 — Arquitectura de aplicaciones segura](cap21-secure-application-architecture.md): la fase de arquitectura como el punto más barato para corregir vulnerabilidades, hasta Zero Trust Architecture.
- [Capítulo 22 — Configuración segura de la aplicación](cap22-secure-application-configuration.md): configurar las protecciones del navegador: CSP, CORS, cabeceras de seguridad, cookies y sandboxing.
- [Capítulo 23 — Experiencia de usuario segura](cap23-secure-user-experience.md): cómo las decisiones de diseño de UX introducen o mitigan riesgos como information disclosure y enumeration.
- [Capítulo 24 — Modelado de amenazas de aplicaciones](cap24-threat-modeling-applications.md): construir un threat model efectivo con sus cinco metas y la identificación del delta.
- [Capítulo 25 — Revisión de código en busca de seguridad](cap25-reviewing-code-for-security.md): revisar código como segundo paso tras la arquitectura, con un catálogo de anti-patrones.
- [Capítulo 26 — Descubrimiento de vulnerabilidades](cap26-vulnerability-discovery.md): combinar análisis estático, dinámico y regresión con fuentes externas como bug bounty y pentesting.
- [Capítulo 27 — Gestión de vulnerabilidades](cap27-vulnerability-management.md): la pipeline de reproducir, puntuar (CVSS), triar y corregir con test de regresión.
- [Capítulo 28 — Defensa contra ataques XSS](cap28-defending-against-xss-attacks.md): tratar datos de usuario como string, sanitizar, evitar sinks del DOM y usar CSP como primera línea.
- [Capítulo 29 — Defensa contra ataques CSRF](cap29-defending-against-csrf-attacks.md): defensa por capas con verificación de cabeceras, tokens anti-CSRF y middleware centralizado.
- [Capítulo 30 — Defensa contra XXE](cap30-defending-against-xxe.md): deshabilitar las external entities del parser o migrar a otro formato de datos como JSON.
- [Capítulo 31 — Defendiéndose contra la inyección](cap31-defending-against-injection.md): prepared statements, defensas por motor y principios genéricos como least authority y allowlisting.
- [Capítulo 32 — Defensa contra el DoS](cap32-defending-against-dos.md): el DoS como cuestión de grado; observabilidad y mitigaciones por tipo (regex, lógico, DDoS).
- [Capítulo 33 — Defendiendo datos y objetos](cap33-defending-data-and-objects.md): mitigar mass assignment, IDOR y serialización con allowlists, DTO y librerías auditadas.
- [Capítulo 34 — Defensa contra ataques del lado del cliente](cap34-defense-against-client-side-attacks.md): mitigar prototype pollution, clickjacking y tabnabbing mediante configuración del navegador.
- [Capítulo 35 — Protegiendo las dependencias de terceros](cap35-securing-third-party-dependencies.md): evaluar el dependency tree contra bases de CVE, separar responsabilidades y gestionar paquetes.
- [Capítulo 36 — Mitigación de vulnerabilidades de lógica de negocio](cap36-mitigating-business-logic-vulnerabilities.md): worst-case design, modelado estadístico con fuzzing y análisis de resultados.
- [Capítulo 37 — Resumen de la Parte III](cap37-part-iii-summary.md): cierre de la defensa distinguiendo mitigaciones perecederas de filosofías y patrones perdurables.
- [Capítulo 38 — Conclusión](cap38-conclusion.md): repaso del ciclo recon-ofensiva-defensa y del desplazamiento del foco hacia las vulnerabilidades lógicas del código.
