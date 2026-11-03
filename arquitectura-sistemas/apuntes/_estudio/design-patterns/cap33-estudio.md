# Capítulo 33 — Strategy (Estrategia) — Estudio

## Tarjetas de repaso

P: ¿Qué es el patrón Strategy?
R: Un patrón de diseño de comportamiento que permite definir una familia de algoritmos, colocar cada uno en una clase separada y hacer sus objetos intercambiables.

P: ¿Cuál es la idea central de Strategy?
R: Extraer de una clase que resuelve una misma tarea de muchas formas distintas todos esos algoritmos, para que puedan sustituirse entre sí sin tocar la clase que los usa.

P: ¿Qué dos roles introduce el patrón?
R: Una clase contexto, que mantiene una referencia a una estrategia y le delega el trabajo, y una interfaz estrategia común que expone un único método para disparar el algoritmo encapsulado.

P: ¿Por qué el contexto es independiente de las estrategias concretas?
R: Porque trabaja con todas las estrategias a través de la misma interfaz, así que se pueden añadir o modificar algoritmos sin cambiar el contexto ni las demás estrategias.

P: En el ejemplo del navegador, ¿qué método encapsula cada algoritmo de enrutamiento?
R: Un único método `crearRuta`, que acepta un origen y un destino y devuelve una colección de puntos de control de la ruta.

P: ¿Qué problema tenía la clase navegadora antes de aplicar Strategy?
R: Cada nuevo algoritmo de enrutamiento duplicaba su tamaño y cualquier cambio en un algoritmo afectaba a toda la clase, aumentando el riesgo de romper código funcional y provocando conflictos de integración en equipo.

P: ¿Qué declara la interfaz `Strategy` en el pseudocódigo y qué estrategias concretas aparecen?
R: Declara `execute(a, b)`; las estrategias concretas son `ConcreteStrategyAdd`, `ConcreteStrategySubtract` y `ConcreteStrategyMultiply` (suma, resta y multiplicación).

P: ¿Cuál es el papel del Cliente en el patrón?
R: Crea una estrategia específica y la pasa al contexto; además puede sustituir la estrategia en tiempo de ejecución mediante el modificador set.

P: ¿Qué principio de diseño cumple Strategy?
R: El principio de abierto/cerrado, ya que se pueden añadir nuevas estrategias sin cambiar el contexto.

P: ¿Qué relación de diseño reemplaza Strategy y por cuál?
R: Sustituye la herencia por la composición.

P: ¿Cuándo no conviene usar Strategy?
R: Cuando sólo hay un par de algoritmos que raramente cambian, pues no vale la pena complicar el programa con nuevas clases e interfaces.

P: ¿Qué diferencia a Strategy de Template Method?
R: Template Method se basa en la herencia y trabaja al nivel de clase (estático); Strategy se basa en la composición y trabaja al nivel de objeto, permitiendo cambiar comportamientos en tiempo de ejecución.

P: ¿En qué se diferencian Decorator y Strategy?
R: Decorator cambia la piel de un objeto; Strategy cambia sus entrañas.

P: ¿Cómo se relacionan State y Strategy?
R: State puede verse como extensión de Strategy: ambos delegan trabajo a objetos ayudantes, pero Strategy los hace independientes entre sí, mientras State permite dependencias entre estados concretos.

## Preguntas de autoevaluación

P: ¿Qué problema de mantenimiento resuelve Strategy en la aplicación de navegación? (sección «El ejemplo que recorre el capítulo»)
R: Evita que cada nuevo algoritmo de enrutamiento haga crecer la clase principal del navegador y que un cambio en un algoritmo afecte a toda la clase; al extraer cada algoritmo a su propia clase se reducen los conflictos y el riesgo de romper código.

P: ¿Cómo logra el contexto ejecutar un algoritmo sin saber cuál es? (sección «Estructura»)
R: Invoca el método de ejecución en la estrategia vinculada a través de la interfaz estrategia común, sin conocer el tipo de estrategia ni cómo se ejecuta.

P: ¿Por qué el cliente debe conocer las diferencias entre estrategias? (sección «Pseudocódigo»)
R: Porque es el cliente quien elige y asigna la estrategia concreta según la acción del usuario, de modo que debe conocer esas diferencias para elegir la mejor opción.

P: ¿En qué situaciones es aplicable el patrón Strategy? (sección «Aplicabilidad»)
R: Cuando se quieren usar variantes de un algoritmo e intercambiarlas en tiempo de ejecución, cuando hay muchas clases similares que sólo difieren en cómo ejecutan un comportamiento, para aislar la lógica de negocio de detalles de algoritmos, y cuando una clase tiene un enorme condicional que selecciona variantes del mismo algoritmo.

P: ¿Cuáles son los pasos clave para implementar Strategy? (sección «Cómo implementarlo»)
R: Identificar un algoritmo cambiante o un gran condicional, declarar la interfaz estrategia común, extraer cada algoritmo a su propia clase que implemente la interfaz, añadir en el contexto un campo y un modificador set, y asociar desde el cliente el contexto con la estrategia adecuada.

P: ¿Qué contrapartidas tiene aplicar Strategy? (sección «Pros y contras»)
R: Añade clases e interfaces que no se justifican si hay pocos algoritmos estables, exige que los clientes conozcan las diferencias entre estrategias, y en lenguajes con soporte funcional las funciones anónimas pueden cumplir el mismo rol sin saturar el código.

P: ¿Qué distingue a Command de Strategy aunque ambos parametricen un objeto con una acción? (sección «Relaciones con otros patrones»)
R: Command convierte una operación en objeto para aplazarla, encolarla o historiarla, mientras Strategy describe distintas formas de hacer lo mismo e intercambiarlas.

## Puntos a dominar

- Distinguir los roles de contexto, interfaz estrategia, estrategias concretas y cliente, y cómo se comunican sólo a través de la interfaz.
- Explicar cómo Strategy sustituye la herencia por composición y cumple el principio de abierto/cerrado.
- Reconocer el síntoma de un gran condicional que selecciona variantes de un algoritmo como candidato a refactorizar con Strategy.
- Saber cuándo NO aplicar el patrón (pocos algoritmos estables) y la alternativa con funciones anónimas en lenguajes funcionales.
- Diferenciar Strategy de Bridge, State, Command, Decorator y Template Method según propósito y mecanismo (composición vs. herencia, nivel de objeto vs. nivel de clase).
