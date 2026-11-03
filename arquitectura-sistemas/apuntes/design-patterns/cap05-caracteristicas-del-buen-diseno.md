# Dive Into Design Patterns — Alexander Shvets (Refactoring.Guru, 2021)
## Capítulo 5 — Características del buen diseño (Features of good design)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF (con palabras pegadas por la justificación) y las citas usan la página del PDF.

## Lo que necesitas saber

Antes de entrar en los patrones propiamente dichos, el capítulo discute el proceso de diseño de arquitectura de software: qué buscar y qué evitar. La tesis es que un buen diseño gira en torno a dos preocupaciones prácticas: la reutilización de código y la extensibilidad, porque ambas determinan el costo y el tiempo de desarrollo, y la capacidad de una aplicación para sobrevivir al cambio.

Sales sabiendo por qué reutilizar código no es tan sencillo como parece, cómo encajan clases, patrones y frameworks en una escala de reutilización, por qué el cambio es inevitable en la vida de un programador, y que existen principios universales de diseño en los que se basa la mayoría de los patrones del libro.

## Reutilización de código

Costos y tiempo son dos de los parámetros más valiosos al desarrollar software: dedicar menos tiempo permite entrar antes al mercado que la competencia, y costos más bajos dejan más dinero para marketing y alcance a clientes potenciales. La reutilización de código es una de las formas más habituales de reducir costos: en lugar de desarrollar algo una y otra vez desde el principio, se reutiliza el código existente en nuevos proyectos.

La idea se ve bien sobre el papel, pero hacer que el código existente funcione en un contexto nuevo suele requerir un esfuerzo adicional. Acoplamientos fuertes entre componentes, dependencias de clases concretas en lugar de interfaces y operaciones incrustadas en el código reducen la flexibilidad y dificultan la reutilización.

Utilizar patrones de diseño es una de las maneras de aumentar la flexibilidad de los componentes y hacerlos más fáciles de reutilizar, aunque esto a veces tiene el precio de complicar los componentes.

### Los tres niveles de reutilización (Erich Gamma)

El capítulo recoge la visión de Erich Gamma, uno de los padres fundadores de los patrones de diseño, quien distingue tres niveles de reutilización:

- **Clases (nivel más bajo):** se reutilizan bibliotecas de clases, contenedores y quizá algunos "equipos" de clases, como contenedor/iterador.
- **Patrones (nivel intermedio):** son más pequeños y abstractos que los frameworks. En realidad son una descripción sobre cómo pueden relacionarse e interactuar un par de clases entre sí.
- **Frameworks (nivel superior):** intentan destilar las decisiones de diseño, identifican las abstracciones clave para resolver un problema, las representan con clases y definen relaciones entre ellas. JUnit es un pequeño framework —el "¡Hola, mundo!" de los frameworks— con `Test`, `TestCase`, `TestSuite` y sus relaciones definidas.

Un framework suele ser más tosco que una única clase, y uno se engancha a él creando subclases. Utilizan el **principio de Hollywood**: "no nos llames, nosotros te llamamos a ti". El framework permite definir el comportamiento personalizado y te llama cuando llega tu turno de hacer algo; lo mismo ocurre con JUnit.

El nivel de reutilización aumenta al pasar de clases a patrones y por último a frameworks. Lo bueno de la capa intermedia es que los patrones ofrecen la reutilización de un modo menos arriesgado que los frameworks: crear un framework comprende un alto riesgo y una inversión considerable, mientras que los patrones permiten reutilizar ideas y conceptos de diseño con independencia del código concreto.

## Extensibilidad

El cambio es lo único constante en la vida de un programador. El capítulo lo ilustra con ejemplos:

- Lanzaste un videojuego para Windows, pero ahora la gente demanda una versión macOS.
- Creaste un framework GUI con botones cuadrados, pero meses después los botones redondos son tendencia.
- Diseñaste una arquitectura para un sitio de comercio electrónico, pero poco después los clientes piden una función para aceptar pedidos por teléfono.

Hay varias razones por las que el cambio es inevitable:

1. **Comprendemos mejor el problema al resolverlo.** A menudo, para cuando terminamos la primera versión, estamos listos para reescribirla desde el principio porque entendemos mucho mejor diversos aspectos del problema. Además, creciste profesionalmente y tu propio código te parece basura.
2. **Algo fuera de tu control ha cambiado.** Por eso tantos equipos saltan de sus ideas originales hacia algo nuevo. Quienes se basaron en Flash para una aplicación online han rehecho o migrado su código desde que, navegador tras navegador, todos dejaron de soportar Flash.
3. **Los postes de la portería se mueven.** El cliente quedó encantado con la versión actual, pero ahora quiere once "pequeños" cambios para que haga otras cosas que nunca mencionó en las primeras sesiones de planificación. No son cambios frívolos: tu excelente primera versión le ha demostrado que todavía es posible mucho más. El lado positivo: si alguien te pide cambiar algo de tu aplicación, eso significa que todavía le importa a alguien.

Por este motivo, todos los desarrolladores experimentados se preparan para posibles cambios futuros cuando diseñan la arquitectura de una aplicación.

## Principios del diseño

El capítulo cierra planteando las grandes preguntas: ¿qué es un buen diseño de software?, ¿cómo medimos su calidad?, ¿qué prácticas debemos llevar a cabo para lograrlo?, ¿cómo hacemos nuestra arquitectura flexible, estable y fácil de comprender?

Las respuestas varían según el tipo de aplicación que estés creando. No obstante, existen varios principios universales del diseño de software que pueden ayudarte a responder estas preguntas para tu propio proyecto. La mayoría de los patrones de diseño tratados en el libro se basa en estos principios.

## Ideas clave

- El buen diseño se evalúa sobre todo por su reutilización y su extensibilidad, que impactan directamente en costo y tiempo.
- Reutilizar código parece simple, pero el acoplamiento fuerte, las dependencias de clases concretas y las operaciones incrustadas lo dificultan.
- Gamma define tres niveles de reutilización: clases, patrones y frameworks; el nivel aumenta en ese orden.
- Los patrones ocupan el nivel intermedio: describen cómo interactúan un par de clases y ofrecen reutilización con menos riesgo que un framework.
- Los frameworks aplican el principio de Hollywood ("no nos llames, nosotros te llamamos a ti"); te enganchas a ellos mediante subclases.
- El cambio es constante: mejor comprensión del problema, factores externos y requisitos movibles obligan a rediseñar.
- Los desarrolladores experimentados diseñan anticipando cambios futuros.
- Existen principios universales de diseño que sustentan la mayoría de los patrones del libro.
