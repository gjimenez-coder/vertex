# Release It! Design and Deploy Production-Ready Software (2nd Edition) — Michael T. Nygard (The Pragmatic Bookshelf, 2018)
## Capítulo 15 — Case Study: Trampled by Your Own Customers (Caso de estudio: pisoteado por tus propios clientes)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas usan la página del PDF `(PDF p. N)`.

## Lo que necesitas saber

El capítulo narra en primera persona el lanzamiento de un reemplazo completo de la plataforma de comercio electrónico de un minorista: tienda online, gestión de contenidos, atención al cliente y procesamiento de pedidos. Fue un proyecto enorme (más de trescientas personas), ya con más de un año de retraso cuando el autor se unió, y con seis fechas de lanzamiento "oficiales" distintas. El día del "big bang" el sitio recibió 10.000 sesiones a las 9:05, 50.000 a las 9:10 y 250.000 a las 9:30, momento en que colapsó.

La tesis es que un esfuerzo masivo de pruebas de carga puede resultar insuficiente si solo se prueba el "camino feliz". El mundo real es ruidoso: buscadores con URLs viejas, spiders, scrapers, shopbots y tráfico raro generan enormes cantidades de sesiones que las pruebas educadas nunca reprodujeron. Las sesiones son el talón de Aquiles de todo servidor de aplicaciones, porque cada una consume RAM, CPU y ancho de banda.

Sales sabiendo por qué contar "usuarios concurrentes" engaña, por qué hay que meter ruido y caos en las pruebas de carga, por qué el sistema necesita dispositivos de seguridad que corten situaciones malas, y cómo un conjunto de "arreglos temporales" acabó permaneciendo años y costando enormes sumas en ingresos perdidos.

## El ejemplo que recorre el capítulo

El hilo conductor es ese único lanzamiento fallido del minorista y los tres años previos: el aseguramiento de calidad, el mes de pruebas de carga, el colapso del día del lanzamiento y las secuelas. El cambio real lo disparaba la CDN con una actualización de metadatos programada a las 9 a.m. hora central, que tardaba unos ocho minutos en propagarse por todo el mundo; el navegador de la sala de conferencias se saltaba la CDN y pegaba directamente a los "origin servers".

## Aiming for Quality Assurance (Apuntar a la calidad)

No existe tal cosa como un "proyecto de sitio web": todos son en realidad proyectos de integración empresarial con una interfaz HTML. Este era un sitio monolítico sobre una suite de comercio con renderizado 100% del lado servidor. Desarrollar back end y front end a la vez no garantiza mejor integración; depende de la ley de Conway, y lo habitual es que ambos lados apunten a un blanco móvil.

Ley de Conway: "las organizaciones que diseñan sistemas están abocadas a producir diseños cuyas estructuras son copias de las estructuras de comunicación de esas organizaciones" (PDF p. 283). Coloquialmente: cuatro equipos haciendo un compilador producen un compilador de cuatro pasadas. Conway se refiere a la estructura de *comunicación*, no al organigrama formal. El autor la usa de forma prescriptiva (crear la estructura de comunicación que quiere que el software refleje) y descriptiva (mapear el software para entender la comunicación real).

Reemplazar todo el stack de golpe trae mucho riesgo técnico: si no se construye con patrones de estabilidad (este no), la probabilidad de fallo del sistema es la probabilidad conjunta de que falle cualquier componente. El autor descubrió que los equipos construían todo para pasar las pruebas, no para correr en producción: a través de quince aplicaciones y más de quinientos puntos de integración, cada archivo de configuración estaba escrito para el entorno de pruebas de integración. Algunos componentes asumían la topología de QA, que no coincidiría con producción (faltaban firewalls, QA tenía una sola instancia donde producción tendría clústeres). Su solución fue añadir un nivel de indirección: una estructura de *overrides* separada del código, donde cada propiedad que variaba entre entornos existía en exactamente un lugar, manteniendo además las contraseñas de producción fuera de QA y del control de versiones.

## Load Testing (Pruebas de carga)

El cliente reservó un mes entero para pruebas de carga y marketing exigió soportar 25.000 usuarios concurrentes. Contar usuarios concurrentes engaña: la capacidad depende de qué hacen (ver la portada rinde mucho más que comprar). No se pueden medir usuarios concurrentes; solo hay una serie de impulsos discretos que el servidor ata a una *sesión*. Como el servidor no distingue al usuario que no volverá a hacer clic del que aún no lo ha hecho, aplica un *timeout*: la sesión dura más que el usuario, así que contar sesiones sobreestima el número de usuarios.

Las pruebas de carga son arte y ciencia: es imposible duplicar el tráfico real, así que se usa análisis de tráfico, experiencia e intuición. Se montó una llamada permanente con el gestor de pruebas, un ingeniero del servicio de carga, un arquitecto, un DBA y el autor. Los scripts mezclaban "grazers", "searchers" y "buyers": más del 90% veía la portada y una página de detalle; se asignó optimistamente un 4% a completar el checkout (lo más caro: integraciones externas CCVS, normalización de direcciones, inventario, available-to-purchase, hasta doce páginas por sesión frente a siete de quien solo navega).

En la primera prueba el sitio se bloqueó por completo con solo 1.200 usuarios concurrentes; había que multiplicar la capacidad por veinte. Tras tres meses, más de sesenta builds y aventuras varias (las máquinas del load farm fueron hackeadas durante la llamada; un ingeniero de AT&T limitó la subred que generaba el 80% de la carga), lograron multiplicar la capacidad por diez: 12.000 sesiones activas (~10.000 clientes). Marketing rebajó el objetivo: preferían un sitio lento a ningún sitio, y 12.000 sesiones bastarían para la temporada baja.

## Murder by the Masses (Asesinato por las masas)

El número de sesiones mató al sitio. Con replicación de sesión activada, cada sesión se serializaba y transmitía a un servidor de respaldo tras cada página, consumiendo RAM, CPU y ancho de banda. Las fuentes del exceso de sesiones:

- **Buscadores con URLs viejas**: generaban ~40% de las visitas; el día del cambio llevaban a clientes a URLs antiguas que, al reenviarse todas las `.html` a los servidores de aplicaciones, creaban una sesión solo para servir un 404. Además los buscadores refrescaban sus páginas cacheadas.
- **Spidering con IDs en query parameters**: un buscador creaba hasta diez sesiones por segundo, por un mandato del equipo de seguridad de evitar cookies de sesión y usar solo parámetros de consulta (una mala decisión).
- **Scrapers y shopbots**: casi una docena de scrapers de alto volumen, muchos buscadores sectoriales de análisis competitivo, algunos ocultando su origen con subredes variadas y distintos user-agent. No había `robots.txt` y, aunque lo hubiera, no lo respetarían. ARIN puede identificar las IPs como de una misma entidad. Ninguno manejaba cookies, así que cada uno creaba sesiones extra.
- **"Random weird stuff"**: p. ej. un equipo de una base naval que repetía la última URL una y otra vez; lo bloquearon sin entender la causa.

## The Testing Gap (El hueco en las pruebas)

Faltaban dos cosas. Primero, se probó la aplicación como se *supone* que debe usarse: los scripts pedían una URL, esperaban la respuesta y pedían otra presente en la página, siempre con cookies; ninguno golpeaba la misma URL 100 veces por segundo sin cookies. Como con los testers que solo pulsan botones en el orden correcto, hay que añadir ruido y crear caos: el ruido puede solo mermar capacidad o puede tumbar el sistema. Segundo, los desarrolladores no incorporaron dispositivos de seguridad que cortaran situaciones malas; ante un fallo la aplicación seguía enviando hilos a la zona de peligro, que se apilaban sobre los ya rotos o colgados. Lo vieron desde el primer día de pruebas pero lo atribuyeron a la metodología en vez de a una deficiencia del sistema para recuperarse.

## Aftermath (Secuelas)

La CDN añadió una *gateway page* con tres capacidades: redirigir a quien no manejaba cookies a una página explicativa; un *throttle* para decidir qué porcentaje de sesiones nuevas se admitía (empezaron bajo, con un ingeniero vigilando las sesiones; a la tercera semana lo mantenían al 100% todo el día); y bloqueo de IPs específicas de shopbots o avalanchas. Si los servidores se saturaban, tardaban casi una hora en volver a servir páginas, de ahí la importancia del throttle.

La portada se generaba dinámicamente (más de 1.000 transacciones de base de datos y recorrido de ochenta y pico categorías) y se servía cinco millones de veces al día siempre idéntica, sin A/B testing, pese a que la personalización era un argumento clave de la plataforma. Crearon scripts que servían una copia estática de la portada a clientes no identificados. Los términos legales ("al ver esta página ya has aceptado...") sirvieron para enviar notificaciones de cese y desistimiento a los bots. El mecanismo de failover de sesión se basaba en serialización contra un *session backup server*; descubrieron que las sesiones guardaban el carrito completo y hasta 500 resultados de la última búsqueda, así que tuvieron que desactivar el failover.

Temas comunes de la respuesta rápida: nada es tan permanente como un arreglo temporal (los reinicios rotativos duraron una década); todo costó enormemente, sobre todo en ingresos perdidos (clientes throttled, usuarios devueltos al carrito en mitad del checkout, portada estática que impedía personalizar, hardware duplicado, un año de remediación en vez de nuevas funciones). Lo peor: nada de esas pérdidas era necesario. Dos años después el sitio soportaba más de cuatro veces la carga en menos servidores del mismo modelo original; el software mejoró tanto que, de haberse construido así desde el principio, los ingenieros habrían brindado con marketing en lugar de "fundir fusibles".

## Ideas clave

- No existe "proyecto de sitio web": es integración empresarial con interfaz HTML; la ley de Conway determina la calidad de las integraciones.
- Construir para pasar pruebas y no para producción deja configuraciones y topologías que no coinciden; resolverlo con un nivel de indirección (overrides por entorno, una propiedad en un solo lugar).
- Contar usuarios concurrentes engaña; las sesiones duran más que los usuarios y son el talón de Aquiles del servidor de aplicaciones por el consumo de RAM, CPU y red.
- Las pruebas de carga educadas (con cookies, enlaces reales) ocultan el comportamiento del mundo real: buscadores, spiders, scrapers, shopbots y tráfico raro crean sesiones masivas.
- Usar parámetros de consulta para el ID de sesión en lugar de cookies multiplica las sesiones (hasta diez por segundo por un spider).
- Hay que meter ruido y caos en las pruebas y construir dispositivos de seguridad que corten situaciones malas antes de que los hilos se apilen.
- La CDN mitigó con gateway page, throttle de sesiones nuevas y bloqueo de IPs; servir una portada estática a usuarios no identificados alivió la carga.
- Nada es tan permanente como un arreglo temporal, y todos cuestan carísimo en ingresos perdidos y oportunidad; dos años después el mismo hardware soportaba cuatro veces la carga.
