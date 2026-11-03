# L: Principio de sustitución de Liskov (Liskov Substitution Principle) — Estudio

## Tarjetas de repaso

P: ¿Qué exige el principio de sustitución de Liskov? / R: Que puedas pasar objetos de las subclases en lugar de objetos de la clase padre sin descomponer el código cliente.

P: ¿Qué debe hacer una subclase al sobrescribir un método? / R: Extender el comportamiento base, no sustituirlo por algo totalmente distinto, para seguir siendo compatible con la superclase.

P: ¿Por qué es fundamental este principio al desarrollar bibliotecas y frameworks? / R: Porque otras personas usarán tus clases sin poder acceder ni cambiar su código.

P: ¿Quién definió el principio y cuándo? / R: Barbara Liskov, en 1987, en su trabajo *Data abstraction and hierarchy*.

P: ¿Qué requisito se aplica a los tipos de parámetros de un método sobrescrito? / R: Deben coincidir o ser más abstractos que los del método de la superclase.

P: ¿Qué requisito se aplica al tipo de retorno de un método sobrescrito? / R: Debe coincidir o ser un subtipo del retorno del método base; los requisitos del retorno son inversos a los de los parámetros.

P: ¿Qué regla rige las excepciones de un método de una subclase? / R: No debe arrojar tipos de excepciones que no espere el método base; deben coincidir o ser subtipos de las del método base.

P: ¿Por qué una excepción inesperada rompe al cliente? / R: Los bloques try-catch del cliente apuntan a las excepciones del método base, así que una excepción inesperada se cuela entre sus líneas defensivas y destroza la aplicación.

P: ¿Qué significa no fortalecer las condiciones previas? / R: La subclase no debe ampliar las exigencias del método base (p. ej., requerir un argumento positivo cuando el base acepta cualquier int), pues rompe al cliente que pasaba negativos.

P: ¿Qué significa no debilitar las condiciones posteriores? / R: La subclase no debe omitir lo que el base garantiza (p. ej., cerrar conexiones de base de datos), porque el cliente que lo espera puede dejar conexiones fantasma.

P: ¿Qué son los invariantes de una superclase y por qué importan? / R: Son las condiciones en que un objeto tiene sentido (p. ej., un gato con cuatro patas, cola y maullido); deben preservarse y es la regla más fácil de vulnerar.

P: ¿Cuál es la forma más segura de extender una clase? / R: Introducir nuevos campos y métodos sin tocar los miembros existentes de la superclase, aunque no siempre es posible en la vida real.

P: ¿Qué regla afecta a los campos privados de la superclase? / R: Una subclase no debe cambiar los valores de campos privados de la superclase.

P: ¿Cómo se resuelve la jerarquía de documentos que viola el principio? / R: Rediseñándola: el documento de solo lectura pasa a ser la clase base y el de escritura se convierte en subclase que añade el comportamiento de guardar.

## Preguntas de autoevaluación

1. ¿En qué se diferencia este principio de otros principios de diseño? / R: Incluye un grupo de requisitos formales para las subclases y sus métodos, en lugar de quedar abierto a la interpretación. (Lo que necesitas saber)

2. Si una clase tiene `alimentar(Gato c)`, ¿por qué sobrescribirlo como `alimentar(GatoDeBengala c)` es incorrecto y como `alimentar(Animal c)` es correcto? / R: Restringirlo a GatoDeBengala descompone la funcionalidad porque no sirve a los gatos genéricos que pasa el cliente; aceptar Animal funciona porque alimenta a cualquier animal, incluidos todos los gatos. (Requisitos formales para las subclases)

3. Si una clase tiene `comprarGato(): Gato`, ¿por qué devolver `Animal` es incorrecto y devolver `GatoDeBengala` es correcto? / R: Devolver Animal da al cliente un animal genérico desconocido que no encaja con la estructura diseñada para un gato; devolver GatoDeBengala sigue siendo un gato. (Requisitos formales para las subclases)

4. ¿Qué ocurre en lenguajes de tipado estático modernos como Java o C# respecto a las reglas de excepciones? / R: Estas reglas vienen integradas y no permiten compilar un programa que las viole. (Requisitos formales para las subclases, PDF p. 65)

5. ¿Por qué el método `guardar` rompe el principio en la versión ANTES de la jerarquía de documentos? / R: `DocumentosDeSoloLectura` sobrescribe `guardar` para arrojar una excepción; como el método base no tiene esa restricción, el cliente se descompone si no comprueba el tipo antes de guardar. (El ejemplo que recorre el capítulo)

6. ¿Qué otro principio se ve arrastrado al violar el de sustitución en el ejemplo de documentos? / R: El principio de abierto/cerrado, porque el cliente se vuelve dependiente de las clases concretas y cada nueva subclase obliga a cambiar su código. (El ejemplo que recorre el capítulo / Ideas clave)

7. ¿Por qué los invariantes son la regla más fácil de vulnerar? / R: Porque quizá no conozcas todos los invariantes de una clase compleja, y pueden estar implícitos en pruebas de unidad y expectativas del cliente. (Requisitos formales para las subclases)

8. En lenguajes de tipado dinámico, ¿qué ejemplo negativo de retorno se menciona? / R: El método base devuelve una cadena pero el sobrescrito devuelve un número. (Requisitos formales para las subclases)

## Puntos a dominar

- Sustituir objetos de la superclase por objetos de la subclase sin romper el código cliente.
- Al sobrescribir, extender el comportamiento base en lugar de reemplazarlo.
- Parámetros iguales o más abstractos; retorno igual o subtipo (requisitos inversos).
- Excepciones de la subclase iguales o subtipos de las del método base.
- No fortalecer las condiciones previas ni debilitar las posteriores.
- Preservar los invariantes de la superclase.
- No cambiar los valores de campos privados de la superclase.
- Reconocer que violar este principio suele arrastrar violaciones de abierto/cerrado, y que rediseñar la jerarquía puede resolver ambos.
