# Encoding and Evolution (Codificación y evolución) — Estudio

## Tarjetas de repaso

P: ¿Qué es *evolvability* y por qué importa en este capítulo? / R: Es la facilidad de un sistema para adaptarse al cambio; importa porque casi todo cambio de funcionalidad cambia los datos almacenados y el código no se despliega de forma instantánea.

P: ¿Qué es *backward compatibility*? / R: Que el código nuevo pueda leer datos escritos por código viejo; suele ser fácil porque el autor del código nuevo conoce el formato antiguo.

P: ¿Qué es *forward compatibility*? / R: Que el código viejo pueda leer datos escritos por código nuevo; es más difícil porque exige que el código antiguo ignore las adiciones del nuevo.

P: ¿Qué son *encoding* y *decoding*? / R: *Encoding* (serialization, marshalling) traduce la representación en memoria a una secuencia de bytes; *decoding* (parsing, deserialization, unmarshalling) hace lo inverso. No tiene relación con el cifrado.

P: ¿Por qué evitar las codificaciones nativas del lenguaje salvo para usos transitorios? / R: Atan los datos a un lenguaje, el decoding puede instanciar clases arbitrarias (riesgo de ejecución remota de código), descuidan el versionado y la compatibilidad, y suelen ser ineficientes.

P: ¿Qué problemas de tipos tienen JSON, XML y CSV? / R: Ambigüedad con los números (XML/CSV no distinguen número de cadena; JSON no distingue enteros de flotantes ni precisión) y falta de soporte de cadenas binarias (se usa Base64, +33% de tamaño).

P: ¿Qué son los *field tags* en Thrift y Protocol Buffers? / R: Números definidos en el esquema que actúan como alias compactos de cada campo, junto con una anotación de tipo, evitando incluir los nombres de campo en los datos.

P: ¿Qué se puede y no se puede cambiar de un campo con field tags? / R: Se puede cambiar el nombre (no se codifica) pero nunca el tag; se pueden añadir campos con tag nuevo (optional o con default) y eliminar solo campos optional, sin reutilizar nunca su tag.

P: ¿En qué se diferencia Avro de Thrift y Protocol Buffers? / R: Avro no usa tags ni nombres en los datos (pura concatenación de valores); empareja campos por nombre comparando la writer's schema con la reader's schema, lo que favorece esquemas generados dinámicamente.

P: ¿Qué son la *writer's schema* y la *reader's schema* en Avro? / R: La writer's schema es con la que se escribió el dato y la reader's schema la que espera quien lee; no deben ser idénticas, solo compatibles, y Avro resuelve las diferencias al decodificar.

P: En Avro, ¿cómo se mantiene la compatibilidad al evolucionar el esquema? / R: Solo añadiendo o quitando campos con valor por defecto; un campo sin default rompe backward al añadir o forward al quitar. `null` solo es default válido dentro de un union type que incluya `null`.

P: ¿Cómo conoce el lector la writer's schema en Avro según el contexto? / R: En archivos grandes (object container files) se incluye una vez al inicio; en bases de datos se guarda un número de versión por registro; en conexiones de red se negocia al establecer la conexión.

P: ¿Cuáles son los tres modos de flujo de datos entre procesos? / R: A través de bases de datos, a través de servicios (REST y RPC) y mediante paso de mensajes asíncrono (message brokers y actores).

P: ¿Por qué el enfoque clásico de RPC es defectuoso? / R: Intenta que una llamada remota parezca local, pero la red es impredecible (pérdidas, timeouts sin saber si llegó), exige idempotencia en reintentos, la latencia varía y hay que codificar parámetros entre lenguajes distintos.

P: ¿Qué ventajas aporta un message broker frente al RPC directo? / R: Actúa de buffer si el receptor no está disponible, reentrega tras caídas, el emisor no necesita IP/puerto del receptor, un mensaje puede ir a varios destinatarios y desacopla lógicamente emisor y receptor.

## Preguntas de autoevaluación

P: ¿Por qué un sistema necesita a la vez backward y forward compatibility durante un rolling upgrade? / R: Porque versiones viejas y nuevas del código coexisten: el código nuevo debe leer datos viejos (backward) y el código viejo debe leer datos nuevos (forward). (Sección "Lo que necesitas saber" e "Ideas clave")

P: ¿Qué hace el código viejo al encontrar un field tag desconocido en Thrift/Protocol Buffers y cómo contribuye a la compatibilidad? / R: Lo ignora usando la anotación de tipo para saber cuántos bytes saltar, lo que mantiene la forward compatibility. (Sección "Evolución de esquema con field tags")

P: ¿Por qué Avro es amistoso con esquemas generados dinámicamente y Thrift/Protocol Buffers no tanto? / R: Como Avro empareja campos por nombre y no usa tags, se puede regenerar el esquema desde una base relacional cuando cambia; con tags habría que reasignarlos a mano. (Sección "Avro")

P: ¿Qué significa que "data outlives code" y qué implica para la evolución de esquemas? / R: El código se reemplaza en minutos, pero datos de hace años siguen en su codificación original salvo que se reescriban; la evolución de esquema hace que la base parezca de un único esquema aunque mezcle versiones históricas. (Sección "Modos de flujo de datos", bases de datos)

P: Al evolucionar un servicio RPC, ¿qué compatibilidad se necesita en peticiones y respuestas y por qué? / R: Se asume que los servidores se actualizan antes que los clientes, así que basta backward compatibility en las peticiones y forward compatibility en las respuestas. (Sección "Modos de flujo de datos", servicios)

P: ¿Qué riesgo aparece cuando código viejo lee, actualiza y reescribe un registro que contiene campos nuevos desconocidos? / R: Que se pierdan esos campos desconocidos; lo deseable es preservarlos, y aunque los formatos lo soportan a veces hay que cuidarlo a nivel de aplicación al mapear a objetos. (Sección "Modos de flujo de datos", bases de datos)

P: ¿En qué se diferencian REST y SOAP como enfoques de web service? / R: REST es una filosofía de diseño sobre HTTP con formatos simples y URLs para recursos (descrita con OpenAPI/Swagger); SOAP es un protocolo XML con WSDL y la familia WS-*, complejo y en declive fuera de grandes empresas. (Sección "Modos de flujo de datos", servicios)

P: ¿Por qué la location transparency funciona mejor en el actor model que en RPC? / R: Porque el actor model ya asume que la entrega de mensajes no está garantizada, de modo que la diferencia entre comunicación local y remota se nota menos. (Sección "Modos de flujo de datos", paso de mensajes asíncrono)

## Puntos a dominar

- Distinguir con precisión backward compatibility (código nuevo lee datos viejos) de forward compatibility (código viejo lee datos nuevos) y asociarlas a los rolling upgrades.
- Explicar por qué las codificaciones nativas del lenguaje son mala idea salvo usos transitorios (acoplamiento, seguridad, versionado, eficiencia).
- Enumerar los problemas de tipos de JSON, XML y CSV, incluido el caso de los enteros mayores a 2⁵³ y la solución de Twitter.
- Dominar las reglas de evolución con field tags (no cambiar tags, añadir solo optional/con default, no reutilizar tags eliminados) y las de Avro (campos con default, union types para `null`, aliases para renombrar).
- Explicar cómo Avro resuelve diferencias entre writer's schema y reader's schema y cómo el lector obtiene la writer's schema en cada contexto.
- Comparar los tres modos de flujo de datos y las garantías de compatibilidad que cada uno exige, incluido "data outlives code".
- Argumentar por qué el RPC clásico es defectuoso y qué aportan los frameworks modernos (futures, streams, service discovery) y los message brokers.
