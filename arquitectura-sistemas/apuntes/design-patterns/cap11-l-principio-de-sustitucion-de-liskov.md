# Dive Into Design Patterns — Alexander Shvets (Refactoring.Guru, 2021)
## Capítulo 11 — L: Principio de sustitución de Liskov (Liskov Substitution Principle)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF (con palabras pegadas por la justificación) y las citas usan la página del PDF.

## Lo que necesitas saber

Al extender una clase, debes poder pasar objetos de las subclases en lugar de objetos de la clase padre sin descomponer el código cliente. Eso significa que la subclase debe permanecer compatible con el comportamiento de la superclase: al sobrescribir un método, hay que extender el comportamiento base en lugar de sustituirlo por algo totalmente distinto.

El principio de sustitución es un grupo de comprobaciones que ayudan a predecir si una subclase sigue siendo compatible con el código que funcionaba con objetos de la superclase. Es fundamental al desarrollar bibliotecas y frameworks, porque otras personas usarán tus clases sin poder acceder ni cambiar su código.

A diferencia de otros principios de diseño, muy abiertos a la interpretación, este principio incluye un grupo de requisitos formales para las subclases y, en concreto, para sus métodos. Debe su nombre a Barbara Liskov, que lo definió en 1987 en su trabajo *Data abstraction and hierarchy* (PDF p. 62).

## Requisitos formales para las subclases

**Los tipos de parámetros en el método de una subclase deben coincidir o ser más abstractos que los del método de la superclase.** Si una clase tiene `alimentar(Gato c)`:
- Bien: una subclase que sobrescribe el método como `alimentar(Animal c)` funciona, porque puede alimentar a cualquier animal, incluidos todos los gatos que pase el cliente.
- Mal: una subclase que restringe el método a `alimentar(GatoDeBengala c)` descompone la funcionalidad, porque no sirve a los gatos genéricos que pasa el cliente.

**El tipo de retorno debe coincidir o ser un subtipo del tipo de retorno del método de la superclase.** Los requisitos del retorno son inversos a los de los parámetros. Si una clase tiene `comprarGato(): Gato`:
- Bien: una subclase que devuelve `comprarGato(): GatoDeBengala`, porque sigue siendo un gato.
- Mal: una subclase que devuelve `comprarGato(): Animal`, porque el cliente recibe un animal genérico desconocido que no encaja con la estructura diseñada para un gato.

En lenguajes de tipado dinámico aparece otro ejemplo negativo: el método base devuelve una cadena, pero el sobrescrito devuelve un número.

**Un método de una subclase no debe arrojar tipos de excepciones que no se espere que arroje el método base.** Los tipos de excepciones deben coincidir o ser subtipos de los que el método base puede arrojar. Los bloques `try-catch` del código cliente se dirigen a las excepciones que probablemente arrojará el método base, así que una excepción inesperada puede colarse entre las líneas defensivas del cliente y destrozar la aplicación. En lenguajes modernos de tipado estático (Java, C#) estas reglas vienen integradas y no permiten compilar un programa que las viole (PDF p. 65).

**Una subclase no debe fortalecer las condiciones previas.** Si el método base acepta un `int` y la subclase exige que el argumento sea positivo (lanzando una excepción si es negativo), amplía las condiciones previas: el código cliente que funcionaba pasando números negativos se descompone.

**Una subclase no debe debilitar las condiciones posteriores.** Si un método de la clase debe cerrar siempre las conexiones de base de datos al devolver un valor y la subclase las deja abiertas para reutilizarlas, el cliente que espera que se cierren puede finalizar el programa dejando conexiones fantasma.

**Los invariantes de una superclase deben preservarse.** Los invariantes son las condiciones en las que un objeto tiene sentido (p. ej., un gato tiene cuatro patas, cola y capacidad de maullar). Pueden definirse explícitamente mediante contratos de interfaz o aserciones, pero también resultar implícitos por pruebas de unidad y expectativas del cliente. Es la regla más fácil de vulnerar, porque quizá no conozcas todos los invariantes de una clase compleja. La forma más segura de extender una clase es introducir nuevos campos y métodos sin tocar los miembros existentes de la superclase, aunque esto no siempre es posible en la vida real.

**Una subclase no debe cambiar los valores de campos privados de la superclase.** Algunos lenguajes permiten acceder a miembros privados mediante mecanismos reflexivos, y otros (Python, JavaScript) no tienen protección alguna para los miembros privados.

## El ejemplo que recorre el capítulo

Una jerarquía de clases de documento que viola el principio de sustitución (PDF p. 67-68).

**ANTES:** el método `guardar` no tiene sentido en un documento de solo lectura, así que la subclase `DocumentosDeSoloLectura` lo sobrescribe y arroja una excepción si alguien lo invoca. Como el método base no tiene esa restricción, el código cliente se descompone si no comprueba el tipo de documento antes de guardar. Además, esto viola el principio de abierto/cerrado, porque el cliente se vuelve dependiente de las clases concretas: cada nueva subclase obliga a cambiar el código cliente.

**DESPUÉS:** el problema se resuelve rediseñando la jerarquía. Como una subclase debe extender el comportamiento de la superclase, el documento de solo lectura pasa a ser la clase base; el documento de escritura se convierte en una subclase que extiende la base y añade el comportamiento de guardar.

## Ideas clave

- Debes poder sustituir objetos de la superclase por objetos de la subclase sin romper el código cliente.
- Al sobrescribir, extiende el comportamiento base; no lo sustituyas por algo distinto.
- Parámetros: iguales o más abstractos; retorno: igual o subtipo (requisitos inversos).
- Las excepciones de la subclase deben coincidir o ser subtipos de las del método base.
- No fortalezcas las condiciones previas ni debilites las posteriores.
- Preserva los invariantes de la superclase; es la regla más fácil de vulnerar.
- No cambies los campos privados de la superclase.
- Violar este principio suele arrastrar violaciones del principio de abierto/cerrado; rediseñar la jerarquía puede resolver ambos.
