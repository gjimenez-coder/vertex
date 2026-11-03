# Refactoring: Improving the Design of Existing Code — Martin Fowler (con Kent Beck, John Brant, William Opdyke y Don Roberts) (Addison-Wesley, 1999)
## Capítulo 13 — Refactoring, Reuse, and Reality (Refactorización, reutilización y realidad)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas usan la página del PDF.

## Lo que necesitas saber

Capítulo invitado escrito por William Opdyke, cuya tesis doctoral en la Universidad de Illinois fue el primer trabajo escrito mayor sobre refactorización. Opdyke desplaza el foco desde la técnica hacia la realidad: por qué la refactorización, aunque nació en las trincheras del desarrollo (programadores de Smalltalk que necesitaban soportar el cambio y la construcción de frameworks), tardó en ser adoptada por los profesionales de la industria. La tesis central es que hacer la refactorización "real" exige atender las preocupaciones prácticas de los desarrolladores y gerentes, no solo demostrar su valor teórico.

Opdyke parte de su experiencia en Bell Labs desarrollando sistemas de conmutación electrónica, donde la mayor parte del coste no está en la versión inicial sino en adaptar el sistema durante décadas. Relata cómo, al volver con el doctorado, descubrió que nadie compartía su entusiasmo: "People just didn't seem to get it" (PDF p. 312). Esa desconexión tenía dos causas: la novedad de la tecnología orientada a objetos (pocos habían llegado a los problemas de evolución que la refactorización resuelve) y razones de sentido común por las que los desarrolladores se resisten a refactorizar.

Sales sabiendo cuáles son las cuatro objeciones típicas a refactorizar y cómo responder a cada una, cómo se refactorizan específicamente los programas C++, qué significa refactorizar con seguridad mediante herramientas automatizadas, y cómo estas mismas lecciones aplican a la reutilización de software y a la transferencia de tecnología.

## El ejemplo que recorre el capítulo

El caso hilo conductor del beneficio a corto plazo es el framework de sistema de archivos Choices. Inicialmente implementaba el formato BSD Unix y luego se extendió a UNIX System V, MS-DOS, archivos persistentes y distribuidos. Como System V se parece a BSD, el desarrollador primero clonó la implementación BSD y la modificó para System V; funcionaba, pero con mucho código duplicado. Después refactorizó: creó superclases abstractas con el comportamiento común, movió variables y funciones comunes a las superclases, y donde las funciones eran casi idénticas definió funciones nuevas en cada subclase para contener las diferencias, reemplazando esos segmentos por llamadas. El código se hizo incrementalmente más similar hasta que las funciones idénticas pudieron subir a la superclase común.

## Una comprobación de realidad

El coste principal de los sistemas de larga vida (lifetimes de décadas) está en cambiarlos, no en construirlos. Opdyke eligió investigar soporte al cambio y evolución del software porque combinaba interés técnico con necesidad de negocio real. La lección de Ralph Johnson que atraviesa el capítulo: si alguien "no lo entiende", la culpa es nuestra; es responsabilidad del que comunica desarrollar y transmitir bien las ideas.

## Por qué los desarrolladores se resisten a refactorizar

El escenario ideal (proyecto nuevo, sin compatibilidad hacia atrás, comprensión total del problema, financiador paciente) es un sueño. Lo habitual es extender software existente, con comprensión incompleta y presión de calendario. Ante eso hay tres caminos:

- Reescribir el programa: creativo, pero ¿quién lo paga y cómo garantizas que hace todo lo que hacía el viejo?
- Copiar y modificar partes: parece rápido e incluso "reutilización", pero con el tiempo los errores se propagan, los programas se hinchan, el diseño se corrompe y el coste incremental del cambio escala.
- Refactorizar: el punto medio. Restructura el software para hacer explícitas las ideas de diseño, extraer componentes reutilizables, clarificar la arquitectura y preparar futuras adiciones.

Incluso quien acepta estas ventajas puede no refactorizar por cuatro razones válidas (PDF p. 313): (1) no entender cómo refactorizar; (2) si el beneficio es a largo plazo, por qué esforzarse ahora, quizá ni sigas en el proyecto; (3) refactorizar es actividad de overhead, te pagan por escribir features nuevas; (4) refactorizar podría romper el programa. Unas son técnicas y otras de gestión; todas deben abordarse.

## Entender cómo y dónde refactorizar

En el proyecto Software Refactory de Illinois tomaron un enfoque minimalista: un conjunto reducido de refactorizaciones basadas en su experiencia y en retrospectivas de desarrolladores Smalltalk. La mayoría son de bajo nivel (crear/borrar una clase, variable o función; cambiar permisos de acceso o argumentos; mover miembros entre clases). Un conjunto menor de alto nivel (crear una superclase abstracta, simplificar con subclases o condicionales, extraer una clase componente reutilizable) se define en términos de las de bajo nivel.

Qué refactorización aplicar depende de los objetivos. Una herramienta automatizada puede identificar debilidades estructurales (funciones con demasiados argumentos o demasiado largas) y similitudes que indican redundancia (dos funciones casi idénticas por copy-and-modify). Es análogo a aplicar lint a un programa C/C++: la herramienta no entiende el significado del programa, solo sugiere; el programador decide qué aplicar. El trabajo en patrones de diseño conecta con esto: la sección de aplicabilidad del template method apunta a la refactorización de superclase abstracta de Opdyke.

## Refactorizar programas C++ (recuadro)

C++ tiene rasgos que facilitan y rasgos que complican la refactorización.

Favorecen: el tipado estático permite acotar las referencias a renombrar; el control de acceso (public, protected, private) limita dónde pueden existir referencias (private: solo la clase y sus friends; protected: clase, subclases, descendientes y friends); el uso de herencia para modelar jerarquías facilita generalizar o especializar el alcance de miembros; y el compilador suele señalar los bugs introducidos.

Complican: la compatibilidad con C es un arma de doble filo. Punteros, operaciones de cast y `sizeof(object)` dificultan refactorizar porque introducen aliasing y exponen la representación interna. Ejemplo del V-table: mover una variable a la superclase es seguro si todas las referencias pasan por la interfaz, pero si se accedió por aritmética de punteros (escribir el quinto byte) o por `if (sizeof(object)==15)`, el cambio altera el comportamiento. "Migrar de C a C++ no convierte a nadie en programador o diseñador orientado a objetos" (parafraseado, PDF p. 317). Además, C++ resuelve referencias en tiempo de compilación, así que cada iteración exige recompilar y relincar (coste mayor que en Smalltalk o CLOS, que permiten interpretación y compilación incremental); los cambios a objetos pueden exigir cambios de esquema en la base de datos; y C++ no ofrece un protocolo de metaobjetos como CLOS.

## Beneficios a corto plazo

La refactorización lleva más de diez años aplicándose por desarrolladores experimentados, muchos de cultura Smalltalk, que valoraba claridad, simplicidad y reutilización. Para que el mainstream la adopte, al menos parte del beneficio debe ser a corto plazo. El caso Choices muestra beneficios inmediatos: los errores del código común se corrigen en un solo sitio, el tamaño del código es menor y el comportamiento específico de cada formato queda separado del común. A mediano plazo, las abstracciones resultantes sirven de punto de partida para nuevos formatos, de modo que añadir soporte cuesta cada vez menos, incluso con personal menos experimentado.

Analogía: la refactorización es como el ejercicio y una dieta equilibrada; todos sabemos que deberíamos, algunos lo posponen hasta una crisis, y conviene consultar a un experto (el médico allí; este libro y los papers aquí). La refactorización es un medio, no un fin.

## Reducir el overhead

Respuesta a "me pagan por features nuevas": hay herramientas y técnicas para hacerlo rápido; la experiencia reportada indica que el overhead se compensa con menor esfuerzo en otras fases; y, al volverse rutina, deja de sentirse como overhead y pasa a sentirse esencial. La herramienta automatizada más madura es la del equipo de Illinois para Smalltalk (ver Capítulo 14), disponible gratis en su web. Para otros lenguajes, muchas técnicas se aplican con un editor de texto o, mejor, un browser. Kent Beck y Ward Cunningham han reportado desarrollo rápido con refactorización en dominios como el trading de bonos. Consejo a los escépticos: "just do it", pruébalo tú mismo y dale tiempo.

## Refactorizar con seguridad

Una refactorización segura es la que no rompe el programa: debe comportarse igual antes y después. Opciones para refactorizar con seguridad: confiar en tu habilidad de codificar; en que el compilador atrape errores; en que la suite de pruebas los atrape; y en que la revisión de código los atrape. Todas tienen límites: los programadores son falibles; hay errores que el compilador no atrapa (sobre todo de scoping ligados a herencia); probar todos los caminos de ejecución es indecidible (Perry y Kaiser muestran que la herencia exige muchas más pruebas de lo que suponía la sabiduría común); y los revisores también son falibles y están ocupados.

El enfoque de Opdyke: un analizador de programa dentro de una herramienta que comprueba si la refactorización es segura antes de aplicarla. Definió la seguridad en términos de propiedades del programa (scoping, typing) que deben seguir cumpliéndose, análogas a las restricciones de integridad al cambiar esquemas de base de datos. Cada refactorización tiene precondiciones necesarias; solo si se cumplen la herramienta la aplica. Las de alto nivel se definen con las de bajo nivel, de modo que la seguridad se conoce por construcción. Ejemplo: borrar una variable referenciada dejaría referencias colgantes, así que la herramienta lo marca; incluso si la referencia estuviera en código que nunca se ejecuta (una condición siempre falsa, indecidible en general), la herramienta toma la ruta segura y avisa al usuario en lugar de aplicar el cambio a ciegas. El prototipo evolucionó a una herramienta más robusta de Roberts, Brant, Johnson y Opdyke (Capítulo 14). Las técnicas de seguridad evitan introducir errores nuevos, pero no detectan los que ya existían, aunque la refactorización puede facilitar verlos.

## Implicaciones para la reutilización y la transferencia de tecnología

Las mismas cuatro preocupaciones aplican más allá de la refactorización: a la reutilización de software y la evolución de sistemas legados (el personal puede no saber qué o cómo reutilizar; necesita beneficios a corto plazo; hay que atender overhead y curva de aprendizaje; y la adopción no debe ser disruptiva, debe interoperar o ser compatible hacia atrás). Opdyke invoca el modelo de Geoffrey Moore (Crossing the Chasm): para triunfar, una idea debe cruzar el "abismo" desde innovadores y early adopters hacia la early y late majority, que se mueven por madurez, coste, soporte y evidencia de éxito ajeno, no por visiones de paradigma. Los investigadores suelen ser innovadores; desarrolladores y, sobre todo, gerentes están en las mayorías. Como señaló Ralph Johnson, estos principios no son exclusivos de la refactorización ni de la reutilización: son cuestiones genéricas de transferencia de tecnología. Hay que llegar a los profesionales en sus propios términos.

## Ideas clave

- La refactorización nació en las trincheras (Smalltalk) y maduró en la investigación; hacerla "real" exige atender preocupaciones prácticas, no solo técnicas.
- Es el punto medio entre reescribir (caro, arriesgado) y copiar-y-modificar (que corrompe el diseño con el tiempo).
- Cuatro objeciones a abordar: no saber cómo, beneficio solo a largo plazo, overhead frente a features, y riesgo de romper el programa.
- Las refactorizaciones complejas se definen en términos de otras de bajo nivel, y herramientas tipo lint pueden sugerir dónde aplicarlas, pero el programador decide.
- En C++, el tipado estático y el control de acceso ayudan; punteros, casts y `sizeof` que exponen la representación interna complican y pueden alterar el comportamiento.
- El caso Choices (BSD → System V) ilustra beneficios a corto plazo: arreglos en un solo sitio, menos código y separación de lo específico frente a lo común.
- Seguridad = preservar propiedades del programa mediante precondiciones verificables; la herramienta solo refactoriza si todo es seguro y, ante la duda, avisa en vez de actuar.
- Las lecciones de refactorización se generalizan a la reutilización y, según el modelo de Moore, a cruzar el abismo de la adopción tecnológica.
