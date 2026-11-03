# Características del buen diseño — Estudio

## Tarjetas de repaso

P: ¿En torno a qué dos preocupaciones prácticas gira un buen diseño de software?
R: La reutilización de código y la extensibilidad, porque determinan costo, tiempo de desarrollo y la capacidad de sobrevivir al cambio.

P: ¿Por qué son valiosos los parámetros de costo y tiempo al desarrollar software?
R: Dedicar menos tiempo permite entrar antes al mercado que la competencia, y costos más bajos dejan más dinero para marketing y alcance a clientes potenciales.

P: ¿Cómo ayuda la reutilización de código a reducir costos?
R: En lugar de desarrollar algo una y otra vez desde el principio, se reutiliza el código existente en nuevos proyectos.

P: ¿Qué factores dificultan la reutilización de código?
R: Los acoplamientos fuertes entre componentes, las dependencias de clases concretas en lugar de interfaces y las operaciones incrustadas en el código.

P: ¿Qué aportan los patrones de diseño a la reutilización y a qué precio?
R: Aumentan la flexibilidad de los componentes y los hacen más fáciles de reutilizar, aunque a veces a costa de complicarlos.

P: ¿Cuáles son los tres niveles de reutilización según Erich Gamma?
R: Clases (nivel más bajo), patrones (nivel intermedio) y frameworks (nivel superior); el nivel aumenta en ese orden.

P: ¿Qué se reutiliza en el nivel de clases?
R: Bibliotecas de clases, contenedores y quizá algunos "equipos" de clases, como contenedor/iterador.

P: ¿Qué son los patrones en la escala de reutilización?
R: Son más pequeños y abstractos que los frameworks; una descripción de cómo pueden relacionarse e interactuar un par de clases entre sí.

P: ¿Qué hace un framework?
R: Destila decisiones de diseño, identifica las abstracciones clave para resolver un problema, las representa con clases y define relaciones entre ellas.

P: ¿Qué ejemplo de framework usa el capítulo y qué elementos define?
R: JUnit, el "¡Hola, mundo!" de los frameworks, con `Test`, `TestCase`, `TestSuite` y sus relaciones.

P: ¿En qué consiste el principio de Hollywood?
R: "No nos llames, nosotros te llamamos a ti": el framework permite definir el comportamiento personalizado y te llama cuando llega tu turno de actuar.

P: ¿Por qué los patrones ofrecen reutilización menos arriesgada que los frameworks?
R: Crear un framework comprende alto riesgo e inversión considerable; los patrones permiten reutilizar ideas y conceptos de diseño con independencia del código concreto.

P: ¿Por qué el cambio es inevitable en la vida de un programador?
R: Porque comprendemos mejor el problema al resolverlo, porque algo fuera de nuestro control cambia y porque los requisitos del cliente se mueven.

P: ¿Cómo reaccionan los desarrolladores experimentados ante la inevitabilidad del cambio?
R: Se preparan para posibles cambios futuros cuando diseñan la arquitectura de una aplicación.

P: ¿Qué relación tienen los principios universales de diseño con los patrones del libro?
R: La mayoría de los patrones de diseño tratados en el libro se basa en estos principios universales.

## Preguntas de autoevaluación

P: ¿Qué dos cualidades definen principalmente la calidad de un buen diseño y por qué importan?
R: La reutilización de código y la extensibilidad, porque impactan directamente en costo y tiempo y en la capacidad de la aplicación de sobrevivir al cambio. (Sección "Lo que necesitas saber")

P: Si reutilizar código parece simple sobre el papel, ¿por qué resulta difícil en la práctica?
R: Porque hacer que el código existente funcione en un contexto nuevo requiere esfuerzo adicional, agravado por acoplamientos fuertes, dependencias de clases concretas y operaciones incrustadas. (Sección "Reutilización de código")

P: Describe cómo cambia el nivel de reutilización al pasar de clases a frameworks.
R: Aumenta: las clases son el nivel más bajo, los patrones el intermedio y los frameworks el superior; los frameworks ofrecen más reutilización pero con mayor riesgo e inversión. (Sección "Los tres niveles de reutilización")

P: ¿Cómo se "engancha" un desarrollador a un framework y qué principio lo rige?
R: Creando subclases; el framework define el comportamiento personalizado y lo llama cuando corresponde, siguiendo el principio de Hollywood. (Sección "Los tres niveles de reutilización")

P: Enumera las tres razones por las que el cambio es inevitable.
R: 1) Comprendemos mejor el problema al resolverlo; 2) algo fuera de nuestro control ha cambiado; 3) los requisitos del cliente se mueven ("los postes de la portería se mueven"). (Sección "Extensibilidad")

P: ¿Qué ejemplo da el capítulo de un cambio externo fuera del control del desarrollador?
R: Quienes se basaron en Flash para una aplicación online tuvieron que rehacer o migrar su código cuando los navegadores dejaron de soportar Flash. (Sección "Extensibilidad")

P: Según el capítulo, ¿qué lado positivo tiene que un cliente pida cambios en tu aplicación?
R: Significa que la aplicación todavía le importa a alguien; además, la primera versión demostró que aún es posible mucho más. (Sección "Extensibilidad")

P: ¿Por qué el capítulo no da una única definición de "buen diseño"?
R: Porque las respuestas varían según el tipo de aplicación, aunque existen principios universales que ayudan a responderlas para cada proyecto. (Sección "Principios del diseño")

## Puntos a dominar

- Explicar por qué reutilización y extensibilidad son los ejes del buen diseño y su relación con costo y tiempo.
- Identificar qué factores (acoplamiento fuerte, dependencias de clases concretas, operaciones incrustadas) dificultan la reutilización.
- Distinguir los tres niveles de reutilización de Gamma —clases, patrones, frameworks— y ordenarlos por grado de reutilización.
- Situar los patrones en el nivel intermedio como descripción de interacción entre un par de clases, con menos riesgo que un framework.
- Explicar el principio de Hollywood y cómo uno se engancha a un framework mediante subclases, con JUnit como ejemplo.
- Reconocer las tres razones de la inevitabilidad del cambio y por qué se diseña anticipándolo.
- Recordar que existen principios universales de diseño que sustentan la mayoría de los patrones del libro.
