# Bridge (Puente) — Estudio

## Tarjetas de repaso

- P: ¿Qué tipo de patrón es Bridge y qué permite hacer? / R: Es un patrón estructural que divide una clase grande o un grupo de clases relacionadas en dos jerarquías separadas —abstracción e implementación— que pueden desarrollarse independientemente.
- P: ¿Qué problema concreto ataca Bridge? / R: La explosión combinatoria que surge cuando una jerarquía de clases intenta crecer en dos dimensiones independientes a la vez.
- P: ¿Qué cambio de enfoque propone Bridge frente a la herencia? / R: Pasar de la herencia a la composición del objeto, extrayendo una dimensión a una jerarquía separada que las clases originales referencian.
- P: En el ejemplo geométrico, ¿qué combinaciones aparecen y por qué son un problema? / R: Formas (Círculo, Cuadrado) con colores (Rojo, Azul) producen clases como CírculoAzul o CuadradoRojo; el número crece en progresión geométrica al añadir formas o colores.
- P: ¿Cómo resuelve Bridge el ejemplo de formas y colores? / R: Extrae el color a su propia jerarquía (Rojo, Azul) y la clase Forma obtiene una referencia a un objeto de color en el que delega el trabajo relacionado con el color.
- P: ¿Qué es la Abstracción en Bridge? / R: Una capa de control de alto nivel (también llamada interfaz) que no hace el trabajo real por sí misma, sino que delega en la capa de implementación.
- P: ¿Qué es la Implementación en Bridge? / R: La capa (también llamada plataforma) que hace el trabajo de bajo nivel.
- P: ¿La Abstracción y la Implementación de Bridge son las interfaces o clases abstractas del lenguaje? / R: No; son cosas diferentes de las interfaces o clases abstractas del lenguaje de programación.
- P: En una aplicación real, ¿qué papel pueden tener GUI y API en Bridge? / R: La GUI actúa como abstracción y las API del sistema operativo (Windows, Linux, macOS) como implementación, intercambiables mientras sigan una interfaz común.
- P: ¿Cuáles son los cinco elementos de la estructura de Bridge? / R: Abstracción, Implementación, Implementaciones Concretas, Abstracciones Refinadas y Cliente.
- P: ¿Qué hace el Cliente en Bridge? / R: Trabaja solo con la abstracción, pero debe vincular el objeto de abstracción con uno de implementación.
- P: ¿Deben coincidir la interfaz de la abstracción y la de la implementación? / R: No; pueden ser completamente diferentes.
- P: ¿Qué característica de Bridge lo hace confundible con Strategy? / R: Que permite cambiar la implementación en tiempo de ejecución asignando un nuevo valor a un campo, aunque la intención de ambos patrones difiere.
- P: ¿Qué dos principios de diseño favorece Bridge? / R: El principio de abierto/cerrado y el principio de responsabilidad única.
- P: ¿En qué se diferencia Bridge de Adapter respecto al momento de diseño? / R: Bridge suele planificarse por anticipado desde el inicio del diseño, mientras que Adapter se usa con una aplicación existente para hacer trabajar juntas clases incompatibles.

## Preguntas de autoevaluación

- P: ¿Por qué la herencia provoca explosión de clases en el ejemplo de formas y colores? / R: Porque se intenta extender en dos dimensiones independientes; añadir un tipo de forma obliga a una subclase por cada color y añadir un color obliga a una subclase por cada forma, creciendo en progresión geométrica. (Sección "El ejemplo que recorre el capítulo" / "Problema")
- P: ¿Cómo actúa la referencia de Forma a Color como "puente"? / R: Forma obtiene un campo que apunta a un objeto de color y le delega todo el trabajo de color, de modo que añadir colores no exige cambiar la jerarquía de forma ni viceversa. (Sección "El ejemplo que recorre el capítulo")
- P: ¿Qué relación tienen Abstracción e Implementación en cuanto a quién hace el trabajo? / R: La Abstracción ofrece control de alto nivel y delega; la Implementación realiza el trabajo de bajo nivel mediante operaciones primitivas sobre las que la abstracción define funcionalidades complejas. (Secciones "Solución: abstracción e implementación" y "Estructura")
- P: En el pseudocódigo, ¿qué clases hacen de abstracción y cuáles de implementación? / R: Las clases Remoto (RemoteControl, AdvancedRemoteControl) son la abstracción y las clases Dispositivo (Device, Tv, Radio) la implementación; el remoto guarda una referencia al dispositivo y opera por su interfaz general. (Sección "Pseudocódigo")
- P: ¿En qué situaciones conviene aplicar Bridge? / R: Al dividir una clase monolítica con muchas variantes de una funcionalidad, al extender en dimensiones ortogonales (una jerarquía por dimensión) y cuando se necesita cambiar implementaciones en tiempo de ejecución. (Sección "Aplicabilidad")
- P: ¿Cuál es el primer paso para implementar Bridge? / R: Identificar las dimensiones ortogonales del problema (abstracción/plataforma, dominio/infraestructura, front end/back end o interfaz/implementación). (Sección "Cómo implementarlo")
- P: ¿Cuál es la principal desventaja de Bridge? / R: El código puede complicarse si se aplica el patrón a una clase muy cohesionada. (Sección "Pros y contras")
- P: ¿Cómo se relaciona Bridge con Abstract Factory y con Builder? / R: Abstract Factory puede usarse con Bridge cuando ciertas abstracciones solo funcionan con implementaciones específicas, encapsulando esas relaciones; con Builder, el director hace de abstracción y las constructoras de implementaciones. (Sección "Relaciones con otros patrones")

## Puntos a dominar

- Reconocer cuándo un diseño crece en dos dimensiones ortogonales e independientes, origen de la explosión combinatoria.
- Distinguir la capa de abstracción (control de alto nivel que delega) de la capa de implementación (trabajo de bajo nivel).
- Entender que la referencia de la abstracción a la implementación es el "puente" que sustituye la herencia por composición.
- Recordar que abstracción e implementación pueden tener interfaces completamente diferentes y evolucionar por separado.
- Identificar la estructura: Abstracción, Implementación, Implementaciones Concretas, Abstracciones Refinadas y Cliente.
- Seguir los pasos de implementación: identificar dimensiones, definir operaciones del cliente, declarar la interfaz de implementación, crear implementaciones concretas, añadir la referencia y delegar, crear abstracciones refinadas y vincular desde el cliente.
- Diferenciar Bridge de Strategy (cambio de implementación en runtime) y de Adapter (planificación anticipada frente a adaptación de código existente).
- Asociar Bridge con los principios de abierto/cerrado y de responsabilidad única.
