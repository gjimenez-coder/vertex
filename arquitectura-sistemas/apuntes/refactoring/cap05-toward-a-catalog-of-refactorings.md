# Refactoring: Improving the Design of Existing Code — Martin Fowler (con Kent Beck, John Brant, William Opdyke y Don Roberts) (Addison-Wesley, 1999)
## Capítulo 5 — Toward a Catalog of Refactorings (Hacia un catálogo de refactorizaciones)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas usan la página del PDF `(PDF p. N)`.

## Lo que necesitas saber

Este capítulo es la puerta de entrada al catálogo de refactorizaciones que ocupa los capítulos 5 a 12. Fowler explica que el catálogo nació de las notas que fue tomando al refactorizar durante años y advierte que no es ni exhaustivo ni infalible, sino un punto de partida sólido para el trabajo propio del lector.

La tesis central es doble: primero, presentar el formato estándar con que se describe cada refactorización para que el catálogo funcione como material de referencia; y segundo, dar contexto honesto sobre el alcance, las convenciones de código y el grado de madurez de estas técnicas. Sales sabiendo cómo leer una entrada del catálogo, cómo localizar referencias de forma fiable antes de refactorizar y qué limitaciones asumir al aplicar las recetas.

## Formato de las refactorizaciones

Cada refactorización se describe con un formato de cinco partes:

- **Nombre (name)**: importante para construir un vocabulario de refactorizaciones; es el nombre que se usa en el resto del libro.
- **Resumen (summary)**: breve descripción de la situación en que se necesita y de lo que hace la refactorización, para encontrarla rápido. Incluye un enunciado corto del problema, qué se hace, y un boceto con un ejemplo simple de antes y después, en código o en UML según lo que mejor transmita la esencia. Todos los diagramas UML del libro se dibujan desde la perspectiva de implementación.
- **Motivación (motivation)**: por qué conviene hacer la refactorización y en qué circunstancias no conviene hacerla.
- **Mecánica (mechanics)**: descripción concisa, paso a paso, de cómo llevarla a cabo. Es deliberadamente escueta, sin explicar por qué cada paso es así; sirve como recordatorio y checklist cuando ya se conoce la técnica.
- **Ejemplos (examples)**: uso muy simple que ilustra cómo funciona, con las explicaciones más extensas que faltan en la mecánica.

Fowler escribe la mecánica con pasos lo más pequeños posible y enfatiza la forma segura: dar pasos muy pequeños y probar después de cada uno. En su trabajo suele dar pasos más grandes, pero si aparece un bug retrocede y vuelve a los pasos pequeños.

Sobre los ejemplos: son del tipo "de libro de texto", deliberadamente simples, pensados solo para ilustrar la refactorización en discusión y no como buen diseño de objetos de negocio. En la mayoría de casos el código sigue teniendo problemas al final, porque corregirlos exige otras refactorizaciones; cada entrada se mantiene autocontenida porque su papel principal es ser referencia. No deben tomarse como sugerencias de cómo diseñar objetos de empleado o pedido.

Convenciones de código destacadas:

- En los ejemplos usa `double` para representar valores monetarios solo por simplicidad; desaconseja firmemente usar `double` para dinero en software comercial y recomienda el patrón Quantity.
- La mayoría de ejemplos usan Java 1.1 (la versión más usada comercialmente al escribir el libro), lo que se nota sobre todo en el uso de colecciones. Cuando una refactorización difiere en Java 2 —como Encapsulate Collection— explica ambos casos.
- Usa código en negrita para resaltar el código cambiado cuando queda oculto entre código sin cambios; no lo aplica a todo el código modificado porque demasiada negrita anula el propósito.

## Encontrar referencias (Finding References)

Muchas refactorizaciones piden encontrar todas las referencias a un método, un campo o una clase. Conviene apoyarse en la computadora para reducir las posibilidades de pasar por alto una referencia y hacerlo más rápido que inspeccionando el código a ojo.

- Como la mayoría de lenguajes tratan los programas como archivos de texto, la mejor ayuda es una búsqueda de texto adecuada. El control de acceso de la característica buscada indica el rango de archivos a revisar.
- No buscar y reemplazar a ciegas: inspeccionar cada referencia para confirmar que de verdad se refiere a lo que se está reemplazando. Reusar el mismo nombre de método en distintas clases, o métodos con firmas distintas en la misma clase, aumenta las probabilidades de equivocarse.
- En un lenguaje fuertemente tipado se puede dejar que el compilador ayude: eliminar la característica antigua y dejar que el compilador encuentre las referencias colgantes, que atrapará todas. Pero esta técnica tiene problemas:
  1. El compilador se confunde cuando una característica se declara más de una vez en una jerarquía de herencia, sobre todo con métodos sobrescritos varias veces; en una jerarquía conviene usar la búsqueda de texto.
  2. El compilador puede ser demasiado lento; entonces se usa primero la búsqueda de texto y el compilador sirve de doble verificación. Esto solo sirve cuando se piensa eliminar la característica; si se quieren ver todos los usos para decidir qué hacer, hay que usar la búsqueda de texto.
  3. El compilador no detecta usos de la API de reflexión, una razón para desconfiar de la reflexión. Con reflexión hay que buscar por texto y poner más peso en las pruebas.
- Algunos entornos Java, como VisualAge de IBM, siguen el ejemplo del navegador de Smalltalk: usan opciones de menú para encontrar referencias en lugar de búsquedas de texto, y guardan el código en una base de datos en memoria en vez de archivos de texto.

## ¿Qué tan maduras son estas refactorizaciones? (How Mature Are These Refactorings?)

Fowler reflexiona sobre el dilema de cuándo publicar: publicar pronto difunde las ideas antes, pero publicar ideas a medio cocer puede causar problemas a quienes las usen. Sus matizaciones:

- La técnica básica —pasos pequeños y pruebas frecuentes— está bien probada durante años, especialmente en la comunidad Smalltalk, por lo que la idea de fondo del refactoring es muy estable.
- Las refactorizaciones son sus notas sobre las que usa; las ha usado todas. Pero hay diferencia entre usar una refactorización y destilarla en pasos mecánicos, y pocas personas han trabajado desde esos pasos para detectar problemas en circunstancias muy específicas. Hay que ser consciente de lo que se hace y adaptar las recetas, como con una receta de cocina.
- Están descritas pensando en software de un solo proceso. Espera ver en el futuro refactorizaciones para programación concurrente y distribuida, que serán diferentes: por ejemplo, en un solo proceso las llamadas a método son baratas, pero en software distribuido hay que minimizar los round trips.
- Muchas refactorizaciones —como Replace Type Code with State/Strategy y Form Template Method— tratan de introducir patrones en un sistema. Hay una relación natural entre patrones y refactorizaciones: los patrones son adonde se quiere llegar; las refactorizaciones son maneras de llegar allí. Cita a la Banda de los Cuatro: "Design Patterns … provide targets for your refactorings" (PDF p. 87). El catálogo no cubre todos los patrones conocidos ni todos los de la Banda de los Cuatro, otra muestra de su carácter incompleto.

El cierre insiste en que el catálogo es un punto de partida: aunque imperfecto, es útil y mejora la capacidad de refactorizar con eficiencia. Anima al lector a desarrollar sus propias refactorizaciones a partir de los ejemplos y a enviárselas por correo.

## Ideas clave

- El catálogo (caps. 5-12) es un punto de partida de referencia, no una colección exhaustiva ni infalible.
- Cada refactorización tiene cinco partes: nombre, resumen, motivación, mecánica y ejemplos.
- La mecánica usa pasos lo más pequeños posible y la regla de oro es probar tras cada paso; los pasos sirven también como checklist.
- Los ejemplos son deliberadamente simples e ilustran una sola refactorización; el código final suele seguir teniendo problemas que exigen otras refactorizaciones.
- Convenciones: `double` para dinero solo por simplicidad (desaconsejado en producción, mejor el patrón Quantity), ejemplos en Java 1.1 con notas para Java 2, y negrita para resaltar cambios.
- Para encontrar referencias, apoyarse en el ordenador: búsqueda de texto inspeccionando cada caso, o el compilador en lenguajes tipados, con cautela ante herencia, lentitud y reflexión.
- El refactoring básico (pasos pequeños y pruebas) es muy estable; las recetas están pensadas para software de un solo proceso y deben adaptarse.
- Patrones y refactorizaciones se complementan: los patrones son el destino, las refactorizaciones el camino.
