# Decorator (Decorador) — Estudio

## Tarjetas de repaso

P: ¿Qué tipo de patrón es Decorator y qué permite hacer? / R: Es un patrón de diseño estructural que permite añadir funcionalidades a un objeto colocándolo dentro de objetos encapsuladores especiales (wrappers) que contienen esas funcionalidades.

P: ¿Con qué otros nombres se conoce a Decorator? / R: Decorador, Envoltorio o Wrapper.

P: ¿Qué dos limitaciones de la herencia resuelve Decorator? / R: Que la herencia es estática (no se puede cambiar el comportamiento en tiempo de ejecución, solo sustituir el objeto por otro de una subclase) y que una subclase solo puede tener una clase padre.

P: ¿Qué mecanismo usa Decorator en lugar de la herencia? / R: Agregación/composición: un objeto mantiene una referencia a otro y le delega parte del trabajo.

P: Según el texto, ¿en qué se diferencian agregación y composición? / R: En la agregación A contiene objetos B y B puede existir sin A; en la composición A está compuesto de B, gestiona su ciclo vital y B no puede existir sin A.

P: ¿Qué es un wrapper? / R: Un objeto que se vincula con un objeto objetivo, contiene el mismo grupo de métodos que el objetivo y le delega todas las solicitudes, pero puede alterar el resultado haciendo algo antes o después de pasar la solicitud.

P: ¿Cuándo un wrapper se convierte en verdadero decorador? / R: Cuando implementa la misma interfaz que el objeto envuelto y su campo de referencia acepta cualquier objeto que siga esa interfaz, permitiendo envolver un objeto en varios wrappers.

P: ¿Por qué el cliente trata igual al objeto puro y al decorado? / R: Porque todos implementan la misma interfaz del componente, así que al cliente no le importa si trabaja con el notificador puro o decorado.

P: ¿Cuáles son los cinco elementos de la estructura del patrón? / R: Componente, Componente Concreto, Decoradora Base, Decoradores Concretos y Cliente.

P: ¿Qué función cumple la Decoradora Base? / R: Tiene un campo que referencia un objeto envuelto con el tipo de la interfaz del componente (para contener componentes concretos y decoradores) y delega todas las operaciones a ese objeto.

P: ¿Cómo actúan los Decoradores Concretos respecto al método padre? / R: Sobrescriben métodos de la decoradora base y ejecutan su comportamiento antes o después de invocar al método padre.

P: ¿Cuál es la analogía del mundo real del capítulo? / R: Vestir ropa: suéter, chaqueta e impermeable extienden tu comportamiento básico pero no son parte de ti y puedes quitártelos cuando quieras.

P: En el pseudocódigo, ¿qué hacen EncryptionDecorator y CompressionDecorator? / R: En writeData encriptan/comprimen antes de delegar, y en readData descifran/descomprimen después.

P: ¿Qué diferencia a Decorator de Strategy? / R: Decorator cambia "la piel" de un objeto; Strategy cambia sus "entrañas".

P: ¿Quién controla la composición en Decorator frente a Proxy? / R: En Decorator la composición siempre la controla el cliente, mientras que Proxy suele gestionar el ciclo de vida de su objeto por su cuenta.

## Preguntas de autoevaluación

P: ¿Por qué la solución inicial con subclases por canal falló en la biblioteca de notificaciones? / R: Porque al querer usar varios canales a la vez, crear subclases combinadas provocaba una explosión combinatoria que inflaba la biblioteca y el código cliente. (El ejemplo que recorre el capítulo)

P: ¿Cómo resuelve Decorator el problema de la biblioteca de notificaciones? / R: Deja la funcionalidad básica de correo en la clase base Notificador y convierte el resto de métodos en decoradores; el cliente envuelve el notificador básico en los decoradores que necesite formando una pila. (El ejemplo que recorre el capítulo)

P: ¿En qué dos situaciones recomienda el capítulo usar Decorator? / R: Cuando necesites asignar funcionalidades adicionales en tiempo de ejecución sin descomponer el código que los utiliza, y cuando sea extraño o imposible extender el comportamiento por herencia (por ejemplo, una clase final). (Aplicabilidad)

P: ¿Qué principio de diseño favorece Decorator y cómo? / R: El principio de responsabilidad única, dividiendo una clase monolítica en clases más pequeñas. (Pros y contras)

P: ¿Cuáles son los principales inconvenientes del patrón? / R: Es difícil eliminar un wrapper específico de la pila, es difícil lograr que el comportamiento no dependa del orden en la pila y el código de configuración inicial de las capas puede tener un aspecto desagradable. (Pros y contras)

P: ¿En qué se diferencian Decorator y Chain of Responsibility pese a tener estructuras similares? / R: Los manejadores de CoR pueden ejecutar operaciones arbitrarias y detener la solicitud, mientras que los decoradores no pueden romper el flujo. (Relaciones con otros patrones)

P: ¿Qué relación guardan Decorator y Composite? / R: Comparten diagrama; un Decorator es como un Composite con un solo componente hijo, pero Decorator añade responsabilidades y Composite solo recapitula resultados de sus hijos, y pueden colaborar. (Relaciones con otros patrones)

## Checklist

Pasos para implementar el patrón (según "Cómo implementarlo"):

- [ ] Verificar que el dominio puede representarse como un componente primario con varias capas opcionales encima.
- [ ] Decidir los métodos comunes al componente y las capas, y declarar una interfaz de componente con ellos.
- [ ] Crear una clase concreta de componente con el comportamiento base.
- [ ] Crear la clase base decoradora con un campo (de tipo interfaz de componente) que referencie al objeto envuelto, delegando todas las operaciones.
- [ ] Asegurarse de que todas las clases implementan la interfaz de componente.
- [ ] Crear los decoradores concretos extendiendo la base, ejecutando su comportamiento antes o después del método padre.
- [ ] Dejar que el código cliente sea responsable de crear y componer los decoradores.
