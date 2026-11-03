# Dive Into Design Patterns — Alexander Shvets (Refactoring.Guru, 2021)
## Capítulo 32 — State (Estado)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF (con palabras pegadas por la justificación) y las citas usan la página del PDF.

## Lo que necesitas saber

State es un patrón de diseño de comportamiento que permite a un objeto alterar su comportamiento cuando su estado interno cambia, de modo que parece como si el objeto cambiara su clase (PDF p. 375). Está estrechamente ligado al concepto de máquina de estados finitos: en cualquier momento el programa se encuentra en un número finito de estados, dentro de cada estado se comporta de forma diferente y puede pasar de uno a otro mediante transiciones también finitas y predeterminadas.

La idea central del patrón es extraer todo el comportamiento específico de cada estado a clases separadas. En lugar de que un único objeto contenga enormes condicionales, ese objeto (el contexto) guarda una referencia a un objeto de estado y le delega el trabajo relacionado con el estado. Sales sabiendo cuándo conviene este patrón, cómo se estructura (contexto, interfaz Estado y estados concretos), cómo se realizan las transiciones y cómo se diferencia de Strategy.

## El ejemplo que recorre el capítulo

El hilo conductor es una clase `Documento` que puede estar en tres estados: Borrador, Moderación y Publicado. El método `publicar` se comporta distinto en cada uno (PDF p. 377):

- En Borrador, mueve el documento a moderación.
- En Moderación, hace público el documento, pero sólo si el usuario actual es un administrador.
- En Publicado, no hace nada en absoluto.

El pseudocódigo final usa un reproductor de audio como contexto, mostrando los mismos controles comportándose distinto según el estado de reproducción.

## Problema

Las máquinas de estado suelen implementarse con muchos operadores condicionales (`if` o `switch`) que seleccionan el comportamiento según el estado actual, que normalmente es un grupo de valores de los campos del objeto. La mayor debilidad de este enfoque aparece al añadir más estados y comportamientos a la clase `Documento`: la mayoría de los métodos contendrán condicionales monstruosos. Un código así es muy difícil de mantener, porque cualquier cambio en la lógica de transición puede requerir modificar los condicionales de estado de cada método. El problema empeora con la evolución del proyecto, ya que es difícil predecir todos los estados y transiciones en la etapa de diseño.

## Solución

El patrón State sugiere crear nuevas clases para todos los estados posibles de un objeto y extraer a esas clases todos los comportamientos específicos del estado. El objeto original, llamado contexto, almacena una referencia a uno de los objetos de estado que representa su estado actual y le delega todo el trabajo relacionado con el estado. Para la transición, el contexto sustituye el objeto de estado activo por otro que represente el nuevo estado; esto sólo es posible si todas las clases de estado siguen la misma interfaz y el contexto trabaja con ellas a través de dicha interfaz.

La estructura recuerda a Strategy, pero hay una diferencia clave: en State los estados particulares pueden conocerse entre sí e iniciar transiciones de uno a otro, mientras que las estrategias casi nunca se conocen.

## Analogía en el mundo real

Los botones de un smartphone se comportan de forma diferente según el estado del dispositivo: desbloqueado ejecutan varias funciones, bloqueado un botón desbloquea la pantalla, y con batería baja un botón muestra la pantalla de carga (PDF p. 381).

## Estructura

1. La clase **Contexto** almacena una referencia a un objeto de estado concreto y le delega el trabajo específico del estado; se comunica con él a través de la interfaz de estado y expone un setter para pasarle un nuevo estado.
2. La interfaz **Estado** declara los métodos específicos del estado. Estos métodos deben tener sentido para todos los estados concretos, para evitar métodos inútiles que nunca se invoquen.
3. Los **Estados Concretos** proporcionan sus propias implementaciones. Para evitar duplicación se pueden incluir clases abstractas intermedias con el comportamiento común. Los estados pueden guardar una referencia inversa al contexto para extraer información o iniciar transiciones.
4. Tanto el contexto como el estado concreto pueden establecer el nuevo estado y realizar la transición sustituyendo el objeto de estado vinculado al contexto.

## Pseudocódigo

El ejemplo usa un `AudioPlayer` como contexto que mantiene un campo `state` y delega las entradas del usuario (`clickLock`, `clickPlay`, `clickNext`, `clickPrevious`) al estado activo. La clase abstracta `State` guarda una referencia inversa al reproductor. Los estados concretos `LockedState`, `ReadyState` y `PlayingState` implementan los comportamientos y disparan transiciones llamando a `player.changeState(...)`. Por ejemplo, en `ReadyState` el `clickPlay` inicia la reproducción y pasa a `PlayingState`; en `LockedState` las acciones de reproducción no hacen nada.

## Aplicabilidad

- Cuando tengas un objeto que se comporta distinto según su estado actual, el número de estados sea enorme y el código específico del estado cambie con frecuencia.
- Cuando una clase esté contaminada con enormes condicionales que alteran su comportamiento según los valores de sus campos; el patrón permite extraer esas ramas a métodos de las clases de estado.
- Cuando tengas mucho código duplicado entre estados y transiciones similares; se componen jerarquías de clases de estado y se reduce la duplicación con clases abstractas base.

## Cómo implementarlo

1. Decide qué clase actuará como contexto.
2. Declara la interfaz de estado, centrándote en los métodos con comportamiento específico del estado.
3. Para cada estado crea una clase derivada de la interfaz y extrae a ella el código relacionado con ese estado (puede requerir hacer públicos campos/métodos, invocar métodos públicos del contexto, o anidar las clases de estado).
4. En el contexto añade un campo de referencia del tipo de la interfaz de estado y un setter público.
5. Sustituye los condicionales de estado del contexto por llamadas a los métodos del objeto de estado.
6. Para cambiar el estado, instancia una clase de estado y pásala al contexto (desde el propio contexto, desde otros estados o desde el cliente).

## Pros y contras

- Principio de responsabilidad única: organiza el código de cada estado en clases separadas.
- Principio de abierto/cerrado: introduce nuevos estados sin cambiar los estados existentes ni el contexto.
- Simplifica el código del contexto eliminando condicionales voluminosos.
- Puede ser excesivo si la máquina de estados tiene pocos estados o cambia raramente.

## Relaciones con otros patrones

- Bridge, State, Strategy y, hasta cierto punto, Adapter tienen estructuras muy similares y se basan en la composición (delegar trabajo a otros objetos), pero resuelven problemas diferentes.
- State puede considerarse una extensión de Strategy. Ambos delegan parte del trabajo a objetos ayudantes, pero Strategy los hace completamente independientes, mientras que State no restringe las dependencias entre estados concretos, permitiéndoles alterar el estado del contexto a voluntad.

## Ideas clave

- State permite que un objeto cambie su comportamiento al cambiar su estado interno, como si cambiara de clase.
- Se basa en el concepto de máquina de estados finitos: estados y transiciones finitos y predeterminados.
- Sustituye condicionales monstruosos por clases de estado que encapsulan el comportamiento específico.
- El contexto delega en un objeto de estado y realiza transiciones sustituyendo ese objeto.
- Todos los estados comparten una misma interfaz; pueden guardar referencia inversa al contexto.
- A diferencia de Strategy, los estados pueden conocerse entre sí e iniciar transiciones.
- Favorece los principios de responsabilidad única y abierto/cerrado.
- Puede ser excesivo con pocos estados o cambios poco frecuentes.
