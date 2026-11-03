# Conclusion (Conclusión) — Estudio

## Tarjetas de repaso

P: ¿Hacia dónde se ha desplazado el foco de los atacantes en las aplicaciones web modernas?
R: Desde las vulnerabilidades en servidores, protocolos de red o navegadores hacia las vulnerabilidades lógicas del código de aplicación.

P: ¿Por qué hoy es más valiosa la colaboración entre desarrolladores y expertos en seguridad que la contribución individual?
R: Porque las aplicaciones web modernas son grandes, distribuidas y dependen fuertemente de terceros.

P: ¿Cómo responde Bell Labs al phreaking telefónico y qué lo elimina finalmente?
R: Introduce el sistema DTMF (dual-tone multifrequency), más difícil de reproducir, y las centrales digitales eliminan finalmente el riesgo (el DTMF permaneció por retrocompatibilidad).

P: ¿Qué hizo el Morris Worm y cómo terminó Robert Morris?
R: Fue el primer virus desplegado fuera del laboratorio, se propagó a unas 15.000 computadoras en un día; Morris fue el primer hacker condenado, con multa de $10.500 y 400 horas de servicio comunitario.

P: ¿Qué es el recon y para qué sirve tanto al atacante como al dueño de la aplicación?
R: Es mapear la aplicación y evaluar cada componente en busca de riesgos; al atacante le sirve para priorizar ataques y evitar detección, y al dueño para priorizar defensas.

P: ¿Por qué las dependencias de terceros son un vector atractivo?
R: Están tan presentes como el código propio o más y no se auditan al mismo estándar; mediante fingerprinting se detectan versiones vulnerables de servidores, frameworks cliente, frameworks CSS y bases de datos.

P: ¿Qué explota el CSRF y qué considerar si las peticiones GET que cambian estado ya están filtradas?
R: Explota la relación de confianza entre navegador y usuario; si las GET state-changing ya están filtradas, conviene considerar web forms.

P: ¿Por qué las vulnerabilidades de lógica de negocio son difíciles de detectar?
R: Son específicas de cada aplicación y escapan a herramientas automáticas como SAST, DAST y SCA, requiriendo enfoque manual y modelado de workflows.

P: ¿Cuánto puede costar menos corregir una vulnerabilidad descubierta en la fase de diseño?
R: Hasta 60 veces menos que si se descubre en producción, y además habilita mitigaciones consistentes para toda la app.

P: ¿Cuál es la superficie más importante para mitigar XSS y qué defensa es primera línea en ataques de cliente?
R: El cliente (navegador) es la superficie más importante para mitigar XSS; CSP es la primera línea de defensa en ataques de cliente.

P: ¿Qué defensas se recomiendan contra injection en SQL y en CLI?
R: En SQL, configuración correcta y prepared statements; en CLI, principio de mínima autoridad (principle of least authority) y separación de concerns.

P: ¿Qué es lo esencial de la gestión de vulnerabilidades respecto al scoring?
R: Usar algún algoritmo de scoring de forma consistente (CVSS es el más conocido), más que cuál se elija.

## Preguntas de autoevaluación

P: ¿Qué sintetiza la conclusión y qué estructura de aprendizaje refuerza?
R: Repasa los puntos clave de recon, ofensiva y defensa sin introducir material nuevo, reforzando el ciclo recon → ofensiva → defensa con una defensa específica por familia de ataque. (Lo que necesitas saber)

P: ¿Cómo cambió la transición de la Web 1.0 a la Web 2.0 el panorama de ataque?
R: La Web 1.0 abrió ataques contra servidores y redes; la Web 2.0 (colaboración usuario-a-usuario sobre HTTP) convirtió al navegador en nuevo vector de ataque. (Historia de la seguridad del software)

P: ¿Por qué el XXE puede filtrar archivos del servidor y cómo se mitiga en parsers modernos?
R: Una debilidad de la especificación XML lo permite (de forma directa o indirecta); los parsers XML modernos permiten desactivar la external entity, y hay que considerar formatos XML-like como SVG, PDF, RTF. (Offense / Defense)

P: ¿Qué defensas adicionales aplican a las peticiones CSRF que cambian estado?
R: Eliminar las GET state-changing, usar CSRF tokens y pedir confirmación MFA en peticiones de privilegio elevado. (Defense)

P: ¿Cómo se defiende frente a DoS y DDoS según el apunte?
R: Contra DoS: escanear regex por backtracing, limitar acceso a funciones costosas y rate limiting; contra DDoS: empezar en el firewall, blackholing o servicios de gestión de ancho de banda. (Defense)

P: ¿Qué tres criterios guiaron la elección de temas de la segunda edición?
R: Aplicabilidad a un amplio rango de aplicaciones web, dificultad que escala linealmente con el conocimiento previo del libro, y relación entre temas para que el libro fluya sin saltos ni consultas externas. (More to Learn)

P: ¿Por qué el autor insiste en el aprendizaje continuo?
R: Porque la seguridad web evoluciona y quien no refresca su conocimiento corre el riesgo de quedar obsoleto; en esta industria "life-long learners excel the most". (More to Learn / Ideas clave)

## Puntos a dominar

- El foco del ataque moderno está en las vulnerabilidades lógicas del código, no tanto en servidores, red o navegador.
- El ciclo recon → ofensiva → defensa y la defensa específica que corresponde a cada familia de ataque (XSS, CSRF, XXE, injection, DoS, data/objetos, cliente, terceros, lógica de negocio).
- El recon abarca toda la superficie: subdominios, APIs, HTTP, arquitectura y dependencias de terceros detectables por fingerprinting.
- La seguridad empieza en la arquitectura: corregir en diseño puede costar hasta 60 veces menos que en producción.
- El cliente (navegador) es la superficie más importante para mitigar XSS; CSP es primera línea de defensa.
- Las vulnerabilidades de lógica de negocio escapan a SAST/DAST/SCA y requieren modelado de workflows y pruebas automatizadas de inputs y flujos.
- Usar un algoritmo de scoring de vulnerabilidades de forma consistente (CVSS es el más conocido).
