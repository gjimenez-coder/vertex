# Caso de estudio: poderes cósmicos fenomenales, un espacio diminuto para vivir — Estudio

## Tarjetas de repaso

P: ¿Qué incidente recorre todo el capítulo? / R: Durante Acción de Gracias y el Black Friday, una tienda online recién lanzada se cayó por completo mientras perdía alrededor de un millón de dólares de ingresos por hora.

P: ¿Cuál es la tesis central del capítulo? / R: Los fallos en producción son inevitables; lo que marca la diferencia es la visibilidad sobre el interior del sistema y la capacidad de reconfigurar y reiniciar componentes individuales sin reiniciar el mundo entero.

P: ¿Por qué importa tanto la temporada navideña para un minorista? / R: Hasta el 50 por ciento de los ingresos anuales ocurre entre el 1 de noviembre y el 31 de diciembre, y Acción de Gracias es el inicio de facto de la temporada.

P: ¿Cómo "tomaba el pulso" el autor al sitio? / R: Con módulos Perl que hacían screen-scraping de la GUI de administración HTML del servidor de aplicaciones, leyendo y fijando propiedades e invocando métodos sobre los componentes.

P: ¿Por qué un GUI no bastaba para operar el sitio? / R: Sirve para explorar cuando no sabes qué buscas, pero se vuelve impracticable ante treinta o cuarenta servidores.

P: ¿Qué son los DRPs en el vocabulario del sitio ATG? / R: Instancias que sirven páginas; el servidor web llama al servidor de aplicaciones vía Dynamo Request Protocol (DRP), de ahí el nombre. "Todos los DRPs en rojo" significa sitio caído.

P: ¿Cuáles eran los signos vitales durante el incidente? / R: Conteos de sesión muy altos, ancho de banda alto sin tope, latencia de página alta, CPU muy baja en web/app/base de datos, búsqueda respondiendo bien y casi todos los hilos de atención ocupados más de cinco segundos.

P: ¿Por qué el tiempo de respuesta es un indicador rezagado? / R: Solo puedes medir las peticiones que terminan; las que nunca completaban no entraban en la media, así que la latencia era efectivamente infinita.

P: ¿Qué mostraban los thread dumps del front-end? / R: Unos pocos hilos llamando al back-end y la mayoría bloqueados esperando una conexión libre en una pila de recursos sin timeout, que nunca se liberaba si el back-end dejaba de responder.

P: ¿Por qué la cadena de sistemas colapsó entera? / R: Los tamaños dispares encadenados (3.000 hilos → 450 hilos → 25 hilos) hacen que el eslabón más pequeño, el servidor de scheduling, derribe todo el sistema.

P: ¿Qué estado tenía el sistema de scheduling de entrega a domicilio? / R: De cuatro servidores, dos en mantenimiento y uno fallando; el único restante (25 hilos) soportaba unas 25 peticiones concurrentes pero recibía unas 90, al 100 por ciento de CPU.

P: ¿Qué permitió throttlear las llamadas de scheduling? / R: El código usaba una subclase de la resource pool estándar con un connection pool separado solo para scheduling (probable ley de Conway); ese componente pudo usarse como throttle.

P: ¿Por qué fijar `max` a cero no cambió nada al principio? / R: Porque `max` solo surte efecto al arrancar la pila; hubo que invocar `stopService()` y `startService()` para que el cambio tuviera efecto.

P: ¿Qué es Recovery-Oriented Computing (ROC)? / R: Una investigación conjunta de Berkeley y Stanford que acepta que los fallos son inevitables y busca mejorar la supervivencia frente a ellos en vez de solo eliminar sus causas.

P: ¿Cuánto redujo la recuperación reiniciar componentes en vez de servidores enteros? / R: Reconfigurar servidores completos habría tardado más de seis horas bajo esa carga; reconfigurar solo el connection pool tardó menos de cinco minutos.

## Preguntas de autoevaluación

P: ¿Con qué actitud encaraba el autor la temporada y en qué se basaba? / R: Con "optimismo cauteloso": casi habían duplicado los servidores en producción, tenían datos de estabilidad bajo carga y mayor visibilidad y control del interior de la tienda que en cualquier otro sistema. (El ejemplo que recorre el capítulo)

P: ¿Por qué una CPU muy baja con casi todos los hilos ocupados era reveladora? / R: Es la firma de un bloqueo esperando en un integration point, no de sobrecarga de cómputo: los 3.000 hilos estaban atados sin hacer nada esperando conexiones libres. (Vital Signs / Diagnostic Tests)

P: ¿Qué fallo humano amplificó el incidente y por qué ocurrió? / R: El ingeniero de guardia ignoró avisos de CPU alta porque los falsos positivos repetidos lo habían entrenado para ignorar esa condición; además marketing anunció entrega gratis sin playbook. (Call In a Specialist)

P: ¿Cómo se consiguió que un DRP deshabilitara la entrega a domicilio de forma controlada? / R: Una pila de recursos con máximo cero queda deshabilitada; al devolver null en vez de conexión, el código mostraba un mensaje cortés de que el scheduling no estaba disponible. (Compare Treatment Options)

P: ¿Qué problema surgió al recuperar el primer DRP y cómo se afrontó? / R: Al ser el único respondiendo, el load manager le mandó todo el tráfico y quedó aplastado; aun así había estrategia para extender la solución al resto. (Does the Condition Respond to Treatment?)

P: ¿Por qué ROC parecía adelantado en 2005 y natural hoy? / R: En 2005 iba por delante de su tiempo; hoy parece natural con microservicios, contenedores y escalado elástico, donde reiniciar componentes individuales es habitual. (Recovery-Oriented Computing)

P: ¿Cómo se gestionó el connection pool durante el resto del fin de semana? / R: El autor escribió un script que fijaba `max`, paraba y reiniciaba el servicio con un comando; el business sponsor pidió subirlo con carga ligera y bajarlo a uno (no a cero) con carga alta. (Winding Down)

## Puntos a dominar

- La pila de recursos (connection pool) sin timeout como mecanismo que propaga un fallo del back-end y agota la capacidad del front-end.
- La lectura de signos vitales: sesiones, ancho de banda, latencia, CPU y estado de los hilos, y por qué el tiempo de respuesta es un indicador rezagado.
- El diagnóstico con thread dumps para localizar hilos bloqueados esperando en un integration point.
- El efecto de los tamaños dispares encadenados (3.000 → 450 → 25 hilos) sobre la resiliencia global.
- El riesgo de que los falsos positivos entrenen a los operadores para ignorar alertas reales.
- El uso de un connection pool separado como throttle y la necesidad de `stopService()`/`startService()` para aplicar cambios de `max`.
- Los principios de Recovery-Oriented Computing: fallos inevitables, modelado incompleto, acción humana como fuente de fallos y foco en la supervivencia.
- El valor de reiniciar componentes en vez de servidores enteros para recuperar en minutos en lugar de horas.
