# Designing Data-Intensive Applications — Martin Kleppmann (O'Reilly Media, 2017)
## Capítulo 4 — Encoding and Evolution (Codificación y evolución)

> Nota de extracción: el texto se obtuvo de la capa de texto del PDF; las citas usan la página del PDF como `(PDF p. N)`.

## Lo que necesitas saber

Las aplicaciones cambian con el tiempo, y casi todo cambio de funcionalidad implica cambiar los datos que se almacenan. El capítulo retoma la idea de *evolvability* (facilidad para adaptarse al cambio): como el código no se despliega de forma instantánea —en servidores se hace un *rolling upgrade* por nodos, y en clientes dependemos de que el usuario actualice—, versiones viejas y nuevas del código y de los datos coexisten en el sistema.

Para que el sistema siga funcionando hay que mantener compatibilidad en ambas direcciones. La *backward compatibility* significa que el código nuevo puede leer datos escritos por código viejo (suele ser fácil, porque el autor del código nuevo conoce el formato antiguo). La *forward compatibility* significa que el código viejo puede leer datos escritos por código nuevo (es más difícil, porque exige que el código antiguo ignore las adiciones del nuevo).

El capítulo recorre varios formatos de codificación —JSON, XML, CSV, Protocol Buffers, Thrift y Avro— analizando cómo manejan los cambios de esquema (*schema evolution*). Luego examina cómo fluyen los datos entre procesos: a través de bases de datos, de servicios (REST y RPC) y de paso de mensajes asíncrono (message brokers y actores). Sales sabiendo elegir un formato según compacidad, tooling y garantías de compatibilidad, y entendiendo que con cuidado los *rolling upgrades* son perfectamente viables.

## Formatos para codificar datos

Los programas trabajan con datos en (al menos) dos representaciones: en memoria (objetos, structs, listas, árboles, hash tables, optimizados para la CPU con punteros) y como secuencia de bytes autocontenida para escribir en disco o enviar por red. Traducir de memoria a bytes es *encoding* (serialization, marshalling); lo inverso es *decoding* (parsing, deserialization, unmarshalling). El libro usa el término *encoding* para no confundirlo con la *serialization* de las transacciones (Capítulo 7). El encoding no tiene nada que ver con el cifrado.

Formatos específicos de un lenguaje: muchos lenguajes traen soporte propio (`java.io.Serializable`, `Marshal` de Ruby, `pickle` de Python, Kryo para Java). Son cómodos, pero tienen problemas profundos:

- Atan los datos a un lenguaje concreto; leerlos desde otro es muy difícil.
- Para restaurar objetos, el decoding debe instanciar clases arbitrarias, lo que es una fuente frecuente de problemas de seguridad: un atacante que logre que decodifiques bytes arbitrarios puede instanciar clases arbitrarias y ejecutar código remoto.
- El versionado suele ser una idea de último momento, descuidando compatibilidad forward y backward.
- La eficiencia (CPU y tamaño) también se descuida; la serialización de Java es conocida por su mal rendimiento y codificación abultada.

Por eso, salvo para usos muy transitorios, es mala idea usar la codificación nativa del lenguaje.

JSON, XML y CSV son los formatos estándar textuales, legibles por humanos y ampliamente soportados, pero con problemas sutiles:

- Ambigüedad con los números: XML y CSV no distinguen número de cadena de dígitos; JSON distingue cadenas de números pero no enteros de flotantes ni precisión. Los enteros mayores a 2⁵³ no se representan exactamente en un flotante IEEE 754 de doble precisión: Twitter usa un entero de 64 bits por tweet y su API devuelve el ID dos veces (número y cadena decimal) para evitar que JavaScript lo corrompa.
- No soportan cadenas binarias; se recurre a Base64, lo que aumenta el tamaño un 33%.
- El soporte de esquemas es opcional (XML Schema, JSON Schema), potente pero complejo; muchas herramientas JSON no lo usan.
- CSV no tiene esquema y es vago (¿qué pasa con comas o saltos de línea en un valor?).

Aun con sus defectos, JSON, XML y CSV son suficientes para muchos fines, sobre todo como formatos de intercambio entre organizaciones, donde lo difícil es ponerse de acuerdo en el formato, no su eficiencia.

## Codificaciones binarias con esquema: Thrift, Protocol Buffers y Avro

Para datos internos de una organización hay menos presión por usar un formato de mínimo común denominador y se puede elegir algo más compacto. A partir de terabytes, el formato importa mucho. Existen codificaciones binarias de JSON (MessagePack, BSON, BJSON, UBJSON, BISON, Smile) y de XML (WBXML, Fast Infoset), pero ninguna tan extendida como las versiones textuales. Al no prescribir esquema, deben incluir todos los nombres de campo en los datos. Un registro de ejemplo (`userName`, `favoriteNumber`, `interests`) codificado con MessagePack ocupa 66 bytes, apenas menos que los 81 del JSON textual sin espacios: la mejora es dudosa frente a perder legibilidad.

Thrift (Facebook) y Protocol Buffers (Google), ambos open source en 2007–08, requieren un esquema definido en su IDL y traen un generador de código que produce clases en varios lenguajes. La gran diferencia frente a las variantes de JSON binario es que no incluyen nombres de campo: usan *field tags* (números del esquema) como alias compactos de cada campo, junto con una anotación de tipo. Thrift tiene dos formatos: BinaryProtocol (59 bytes en el ejemplo) y CompactProtocol (34 bytes), que empaqueta tipo y tag en un byte y usa enteros de longitud variable. Protocol Buffers tiene un único formato y cabe en 33 bytes. Los marcadores `required`/`optional` no cambian la codificación; `required` solo habilita una verificación en tiempo de ejecución que falla si el campo no está.

### Evolución de esquema con field tags

Un registro codificado es la concatenación de sus campos; cada uno se identifica por su tag y su tipo, y si no tiene valor se omite. De ahí las reglas:

- Puedes cambiar el **nombre** de un campo (no se codifica), pero **nunca su tag**: invalidaría todos los datos existentes.
- Puedes **añadir** campos con un tag nuevo. El código viejo que encuentra un tag desconocido lo ignora (la anotación de tipo le dice cuántos bytes saltar): así se mantiene la *forward compatibility*. Para *backward compatibility*, todo campo añadido tras el despliegue inicial debe ser `optional` o tener valor por defecto (no puede ser `required`).
- Puedes **eliminar** solo campos `optional`, y nunca reutilizar su tag.

Cambiar el tipo de dato es posible pero arriesga pérdida de precisión o truncamiento (p. ej., un entero de 64 bits leído por código viejo con variable de 32 bits se trunca). Protocol Buffers no tiene tipo lista: usa el marcador `repeated`, lo que permite convertir un campo `optional` en `repeated`. Thrift sí tiene tipo lista dedicado, que no permite esa evolución pero admite listas anidadas.

## Avro

Apache Avro (2009, subproyecto de Hadoop) usa esquema pero sin tags. Tiene dos lenguajes de esquema: Avro IDL (para humanos) y uno basado en JSON (para máquinas). El ejemplo ocupa solo 32 bytes, lo más compacto de todo. En los datos no hay nada que identifique campos ni tipos: es pura concatenación de valores (una cadena es longitud + bytes UTF-8). Para parsear, se recorren los campos en el orden del esquema. Por eso el dato solo se decodifica bien si el lector usa un esquema **compatible** con el del escritor.

Aquí está la idea clave: la *writer's schema* (el esquema con el que se escribió) y la *reader's schema* (el que espera quien lee) no tienen que ser idénticas, solo compatibles. Al decodificar, Avro resuelve las diferencias mirando ambas en paralelo: empareja campos por **nombre**, ignora un campo que esté en el escritor pero no en el lector, y rellena con el valor por defecto del lector un campo que este espera pero el escritor no tiene.

Reglas de evolución: *forward compatibility* es tener esquema nuevo como escritor y viejo como lector; *backward compatibility* es lo inverso. Para mantener compatibilidad solo puedes añadir o quitar campos **con valor por defecto**. Un campo sin default rompe backward (al añadir) o forward (al quitar). En Avro `null` no es default válido salvo que uses un *union type* (`union { null, long, string }`) y `null` sea una de sus ramas; así Avro no tiene marcadores `optional`/`required`. Cambiar el nombre de un campo es posible con *aliases* en el esquema del lector: es backward pero no forward compatible; añadir una rama a un union también.

¿Cómo sabe el lector la *writer's schema*? No se incluye en cada registro (sería más grande que el dato). Según el contexto:

- **Archivo grande con muchos registros** (típico en Hadoop): el esquema se incluye una vez al inicio, en los *object container files*.
- **Base de datos con registros individuales**: se guarda un número de versión al inicio de cada registro y una lista de versiones de esquema en la base (así trabaja Espresso de LinkedIn).
- **Conexión de red bidireccional**: los procesos negocian la versión al establecer la conexión (así funciona el RPC de Avro).

La gran ventaja de no tener tags es que Avro es amistoso con esquemas generados dinámicamente: puedes volcar una base relacional a un archivo Avro generando el esquema desde el esquema relacional, y si la base cambia, regeneras el esquema; como los campos se emparejan por nombre, sigue funcionando. Con Thrift o Protocol Buffers habría que asignar los tags a mano. Además, Thrift y Protocol Buffers dependen de generación de código (útil en lenguajes de tipado estático), mientras que Avro ofrece generación opcional y funciona igual sin ella, porque el object container file es autodescriptivo.

Los esquemas tienen méritos frente a las "binary JSON": son más compactos (omiten nombres de campo), sirven de documentación siempre actualizada (son necesarios para decodificar), permiten comprobar compatibilidad antes de desplegar, y habilitan generación de código con chequeo de tipos. En resumen, la evolución de esquemas da la misma flexibilidad que las bases schema-on-read con mejores garantías y tooling.

## Modos de flujo de datos

La compatibilidad es una relación entre el proceso que codifica y el que decodifica. Hay tres formas comunes de que los datos fluyan entre procesos.

**A través de bases de datos.** El que escribe codifica y el que lee decodifica. Si solo hay un proceso, leer es enviarte un mensaje a tu yo futuro, y hace falta backward compatibility. Como suele haber varios procesos (versiones nuevas y viejas durante un rolling upgrade), también se necesita forward compatibility. Un riesgo adicional: si código nuevo escribe un campo nuevo y código viejo lee, actualiza y reescribe el registro, lo deseable es que preserve el campo desconocido; los formatos lo soportan, pero a veces hay que cuidarlo a nivel de aplicación para no perderlo al mapear a objetos del modelo. Además, *data outlives code*: el código se reemplaza en minutos, pero los datos de hace cinco años siguen en su codificación original salvo que los reescribas (migrar es caro). La mayoría de las bases relacionales permiten añadir una columna con default null sin reescribir datos. La evolución de esquema hace que toda la base parezca codificada con un único esquema aunque el almacenamiento mezcle versiones históricas. Para *archival storage* (snapshots, data warehouse), el volcado se escribe de una vez con el esquema más reciente; formatos como Avro object container files o columnares como Parquet encajan bien.

**A través de servicios: REST y RPC.** El arreglo habitual es clientes y servidores; la API que expone el servidor es un *service*. Un servidor puede ser a su vez cliente de otro: así se descompone una app grande en servicios por área de funcionalidad (SOA, hoy microservicios), con el objetivo de que cada servicio sea desplegable y evolucionable de forma independiente. Un *web service* usa HTTP como transporte y aparece en tres contextos: app cliente en el dispositivo del usuario, servicio a servicio dentro de la organización (middleware), y entre organizaciones distintas (APIs públicas, procesamiento de tarjetas, OAuth). Hay dos enfoques: REST (filosofía de diseño sobre HTTP, formatos simples, URLs para recursos; una API así es *RESTful*, descrita con OpenAPI/Swagger) y SOAP (protocolo XML con WSDL y la familia WS-*, complejo, dependiente de tooling y en declive fuera de grandes empresas).

Los RPC (desde los años 70: EJB, RMI, DCOM, CORBA) intentan que una llamada remota parezca una llamada local (*location transparency*), pero el enfoque es fundamentalmente defectuoso: una petición de red es impredecible (puede perderse), puede devolver sin resultado por timeout (no sabes si llegó), los reintentos exigen idempotencia, la latencia es muy variable, hay que codificar los parámetros en bytes, y cliente y servidor pueden usar lenguajes distintos. Los frameworks actuales (gRPC sobre Protocol Buffers, Thrift, Avro RPC, Finagle, Rest.li) son más explícitos sobre esta diferencia: usan *futures*/promesas, streams y service discovery. Un encoding binario a medida rinde mejor que JSON sobre REST, pero REST gana en experimentación, soporte universal y ecosistema de herramientas; por eso predomina en APIs públicas. Para evolución de RPC se asume que los servidores se actualizan primero y los clientes después: basta backward compatibility en las peticiones y forward compatibility en las respuestas. La compatibilidad debe mantenerse largo tiempo (el proveedor no controla a sus clientes externos), a veces manteniendo varias versiones de la API en paralelo; no hay acuerdo sobre cómo versionar (número en la URL, en el header `Accept`, o por cliente).

**Paso de mensajes asíncrono.** Está entre RPC y bases de datos: baja latencia como RPC, pero vía un intermediario (*message broker*) que almacena el mensaje temporalmente. Ventajas frente a RPC directo: actúa de buffer si el receptor no está disponible, reentrega tras caídas, el emisor no necesita conocer IP y puerto del receptor, un mensaje puede ir a varios destinatarios, y desacopla lógicamente emisor y receptor. La comunicación suele ser unidireccional y asíncrona. Brokers populares: RabbitMQ, ActiveMQ, HornetQ, NATS, Apache Kafka. El emisor envía a una *queue* o *topic* y el broker entrega a los consumidores. El broker no impone modelo de datos (el mensaje es bytes con metadatos), así que cualquier encoding backward/forward compatible da máxima flexibilidad; si un consumidor republica, hay que preservar campos desconocidos.

El *actor model* encapsula la lógica en actores con estado local que se comunican por mensajes asíncronos (la entrega no está garantizada). En frameworks distribuidos escala a varios nodos codificando el mensaje para la red; la location transparency funciona mejor que en RPC porque el modelo ya asume pérdida de mensajes. Para rolling upgrades siguen importando forward y backward compatibility. Akka usa la serialización de Java por defecto (sin compatibilidad, reemplazable por Protocol Buffers); Orleans usa un formato propio que no soporta rolling upgrades por defecto; Erlang OTP hace difícil cambiar esquemas de record (el nuevo tipo `maps` podría ayudar).

## Ideas clave

- La elección de formato de codificación afecta no solo la eficiencia, sino la arquitectura de la aplicación y sus opciones de despliegue.
- Los *rolling upgrades* exigen que versiones viejas y nuevas del código coexistan, de modo que todo dato en circulación debe ser *backward compatible* (código nuevo lee datos viejos) y *forward compatible* (código viejo lee datos nuevos).
- Las codificaciones nativas de cada lenguaje atan los datos a ese lenguaje y suelen fallar en compatibilidad y seguridad; úsalas solo para fines transitorios.
- JSON, XML y CSV son textuales y universales, pero vagos con tipos (números, cadenas binarias); su compatibilidad depende de cómo los uses.
- Thrift y Protocol Buffers usan field tags y generación de código; Avro resuelve diferencias entre writer's schema y reader's schema emparejando campos por nombre, sin tags, lo que favorece esquemas generados dinámicamente.
- En formatos con esquema, la evolución se logra con reglas claras: no cambiar tags, añadir solo campos opcionales o con default, y no reutilizar tags eliminados.
- Los datos fluyen por bases de datos (data outlives code), por servicios (REST y RPC, con compatibilidad asimétrica entre peticiones y respuestas) y por paso de mensajes asíncrono (brokers y actores).
- Con un poco de cuidado, compatibilidad backward/forward y rolling upgrades son perfectamente alcanzables.
