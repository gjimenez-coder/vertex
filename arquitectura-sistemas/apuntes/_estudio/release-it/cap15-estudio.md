# Case Study: Trampled by Your Own Customers (Caso de estudio: pisoteado por tus propios clientes) — Estudio

## Tarjetas de repaso

P: ¿Qué sucedió el día del "big bang" del lanzamiento del minorista? / R: El sitio recibió 10.000 sesiones a las 9:05, 50.000 a las 9:10 y 250.000 a las 9:30, momento en que colapsó.

P: Según el capítulo, ¿qué es realmente un "proyecto de sitio web"? / R: No existe tal cosa: todos son proyectos de integración empresarial con una interfaz HTML.

P: ¿Qué enuncia la ley de Conway? / R: Las organizaciones que diseñan sistemas producen diseños cuyas estructuras son copias de las estructuras de comunicación de esas organizaciones (no del organigrama formal).

P: ¿Qué problema encontró el autor en las configuraciones de los equipos? / R: Construían todo para pasar las pruebas, no para producción: cada archivo de configuración estaba escrito para el entorno de pruebas de integración, asumiendo la topología de QA.

P: ¿Cómo resolvió el problema de configuración por entorno? / R: Añadiendo un nivel de indirección: una estructura de overrides separada del código donde cada propiedad que variaba existía en un solo lugar, con las contraseñas de producción fuera de QA y del control de versiones.

P: ¿Por qué engaña contar "usuarios concurrentes"? / R: No se pueden medir usuarios concurrentes; el servidor solo ve impulsos discretos atados a sesiones, y como aplica un timeout, la sesión dura más que el usuario y sobreestima su número.

P: ¿Por qué son las sesiones el talón de Aquiles del servidor de aplicaciones? / R: Porque cada sesión consume RAM, CPU y ancho de banda, y con replicación activada se serializa y transmite a un servidor de respaldo tras cada página.

P: ¿Qué perfiles mezclaban los scripts de prueba de carga? / R: "grazers", "searchers" y "buyers"; más del 90% veía portada y una página de detalle, y un 4% optimista completaba el checkout (lo más caro, hasta doce páginas).

P: ¿Cuáles fueron las fuentes del exceso de sesiones que mató al sitio? / R: Buscadores con URLs viejas (~40% de las visitas), spidering con IDs en query parameters, scrapers y shopbots sin cookies, y "random weird stuff" como una base naval repitiendo una URL.

P: ¿Por qué un spider podía crear hasta diez sesiones por segundo? / R: Porque el equipo de seguridad mandó evitar cookies de sesión y usar solo parámetros de consulta, una mala decisión; al no manejar cookies cada petición creaba una sesión nueva.

P: ¿Cuáles eran las dos cosas que faltaban (el "testing gap")? / R: Probar con ruido/caos en lugar de solo el camino feliz con cookies, y dispositivos de seguridad que cortaran situaciones malas en vez de seguir enviando hilos a la zona de peligro.

P: ¿Qué tres capacidades añadió la gateway page de la CDN? / R: Redirigir a quien no manejaba cookies a una página explicativa, un throttle del porcentaje de sesiones nuevas admitidas, y bloqueo de IPs específicas de shopbots o avalanchas.

P: ¿Qué guardaban las sesiones que obligó a desactivar el failover? / R: El carrito completo y hasta 500 resultados de la última búsqueda, serializados contra un session backup server.

P: ¿Cuál es el tema común sobre los arreglos temporales? / R: Nada es tan permanente como un arreglo temporal; los reinicios rotativos duraron una década y todo costó enormemente, sobre todo en ingresos perdidos.

P: ¿Qué demostró el sitio dos años después? / R: Soportaba más de cuatro veces la carga en menos servidores del mismo modelo original, mostrando que las pérdidas no eran necesarias.

## Preguntas de autoevaluación

P: ¿Por qué un esfuerzo masivo de pruebas de carga puede resultar insuficiente? / R: Porque suele probar solo el "camino feliz" (peticiones educadas con cookies y enlaces reales) y no reproduce el ruido del mundo real: buscadores, spiders, scrapers, shopbots y tráfico raro. (Lo que necesitas saber / The Testing Gap)

P: ¿Qué relación tiene la ley de Conway con la calidad de las integraciones del sistema? / R: La calidad de las integraciones depende de la estructura de comunicación de la organización; desarrollar back end y front end a la vez no garantiza mejor integración si ambos apuntan a un blanco móvil. (Aiming for Quality Assurance)

P: ¿Por qué sobreestima el número de usuarios el conteo de sesiones? / R: Porque el servidor no distingue al usuario que no volverá a hacer clic del que aún no lo ha hecho, y aplica un timeout; así la sesión dura más que el usuario. (Load Testing)

P: ¿Qué resultado dio la primera prueba de carga y cómo evolucionó la capacidad? / R: El sitio se bloqueó con solo 1.200 usuarios concurrentes; tras tres meses y más de sesenta builds lograron multiplicar la capacidad por diez, hasta 12.000 sesiones activas (~10.000 clientes). (Load Testing)

P: ¿Cómo contribuían los buscadores con URLs viejas al colapso? / R: Generaban ~40% de las visitas y llevaban a clientes a URLs antiguas que, al reenviarse todas las .html a los servidores de aplicaciones, creaban una sesión solo para servir un 404, además de refrescar sus páginas cacheadas. (Murder by the Masses)

P: ¿Por qué era crítico el throttle de sesiones nuevas? / R: Porque si los servidores se saturaban tardaban casi una hora en volver a servir páginas, así que convenía admitir solo un porcentaje de sesiones nuevas y vigilarlas. (Aftermath)

P: ¿Qué contradicción había con la portada dinámica del sitio? / R: Se generaba dinámicamente (más de 1.000 transacciones de base de datos y ochenta y pico categorías) y se servía cinco millones de veces al día siempre idéntica, pese a que la personalización era un argumento clave; crearon scripts para servir una copia estática a usuarios no identificados. (Aftermath)

## Checklist

- Tratar el proyecto como una integración empresarial, no como un "proyecto de sitio web", y diseñar la estructura de comunicación según la ley de Conway.
- Separar la configuración del código con un nivel de indirección (overrides por entorno), con cada propiedad variable en un solo lugar y las contraseñas de producción fuera de QA y del control de versiones.
- No contar usuarios concurrentes como medida de capacidad; medir y dimensionar por sesiones considerando su consumo de RAM, CPU y red.
- Incluir ruido y caos en las pruebas de carga: peticiones sin cookies, URLs viejas, misma URL repetida, scrapers y shopbots, no solo el camino feliz.
- Usar cookies para el ID de sesión en lugar de parámetros de consulta, para evitar que spiders multipliquen las sesiones.
- Construir dispositivos de seguridad que corten situaciones malas y eviten apilar hilos sobre los ya rotos o colgados.
- Mitigar con una gateway page: redirección de clientes sin cookies, throttle de sesiones nuevas y bloqueo de IPs de shopbots.
- Servir una copia estática de la portada a clientes no identificados cuando la generación dinámica satura la base de datos.
- Revisar qué guardan las sesiones (carrito, resultados de búsqueda) antes de activar el failover por serialización.
- Tratar los "arreglos temporales" como deuda real: documentarlos y planificar su remediación, porque tienden a volverse permanentes.
