# Identifying Weak Points in Application Architecture — Estudio

## Tarjetas de repaso

P: ¿Qué cierra la fase de recon según el capítulo? / R: Unir todo lo recopilado (tecnologías, API endpoints, funcionalidad, dominios, configuraciones y sistemas de autenticación/sesión) en notas organizadas para priorizar dónde buscar vulnerabilidades.

P: ¿Cuál es la tesis central del capítulo sobre el origen de las vulnerabilidades? / R: La mayoría de las vulnerabilidades no surgen de métodos mal escritos, sino de una arquitectura de aplicación mal diseñada.

P: ¿Qué diferencia un XSS aislado de vulnerabilidades múltiples? / R: Un solo XSS puede ser un método descuidado, pero vulnerabilidades múltiples delatan una arquitectura débil.

P: ¿Qué funcionalidad comparte toda versión del sistema de mensajería directa (IM)? / R: UI para escribir mensaje, API endpoint que recibe el envío, tabla de BD para almacenarlo, API endpoint para recuperarlo y código UI para mostrarlo.

P: ¿Por qué la versión insegura del IM termina ejecutando un script? / R: Porque no rechaza scripts en el POST, ni en la escritura/lectura de BD, ni filtra el mensaje, de modo que se carga en el DOM como `message <script> alert('hacked');</script>`.

P: ¿Cómo debe implementarse la seguridad según el capítulo, en vez de caso por caso? / R: Abstrayéndola dentro de la arquitectura antes y durante el desarrollo de features, no caso por caso (costoso y fácil de olvidar).

P: ¿Qué hace del método `appendToDOM` un indicador de arquitectura segura? / R: Usa DOMPurify y su flag `unsafe` está desactivado por defecto y es el último parámetro de la firma, así es poco probable activarlo por accidente.

P: ¿En qué capas podía aparecer el riesgo de XSS en el servicio de mensajería? / R: API POST, Database Write, Database Read, API GET y Client Read.

P: ¿Qué principio resume la frase "una aplicación es tan segura como el eslabón más débil de su arquitectura"? / R: Defender en una sola capa deja hueco a nuevos endpoints menos protegidos; la seguridad debe estar en múltiples capas.

P: ¿Qué funcionalidad conviene priorizar al testear según la proporción de mecanismos por capa? / R: La funcionalidad con pocos mecanismos de seguridad o muchas capas (baja proporción de mecanismos por capa), por ser más probablemente explotable.

P: ¿Qué mecanismo específico puede usar el API POST que otras capas no pueden? / R: Invocar un headless browser para simular el renderizado y rechazar el payload si detecta ejecución de script.

P: ¿Cuál es la "regla de oro" sobre reinvención en seguridad? / R: Nunca implementar tu propia criptografía ("never rolling your own cryptography").

P: ¿Por qué se recomienda adoptar SHA-3 en lugar de crear un hashing propio? / R: SHA-3 lleva casi 20 años en desarrollo, probado por el NIST y grandes firmas; replicar ese testing costaría decenas de millones, mientras que adoptarlo (p. ej. vía OpenJDK) cuesta cero.

P: ¿Qué features conviene reinventar y cuáles dejar en paz? / R: Reinventar solo features puramente funcionales (esquema de comentarios, notificaciones); dejar bases de datos, aislamiento de procesos, gestión de memoria y criptografía a los expertos.

## Preguntas de autoevaluación

P: ¿Por qué el análisis arquitectónico es una técnica de recon útil para priorizar ataques? / R: Porque las funcionalidades mal arquitecturadas deben atacarse primero, ya que las bien diseñadas se mantienen consistentes al saltar de un endpoint a otro. (Sección "Lo que necesitas saber")

P: ¿Qué quiere ilustrar el autor al imaginar 10 variaciones del sistema de IM escritas en 5 años? / R: Que cada implementación será estructuralmente distinta, pero los riesgos de seguridad serán en su mayoría los mismos. (Sección "El ejemplo que recorre el capítulo")

P: Según el capítulo, ¿tendría huecos de seguridad una aplicación escrita por expertos en seguridad si su arquitectura fuera insegura? / R: Sí; aun escrita por ingenieros expertos, probablemente tendría huecos con el tiempo si la arquitectura es inherentemente insegura. (Sección "Señales de arquitectura segura vs. insegura")

P: ¿Cómo podría un nuevo endpoint saltarse una protección existente contra XSS? / R: Si solo se sanitiza en el API POST, un endpoint nuevo (p. ej. mensajería masiva con listas de mensajes) con menos saneamiento podría introducir scripts en la BD, esquivando la protección original. (Sección "Múltiples capas de seguridad")

P: ¿Por qué ningún mecanismo de una sola capa es infalible? / R: Porque cada mecanismo detecta payloads diferentes; por ejemplo, un bug en una API del headless browser podría dejar pasar el script y ejecutarse solo en el navegador vulnerable de un usuario real. (Sección "Múltiples capas de seguridad")

P: ¿Por qué el deseo de reinventar tecnología se considera principalmente un problema organizativo? / R: Porque no suele nacer como problema de arquitectura, sino organizativo, aunque se refleja en la arquitectura; tiene ventajas como evitar licencias, añadir funcionalidad y generar publicidad. (Sección "Adopción y reinvención")

P: ¿Qué tipo de aplicaciones suelen ser las más fáciles de vulnerar? / R: Las aplicaciones llenas de bases de datos, criptografía y optimizaciones de hardware a medida. (Sección "Adopción y reinvención")

## Checklist

- [ ] Reunir y organizar las notas de recon (tecnologías, endpoints por verbo HTTP, shapes de API, funcionalidad, dominios, configuraciones, auth/sesión) antes de buscar vulnerabilidades.
- [ ] Identificar si la seguridad está abstraída en la arquitectura o implementada caso por caso.
- [ ] Buscar mecanismos indicadores de arquitectura segura (p. ej. `appendToDOM` con `unsafe` desactivado por defecto) y señalar su ausencia.
- [ ] Mapear las capas de cada funcionalidad (API POST, DB Write, DB Read, API GET, Client Read) y contar los mecanismos de seguridad por capa.
- [ ] Priorizar las funcionalidades con baja proporción de mecanismos por capa o protegidas en una sola capa.
- [ ] Revisar endpoints nuevos o alternativos que puedan saltarse las protecciones existentes.
- [ ] Evaluar caso por caso dónde se ha reinventado tecnología, marcando como riesgo crítico la criptografía propia y verificando el uso de implementaciones probadas (p. ej. SHA-3 vía OpenJDK).
