# Release It! Design and Deploy Production-Ready Software (2nd Edition) — Michael T. Nygard (The Pragmatic Bookshelf, 2018)
## Capítulo 14 — Handling Versions (Manejo de versiones)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF y las citas usan la página del PDF.

## Lo que necesitas saber

Una vez que podemos desplegar fácil y repetidamente, también podemos cambiar fácilmente cómo nuestro software habla con el resto del mundo. El riesgo es romper a las aplicaciones consumidoras: cada vez que lo hacemos, forzamos a otros equipos a trabajar para volver a funcionar. Algo va mal si nuestro equipo genera trabajo para varios equipos; es mejor que hagamos trabajo extra para mantener compatibilidad antes que trasladar los costes de migración a otros.

La tesis es el respeto a la autonomía: cada consumidor tiene su propio equipo y calendario, así que no se les puede forzar a publicar al mismo tiempo que nosotros solo para que cambiemos nuestra API. Coordinar despliegues entre consumidor y proveedor no escala; el efecto dominó puede obligar a toda la empresa a actualizar a la vez. Por eso la mayoría de versiones nuevas de un servicio deberían ser compatibles.

Sales sabiendo cómo hacer cambios de API no rompedores, cómo ayudar a los consumidores cuando un cambio rompedor es inevitable, y cómo defenderte de las versiones ajenas tanto al recibir peticiones como al llamar a otros servicios.

## El ejemplo que recorre el capítulo

Un servicio de préstamos peer-to-peer que recoge una solicitud de préstamo para análisis de crédito. Sus rutas iniciales incluyen crear y ver solicitudes (`POST /applications`, `GET /applications/:id`, búsqueda con `GET /applications?q=...`) y gestionar prestatarios (`POST /borrower`, `GET /borrower/:id`, `PUT /borrower/:id`). Al tener éxito surgen nuevos requisitos: la representación de la solicitud se queda corta para una UI más rica con varios idiomas y monedas, y una misma entidad legal puede ser prestataria y prestamista según el país. Esto fuerza cambios rompedores en los datos devueltos y la necesidad de reemplazar las rutas de `/borrower` por algo más general.

## Help Others Handle Your Versions (Ayuda a otros a manejar tus versiones)

Si quieres que respeten tu autonomía, debes respetar la suya: no puedes imponer tu calendario de releases. Esto vale tanto para SaaS en Internet como dentro de una organización o un canal de socios.

### Cambios de API no rompedores

Nygard aplica el principio de robustez de Postel (de la especificación TCP): "Be conservative in what you do, be liberal in what you accept from others." (PDF p. 270). Lo que llamamos "API" es en realidad una pila de acuerdos en capas: handshaking y duración de la conexión, framing de la petición, codificación de contenido, sintaxis del mensaje, semántica del mensaje, y autorización/autenticación. Elegir la familia HTTP aporta algunos acuerdos de serie (los headers `Content-Type` y `Content-Length` ayudan con el framing), pero decir "acepto HTTP" en realidad significa aceptar un subconjunto del estándar, con límites en content types, verbos y códigos de estado.

Un cambio rompedor es cualquier ruptura unilateral de un acuerdo previo. La lista de cambios que rompen incluye:

- Rechazar un protocolo de red que antes funcionaba
- Rechazar framing o codificación de contenido que antes funcionaban
- Rechazar sintaxis de petición que antes funcionaba
- Rechazar enrutamiento de petición (URL o cola) que antes funcionaba
- Añadir campos obligatorios a la petición
- Prohibir información opcional que antes se permitía
- Quitar información de la respuesta que antes se garantizaba
- Exigir un nivel mayor de autorización

Peticiones y respuestas se tratan de forma asimétrica (peticiones covariantes, respuestas contravariantes; también se puede pensar con el principio de sustitución de Liskov). Siempre se puede aceptar más que antes, pero no menos ni exigir más; siempre se puede devolver más, pero no menos. En términos de conjuntos (perspectiva atribuida a Rich Hickey, creador de Clojure), son siempre seguros:

- Requerir un subconjunto de los parámetros antes requeridos
- Aceptar un superconjunto de los parámetros antes aceptados
- Devolver un superconjunto de los valores antes devueltos
- Imponer un subconjunto de las restricciones antes requeridas

### La trampa: la implementación como especificación de facto

Hay un hueco entre lo que decimos que aceptamos y lo que de verdad aceptamos. Si un servicio recibía un campo `url` como string sin validar y luego añades validación con una expresión regular, pasa a rechazar peticiones que antes aceptaba: eso es un cambio rompedor, aunque la documentación dijera "pasa una URL". En cuanto el servicio entra en producción, su implementación se vuelve la especificación de facto. Lo mismo ocurre cuando una entrada aceptable produce un comportamiento inesperado (un caso límite, una colección vacía): no eres libre de cambiarlo aunque nunca pretendieras soportarlo.

Aun así conviene publicar los formatos de mensaje con algo como Swagger/OpenAPI, para que otros programen contra la especificación y para poder aplicar pruebas generadas que fuercen los límites. Hay dos tipos de pruebas: *inbound* (ejercitas tu propia API para confirmar que hace lo que crees) y *outbound* (ejercitas tus dependencias con tus propias pruebas para comprobar que entiendes bien su spec).

En un proyecto del autor, dos equipos separados geográficamente acordaron una especificación y el equipo consumidor escribió pruebas FIT que ilustraban cada caso (pruebas de contrato) corriendo contra el staging del otro equipo. El solo hecho de escribirlas destapó muchos casos límite; casi el 100 % falló en la primera ejecución. Estas pruebas de contrato las posee el servicio que llama y actúan como alerta temprana si el proveedor cambia; funcionó mejor así que si las hubiera escrito el equipo implementador.

### Cambios de API rompedores

Cuando no queda otra, aún puedes ayudar a los consumidores. El primer prerrequisito es poner un número de versión en los formatos de petición y respuesta: es la versión del formato, no de la aplicación, y sirve sobre todo para depurar, no para que el consumidor haga de puente entre versiones. HTTP ofrece varias opciones, ninguna bonita:

1. Añadir un discriminador de versión en la URL (prefijo o query param). Es lo más común. Ventajas: enrutar es fácil, las URLs se comparten/almacenan/envían sin tratamiento especial, puedes consultar logs por versión y el consumidor ve de un vistazo qué versión usa. Desventaja: distintas representaciones de la misma entidad parecen recursos distintos, un no-no en REST.
2. Usar el header `Accept` en GET y `Content-Type` en PUT/POST, con media types como `application/vnd.lendzit.loan-request.v1` y `.v2`. Ventaja: los clientes actualizan sin cambiar rutas. Desventajas: la URL ya no basta, los media types genéricos no ayudan y el soporte de enrutamiento por media type varía según el framework.
3. Usar un header propio como `api-version`. Ventajas: flexibilidad total, ortogonal a URL y media type. Desventajas: hay que escribir helpers de enrutamiento y es "conocimiento secreto" a compartir con los consumidores.
4. Solo para PUT/POST, un campo en el cuerpo que indique la versión. Ventajas: sin enrutamiento, fácil. Desventaja: no cubre todos los casos.

Nygard suele optar por poner algo en la URL: basta por sí sola y los intermediarios (cachés, proxies, balanceadores) no necesitan configuración especial y propensa a errores; importa especialmente cuando la nueva versión implica un cambio de lenguaje o framework y se quiere correr en un clúster separado.

Elijas lo que elijas, como proveedor debes soportar la versión vieja y la nueva durante un tiempo, lado a lado (con despliegue sin downtime). Conviene probar llamadas mezcladas de ambas versiones sobre las mismas entidades: a menudo las entidades creadas con la nueva versión provocan errores 500 al accederlas con la vieja. Si versionas en la URL, sube todas las rutas a la vez aunque solo cambie una. Internamente, para evitar duplicar el código v1 en v2, la preferencia del autor es resolverlo en el controlador: los métodos de la API nueva van directos a la lógica actual y los de la vieja convierten objetos viejos a actuales en las peticiones y actuales a viejos en las respuestas.

## Handle Others' Versions (Maneja las versiones de otros)

Al recibir peticiones no tienes ningún control sobre el formato: alguien te pasará un mensaje erróneo. Lo mismo al llamar a otros servicios, que pueden empezar a rechazar tus peticiones en cualquier momento porque quizá no sigan las reglas de seguridad descritas. Hay que ser defensivo siempre.

En el ejemplo, se añaden campos nuevos: `creditScore` al prestatario, `collateralCategory` al préstamo y un nuevo valor permitido en la lista `riskAdjustments`. Un consumidor puede enviarlos todos, algunos o ninguno; salvo casos raros donde respondes con "bad request", tu función debe aceptar cualquier combinación. ¿Qué haces si llega `collateralCategory` = "mobile home" pero falta la lista de ajustes de riesgo, o si falta el credit score? Todas esas preguntas necesitan respuesta. Como mucho puedes esperar que los campos tengan el tipo sintáctico correcto, y solo si usas una librería de mapeo automática; con JSON crudo ni eso.

Esto refuerza el enfoque de pruebas de contrato. Un fallo común en las pruebas de integración es sobre-especificar la llamada: montar una petición, emitirla y luego afirmar sobre la respuesta usando los datos de la petición original. Eso verifica el bucle actual, pero no que el llamador cumpla el contrato ni que pueda manejar cualquier respuesta permitida; un release del proveedor puede cambiar la respuesta de forma permitida pero inesperada y romper al consumidor. Además, provocar respuestas de error suele requerir flags especiales que tarde o temprano acaban en producción.

Nygard prefiere que cada lado compruebe su propia conformidad con la spec, partiendo la prueba en dos: el *Request Side* comprueba que las peticiones se construyen según los requisitos del proveedor, y el *Response Side* comprueba que el llamador está preparado para manejar sus respuestas (generando una respuesta falsa). Ninguna de las dos invoca el servicio externo; aíslan los fallos de comunicación y hacen el código más robusto al no asumir sin justificación cómo se comporta la otra parte. El software debe seguir siendo cínico: aunque un proveedor jure despliegues sin downtime, protégete con las técnicas de autodefensa de los Stability Patterns.

## Wrapping Up (Cierre)

El versionado es intrínsecamente desordenado y seguirá siendo complejo. Nygard recomienda una filosofía utilitarista: el sufrimiento neto en la organización se minimiza si todos piensan globalmente y actúan localmente. La alternativa es una organización que se frena poco a poco porque cada release queda atada esperando actualizaciones sincronizadas de sus clientes. El capítulo mostró cómo manejar nuestras versiones para ayudar a otros y cómo defendernos de los cambios de versión de consumidores y proveedores.

## Ideas clave

- Respeta la autonomía de tus consumidores: coordinar despliegues no escala, así que la mayoría de versiones deben ser compatibles.
- Una API es una pila de acuerdos en capas; un cambio rompedor es cualquier ruptura unilateral de un acuerdo previo.
- Principio de robustez de Postel: sé conservador en lo que haces y liberal en lo que aceptas; de ahí la asimetría entre peticiones y respuestas.
- Son seguros: requerir un subconjunto de lo requerido, aceptar un superconjunto de lo aceptado, devolver un superconjunto de lo devuelto, imponer un subconjunto de las restricciones.
- Una vez en producción, la implementación se convierte en la especificación de facto: no puedes rechazar entradas que antes aceptabas.
- Ante un cambio rompedor inevitable: versiona los formatos y soporta la versión vieja y la nueva en paralelo; de las opciones HTTP, el autor prefiere la versión en la URL.
- Al recibir, nunca confíes en el formato; acepta cualquier combinación de campos nuevos y define qué hacer ante los que falten.
- Usa pruebas de contrato que cada lado comprueba por separado (request side y response side) y mantén el software cínico y defensivo frente a proveedores y consumidores.
