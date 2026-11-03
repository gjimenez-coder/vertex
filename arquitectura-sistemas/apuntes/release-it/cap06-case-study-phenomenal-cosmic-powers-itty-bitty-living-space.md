# Release It! Design and Deploy Production-Ready Software (2nd Edition) — Michael T. Nygard (The Pragmatic Bookshelf, 2018)
## Capítulo 6 — Case Study: Phenomenal Cosmic Powers, Itty-Bitty Living Space (Caso de estudio: poderes cósmicos fenomenales, un espacio diminuto para vivir)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas usan la página del PDF `(PDF p. N)`.

## Lo que necesitas saber
Este capítulo es un caso de estudio narrado en primera persona: el autor cuenta cómo, durante el fin de semana de Acción de Gracias y el Black Friday, una tienda online recién lanzada se cayó por completo mientras perdía ingresos a razón de alrededor de un millón de dólares por hora. La tesis central es que los fallos en producción son inevitables y que lo que marca la diferencia entre un desastre y una recuperación es la visibilidad sobre el interior del sistema y la capacidad de reconfigurar y reiniciar componentes individuales sin reiniciar el mundo entero.

Sales sabiendo cómo una cadena de sistemas de tamaños muy dispares (un front-end enorme llamando a un sistema mediano que a su vez llamaba a un sistema diminuto) puede colapsar por una pila de recursos sin timeout, y cómo un diagnóstico disciplinado —thread dumps, signos vitales, herramientas propias— permitió improvisar un throttle sobre la marcha. El capítulo introduce además el proyecto Recovery-Oriented Computing (ROC) como marco conceptual de fondo.

## El ejemplo que recorre el capítulo
El hilo conductor es un único incidente real. El autor había lanzado una tienda online en verano y encaraba la temporada navideña con "optimismo cauteloso": casi habían duplicado los servidores en producción, tenían datos de estabilidad bajo carga y una visibilidad y control del interior de la tienda mayores que en cualquier otro sistema en el que había trabajado. El relato va desde la preparación hasta la caída y la recuperación.

## Baby's First Christmas / Taking the Pulse
El contexto comercial: hasta el 50 por ciento de los ingresos anuales de un minorista ocurre entre el 1 de noviembre y el 31 de diciembre, y Acción de Gracias es el inicio de facto de la temporada. El tráfico en tiendas físicas puede cuadruplicarse de la noche a la mañana y el de las tiendas online aumentar un 1.000 por ciento: "este es el verdadero test de carga, el único que importa".

Para "tomar el pulso" al sitio, el autor escribió una colección de módulos Perl que hacían screen-scraping de la GUI de administración HTML del servidor de aplicaciones, parseando los valores. Como toda la GUI era HTML, el servidor nunca distinguía un módulo Perl de un navegador. Con ellos podía leer y fijar propiedades e invocar métodos sobre los componentes. Clave del aprendizaje: un GUI sirve para explorar cuando no sabes qué buscas, pero se vuelve impracticable ante treinta o cuarenta servidores. El equipo había aprendido el ritmo normal del sitio observando esas estadísticas; "nada supera el poder de reconocimiento de patrones del cerebro humano".

## Thanksgiving Day / Black Friday
El día de Acción de Gracias el sitio aguantó: para medianoche habían tomado tantos pedidos como en todo octubre, con la latencia de página estresada pero nominal y estable. Pasó el primer test de carga asesino. El Black Friday, el autor salió a comprar y, estando lejos de su punto de acceso, recibió la llamada de Daniel desde el site operations center (SOC): SiteScope en rojo en todos los DRPs, reinicios rolling fallando de inmediato.

Vocabulario del sitio ATG: las peticiones de página las atienden instancias que solo sirven páginas; el servidor web llama al servidor de aplicaciones vía Dynamo Request Protocol (DRP), por lo que a esas instancias se les llama DRPs. "Todos los DRPs en rojo" significaba sitio caído. Un reinicio rolling de todos los servidores de un host tarda unos diez minutos; se pueden hacer cuatro o cinco hosts a la vez, no más, o la base de datos se resiente.

## Vital Signs
Veinte minutos dentro del incidente se sabía: conteos de sesión muy altos; ancho de banda alto pero sin tope; latencia de página del servidor de aplicaciones alta; uso de CPU de web, aplicación y base de datos muy bajo; los servidores de búsqueda (el culpable habitual) respondían bien; casi todos los hilos de atención de peticiones ocupados, muchos llevando más de cinco segundos.

Aprendizaje sobre métricas: el tiempo de respuesta es siempre un indicador rezagado; solo puedes medir las peticiones que terminan, así que las que nunca completaban no entraban en la media. La latencia no era solo alta: era efectivamente infinita.

## Diagnostic Tests
Los thread dumps del front-end mostraban el patrón: unos pocos hilos llamando al back-end y la mayoría esperando una conexión libre para llamar al back-end. Los hilos bloqueados esperaban en una pila de recursos (resource pool) sin timeout. Si el back-end dejaba de responder, los hilos que llamaban nunca volvían y los bloqueados nunca tenían su turno. Los 3.000 hilos de atención, en los 100 DRPs, estaban atados sin hacer nada: eso explicaba la CPU baja.

El order management system (6 hosts, 6 instancias, 450 hilos) mostraba lo mismo: algunos hilos llamando a un integration point externo —el sistema de scheduling de entrega a domicilio— y el resto bloqueados esperando. Ese sistema lo gestionaba otro grupo sin soporte 24/7, con un busca por turnos.

## Call In a Specialist
De los cuatro servidores de scheduling, dos estaban en mantenimiento ese fin de semana y uno fallaba por razones desconocidas. El único servidor que quedaba (1 host, 1 instancia, 25 hilos) soportaba unas 25 peticiones concurrentes antes de colgarse, y estaba recibiendo unas 90. Estaba al 100 por ciento de CPU. El ingeniero de guardia había recibido avisos pero los ignoró: los falsos positivos de CPU alta los habían entrenado para ignorar esa condición. Para colmo, marketing había publicado un anuncio ofreciendo entrega a domicilio gratis para todos los pedidos online antes del lunes. Era el escenario de pesadilla, sin playbook: había que improvisar.

## Compare Treatment Options
La única salida era dejar de hacer tantas peticiones de disponibilidad de horario; había que throttlear las llamadas, pero el order management system no podía hacerlo. El código de la tienda usaba una subclase de la resource pool estándar, con un connection pool separado solo para las peticiones de scheduling (probablemente un ejemplo de la ley de Conway), y eso salvó el fin de semana: ese componente podía usarse como throttle. Una pila de recursos con máximo cero queda efectivamente deshabilitada; si devolvía null en vez de una conexión, el código mostraba al usuario un mensaje cortés de que el scheduling de entregas no estaba disponible.

## Does the Condition Respond to Treatment?
Fijar `max` a cero y `checkoutBlockTime` a cero en un DRP no cambió nada, porque `max` solo surte efecto al arrancar la pila. Entonces el autor invocó `stopService()` y `startService()` del componente y ese DRP volvió a atender peticiones. Pero al ser el único respondiendo, el load manager le mandó todo el tráfico y quedó aplastado. Aun así, había estrategia.

## Recovery-Oriented Computing
El proyecto Recovery-Oriented Computing (ROC) fue una investigación conjunta de Berkeley y Stanford. Sus principios fundacionales: los fallos son inevitables en hardware y software; el modelado y el análisis nunca pueden ser completos y no se pueden predecir a priori todos los modos de fallo; la acción humana es una fuente mayor de fallos del sistema. A diferencia del trabajo clásico centrado en eliminar las causas de fallo, ROC acepta que los fallos ocurrirán y busca mejorar la supervivencia frente a ellos. En 2005 era adelantado a su tiempo; hoy parece natural con microservicios, contenedores y escalado elástico.

El autor aplicó sus scripts a todos los DRPs, fijando `max` y `checkoutBlockTime` a cero y reciclando el servicio. Poder reiniciar componentes en vez de servidores enteros es clave en ROC: reconfigurar y reiniciar los servidores completos habría tardado más de seis horas bajo esa carga; reconfigurar solo el connection pool tardó menos de cinco minutos. Unos 90 segundos después los DRPs pasaron a verde en SiteScope.

## Winding Down
El autor escribió un script que ajustaba el máximo del connection pool con un solo comando (fijaba `max`, paraba el servicio y lo reiniciaba), de modo que un ingeniero en el SOC o en el "command post" pudiera cambiar las conexiones máximas. Se usó constantemente durante el fin de semana: como poner el máximo a cero deshabilitaba del todo la entrega a domicilio, el business sponsor pidió subirlo con carga ligera y bajarlo a uno (no a cero) con carga alta.

## Ideas clave
- Una pila de recursos (connection pool) sin timeout propaga un fallo del back-end: los hilos quedan bloqueados para siempre y agotan toda la capacidad del front-end.
- CPU muy baja con casi todos los hilos ocupados es la firma de un bloqueo esperando en un integration point, no de sobrecarga de cómputo.
- El tiempo de respuesta es un indicador rezagado: solo mides lo que completa, así que lo peor queda invisible en las medias.
- Los tamaños dispares encadenados (3.000 hilos → 450 hilos → 25 hilos) hacen que el eslabón más pequeño derribe todo el sistema.
- Los falsos positivos repetidos entrenan a los operadores para ignorar alertas reales.
- Tener herramientas propias para leer y fijar propiedades e invocar métodos en componentes dio la visibilidad y el control que permitieron improvisar un throttle.
- Reiniciar componentes en vez de servidores enteros (idea central de ROC) redujo la recuperación de seis horas a menos de cinco minutos.
- ROC parte de que los fallos son inevitables y busca supervivencia, no solo prevención.
