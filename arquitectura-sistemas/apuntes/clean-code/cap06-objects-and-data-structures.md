# Clean Code: A Handbook of Agile Software Craftsmanship — Robert C. Martin (Prentice Hall, 2008)
## Capítulo 6 — Objects and Data Structures (Objetos y estructuras de datos)

> Nota de extracción: texto obtenido de la capa de texto del PDF; las citas usan la página del PDF.

## Lo que necesitas saber

El capítulo parte de una pregunta incómoda: si mantenemos las variables privadas para no depender de su tipo o implementación, ¿por qué tantos programadores añaden automáticamente getters y setters que exponen esas variables como si fueran públicas? A partir de ahí Martin distingue dos conceptos complementarios y casi opuestos: los objetos, que ocultan sus datos tras abstracciones y exponen funciones que operan sobre ellos; y las estructuras de datos, que exponen sus datos y no tienen funciones significativas.

La tesis central es que no todo debe ser un objeto: la idea de que "todo es un objeto" es un mito. Objetos y estructuras de datos ofrecen flexibilidades contrarias, y un buen diseñador elige según lo que el sistema necesite añadir con más facilidad: tipos nuevos o funciones nuevas.

Sales sabiendo qué es la abstracción de datos (frente a simplemente poner accesores), la anti-simetría datos/objeto, la Ley de Demeter y sus "train wrecks", el problema de los híbridos, y las variantes de estructuras de datos: DTO, beans y Active Record.

## Abstracción de datos (Data Abstraction)

Ocultar la implementación no es solo poner una capa de funciones entre las variables: es cuestión de abstracciones. Una clase no debe empujar sus variables hacia afuera mediante getters y setters, sino exponer interfaces abstractas que permitan manipular la esencia de los datos sin conocer su implementación.

El ejemplo del punto cartesiano lo ilustra. Un `Point` con `x` e `y` públicos (o con getters/setters por variable) está claramente implementado en coordenadas rectangulares y obliga a manipular las coordenadas por separado: expone implementación. En cambio, la versión abstracta no deja ver si la implementación es rectangular, polar o ninguna, y además impone una política de acceso: se leen las coordenadas de forma independiente, pero se fijan juntas como operación atómica.

```java
public interface Point {
  double getX();
  double getY();
  void setCartesian(double x, double y);
  double getR();
  double getTheta();
  void setPolar(double r, double theta);
}
```

Con el `Vehicle` ocurre igual: exponer `getFuelTankCapacityInGallons()` y `getGallonsOfGasoline()` son accesores concretos; exponer `getPercentFuelRemaining()` expresa el dato en términos abstractos. La peor opción es añadir getters y setters sin pensar; hay que reflexionar sobre la mejor manera de representar los datos.

## Anti-simetría datos/objeto (Data/Object Anti-Symmetry)

Objetos y estructuras de datos son opuestos virtuales, y esa diferencia tiene implicaciones de gran alcance. El ejemplo de las formas lo muestra:

- Versión procedimental: clases `Square`, `Rectangle`, `Circle` como simples estructuras de datos sin comportamiento, y una clase `Geometry` que concentra toda la lógica (por ejemplo `area(Object shape)` con `instanceof`). Añadir una función nueva como `perimeter()` no afecta a las formas ni a quienes dependen de ellas; pero añadir una forma nueva obliga a cambiar todas las funciones de `Geometry`.
- Versión orientada a objetos: cada forma implementa `Shape` con su propio `area()` polimórfico, sin clase `Geometry`. Añadir una forma nueva no afecta a las funciones existentes; pero añadir una función nueva obliga a cambiar todas las formas.

De ahí la dicotomía fundamental:

> "Procedural code makes it easy to add new functions without changing the existing data structures. OO code... makes it easy to add new classes without changing existing functions." (PDF p. 128)

Y su complemento: el código procedimental dificulta añadir estructuras de datos nuevas (hay que cambiar todas las funciones), mientras que el OO dificulta añadir funciones nuevas (hay que cambiar todas las clases). Lo difícil para OO es fácil para procedimientos y viceversa. Hay técnicas conocidas para esquivar el problema en OO (VISITOR, dual-dispatch), pero tienen costes y suelen devolver el programa a una estructura procedimental.

## La Ley de Demeter (The Law of Demeter)

Heurística que dice que un módulo no debe conocer las entrañas de los objetos que manipula. Más precisamente, un método `f` de una clase `C` solo debería llamar a los métodos de:

- `C`
- un objeto creado por `f`
- un objeto pasado como argumento a `f`
- un objeto guardado en una variable de instancia de `C`

El método no debe invocar métodos sobre objetos devueltos por las funciones permitidas. En otras palabras: habla con amigos, no con extraños.

### Train wrecks

Encadenamientos como `ctxt.getOptions().getScratchDir().getAbsolutePath()` se llaman "train wrecks" (choque de trenes) porque parecen vagones acoplados; son estilo descuidado y conviene partirlos en variables intermedias. Que esto viole o no la Ley de Demeter depende de si `ctxt`, `Options` y `ScratchDir` son objetos o estructuras de datos: si son objetos, conocer sus entrañas es una violación clara; si son estructuras de datos, exponen su estructura de forma natural y Demeter no aplica. El uso de accesores confunde el asunto: con `ctxt.options.scratchDir.absolutePath` ni siquiera estaríamos preguntándonos por Demeter. El problema es que frameworks y estándares (p. ej. los "beans") exigen accesores y mutadores incluso en estructuras simples.

### Híbridos

La confusión genera estructuras híbridas, mitad objeto mitad estructura de datos: tienen funciones que hacen cosas importantes y a la vez variables públicas (o accesores/mutadores que las vuelven públicas de hecho). Dificultan añadir funciones nuevas y también estructuras nuevas: lo peor de ambos mundos. Hay que evitarlos; denotan un diseño confuso.

### Ocultar la estructura

Si `ctxt` es un objeto con comportamiento real, no deberíamos poder navegar por él. En lugar de pedirle el path absoluto del directorio scratch para construir un archivo, debemos decirle que haga algo:

```java
BufferedOutputStream bos = ctxt.createScratchFileStream(classFileName);
```

Así `ctxt` oculta sus internos y la función que llama no viola la Ley de Demeter navegando por objetos que no debería conocer.

## Data Transfer Objects (DTO)

La forma por excelencia de una estructura de datos es una clase con variables públicas y sin funciones: un Data Transfer Object. Son muy útiles al comunicarse con bases de datos o al parsear mensajes de sockets, y suelen ser la primera de una serie de etapas de traducción de datos crudos a objetos de la aplicación.

La forma "bean" es más habitual: variables privadas manipuladas por getters y setters (como la clase `Address`). Esa cuasi-encapsulación tranquiliza a algunos puristas OO, pero normalmente no aporta ningún otro beneficio.

### Active Record

Son DTO especiales: estructuras de datos con variables públicas (o accedidas por beans) que además tienen métodos de navegación como `save` y `find`, normalmente traducción directa de tablas de base de datos. El error frecuente es tratarlos como objetos metiéndoles reglas de negocio, creando un híbrido. La solución es tratar el Active Record como estructura de datos y crear objetos separados que contengan las reglas de negocio y oculten sus datos internos (probablemente instancias del propio Active Record).

## Ideas clave

- Ocultar la implementación es cuestión de abstracciones, no de poner getters y setters sobre las variables.
- Objetos: ocultan datos, exponen comportamiento. Estructuras de datos: exponen datos, sin comportamiento significativo. Son opuestos complementarios.
- El código procedimental facilita añadir funciones y dificulta añadir tipos de datos; el OO facilita añadir tipos y dificulta añadir funciones.
- La idea de que "todo es un objeto" es un mito: a veces conviene de verdad una estructura de datos simple con procedimientos operando sobre ella.
- Ley de Demeter: habla con amigos, no con extraños; un módulo no debe conocer las entrañas de los objetos que manipula.
- Los "train wrecks" encadenan llamadas sobre valores devueltos; su licitud depende de si se trata de objetos o de estructuras de datos.
- Los híbridos mitad objeto mitad estructura de datos son lo peor de ambos mundos; hay que evitarlos.
- DTO, beans y Active Record son estructuras de datos; las reglas de negocio van en objetos aparte que ocultan sus datos.
