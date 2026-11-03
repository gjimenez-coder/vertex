# Dive Into Design Patterns — Alexander Shvets (Refactoring.Guru, 2021)
## Capítulo 1 — Conceptos básicos de POO (Basics of OOP)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF (páginas 9-13) y las citas usan la página del PDF.

## Lo que necesitas saber

Este primer capítulo establece el vocabulario mínimo de la programación orientada a objetos (POO) que el libro usará más adelante. La POO se presenta como un paradigma basado en envolver bloques de información y su comportamiento relacionado en unidades especiales llamadas objetos, que se construyen a partir de un conjunto de "planos" definidos por el programador, llamados clases.

El autor explica estos conceptos con ejemplos de gatos para que la lectura sea cercana, como una conversación entre amigos. Aclara una convención importante: aunque los diagramas y el código estén en inglés (como lo estarían en un proyecto real), en el texto puede referirse a las clases con sus nombres en español (por ejemplo, la clase Gato) para no interrumpir la lectura con palabras extrañas.

Al terminar el capítulo sales sabiendo distinguir objeto de clase, identificar los miembros de una clase (campos y métodos), diferenciar estado y comportamiento, y entender cómo las clases se organizan en jerarquías mediante herencia, con superclases y subclases.

## El ejemplo que recorre el capítulo

El hilo conductor es un conjunto de mascotas. Óscar es un gato concreto; Luna, la gata de un amigo, es otro gato; Fido es el perro de un vecino. A partir de lo que gatos y perros tienen en común se construye una jerarquía que culmina en organismos vivos, lo que permite ilustrar instancias, clases, herencia y jerarquías con un solo caso.

## Objetos, clases

Óscar es un objeto: una instancia de la clase Gato. Cada gato tiene atributos estándar —nombre, sexo, edad, peso, color, comida favorita, etc.—; estos son los campos de la clase.

Todos los gatos se comportan de forma similar: respiran, comen, corren, duermen y maúllan. Estos son los métodos de la clase. Colectivamente, los campos y los métodos se denominan los miembros de la clase.

El libro introduce dos términos clave:

- Estado: la información almacenada dentro de los campos del objeto.
- Comportamiento: lo que definen todos los métodos del objeto.

Los objetos son instancias de clases. Luna también es una instancia de la clase Gato y tiene el mismo grupo de atributos que Óscar; la diferencia está en los valores de esos atributos: su sexo es hembra, tiene un color diferente y pesa menos. Por lo tanto, una clase es como un plano que define la estructura de los objetos, que son instancias concretas de esa clase.

## Jerarquías de clase

Un programa real contiene más de una clase, y algunas de ellas pueden organizarse en jerarquías de clase.

Perros y gatos tienen mucho en común: nombre, sexo, edad y color son atributos tanto de perros como de gatos; ambos pueden respirar, dormir y correr. Por eso puede definirse una clase base Animal que enumere los atributos y comportamientos comunes.

El capítulo fija la terminología de la herencia:

- Superclase: la clase padre, como Animal.
- Subclases: sus hijas, como Gato y Perro.

Las subclases heredan el estado y el comportamiento de su padre y se limitan a definir atributos o comportamientos que son diferentes. Así, la clase Gato contendrá el método maullar y la clase Perro, el método ladrar.

La jerarquía puede extenderse hacia arriba: se puede extraer una clase más genérica, Organismo vivo, que se convierte en superclase de Animal y Planta. Esa pirámide de clases es una jerarquía. En ella, la clase Gato lo hereda todo de las clases Animal y Organismo.

Las subclases pueden sobrescribir el comportamiento de los métodos que heredan de las clases padre: pueden sustituir completamente el comportamiento por defecto o limitarse a mejorarlo con material adicional.

## Notas sobre UML

El libro usa diagramas de clases en UML a lo largo del texto. Dos observaciones del autor:

- Los nombres de las cosas en los diagramas están en inglés, como estarían en código real; los comentarios y notas pueden estar en español.
- En un diagrama UML las clases se pueden simplificar cuando es más importante mostrar sus relaciones que sus contenidos.

## Ideas clave

- La POO envuelve información y comportamiento en objetos, construidos a partir de clases ("planos").
- Un objeto es una instancia concreta de una clase; distintos objetos de la misma clase comparten atributos pero con valores propios.
- Los campos y los métodos son los miembros de una clase.
- El estado son los valores de los campos; el comportamiento es lo que definen los métodos.
- Las clases se organizan en jerarquías mediante herencia: superclase (padre) y subclases (hijas).
- Las subclases heredan estado y comportamiento y definen solo lo que es diferente (p. ej., maullar vs. ladrar).
- Una jerarquía puede generalizarse hacia arriba (Organismo → Animal/Planta); una subclase hereda de toda la cadena de ancestros.
- Las subclases pueden sobrescribir métodos heredados: sustituir el comportamiento por defecto o ampliarlo.
