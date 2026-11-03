# Web Application Security (2nd Edition) — Andrew Hoffman (O'Reilly Media, 2024)
## Capítulo 30 — Defending Against XXE (Defensa contra XXE)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas indican la página del PDF (p. ej. "(PDF p. 401)").

## Lo que necesitas saber
Este capítulo cierra el bloque sobre XXE (XML External Entity) centrándose en cómo defenderse. La tesis central es sencilla: a pesar de lo peligroso que resulta, XXE es fácil de mitigar. En la mayoría de los casos basta con deshabilitar las external entities en el parser de XML, normalmente con una sola línea de configuración.

El capítulo advierte que la aparente simplicidad de la defensa contrasta con lo extendida que sigue estando la vulnerabilidad en producción, sobre todo porque muchos parsers (en especial los basados en Java) traen XXE habilitado por defecto. La recomendación es no asumir nada y verificar siempre la documentación del API del parser.

Además de la mitigación directa, el capítulo plantea una segunda vía: reevaluar el formato de datos. Si la aplicación no necesita XML real, migrar a JSON u otro formato puede eliminar el riesgo de XXE de raíz. Sales sabiendo cómo bloquear XXE, cuándo conviene cambiar de formato de datos y por qué estos ataques son tan peligrosos pese a su fácil remediación.

## Mitigación directa: deshabilitar external entities
La defensa principal es configurar correctamente el parser de XML para que no procese external entities. Es, por lo general, una sola línea de configuración, aunque el mecanismo exacto depende del parser:

```java
factory.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true);
```

Puntos clave:
- OWASP señala que XXE es particularmente peligroso en parsers de XML basados en Java, ya que muchos tienen XXE habilitado por defecto.
- Según el lenguaje y el parser, XXE puede estar deshabilitado por defecto, pero no debe asumirse.
- "Don't just expect it is disabled by default." (PDF p. 401). Siempre revisa la documentación del API del parser.

## Evaluar otros formatos de datos
Según los casos de uso, puede ser posible rediseñar la aplicación para usar otro formato en lugar de XML, simplificando el código y eliminando el riesgo de XXE. El intercambio típico es XML por JSON.

JSON es práctico cuando la aplicación solo envía payloads jerárquicos estándar que casualmente tienen forma de XML. No sirve si la aplicación realmente parsea XML, SVG u otros tipos de archivo derivados de XML.

Comparación XML frente a JSON (Tabla 30-1):

| Categoría | XML | JSON |
|---|---|---|
| Tamaño del payload | Grande | Compacto |
| Complejidad de la especificación | Alta | Baja |
| Facilidad de uso | Requiere parsing complejo | Parsing simple, compatible con JavaScript |
| Soporte de metadata | Sí | No |
| Renderizado (estructura tipo HTML) | Fácil | Difícil |
| Contenido mixto | Soportado | No soportado |
| Validación de esquema | Soportada | No soportada |
| Mapeo de objetos | Ninguno | JavaScript |
| Legibilidad | Baja | Alta |
| Soporte de comentarios | Sí | No |
| Seguridad | Menor | Mayor |

Conclusiones que resalta el texto:
- JSON es un formato mucho más ligero que XML.
- JSON ofrece menos rigidez, pero payloads más rápidos y fáciles de manejar.
- JSON mapea a objetos JavaScript, mientras que XML mapea más de cerca a árboles DOM (el DOM es un formato derivado de XML).

Recomendaciones de uso:
- JSON es alternativa aceptable para cualquier API que maneje datos estructurados ligeros interpretados por JavaScript.
- XML sigue siendo ideal cuando el payload acabará renderizándose, o cuando se requiere una estructura de datos muy rígida (gracias a su schema validation).
- JSON es perfecto para APIs en desarrollo continuo, donde el contrato cliente-servidor no necesita mantenimiento constante.

Los riesgos de seguridad de XML provienen del poder de su especificación y de su capacidad para incorporar archivos externos y multimedia; por eso es naturalmente menos seguro que JSON, que solo almacena pares clave/valor en formato de string. Si la organización no quiere moverse a JSON, el texto menciona YAML, BSON o EDN como alternativas adecuadas, pero que requieren un análisis similar antes de adoptarlas.

## Riesgos avanzados de XXE
Los ataques XXE suelen empezar como ataques de solo lectura (read-only), pero pueden progresar hacia formas más avanzadas. XXE es un ataque "gateway": ofrece al atacante una plataforma de reconocimiento (recon) para acceder a datos que de otro modo serían inaccesibles desde fuera del servidor web.

Con esos datos, otras partes de la aplicación pueden comprometerse más fácilmente. El impacto final puede ir desde acceso de solo lectura hasta remote code execution (RCE) y la toma completa del servidor. Por eso estos ataques son tan peligrosos.

## Resumen del capítulo
El autor justifica incluir XXE en el libro por lo comunes que son los parsers de XML mal configurados en producción y por el nivel de riesgo que representa un ataque de external entity. Aunque suelen ser fáciles de mitigar, siguen estando muy extendidos. De ahí la insistencia en revisar cada configuración de parser antes de publicar cualquier aplicación que use XML o tipos de datos similares a XML. Deben tomarse todas las precauciones al trabajar con un parser de XML del lado servidor para evitar que una vulnerabilidad XXE se cuele por accidente en el código.

## Ideas clave
- XXE es, en general, fácil de defender: basta con deshabilitar las external entities en el parser de XML, a menudo con una sola línea de configuración.
- Muchos parsers de XML basados en Java tienen XXE habilitado por defecto; nunca asumas el valor por defecto y consulta la documentación del API.
- Rediseñar la aplicación hacia otro formato (típicamente JSON) puede eliminar el riesgo de XXE de raíz y simplificar el código.
- JSON conviene para datos estructurados ligeros consumidos por JavaScript; XML sigue siendo mejor si el payload se renderiza o si se necesita rigidez con schema validation.
- XML es menos seguro que JSON porque su especificación permite incorporar archivos externos y multimedia.
- YAML, BSON y EDN son alternativas válidas a JSON, pero requieren un análisis previo similar.
- XXE es un ataque "gateway": empieza en solo lectura y puede escalar a RCE y toma completa del servidor.
- Pese a ser fácil de mitigar, XXE sigue siendo muy común; verifica cada configuración de parser antes de desplegar.
