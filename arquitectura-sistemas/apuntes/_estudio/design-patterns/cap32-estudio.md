# State (Estado) — Estudio

## Tarjetas de repaso

P: ¿Qué permite el patrón State?
R: Permite a un objeto alterar su comportamiento cuando su estado interno cambia, de modo que parece como si el objeto cambiara su clase.

P: ¿A qué tipo de patrón de diseño pertenece State?
R: Es un patrón de diseño de comportamiento.

P: ¿Con qué concepto está estrechamente ligado State?
R: Con la máquina de estados finitos: el programa está en un número finito de estados, se comporta distinto en cada uno y pasa de uno a otro mediante transiciones finitas y predeterminadas.

P: ¿Cuál es la idea central del patrón State?
R: Extraer todo el comportamiento específico de cada estado a clases separadas; el contexto guarda una referencia a un objeto de estado y le delega el trabajo.

P: ¿Qué problema aborda State?
R: Las máquinas de estado implementadas con muchos condicionales (if/switch) se vuelven inmantenibles: al añadir estados los métodos se llenan de condicionales monstruosos.

P: ¿Qué es el contexto en el patrón State?
R: El objeto original que almacena una referencia a un objeto de estado concreto y le delega todo el trabajo relacionado con el estado, comunicándose a través de la interfaz de estado.

P: ¿Qué declara la interfaz Estado?
R: Los métodos específicos del estado, que deben tener sentido para todos los estados concretos para evitar métodos inútiles que nunca se invoquen.

P: ¿Cómo se realiza una transición de estado?
R: El contexto sustituye el objeto de estado activo por otro que represente el nuevo estado; sólo es posible si todas las clases de estado siguen la misma interfaz.

P: ¿Para qué sirve la referencia inversa al contexto en los estados concretos?
R: Para extraer información del contexto o iniciar transiciones.

P: ¿Cuál es la diferencia clave entre State y Strategy?
R: En State los estados pueden conocerse entre sí e iniciar transiciones; las estrategias casi nunca se conocen y son completamente independientes.

P: ¿Qué principios de diseño favorece State?
R: El principio de responsabilidad única (código de cada estado en clases separadas) y el principio de abierto/cerrado (nuevos estados sin cambiar los existentes ni el contexto).

P: ¿Cuándo puede ser excesivo aplicar State?
R: Cuando la máquina de estados tiene pocos estados o cambia raramente.

P: En el ejemplo del Documento, ¿cómo se comporta el método publicar en cada estado?
R: En Borrador mueve el documento a moderación; en Moderación lo hace público sólo si el usuario es administrador; en Publicado no hace nada.

P: En el pseudocódigo del AudioPlayer, ¿cómo delega las entradas del usuario?
R: El contexto mantiene un campo state y delega clickLock, clickPlay, clickNext y clickPrevious al estado activo, que dispara transiciones con player.changeState(...).

## Preguntas de autoevaluación

P: ¿Por qué el enfoque de condicionales para máquinas de estado se vuelve difícil de mantener? (Sección "Problema")
R: Porque al añadir más estados y comportamientos la mayoría de los métodos contienen condicionales monstruosos, y cualquier cambio en la lógica de transición puede requerir modificar los condicionales de estado de cada método.

P: ¿Qué propone la solución de State para eliminar esos condicionales? (Sección "Solución")
R: Crear nuevas clases para todos los estados posibles, extraer a ellas el comportamiento específico del estado, y que el contexto delegue el trabajo a un objeto de estado a través de una interfaz común, sustituyéndolo para las transiciones.

P: ¿Por qué los métodos de la interfaz Estado deben tener sentido para todos los estados concretos? (Sección "Estructura")
R: Para evitar métodos inútiles que nunca se invoquen en algunos estados.

P: ¿En qué casos conviene aplicar el patrón State? (Sección "Aplicabilidad")
R: Cuando un objeto se comporta distinto según su estado, hay muchos estados y el código cambia con frecuencia; cuando una clase está contaminada con enormes condicionales; y cuando hay mucho código duplicado entre estados y transiciones similares.

P: ¿Cómo se reduce la duplicación entre estados con comportamiento común? (Secciones "Estructura" y "Aplicabilidad")
R: Incluyendo clases abstractas intermedias (jerarquías de clases de estado) que contengan el comportamiento común.

P: ¿Desde dónde puede realizarse el cambio de estado en el contexto? (Sección "Cómo implementarlo")
R: Instanciando una clase de estado y pasándola al contexto desde el propio contexto, desde otros estados o desde el cliente.

P: ¿Qué patrones comparten estructura con State y en qué se basan todos ellos? (Sección "Relaciones con otros patrones")
R: Bridge, State, Strategy y hasta cierto punto Adapter tienen estructuras muy similares y se basan en la composición (delegar trabajo a otros objetos), pero resuelven problemas diferentes.

P: ¿Por qué se dice que State es una extensión de Strategy? (Sección "Relaciones con otros patrones")
R: Ambos delegan parte del trabajo a objetos ayudantes, pero Strategy los hace completamente independientes, mientras que State no restringe las dependencias entre estados concretos y les permite alterar el estado del contexto.

## Puntos a dominar

- Explicar qué permite State y su relación con la máquina de estados finitos.
- Identificar los tres participantes: contexto, interfaz Estado y estados concretos, y el rol de cada uno.
- Reconocer el problema de los condicionales monstruosos y cómo el patrón lo resuelve.
- Describir cómo se realiza una transición sustituyendo el objeto de estado a través de la interfaz común.
- Distinguir State de Strategy: dependencias entre estados y capacidad de iniciar transiciones.
- Enumerar los pasos de implementación: elegir contexto, declarar interfaz, crear estados, añadir campo y setter, sustituir condicionales, y disparar transiciones.
- Valorar pros (responsabilidad única, abierto/cerrado, contexto simplificado) y contras (excesivo con pocos estados o cambios raros).
