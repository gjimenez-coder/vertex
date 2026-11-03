# Composite (Objeto compuesto) — Estudio

## Tarjetas de repaso

P: ¿Qué tipo de patrón es Composite y qué permite hacer? / R: Es un patrón de diseño estructural que permite componer objetos en estructuras de árbol y trabajar con esas estructuras como si fueran objetos individuales.

P: ¿Cuándo tiene sentido aplicar Composite? / R: Solo cuando el modelo central de la aplicación puede representarse en forma de árbol.

P: ¿Cuál es la tesis central del patrón? / R: Dar a elementos simples y contenedores una interfaz común para que el cliente invoque un comportamiento sobre toda la estructura sin conocer clases concretas ni el nivel de anidación; los objetos propagan la solicitud recursivamente.

P: ¿Qué papel cumple la Hoja (Leaf)? / R: Es un elemento básico sin subelementos; normalmente realiza la mayoría del trabajo real porque no tiene a quién delegar.

P: ¿Qué hace el Contenedor (compuesto) al recibir una solicitud? / R: Delega el trabajo a sus subelementos, procesa los resultados intermedios y devuelve el resultado final, operando con sus hijos solo a través de la interfaz componente.

P: ¿Qué es el Componente en la estructura del patrón? / R: La interfaz que describe las operaciones comunes a los elementos simples y complejos del árbol.

P: ¿Cómo trabaja el Cliente con los elementos? / R: A través de la interfaz componente, de modo que trata igual a elementos simples y complejos.

P: En el ejemplo de Productos y Cajas, ¿cómo se calcula el precio total? / R: Para un producto devuelve su precio; para una caja recorre cada artículo, pregunta su precio y suma el total, descendiendo recursivamente por cada caja interna, y puede añadir costos extra como empaquetado.

P: ¿Qué hace la clase CompoundGraphic en el pseudocódigo? / R: Es un contenedor que puede incluir cualquier cantidad de subformas (incluidas otras compuestas); en lugar de actuar por su cuenta, pasa la solicitud recursivamente a sus hijos y "suma" el resultado.

P: ¿Qué principios de diseño favorece Composite? / R: Favorece el polimorfismo, la recursión y el Principio de abierto/cerrado.

P: ¿Cuál es el principal inconveniente del patrón? / R: Puede ser difícil dar una interfaz común a clases cuya funcionalidad difiere demasiado, obligando a sobregeneralizarla y volviéndola más difícil de comprender.

P: ¿Por qué declarar los métodos de añadir/eliminar hijos en la interfaz componente es discutible? / R: Porque viola el Principio de segregación de la interfaz (quedarían vacíos en la hoja), aunque permite tratar todos los elementos por igual.

P: ¿Qué analogía del mundo real ilustra el patrón? / R: Una estructura militar (ejército, divisiones, brigadas, pelotones, escuadrones, soldados), donde las órdenes se dan arriba y se pasan hacia abajo por cada nivel.

P: ¿Cómo se relacionan Composite y Decorator? / R: Tienen diagramas similares por la composición recursiva, pero Decorator tiene un único componente hijo y añade responsabilidades, mientras Composite recapitula los resultados de sus hijos; además pueden colaborar.

## Preguntas de autoevaluación

P: ¿Por qué la solución directa de calcular el precio "desenvolviendo" todas las cajas resulta problemática? / R: Porque exige conocer de antemano las clases, el nivel de anidación y otros detalles, lo que la vuelve demasiado complicada o imposible. (Sección "El ejemplo que recorre el capítulo")

P: ¿Qué ventaja ofrece tratar productos y cajas a través de una interfaz común? / R: No hay que preocuparse por las clases concretas: productos simples y cajas sofisticadas se tratan por igual, y al invocar un método los objetos pasan la solicitud a lo largo del árbol, ejecutando el comportamiento recursivamente. (Sección "Problema y solución")

P: ¿Qué diferencia el trabajo que hacen las hojas frente a los contenedores? / R: Las hojas realizan la mayoría del trabajo real al no tener a quién delegar; los contenedores delegan en sus hijos y recapitulan resultados. (Sección "Estructura" / "Ideas clave")

P: ¿En qué dos situaciones conviene usar Composite según la aplicabilidad? / R: Cuando debes implementar una estructura de objetos en forma de árbol con hojas y contenedores que comparten interfaz, y cuando quieres que el cliente trate elementos simples y complejos de la misma forma sin preocuparse por su clase concreta. (Sección "Aplicabilidad")

P: ¿Cuál es el primer paso al implementar el patrón? / R: Asegurarte de que el modelo central puede representarse como árbol y dividirlo en elementos simples y contenedores (que deben poder contener ambos tipos). (Sección "Cómo implementarlo")

P: ¿Por qué el cliente del editor gráfico puede manejar estructuras muy complejas sin acoplarse a clases concretas? / R: Porque usa la interfaz común y no sabe si trabaja con una forma simple o compuesta. (Sección "Pseudocódigo")

P: ¿Cómo se relacionan Chain of Responsibility y Composite? / R: Se usan a menudo juntos: una hoja puede pasar una solicitud por la cadena de componentes padre hasta la raíz. (Sección "Relaciones con otros patrones")

P: ¿Por qué un diseño con uso amplio de Composite y Decorator se beneficia de Prototype? / R: Porque Prototype permite clonar estructuras complejas en vez de reconstruirlas. (Sección "Relaciones con otros patrones")

## Puntos a dominar

- Reconocer cuándo el modelo central puede representarse como un árbol, requisito indispensable para aplicar Composite.
- Identificar los cuatro elementos de la estructura: Componente (interfaz), Hoja, Contenedor (compuesto) y Cliente.
- Explicar cómo el contenedor delega el trabajo en sus hijos y recapitula los resultados de forma recursiva.
- Diseñar la interfaz componente con métodos que tengan sentido tanto para elementos simples como complejos.
- Usar un campo matriz tipado con la interfaz componente en el contenedor para almacenar subelementos de ambos tipos.
- Entender la tensión de declarar add/remove en la interfaz: viola la segregación de interfaz pero uniformiza el trato de los elementos.
- Enumerar pros (polimorfismo, recursión, abierto/cerrado) y el contra (sobregeneralización de la interfaz).
- Distinguir Composite de Decorator y conocer sus relaciones con Builder, Chain of Responsibility, Iterator, Visitor, Flyweight y Prototype.
