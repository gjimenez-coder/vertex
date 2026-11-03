# Release It! Design and Deploy Production-Ready Software (2nd Edition) — Michael T. Nygard (The Pragmatic Bookshelf, 2018)
## Capítulo 13 — Design for Deployment (Diseñar para el despliegue)

> Nota de extracción: el texto se obtuvo de la capa de texto del PDF; las citas usan la página del PDF `(PDF p. N)`.

## Lo que necesitas saber

El capítulo parte de la premisa central del libro: la versión 1.0 es el comienzo de la vida del sistema, no el final, así que habrá muchísimos despliegues a producción. Por eso el despliegue debe tratarse como una *feature* más del software y diseñarse desde la aplicación, en lugar de dejárselo a operaciones. El objetivo explícito es el despliegue sin interrupciones (zero downtime).

Nygard ataca "la falacia del tiempo de inactividad planificado": para el usuario, el downtime es downtime, da igual el correo interno que se haya enviado. El problema de fondo es que solemos diseñar solo para el estado *después* de una versión, asumiendo un salto cuántico instantáneo. En realidad la actualización lleva tiempo y el usuario ve el sistema en el estado "durante". La solución es diseñar aplicaciones que colaboren con su propio despliegue a lo largo de ese lapso.

El capítulo aborda tres grandes preocupaciones: automatización, orquestación y despliegue sin interrupciones. Sales sabiendo cómo funciona un *build pipeline*, la diferencia entre infraestructura mutable (convergencia) e inmutable, las fases de un despliegue (preparación, rollout, limpieza) y cómo evolucionar esquemas relacionales, bases de datos *schemaless* y *assets* web sin tumbar el servicio.

## Tantas máquinas (So Many Machines)

Nygard usa "máquina" como sinónimo genérico de "instancia configurable de sistema operativo" (metal físico, VM, contenedor o unikernel). Un *service* es una interfaz invocable, siempre compuesta de copias redundantes de software en varias máquinas. Hoy hay más formas de ejecutar software en producción que nunca y, por tanto, más máquinas (sobre todo virtuales): hablamos de mascotas (pets) y ganado (cattle), pero por su vida efímera algunas merecen llamarse "efímeras" (mayflies). Esa complejidad debe devolvernos algo: mayor disponibilidad durante los despliegues.

## Despliegues automatizados (Automated Deployments)

La primera herramienta es el *build pipeline*, que arranca tras un *commit* y es, en esencia, un servidor de integración continua (CI) crecido. Empieza como CI (pruebas unitarias, análisis estático, compilación) pero no se detiene en el informe y el *archive*: continúa hasta desplegar en producción, pasando por despliegue en un entorno de prueba, scripts de migración y pruebas de integración.

> "We call it a build pipeline, but it's more like a build funnel." (PDF p. 249)

Cada etapa busca motivos para rechazar la build (pruebas fallidas, *lint*, integración, *archive* sospechoso). Productos habituales: Jenkins (el más común), GoCD de Thoughtworks, Spinnaker de Netflix y AWS Code Pipeline. Consejo: no caer en la trampa del análisis buscando "la mejor" herramienta; elegir una que sirva y dominarla.

Al final del pipeline entra la gestión de configuración. Estas herramientas comparten rasgos: se declara el estado final deseado en archivos de texto versionables (no las acciones concretas, como haría un shell script), y la herramienta calcula qué hacer para que la máquina coincida. El mapeo de configuración a hosts puede ser **manual** (el operador asigna roles) o **automático** (el operador pide "X réplicas del servicio Y en estas ubicaciones" y la plataforma PaaS lo cumple combinando capacidad y restricciones).

Dos estilos de empaquetado:

- **Convergencia**: se arranca una imagen mínima y scripts reutilizables instalan paquetes, crean usuarios, generan archivos desde plantillas e instalan la build. La herramienta examina el estado actual y planifica cómo llegar al deseado, respetando dependencias entre pasos.
- **Infraestructura inmutable**: la unidad de empaquetado es una imagen de VM o contenedor, construida por el pipeline y registrada en la plataforma (p. ej. AMIs de Amazon, que leen "user data" al arrancar). Siempre se parte de un estado conocido (la imagen base), así que debería tener éxito siempre; para cambiar, se reconstruye y se borra la máquina vieja.

Los partidarios de la inmutabilidad argumentan que la convergencia nunca funciona: máquinas longevas acumulan estado irreparable o no contemplado por las recetas (parámetros del kernel, timeouts TCP). En resumen: la inmutabilidad es para el ganado y se alinea con IaaS/PaaS y mapeo automático; la convergencia es para las mascotas y predomina en despliegues físicos y VMs longevas.

## Despliegue continuo (Continuous Deployment)

Entre el *commit* y la ejecución en producción, el código es pura responsabilidad: inventario sin terminar, con bugs desconocidos. El despliegue continuo busca minimizar ese retraso. Existe un círculo vicioso: a mayor demora, más cambios se acumulan por despliegue, mayor riesgo; la reacción natural de añadir revisiones alarga aún más la demora y agrava el riesgo. La única salida es el lema "If it hurts, do it more often", que en el límite significa ejecutar el pipeline completo en cada commit.

La variación aparece al final del pipeline: algunos equipos disparan el despliegue a producción de forma automática; otros ponen una etapa de "pausa" con aprobación humana. Ambas son válidas según el contexto: si el coste de ir lento supera al del error, inclínate por lo automático; en entornos críticos o muy regulados, por la revisión humana (con un "pulsador de botón" autorizado disponible siempre, incluso para un cambio de urgencia a las 2 a.m.).

## Fases del despliegue (Phases of Deployment)

El despliegue continuo surgió primero en empresas que usaban PHP, donde desplegar es casi copiar archivos. En el otro extremo están las aplicaciones Java/C# enormes con cachés en memoria y pools de conexiones que tardan en copiarse y reiniciarse. Cuanto mayor el grano del empaquetado (archivos < archives < máquinas completas), más tarda en aplicarse y activarse; hay que tenerlo en cuenta al planear un rollout por tandas.

Entran en juego dos escalas de tiempo: la **microscópica** (una instancia) y la **macroscópica** (todo el rollout). A nivel micro importan cuatro lapsos:

1. **Preparar** el cambio (copiar archivos para un symlink, o desplegar la nueva imagen).
2. **Drenar** (drain) la actividad tras dejar de aceptar peticiones: segundos en un microservicio sin estado, pero muy largo con sesiones pegajosas (sticky). Los hilos bloqueados también atascan el drenaje.
3. **Aplicar** el cambio (rápido si es un symlink; en infraestructura desechable se solapa con el drenaje).
4. **Arrancar** hasta estar listo para recibir carga: más que el tiempo de inicio, incluye calentar cachés y JIT y establecer conexiones. Enviar carga antes provoca errores o latencias enormes.

A nivel macro, la preparación abarca todo lo que puede hacerse sin perturbar la versión vigente (p. ej. publicar contenido y assets nuevos con rutas/URLs nuevas).

## Esquemas de bases de datos relacionales (Relational Database Schemata)

Los cambios de esquema son un motor del "downtime planificado". Base imprescindible: un *framework* de migraciones (p. ej. Liquibase) que permita avanzar y retroceder versiones del esquema de forma programática. Pero el framework no garantiza compatibilidad hacia atrás y hacia adelante: hay que separar los cambios en **expansión** y **limpieza**.

La **fase de expansión** incluye cambios seguros de aplicar antes de desplegar el código (todos *añaden* algo y nada lo usa la app actual): añadir tablas, vistas, columnas *nullable*, alias/sinónimos, stored procedures, triggers, y copiar datos a tablas/columnas nuevas. Cuidado con los triggers: solo son seguros si son incondicionales y no lanzan errores.

Los triggers permiten crear **shims**: en carpintería, una cuña que rellena un hueco; en despliegues, código que une la versión vieja y la nueva. Al dividir una tabla, durante el rollout unas instancias usan la tabla nueva y otras la vieja, de modo que un dato escrito en la vieja justo antes de apagarse podría perderse. Un trigger INSERT en la tabla vieja lo replica en la nueva, y un UPDATE en la nueva actualiza la vieja; típicamente hacen falta shims para insert, update y delete en ambos sentidos, evitando bucles infinitos. Media docena de shims por cambio es mucho trabajo: ese es el precio de agrupar cambios en una versión. Hay que probarlos con una muestra realista de datos de producción (incluidos NULLs y registros de hace una década que la app actual ya no podría generar).

## Bases de datos sin esquema (Schemaless Databases)

Una base *schemaless* solo lo es para el motor; la aplicación sí espera estructura. ¿Funcionarán *todos* los documentos antiguos con la versión nueva? Puede haber documentos convertidos en "bombas de tiempo" que hoy ya no se pueden leer. Tres enfoques:

1. **Translation pipeline**: la app lee cualquier versión jamás creada; cada nueva versión de documento añade un traductor al final (V1→V2→…→actual). Si el formato se dividió, el pipeline también se bifurca. Coste: muchas permutaciones a probar y tiempo de traducción creciente.
2. **Migración durante el despliegue**: funciona mientras los datos son pequeños. La app debe leer versión nueva y vieja. Con rollout y migración concurrentes hay cuatro escenarios; solo falla el nº 4 (instancia vieja lee documento nuevo), así que conviene desplegar la versión de la app *antes* de migrar los datos.
3. **"Trickle, then batch"** (el preferido del autor): código condicional que migra cada documento al tocarlo, amortizando el coste entre peticiones; después, una migración por lotes (batch) sobre los documentos no tocados, segura porque ya no quedan instancias viejas. Al terminar, se despliega una versión que elimina el chequeo condicional. Restricción: no tener dos migraciones *trickle* solapadas sobre el mismo tipo de documento. No se limita a schemaless; sirve para cualquier migración grande.

## Assets web (Web Assets)

Las versiones de los assets de front-end (imágenes, hojas de estilo, JavaScript) están hoy muy acopladas a los cambios de back-end. Tres preocupaciones: *cache-busting*, versionado y afinidad de sesión.

Los assets estáticos deben tener cabeceras de expiración muy lejanas (diez años es razonable). Al desplegar, el *cache busting* fuerza al navegador y a los proxies intermedios a traer la versión nueva. Hay librerías que añaden un *query string*; Nygard prefiere usar el SHA del commit de git e incorporar la versión en la URL o el nombre de archivo (no en el query string), para tener versiones vieja y nueva en directorios distintos.

```html
<link rel="stylesheet" href="/a5019c6f/styles/app.css"/>
<script src="/a5019c6f/js/login.js"></script>
```

Advertencia: el consejo de versionar y luego reescribir la URL para eliminar la versión asume un *big bang* con cambio instantáneo y no sirve. Si app y assets salen del mismo servidor, el navegador puede pedir la página a una instancia nueva y el asset a una vieja; dos soluciones: configurar afinidad de sesión, o desplegar todos los assets en cada host antes de activar el código (lo que rompe el estilo inmutable). En general, es más fácil servir los estáticos desde otro clúster.

## Rollout

Para infraestructura de **convergencia** con máquinas longevas, hay que decidir cuántas máquinas actualizar a la vez: todas a la vez rompe el zero downtime; una a una tarda demasiado. Lo habitual son tandas (p. ej. grupos Alpha, Bravo, Charlie, Delta, Foxtrot): detener la entrada de peticiones en el grupo, drenar la carga, ejecutar la herramienta de configuración, esperar health checks en verde, reanudar peticiones y repetir. El primer grupo debe ser el **canary**: se pausa ahí, se sube el tráfico gradualmente con *traffic shaping* y se vigilan picos de errores, latencia o RAM antes de seguir.

Toda aplicación debe exponer una ruta de **health check** de extremo a extremo que reporte versión de la app y del runtime, IP del host y estado de pools, cachés y circuit breakers. Así un simple cambio de estado avisa al balanceador de que no mande trabajo nuevo, dejando terminar las peticiones en curso. El servicio debe arrancar con el flag "available" en false hasta estar listo. Durante la actualización de Charlie, Alpha y Bravo ya están, y Delta y Foxtrot esperan: conviven las dos versiones.

Para infraestructura **inmutable** no se tocan las máquinas viejas: se levantan nuevas con el código nuevo. Decisión clave: arrancarlas en el clúster existente (necesita *stickiness* para que un llamante no rebote entre versiones, pero no interrumpe conexiones) o en un clúster nuevo que se valida antes de cambiar la IP (menos preocupación por stickiness, pero el cambio de IP puede ser traumático para peticiones en curso). Con despliegues muy frecuentes, mejor arrancar en el clúster existente. En todos los modelos, los datos de sesión en memoria se pierden: deben ser solo caché local de información disponible en otro sitio, desacoplando la vida del proceso de la de la sesión.

## Limpieza (Cleanup)

Un trabajo no está hecho hasta recoger las herramientas. Primero se eliminan los shims (ya innecesarios cuando todas las instancias están en el código nuevo), pero la eliminación se mete en una nueva migración. Luego llega la **contracción** del esquema: eliminar tablas, vistas, columnas, alias/sinónimos y stored procedures en desuso, y aplicar restricciones NOT NULL y de clave foránea. Las restricciones solo pueden añadirse *tras* el rollout, porque la versión vieja no sabría satisfacerlas (romperían el principio de no detectabilidad). Un framework de migraciones facilita esta división y aplica automáticamente los *change sets* ausentes del esquema.

En bases *schemaless*, la limpieza ejecuta *one-shots* para borrar documentos/claves o elementos que ya no se usan. También es buen momento para revisar los *feature toggles* (los nuevos deberían venir en "off" por defecto): decidir cuáles activar y programar la retirada de los que ya no hagan falta.

## Desplegar como los profesionales (Deploy Like the Pros)

La frontera entre operaciones y desarrollo se ha vuelto fractal: hay que diseñar el software para ser desplegable igual que se diseña para producción. La buena noticia es que diseñar para el despliegue permite hacer cambios grandes en pasos pequeños. Todo descansa en la automatización y el control de calidad: el pipeline debe aplicar la sabiduría de arquitectos, desarrolladores, testers y DBAs. Ejemplo de omisión que causa horas de downtime: olvidar un índice en una restricción de clave foránea. Como SQL es difícil de parsear, la solución es especificar los cambios de esquema en algo que no sea DDL (un DSL propio o una librería de migración), convirtiéndolos en datos para que el pipeline tenga "visión de rayos X" y rechace toda build con una FK sin índice. Que los humanos definan las reglas y las máquinas las apliquen.

## Ideas clave

- La v1.0 es el inicio del sistema: habrá muchísimos despliegues, así que el despliegue es una *feature* a diseñar, con el objetivo de zero downtime.
- El "downtime planificado" es una falacia: para el usuario el downtime es downtime; hay que diseñar para el estado "durante", no solo para el final.
- El *build pipeline* es un embudo: cada etapa busca rechazar la build; el despliegue continuo exige correr el pipeline completo en cada commit ("If it hurts, do it more often").
- Dos estilos de infraestructura: convergencia (mascotas, VMs longevas, mapeo manual) frente a inmutable (ganado, IaaS/PaaS, mapeo automático, imágenes reconstruidas).
- Un despliegue tiene escala micro (preparar, drenar, aplicar, arrancar por instancia) y macro (preparación, rollout y limpieza).
- Los cambios de esquema relacional se dividen en expansión (aditiva, antes del código; con shims/triggers para unir versiones) y contracción (eliminaciones y restricciones, solo tras el rollout).
- Para datos *schemaless*: translation pipeline, migración durante el despliegue, o "trickle, then batch" (migrar al tocar y luego por lotes), que es el enfoque preferido.
- En el rollout usar tandas con grupo *canary*, health checks de extremo a extremo y flag "available"; los datos de sesión en memoria deben ser solo caché.
- El pipeline debe convertir los cambios de esquema en datos para detectar errores mecánicos (p. ej. FK sin índice): humanos definen reglas, máquinas las aplican.
