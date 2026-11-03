# Dive Into Design Patterns — Alexander Shvets (Refactoring.Guru, 2021)
## Capítulo 18 — Singleton (Singleton)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF (con palabras pegadas por la justificación) y las citas usan la página del PDF.

## Lo que necesitas saber

Singleton es un patrón de diseño creacional que asegura que una clase tenga una única instancia y, al mismo tiempo, proporciona un punto de acceso global a esa instancia. También se le llama "Instancia única".

El patrón resuelve dos problemas a la vez, lo que de entrada vulnera el Principio de responsabilidad única. El primero es garantizar que una clase tenga una sola instancia, algo habitual cuando se controla el acceso a un recurso compartido (una base de datos, un archivo). El segundo es ofrecer un punto de acceso global a esa instancia, como harías con una variable global, pero sin el riesgo de que cualquier código la sobrescriba.

Sales sabiendo cómo esconder el constructor, cómo exponer un método de creación estático con inicialización diferida, cuándo conviene usar Singleton, qué tratamiento especial exige en entornos multihilo y qué contras asumes (acoplamiento oculto, dificultad para las pruebas unitarias).

## El ejemplo que recorre el capítulo

El hilo conductor es una clase de conexión a base de datos. Esta clase no tiene constructor público, por lo que la única manera de obtener su objeto es invocar el método `obtenerInstancia` (`getInstance`), que almacena en caché el primer objeto creado y lo devuelve en todas las llamadas siguientes. La analogía del mundo real es el gobierno: un país solo tiene un gobierno oficial, y el título "Gobierno de X" actúa como punto de acceso global independientemente de quién lo integre (PDF p. 152).

## Problema

- Controlar cuántas instancias tiene una clase suele servir para controlar el acceso a un recurso compartido. En lugar de recibir un objeto nuevo, el cliente obtiene el que ya se había creado, muchas veces sin darse cuenta de que trabaja siempre con el mismo objeto.
- Este comportamiento es imposible de implementar con un constructor normal, ya que por diseño una llamada al constructor siempre devuelve un objeto nuevo.
- Las variables globales son útiles pero poco seguras: cualquier código podría sobrescribirlas y descomponer la aplicación. Singleton permite acceder al objeto desde cualquier parte del programa y, a la vez, evita que otro código sobrescriba esa instancia.
- También conviene no dispersar por todo el programa el código que resuelve el primer problema; es mejor tenerlo dentro de una clase.

## Solución

Todas las implementaciones comparten dos pasos:

- Hacer privado el constructor por defecto para impedir que otros objetos usen `new` con la clase Singleton.
- Crear un método de creación estático que actúe como constructor: invoca al constructor privado, guarda el objeto en un campo estático y, en las llamadas siguientes, devuelve el objeto almacenado en caché.

Así, cada vez que se invoque el método estático se devolverá siempre el mismo objeto.

## Estructura

La clase Singleton declara el método estático `obtenerInstancia`, que devuelve la misma instancia de su propia clase. El constructor debe ocultarse del código cliente, de modo que la llamada a `obtenerInstancia` sea la única manera de obtener el objeto.

## Pseudocódigo

La clase `Database` ilustra el patrón: campo estático privado para la instancia, constructor privado e `getInstance` con inicialización diferida y bloqueo de hilo para el caso multihilo.

```
class Database is
    private static field instance: Database

    private constructor Database() is
        // Inicialización, p. ej. la conexión al servidor.

    public static method getInstance() is
        if (Database.instance == null) then
            acquireThreadLock() and then
                // Comprobar de nuevo que ningún otro hilo la
                // inicializó mientras éste esperaba el desbloqueo.
                if (Database.instance == null) then
                    Database.instance = new Database()
        return Database.instance

    public method query(sql) is
        // Toda consulta pasa por aquí: lugar para throttling o caché.

class Application is
    method main() is
        Database foo = Database.getInstance()
        foo.query("SELECT ...")
        Database bar = Database.getInstance()
        bar.query("SELECT ...")
        // `bar` contiene el mismo objeto que `foo`.
```

## Aplicabilidad

- Úsalo cuando una clase deba tener una sola instancia disponible para todos los clientes (por ejemplo, un único objeto de base de datos compartido). El patrón deshabilita las demás formas de crear objetos salvo el método especial de creación, que crea un objeto nuevo o devuelve el existente.
- Úsalo cuando necesites un control más estricto de las variables globales: a diferencia de estas, Singleton garantiza una única instancia y nada, salvo la propia clase, puede sustituir la instancia en caché. Si hace falta, puedes ajustar la limitación para permitir cierto número de instancias cambiando solo el cuerpo de `getInstance`.

## Cómo implementarlo

1. Añade un campo estático privado para almacenar la instancia.
2. Declara un método de creación estático público para obtenerla.
3. Implementa una inicialización diferida: crea el objeto en la primera llamada y devuélvelo en las siguientes.
4. Declara el constructor como privado; el método estático podrá seguir invocándolo, pero no otros objetos.
5. Repasa el código cliente y sustituye las llamadas directas al constructor por llamadas al método de creación estático.

## Pros y contras

Pros:

- Certeza de que una clase tiene una única instancia.
- Punto de acceso global a dicha instancia.
- La instancia solo se inicializa cuando se requiere por primera vez.

Contras:

- Vulnera el Principio de responsabilidad única al resolver dos problemas a la vez.
- Puede enmascarar un mal diseño, por ejemplo cuando los componentes saben demasiado unos de otros.
- Requiere tratamiento especial en entornos multihilo para que varios hilos no creen el objeto varias veces.
- Dificulta las pruebas unitarias del código cliente: muchos frameworks dependen de la herencia para crear mock objects, y como el constructor es privado y en la mayoría de lenguajes no se pueden sobrescribir métodos estáticos, hay que idear una forma original de simular el Singleton.

## Relaciones con otros patrones

- Una Facade suele poder transformarse en Singleton, ya que un único objeto fachada basta en la mayoría de los casos.
- Flyweight puede asemejarse a Singleton si reduces todo el estado compartido a un único objeto flyweight, pero hay dos diferencias: solo debe existir una instancia de Singleton (Flyweight puede tener varias con distintos estados intrínsecos), y el Singleton puede ser mutable mientras que los flyweight son inmutables.
- Abstract Factory, Builder y Prototype pueden implementarse como Singletons.

## Ideas clave

- Singleton garantiza una única instancia y un punto de acceso global a ella.
- Resuelve dos problemas a la vez, lo que de entrada vulnera el Principio de responsabilidad única.
- Se construye ocultando el constructor y exponiendo un método de creación estático con inicialización diferida y caché.
- Es una alternativa más segura y controlada que las variables globales.
- En entornos multihilo exige bloqueo para evitar crear el objeto más de una vez.
- Puede enmascarar acoplamiento excesivo entre componentes.
- Complica las pruebas unitarias por su dependencia de constructores privados y métodos estáticos.
