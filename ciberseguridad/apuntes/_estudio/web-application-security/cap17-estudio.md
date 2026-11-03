# Exploiting Third-Party Dependencies (Explotación de dependencias de terceros) — Estudio

## Tarjetas de repaso

P: ¿Cuál es la tesis central del capítulo sobre el OSS?
R: El software moderno depende fuertemente de OSS, y esa dependencia, aunque conveniente, supone un riesgo de seguridad significativo y explotable.

P: ¿Por qué el código OSS representa un eslabón débil?
R: Normalmente no ha sido auditado con el mismo rigor que el código propio, y auditar una gran base de código OSS es poco práctico y muy caro.

P: ¿Qué es BuiltWith y para qué sirve a un atacante?
R: Es una aplicación web que hace fingerprinting de otras webs para determinar su tecnología; permite identificar rápido el stack como primer paso de recon.

P: ¿Qué determina el método de integración de OSS?
R: El tipo de datos que fluye entre ambas partes, el método de transporte y el nivel de privilegio que el código OSS recibe de la aplicación principal.

P: ¿Cuál es el riesgo del modelo de branching?
R: Es fácil incorporar accidentalmente código no revisado de la rama principal a la de producción.

P: ¿Qué ventaja ofrecen los forks frente a las branches?
R: Mayor separación: son repositorios nuevos con sus propios permisos, dueño y Git hooks para evitar merges inseguros.

P: ¿Por qué las integraciones self-hosted con instaladores son el método más arriesgado?
R: Dificultan encontrar vulnerabilidades después, requieren privilegios elevados y pueden derivar fácilmente en un backdoor RCE porque el script suele ejecutarse como admin.

P: ¿Cuándo es ideal la integración a nivel de código fuente (source code integration)?
R: Para scripts cortos de 50–100 líneas o pequeñas utilidades y funciones helper.

P: ¿Qué es un package manager y qué beneficios aporta?
R: Una aplicación intermediaria que garantiza descargar las dependencias correctas desde fuentes fiables; abstrae la integración, reduce el tamaño inicial del repo y trae solo las dependencias necesarias.

P: ¿Qué archivos delatan que una aplicación usa npm?
R: Los archivos `package.json` y `package.lock` en la raíz.

P: ¿Qué ocurrió en el incidente left-pad (2016)?
R: Una utilidad de una página mantenida por una persona fue retirada de npm y rompió el pipeline de millones de aplicaciones; desde entonces npm no permite retirar paquetes tras cierto tiempo.

P: ¿Qué demostró el incidente eslint-scope (2018)?
R: Que las librerías npm pueden ser vectores de ataque: se comprometieron las credenciales del dueño y se publicó una versión que robaba credenciales locales.

P: ¿Cuál es el package manager más popular de Java y quién lo soporta?
R: Maven, soportado por la Apache Software Foundation.

P: ¿Cuál es la vía más rápida de explotar dependencias de terceros?
R: Encontrar vulnerabilidades conocidas aún no parcheadas en dependencias populares y atacarlas.

P: ¿Qué son NVD y la base CVE?
R: La National Vulnerability Database (US Department of Commerce) y la base CVE de Mitre (patrocinada por el US Department of Homeland Security), donde se divulgan públicamente las vulnerabilidades.

## Preguntas de autoevaluación

P: ¿Por qué las empresas asumen el riesgo de usar OSS en lugar de auditarlo a fondo?
R: Porque lo ideal sería evaluar cada pull request entrante, algo que casi ninguna empresa financia por lo caro e impráctico, así que asumen el riesgo de usar software relativamente desconocido. (Sección: Lo que necesitas saber)

P: ¿En qué se diferencian el enfoque centralizado y el descentralizado de integración?
R: El centralizado integra el OSS directamente en el código central de la aplicación; el descentralizado ejecuta el OSS en su propio servidor y expone una API para comunicación unidireccional hacia la integración. (Sección: Métodos de integración)

P: ¿Cuál es la contra principal de usar forks a largo plazo?
R: Fusionar código del repo original se vuelve complejo, requiere cherry-picking cuidadoso y los commits pueden dejar de ser compatibles tras refactorizaciones importantes. (Sección: Branches y forks)

P: ¿Qué desventaja tiene la source code integration frente a los parches upstream?
R: No hay forma fácil de enterarse de los parches upstream, y aplicar ese parche puede ser difícil y lento, especialmente con paquetes grandes. (Sección: Source code integration)

P: ¿Cómo resuelve npm las dependencias y en qué momento?
R: Resuelve tanto dependencias de nivel superior como dependencias hijas recursivas en build time. (Sección: Package managers — JavaScript (npm))

P: ¿Qué técnicas suele requerir atacar vía package manager?
R: Una combinación de social engineering y ofuscación de código, para que el código malicioso quede fuera de la vista pero siga siendo ejecutable. (Sección: Otros lenguajes)

P: ¿Por qué las bases CVE son poco útiles para paquetes pequeños pero valiosas para los grandes?
R: Los paquetes pequeños (p. ej. un repo con dos contribuidores y 300 descargas) apenas tienen vulnerabilidades documentadas; las dependencias grandes como WordPress, Bootstrap o JQuery ya han sido muy escrutadas y tienen fallos reportados con pasos de reproducción y severidad. (Sección: Common Vulnerabilities and Exposures (CVE) Database)

P: Aun con las bases CVE disponibles, ¿qué sigue necesitando el atacante?
R: Recon para identificar las dependencias, cómo se integran, y las versiones y configuraciones que usan. (Sección: Common Vulnerabilities and Exposures (CVE) Database)

## Checklist

Puntos a dominar:

- [ ] Explicar por qué el OSS es un vector de entrada preferente y la metáfora del eslabón más débil.
- [ ] Describir el papel del recon y herramientas de fingerprinting como BuiltWith.
- [ ] Comparar los métodos de integración (branch/fork, self-hosted, código fuente directo, package manager) y sus riesgos de datos, transporte y privilegio.
- [ ] Identificar por qué las integraciones self-hosted con instaladores (WordPress) son las más arriesgadas (privilegios elevados, backdoor RCE).
- [ ] Reconocer archivos y funcionamiento de npm (`package.json`, `package.lock`, resolución recursiva en build time).
- [ ] Recordar los incidentes de npm: left-pad (2016), eslint-scope (2018), event-stream/flatmap-stream (2018).
- [ ] Situar Maven (Apache) y otros package managers (NuGet, Conan, Spack) y sus vectores de ataque.
- [ ] Explicar cómo NVD y la base CVE de Mitre aceleran la explotación de vulnerabilidades conocidas no parcheadas.
- [ ] Recordar la advertencia ética: explotar dependencias requiere permiso escrito explícito del dueño en un escenario de red team.
