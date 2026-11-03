# Dive Into Design Patterns — Alexander Shvets (Refactoring.Guru, 2021)
## Capítulo 22 — Decorator (Decorador)

> Nota de extracción: texto obtenido de la capa de texto del PDF; las citas usan la página del PDF.

## Lo que necesitas saber

Decorator es un patrón de diseño estructural que permite añadir funcionalidades a un objeto colocándolo dentro de objetos encapsuladores especiales (wrappers) que contienen esas funcionalidades. También se le conoce como Decorador, Envoltorio o Wrapper.

La tesis central es que, cuando necesitas alterar el comportamiento de un objeto, la herencia resulta limitada: es estática (no puedes cambiar el comportamiento en tiempo de ejecución, solo sustituir el objeto completo por otro de una subclase distinta) y en la mayoría de lenguajes una subclase solo puede tener una clase padre. Decorator supera estas restricciones usando agregación/composición en lugar de herencia: un objeto mantiene una referencia a otro y le delega parte del trabajo.

Sales sabiendo cómo envolver un objeto en una pila de decoradores que comparten la misma interfaz que el objeto envuelto, de modo que el cliente los trata de forma idéntica, y cómo añadir o quitar responsabilidades dinámicamente combinando varios wrappers.

## El ejemplo que recorre el capítulo

El hilo conductor es una biblioteca de notificaciones. La versión inicial tenía una clase `Notificador` con un único método `send` que enviaba un mensaje a una lista de correos electrónicos configurada en el constructor. Cuando los usuarios pidieron también SMS, Facebook y Slack, la primera idea fue extender la clase con subclases por cada canal. Pero al querer usar varios canales a la vez (“si tu casa está en llamas, probablemente quieras que te informen a través de todos los canales”, PDF p. 209), crear subclases combinadas provocaba una explosión combinatoria que inflaba tanto la biblioteca como el código cliente.

La solución con Decorator: deja la funcionalidad básica de correo en la clase base `Notificador` y convierte el resto de métodos de notificación en decoradores. El cliente envuelve un notificador básico en los decoradores que necesite, formando una pila; el último decorador de la pila es el objeto con el que trabaja. Como todos implementan la interfaz de la notificadora base, al cliente no le importa si trabaja con el notificador “puro” o decorado. La misma idea sirve para otras funcionalidades como el formateo de mensajes o la composición de la lista de destinatarios.

## Problema y solución

La herencia tiene dos limitaciones importantes: es estática y las subclases solo pueden tener una clase padre. Una forma de superarlas es emplear agregación o composición. Según la nota del texto (PDF p. 211): en la agregación el objeto A contiene objetos B y B puede existir sin A; en la composición A está compuesto de B, gestiona su ciclo vital y B no puede existir sin A. Ambas funcionan parecido: un objeto tiene una referencia a otro y le delega trabajo. La agregación/composición es el principio clave tras muchos patrones, incluido Decorator.

Un wrapper es un objeto que se vincula con un objeto objetivo, contiene el mismo grupo de métodos que el objetivo y le delega todas las solicitudes, pero puede alterar el resultado haciendo algo antes o después de pasar la solicitud. Un wrapper se convierte en verdadero decorador cuando implementa la misma interfaz que el objeto envuelto y su campo de referencia acepta cualquier objeto que siga esa interfaz, lo que permite envolver un objeto en varios wrappers y acumular el comportamiento combinado.

## Analogía en el mundo real

Vestir ropa es un ejemplo de uso de decoradores. Cuando tienes frío te pones un suéter; si sigues con frío, una chaqueta encima; si llueve, un impermeable. Todas estas prendas “extienden” tu comportamiento básico pero no son parte de ti, y puedes quitarte cualquiera cuando quieras.

## Estructura

1. **Componente**: declara la interfaz común para wrappers y objetos envueltos.
2. **Componente Concreto**: clase de objetos envueltos; define el comportamiento básico que los decoradores pueden alterar.
3. **Decoradora Base**: tiene un campo que referencia un objeto envuelto, declarado con el tipo de la interfaz del componente para poder contener tanto componentes concretos como decoradores. Delega todas las operaciones al objeto envuelto.
4. **Decoradores Concretos**: definen funcionalidades adicionales que se añaden dinámicamente; sobrescriben métodos de la decoradora base y ejecutan su comportamiento antes o después de invocar al método padre.
5. **Cliente**: puede envolver componentes en varias capas de decoradores, siempre que trabaje con todos a través de la interfaz del componente.

## Pseudocódigo

El ejemplo permite comprimir y encriptar información delicada de forma independiente del código que usa esos datos. Una interfaz `DataSource` define `writeData(data)` y `readData()`. `FileDataSource` es el componente concreto que lee y escribe en archivo. La clase base `DataSourceDecorator` implementa `DataSource`, guarda un campo `wrappee: DataSource` y delega todo a él. Los decoradores concretos `EncryptionDecorator` y `CompressionDecorator` extienden la base: en `writeData` encriptan/comprimen antes de delegar, y en `readData` descifran/descomprimen después. El cliente monta la pila (por ejemplo `Cifrado > Compresión > FileDataSource`), de modo que justo antes de escribir en disco los datos se encriptan y comprimen, y al leerlos pasan por los mismos decoradores que los descomprimen y decodifican. La clase original escribe los datos ya protegidos sin conocer el cambio. `SalaryManager` trabaja con una fuente de datos preconfigurada sin preocuparse por el almacenamiento, y `ApplicationConfigurator` monta distintas pilas en tiempo de ejecución según la configuración (`enabledEncryption`, `enabledCompression`).

## Aplicabilidad

- Úsalo cuando necesites asignar funcionalidades adicionales a objetos en tiempo de ejecución sin descomponer el código que los utiliza; permite estructurar la lógica de negocio en capas y componer combinaciones distintas.
- Úsalo cuando resulte extraño o imposible extender el comportamiento por herencia. Para una clase `final`, la única forma de reutilizar su comportamiento es envolverla con tu propio wrapper usando Decorator.

## Cómo implementarlo

1. Verifica que el dominio puede representarse como un componente primario con varias capas opcionales encima.
2. Decide los métodos comunes al componente y las capas, y declara una interfaz de componente con ellos.
3. Crea una clase concreta de componente con el comportamiento base.
4. Crea la clase base decoradora con un campo (de tipo interfaz de componente) que referencie al objeto envuelto, delegando todas las operaciones.
5. Asegúrate de que todas las clases implementan la interfaz de componente.
6. Crea los decoradores concretos extendiendo la base, ejecutando su comportamiento antes o después del método padre.
7. El código cliente es responsable de crear y componer los decoradores.

## Pros y contras

Pros: extender el comportamiento de un objeto sin crear una nueva subclase; añadir o eliminar responsabilidades en tiempo de ejecución; combinar comportamientos envolviendo un objeto con varios decoradores; aplicar el principio de responsabilidad única dividiendo una clase monolítica en clases más pequeñas. Contras: resulta difícil eliminar un wrapper específico de la pila; es difícil lograr que el comportamiento no dependa del orden en la pila; el código de configuración inicial de las capas puede tener un aspecto desagradable.

## Relaciones con otros patrones

- **Adapter** cambia la interfaz de un objeto; Decorator la mejora sin cambiarla y soporta composición recursiva. Adapter da una interfaz diferente, Proxy la misma y Decorator una mejorada.
- **Chain of Responsibility** y Decorator tienen estructuras similares (composición recursiva), pero los manejadores de CoR pueden ejecutar operaciones arbitrarias y detener la solicitud, mientras que los decoradores no pueden romper el flujo.
- **Composite** y Decorator comparten diagrama; un Decorator es como un Composite con un solo componente hijo, pero Decorator añade responsabilidades y Composite solo “recapitula” resultados de sus hijos. Pueden colaborar.
- Diseños con uso amplio de Composite y Decorator pueden beneficiarse de **Prototype** para clonar estructuras complejas.
- Decorator cambia “la piel” de un objeto; **Strategy** cambia sus “entrañas”.
- Decorator y **Proxy** tienen estructuras similares pero propósitos distintos: Proxy suele gestionar el ciclo de vida de su objeto por su cuenta, mientras que la composición de los decoradores siempre la controla el cliente.

## Ideas clave

- Decorator añade funcionalidades envolviendo un objeto en wrappers que comparten su interfaz.
- Resuelve las limitaciones de la herencia (estática, una sola clase padre) mediante agregación/composición.
- El cliente trata igual al objeto puro y al decorado porque todos siguen la misma interfaz.
- Los decoradores se apilan y actúan antes o después de delegar la solicitud al objeto envuelto.
- Permite añadir y quitar responsabilidades en tiempo de ejecución y combinar comportamientos.
- Favorece el principio de responsabilidad única al dividir clases monolíticas.
- Inconvenientes: quitar un wrapper concreto es difícil, el comportamiento puede depender del orden y la configuración inicial puede ser aparatosa.
