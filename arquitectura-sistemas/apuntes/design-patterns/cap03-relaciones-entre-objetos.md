# Dive Into Design Patterns — Alexander Shvets (Refactoring.Guru, 2021)
## Capítulo 3 — Relaciones entre objetos (Relaciones entre objetos)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF (con palabras pegadas por la justificación) y las citas usan la página del PDF.

## Lo que necesitas saber

El capítulo completa el panorama de relaciones entre objetos y clases en la POO. Más allá de la herencia y la implementación, ya tratadas, existen otros vínculos que conviene distinguir: dependencia, asociación, agregación y composición. La tesis central es que todas estas relaciones pueden ordenarse de la más débil a la más fuerte según el grado de acoplamiento y responsabilidad que establecen entre las clases implicadas.

Sales sabiendo definir cada relación, reconocer cómo se representa en UML y, sobre todo, entender las diferencias finas: cuándo una dependencia es además una asociación, y cómo la composición se diferencia de la agregación por el control del ciclo de vida. El capítulo cierra con una "visión global" que resume las seis relaciones en una sola escala.

## El ejemplo que recorre el capítulo

Un contexto académico sirve de hilo conductor en los diagramas UML: un `Profesor` que depende de los materiales del curso (dependencia), que se comunica con los estudiantes (asociación), departamentos que contienen profesores (agregación) y una universidad que consta de departamentos (composición). El ejemplo de código de la clase `Profesor` reúne dependencia y asociación en un mismo caso.

## Dependencia

Es la relación más básica y débil entre clases. Existe una dependencia cuando ciertos cambios en la definición de una clase pueden provocar modificaciones en otra. Ocurre normalmente al usar nombres de clases concretas en el código: al especificar tipos en las firmas de un método, al instanciar objetos mediante llamadas al constructor, etc.

Se puede debilitar haciendo que el código dependa de interfaces o clases abstractas en lugar de clases concretas. En UML no se muestran todas las dependencias —hay demasiadas en cualquier código real—; conviene ser selectivo y mostrar solo las importantes para lo que se quiere comunicar.

## Asociación

Es una relación en la que un objeto utiliza o interactúa con otro. En UML se muestra con una flecha simple desde un objeto apuntando al objeto que utiliza; una asociación bidireccional es normal y lleva una punta en cada extremo. Puede verse como una dependencia especializada: un objeto siempre tiene acceso a los objetos con los que interactúa, mientras que la dependencia simple no establece un vínculo permanente.

En general se usa para representar un campo en una clase: el vínculo siempre está ahí. Pero no tiene que ser un campo; desde una perspectiva de interfaz puede indicar la presencia de un método que devuelve el objeto relacionado.

### Ejemplo combinado: dependencia y asociación

```
class Professor is
    field Student student
    // ...
    method teach(Course c) is
        // ...
        this.student.remember(c.getKnowledge())
```

El método `teach` toma un argumento de la clase `Course` que se usa en el cuerpo: si cambia `getKnowledge` (nombre o parámetros), el código se descompone. Eso es dependencia. El campo `student` también hace a `Student` una dependencia —si cambia `remember`, `Professor` se rompe—, pero como `student` siempre está accesible para cualquier método de `Professor`, `Student` es además una asociación.

## Agregación

Es una asociación especializada que representa relaciones "uno a muchos", "muchos a muchos" o "todo a parte" entre múltiples objetos, frente a la asociación simple que describe relaciones entre un par de objetos. Un objeto "tiene" un grupo de otros y actúa como contenedor o colección. El componente puede existir sin el contenedor y vincularse a varios contenedores a la vez. En UML se muestra con una línea con un diamante vacío en el lado del contenedor y una flecha apuntando hacia el componente.

UML representa relaciones entre clases: un objeto universidad puede constar de varios departamentos aunque el diagrama muestre un solo "bloque" por entidad. La notación puede indicar cantidades en ambos lados, pero pueden omitirse si el contexto las deja claras.

## Composición

Es una agregación específica en la que un objeto se compone de una o más instancias del otro. La diferencia está en que el componente solo puede existir como parte del contenedor. En UML se representa igual que la agregación pero con un diamante relleno en la base de la flecha.

El texto advierte que muchas personas usan "composición" cuando en realidad se refieren tanto a la agregación como a la composición. El caso más notorio es el principio "escoge composición antes que herencia": no es que se ignore la diferencia, sino que "composición" suena más natural en inglés.

## La visión global

Las seis relaciones, ordenadas de la más débil a la más fuerte (PDF p. 27):

- Dependencia: la clase A puede verse afectada por cambios en la clase B.
- Asociación: el objeto A conoce al objeto B. La clase A depende de B.
- Agregación: el objeto A conoce al objeto B y consiste en B. La clase A depende de B.
- Composición: el objeto A conoce al objeto B, consiste en B y gestiona el ciclo vital de B. La clase A depende de B.
- Implementación: la clase A define métodos declarados en la interfaz B. Los objetos A pueden tratarse como B. La clase A depende de B.
- Herencia: la clase A hereda la interfaz y la implementación de la clase B, pero puede extenderla. El objeto A puede tratarse como B. La clase A depende de B.

## Ideas clave

- La dependencia es la relación más débil; surge al usar clases concretas y se debilita dependiendo de interfaces o clases abstractas.
- La asociación añade a la dependencia un vínculo permanente: el objeto siempre tiene acceso al otro (normalmente un campo).
- Una misma clase puede ser a la vez dependencia y asociación, según se use como argumento puntual o como campo accesible.
- La agregación es una asociación "todo a parte" donde el componente existe de forma independiente y puede pertenecer a varios contenedores.
- La composición es una agregación donde el contenedor gestiona el ciclo de vida del componente, que no existe sin él.
- En UML: diamante vacío = agregación; diamante relleno = composición.
- UML modela relaciones entre clases, no entre objetos individuales, y puede omitir cardinalidades claras por contexto.
- Las seis relaciones forman una escala creciente de acoplamiento: dependencia → asociación → agregación → composición → implementación → herencia.
