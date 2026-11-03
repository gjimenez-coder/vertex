# Conexiones entre libros

Enlaces temáticos entre *Web Application Security* (2nd Edition, Andrew Hoffman) y *AI Under Attack* (Kris Kimmerle & David Okeyode). Solo se incluyen temas con respaldo explícito en los apuntes de ambos libros.

## Inyección (injection / prompt injection)

- Web Application Security: toda inyección necesita un intérprete y un payload sin sanear, de SQL injection a command injection ([cap13](web-application-security/cap13-injection.md)).
- AI Under Attack: la prompt injection explota que los LLM siguen instrucciones y no distinguen las del usuario de las del atacante ([cap06](ai-under-attack/cap06-prompt-injection-and-jailbreaking.md)).
- Conexión: ambos describen la misma causa raíz —mezclar datos no confiables con una capa que los ejecuta o interpreta— pero en web el intérprete es un motor SQL/OS mientras que en IA es el propio modelo de lenguaje, cuyo espacio de entrada infinito impide el saneamiento clásico.

## Defensa frente a la inyección (saneamiento y fronteras de confianza)

- Web Application Security: defiende con prepared statements, least authority y allowlisting en vez de blocklists ([cap31](web-application-security/cap31-defending-against-injection.md)).
- AI Under Attack: defiende con jerarquía de instrucciones y fronteras en el prompt, tratando el contenido externo como evidencia y no como autoridad ([cap15](ai-under-attack/cap15-defensive-prompt-engineering.md)).
- Conexión: los dos separan la intención (código/instrucción) de los datos del usuario; se diferencian en que la frontera de web es determinista (parametrizar) y la de IA es probabilística y nunca una frontera de seguridad completa.

## Modelado de amenazas (threat modeling)

- Web Application Security: construye un threat model con cinco metas, identificación del delta entre vectores y mitigaciones, y threat actors ([cap24](web-application-security/cap24-threat-modeling-applications.md)).
- AI Under Attack: extiende STRIDE/PASTA con amenazas específicas de IA en la intersección de modelo, datos y herramientas ([cap02](ai-under-attack/cap02-threat-modeling-ai-systems.md)).
- Conexión: ambos usan el modelado de amenazas como paso previo al diseño seguro; AI Under Attack parte de las mismas metodologías base y las amplía porque la superficie de IA añade modelo, datos de entrenamiento y herramientas.

## Zero Trust Architecture

- Web Application Security: patrón NIST SP-800-207 que sustituye la confianza implícita por verificación explícita y continua en cada acción privilegiada ([cap21](web-application-security/cap21-secure-application-architecture.md)).
- AI Under Attack: aplica Zero Trust a cada acción del agente para que la autenticación no se trate como permiso para actuar ([cap18](ai-under-attack/cap18-securing-ai-agents-with-zero-trust-architecture.md)).
- Conexión: comparten el mismo principio de verificación continua; AI Under Attack lo instancia en seis preguntas por cada acción del agente, trasladando el patrón de arquitectura web a la autoridad delegada de los agentes.

## Dependencias de terceros y cadena de suministro

- Web Application Security: el OSS es un vector preferente y se evalúa el dependency tree contra bases CVE/NVD ([cap35](web-application-security/cap35-securing-third-party-dependencies.md)).
- AI Under Attack: el riesgo de cadena de suministro entra como artefactos cotidianos (modelos, pesos) con validación por clase de dependencia y uso de SBOM ([cap17](ai-under-attack/cap17-external-dependencies-supply-chain-integrity-and-multi-tenant-risk.md)).
- Conexión: ambos tratan el software/artefacto importado como superficie de ataque gestionada con inventario y bases de vulnerabilidades; se diferencian en que en IA el artefacto peligroso es el propio modelo (pickle vs safetensors) y no solo el paquete de código.

## Defensa en capas (defense in depth)

- Web Application Security: la defensa es un proceso continuo y por etapas, análogo a fortificar un castillo ([cap20](web-application-security/cap20-securing-modern-web-applications.md)).
- AI Under Attack: cuatro pilares (robustness, containment, observability, interpretability) con capas que fallan de forma independiente ([cap04](ai-under-attack/cap04-foundations-of-ai-defense.md)).
- Conexión: los dos rechazan la defensa de un solo control y apuestan por capas redundantes; AI Under Attack añade la contención ("asumir el fallo") como pilar explícito frente al enfoque más preventivo del libro web.

## Abuso de la confianza y autoridad delegada (CSRF / confused deputy)

- Web Application Security: CSRF explota la confianza navegador-usuario-servidor para ejecutar acciones privilegiadas sin que la víctima lo note ([cap11](web-application-security/cap11-cross-site-request-forgery.md)).
- AI Under Attack: el confused deputy usa la autoridad legítima del sistema para un fin no autorizado, persuadiendo al agente de actuar como diputado confundido ([cap10](ai-under-attack/cap10-agent-exploitation-techniques.md)).
- Conexión: ambos ataques no rompen la autenticación sino que abusan de una identidad ya confiable para actuar en nombre de otro; es el mismo patrón de confused deputy sobre el navegador en web y sobre el agente en IA.

## Saneamiento de salida en el DOM (DOMPurify, CSP, Trusted Types)

- Web Application Security: trata los datos como string, sanitiza y usa CSP como primera línea contra XSS ([cap28](web-application-security/cap28-defending-against-xss-attacks.md)).
- AI Under Attack: usa DOMPurify junto con CSP y Trusted Types para no renderizar la salida del modelo en páginas privilegiadas ([cap14](ai-under-attack/cap14-building-secure-ai-applications-and-apis.md)).
- Conexión: comparten exactamente las mismas herramientas de navegador; la diferencia es que en IA la fuente no confiable del XSS es la salida generada por el modelo, tratada con la misma desconfianza que la entrada de un usuario.

## Validación ofensiva: descubrimiento de vulnerabilidades y red teaming

- Web Application Security: combina análisis estático, dinámico y regresión con fuentes externas como bug bounty y pentesting ([cap26](web-application-security/cap26-vulnerability-discovery.md)).
- AI Under Attack: el AI red teaming valida el comportamiento interno del sistema, no solo su cáscara, y mide con evidencia ([cap12](ai-under-attack/cap12-ai-red-teaming-and-evaluation.md)).
- Conexión: ambos buscan activamente los fallos antes que el atacante; se diferencian en que el red teaming de IA debe sondear comportamiento probabilístico y emergente, no solo rutas de código deterministas.

## Marcos de referencia de vulnerabilidades (CVE/CVSS vs OWASP/MITRE ATLAS)

- Web Application Security: usa CVE (Mitre) y el scoring CVSS v3.1 para localizar y puntuar fallos conocidos ([cap27](web-application-security/cap27-vulnerability-management.md)).
- AI Under Attack: usa MITRE ATLAS, OWASP Top 10 for LLMs y NIST AI RMF como capas de mapeo, no como sustituto de la evidencia ([cap12](ai-under-attack/cap12-ai-red-teaming-and-evaluation.md)).
- Conexión: los dos se apoyan en catálogos y marcos públicos para estructurar el riesgo; se diferencian en que los marcos de IA son de mapeo de amenazas emergentes y no un repositorio de vulnerabilidades puntuables como CVE/CVSS.

## Temas exclusivos de cada libro

### Solo en Web Application Security
- Reconocimiento (recon): subdominios, análisis de APIs, fingerprinting, transferencia de zona DNS ([cap02](web-application-security/cap02-introduction-to-web-application-reconnaissance.md), [cap04](web-application-security/cap04-finding-subdomains.md), [cap05](web-application-security/cap05-api-analysis.md)).
- Cross-Site Scripting (stored, reflected, DOM-based, mXSS) ([cap10](web-application-security/cap10-cross-site-scripting.md)).
- XML External Entity (XXE) y su mitigación ([cap12](web-application-security/cap12-xml-external-entity.md), [cap30](web-application-security/cap30-defending-against-xxe.md)).
- Denegación de servicio (ReDoS, DDoS, YoYo attack) y su defensa ([cap14](web-application-security/cap14-denial-of-service.md), [cap32](web-application-security/cap32-defending-against-dos.md)).
- Ataques a datos y objetos: mass assignment, IDOR, serialización ([cap15](web-application-security/cap15-attacking-data-and-objects.md), [cap33](web-application-security/cap33-defending-data-and-objects.md)).
- Ataques del lado del cliente: prototype pollution, clickjacking, tabnabbing ([cap16](web-application-security/cap16-client-side-attacks.md), [cap34](web-application-security/cap34-defense-against-client-side-attacks.md)).
- Vulnerabilidades de lógica de negocio y worst-case design ([cap18](web-application-security/cap18-business-logic-vulnerabilities.md), [cap36](web-application-security/cap36-mitigating-business-logic-vulnerabilities.md)).
- Historia de la seguridad del software ([cap01](web-application-security/cap01-the-history-of-software-security.md)).

### Solo en AI Under Attack
- No-determinismo, comportamiento emergente y alignment drift ([cap01](ai-under-attack/cap01-why-ai-security-is-different.md)).
- Anatomía del stack de IA y sus trust boundaries ([cap05](ai-under-attack/cap05-anatomy-of-an-ai-system.md)).
- Abuso de memoria, contexto y estado (context poisoning, conversation hijacking) ([cap07](ai-under-attack/cap07-memory-context-and-state-abuse.md)).
- Ataques a sistemas RAG (embedding attack, RAG poisoning) ([cap08](ai-under-attack/cap08-attacks-on-rag-systems.md)).
- Arquitectura y explotación de agentes (tool chaining, goal hijacking) ([cap09](ai-under-attack/cap09-agent-architecture-and-vulnerabilities.md), [cap10](ai-under-attack/cap10-agent-exploitation-techniques.md)).
- Ataques a datos de entrenamiento e integridad del modelo (poisoning, backdoors, model extraction) ([cap11](ai-under-attack/cap11-attacks-on-training-data-and-model-integrity.md)).
- Seguridad de infraestructura de IA, MLOps y entornos de ejecución ([cap13](ai-under-attack/cap13-securing-ai-infrastructure-mlops-and-runtime-environments.md)).
- Guardrails y supervisión humana (HITL/HOTL) ([cap16](ai-under-attack/cap16-guardrails-and-human-oversight.md)).
- Gobernanza, riesgo y cumplimiento de la IA (GRC, EU AI Act) ([cap19](ai-under-attack/cap19-ai-governance-risk-and-compliance.md)).
- Operaciones de seguridad de IA y futuro de la disciplina ([cap21](ai-under-attack/cap21-ai-security-operations.md), [cap23](ai-under-attack/cap23-the-future-of-ai-security.md)).
