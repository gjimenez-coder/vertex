# Dive Into Design Patterns — Alexander Shvets (Refactoring.Guru, 2021)
## Capítulo 33 — Strategy (Estrategia)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF (con palabras pegadas por la justificación de párrafos); las citas usan la página del PDF.

## Lo que necesitas saber

Strategy es un patrón de diseño de comportamiento que permite definir una familia de algoritmos, colocar cada uno en una clase separada y hacer sus objetos intercambiables (PDF p. 392). La idea central es extraer de una clase que resuelve una misma tarea de muchas formas distintas todos esos algoritmos, para que puedan sustituirse entre sí sin tocar la clase que los usa.

El patrón introduce dos roles. Una clase *contexto* mantiene una referencia a una estrategia y le delega el trabajo en lugar de ejecutarlo por su cuenta; una interfaz *estrategia* común expone un único método para disparar el algoritmo encapsulado. Como el contexto trabaja con todas las estrategias a través de esa misma interfaz, se vuelve independiente de las estrategias concretas: puedes añadir nuevos algoritmos o modificar los existentes sin cambiar el contexto ni las demás estrategias.

Sales sabiendo cuándo conviene sustituir herencia por composición para variar comportamiento, cómo eliminar grandes condicionales que seleccionan variantes de un algoritmo, y cómo permitir que el cliente intercambie algoritmos durante el tiempo de ejecución.

## El ejemplo que recorre el capítulo

Una aplicación de navegación para viajeros ocasionales, centrada en un mapa que ayuda a orientarse en cualquier ciudad (PDF p. 393). Su función más solicitada era la planificación automática de rutas: el usuario introduce una dirección y ve la ruta más rápida en el mapa.

La primera versión sólo generaba rutas sobre carreteras. Luego se añadieron rutas a pie, en transporte público, para ciclistas y para recorrer las atracciones turísticas. El problema: cada nuevo algoritmo de enrutamiento duplicaba el tamaño de la clase principal del navegador, y cualquier cambio en un algoritmo —un arreglo de error o un ajuste de la representación de la calle— afectaba a toda la clase, aumentando el riesgo de romper código ya funcional (PDF p. 394). Además, el trabajo en equipo se volvió ineficiente por los conflictos de integración al tocar todos la misma clase enorme.

La solución con Strategy: cada algoritmo de enrutamiento se extrae a su propia clase con un único método `crearRuta`, que acepta un origen y un destino y devuelve una colección de puntos de control de la ruta (PDF p. 396). A la clase navegadora principal no le importa qué algoritmo se selecciona; su labor es representar los puntos en el mapa. Un método permite cambiar la estrategia activa, de modo que los botones de la interfaz puedan sustituir el comportamiento de enrutamiento.

## Analogía en el mundo real

Llegar al aeropuerto admite varias estrategias de transporte: autobús, taxi o bicicleta. Eliges una según factores como el presupuesto o los límites de tiempo (PDF p. 397).

## Estructura

1. La clase **Contexto** mantiene una referencia a una estrategia concreta y se comunica con ella únicamente a través de la interfaz estrategia.
2. La **interfaz Estrategia** es común a todas las estrategias concretas y declara el método que el contexto usa para ejecutar una estrategia.
3. Las **Estrategias Concretas** implementan distintas variaciones del algoritmo que usa el contexto.
4. El contexto invoca el método de ejecución en la estrategia vinculada cada vez que necesita ejecutar el algoritmo, sin saber con qué tipo de estrategia funciona ni cómo se ejecuta (PDF p. 399).
5. El **Cliente** crea una estrategia específica y la pasa al contexto; el contexto expone un modificador *set* que permite sustituir la estrategia durante el tiempo de ejecución.

## Pseudocódigo

El contexto usa varias estrategias para ejecutar operaciones aritméticas. La interfaz `Strategy` declara `execute(a, b)`; las estrategias concretas (`ConcreteStrategyAdd`, `ConcreteStrategySubtract`, `ConcreteStrategyMultiply`) implementan suma, resta y multiplicación.

```
interface Strategy is
    method execute(a, b)

class ConcreteStrategyAdd implements Strategy is
    method execute(a, b) is
        return a + b

class Context is
    private strategy: Strategy
    method setStrategy(Strategy strategy) is
        this.strategy = strategy
    method executeStrategy(int a, int b) is
        return strategy.execute(a, b)
```

El cliente elige la estrategia concreta según la acción del usuario (`setStrategy(new ConcreteStrategyAdd())`, etc.) y luego llama a `executeStrategy`. El cliente debe conocer las diferencias entre estrategias para elegir la mejor opción (PDF p. 400–401).

## Aplicabilidad

- Cuando quieras usar distintas variantes de un algoritmo dentro de un objeto y cambiar de uno a otro en tiempo de ejecución.
- Cuando tengas muchas clases similares que sólo se diferencien en la forma en que ejecutan cierto comportamiento: extraes la parte variante a una jerarquía separada y reduces el código duplicado.
- Para aislar la lógica de negocio de los detalles de implementación de algoritmos que no son tan importantes en ese contexto.
- Cuando tu clase tenga un enorme operador condicional que cambie entre variantes del mismo algoritmo: se suprime extrayendo cada algoritmo a su propia clase con la misma interfaz (PDF p. 401–403).

## Cómo implementarlo

1. Identifica en el contexto un algoritmo que cambie con frecuencia (o un gran condicional que seleccione una variante en tiempo de ejecución).
2. Declara la interfaz estrategia común a todas las variantes.
3. Extrae uno a uno los algoritmos a sus propias clases, todas implementando la interfaz estrategia.
4. Añade en el contexto un campo para la referencia a la estrategia y un modificador *set*; el contexto trabaja con la estrategia sólo a través de la interfaz.
5. Los clientes asocian el contexto con la estrategia adecuada a cómo esperan que realice su trabajo (PDF p. 402–403).

## Pros y contras

Pros: intercambias algoritmos en tiempo de ejecución; aíslas los detalles de implementación del código que los usa; sustituyes la herencia por composición; cumples el principio de abierto/cerrado (nuevas estrategias sin cambiar el contexto). Contras: si sólo tienes un par de algoritmos que raramente cambian, no hay razón para complicar el programa con nuevas clases e interfaces; los clientes deben conocer las diferencias entre estrategias para elegir. Además, lenguajes modernos con soporte funcional permiten usar funciones anónimas como estrategias sin saturar el código con clases e interfaces (PDF p. 404).

## Relaciones con otros patrones

- **Bridge, State, Strategy** (y en parte Adapter) tienen estructuras muy similares basadas en la composición, pero resuelven problemas diferentes.
- **Command y Strategy** parametrizan un objeto con una acción; Command convierte una operación en objeto (para aplazar, encolar o historiar), mientras Strategy describe distintas formas de hacer lo mismo e intercambiarlas.
- **Decorator** cambia la piel de un objeto; **Strategy** cambia sus entrañas.
- **Template Method** se basa en la herencia y trabaja al nivel de clase (estático); **Strategy** se basa en la composición y trabaja al nivel de objeto, permitiendo cambiar comportamientos en tiempo de ejecución.
- **State** puede verse como extensión de Strategy: ambos delegan trabajo a objetos ayudantes, pero Strategy los hace independientes entre sí, mientras State permite dependencias entre estados concretos (PDF p. 404–405).

## Ideas clave

- Strategy define una familia de algoritmos intercambiables, cada uno en su propia clase.
- El contexto delega en una estrategia a través de una interfaz común y no conoce la clase concreta.
- El cliente elige y asigna la estrategia; puede cambiarla en tiempo de ejecución con un modificador *set*.
- Sustituye herencia por composición y cumple el principio de abierto/cerrado.
- Suprime grandes condicionales que seleccionan variantes de un algoritmo.
- Evítalo si hay pocos algoritmos estables; considera funciones anónimas en lenguajes funcionales.
- Comparte estructura con Bridge, State y Adapter, pero se distingue por su propósito.
