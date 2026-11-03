# Handling Versions (Manejo de versiones) — Estudio

## Tarjetas de repaso

P: ¿Por qué la mayoría de versiones nuevas de un servicio deberían ser compatibles?
R: Porque coordinar despliegues entre consumidor y proveedor no escala; cada consumidor tiene su propio equipo y calendario y no se le puede forzar a publicar al mismo tiempo que nosotros. Un cambio rompedor desencadena un efecto dominó que puede obligar a toda la empresa a actualizar a la vez.

P: ¿Qué principio de robustez aplica Nygard y cómo se enuncia?
R: El principio de robustez de Postel, tomado de la especificación TCP: "Be conservative in what you do, be liberal in what you accept from others."

P: ¿Qué es realmente una "API" según el capítulo?
R: Una pila de acuerdos en capas: handshaking y duración de la conexión, framing de la petición, codificación de contenido, sintaxis del mensaje, semántica del mensaje y autorización/autenticación.

P: ¿Qué es un cambio rompedor (breaking change)?
R: Cualquier ruptura unilateral de un acuerdo previo; por ejemplo rechazar un protocolo, framing, sintaxis o enrutamiento que antes funcionaban, añadir campos obligatorios, prohibir información opcional antes permitida, quitar información garantizada de la respuesta o exigir mayor autorización.

P: ¿Cómo se tratan de forma asimétrica peticiones y respuestas?
R: Peticiones covariantes y respuestas contravariantes: siempre se puede aceptar más que antes (no menos ni exigir más) y siempre se puede devolver más (no menos). También se puede razonar con el principio de sustitución de Liskov.

P: ¿Qué cuatro cambios son siempre seguros (perspectiva de conjuntos atribuida a Rich Hickey)?
R: Requerir un subconjunto de los parámetros antes requeridos, aceptar un superconjunto de los antes aceptados, devolver un superconjunto de los antes devueltos e imponer un subconjunto de las restricciones antes requeridas.

P: ¿Qué significa que "la implementación se vuelve la especificación de facto"?
R: Que en cuanto el servicio entra en producción no eres libre de rechazar entradas que antes aceptabas ni de cambiar comportamientos de casos límite, aunque la documentación dijera otra cosa o nunca pretendieras soportarlos.

P: ¿Qué diferencia hay entre pruebas inbound y outbound?
R: Las inbound ejercitan tu propia API para confirmar que hace lo que crees; las outbound ejercitan tus dependencias con tus propias pruebas para comprobar que entiendes bien su especificación.

P: ¿Qué son las pruebas de contrato y quién las posee?
R: Pruebas que ilustran cada caso de una especificación acordada; las posee el servicio que llama y actúan como alerta temprana si el proveedor cambia. En el proyecto del autor casi el 100 % falló en la primera ejecución al destapar casos límite.

P: ¿Para qué sirve poner un número de versión en los formatos de petición y respuesta?
R: Es la versión del formato (no de la aplicación) y sirve sobre todo para depurar, no para que el consumidor haga de puente entre versiones.

P: ¿Cuáles son las opciones HTTP para discriminar la versión de la API?
R: (1) Discriminador en la URL (prefijo o query param), (2) headers `Accept`/`Content-Type` con media types tipo `application/vnd.lendzit.loan-request.v1`, (3) header propio como `api-version`, (4) un campo de versión en el cuerpo solo para PUT/POST.

P: ¿Qué opción de versionado prefiere Nygard y por qué?
R: Poner algo en la URL: basta por sí sola y los intermediarios (cachés, proxies, balanceadores) no necesitan configuración especial y propensa a errores; importa sobre todo si la nueva versión cambia de lenguaje o framework y corre en un clúster separado.

P: ¿Cómo evita el autor duplicar código v1 en v2?
R: Resolviéndolo en el controlador: los métodos de la API nueva van directos a la lógica actual y los de la vieja convierten objetos viejos a actuales en las peticiones y actuales a viejos en las respuestas.

P: Al recibir peticiones con campos nuevos, ¿qué debe hacer tu función?
R: Salvo casos raros donde respondes "bad request", debe aceptar cualquier combinación de campos (todos, algunos o ninguno) y definir qué hacer ante los que falten; como mucho se puede esperar el tipo sintáctico correcto, y solo con una librería de mapeo automática.

P: ¿Cómo divide Nygard las pruebas de contrato para no sobre-especificar?
R: En dos lados que no invocan el servicio externo: el Request Side comprueba que las peticiones se construyen según los requisitos del proveedor, y el Response Side comprueba que el llamador maneja cualquier respuesta permitida (generando una respuesta falsa).

## Preguntas de autoevaluación

P: ¿Por qué es mejor que tu equipo haga trabajo extra para mantener compatibilidad en vez de forzar a otros a migrar?
R: Porque si tu equipo genera trabajo para varios equipos, algo va mal; trasladar los costes de migración a otros no respeta su autonomía ni escala. (Sección: Lo que necesitas saber)

P: ¿Por qué añadir validación con una expresión regular a un campo `url` antes aceptado como string es un cambio rompedor?
R: Porque pasa a rechazar peticiones que antes aceptaba, y una vez en producción la implementación es la especificación de facto, aunque la documentación dijera "pasa una URL". (Sección: La trampa: la implementación como especificación de facto)

P: ¿Qué requisitos del ejemplo peer-to-peer fuerzan cambios rompedores?
R: Una UI más rica con varios idiomas y monedas deja corta la representación de la solicitud, y que una misma entidad legal pueda ser prestataria y prestamista según el país obliga a reemplazar las rutas de `/borrower` por algo más general. (Sección: El ejemplo que recorre el capítulo)

P: ¿Qué desventaja tiene versionar en la URL desde la óptica REST?
R: Que distintas representaciones de la misma entidad parecen recursos distintos, lo cual es un no-no en REST. (Sección: Cambios de API rompedores)

P: Cuando mantienes la versión vieja y la nueva en paralelo, ¿qué conviene probar y qué problema aparece a menudo?
R: Probar llamadas mezcladas de ambas versiones sobre las mismas entidades; a menudo las entidades creadas con la versión nueva provocan errores 500 al accederlas con la vieja. (Sección: Cambios de API rompedores)

P: ¿Cuál es el fallo común al sobre-especificar una prueba de integración?
R: Montar una petición, emitirla y afirmar sobre la respuesta usando los datos de la petición original: verifica el bucle actual pero no que el llamador cumpla el contrato ni que maneje cualquier respuesta permitida; un cambio permitido pero inesperado del proveedor puede romper al consumidor. (Sección: Handle Others' Versions)

P: ¿Por qué el software debe seguir siendo "cínico" aunque un proveedor prometa despliegues sin downtime?
R: Porque no tienes control sobre el formato que recibes ni garantía de que el proveedor siga las reglas; hay que protegerse con las técnicas de autodefensa de los Stability Patterns y no asumir sin justificación cómo se comporta la otra parte. (Sección: Handle Others' Versions)

P: ¿Qué filosofía recomienda Nygard para el versionado en una organización?
R: Una filosofía utilitarista: el sufrimiento neto se minimiza si todos piensan globalmente y actúan localmente; la alternativa es una organización que se frena porque cada release queda atada a actualizaciones sincronizadas de sus clientes. (Sección: Wrapping Up)

## Checklist

- [ ] Antes de cambiar una API, verifica que solo requieres un subconjunto de lo antes requerido, aceptas un superconjunto de lo aceptado, devuelves un superconjunto de lo devuelto e impones un subconjunto de las restricciones.
- [ ] Revisa la lista de cambios rompedores (protocolo, framing, sintaxis, enrutamiento, campos obligatorios, información opcional, respuesta garantizada, nivel de autorización) para confirmar que tu cambio no rompe ninguno.
- [ ] Publica los formatos de mensaje con Swagger/OpenAPI para que otros programen contra la especificación.
- [ ] Escribe pruebas inbound (tu propia API) y outbound (tus dependencias), y mantén pruebas de contrato en el lado que llama.
- [ ] Si el cambio es rompedor, añade un número de versión al formato de petición y respuesta.
- [ ] Elige un mecanismo de versionado (URL, media types `Accept`/`Content-Type`, header `api-version` o campo en el cuerpo para PUT/POST); por defecto, versiona en la URL.
- [ ] Soporta la versión vieja y la nueva en paralelo con despliegue sin downtime y sube todas las rutas a la vez si versionas en la URL.
- [ ] Prueba llamadas mezcladas de ambas versiones sobre las mismas entidades para detectar errores 500.
- [ ] Centraliza la conversión entre versiones en el controlador para no duplicar código.
- [ ] Al recibir peticiones, acepta cualquier combinación de campos nuevos y define el comportamiento ante campos ausentes.
- [ ] Divide las pruebas de contrato en Request Side y Response Side sin invocar el servicio externo.
- [ ] Aplica los Stability Patterns de autodefensa frente a proveedores y consumidores.
