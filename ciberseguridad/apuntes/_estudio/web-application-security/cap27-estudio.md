# Vulnerability Management (Gestión de vulnerabilidades) — Estudio

## Tarjetas de repaso

P: ¿Cuáles son las etapas de la pipeline de gestión de vulnerabilidades?
R: Reproducir → puntuar → triar → corregir con solución permanente → acompañar con un test de regresión.

P: ¿Qué vulnerabilidades no requieren la pipeline de gestión y cómo se defienden?
R: Las de la fase de arquitectura, que pueden defenderse mediante código defensivo y contramedidas antes de escribir código.

P: ¿Cuál es el primer paso tras recibir un reporte de vulnerabilidad?
R: Reproducirla en un entorno tipo producción (staging).

P: ¿Qué beneficios aporta reproducir una vulnerabilidad?
R: Confirmar que es real, evitar perder horas de ingeniería en falsos positivos, evitar pagar bounties por falsos positivos y comprender qué causó el fallo en el código.

P: ¿Qué características debe tener el entorno de staging para reproducir?
R: Imitar producción lo más posible, estar totalmente automatizado, ser accesible solo por red interna o login cifrado y usar mock users y mock objects en vez de usuarios reales.

P: ¿Qué es CVSS y por qué se recomienda como punto de partida?
R: El Common Vulnerability Scoring System, un sistema gratuito y ampliamente disponible para puntuar vulnerabilidades; buen punto de partida para organizaciones con presupuesto limitado o sin ingenieros de seguridad dedicados.

P: ¿En qué tres categorías divide el scoring CVSS v3.1?
R: Base (la vulnerabilidad en sí), Temporal (la severidad a lo largo del tiempo) y Environmental (según el entorno en que existe).

P: ¿Cuáles son las ocho entradas del base score de CVSS v3.1?
R: Attack Vector (AV), Attack Complexity (AC), Privileges Required (PR), User Interaction (UI), Scope (S), Confidentiality (C), Integrity (I) y Availability (A).

P: ¿Qué diferencia hay entre Scope "Unchanged" y "Changed"?
R: "Unchanged" si el ataque solo afecta al sistema local; "Changed" si se propaga fuera de la funcionalidad donde se entrega el payload (p. ej., al sistema operativo o filesystem).

P: ¿Cómo se mapea el número del base score (0–10) a frameworks no numéricos?
R: 0.1–4 low, 4.1–6.9 medium, 7–8.9 high, 9+ critical.

P: ¿Qué mide el temporal score y cuáles son sus tres categorías?
R: La preparación de la organización frente a la vulnerabilidad según su estado al reportarla: Exploitability, Remediation Level y Report Confidence.

P: ¿Qué tres requisitos añade el environmental score sobre el base?
R: Confidentiality Requirement, Integrity Requirement y Availability Requirement.

P: ¿Por qué el scoring no puede ser la única métrica de priorización?
R: Porque también cuentan métricas de negocio como contratos de clientes y relaciones comerciales.

P: ¿Qué debe acompañar siempre a un bug de seguridad cerrado y por qué?
R: Un test de regresión, cuyo valor crece con el tiempo porque las oportunidades de regresión aumentan exponencialmente con el tamaño del código.

## Preguntas de autoevaluación

P: ¿Por qué montar un buen entorno de staging obliga a automatizar el proceso de reproducción?
R: Porque imitar producción lo más posible es difícil, así que el proceso debe estar totalmente automatizado para reproducir con eficiencia. (Sección "Reproducir vulnerabilidades")

P: ¿Qué ejemplo da el libro de un falso positivo que parece vulnerabilidad?
R: Un usuario que por error hace "pública" una imagen que normalmente pondría "privada" en una app de fotos; es un error de configuración del usuario, no un fallo. (Sección "Reproducir vulnerabilidades")

P: ¿Qué limitaciones se le critican a CVSS y para qué funciona bien?
R: Se le critica por no puntuar bien sistemas raros, únicos o vulnerabilidades encadenadas, pero funciona bien como sistema de propósito general para vulnerabilidades comunes (OWASP top 10). (Sección "Common Vulnerability Scoring System (CVSS)")

P: ¿Qué distingue un Attack Complexity Low de uno High?
R: Low si el ataque es repetible sin setup; High si requiere un usuario concreto, en un momento y una página concretos. (Sección "CVSS: Base Scoring")

P: ¿Qué mide el temporal score frente al base score?
R: El temporal mide las mitigaciones disponibles y la calidad/fiabilidad del reporte, no la vulnerabilidad en sí, aunque mantiene el rango 0–10. (Sección "CVSS: Temporal Scoring")

P: ¿Cuándo conviene desarrollar un sistema de scoring propio según el libro?
R: Cuando la aplicación web interactúa con tecnología física (p. ej., una cámara de seguridad controlada por portal web o dispositivos IoT), por implicaciones adicionales como filtrar vídeos sensibles. (Sección "Scoring avanzado")

P: ¿Qué nunca se debe hacer al aplicar un fix parcial?
R: Nunca enviar un fix parcial y cerrar el bug sin antes abrir otro que detalle los fixes restantes y su score apropiado. (Sección "Más allá del triaje y el scoring")

## Puntos a dominar

- Entender la pipeline completa: reproducir → puntuar → triar → corregir → test de regresión.
- Saber por qué se reproduce primero (validar, evitar falsos positivos y bounties indebidos, entender la causa) y cómo debe ser el staging (automatizado, mock users/objects, acceso interno o cifrado).
- Conocer las tres capas de CVSS v3.1 (base, temporal, environmental) y que lo más usado es el base score.
- Dominar las ocho entradas del base score (AV, AC, PR, UI, Scope, C, I, A) y el mapeo 0–10 a low/medium/high/critical.
- Distinguir qué mide cada capa: base (la vulnerabilidad), temporal (madurez de mitigaciones y calidad del reporte), environmental (ajuste al contexto propio).
- Recordar que el scoring prioriza pero debe combinarse con métricas de negocio (contratos, relaciones).
- Preferir fixes permanentes de toda la superficie; si solo hay fix parcial, abrir un bug nuevo antes de cerrar el anterior.
- Asociar siempre un test de regresión a cada bug de seguridad cerrado.
