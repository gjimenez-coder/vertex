# Defending Against DoS (Defensa contra el DoS) — Estudio

## Tarjetas de repaso

P: ¿Por qué el DoS no se trata como una vulnerabilidad binaria como el XSS? / R: Porque el DoS es una cuestión de grado medida por el consumo de recursos (alto/medio/bajo), mientras que con el XSS o tienes un exploit o no lo tienes.

P: ¿Cuál es la primera medida transversal para defenderse del DoS? / R: La observabilidad: un sistema de logging completo que registre todas las peticiones junto a su tiempo de respuesta.

P: ¿Por qué hay que registrar manualmente el rendimiento de los jobs asíncronos? / R: Porque trabajos como un backup lanzado por API corren en segundo plano sin devolver respuesta, y sin registro manual su rendimiento no quedaría reflejado.

P: ¿Qué es un regex DoS sink o "evil regex"? / R: Una expresión regular maliciosa que hace backtracing significativo sobre un grupo repetido, con forma similar a `(a[ab]*)+`.

P: ¿Qué provocan los cuantificadores `+` y `*` en una evil regex? / R: El `+` provoca una coincidencia greedy (busca todas las coincidencias posibles antes de devolver) y el `*` hace coincidir la subexpresión tantas veces como sea posible.

P: ¿Cómo se previene principalmente el regex DoS? / R: Con un proceso de revisión de código adecuado que impida que entren evil regex al codebase, apoyándose en herramientas OSS o un regex performance tester.

P: ¿Qué regla absoluta aplica a las regex suministradas por el usuario? / R: Nunca permitirlas (es "como caminar por un campo minado") y verificar que las integraciones externas tampoco usen regex mal escritas o de usuario.

P: ¿De dónde surge normalmente el DoS lógico? / R: De que los desarrolladores introduzcan por accidente un segmento de lógica abusable que consuma recursos del sistema.

P: ¿Cómo conviene clasificar la funcionalidad expuesta frente al DoS lógico? / R: En términos de riesgo DoS (alto/medio/bajo), no como vulnerable/seguro, llamando "safe" al código extremadamente difícil de explotar.

P: ¿Qué es una botnet? / R: El conjunto de dispositivos comprometidos (robot + network) controlados en masa mediante malware que abre una puerta trasera.

P: ¿Qué dispositivos pueden formar parte de una botnet? / R: No solo PCs, sino también dispositivos móviles e IoT (routers, hotspots, "smart toasters"), a menudo más fácilmente que los equipos de escritorio.

P: ¿Cuál es el objetivo típico de un DDoS frente a un DoS de un solo origen? / R: El DDoS no ataca bugs de lógica, sino que abruma al objetivo con un volumen enorme de tráfico de apariencia legítima.

P: ¿En qué consiste el servicio de gestión de ancho de banda (bandwidth management)? / R: Analiza cada paquete que lo atraviesa con escaneos consolidados y, si detecta un patrón malicioso, no reenvía el paquete al servidor web.

P: ¿Qué es el blackholing? / R: Levantar servidores adicionales de modo que el tráfico sospechoso se envíe a un blackhole server que aparenta funcionar pero no realiza operaciones, mientras el tráfico legítimo va al servidor real.

P: ¿Qué riesgo común tienen todas las mitigaciones agresivas de DoS/DDoS? / R: Que los filtros demasiado sensibles bloqueen también tráfico legítimo, por lo que hay que medir antes los patrones de uso reales.

## Preguntas de autoevaluación

P: ¿Por qué los ataques DoS resultan difíciles de detectar a posteriori? / R: Porque consumen recursos del sistema y pueden entrar por canales legítimos como un endpoint de API. (Lo que necesitas saber)

P: ¿Por qué el regex DoS se considera probablemente la forma de DoS más fácil de defender? / R: Porque con un proceso de revisión de código adecuado puedes impedir que los evil regex entren en el codebase, aunque exige conocer cómo se estructuran los ataques. (Protección contra Regex DoS)

P: ¿Puede una aplicación bien escrita caer en DoS lógico? / R: Sí; aunque los sistemas sin lógica explotable no suelen caer, sigue siendo posible si el atacante dispone de recursos enormes, porque el DoS se mide en una escala y no de forma binaria. (Protección contra DoS lógico)

P: ¿Por qué una misma función puede ser inofensiva en un equipo y explotable en otro? / R: Porque el consumo de recursos depende del dispositivo: puede no notarse en un escritorio potente y sí explotarse en un móvil antiguo. (Protección contra DoS lógico)

P: ¿Por qué el DDoS es por naturaleza más simple que un DoS de un solo origen? / R: Porque el DoS de un único origen suele apuntar a un bug del código (regex mal escrita, API que acapara recursos), mientras que el DDoS solo busca abrumar con volumen de tráfico. (Protección contra DDoS)

P: ¿Por qué el servicio de gestión de ancho de banda es eficaz para aplicaciones pequeñas o de hobby? / R: Porque puede interceptar grandes cantidades de peticiones que la infraestructura de esas aplicaciones no soportaría. (Protección contra DDoS)

P: ¿Ante qué escala de DDoS funciona bien y ante cuál mal el blackholing? / R: Funciona bien contra DDoS pequeños, pero mal contra ataques a gran escala, y si no se apunta con precisión puede desviar también tráfico legítimo. (Protección contra DDoS)

## Checklist

- [ ] Implementar un logging completo que registre todas las peticiones con su tiempo de respuesta.
- [ ] Registrar manualmente el rendimiento de los jobs asíncronos (p. ej., backups lanzados por API).
- [ ] Revisar el código en busca de evil regex con backtracing sobre grupos repetidos como `(a[ab]*)+`.
- [ ] Apoyarse en una herramienta OSS o un regex performance tester para detectar regex peligrosas y reducir falsos positivos.
- [ ] Verificar que no existan puntos donde se use una regex suministrada por el usuario.
- [ ] Comprobar que las integraciones externas no usen regex mal escritas o de usuario.
- [ ] Identificar las áreas del codebase donde se usan recursos críticos del sistema (riesgo de DoS lógico).
- [ ] Clasificar la funcionalidad expuesta por riesgo DoS (alto/medio/bajo) en lugar de vulnerable/seguro.
- [ ] Evaluar un servicio de gestión de ancho de banda como mitigación principal de DDoS.
- [ ] Considerar blackholing para DDoS pequeños, apuntando con precisión para no desviar tráfico legítimo.
- [ ] Medir los patrones de uso de los usuarios legítimos antes de aplicar mitigaciones agresivas.
