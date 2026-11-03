# Refactoring to microservices (Refactorización hacia microservicios) — Estudio

## Tarjetas de repaso

P: ¿Qué es una *strangler application*? / R: Una nueva aplicación de microservicios que crece alrededor del monolito, implementando nuevas funciones como servicios y extrayendo capacidades existentes, hasta que el monolito se reduce y desaparece o queda como un microservicio más.

P: ¿Por qué se evita el *big bang rewrite*? / R: Porque es muy arriesgado: duplicas funcionalidad durante meses o años, el monolito sigue siendo un objetivo en movimiento y puedes reimplementar funciones ya innecesarias ("the only thing a Big Bang rewrite guarantees is a Big Bang!").

P: ¿Cuándo se justifica migrar un monolito a microservicios? / R: Solo si resuelve un problema de negocio significativo (entrega lenta, releases con errores, mala escalabilidad) y no cuando el problema es un mal proceso de desarrollo, que a veces se arregla con pruebas automatizadas.

P: ¿Cuáles son las tres estrategias para estrangular el monolito? / R: Implementar nuevas funciones como servicios, separar la capa de presentación del backend y romper el monolito extrayendo capacidades de negocio en servicios.

P: ¿Qué dice la Ley de los Agujeros aplicada a la migración? / R: "If you find yourself in a hole, stop digging": no añadas código nuevo al monolito; implementa las funciones nuevas como servicios.

P: ¿Qué dos elementos integran una función nueva con el monolito? / R: Un API gateway que enruta las peticiones nuevas al servicio y las antiguas al monolito, y el *integration glue code* (adaptadores en monolito y servicio que usan IPC como REST o eventos de dominio).

P: ¿Qué incluye el corte vertical al extraer una capacidad de negocio? / R: Adaptadores de entrada (endpoints de API), lógica de dominio, adaptadores de salida (acceso a datos) y el esquema de base de datos.

P: ¿Cómo se dividen las referencias entre objetos al partir el modelo de dominio? / R: Pensando en agregados DDD que se referencian por clave primaria; por ejemplo, la referencia de `Order` a `Restaurant` se sustituye por un campo `restaurantId`.

P: ¿Para qué sirve replicar datos del servicio extraído de vuelta al monolito? / R: Para preservar la estructura original durante la transición, dejando los campos movidos de solo lectura, de modo que solo haya que cambiar los puntos que actualizan esos campos y minimizar los cambios al monolito.

P: ¿Qué es una *anti-corruption layer* (ACL)? / R: Una capa que traduce entre los modelos de dominio del servicio y del monolito para evitar que el modelo heredado contamine al modelo más limpio del servicio nuevo.

P: ¿Qué dos opciones hay para consultar datos del otro lado en el integration glue? / R: Invocar su API de consulta (simple pero potencialmente ineficiente y con menor disponibilidad por IPC síncrona) o mantener una réplica tipo vista CQRS que se actualiza suscribiéndose a eventos de dominio (eficiente pero más compleja).

P: ¿Cuándo necesita el monolito transacciones compensatorias en una saga? / R: Solo si las transacciones posteriores pueden fallar; si cada transacción del monolito es *pivot* o *retriable*, nunca compensa, lo que se logra secuenciando con cuidado las extracciones.

P: ¿Cómo se soportan a la vez la seguridad del monolito y la de los servicios durante la transición? / R: Con un cambio pequeño en el login handler que devuelve una cookie `USERINFO` (un JWT con ID y roles); el API gateway la valida y la pasa en el header `Authorization` al invocar servicios.

P: ¿Qué infraestructura de despliegue es imprescindible al empezar la migración? / R: Solo un pipeline de despliegue con pruebas automatizadas; con pocos servicios basta incluso un archivo de configuración fijo para el descubrimiento, difiriendo las decisiones costosas de infraestructura.

## Preguntas de autoevaluación

P: ¿Por qué debe hacerse la migración de forma incremental y no de una sola vez? / R: Porque el *big bang rewrite* es muy arriesgado (duplica funcionalidad durante meses o años y persigue un objetivo en movimiento), mientras que la strangler application da retorno inmediato y permite demostrar valor pronto para conservar el apoyo del negocio. (Sección "Visión general de la refactorización a microservicios")

P: ¿Cuál de las tres estrategias migra realmente la funcionalidad y por qué siempre se acaba usando? / R: Extraer capacidades de negocio en servicios; las otras frenan el crecimiento o separan capas, pero la extracción es la que mueve la funcionalidad del monolito, por lo que siempre se termina aplicando. (Sección "Estrategias para refactorizar el monolito")

P: ¿Cuándo conviene NO implementar una función nueva como servicio? / R: Cuando la función es demasiado pequeña o está muy acoplada al monolito, causando problemas de rendimiento por IPC excesiva o de consistencia; entonces se implementa en el monolito y se extrae después junto a funciones relacionadas. (Sección "Estrategias para refactorizar el monolito")

P: ¿Qué dos desafíos principales aparecen al extraer una capacidad de negocio? / R: Dividir el modelo de dominio (eliminar referencias que cruzarían fronteras de servicio y extraer funcionalidad embebida en *god classes* como `Order`) y refactorizar la base de datos (p. ej. partir `ORDERS` y crear `DELIVERY`). (Sección "Estrategias para refactorizar el monolito")

P: ¿Cómo evita el ejemplo de Delayed Order Service ser ineficiente al obtener datos? / R: Obtiene la información de contacto del cliente vía `CustomerContactInfoRepository` con llamada REST porque es poco frecuente, pero mantiene réplicas de `Order` y `Restaurant` suscribiéndose a eventos porque consultarlos todos sería ineficiente. (Sección "Ejemplo 1: nueva función como servicio — Delayed Order Service")

P: ¿Cuáles son los tres pasos para cambiar el monolito al extraer Delivery Service? / R: (1) Encapsular la gestión de entregas tras una interfaz `DeliveryService` de grano grueso; (2) cambiar todos los puntos que la invocan para usar esa interfaz (lo más laborioso); (3) implementar la interfaz con un proxy que envía mensajes al servicio, usando un *feature toggle* para alternar entre la implementación antigua y la nueva. (Sección "Ejemplo 2: romper el monolito — extraer Delivery Service")

P: ¿Cómo evita Delivery Service tener que conocer el ciclo de vida del pedido? / R: Ofrece una API de notificaciones con tres mensajes (`ScheduleDelivery`, `ReviseDelivery`, `CancelDelivery`) en lugar de reaccionar a eventos `Order`, de modo que no necesita conocer dicho ciclo de vida. (Sección "Ejemplo 2: romper el monolito — extraer Delivery Service")

P: ¿Por qué la secuencia de extracciones afecta a la complejidad de las sagas en el monolito? / R: Porque extraer Order Service antes que Kitchen y Accounting hace que la transacción del monolito quede como pivot o retriable, evitando transacciones compensatorias (p. ej. un estado `APPROVAL_PENDING` como semantic lock) que serían costosas y arriesgadas de añadir. (Sección "Diseñar la colaboración entre el servicio y el monolito")

## Puntos a dominar

- Confirmar que los problemas de entrega provienen de haber superado la arquitectura monolítica y no de un mal proceso de desarrollo antes de migrar.
- Explicar el patrón *Strangler application* y por qué se descarta el *big bang rewrite*.
- Enumerar y distinguir las tres estrategias de estrangulamiento, identificando la extracción de capacidades como la clave de la migración.
- Describir el corte vertical de una extracción y cómo dividir el modelo de dominio con referencias por clave primaria al estilo agregados DDD.
- Justificar la replicación de datos de vuelta al monolito para minimizar cambios en su código y esquema.
- Diseñar el *integration glue* con repositorios o interfaces de servicio, eligiendo entre API de consulta y réplica CQRS, y aplicando una anti-corruption layer.
- Razonar cuándo el monolito requiere transacciones compensatorias y cómo secuenciar extracciones para que sus transacciones sean pivot o retriable.
- Explicar el mecanismo de la cookie `USERINFO` (JWT) para soportar seguridad del monolito y de los servicios durante la transición.
