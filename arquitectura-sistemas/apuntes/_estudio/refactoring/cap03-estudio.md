# Bad Smells in Code (Malos olores en el código) — Estudio

## Tarjetas de repaso

P: ¿Qué es un *smell* (olor) en el código y para qué sirve?
R: Una estructura en el código que sugiere o grita la posibilidad de refactorizar; describe el *cuándo* refactorizar, no el *cómo*.

P: Según los autores, ¿qué supera a cualquier conjunto de métricas para decidir cuándo refactorizar?
R: La intuición humana informada; ningún conjunto de métricas rivaliza con ella, por eso solo dan indicios de que hay un problema.

P: ¿Cuál es el "número uno del desfile de hedores" y por qué?
R: El código duplicado (Duplicated Code): la misma estructura en más de un sitio, y unificarla siempre mejora el programa.

P: ¿Qué refactorizaciones aplicar a código duplicado en dos subclases hermanas?
R: *Extract Method* en ambas y luego *Pull Up Field*; si es parecido pero no igual, *Extract Method* y quizá *Form Template Method*; si el algoritmo difiere, *Substitute Algorithm*.

P: En Long Method, ¿qué es realmente lo clave, más allá de la longitud?
R: La distancia semántica entre qué hace el método y cómo lo hace; cuando sientas la necesidad de comentar, escribe un método nombrado por la intención.

P: ¿Qué diferencia a Divergent Change de Shotgun Surgery?
R: En Divergent Change una clase cambia de formas distintas por razones distintas; en Shotgun Surgery un solo cambio obliga a muchos cambios pequeños en muchas clases. Son caras opuestas.

P: ¿Qué es Feature Envy y cuál es su regla general?
R: Un método más interesado en otra clase que en la suya (invoca muchos getters ajenos). Regla: poner el método donde están la mayoría de los datos, usando *Move Method*.

P: ¿Qué prueba sencilla delata un Data Clump?
R: Si borras uno de los valores que aparecen juntos, ¿tienen sentido los demás? Si no, hay un objeto esperando nacer (*Extract Class*).

P: ¿Cuál es el verdadero problema de los Switch Statements y su respuesta elegante?
R: La duplicación del mismo switch disperso que hay que cambiar en todas partes; la respuesta elegante es la polimorfia (*Replace Conditional with Polymorphism*).

P: ¿Cuándo NO conviene usar polimorfia para un switch?
R: Cuando son pocos casos estables: entonces la polimorfia es excesiva y se usa *Replace Parameter with Explicit Methods*; para un caso nulo, *Introduce Null Object*.

P: ¿Qué es Middle Man y cómo se corrige el exceso de delegación?
R: Una clase cuya interfaz delega en exceso en otra; se corrige con *Remove Middle Man*, *Inline Method* si son pocos, o *Replace Delegation with Inheritance* si hay comportamiento adicional.

P: ¿Qué hacer con una Incomplete Library Class, dado que no se puede modificar?
R: Como *Move Method* es inútil, si faltan un par de métodos usar *Introduce Foreign Method*; si falta mucho comportamiento, *Introduce Local Extension*.

P: ¿Qué postura tienen los autores sobre los comentarios?
R: No son mal olor, pero suelen actuar como desodorante que tapa código malo; primero refactorizar hasta que el comentario quede superfluo.

P: ¿Cuál es la regla rectora que conecta muchos olores?
R: Poner juntas las cosas que cambian juntas; datos y el comportamiento que los usa suelen cambiar a la vez.

## Preguntas de autoevaluación

P: ¿Por qué el capítulo se centra en los *smells* en vez de dar criterios numéricos precisos?
R: Porque, según la experiencia de los autores, ningún conjunto de métricas rivaliza con la intuición humana informada; los smells solo dan indicios de un problema resoluble. El lector debe desarrollar su propio sentido de cuánto es "demasiado". (Lo que necesitas saber)

P: Si encuentras código duplicado en dos clases no relacionadas, ¿cómo lo abordarías?
R: Aplicando *Extract Class* en una y usando el nuevo componente en la otra, o decidiendo en qué clase (o en una tercera) debe vivir el método. (Duplicated Code)

P: ¿Por qué no preocupa demasiado el coste de las llamadas al dividir métodos largos?
R: Porque en OO moderno el coste de las llamadas es mínimo; el coste real para el lector se mitiga con buenos nombres, con los que no hace falta mirar el cuerpo del método. (Long Method)

P: ¿Cómo se detecta una Large Class y qué pista dan los nombres de sus variables?
R: Por tener demasiadas variables de instancia (suele hacer demasiado y aparecer duplicación); prefijos o sufijos comunes señalan componentes que agrupar con *Extract Class* o *Extract Subclass*. (Large Class)

P: ¿Qué son las Parallel Inheritance Hierarchies y cómo se eliminan?
R: Un caso especial de shotgun surgery donde cada subclase de una jerarquía obliga a crear otra en la paralela (se reconocen por prefijos de nombre iguales). Se hace que una jerarquía referencie a la otra y, con *Move Method* y *Move Field*, desaparece una. (Parallel Inheritance Hierarchies)

P: ¿Cuándo un Refused Bequest es un olor fuerte que conviene limpiar?
R: Cuando la subclase reutiliza comportamiento pero rechaza la interfaz del padre; ahí se aplica *Replace Inheritance with Delegation*. Nueve de cada diez veces el olor es demasiado tenue para actuar. (Refused Bequest)

P: ¿Qué debe ocurrir con una Data Class a largo plazo y con qué refactorizaciones?
R: Debe asumir responsabilidad moviendo comportamiento hacia ella (*Move Method*, o *Extract Method* previo) y ocultando accesores con *Hide Method*, además de *Encapsulate Field/Collection* y *Remove Setting Method*. (Data Class)

P: ¿Cuál es el buen uso de un comentario según el capítulo?
R: Cuando no sabes qué hacer, o para explicar *por qué* hiciste algo (no el cómo). El texto recomienda refactorizar antes para que el comentario se vuelva superfluo. (Comments)

## Puntos a dominar

- Reconocer que los smells indican el *cuándo* refactorizar y confiar en la intuición informada más que en métricas fijas.
- Identificar Duplicated Code como el peor olor y cómo casi todos los demás (clases grandes, métodos largos) lo alimentan.
- Distinguir Divergent Change de Shotgun Surgery y buscar la relación uno a uno entre tipos de cambio y clases.
- Aplicar *Extract Method* y *Move Method* como refactorizaciones recurrentes en casi todos los olores.
- Curar olores creando objetos pequeños a partir de primitivos y grumos de datos (Primitive Obsession, Data Clumps).
- Resolver Switch Statements con polimorfia, salvo pocos casos estables.
- Tratar los comentarios con moderación: refactorizar hasta volverlos innecesarios y reservarlos para el *por qué*.
