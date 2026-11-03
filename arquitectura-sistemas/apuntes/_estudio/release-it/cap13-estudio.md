# Design for Deployment (Diseñar para el despliegue) — Estudio

## Tarjetas de repaso

P: ¿Por qué el despliegue debe tratarse como una *feature* del software? / R: Porque la v1.0 es el comienzo de la vida del sistema, no el final, así que habrá muchísimos despliegues; conviene diseñarlos desde la aplicación con el objetivo de zero downtime, en lugar de dejárselos a operaciones.

P: ¿En qué consiste "la falacia del tiempo de inactividad planificado"? / R: En que para el usuario el downtime es downtime, da igual el aviso interno; el error de fondo es diseñar solo para el estado *después* de la versión, asumiendo un salto instantáneo, cuando el usuario ve el sistema "durante" la actualización.

P: ¿Qué es un *build pipeline* y en qué se diferencia de un CI tradicional? / R: Es un servidor de integración continua crecido: empieza como CI (pruebas unitarias, análisis estático, compilación) pero no se detiene en el informe y el *archive*, sino que continúa hasta desplegar en producción pasando por entorno de prueba, scripts de migración y pruebas de integración. Nygard lo describe como un embudo.

P: ¿Qué diferencia hay entre mapeo de configuración a hosts manual y automático? / R: En el manual el operador asigna roles a las máquinas; en el automático el operador pide "X réplicas del servicio Y en estas ubicaciones" y la plataforma PaaS lo cumple combinando capacidad y restricciones.

P: ¿Qué distingue la infraestructura por convergencia de la inmutable? / R: La convergencia arranca una imagen mínima y scripts instalan y llevan la máquina al estado deseado (mascotas, VMs longevas, mapeo manual); la inmutable empaqueta una imagen de VM o contenedor construida por el pipeline y, para cambiar, reconstruye y borra la máquina vieja (ganado, IaaS/PaaS, mapeo automático).

P: ¿Cuál es el argumento de los partidarios de la inmutabilidad contra la convergencia? / R: Que la convergencia nunca funciona del todo: las máquinas longevas acumulan estado irreparable o no contemplado por las recetas, como parámetros del kernel o timeouts TCP.

P: ¿Qué significa el lema "If it hurts, do it more often" en despliegue continuo? / R: Que para romper el círculo vicioso de demora, acumulación de cambios y riesgo creciente, hay que desplegar más a menudo; en el límite, ejecutar el pipeline completo en cada commit.

P: ¿Cuáles son los cuatro lapsos de la escala microscópica de un despliegue por instancia? / R: Preparar el cambio, drenar (drain) la actividad tras dejar de aceptar peticiones, aplicar el cambio y arrancar hasta estar listo para recibir carga (incluye calentar cachés y JIT y establecer conexiones).

P: ¿En qué se dividen los cambios de esquema relacional para lograr compatibilidad? / R: En expansión (cambios aditivos seguros de aplicar antes de desplegar el código: tablas, vistas, columnas nullable, alias, procedures, triggers, copias de datos) y contracción/limpieza (eliminaciones y restricciones, solo tras el rollout).

P: ¿Qué es un *shim* en un despliegue y para qué sirve? / R: Es código (p. ej. un trigger) que une la versión vieja y la nueva durante el rollout; al dividir una tabla, un trigger INSERT en la tabla vieja replica en la nueva y un UPDATE en la nueva actualiza la vieja, evitando perder datos y bucles infinitos.

P: ¿Cuáles son los tres enfoques para migrar bases de datos *schemaless*? / R: Translation pipeline (la app lee cualquier versión y cada versión añade un traductor), migración durante el despliegue (desplegando la app antes de migrar datos) y "trickle, then batch", el preferido del autor.

P: ¿En qué consiste "trickle, then batch"? / R: Código condicional que migra cada documento al tocarlo, amortizando el coste entre peticiones; luego una migración por lotes sobre los no tocados (segura porque ya no hay instancias viejas), y finalmente se despliega una versión que elimina el chequeo condicional.

P: ¿Cómo recomienda Nygard versionar los assets web para hacer *cache busting*? / R: Con cabeceras de expiración muy lejanas (unos diez años) y usando el SHA del commit de git incorporado en la URL o el nombre de archivo (no en el query string), para tener versiones vieja y nueva en directorios distintos.

P: ¿Qué debe exponer y reportar una ruta de *health check* de extremo a extremo? / R: Versión de la app y del runtime, IP del host y estado de pools, cachés y circuit breakers; el servicio debe arrancar con el flag "available" en false hasta estar listo, para avisar al balanceador de que no mande trabajo nuevo.

P: ¿Por qué las restricciones NOT NULL y de clave foránea solo pueden añadirse tras el rollout? / R: Porque la versión vieja de la app no sabría satisfacerlas y las violaría, rompiendo el principio de no detectabilidad; por eso pertenecen a la fase de contracción, no a la de expansión.

## Preguntas de autoevaluación

P: ¿Cuáles son las tres grandes preocupaciones que aborda el capítulo? / R: Automatización, orquestación y despliegue sin interrupciones (zero downtime). (Sección "Lo que necesitas saber")

P: ¿Qué quiere decir Nygard con "máquina" y con "service"? / R: "Máquina" es una instancia configurable de sistema operativo (metal físico, VM, contenedor o unikernel); un "service" es una interfaz invocable compuesta de copias redundantes de software en varias máquinas. (Sección "Tantas máquinas")

P: Ante dos equipos, uno que despliega a producción de forma automática y otro que pone una etapa de pausa con aprobación humana, ¿cuál es correcto? / R: Ambos son válidos según el contexto: si el coste de ir lento supera al del error, conviene lo automático; en entornos críticos o muy regulados, la revisión humana (con un "pulsador de botón" autorizado siempre disponible). (Sección "Despliegue continuo")

P: ¿Por qué el grano del empaquetado afecta a la planificación de un rollout? / R: Porque cuanto mayor es el grano (archivos < archives < máquinas completas), más tarda el cambio en aplicarse y activarse, lo que hay que tener en cuenta al desplegar por tandas. (Sección "Fases del despliegue")

P: Al migrar durante el despliegue en una base schemaless, ¿por qué conviene desplegar la app antes de migrar los datos? / R: Porque de los cuatro escenarios de rollout y migración concurrentes solo falla el nº 4 (una instancia vieja lee un documento nuevo); desplegar la app nueva primero evita ese caso. (Sección "Bases de datos sin esquema")

P: ¿Por qué falla el consejo de versionar los assets y luego reescribir la URL para eliminar la versión? / R: Porque asume un *big bang* con cambio instantáneo; si app y assets salen del mismo servidor, el navegador puede pedir la página a una instancia nueva y el asset a una vieja. Se resuelve con afinidad de sesión o sirviendo los estáticos desde otro clúster. (Sección "Assets web")

P: En un rollout por tandas, ¿qué papel cumple el grupo *canary*? / R: Es el primer grupo: se pausa ahí, se sube el tráfico gradualmente con *traffic shaping* y se vigilan picos de errores, latencia o RAM antes de continuar con el resto de grupos. (Sección "Rollout")

P: ¿Cómo logra el pipeline detectar errores mecánicos como una clave foránea sin índice? / R: Especificando los cambios de esquema en algo que no sea DDL (un DSL propio o una librería de migración) para convertirlos en datos; así el pipeline gana "visión de rayos X" y rechaza toda build que incumpla las reglas. Los humanos definen las reglas y las máquinas las aplican. (Sección "Desplegar como los profesionales")

## Checklist

- [ ] Tratar el despliegue como una *feature* diseñada desde la aplicación, con zero downtime como objetivo.
- [ ] Montar un *build pipeline* que vaya del commit hasta producción (CI, migraciones, pruebas de integración), buscando en cada etapa motivos para rechazar la build.
- [ ] Elegir el estilo de empaquetado adecuado: convergencia para mascotas/VMs longevas, inmutable para ganado/IaaS/PaaS; no perderse buscando "la mejor" herramienta.
- [ ] Minimizar la demora entre commit y producción; acercarse a ejecutar el pipeline completo en cada commit.
- [ ] Diseñar cada instancia para preparar, drenar, aplicar y arrancar (calentando cachés/JIT y conexiones) antes de recibir carga.
- [ ] Separar los cambios de esquema relacional en expansión (antes del código) y contracción (tras el rollout); usar un framework de migraciones (p. ej. Liquibase).
- [ ] Crear shims (insert, update, delete en ambos sentidos) para unir versiones al dividir tablas, evitando bucles, y probarlos con datos reales de producción (NULLs y registros antiguos).
- [ ] Para datos schemaless, aplicar "trickle, then batch" sin solapar dos migraciones trickle sobre el mismo tipo de documento.
- [ ] Versionar assets con el SHA del commit en la URL/nombre de archivo, con expiración lejana; servir estáticos desde otro clúster o usar afinidad de sesión.
- [ ] Hacer el rollout por tandas con grupo canary, traffic shaping y health checks de extremo a extremo; arrancar con flag "available" en false.
- [ ] Mantener los datos de sesión en memoria solo como caché de información disponible en otro sitio.
- [ ] En la limpieza: eliminar shims (en una nueva migración), contraer el esquema, añadir restricciones NOT NULL y FK, ejecutar one-shots en schemaless y revisar los *feature toggles* (nuevos en "off").
