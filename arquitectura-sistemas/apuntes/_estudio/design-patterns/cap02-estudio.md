# Los pilares de la POO (The Pillars of OOP) — Estudio

## Tarjetas de repaso

P: ¿Cuáles son los cuatro pilares de la POO? / R: Abstracción, encapsulación, herencia y polimorfismo.

P: ¿Qué es la abstracción? / R: El modelo de un objeto o fenómeno del mundo real, limitado a un contexto específico, que copia solo los atributos y comportamientos relevantes e ignora el resto.

P: ¿Por qué un objeto del programa no representa al objeto real con precisión del 100 %? / R: Porque solo copia los atributos y comportamientos relevantes para un contexto específico, y rara vez hace falta más.

P: ¿Cómo ilustra el libro la abstracción con la clase `Avión`? / R: El mismo objeto real se modela distinto según el contexto: en un simulador de vuelo contiene datos del vuelo; en una app de reserva solo el mapa de asientos y los asientos disponibles.

P: ¿Qué es la encapsulación? / R: La capacidad de un objeto de esconder partes de su estado y comportamiento, exponiendo únicamente una interfaz limitada al resto del programa.

P: ¿Qué diferencia hay entre miembro privado y protegido? / R: Privado es accesible solo desde los métodos de su propia clase; protegido hace que el miembro también esté disponible para las subclases.

P: ¿Qué es la interfaz de un objeto (parte pública)? / R: La parte pública abierta a interacciones con otros objetos; el ejemplo del auto expone encendido, volante y pedales y oculta el motor.

P: ¿Por qué una interfaz (tipo `interface`/`protocol`) no puede declarar campos? / R: Porque las interfaces solo se interesan por los comportamientos de los objetos y definen contratos de interacción.

P: ¿Qué es la herencia y cuál es su principal ventaja? / R: La capacidad de crear nuevas clases sobre otras existentes; su ventaja principal es la reutilización de código extendiendo una clase en vez de duplicarla.

P: ¿Qué consecuencia tiene la herencia sobre la interfaz de la subclase? / R: La subclase tiene la misma interfaz que su clase padre: no puede esconder un método de la superclase y debe implementar todos los métodos abstractos aunque no tengan sentido.

P: ¿Cuántas superclases e interfaces puede tener una clase? / R: En la mayoría de los lenguajes extiende una única superclase, pero puede implementar varias interfaces al mismo tiempo.

P: Si una superclase implementa una interfaz, ¿qué ocurre con sus subclases? / R: Todas sus subclases deben implementarla también.

P: ¿Qué es el polimorfismo? / R: La capacidad de un programa de detectar la verdadera clase de un objeto e invocar su implementación, incluso aunque su tipo real sea desconocido en el contexto actual.

P: ¿Por qué conviene declarar abstracto el método `emitirSonido` en `Animal`? / R: Porque todas las subclases deben sobrescribirlo; así se omite una implementación por defecto y se fuerza a cada subclase a definir la suya.

P: ¿Cómo se explica el polimorfismo como "fingir ser otra cosa"? / R: Un objeto puede fingir ser otra cosa, normalmente una clase que extiende o una interfaz que implementa; en la bolsa, perros y gatos fingen ser animales genéricos.

## Preguntas de autoevaluación

P: ¿Qué significa que la abstracción esté "limitada a un contexto específico"? (sección Abstracción)
R: Que el objeto del programa copia solo los atributos y comportamientos relevantes para ese contexto e ignora el resto; por eso un `Avión` se modela distinto en un simulador que en una app de reserva.

P: En el ejemplo del auto, ¿qué representa la interfaz y qué queda oculto? (sección Encapsulación)
R: La interfaz es la parte pública (encendido, volante, pedales); queda oculto bajo el capó el detalle de conectar cables, rotar el cigüeñal o iniciar el ciclo de potencia del motor.

P: ¿Cómo permite la interfaz `TransporteAéreo` que la clase `Aeropuerto` trabaje con objetos distintos? (sección Encapsulación)
R: Restringiendo `Aeropuerto` a objetos que implementen `TransporteAéreo`; mientras la firma del método coincida con la declarada en la interfaz, cualquier objeto volador (`Avión`, `Helicóptero`, `GrifoDomesticado`) podrá aterrizar o despegar.

P: ¿Por qué la herencia obliga a implementar métodos abstractos que quizá no tengan sentido en la subclase? (sección Herencia)
R: Porque la subclase hereda la misma interfaz que su superclase y no puede esconder métodos declarados en ella, así que debe implementar todos los métodos abstractos aunque no tengan sentido.

P: En el ejemplo de la bolsa de animales, ¿cómo sabe el programa qué sonido emitir si no conoce el tipo concreto? (sección Polimorfismo)
R: Gracias al polimorfismo, el programa rastrea la subclase real del objeto y ejecuta la implementación correspondiente de `makeSound`, aunque su tipo concreto sea desconocido en el contexto.

P: ¿Qué dos significados del término "interfaz" distingue el autor? (sección Encapsulación)
R: La parte pública de un objeto abierta a interacciones, y el tipo `interface` (o `protocol`) del lenguaje que define contratos de comportamiento.

P: ¿Qué relación tienen interfaces y clases/métodos abstractos con los pilares? (sección Encapsulación)
R: Se basan en abstracción y encapsulación; el mecanismo de interfaz permite definir contratos de interacción entre objetos centrados en sus comportamientos.

## Puntos a dominar

- Definir con precisión cada uno de los cuatro pilares: abstracción, encapsulación, herencia y polimorfismo.
- Explicar la abstracción como modelo limitado a un contexto, usando el caso `Avión` (simulador vs. reserva).
- Distinguir miembros privados (solo la clase) de protegidos (también subclases) y qué es la interfaz pública de un objeto.
- Justificar por qué una interfaz define comportamientos y no puede declarar campos.
- Describir la herencia como reutilización de código y sus consecuencias sobre la interfaz heredada y los métodos abstractos.
- Recordar las reglas: una sola superclase, varias interfaces; si la superclase implementa una interfaz, las subclases también.
- Explicar el polimorfismo con el ejemplo de la bolsa de animales y el bucle que invoca `makeSound` según la clase real.
