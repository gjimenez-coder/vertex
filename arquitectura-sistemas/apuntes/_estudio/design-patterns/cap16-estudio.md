# Builder (Constructor) — Estudio

## Tarjetas de repaso

P: ¿Qué tipo de patrón es Builder y qué permite hacer?
R: Es un patrón de diseño creacional que permite construir objetos complejos paso a paso y producir distintos tipos y representaciones con el mismo código de construcción.

P: ¿Cuándo aporta valor el patrón Builder?
R: Cuando la inicialización de un objeto es laboriosa: muchos campos y objetos anidados que quedarían sepultados en un constructor monstruoso o dispersos por el código cliente.

P: ¿Cuál es la idea central del patrón?
R: Sacar el código de construcción de la clase del producto y colocarlo en objetos independientes llamados constructores (builders), invocando solo los pasos que cada configuración necesita.

P: ¿Qué dos problemas resuelve Builder?
R: El constructor telescópico (un único constructor gigante con muchos parámetros opcionales sin usar) y la explosión de subclases por cada combinación de parámetros.

P: ¿Cómo se crean distintas representaciones de un producto con Builder?
R: Con varios constructores que implementan los mismos pasos de forma diferente (p. ej. paredes de madera para una cabaña, de piedra para un castillo) y un cliente que interactúa mediante una interfaz común.

P: ¿Qué es la clase directora y qué hace?
R: Una clase que define el orden en que se ejecutan los pasos de construcción; el constructor aporta la implementación. Es opcional, pero encapsula rutinas reutilizables y oculta los detalles al cliente.

P: ¿Qué declara la interfaz Constructora?
R: Los pasos de construcción comunes a todos los tipos de constructores.

P: ¿Deben los Productos pertenecer a la misma jerarquía o interfaz?
R: No. Los constructores concretos pueden crear productos que no siguen una interfaz común ni comparten jerarquía de clases.

P: ¿Por qué el método de extracción (getProduct) no se declara en la interfaz constructora?
R: Porque cuando los productos no comparten interfaz el tipo de retorno varía y no puede declararse en la interfaz en lenguajes de tipado estático; vive en el constructor concreto.

P: ¿Para qué se invoca reset al final de getProduct?
R: Para dejar el constructor listo para elaborar otro producto; es práctica común.

P: En el pseudocódigo, ¿qué construye CarManualBuilder y en qué se diferencia de CarBuilder?
R: Construye un Manual reutilizando el mismo proceso: implementa los mismos métodos pero, en lugar de fabricar piezas, las describe. Car y Manual no comparten interfaz.

P: ¿De dónde se extrae el resultado final de la construcción y por qué?
R: Del constructor, no del director, porque el director no conoce ni depende de constructores y productos concretos.

P: ¿Cuáles son los pros del patrón Builder?
R: Construir objetos paso a paso (aplazando o ejecutando pasos de forma recursiva), reutilizar el mismo código para varias representaciones y cumplir el principio de responsabilidad única aislando la construcción compleja de la lógica de negocio.

P: ¿Cuál es el principal contra del patrón?
R: Aumenta la complejidad general del código porque exige crear varias clases nuevas.

## Preguntas de autoevaluación

P: ¿Por qué crear una subclase de Casa por cada combinación de parámetros es problemático?
R: Hace crecer sin control la jerarquía: cada parámetro nuevo (p. ej. el estilo del porche) la amplía más. (Sección: Problema)

P: ¿Qué desventaja tiene resolver el problema con un único constructor gigante?
R: Elimina las subclases, pero no todos los parámetros son necesarios siempre, así que gran parte queda sin usar y las llamadas resultan feas. (Sección: Problema)

P: ¿Es obligatoria la clase directora para usar el patrón? Justifica.
R: No es estrictamente necesaria: el cliente puede invocar los pasos directamente. Pero es un buen lugar para colocar rutinas de construcción reutilizables y ocultar los detalles al cliente. (Sección: Clase directora)

P: ¿Cuáles son los cinco elementos de la estructura del patrón?
R: La interfaz Constructora, los Constructores Concretos, los Productos, la Directora y el Cliente. (Sección: Estructura)

P: ¿En qué casos conviene aplicar Builder según la aplicabilidad del capítulo?
R: Para evitar el constructor telescópico, para crear distintas representaciones de un producto con pasos similares que varían en los detalles, y para construir árboles con Composite u otros objetos complejos de forma recursiva. (Sección: Aplicabilidad)

P: ¿Cómo se relacionan Builder y Abstract Factory?
R: Builder construye objetos complejos paso a paso y permite pasos adicionales antes de extraer el producto; Abstract Factory crea familias de objetos relacionados y devuelve el producto de inmediato. (Sección: Relaciones con otros patrones)

P: ¿Qué papel cumplen la directora y las constructoras cuando Builder se combina con Bridge?
R: La directora hace de abstracción y las constructoras de implementaciones. (Sección: Relaciones con otros patrones)

P: ¿Qué garantía ofrece Builder sobre el producto durante la construcción?
R: El producto incompleto nunca se expone al cliente; el constructor no permite a otros objetos acceder al producto mientras se construye. (Secciones: Solución e Ideas clave)

## Checklist

Cómo implementarlo (pasos prácticos que respalda el capítulo):

- [ ] Definir claramente los pasos de construcción comunes a todas las representaciones; si no se puede, no procede el patrón.
- [ ] Declarar esos pasos en la interfaz constructora base.
- [ ] Crear un constructor concreto por representación e implementar sus pasos, incluyendo un método de extracción (fuera de la interfaz si los productos no comparten jerarquía).
- [ ] Considerar una clase directora que encapsule varias formas de construir usando el mismo constructor.
- [ ] En el cliente, crear constructor y director, y pasar el constructor al director antes de construir.
- [ ] Obtener el resultado del director solo si todos los productos siguen la misma interfaz; si no, extraerlo del constructor.
- [ ] Invocar reset al final de getProduct para dejar el constructor listo para otro producto.
