# Defending Data and Objects (Defendiendo datos y objetos) — Estudio

## Tarjetas de repaso

P: Fuera del almacenamiento en base de datos, ¿de qué dos formas viven los objetos con los que interactúa el código?
R: De forma efímera (en memoria) o persistente (en el sistema de archivos).

P: ¿Por qué muchas defensas pensadas para datos efímeros también protegen los datos en disco?
R: Porque los lenguajes operan principalmente en memoria, así que los datos persistentes suelen cargarse en memoria durante las operaciones.

P: ¿De qué nace un ataque de mass assignment?
R: De confiar en el objeto enviado por el cliente para actualizar campos de la base de datos, pudiendo un usuario malicioso manipularlos.

P: ¿Cuál es la mitigación más simple contra mass assignment?
R: Restringir mediante un allowlist los campos aceptados del cliente, aplicado como validación antes de llamar a db.update().

P: ¿Qué es un Data Transfer Object (DTO) y cómo mitiga mass assignment?
R: Un objeto intermediario usado al pasar datos entre servicios o funciones; al pasar los datos por su constructor, rechaza cualquier parámetro adicional.

P: ¿Cuál es la primera defensa recomendada contra IDOR?
R: Una buena arquitectura: los objetos y archivos nunca deberían referenciarse directamente ni mediante una estructura de API fácil de adivinar.

P: ¿Qué solución combina el capítulo cuando un usuario necesita acceder a un archivo concreto?
R: Enmascarar la llamada de API (para no mostrar el nombre del archivo) con comprobaciones de autorización antes de devolver cada archivo.

P: ¿Qué condiciones deben cumplir los nombres de archivo aleatorios para aportar seguridad frente a IDOR?
R: Que existan otros mecanismos como rate limits y que la entropía sea suficiente para que hagan falta millones de intentos para encontrar otro archivo.

P: ¿Cómo califica el autor el uso de referencias generadas aleatoriamente contra IDOR?
R: Como una mitigación a corto plazo, no la solución ideal, hasta que sea posible una re-arquitectura a largo plazo.

P: ¿Cuál es la raíz de todo ataque de serialización y su mitigación principal?
R: En el núcleo hay una serialización débil; la mitigación principal es usar librerías de serialización y deserialización sólidas y bien probadas.

P: ¿Qué características debe tener la librería de serialización elegida para una aplicación web?
R: Ser open source con millones de usuarios e historial de auditorías de seguridad, usar un formato popular como JSON o YAML y evitar formatos con poco historial.

P: ¿Qué tratamiento requieren los datos que el servidor o el navegador pudieran interpretar como script?
R: Sanitizarse antes de serializar o deserializar; también se puede aplicar allowlist a caracteres de entrada y tipos de objeto.

P: ¿Cuál es la tesis central del capítulo sobre los ataques a datos y objetos?
R: Aunque son un blanco frecuente, son bastante sencillos de defender si se diseña la aplicación teniendo en cuenta estos riesgos desde el principio.

## Preguntas de autoevaluación

P: ¿Qué cuatro clases de ataque enseña a mitigar el capítulo?
R: Mass assignment, IDOR, ataques de serialización y, con ello, por qué una buena arquitectura y librerías sólidas bastan en la mayoría de los casos. (Lo que necesitas saber)

P: En el ejemplo de "MegaGame", ¿por qué es vulnerable el endpoint updatePlayerData?
R: Porque el desarrollador actualiza campos de la base de datos a partir de un objeto (req.body.data) que un usuario malicioso puede manipular. (Defending Against Mass Assignment)

P: ¿Cuáles son las dos defensas generalmente aceptadas contra mass assignment y cómo se diferencian?
R: El allowlist con validación (restringe los campos aceptados, método más sencillo) y el DTO (mitigación más intensiva que rechaza parámetros adicionales al pasar los datos por su constructor). (Validation and Allowlisting; Data Transfer Objects)

P: ¿Por qué no basta con nombres de archivo aleatorios para defenderse de IDOR?
R: Porque solo aportan seguridad si existen mecanismos como rate limits y entropía suficiente; el autor los considera una mitigación a corto plazo frente a una re-arquitectura a largo plazo. (Defending Against IDOR)

P: ¿Qué hay que considerar además de elegir una buena librería al defenderse de ataques de serialización?
R: El tipo de dato a serializar: sanitizar los datos interpretables como script o con caracteres de escape comunes, y poder aplicar allowlist a caracteres y tipos de objeto. (Defending Against Serialization Attacks)

P: Según el resumen, ¿por qué debería dar tranquilidad conocer estos ataques?
R: Porque, aunque parezcan un fallo de los lenguajes de la web, suelen ser fáciles de defender y las mitigaciones están al alcance si se diseña la aplicación con ellos en mente. (Summary)

## Puntos a dominar

- Entender que los objetos viven efímeros (memoria) o persistentes (sistema de archivos) y que muchas defensas sirven para ambos casos.
- Identificar que mass assignment surge de confiar en el objeto enviado por el cliente para actualizar la base de datos.
- Saber aplicar un allowlist de campos como validación antes de escribir en la base de datos.
- Comprender cómo un DTO rechaza parámetros adicionales mediante su constructor.
- Reconocer la buena arquitectura (no referenciar objetos directamente, enmascarar la API, validar autorización) como primera defensa contra IDOR.
- Valorar nombres aleatorios con entropía suficiente y rate limits solo como mitigación a corto plazo frente a IDOR.
- Elegir librerías de serialización open source auditadas y formatos probados como JSON o YAML, evitando formatos sin historial.
- Sanitizar o aplicar allowlist a caracteres y tipos de objeto interpretables como script antes de serializar o deserializar.
