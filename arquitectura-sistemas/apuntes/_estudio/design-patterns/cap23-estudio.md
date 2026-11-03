# Facade (Fachada) — Estudio

## Tarjetas de repaso

P: ¿Qué tipo de patrón de diseño es Facade? / R: Un patrón estructural que proporciona una interfaz simplificada a una biblioteca, framework o grupo complejo de clases.

P: ¿Cuál es el objetivo principal de Facade? / R: Que el código cliente use solo las funciones realmente importantes de un subsistema complejo sin lidiar con su maquinaria interna.

P: ¿Qué problema resuelve Facade? / R: El acoplamiento de la lógica de negocio a los detalles de implementación de clases de terceros (inicializarlas, gestionar dependencias, ordenar llamadas), que la hace difícil de comprender y mantener.

P: ¿Añade Facade funcionalidad nueva al subsistema? / R: No; solo ofrece una interfaz simplificada, incluso con funcionalidad limitada respecto a trabajar directamente con el subsistema.

P: ¿Conocen las clases del subsistema a la fachada? / R: No; operan dentro del sistema y trabajan entre sí directamente, sin saber de la existencia de la fachada.

P: ¿Para qué sirve una fachada adicional? / R: Para evitar contaminar una única fachada con funciones no relacionadas que la volverían compleja; pueden usarla clientes y otras fachadas.

P: ¿Qué papel cumple el Cliente en la estructura? / R: Usa la fachada en lugar de invocar directamente los objetos del subsistema.

P: ¿Qué beneficio aporta Facade ante cambios del framework? / R: Al actualizar o cambiar el framework solo hay que reescribir la clase fachada, protegiendo al cliente.

P: ¿Cuál es el principal riesgo de Facade? / R: Convertirse en un objeto todopoderoso acoplado a todas las clases de la aplicación.

P: ¿En qué se diferencian Facade y Adapter? / R: Facade define una interfaz nueva para objetos existentes y trabaja con todo un subsistema; Adapter hace usable una interfaz existente y normalmente envuelve un solo objeto.

P: ¿En qué se diferencian Facade y Mediator? / R: Ambos organizan clases muy acopladas, pero Facade no introduce funcionalidad nueva y el subsistema no la conoce; Mediator centraliza la comunicación y los componentes solo conocen al mediador.

P: ¿Por qué una fachada suele poder ser Singleton? / R: Porque un único objeto fachada basta en la mayoría de los casos.

P: ¿En qué se diferencian Facade y Proxy? / R: Proxy tiene la misma interfaz que su objeto de servicio (son intercambiables); Facade define una interfaz distinta para todo un subsistema.

## Preguntas de autoevaluación

P: ¿Cuándo conviene usar el patrón Facade? / R: Cuando se necesita una interfaz limitada pero directa a un subsistema complejo, o cuando se quiere estructurar un subsistema en capas. (Sección "Aplicabilidad")

P: En el ejemplo del framework de conversión de vídeo, ¿qué encapsula la clase `VideoConverter` y tras qué método? / R: Encapsula las clases del framework (`VideoFile`, `OggCompressionCodec`, `MPEG4CompressionCodec`, `CodecFactory`, `BitrateReader`, `AudioMixer`) tras un único método `convert(filename, format)`. (Sección "El ejemplo que recorre el capítulo")

P: ¿Cómo ilustra la analogía del pedido por teléfono el papel de una fachada? / R: El operador es la fachada que da una interfaz de voz sencilla al sistema de pedidos, las pasarelas de pago y los servicios de entrega. (Sección "Analogía en el mundo real")

P: ¿Qué pasos clave propone el capítulo para implementar una fachada? / R: Comprobar si cabe una interfaz más simple; declararla e implementarla en una clase fachada que redirija llamadas y gestione el ciclo de vida del subsistema; hacer que todo el cliente se comunique solo por la fachada; y extraer una fachada refinada si crece demasiado. (Sección "Cómo implementarlo")

P: ¿Cómo ayuda Facade a estructurar un subsistema en capas? / R: Creando fachadas que definan puntos de entrada a cada nivel y exigiendo que los subsistemas se comuniquen solo mediante fachadas, lo que reduce el acoplamiento; por ejemplo, separar capa de vídeo y de audio. (Sección "Aplicabilidad")

P: ¿Cuáles son el pro y el contra principales del patrón? / R: A favor, aísla el código de la complejidad de un subsistema; en contra, la fachada puede volverse un objeto todopoderoso acoplado a toda la aplicación. (Sección "Pros y contras")

P: ¿Qué diferencia a Facade de Abstract Factory y de Flyweight? / R: Abstract Factory puede sustituir a Facade cuando solo se quiere ocultar cómo se crean los objetos; Flyweight crea muchos objetos pequeños, mientras Facade crea un único objeto que representa un subsistema completo. (Sección "Relaciones con otros patrones")

## Puntos a dominar

- Definir Facade como patrón estructural que simplifica el acceso a un subsistema complejo sin añadir funcionalidad nueva.
- Identificar el problema del acoplamiento entre lógica de negocio y detalles de bibliotecas/frameworks de terceros.
- Reconocer los cuatro elementos de la estructura: Facade, Fachada Adicional, Subsistema Complejo y Cliente.
- Recordar que el subsistema no conoce la fachada y sus objetos siguen comunicándose entre sí directamente.
- Enumerar los dos casos de aplicabilidad: interfaz limitada directa y estructuración en capas.
- Reproducir los pasos de implementación, incluida la extracción de una fachada refinada cuando crece en exceso.
- Distinguir Facade de Adapter, Mediator, Proxy, Abstract Factory, Flyweight y Singleton.
- Tener presente el riesgo de que la fachada se convierta en un objeto todopoderoso.
