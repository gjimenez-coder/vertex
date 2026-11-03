# Introduction to Web Application Reconnaissance (Introducción al reconocimiento de aplicaciones web) — Estudio

## Tarjetas de repaso

P: ¿Qué es la web application reconnaissance (recon)? / R: La fase exploratoria de recopilación de datos que suele ocurrir antes de intentar hackear una aplicación web.

P: ¿Quiénes realizan el recon? / R: Hackers, pen testers o bug bounty hunters, pero también sirve a los security engineers para encontrar y parchear mecanismos mal protegidos.

P: ¿Por qué las habilidades de recon por sí solas tienen poco valor? / R: Porque se vuelven muy valiosas solo combinadas con conocimiento ofensivo de hacking y experiencia defensiva en ingeniería de seguridad.

P: ¿Qué revela realmente una UI pública sobre una aplicación? / R: Solo un subconjunto de la funcionalidad; nunca la totalidad de la aplicación.

P: ¿Qué se puede descubrir mediante recon más allá de la UI? / R: APIs y endpoints destinados a usuarios con permisos elevados (admins, moderadores) no visibles desde la interfaz.

P: ¿Qué es RBAC? / R: Role-based access control: una estructura de permisos por niveles que usan la mayoría de aplicaciones que automatizan el acceso a datos.

P: ¿Usan las aplicaciones actuales un único nivel de permisos para todos los usuarios? / R: Muy pocas; casi todas usan permisos por niveles (RBAC).

P: ¿Qué advertencia legal/ética da el libro sobre el recon? / R: Que muchas técnicas pueden marcar tu IP (bans o acciones legales) y solo deben ejecutarse contra aplicaciones propias o con permiso escrito.

P: ¿Qué es un "glitch" en el contexto de comparar permisos? / R: Un fallo que permite a usuarios no privilegiados aprovechar funcionalidad reservada a usuarios privilegiados.

P: ¿Se necesita una UI para hacer recon de una aplicación? / R: No; con reverse engineering de la estructura de las APIs y de los payloads que aceptan se puede mapear sin acceso directo.

P: ¿Qué significa "topography" aplicado a aplicaciones web? / R: El estudio de las características, formas y superficies; en web designa los datos sobre código, estructura de red y funcionalidades.

P: ¿Qué es un "mapa" de la aplicación web? / R: Los datos recopilados sobre el código, la estructura de red y el conjunto de funcionalidades de una aplicación.

P: ¿Qué formato prefiere el autor para documentar el recon y por qué? / R: Un formato tipo JSON, porque las estructuras jerárquicas abundan en web y facilitan ordenar y buscar las notas.

P: ¿Qué importa más que la herramienta o el formato al documentar el recon? / R: El contenido y la estructura: preservar relaciones y jerarquías manteniéndolas legibles y recorribles manualmente.

## Preguntas de autoevaluación

P: ¿Por qué un security engineer querría dominar el recon si es una técnica usada por atacantes? / R: Para encontrar mecanismos mal protegidos y parchearlos antes de que lo haga un actor malicioso. (Lo que necesitas saber)

P: En el ejemplo de MegaBank, ¿qué nivel de acceso tiene un cliente sobre su saldo y qué no puede hacer online? / R: Acceso de lectura (read-only) al saldo; ningún cliente puede crear, modificar o eliminar cuentas online. (El ejemplo que recorre el capítulo)

P: ¿Qué diferencia de permisos existe entre un Teller y un Banker en MegaBank? / R: El Teller crea cuentas nuevas con el papeleo del cliente; el Banker modifica cuentas existentes en nombre de los clientes. (El ejemplo que recorre el capítulo)

P: ¿Por qué el hecho de que un banco grande no pueda contratar desarrolladores para cada operación manual lleva a RBAC? / R: Porque obliga a automatizar el acceso a datos, y esa automatización se estructura con permisos por niveles (RBAC). (Information Gathering)

P: ¿Cómo puede exponerse accidentalmente un servidor interno a una red pública? / R: Al olvidar una sola línea de configuración de red o firewall, un servidor HTTP puede quedar en una red pública en lugar de confinado a la interna. (Information Gathering)

P: ¿Cuál debería ser el primer paso antes de intentar hackear una aplicación y por qué? / R: Construir un mapa de su estructura, organización y funcionalidad, para entenderla a fondo y poder priorizar mejor los ataques. (Web Application Mapping)

P: ¿Qué requisitos debe cumplir el formato elegido para el mapa de recon? / R: Ser fácilmente recorrible y capaz de almacenar la información y las relaciones relevantes, escalando de aplicaciones simples a robustas. (Web Application Mapping)

## Puntos a dominar

- Definir el recon como fase previa al hackeo y explicar por qué su valor depende de combinarlo con hacking ofensivo e ingeniería de seguridad defensiva.
- Razonar que una UI pública solo expone un subconjunto de la aplicación y que existen APIs/endpoints de permisos elevados ocultos.
- Explicar el modelo RBAC y reconocer que casi ninguna aplicación usa un único nivel de permisos.
- Comparar los permisos de admin/moderador con los de un usuario estándar para detectar glitches de escalado de privilegios.
- Entender que se puede mapear una aplicación sin UI mediante reverse engineering de APIs y payloads.
- Reconocer la advertencia ética/legal: ejecutar recon solo contra aplicaciones propias o con permiso escrito.
- Construir un mapa jerárquico del recon (JSON, Notion, XMind) que preserve relaciones y sea fácil de recorrer.
