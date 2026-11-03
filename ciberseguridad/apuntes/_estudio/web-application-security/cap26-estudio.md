# Vulnerability Discovery (Descubrimiento de vulnerabilidades) — Estudio

## Tarjetas de repaso

P: ¿A qué código apunta el proceso de descubrimiento de vulnerabilidades de este capítulo? / R: Al código en producción, no al de preproducción.

P: ¿Por qué no basta un solo método de descubrimiento? / R: Porque cada técnica tiene su propósito y posición en el ciclo de vida; hay que combinar varias.

P: ¿Cuáles son las tres formas más comunes de automatización de seguridad? / R: Análisis estático, análisis dinámico y pruebas de regresión de vulnerabilidades.

P: ¿Qué tipos de vulnerabilidad NO detecta bien la automatización? / R: Las vulnerabilidades lógicas específicas de la aplicación y las que requieren chaining (varias débiles que juntas producen una fuerte).

P: ¿Qué hace el análisis estático y qué NO hace? / R: Examina el código fuente (sintaxis y errores comunes) sin ejecutarlo; ejecutar el código sería análisis dinámico.

P: ¿Por qué el análisis estático es más fácil en lenguajes tipados estáticamente? / R: Porque la herramienta entiende el tipo de dato esperado y este no cambia al recorrer funciones y clases; en JavaScript las variables son objetos mutables difíciles de analizar sin runtime.

P: ¿Cuáles son las dos limitaciones principales del análisis estático? / R: Genera muchos falsos positivos y sufre con lenguajes dinámicos.

P: ¿Cómo detecta el análisis estático un CSRF? / R: Buscando peticiones GET que cambian estado (state-changing GET requests).

P: ¿Cuándo analiza el código el análisis dinámico y para qué es ideal? / R: Tras ejecutarlo; ideal para lenguajes dinámicos y para vulnerabilidades que son efecto secundario de la operación normal (datos sensibles en memoria, side-channel attacks).

P: ¿Qué trade-off tiene el análisis dinámico frente al estático? / R: Produce menos falsos positivos y mayor introspección, pero cuesta más en mantenimiento, costo y rendimiento, y es más lento.

P: ¿Qué verifica una prueba de regresión de vulnerabilidades? / R: Si una vulnerabilidad conocida sigue existiendo, evitando que el fallo se reintroduzca en el código.

P: ¿En qué se diferencia una prueba de regresión de vulnerabilidad de una funcional? / R: No en el framework, sino en el propósito.

P: ¿Por qué hace falta un programa de divulgación responsable? / R: Porque las pruebas internas no cubren todos los casos de uso de los clientes y los usuarios técnicos no reportarán sin una ruta legal explícita.

P: ¿Qué ofrecen los bug bounty programs que no da la divulgación responsable? / R: Incentivos (premios en efectivo) por reportes correctamente enviados y documentados.

P: ¿Qué ventaja tienen las firmas de pentesting de terceros sobre los bug bounty hunters? / R: Pueden tener asignadas partes concretas de la app y, mediante acuerdos legales, recibir el código fuente para resultados más precisos.

## Preguntas de autoevaluación

P: Según el capítulo, ¿qué relación hay entre arquitectura, revisión de código y número de vulnerabilidades? / R: Las aplicaciones mejor arquitecturadas sufren menos vulnerabilidades y de menor riesgo; tras ellas, las que tienen procesos de revisión de código suficientes sufren menos que las que no los tienen. (Sección: Lo que necesitas saber)

P: ¿Por qué la automatización es esencial aunque no atrape todas las vulnerabilidades? / R: Porque suele ser barata, efectiva y duradera, y encuentra fallos de seguridad rutinarios que se escaparon a arquitectos y revisores. (Sección: Security Automation)

P: Nombra dos exploits detectables mediante análisis estático y cómo. / R: SQL injection, buscando cadenas provistas por el usuario usadas en queries; DOM XSS, buscando sinks específicos del DOM como `setInterval()`. (Sección: Static Analysis)

P: ¿Por qué el análisis dinámico es adecuado para lenguajes dinámicos? / R: Porque observa la salida en vez del flujo de entrada (que es vago), analizando las salidas contra un modelo de vulnerabilidades y malas configuraciones. (Sección: Dynamic Analysis)

P: En el ejemplo de Steve, ¿qué vulnerabilidad aparece y cómo se corrige? / R: Un CSRF, porque un GET state-changing puede dispararse desde un hipervínculo; se corrige cambiando la petición de HTTP GET a HTTP POST. (Sección: Vulnerability Regression Testing)

P: ¿Qué comprueba la prueba de regresión que escribe Steve y cuándo falla? / R: Revisa las HTTP Options del endpoint y falla si acepta más de un verbo o si el verbo no es POST. (Sección: Vulnerability Regression Testing)

P: ¿Qué papel juegan HackerOne y Bugcrowd en los bug bounty programs? / R: Son empresas intermediarias que ofrecen plantillas legales personalizables e interfaz web para envío y triaje, facilitando montar el programa. (Sección: Bug Bounty Programs)

P: ¿Cuándo es ideal contratar pruebas de penetración de terceros? / R: Idealmente apuntan a áreas de alto riesgo y recién escritas antes del release; las pruebas post-release también sirven para áreas de alto riesgo y para verificar consistencia entre plataformas. (Sección: Third-Party Penetration Testing)

## Checklist

- Configurar el análisis estático para buscar las vulnerabilidades comunes del OWASP top 10.
- Ejecutar el análisis estático localmente (linter), bajo demanda contra el repositorio o en cada commit/push a la rama principal.
- Usar más configuración del análisis estático para imponer buenas prácticas: rechazar endpoints de API sin funciones de autorización importadas o funciones que consumen input sin librería de validaciones como única fuente de verdad.
- Preparar un entorno similar a producción (servidores, licencias) antes de aplicar análisis dinámico en aplicaciones grandes.
- Escribir una prueba de regresión por cada vulnerabilidad conocida tras el triaje, usando el framework que reproduzca el fallo (Jest en JavaScript).
- Correr las pruebas de regresión en hooks de commit o push, rechazando si fallan; usar corridas diarias programadas como segunda mejor opción.
- Publicar un programa de divulgación responsable con lista de formas de probar sin riesgo legal, método claro de envío y plantilla de reporte, con posible cláusula de no-publicación durante la corrección.
- Complementar la divulgación responsable con un bug bounty program (p. ej. vía HackerOne o Bugcrowd) para incentivar el reporte.
- Contratar firmas de pentesting de terceros dirigidas a áreas de alto riesgo y recién escritas antes del release, con acuerdos legales que permitan compartir el código fuente.
