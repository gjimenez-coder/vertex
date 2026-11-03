# Clean Code: A Handbook of Agile Software Craftsmanship — Robert C. Martin (Prentice Hall, 2008)
## Capítulo 8 — Boundaries (Límites)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas usan la página del PDF.

## Lo que necesitas saber

El capítulo (escrito por James Grenning) trata de cómo integrar limpiamente en nuestro sistema el software que no controlamos: paquetes de terceros, código open source o subsistemas producidos por otros equipos de la propia empresa. En esos puntos de contacto —los "límites" o *boundaries*— aparecen tensiones y riesgos que conviene gestionar de forma deliberada.

La tesis central es que debemos aislar nuestro código de las particularidades del código ajeno: depender de algo que controlamos es mejor que depender de algo que no controlamos, "no sea que acabe controlándonos a nosotros" (PDF p. 151). Para ello se limita el número de lugares que conocen el detalle externo, se envuelve o adapta la interfaz, y se respaldan los límites con pruebas.

Sales sabiendo tres técnicas concretas: encapsular interfaces de terceros demasiado amplias (ejemplo de `Map`), escribir *learning tests* para explorar y vigilar una API externa (ejemplo de log4j), y definir la interfaz que desearíamos tener cuando el código del otro lado todavía no existe (ejemplo del *Transmitter*).

## Using Third-Party Code (Usar código de terceros)

Existe una tensión natural entre quien provee una interfaz y quien la usa: los proveedores buscan amplia aplicabilidad para muchos entornos y audiencias, mientras que los usuarios quieren una interfaz enfocada a sus necesidades concretas. Esa tensión causa problemas en los límites.

El ejemplo es `java.util.Map`: una interfaz muy amplia con muchas capacidades. Esa potencia también es una responsabilidad. Si pasamos un `Map` por el sistema, cualquier receptor puede llamar a `clear()` y vaciarlo, y los `Map` no restringen de forma fiable los tipos que se almacenan; cualquier usuario decidido puede añadir elementos de cualquier tipo.

Un uso típico aparece así:

```java
Map sensors = new HashMap();
...
Sensor s = (Sensor)sensors.get(sensorId);
```

El cliente carga con la responsabilidad de obtener un `Object` y castearlo, repetido una y otra vez. Los *generics* mejoran la legibilidad:

```java
Map<Sensor> sensors = new HashMap<Sensor>();
...
Sensor s = sensors.get(sensorId);
```

Pero `Map<Sensor>` sigue ofreciendo más capacidad de la que necesitamos, y pasar esa instancia por todo el sistema crea muchos lugares que arreglar si la interfaz de `Map` cambia (como ocurrió al añadirse *generics* en Java 5). La forma más limpia es encapsularla:

```java
public class Sensors {
    private Map sensors = new HashMap();

    public Sensor getById(String id) {
        return (Sensor) sensors.get(id);
    }
    //snip
}
```

Así la interfaz del límite (`Map`) queda oculta y puede evolucionar con poco impacto; el uso de *generics* pasa a ser un detalle de implementación. La interfaz queda además ajustada y restringida a las necesidades de la aplicación, es más difícil de usar mal, y la clase `Sensors` puede imponer reglas de diseño y de negocio.

El consejo no es encapsular todo `Map`, sino no pasar `Map` (ni otra interfaz de límite) por el sistema: mantenerla dentro de la clase, o de una familia cercana de clases, y evitar devolverla o aceptarla como argumento en APIs públicas.

## Exploring and Learning Boundaries (Explorar y aprender los límites)

El código de terceros nos da más funcionalidad en menos tiempo. No es nuestro trabajo probar ese código, pero sí nos conviene escribir pruebas para él. Aprender e integrar una librería externa a la vez es doblemente difícil, y es fácil quedar atrapado en largas sesiones de depuración sin saber si el fallo es nuestro o suyo.

La alternativa son los *learning tests* (nombre acuñado por Jim Newkirk): en lugar de experimentar en el código de producción, escribimos pruebas que exploran nuestra comprensión de la API, llamándola como esperamos usarla. Son experimentos controlados enfocados en lo que queremos obtener de la API.

## Learning log4j (Aprender log4j)

Como ejemplo se quiere usar apache log4j en lugar de un *logger* propio. Se empieza con un test que espera imprimir "hello" en consola:

```java
@Test
public void testLogCreate() {
    Logger logger = Logger.getLogger("MyLogger");
    logger.info("hello");
}
```

El *logger* da error: hace falta un `Appender`. Se prueba con `ConsoleAppender`, pero carece de *output stream*. Tras más lectura y búsquedas se llega a:

```java
logger.removeAllAppenders();
logger.addAppender(new ConsoleAppender(
    new PatternLayout("%p %t %m%n"),
    ConsoleAppender.SYSTEM_OUT));
logger.info("hello");
```

Experimentando, se ve que quitar `ConsoleAppender.SystemOut` sigue imprimiendo, pero quitar `PatternLayout` vuelve a quejarse por la falta de *output stream*: el constructor por defecto de `ConsoleAppender` queda "unconfigured", algo poco obvio, que parece un bug o una inconsistencia. Todo ese conocimiento queda codificado en un conjunto de pruebas unitarias simples (`LogTest.java`), que luego permite encapsular la inicialización en una clase propia aislada del límite de log4j.

## Learning Tests Are Better Than Free (Los learning tests salen gratis o mejor)

Los *learning tests* no cuestan nada: de todos modos había que aprender la API, y escribirlos es una forma fácil y aislada de adquirir ese conocimiento. Además tienen retorno positivo: cuando sale una nueva versión del paquete, se ejecutan para detectar diferencias de comportamiento. Verifican que el código de terceros sigue funcionando como esperamos, porque sus autores tienen presiones para cambiarlo, arreglar bugs y añadir capacidades, y cada versión trae riesgo. Si un cambio es incompatible con nuestras pruebas, lo sabremos de inmediato. Se necesiten o no, un límite limpio debe apoyarse en pruebas que ejerciten la interfaz igual que el código de producción, facilitando la migración.

## Using Code That Does Not Yet Exist (Usar código que aún no existe)

Hay otro tipo de límite: el que separa lo conocido de lo desconocido. En un sistema de comunicaciones por radio, había un subsistema, el "Transmitter", poco conocido y cuya interfaz aún no estaba definida. Para no quedar bloqueados, el equipo empezó a trabajar lejos de esa parte desconocida.

Al toparse con el límite, supieron qué querían de la interfaz: algo como "sintoniza el transmisor en la frecuencia dada y emite una representación analógica de los datos de este *stream*". Como la API no existía, definieron su propia interfaz, `Transmitter`, con un método `transmit` que recibía una frecuencia y un *data stream*: la interfaz que desearían tener. Lo bueno de escribir la interfaz deseada es que está bajo nuestro control, y mantiene el código cliente legible y enfocado.

Así se aisló `CommunicationsController` de la API indefinida del transmisor. Cuando la API quedó definida, se escribió un `TransmitterAdapter` para salvar la distancia; el patrón ADAPTER (del libro [GOF]) encapsula la interacción y ofrece un único lugar que cambiar cuando la API evoluciona. El diseño también da una *seam* conveniente para pruebas: con un `FakeTransmitter` se prueba `CommunicationsController`, y se pueden crear pruebas de límite una vez exista la API real.

## Clean Boundaries (Límites limpios)

En los límites pasan cosas interesantes, sobre todo el cambio. Un buen diseño acomoda el cambio sin grandes inversiones ni retrabajo. El código del límite necesita separación clara y pruebas que definan las expectativas, evitando que demasiado código conozca los detalles del tercero. Gestionamos los límites teniendo muy pocos lugares que los referencien: envolviéndolos (como con `Map`) o usando un ADAPTER que convierta de nuestra interfaz ideal a la provista. En cualquier caso, el código se expresa mejor, promueve un uso consistente a través del límite y tiene menos puntos de mantenimiento cuando el código de terceros cambia.

## Ideas clave

- En los límites del sistema (código de terceros, open source, subsistemas de otros equipos) hay tensión entre proveedor y usuario de la interfaz; gestiónalos con cuidado.
- No pases interfaces de límite como `Map` por todo el sistema: mantenlas dentro de una clase o familia de clases y evita devolverlas o aceptarlas en APIs públicas.
- Encapsular la interfaz externa la hace evolucionar con poco impacto, la ajusta a tus necesidades, la hace más difícil de usar mal y permite imponer reglas de negocio.
- Los *learning tests* exploran una API externa con experimentos controlados, sin mezclar aprendizaje e integración en el código de producción.
- Los *learning tests* salen gratis o con retorno positivo: ante una nueva versión, detectan de inmediato cambios de comportamiento incompatibles.
- Cuando el código del otro lado no existe aún, define "la interfaz que desearías tener"; queda bajo tu control y mantiene el cliente limpio.
- El patrón ADAPTER puente entre tu interfaz ideal y la API real, y concentra en un solo sitio los cambios cuando esa API evoluciona; también crea *seams* para pruebas.
- Es mejor depender de algo que controlas que de algo que no controlas; limita los lugares del código que conocen los detalles del tercero.
