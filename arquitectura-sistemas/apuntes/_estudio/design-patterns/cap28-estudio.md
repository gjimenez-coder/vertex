# Iterator (Iterador) — Estudio

## Tarjetas de repaso

P: ¿Qué tipo de patrón de diseño es Iterator y qué permite hacer?
R: Es un patrón de comportamiento que permite recorrer los elementos de una colección sin exponer su representación subyacente (lista, pila, árbol, grafo, etc.).

P: ¿Cuál es la idea central del patrón Iterator?
R: Extraer el comportamiento de recorrido de una colección y colocarlo en un objeto independiente llamado iterador.

P: ¿Qué problema provoca mezclar los algoritmos de recorrido con la colección?
R: Nubla la responsabilidad principal de la colección (el almacenamiento eficiente de la información) y acopla el código cliente a clases concretas.

P: ¿Por qué pueden varios iteradores recorrer la misma colección de forma independiente y simultánea?
R: Porque cada iterador encapsula su propio estado de recorrido, como la posición actual y cuántos elementos quedan hasta el final.

P: ¿Qué métodos típicos conforman la interfaz iteradora común del capítulo?
R: `getNext()`, que extrae el siguiente elemento, y `hasMore()`, que indica si quedan elementos; el cliente ejecuta el método principal hasta que no devuelve nada.

P: ¿Por qué todos los iteradores deben implementar la misma interfaz?
R: Para que el código cliente sea compatible con cualquier tipo de colección o algoritmo de recorrido.

P: ¿Qué papel juega la Colección respecto a los iteradores?
R: Actúa como fábrica: declara uno o varios métodos que devuelven iteradores, con la interfaz iteradora como tipo de retorno, y puede ofrecer distintos tipos de recorrido.

P: ¿Cómo se añade una nueva forma de recorrer una colección sin romper el código?
R: Se crea una nueva clase iteradora sin cambiar la colección ni el cliente, respetando el principio abierto/cerrado.

P: ¿Qué hacen los iteradores `amigos` y `colegas` del ejemplo de Facebook?
R: `amigos` recorre los amigos de un perfil; `colegas` hace lo mismo pero omite a los amigos que no trabajan en la misma empresa que la persona objetivo.

P: ¿Qué ventaja de seguridad/encapsulación ofrece pasar un iterador en vez de la colección?
R: No se expone la colección completa al cliente y se puede cambiar en tiempo de ejecución la forma de recorrerla pasándole un iterador diferente.

P: ¿Qué estado y método auxiliar guarda `FacebookIterator`?
R: Guarda referencia a la colección (`facebook`), el `profileId`, el `type`, su `currentPosition` y una `cache`; un método `lazyInit()` carga la caché mediante `socialGraphRequest` solo cuando hace falta.

P: ¿Cuáles son los principales inconvenientes del patrón Iterator?
R: Puede resultar excesivo con colecciones sencillas y ser menos eficiente que recorrer directamente los elementos de algunas colecciones especializadas.

P: ¿Qué dos principios de diseño refuerza Iterator según sus pros?
R: El de responsabilidad única (extrae los recorridos voluminosos a clases independientes) y el abierto/cerrado (añadir colecciones e iteradores sin romper el código existente).

## Preguntas de autoevaluación

P: ¿Por qué una estructura compleja como un árbol complica tener los recorridos dentro de la propia colección?
R: Porque puede requerir hoy recorrido en profundidad, mañana en anchura y después acceso aleatorio; acumular esos algoritmos nubla la responsabilidad principal de la colección y algunos recorridos resultan extraños en una clase genérica. (Sección «Problema»)

P: ¿Cómo logra el patrón que el cliente no se acople a clases concretas?
R: El cliente trabaja con colecciones e iteradores a través de sus interfaces, obteniendo normalmente los iteradores desde las colecciones. (Secciones «Solución» y «Estructura»)

P: En la analogía de Roma, ¿qué representan las tres opciones de visita?
R: Dar vueltas con direcciones aleatorias, usar una guía virtual en el smartphone o contratar un guía local humano actúan como iteradores sobre la colección de atracciones de Roma. (Sección «Analogía en el mundo real»)

P: ¿Cuáles son los cinco elementos de la estructura del patrón?
R: La interfaz Iteradora, los Iteradores Concretos, la interfaz Colección, las Colecciones Concretas y el Cliente. (Sección «Estructura»)

P: ¿En qué situaciones conviene aplicar Iterator?
R: Cuando quieres ocultar la complejidad de la estructura interna de una colección, reducir la duplicación del código de recorrido no trivial, o recorrer estructuras de datos distintas o de tipos no conocidos de antemano. (Sección «Aplicabilidad»)

P: Al implementar el patrón, ¿cómo se establece el vínculo entre colección e iterador?
R: Las clases iteradoras concretas se vinculan a una única instancia de la colección, normalmente por el constructor; el objeto de colección se pasa a sí mismo al construir el iterador. (Sección «Cómo implementarlo»)

P: ¿Qué permite que cada iterador mantenga su propio estado respecto a la ejecución?
R: Recorrer la misma colección en paralelo y también retrasar una iteración para continuarla más tarde. (Sección «Pros y contras»)

P: ¿Cómo se relaciona Iterator con Factory Method y con Memento?
R: Factory Method permite que las subclases de la colección devuelvan distintos tipos de iteradores compatibles; Memento captura el estado de la iteración actual para reanudarla si fuera necesario. (Sección «Relaciones con otros patrones»)

## Puntos a dominar

- Explicar que Iterator separa el recorrido del almacenamiento trasladando la lógica a un objeto iterador independiente.
- Reconocer la interfaz iteradora común (`getNext()` y `hasMore()`) como mecanismo que desacopla al cliente de colecciones y algoritmos concretos.
- Justificar por qué varios iteradores recorren la misma colección en paralelo e independientemente gracias a su estado propio (posición, caché).
- Describir la colección como fábrica de iteradores capaz de ofrecer varios recorridos (p. ej., `amigos` y `colegas`).
- Argumentar cómo añadir un nuevo tipo de recorrido o de colección respeta el principio abierto/cerrado sin modificar el código existente.
- Identificar cuándo pasar un iterador en lugar de la colección oculta la estructura y permite cambiar el recorrido en tiempo de ejecución.
- Valorar los límites del patrón: puede ser excesivo con colecciones simples y menos eficiente que el acceso directo en colecciones especializadas.
