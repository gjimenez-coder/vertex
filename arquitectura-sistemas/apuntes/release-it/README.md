# Release It! Design and Deploy Production-Ready Software (2nd Edition)

Autor: Michael T. Nygard (The Pragmatic Bookshelf, 2018)

Estos apuntes recorren cómo diseñar y desplegar sistemas distribuidos para las condiciones hostiles del mundo real, donde el software está bajo ataque desde el momento en que se libera. El libro parte de que los fallos son inevitables y de que "feature complete" no equivale a "production ready": la meta no es pasar QA, sino sobrevivir a la vida en producción. Cuatro bloques estructuran el material —estabilidad, diseño para producción, entrega y problemas sistémicos— y se apoyan en casos de estudio basados en incidentes reales, con cifras de coste conservadas para subrayar que hay dinero real en juego.

## Capítulos

- [Capítulo 0 — Prólogo (Preface)](cap00-preface.md): presenta el propósito del libro: diseñar y desplegar sistemas distribuidos para el "lodo y el fango" del mundo real, donde el software estará bajo ataque desde su liberación.
- [Capítulo 1 — Living in Production (Vivir en producción)](cap01-living-in-production.md): que un sistema esté "feature complete" no significa que esté listo para producción; el diseño debe atender también lo que el sistema no debe hacer.
- [Capítulo 2 — Case Study: The Exception That Grounded an Airline (La excepción que dejó en tierra a una aerolínea)](cap02-case-study-the-exception-that-grounded-an-airline.md): un único `SQLException` no capturado provocó un efecto dominó que paralizó a una aerolínea durante horas.
- [Capítulo 3 — Stabilize Your System (Estabiliza tu sistema)](cap03-stabilize-your-system.md): el software empresarial debe ser cínico, esperar fallos y levantar barreras internas para que una grieta no se propague por la malla de sistemas.
- [Capítulo 4 — Stability Antipatterns (Antipatrones de estabilidad)](cap04-stability-antipatterns.md): cataloga los antipatrones que crean, aceleran o multiplican las grietas que derriban un sistema, empezando por los Integration Points.
- [Capítulo 5 — Stability Patterns (Patrones de estabilidad)](cap05-stability-patterns.md): presenta patrones (Circuit Breaker, Timeouts, Bulkheads, etc.) que reducen o mitigan el daño de las grietas que se propagan.
- [Capítulo 6 — Case Study: Phenomenal Cosmic Powers, Itty-Bitty Living Space (Poderes cósmicos fenomenales, un espacio diminuto para vivir)](cap06-case-study-phenomenal-cosmic-powers-itty-bitty-living-space.md): una tienda online recién lanzada se cae en Black Friday; la visibilidad y el reinicio de componentes individuales marcan la diferencia.
- [Capítulo 7 — Foundations (Fundamentos)](cap07-foundations.md): abre el "diseño para producción" tratando red, logging, monitorización, control y seguridad como preocupaciones de primera clase.
- [Capítulo 8 — Processes on Machines (Procesos en las máquinas)](cap08-processes-on-machines.md): baja al nivel de la instancia individual, que debe ser un "buen ciudadano": transparente, controlable, bien configurada y capaz de gestionar conexiones.
- [Capítulo 9 — Interconnect (Interconexión)](cap09-interconnect.md): la capa donde se construye la alta disponibilidad mediante gestión de tráfico, balanceo de carga y descubrimiento de servicios.
- [Capítulo 10 — Control Plane (Plano de control)](cap10-control-plane.md): define el control plane como el software que gestiona otro software, y sus implicaciones de automatización, transparencia y configuración.
- [Capítulo 11 — Security (Seguridad)](cap11-security.md): la seguridad debe integrarse desde el diseño; repasa inyección, gestión de sesiones, XSS, mínimo privilegio y gestión de secretos.
- [Capítulo 12 — Case Study: Waiting for Godot (Esperando a Godot)](cap12-case-study-waiting-for-godot.md): una noche de despliegue manual y ritualizado muestra lo caro e improductivo que es poner código en producción sin automatización.
- [Capítulo 13 — Design for Deployment (Diseñar para el despliegue)](cap13-design-for-deployment.md): el despliegue es una feature más del software y debe diseñarse buscando zero downtime desde la aplicación.
- [Capítulo 14 — Handling Versions (Manejo de versiones)](cap14-handling-versions.md): cómo cambiar la forma en que el software habla con el mundo sin romper a los consumidores, respetando su autonomía.
- [Capítulo 15 — Case Study: Trampled by Your Own Customers (Pisoteado por tus propios clientes)](cap15-case-study-trampled-by-your-own-customers.md): un lanzamiento "big bang" de comercio electrónico colapsa bajo cientos de miles de sesiones; las sesiones, no los usuarios, son el talón de Aquiles.
- [Capítulo 16 — Adaptation (Adaptación)](cap16-adaptation.md): el cambio está garantizado pero la supervivencia no; hay que diseñar la adaptación en personas, procesos, herramientas y arquitectura.
- [Capítulo 17 — Chaos Engineering (Ingeniería del caos)](cap17-chaos-engineering.md): la disciplina de experimentar sobre un sistema distribuido en producción para construir confianza en su capacidad de resistir condiciones turbulentas.
