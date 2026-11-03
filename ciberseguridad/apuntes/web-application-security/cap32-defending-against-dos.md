# Web Application Security (2nd Edition) — Andrew Hoffman (O'Reilly Media, 2024)
## Capítulo 32 — Defending Against DoS (Defensa contra el DoS)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas indican la página del PDF.

## Lo que necesitas saber
Este capítulo cierra el estudio del DoS mostrando cómo defenderse de sus distintas variantes. La tesis es que el DoS no es una vulnerabilidad binaria como el XSS, sino una cuestión de grado medida por el consumo de recursos; por eso detectarlo y prevenirlo exige estrategias distintas según el tipo de ataque.

El primer requisito transversal es la observabilidad. Como los ataques DoS consumen recursos del sistema y pueden entrar por canales legítimos (como un endpoint de API), resultan difíciles de detectar a posteriori. La primera medida debe ser un sistema de logging completo que registre todas las peticiones junto a su tiempo de respuesta, incluyendo manualmente el rendimiento de trabajos asíncronos tipo "job" (por ejemplo, un backup lanzado por API que corre en segundo plano sin devolver respuesta).

Sales sabiendo cómo mitigar las cuatro familias de amenaza DoS recordadas del Capítulo 14 (agotar recursos del servidor, agotar recursos del cliente, solicitar recursos no disponibles y denegar acceso a recursos) y, en concreto, cómo defenderte del regex DoS, el DoS lógico y el DDoS, entendiendo que cada uno requiere un enfoque diferente y que algunas contramedidas pueden afectar también a los usuarios legítimos.

## Protección contra Regex DoS
Es probablemente la forma de DoS más fácil de defender, pero exige conocer cómo se estructuran los ataques. Con un proceso de revisión de código adecuado puedes impedir que entren en el codebase los *regex DoS sinks* (expresiones regulares maliciosas o "evil regex").

- Hay que buscar regex que hagan *backtracing* significativo sobre un grupo repetido, con forma similar a `(a[ab]*)+`, donde `+` provoca una coincidencia *greedy* (busca todas las coincidencias posibles antes de devolver) y `*` hace coincidir la subexpresión tantas veces como sea posible.
- Distinguir regex peligrosas de las inofensivas construidas sobre la misma tecnología es difícil y genera falsos positivos; aquí resulta útil una herramienta OSS que escanee las expresiones regulares o un *regex performance tester* para comprobar entradas manualmente.
- Segundo paso: asegurarse de que no haya puntos donde se use una regex suministrada por el usuario. Permitir regex subidas por el usuario es "como caminar por un campo minado" (PDF p. 415); hay que verificar también que las integraciones externas no usen regex mal escritas o de usuario.

## Protección contra DoS lógico
El DoS lógico es mucho más difícil de detectar y prevenir que el regex DoS. Como aquel, normalmente no es explotable salvo que los desarrolladores introduzcan por accidente un segmento de lógica abusable que consuma recursos del sistema.

Los sistemas sin lógica explotable no suelen caer en DoS lógico, pero sigue siendo posible: el DoS se mide en una escala, no de forma binaria, y una app bien escrita podría caer si el atacante dispone de recursos enormes. Por eso conviene pensar la funcionalidad expuesta en términos de riesgo DoS (alto/medio/bajo) en lugar de vulnerable/seguro, como sí ocurre con el XSS, que es completamente binario: "Either you have an XSS exploit or you do not. Period." (PDF p. 415).

Una misma función puede no notarse en un escritorio potente y sí explotarse en un móvil antiguo. Se llama "safe" al código extremadamente difícil de explotar y "vulnerable" a las otras dos categorías, pecando de cautos. Para protegerse hay que identificar las áreas del codebase donde se usan recursos críticos del sistema.

## Protección contra DDoS
Los ataques de denegación de servicio distribuida (DDoS) son mucho más difíciles de defender que los de un único atacante. Mientras el DoS de un solo origen suele apuntar a un bug del código (regex mal escrita, llamada de API que acapara recursos), el DDoS es por naturaleza más simple.

- La mayoría de DDoS en la web se originan en múltiples fuentes controladas desde un punto central: un atacante o grupo distribuye malware que corre en segundo plano en PCs legítimos (a veces empaquetado con un programa legítimo) y abre una puerta trasera para controlarlos en masa.
- No solo los PCs son vulnerables: también dispositivos móviles e IoT (routers, hotspots, "smart toasters"), a menudo más fácilmente que los equipos de escritorio.
- El conjunto de dispositivos comprometidos se denomina *botnet* (robot + network).
- El DDoS no suele atacar bugs de lógica, sino abrumar al objetivo con un volumen enorme de tráfico de apariencia legítima, dejando fuera a los usuarios reales o degradando mucho su experiencia.

Los DDoS no se pueden prevenir, pero sí mitigar:

- **Servicio de gestión de ancho de banda (bandwidth management):** la vía más sencilla. El servicio analiza cada paquete que lo atraviesa con escaneos consolidados; si detecta un patrón malicioso, no reenvía el paquete a tu servidor web. Es eficaz porque puede interceptar grandes cantidades de peticiones que la infraestructura de aplicaciones pequeñas o de hobby no soportaría.
- **Blackholing:** se levantan servidores adicionales junto al servidor principal (Figura 32-1). El tráfico sospechoso o repetido se envía a un *blackhole server* que aparenta funcionar como el servidor de aplicación pero no realiza operaciones; el tráfico legítimo va al servidor real. Si no se apunta con precisión, puede desviar también tráfico legítimo. Funciona bien contra DDoS pequeños, pero mal contra ataques a gran escala.

Con cualquiera de estas técnicas, los filtros demasiado sensibles bloquearán también tráfico legítimo, así que conviene tener métricas profundas de los patrones de uso de los usuarios legítimos antes de aplicar mitigaciones agresivas.

## Ideas clave
- El DoS es una cuestión de grado (alto/medio/bajo), no binaria como el XSS; evalúa la funcionalidad por riesgo de consumo de recursos.
- Un logging completo con tiempos de respuesta, incluyendo jobs asíncronos, es la primera defensa para detectar DoS, incluso pasados.
- El regex DoS se previene con revisión de código buscando regex con backtracing sobre grupos repetidos como `(a[ab]*)+`, apoyándote en herramientas OSS.
- Nunca permitas regex suministradas por el usuario ni dependas de integraciones que lo hagan.
- El DoS lógico surge de lógica accidental que consume recursos críticos; identifica esas áreas del codebase.
- El DDoS proviene de botnets (PCs, móviles e IoT comprometidos) que abruman con tráfico de apariencia legítima.
- El DDoS no se previene, pero se mitiga con servicios de gestión de ancho de banda y con blackholing (mejor contra ataques pequeños).
- Toda mitigación agresiva puede bloquear usuarios legítimos: mide primero los patrones de uso reales.
