# Conceptos básicos de POO (Basics of OOP) — Estudio

## Tarjetas de repaso

P: ¿Qué es la POO según el capítulo? / R: Un paradigma basado en envolver bloques de información y su comportamiento relacionado en unidades especiales llamadas objetos, construidos a partir de planos llamados clases.

P: ¿Qué es un objeto? / R: Una instancia concreta de una clase; por ejemplo, Óscar es un objeto de la clase Gato.

P: ¿Qué es una clase? / R: Un plano que define la estructura de los objetos, los cuales son instancias concretas de esa clase.

P: ¿Qué son los campos de una clase? / R: Los atributos estándar de los objetos, como nombre, sexo, edad, peso, color y comida favorita.

P: ¿Qué son los métodos de una clase? / R: El comportamiento común de los objetos, como respirar, comer, correr, dormir y maullar.

P: ¿Qué son los miembros de una clase? / R: Colectivamente, los campos y los métodos de la clase.

P: ¿Qué es el estado de un objeto? / R: La información almacenada dentro de los campos del objeto.

P: ¿Qué es el comportamiento de un objeto? / R: Lo que definen todos los métodos del objeto.

P: Si Óscar y Luna son de la clase Gato, ¿en qué se diferencian? / R: Comparten el mismo grupo de atributos, pero difieren en los valores (Luna es hembra, otro color y pesa menos).

P: ¿Qué es una superclase? / R: La clase padre de una jerarquía, como Animal respecto de Gato y Perro.

P: ¿Qué son las subclases? / R: Las clases hijas, como Gato y Perro, que heredan estado y comportamiento de su padre y definen solo lo diferente.

P: ¿Qué es una jerarquía de clases? / R: La organización piramidal de clases mediante herencia; por ejemplo, Organismo vivo → Animal/Planta, donde Gato hereda de Animal y de Organismo.

P: ¿Qué pueden hacer las subclases con los métodos heredados? / R: Sobrescribirlos: sustituir completamente el comportamiento por defecto o limitarse a ampliarlo con material adicional.

P: ¿Por qué la clase Gato tiene maullar y la clase Perro ladrar? / R: Porque las subclases heredan lo común de Animal y solo definen los atributos o comportamientos que son diferentes.

## Preguntas de autoevaluación

P: ¿Cuál es la diferencia entre objeto y clase? / R: La clase es el plano que define la estructura; el objeto es una instancia concreta de esa clase (sección "Objetos, clases").

P: ¿Por qué se puede definir una clase base Animal a partir de perros y gatos? / R: Porque comparten atributos (nombre, sexo, edad, color) y comportamientos (respirar, dormir, correr), que se enumeran en la clase base (sección "Jerarquías de clase").

P: ¿Qué hereda la clase Gato en la jerarquía completa? / R: Lo hereda todo de las clases Animal y Organismo vivo, al extenderse la jerarquía hacia arriba (sección "Jerarquías de clase").

P: ¿Cómo se relacionan campos y métodos con estado y comportamiento? / R: El estado son los valores almacenados en los campos y el comportamiento es lo que definen los métodos; juntos, campos y métodos son los miembros (sección "Objetos, clases").

P: ¿Qué convención de idioma usa el autor para nombrar clases? / R: En diagramas y código los nombres van en inglés como en un proyecto real, pero en el texto puede referirse a las clases con nombres en español (p. ej., la clase Gato) (sección "Lo que necesitas saber" y "Notas sobre UML").

P: ¿Cuándo se simplifican las clases en un diagrama UML? / R: Cuando es más importante mostrar sus relaciones que sus contenidos (sección "Notas sobre UML").

P: ¿Qué ejemplo recorre todo el capítulo y para qué sirve? / R: Un conjunto de mascotas (Óscar, Luna, Fido) que, por lo que gatos y perros tienen en común, construye una jerarquía hasta organismos vivos, ilustrando instancias, clases, herencia y jerarquías (sección "El ejemplo que recorre el capítulo").

## Puntos a dominar

- Distinguir objeto (instancia) de clase (plano).
- Identificar los miembros de una clase: campos y métodos.
- Diferenciar estado (valores de los campos) de comportamiento (lo que definen los métodos).
- Explicar la herencia con superclase (padre) y subclases (hijas).
- Comprender cómo una jerarquía se generaliza hacia arriba (Organismo → Animal/Planta) y que una subclase hereda de toda la cadena.
- Reconocer la sobrescritura de métodos: sustituir o ampliar el comportamiento heredado.
- Recordar las convenciones de idioma y de simplificación en diagramas UML del libro.
