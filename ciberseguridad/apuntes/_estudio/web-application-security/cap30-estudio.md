# Defending Against XXE (Defensa contra XXE) — Estudio

## Tarjetas de repaso

P: ¿Cuál es la tesis central del capítulo sobre XXE?
R: Pese a lo peligroso que resulta, XXE es fácil de mitigar; en la mayoría de los casos basta con deshabilitar las external entities en el parser de XML.

P: ¿Cuál es la defensa principal y directa contra XXE?
R: Configurar correctamente el parser de XML para que no procese external entities, normalmente con una sola línea de configuración.

P: ¿Qué línea de configuración ilustra la mitigación en un parser Java?
R: `factory.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true);`

P: ¿Qué advierte OWASP sobre los parsers basados en Java?
R: Que XXE es particularmente peligroso en ellos, ya que muchos traen XXE habilitado por defecto.

P: ¿Por qué no se debe asumir que XXE está deshabilitado por defecto?
R: Porque depende del lenguaje y del parser; hay que revisar siempre la documentación del API ("Don't just expect it is disabled by default", PDF p. 401).

P: ¿Cuál es la segunda vía de defensa que plantea el capítulo además de la mitigación directa?
R: Reevaluar el formato de datos: si la aplicación no necesita XML real, migrar a otro formato (típicamente JSON) elimina el riesgo de XXE de raíz.

P: ¿Cuándo es JSON una alternativa aceptable a XML?
R: Cuando la aplicación solo envía payloads jerárquicos estándar con forma de XML y maneja datos estructurados ligeros interpretados por JavaScript.

P: ¿Cuándo NO sirve migrar a JSON?
R: Cuando la aplicación realmente parsea XML, SVG u otros tipos de archivo derivados de XML.

P: ¿A qué mapea JSON y a qué mapea XML?
R: JSON mapea a objetos JavaScript; XML mapea más de cerca a árboles DOM (el DOM es un formato derivado de XML).

P: ¿Por qué XML es naturalmente menos seguro que JSON?
R: Porque su especificación es potente y permite incorporar archivos externos y multimedia, mientras que JSON solo almacena pares clave/valor en formato string.

P: ¿Qué alternativas a JSON menciona el texto si la organización no quiere migrar a JSON?
R: YAML, BSON o EDN, aunque requieren un análisis similar antes de adoptarlas.

P: ¿Por qué se describe XXE como un ataque "gateway"?
R: Porque ofrece al atacante una plataforma de reconocimiento (recon) para acceder a datos inaccesibles desde fuera, y con ellos comprometer otras partes de la aplicación.

P: ¿Hasta dónde puede escalar el impacto de un ataque XXE?
R: Desde acceso de solo lectura (read-only) hasta remote code execution (RCE) y la toma completa del servidor.

P: ¿Cuándo sigue siendo XML la mejor opción frente a JSON?
R: Cuando el payload acabará renderizándose o cuando se requiere una estructura de datos muy rígida gracias a su schema validation.

## Preguntas de autoevaluación

P: ¿Por qué, siendo tan fácil de mitigar, XXE sigue estando muy extendido en producción?
R: Porque muchos parsers (en especial los basados en Java) traen XXE habilitado por defecto y los desarrolladores asumen la configuración por defecto sin verificarla. (Sección "Mitigación directa: deshabilitar external entities" y "Resumen del capítulo")

P: Según la Tabla 30-1, ¿qué ventajas tiene JSON frente a XML en tamaño, legibilidad y seguridad?
R: JSON tiene payload compacto (XML grande), legibilidad alta (XML baja) y mayor seguridad (XML menor). (Sección "Evaluar otros formatos de datos")

P: ¿Qué capacidades conserva XML que JSON no soporta según la comparación?
R: Soporte de metadata, contenido mixto, validación de esquema (schema validation) y soporte de comentarios. (Sección "Evaluar otros formatos de datos", Tabla 30-1)

P: Para una API en desarrollo continuo donde el contrato cliente-servidor cambia, ¿qué formato recomienda el texto y por qué?
R: JSON, porque es perfecto cuando el contrato no necesita mantenimiento constante y maneja datos estructurados ligeros. (Sección "Evaluar otros formatos de datos")

P: ¿De dónde provienen concretamente los riesgos de seguridad de XML?
R: Del poder de su especificación y de su capacidad para incorporar archivos externos y multimedia. (Sección "Evaluar otros formatos de datos")

P: ¿Por qué un ataque que empieza en solo lectura puede ser tan peligroso?
R: Porque XXE actúa como plataforma de recon; con los datos obtenidos se comprometen otras partes de la aplicación, pudiendo escalar hasta RCE y toma total del servidor. (Sección "Riesgos avanzados de XXE")

P: ¿Qué recomendación de proceso da el autor antes de desplegar una aplicación que use XML?
R: Revisar y verificar cada configuración de parser y tomar todas las precauciones al trabajar con un parser de XML del lado servidor. (Sección "Resumen del capítulo")

## Checklist

- [ ] Deshabilitar las external entities en el parser de XML (p. ej. `disallow-doctype-decl` en parsers Apache/Java).
- [ ] No asumir el valor por defecto: consultar la documentación del API del parser para confirmar que XXE está deshabilitado.
- [ ] Prestar atención especial a parsers basados en Java, que suelen traer XXE habilitado por defecto.
- [ ] Evaluar si la aplicación necesita XML real o si puede migrar a JSON para eliminar el riesgo de raíz.
- [ ] Antes de migrar, comprobar que no se parsea XML, SVG u otros tipos derivados de XML (donde JSON no sirve).
- [ ] Si se considera otra alternativa (YAML, BSON, EDN), realizar un análisis previo similar al de JSON.
- [ ] Verificar cada configuración de parser antes de publicar cualquier aplicación que use XML o tipos de datos similares.
