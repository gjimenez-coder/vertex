# Dive Into Design Patterns — Alexander Shvets (Refactoring.Guru, 2021)
## Capítulo 28 — Iterator (Iterador)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF (con palabras pegadas por la justificación) y las citas usan la página del PDF.

## Lo que necesitas saber

Iterator es un patrón de diseño de comportamiento que permite recorrer los elementos de una colección sin exponer su representación subyacente, ya sea una lista, una pila, un árbol, un grafo u otra estructura (PDF p. 311). La idea central es extraer el comportamiento de recorrido de una colección y colocarlo en un objeto independiente llamado iterador.

La tesis del capítulo es que mezclar los algoritmos de recorrido con la colección nubla su responsabilidad principal —el almacenamiento eficiente de la información— y acopla el código cliente a clases concretas. El patrón resuelve ambos problemas delegando el recorrido a iteradores que comparten una interfaz común.

Sales sabiendo cómo separar el recorrido del almacenamiento, cómo permitir que varios iteradores recorran la misma colección de forma independiente y simultánea, y cómo añadir nuevos tipos de recorrido sin modificar ni la colección ni el cliente.

## El ejemplo que recorre el capítulo

El pseudocódigo recorre un tipo especial de colección que encapsula el acceso al grafo social de Facebook (PDF p. 318). La colección ofrece varios iteradores: el iterador `amigos` recorre los amigos de un perfil, y el iterador `colegas` hace lo mismo pero omite a los amigos que no trabajan en la misma empresa que la persona objetivo. Ambos implementan una interfaz común, de modo que el cliente extrae perfiles sin conocer detalles como la autenticación o el envío de solicitudes REST.

## Problema

Las colecciones son de los tipos de datos más utilizados en programación, pero una colección es tan solo un contenedor de objetos. La mayoría almacena sus elementos en listas simples, pero algunas se basan en pilas, árboles, grafos u otras estructuras complejas. Independientemente de su estructura, una colección debe ofrecer una forma de recorrer cada elemento sin acceder a los mismos una y otra vez.

Para una lista basta con un bucle, pero recorrer una estructura compleja como un árbol puede requerir hoy un recorrido en profundidad, mañana uno en anchura y la semana siguiente un acceso aleatorio (PDF p. 312-313). Añadir más y más algoritmos de recorrido a la colección nubla gradualmente su responsabilidad principal, y algunos algoritmos personalizados para una aplicación específica resultan extraños dentro de una clase genérica de colección. Por su parte, el cliente que trabaja con varias colecciones no tiene más opción que acoplarse a las clases concretas.

## Solución

Los iteradores implementan varios algoritmos de recorrido. Varios objetos iteradores pueden recorrer la misma colección al mismo tiempo. Además del algoritmo, un objeto iterador encapsula todos los detalles del recorrido, como la posición actual y cuántos elementos quedan hasta el final; por eso varios iteradores pueden recorrer la misma colección de forma independiente entre sí (PDF p. 314).

Normalmente los iteradores aportan un método principal para extraer elementos de la colección, y el cliente ejecuta ese método hasta que no devuelve nada, señal de que se recorrieron todos los elementos. Todos los iteradores deben implementar la misma interfaz, lo que hace que el código cliente sea compatible con cualquier tipo de colección o algoritmo de recorrido. Si necesitas una forma particular de recorrer una colección, creas una nueva clase iteradora sin cambiar la colección ni el cliente.

## Analogía en el mundo real

Para visitar Roma tienes tres opciones: dar vueltas con direcciones aleatorias en tu cabeza, comprar una aplicación de guía virtual para el smartphone, o contratar un guía local humano que conozca la ciudad. Todas actúan como iteradores sobre la amplia colección de visitas y atracciones de Roma (PDF p. 315-316).

## Estructura

1. La interfaz **Iteradora** declara las operaciones para recorrer una colección: extraer el siguiente elemento, recuperar la posición actual, reiniciar la iteración, etc.
2. Los **Iteradores Concretos** implementan algoritmos específicos de recorrido y controlan el progreso por su cuenta, lo que permite que varios recorran la misma colección con independencia.
3. La interfaz **Colección** declara uno o varios métodos para obtener iteradores; el tipo de retorno debe ser la interfaz iteradora para que las colecciones concretas puedan devolver distintos tipos de iteradores.
4. Las **Colecciones Concretas** devuelven nuevas instancias de una clase iteradora concreta cada vez que el cliente lo solicita.
5. El **Cliente** trabaja con colecciones e iteradores a través de sus interfaces, por lo que no se acopla a clases concretas. Normalmente los clientes obtienen los iteradores de las colecciones, aunque en algunos casos pueden crear uno directamente (PDF p. 316-317).

## Pseudocódigo

La interfaz `SocialNetwork` declara métodos fábrica `createFriendsIterator(profileId)` y `createCoworkersIterator(profileId)`, ambos con retorno `ProfileIterator`. La clase concreta `Facebook` los implementa devolviendo un `FacebookIterator` con el tipo correspondiente. La interfaz común `ProfileIterator` declara `getNext():Profile` y `hasMore():bool`.

`FacebookIterator` guarda una referencia a la colección (`facebook`), el `profileId`, el `type`, y su propio estado de iteración (`currentPosition` y una `cache`). Un método `lazyInit()` carga la caché mediante `socialGraphRequest` solo cuando hace falta (PDF p. 319-321).

El capítulo destaca un truco útil: puedes pasar un iterador a la clase cliente en lugar de darle acceso a la colección completa, con lo que no la expones. Además, puedes cambiar en tiempo de ejecución la forma en que el cliente trabaja con la colección pasándole un iterador diferente. El cliente `SocialSpammer` recibe un `ProfileIterator` en `send(iterator, message)` y recorre perfiles con `hasMore()`/`getNext()`, sin acoplarse a clases iteradoras concretas (PDF p. 322).

## Aplicabilidad

- Cuando tu colección tenga una estructura de datos compleja internamente pero quieras ocultar esa complejidad al cliente, por conveniencia o por seguridad; el iterador también protege la colección frente a acciones descuidadas o maliciosas.
- Para reducir la duplicación del código de recorrido: los algoritmos de iteración no triviales son voluminosos y, dentro de la lógica de negocio, dificultan el mantenimiento; moverlos a iteradores designados deja el código más breve y limpio.
- Cuando quieras que tu código recorra distintas estructuras de datos o cuyos tipos no se conozcan de antemano, apoyándote en las interfaces genéricas de colección e iterador (PDF p. 323-324).

## Cómo implementarlo

1. Declara la interfaz iteradora con, al menos, un método para extraer el siguiente elemento (opcionalmente, el previo, la posición actual o la comprobación de fin).
2. Declara la interfaz de colección con un método para buscar iteradores, cuyo tipo de retorno sea la interfaz iteradora.
3. Implementa clases iteradoras concretas vinculadas a una única instancia de la colección, normalmente a través del constructor.
4. Implementa la interfaz de colección en tus clases de colección; el objeto de colección debe pasarse a sí mismo al constructor del iterador para establecer el vínculo.
5. Repasa el código cliente para sustituir todo el código de recorrido por el uso de iteradores (PDF p. 324-325).

## Pros y contras

- Principio de responsabilidad única: extraes los algoritmos de recorrido voluminosos a clases independientes.
- Principio de abierto/cerrado: puedes añadir nuevos tipos de colecciones e iteradores sin descomponer el código existente.
- Puedes recorrer la misma colección en paralelo, porque cada iterador tiene su propio estado; por la misma razón puedes retrasar una iteración y continuarla luego.
- Puede resultar excesivo si solo trabajas con colecciones sencillas.
- Usar un iterador puede ser menos eficiente que recorrer directamente los elementos de algunas colecciones especializadas (PDF p. 324-325).

## Relaciones con otros patrones

- Puedes usar Iteradores para recorrer árboles Composite.
- Factory Method junto con Iterator permite que las subclases de la colección devuelvan distintos tipos de iteradores compatibles.
- Memento junto con Iterator captura el estado de la iteración actual para reanudarla si fuera necesario.
- Visitor junto con Iterator recorre una estructura compleja y ejecuta una operación sobre sus elementos, aunque todos tengan clases distintas (PDF p. 326).

## Ideas clave

- Iterator separa el recorrido del almacenamiento, trasladando la lógica de recorrido a un objeto iterador independiente.
- La interfaz iteradora común (típicamente `getNext()` y `hasMore()`) desacopla al cliente de las colecciones y algoritmos concretos.
- Cada iterador mantiene su propio estado (posición, caché), de modo que varios pueden recorrer la misma colección en paralelo e independientemente.
- La colección actúa como fábrica de iteradores, y puede ofrecer varios para distintas formas de recorrido (p. ej., `amigos` y `colegas`).
- Añadir un nuevo tipo de recorrido o de colección no exige modificar el código existente (abierto/cerrado).
- Pasar un iterador en vez de la colección completa oculta la colección y permite cambiar el recorrido en tiempo de ejecución.
- El patrón puede ser excesivo con colecciones simples y algo menos eficiente que el acceso directo en colecciones especializadas.
