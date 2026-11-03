# Release It! Design and Deploy Production-Ready Software (2nd Edition) — Michael T. Nygard (The Pragmatic Bookshelf, 2018)
## Capítulo 12 — Case Study: Waiting for Godot (Caso de estudio: Esperando a Godot)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF y las citas usan la página del PDF.

## Lo que necesitas saber

Este capítulo es una viñeta narrativa, no un tratado técnico: el autor relata en primera persona una noche de despliegue de un sistema grande y antiguo para mostrar lo doloroso, caro e improductivo que puede llegar a ser poner código en producción cuando el proceso es manual y ritualizado. La tesis es que "no basta con escribir el código; nada está hecho hasta que corre en producción" (PDF p. 244), y que el camino a producción, en sistemas viejos, suele ser un camino de tierra lleno de baches, bandidos y controles fronterizos.

Sales sabiendo que existe un antipatrón —el "ejército de despliegue" (deployment army)— y por qué aparece: cuanto más tiempo lleva viviendo tu software en producción, más probable es tenerlo. El capítulo funciona como gancho emocional y económico para los capítulos siguientes, donde se analizarán las fuerzas que llevan a este antipatrón y cómo salir del "pozo de la desesperación" haciendo los despliegues más rápidos y rutinarios.

## El ejemplo que recorre el capítulo

El hilo conductor es una única noche de despliegue. Son las 1:17 a.m. y el autor siente que el tiempo se ha detenido, como en una película de cine negro. Más de veinte personas están alrededor de una mesa de conferencias con la cabeza inclinada sobre sus laptops, y otras tantas están conectadas por un puente de conferencia desde cuatro lugares del mundo. En total, el despliegue consumirá a más de cuarenta personas durante un periodo de 24 horas. El equipo "B" se ha ido a dormir para estar fresco y arreglar los problemas que queden por la mañana: es una fila explícita del playbook, porque un error de operador se achacó una vez a la fatiga.

El relato avanza siguiendo el reloj de Lamport del playbook (el tiempo lógico del proceso) frente al reloj solar de la pared, y termina mal: el despliegue falla la UAT y hay que hacer rollback alrededor de las 5 a.m. Esa misma tarde empiezan a planear el segundo intento, programado para dos días después.

## El playbook y el proceso ritualizado

El despliegue se gobierna con un playbook, un guion fila por fila que marca qué ocurre y cuándo. Puntos destacados del relato:

- El proceso tiene su propio "proceso para actualizar el proceso": dos días antes empiezan a revisar y actualizar el playbook. El comandante del despliegue (release commander) recorre cada fila y el equipo confirma o actualiza cada paso para esa versión concreta. Cada reunión de revisión dura dos o tres horas.
- La tarde anterior arrancó la primera fila con rondas de informes de estado de cada área: dev, QA, content, merchants, order management, etc.
- Hubo una reunión de go/no-go a las 3 p.m. Todos dieron luz verde, aunque QA avisó de que no había terminado de probar y podía aún aparecer un problema bloqueante (showstopper).
- Tras el go/no-go, un correo avisó a los stakeholders de negocio: su señal para irse a casa, cenar a las cuatro de la tarde, dormir y levantarse a la 1 a.m. para hacer el "smoke test" de las funciones nuevas. Esa es la ventana de UAT: de 1 a 3 a.m.
- El playbook incluye monitorizar unos números en una gráfica porque en una versión de hace un par de años esos números fueron en la dirección equivocada; el código causante se reescribió hace tiempo, pero el paso sigue ahí. Como dice el autor, "no hay nada que hacer" (Nothing to be done).

## El trabajo de Sys Ops

El autor es Sys Ops. El término "DevOps" aún no existirá hasta un año después "y en una galaxia distinta a esa sala de conferencias". Su turno llega cuando el comandante pide actualizar los symlinks. Entonces pulsa Enter en una ventana de PuTTY conectada al jumphost, la única máquina desde la que las demás aceptan conexiones SSH. Su script hace tres cosas en cada máquina:

- actualiza un enlace simbólico para que apunte al nuevo code drop,
- ejecuta el precompilador de JSP,
- y arranca los procesos de servidor.

Otro script había colocado el código en los servidores horas antes.

## El coste y el contraste con Etsy

Aburrido, el autor hace cuentas en una servilleta y luego una hoja de cálculo: el tamaño del "ejército" por un día. Suponiendo unos 100 dólares por hora y persona, más algunas ventas perdidas mientras el sitio está "de pesca" (pero no muchas, porque están offline en una franja de poca actividad), el despliegue cuesta alrededor de 100.000 dólares. Y lo hacen entre cuatro y seis veces al año.

Años después presencia un despliegue en la tienda online Etsy: un inversor de visita pulsa, como parte rutinaria, el botón del "deployinator". El inversor parece contento pero no impresionado, mientras el autor siente una histeria contenida y, a la vez, una profunda sensación de pérdida por todo ese tiempo en el ejército de despliegue: potencial desperdiciado, humanidad malgastada, personas usadas como si fueran bots, con sus vidas, familias y patrones de sueño alterados.

## Por qué falló

El despliegue falló la UAT por una causa clásica: una función había pasado QA porque los datos del entorno de QA no coincidían con los de producción. Producción tenía contenido extra con JavaScript que reescribía parte de una página de un tercero, y eso no funcionó con la nueva estructura de página. Hubo rollback de madrugada. (El autor bromea: "párame si ya has oído esta antes".)

## Ideas clave

- Nada está hecho hasta que corre en producción; en sistemas antiguos el camino a producción suele ser penoso.
- El "ejército de despliegue" (deployment army) es un antipatrón: cuanto más viejo es el software, más probable resulta.
- Los despliegues manuales y ritualizados consumen decenas de personas durante 24 horas y pueden costar del orden de 100.000 dólares cada uno, varias veces al año.
- El playbook crece con pasos defensivos que ya no tienen sentido (monitorizar números cuyo código causante se reescribió) y añade reglas por experiencias pasadas (el equipo "B" duerme para evitar errores por fatiga).
- La divergencia entre el entorno de QA y producción (datos y contenido distintos) es una causa recurrente de fallos en UAT.
- Automatizar y rutinizar el despliegue (como el "deployinator" de Etsy) tiene beneficio financiero inmediato y desencadena un círculo virtuoso.
- Lo mejor de todo: dejar de desperdiciar potencial humano en trabajos que deberían ser scripts.
