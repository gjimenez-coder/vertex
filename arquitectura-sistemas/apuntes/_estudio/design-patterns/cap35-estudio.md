# Capítulo 35 — Visitor (Visitante) — Estudio

## Tarjetas de repaso

P: ¿Qué tipo de patrón de diseño es Visitor y qué permite hacer? / R: Es un patrón de comportamiento que permite separar los algoritmos de los objetos sobre los que operan, colocando el comportamiento en una clase visitante aparte.

P: ¿Dónde se coloca el nuevo comportamiento en Visitor y cómo recibe el objeto original? / R: En una clase visitante separada; el objeto original se pasa a uno de los métodos del visitante como argumento.

P: ¿Qué principio de diseño respeta Visitor al añadir operaciones? / R: El principio de abierto/cerrado: se añaden operaciones nuevas a una jerarquía de clases sin modificarlas.

P: ¿Qué es el Double Dispatch en el contexto de Visitor? / R: Delegar en el propio objeto la elección del método visitante adecuado, porque es él quien conoce su clase exacta.

P: ¿Por qué el polimorfismo simple no resuelve la elección del método visitante? / R: Porque los métodos visitantes tienen firmas distintas, así que el polimorfismo directo no sirve.

P: ¿Por qué la sobrecarga de métodos tampoco resuelve la selección del método? / R: Porque la clase exacta del nodo es desconocida de antemano, y el mecanismo recurre por defecto al método que toma la clase base.

P: ¿Cuáles son los cuatro elementos de la estructura de Visitor? / R: La interfaz Visitante, los visitantes concretos, la interfaz Elemento con el método `accept`, y los elementos concretos que redirigen la llamada.

P: ¿Qué hace el método `accept` de un elemento concreto? / R: Redirige la llamada al método visitante que coincide con la clase actual del elemento (por ejemplo, `City.accept` invoca `v.doForCity(this)`).

P: ¿Deben los métodos de la interfaz Visitante tener el mismo nombre? / R: Pueden compartir nombre si el lenguaje soporta sobrecarga, pero los tipos de sus parámetros deben ser diferentes.

P: ¿Qué conocimiento necesitan tener los visitantes sobre los elementos? / R: Los visitantes deben conocer todas las clases de elemento concreto; los elementos solo trabajan con visitantes a través de la interfaz visitante.

P: ¿Cuál es la principal desventaja de Visitor? / R: Hay que actualizar todos los visitantes cada vez que se añade o elimina una clase de la jerarquía de elementos.

P: ¿Qué otra limitación tienen los visitantes respecto a los elementos? / R: Pueden carecer del acceso necesario a los campos y métodos privados de los elementos.

P: ¿Cómo se relaciona Visitor con el patrón Command? / R: Visitor puede verse como una versión potente de Command: sus objetos ejecutan operaciones sobre varios objetos de distintas clases.

P: ¿Con qué patrón se combina Visitor para recorrer una estructura de datos compleja? / R: Con Iterator, para recorrer la estructura y ejecutar una operación sobre sus elementos aunque tengan clases distintas.

## Preguntas de autoevaluación

P: ¿Cuál era la tarea del equipo con el grafo geográfico y qué dos problemas tenía la idea inicial? / R: Exportar el grafo a formato XML. La idea de añadir un método de exportación a cada clase de nodo chocaba con que el arquitecto no permitía alterar clases en producción (riesgo de error) y con que la lógica de exportación no pertenecía a clases dedicadas a geodatos. (El ejemplo que recorre el capítulo / Problema)

P: ¿Por qué fue aceptable, según el autor, modificar las clases de nodo para añadir el método `accept`? / R: Porque el cambio es trivial y permite añadir más comportamientos sin volver a tocar esas clases; al extraer una interfaz común, los nodos existentes funcionan con cualquier visitante nuevo. (Solución)

P: ¿Cuándo conviene aplicar el patrón Visitor? / R: Cuando necesitas operar sobre todos los elementos de una estructura compleja (como un árbol), para limpiar la lógica de negocio de comportamientos auxiliares, y cuando un comportamiento solo tiene sentido en algunas clases de la jerarquía. (Aplicabilidad)

P: En el pseudocódigo, ¿cómo implementan las formas geométricas el método de aceptación? / R: Cada forma concreta (`Dot`, `Circle`, `Rectangle`, `CompoundShape`) implementa `accept(v: Visitor)` invocando el método visitante que coincide con su clase, por ejemplo `v.visitDot(this)`. (Pseudocódigo)

P: ¿Qué papel juega el cliente en el patrón Visitor? / R: Suele ser una colección u objeto complejo (como un árbol Composite); crea los visitantes y los pasa a los elementos mediante los métodos de aceptación, trabajando a través de una interfaz abstracta sin conocer las clases concretas. (Estructura / Cómo implementarlo)

P: ¿Cómo se maneja un comportamiento que solo aplica a algunas clases de la jerarquía? / R: Se extrae a un visitante que implementa solo los métodos de las clases relevantes y deja vacíos los demás. (Aplicabilidad)

P: ¿Qué dos opciones ofrece el capítulo si el visitante necesita miembros privados del elemento? / R: Hacer públicos esos miembros (violando la encapsulación) o anidar la clase visitante dentro de la clase elemento, si el lenguaje lo soporta. (Cómo implementarlo)

P: ¿Qué ilustra la analogía del agente de seguros? / R: Que el visitante ofrece comportamientos distintos según el tipo de objeto que visita: pólizas médicas a un edificio residencial, antirrobo a un banco, y contra incendios e inundaciones a una cafetería. (Analogía en el mundo real)

## Puntos a dominar

- Entender que Visitor separa algoritmos de los objetos sobre los que operan, respetando el principio de abierto/cerrado.
- Explicar el Double Dispatch y por qué ni el polimorfismo simple ni la sobrecarga resuelven la selección del método visitante.
- Reconocer los cuatro componentes de la estructura: interfaz Visitante, visitantes concretos, interfaz Elemento con `accept` y elementos concretos.
- Saber que el método `accept` de cada elemento concreto redirige la llamada al método visitante que coincide con su clase.
- Identificar cuándo aplicar el patrón: estructuras complejas (árboles, Composite), limpieza de lógica auxiliar y comportamientos específicos de ciertas clases.
- Tener presente el principal compromiso: actualizar todos los visitantes ante cada cambio en la jerarquía de elementos, y la posible falta de acceso a miembros privados.
- Relacionar Visitor con Command, Composite e Iterator según describe el capítulo.
