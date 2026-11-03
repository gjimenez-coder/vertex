# Moving Features Between Objects (Mover características entre objetos) — Estudio

## Tarjetas de repaso

P: ¿Cuál es la tesis central del capítulo sobre dónde poner las responsabilidades? / R: No hace falta acertar a la primera; el refactoring permite cambiar de opinión y mover el comportamiento cuando una decisión que era razonable deja de serlo.

P: ¿Cuáles son las dos refactorizaciones básicas para reubicar características y en qué orden conviene usarlas? / R: Move Method y Move Field; si hay que usar ambas, se mueve primero el campo y luego el método.

P: ¿Cuál es el síntoma que justifica aplicar Move Method? / R: Un método usa o es usado por más características de otra clase que de aquella en la que está definido (clases con demasiado comportamiento o demasiado acopladas).

P: Cuando un método movido necesita una característica de la clase origen, ¿qué cuatro opciones hay? / R: Moverla también al destino, crear/usar una referencia del destino al origen, pasar el objeto origen como parámetro, o (si es una variable) pasarla como parámetro.

P: ¿Cuál es el síntoma de Move Field? / R: Un campo lo usa otra clase más que la clase en la que está definido, uso que puede ser indirecto vía getters/setters, y los métodos tienen sentido donde están.

P: ¿Por qué Fowler insiste en eliminar el campo o método en la clase origen? / R: Para que el compilador detecte los métodos o referencias que no se han redirigido.

P: ¿Qué es Extract Class y cuál es su buena señal de aplicación? / R: Dividir una clase que hace el trabajo de dos; la buena señal es un subconjunto de datos y métodos que van juntos o cambian juntos.

P: Al exponer una clase extraída, ¿qué opciones hay para gestionar el aliasing? / R: Aceptarla como objeto de referencia (Change Value to Reference), hacerla inmutable o dar una interfaz inmutable, o clonarla al pasarla.

P: ¿Qué relación tienen Extract Class e Inline Class? / R: Son inversos: Extract Class divide una clase sobrecargada e Inline Class funde una clase que ya no aporta valor en otra.

P: ¿Qué problema resuelve Hide Delegate y cómo? / R: Reduce el acoplamiento del cliente con el delegado colocando un método delegante simple en el servidor, de modo que los cambios se limiten al servidor.

P: ¿Cuál es el precio de Hide Delegate que motiva Remove Middle Man? / R: Cada nueva característica exige un nuevo método delegante en el servidor, hasta que este se vuelve solo un intermediario.

P: ¿Cuándo se usa Introduce Foreign Method y cuándo Introduce Local Extension? / R: El método foráneo para uno o dos métodos adicionales en una clase que no puedes modificar; la extensión local para más de uno o dos.

P: ¿Cómo se estructura un Introduce Foreign Method? / R: Se crea el método en la clase cliente con una instancia del servidor como primer argumento, sin acceder a características del cliente, comentándolo como "foreign method; should be in server".

P: Entre subclase y wrapper para una extensión local, ¿qué prefiere Fowler y cuál es el obstáculo? / R: Prefiere la subclase por ser menos trabajo; su obstáculo es que debe aplicarse en el momento de la creación del objeto.

## Preguntas de autoevaluación

P: ¿Por qué en el ejemplo de Move Method el campo `_daysOverdrawn` se queda en `Account` y se pasa como parámetro a `AccountType`? / R: Porque varía con cada cuenta, así que debe permanecer en la cuenta y pasarse como parámetro al método movido. (Sección: Move Method)

P: ¿Qué ventaja aporta la autoencapsulación (Self Encapsulate Field) al hacer Move Field? / R: Solo hay que redirigir los accesores, lo que permite dar un paso más pequeño y facilita un posterior Move Method. (Sección: Move Field)

P: Además de dividir responsabilidades, ¿qué beneficio ofrece Extract Class en programas concurrentes? / R: Mejora la "liveness" al permitir bloqueos separados. (Sección: Extract Class)

P: ¿Cuáles son los pasos clave de la mecánica de Inline Class? / R: Declarar el protocolo público de la origen en la clase absorbente delegando, redirigir todas las referencias a la absorbente, compilar y probar, y mover características con Move Method y Move Field hasta vaciar la origen. (Sección: Inline Class)

P: Según el capítulo, ¿por qué no importa demasiado acertar cuánto ocultar entre Hide Delegate y Remove Middle Man? / R: Porque se puede ajustar con el tiempo: "Refactoring means you never have to say you're sorry" (PDF p. 130). (Sección: Remove Middle Man)

P: ¿Qué problemas surgen al usar un wrapper como extensión local de la clase `Date` de Java? / R: Problemas con métodos que toman un original como argumento (p. ej. `after`) y con métodos del sistema como `equals`, que Java asume simétrico; por eso se expone el wrapping con un nuevo nombre, `equalsDate`. (Sección: Introduce Local Extension)

P: ¿Por qué no merece la pena factorizar un método foráneo que solo se usa una vez? / R: Porque solo tiene sentido extraerlo si se repite; la repetición es la raíz de todo mal del software. (Sección: Introduce Foreign Method)

## Puntos a dominar

- Reconocer que la ubicación de responsabilidades no se acierta a la primera y que el refactoring permite reubicarlas con seguridad (compilar y probar en cada paso).
- Distinguir los síntomas de Move Method (método más ligado a otra clase) y Move Field (campo más usado por otra clase) y recordar mover primero el campo.
- Eliminar el campo o método en origen para que el compilador detecte referencias no redirigidas.
- Aplicar Extract Class ante clases sobrecargadas e Inline Class cuando una clase ya no aporta valor, entendiéndolos como inversos.
- Gestionar el aliasing al exponer una clase extraída: referencia, inmutabilidad o clonación.
- Usar Hide Delegate para reducir acoplamiento y Remove Middle Man para revertir el exceso de delegación.
- Elegir entre Introduce Foreign Method (1–2 métodos) e Introduce Local Extension (más) cuando no puedes modificar la clase servidor.
- Preferir la subclase frente al wrapper salvo que la extensión deba aplicarse tras la creación de un objeto mutable.
