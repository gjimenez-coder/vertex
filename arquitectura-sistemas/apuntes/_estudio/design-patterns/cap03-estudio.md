# Relaciones entre objetos — Estudio

## Tarjetas de repaso

P: ¿Cuál es la relación más básica y débil entre clases? / R: La dependencia.

P: ¿Cuándo existe una dependencia entre dos clases? / R: Cuando ciertos cambios en la definición de una clase pueden provocar modificaciones en otra; suele surgir al usar nombres de clases concretas (tipos en firmas de métodos, instanciación por constructor, etc.).

P: ¿Cómo se debilita una dependencia? / R: Haciendo que el código dependa de interfaces o clases abstractas en lugar de clases concretas.

P: ¿Qué es una asociación? / R: Una relación en la que un objeto utiliza o interactúa con otro, con un vínculo permanente: el objeto siempre tiene acceso a los objetos con los que interactúa.

P: ¿Qué diferencia a la asociación de la dependencia simple? / R: La asociación establece un vínculo permanente (el objeto siempre tiene acceso al otro), mientras que la dependencia simple no establece ese acceso permanente.

P: ¿Cómo se representa una asociación en UML? / R: Con una flecha simple desde un objeto apuntando al que utiliza; si es bidireccional, lleva una punta en cada extremo.

P: ¿Puede una misma clase ser dependencia y asociación a la vez? / R: Sí; por ejemplo, una clase usada como argumento puntual es dependencia, y si además es un campo siempre accesible pasa a ser también asociación.

P: ¿Qué es la agregación? / R: Una asociación especializada que representa relaciones "uno a muchos", "muchos a muchos" o "todo a parte"; un objeto "tiene" un grupo de otros y actúa como contenedor o colección.

P: En la agregación, ¿puede el componente existir sin el contenedor? / R: Sí; el componente puede existir sin el contenedor y vincularse a varios contenedores a la vez.

P: ¿Qué es la composición? / R: Una agregación específica en la que un objeto se compone de otras instancias y el componente solo puede existir como parte del contenedor.

P: ¿Cómo se distinguen agregación y composición en UML? / R: Diamante vacío en el lado del contenedor = agregación; diamante relleno en la base de la flecha = composición.

P: ¿Cuál es la diferencia clave entre agregación y composición? / R: En la composición el contenedor gestiona el ciclo de vida del componente, que no existe sin él; en la agregación el componente existe de forma independiente.

P: ¿Cuál es el orden de las seis relaciones de más débil a más fuerte? / R: Dependencia → asociación → agregación → composición → implementación → herencia.

P: ¿Qué establece la relación de implementación? / R: La clase A define métodos declarados en la interfaz B; los objetos A pueden tratarse como B y la clase A depende de B.

P: ¿Qué aporta la herencia frente a la implementación? / R: La clase A hereda la interfaz y la implementación de B y puede extenderla; el objeto A puede tratarse como B.

## Preguntas de autoevaluación

P: ¿Por qué UML no muestra todas las dependencias de un código? / R: Porque hay demasiadas en cualquier código real; conviene ser selectivo y mostrar solo las importantes para lo que se quiere comunicar. (Sección: Dependencia)

P: En el ejemplo de la clase `Professor`, ¿por qué `Course` es una dependencia pero no una asociación, y `Student` sí es ambas? / R: `Course` se usa como argumento puntual del método `teach` (si cambia `getKnowledge` el código se rompe), pero no queda accesible de forma permanente; `Student` es un campo siempre accesible para cualquier método de `Professor`, por lo que además de dependencia es asociación. (Sección: Ejemplo combinado: dependencia y asociación)

P: ¿Qué diferencia a la agregación de la asociación simple? / R: La asociación simple describe relaciones entre un par de objetos, mientras que la agregación representa relaciones "uno a muchos", "muchos a muchos" o "todo a parte" entre múltiples objetos, con un objeto que actúa como contenedor. (Sección: Agregación)

P: ¿Qué significa que UML modela relaciones entre clases y no entre objetos individuales? / R: Un objeto universidad puede constar de varios departamentos aunque el diagrama muestre un solo "bloque" por entidad; además las cardinalidades pueden omitirse si el contexto las deja claras. (Sección: Agregación)

P: ¿Por qué el texto advierte sobre el uso del término "composición"? / R: Porque muchas personas dicen "composición" cuando se refieren tanto a agregación como a composición; el caso notorio es "escoge composición antes que herencia", donde "composición" suena más natural en inglés sin ignorar la diferencia. (Sección: Composición)

P: ¿Qué relación añade la gestión del ciclo de vida del componente? / R: La composición: el objeto A conoce a B, consiste en B y gestiona su ciclo vital, de modo que B no existe sin A. (Sección: La visión global)

P: ¿Cuál es la tesis central que ordena todas estas relaciones? / R: Que las relaciones pueden ordenarse de la más débil a la más fuerte según el grado de acoplamiento y responsabilidad que establecen entre las clases. (Sección: Lo que necesitas saber)

## Puntos a dominar

- Definir cada una de las seis relaciones: dependencia, asociación, agregación, composición, implementación y herencia.
- Ordenar las seis relaciones de más débil a más fuerte según acoplamiento.
- Distinguir dependencia de asociación por la existencia de un vínculo permanente (campo accesible).
- Reconocer cuándo una misma clase es a la vez dependencia y asociación según su uso (argumento puntual vs. campo).
- Diferenciar agregación y composición por el control del ciclo de vida y la independencia del componente.
- Identificar la notación UML: flecha simple (asociación), diamante vacío (agregación), diamante relleno (composición).
- Recordar que las dependencias se debilitan dependiendo de interfaces o clases abstractas.
- Entender que UML modela relaciones entre clases y puede omitir cardinalidades claras por contexto.
