# Dive Into Design Patterns — Alexander Shvets (Refactoring.Guru, 2021)
## Capítulo 23 — Facade (Fachada)

> Nota de extracción: texto obtenido de la capa de texto del PDF; las citas usan la página del PDF.

## Lo que necesitas saber

Facade es un patrón de diseño estructural que proporciona una interfaz simplificada a una biblioteca, un framework o cualquier otro grupo complejo de clases (PDF p. 227). Su objetivo es que el código cliente pueda usar solo las funciones realmente importantes de un subsistema complejo sin lidiar con toda su maquinaria interna.

La tesis central es que cuando tu código tiene que trabajar con un amplio grupo de objetos de una biblioteca sofisticada —inicializarlos, gestionar dependencias, ejecutar métodos en el orden correcto—, la lógica de negocio queda estrechamente acoplada a los detalles de implementación de clases de terceros, lo que la hace difícil de comprender y mantener. Una fachada rompe ese acoplamiento concentrando la complejidad tras una sola clase.

Sales sabiendo cuándo conviene una fachada (interfaz limitada pero directa a un subsistema complejo, o estructurar un subsistema en capas), cómo se implementa paso a paso, y cómo se diferencia de patrones afines como Adapter, Mediator, Proxy, Abstract Factory, Flyweight y Singleton.

## El ejemplo que recorre el capítulo

El hilo conductor es un framework complejo de conversión de vídeo (PDF p. 231). Una aplicación que sube breves vídeos de gatos a redes sociales podría usar una biblioteca de conversión profesional, pero en realidad solo necesita una clase con un método simple `codificar(nombreDelArchivo, formato)` (PDF p. 229). Al crear esa clase y conectarla con la biblioteca de conversión, se obtiene la primera fachada.

En el pseudocódigo, una clase `VideoConverter` encapsula las clases del framework (`VideoFile`, `OggCompressionCodec`, `MPEG4CompressionCodec`, `CodecFactory`, `BitrateReader`, `AudioMixer`) tras un único método `convert(filename, format)`:

```
class VideoConverter is
    method convert(filename, format):File is
        file = new VideoFile(filename)
        sourceCodec = new CodecFactory.extract(file)
        if (format == "mp4")
            destinationCodec = new MPEG4CompressionCodec()
        else
            destinationCodec = new OggCompressionCodec()
        buffer = BitrateReader.read(filename, sourceCodec)
        result = BitrateReader.convert(buffer, destinationCodec)
        result = (new AudioMixer()).fix(result)
        return new File(result)

class Application is
    method main() is
        convertor = new VideoConverter()
        mp4 = convertor.convert("funny-cats-video.ogg", "mp4")
        mp4.save()
```

Así la clase `Application` no depende de un millón de clases del framework; si se cambia de framework, solo hay que reescribir la clase fachada.

## Problema

Trabajar directamente con un amplio grupo de objetos de una biblioteca o framework obliga a inicializarlos, llevar el registro de dependencias y ejecutar los métodos en el orden correcto. El resultado es una lógica de negocio acoplada a los detalles de implementación de las clases de terceros, difícil de comprender y mantener.

## Solución

Una fachada es una clase que proporciona una interfaz simple a un subsistema complejo con muchas partes móviles. Puede ofrecer una funcionalidad limitada comparada con trabajar directamente con el subsistema, incluyendo solo las funciones realmente importantes para los clientes. Resulta útil cuando integras tu aplicación con una biblioteca sofisticada con decenas de funciones de la cual solo necesitas una pequeña parte.

## Analogía en el mundo real

Hacer pedidos por teléfono: cuando llamas a una tienda, el operador es tu fachada a todos los servicios y departamentos. Te da una sencilla interfaz de voz al sistema de pedidos, las pasarelas de pago y varios servicios de entrega (PDF p. 229).

## Estructura

1. El patrón **Facade** da un acceso práctico a una parte específica de la funcionalidad del subsistema: sabe a dónde dirigir la petición del cliente y cómo operar todas las partes móviles.
2. Puede crearse una clase **Fachada Adicional** para evitar contaminar una única fachada con funciones no relacionadas que la convertirían en otra estructura compleja. Las fachadas adicionales pueden usarse por clientes y por otras fachadas.
3. El **Subsistema Complejo** consiste en decenas de objetos diversos. Para que hagan algo significativo hay que profundizar en sus detalles de implementación (inicializar objetos en el orden correcto, suministrar datos en el formato adecuado). Las clases del subsistema no conocen la existencia de la fachada: operan dentro del sistema y trabajan entre sí directamente.
4. El **Cliente** usa la fachada en lugar de invocar directamente los objetos del subsistema.

## Aplicabilidad

- Úsalo cuando necesites una interfaz limitada pero directa a un subsistema complejo. Los subsistemas tienden a volverse más complejos con el tiempo; incluso aplicar patrones de diseño suele aumentar el número de clases. Facade ofrece un atajo a las funciones más utilizadas que mejor encajan con los requisitos del cliente.
- Úsalo cuando quieras estructurar un subsistema en capas. Crea fachadas que definan puntos de entrada a cada nivel y reduce el acoplamiento entre subsistemas exigiéndoles comunicarse solo mediante fachadas. En el ejemplo del vídeo, el framework puede dividirse en una capa de vídeo y otra de audio, cada una con su fachada; este procedimiento es similar al patrón Mediator.

## Cómo implementarlo

1. Comprueba si es posible ofrecer una interfaz más simple que la del subsistema existente. Vas bien si esa interfaz hace que el código cliente sea independiente de muchas de las clases del subsistema.
2. Declara e implementa esa interfaz en una nueva clase fachada, que redirija las llamadas del cliente a los objetos adecuados del subsistema y se responsabilice de inicializarlo y gestionar su ciclo de vida (salvo que el cliente ya lo haga).
3. Para aprovechar el patrón al máximo, haz que todo el código cliente se comunique con el subsistema solo a través de la fachada. Así el cliente queda protegido de cambios en el subsistema: al actualizarlo a una nueva versión solo se modifica la fachada.
4. Si la fachada se vuelve demasiado grande, extrae parte de su comportamiento a una nueva clase fachada refinada.

## Pros y contras

- A favor: puedes aislar tu código de la complejidad de un subsistema.
- En contra: una fachada puede convertirse en un objeto todopoderoso acoplado a todas las clases de una aplicación.

## Relaciones con otros patrones

- **Adapter**: Facade define una interfaz nueva para objetos existentes, mientras que Adapter intenta hacer usable la interfaz existente. Adapter normalmente envuelve un objeto; Facade trabaja con todo un subsistema.
- **Abstract Factory**: puede ser alternativa a Facade cuando solo quieres ocultar cómo se crean los objetos del subsistema.
- **Flyweight**: muestra cómo crear muchos objetos pequeños; Facade, cómo crear un único objeto que representa un subsistema completo.
- **Mediator**: ambos organizan la colaboración entre clases muy acopladas. Facade define una interfaz simplificada sin introducir funcionalidad nueva y el subsistema no la conoce; Mediator centraliza la comunicación y los componentes solo conocen al mediador.
- **Singleton**: una clase fachada suele poder transformarse en Singleton, pues un único objeto fachada basta en la mayoría de los casos.
- **Proxy**: ambos pueden almacenar y inicializar por su cuenta una entidad compleja. A diferencia de Facade, Proxy tiene la misma interfaz que su objeto de servicio, lo que los hace intercambiables.

## Ideas clave

- Facade es un patrón estructural que da una interfaz simplificada a un subsistema complejo, sin añadir funcionalidad nueva.
- Reduce el acoplamiento entre el código cliente y los detalles de implementación de bibliotecas o frameworks de terceros.
- El subsistema no conoce la fachada; sus objetos siguen comunicándose directamente entre sí.
- Al cambiar o actualizar el framework, solo hay que reescribir la clase fachada.
- Las fachadas adicionales o refinadas evitan que una sola fachada crezca en exceso.
- Sirve también para estructurar subsistemas en capas con un punto de entrada por nivel.
- Riesgo principal: convertirse en un objeto todopoderoso acoplado a toda la aplicación.
