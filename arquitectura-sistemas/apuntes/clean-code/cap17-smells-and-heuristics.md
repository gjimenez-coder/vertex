# Clean Code: A Handbook of Agile Software Craftsmanship — Robert C. Martin (Prentice Hall, 2008)
## Capítulo 17 — Smells and Heuristics (Olores y heurísticas)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF y las citas usan la página del PDF.

## Lo que necesitas saber

Este capítulo es un catálogo de referencia de "code smells" (olores del código) y heurísticas que el autor recopiló refactorizando programas: en cada cambio se preguntaba por qué lo hacía y anotaba la razón. El resultado es una lista larga de señales que delatan código problemático, agrupada por categorías: comentarios, entorno, funciones, generales, Java, nombres y pruebas. La lista toma muchos olores de *Refactoring* de Martin Fowler y añade otros propios.

Está pensado para leerse de arriba abajo y también como referencia; el apéndice C del libro (PDF p. 409) cruza cada heurística con el resto del texto. Sales sabiendo reconocer los síntomas más frecuentes de código sucio y las correcciones típicas asociadas.

La tesis de cierre es clave: la lista no pretende ser completa ni sustituir el juicio. Lo que importa es que implica un sistema de valores. El código limpio no nace de seguir reglas, sino de valores que impulsan disciplinas; ser un artesano del software no se logra memorizando heurísticas.

## Comentarios (C)

- **C1 Inappropriate Information**: no guardar en comentarios lo que corresponde a otros sistemas (control de versiones, seguimiento de incidencias). Nada de historiales de cambios ni metadatos (autor, fecha, número de SPR).
- **C2 Obsolete Comment**: un comentario viejo, irrelevante o incorrecto está obsoleto. Lo mejor es no escribir comentarios que caducarán; si aparece uno obsoleto, actualizarlo o eliminarlo.
- **C3 Redundant Comment**: redundante si describe algo que ya se describe solo, como `i++; // increment i` o un Javadoc que repite la firma. Los comentarios deben decir lo que el código no puede.
- **C4 Poorly Written Comment**: si vale la pena escribirlo, hazlo bien: palabras cuidadas, gramática correcta, breve, sin divagar ni decir lo obvio.
- **C5 Commented-Out Code**: el código comentado se pudre y nadie lo borra. Bórralo; el control de versiones lo recuerda.

## Entorno (E)

- **E1 Build Requires More Than One Step**: compilar debe ser una operación trivial de un solo paso (`svn get`, `ant all`), sin secuencias de comandos arcanos ni búsquedas de JARs sueltos.
- **E2 Tests Require More Than One Step**: todas las pruebas unitarias deben ejecutarse con un solo comando o botón.

## Funciones (F)

- **F1 Too Many Arguments**: pocos argumentos; cero es lo mejor, luego uno, dos y tres. Más de tres es muy cuestionable.
- **F2 Output Arguments**: antinaturales; si hay que cambiar un estado, cámbiese el del objeto sobre el que se invoca.
- **F3 Flag Arguments**: un booleano declara que la función hace más de una cosa; eliminarlos.
- **F4 Dead Function**: los métodos nunca llamados se descartan.

## Generales (G)

Las heurísticas generales son el bloque más extenso:

- **G1 Multiple Languages in One Source File**: minimizar número y extensión de lenguajes por archivo; el ideal es uno solo.
- **G2 Obvious Behavior Is Unimplemented**: por el principio de mínima sorpresa, implementar lo que otro programador razonablemente esperaría (p. ej. `"Monday"` → `Day.MONDAY`, ignorar mayúsculas y abreviaturas).
- **G3 Incorrect Behavior at the Boundaries**: no confiar en la intuición; buscar cada condición límite y escribir una prueba.
- **G4 Overridden Safeties**: desactivar seguridades es arriesgado (como Chernobyl); apagar advertencias del compilador o pruebas que fallan trae problemas.
- **G5 Duplication**: una de las reglas más importantes. Es el principio DRY (Don't Repeat Yourself) de Hunt y Thomas y el "Once, and only once" de Beck. Cada duplicación es una abstracción perdida: bloques idénticos → métodos; `switch`/`if-else` repetidos → polimorfismo; algoritmos similares → patrones TEMPLATE METHOD o STRATEGY.
- **G6 Code at Wrong Level of Abstraction**: separar conceptos de alto y bajo nivel por completo. Ejemplo: `percentFull()` no pertenece a la interfaz `Stack` sino a una derivada como `BoundedStack`; no se puede fingir una abstracción mal ubicada.
- **G7 Base Classes Depending on Their Derivatives**: en general las clases base no deben conocer a sus derivadas; permite desplegarlas en JARs distintos e independientes.
- **G8 Too Much Information**: interfaces pequeñas y ajustadas reducen el acoplamiento. Oculta datos, funciones de utilidad, constantes y temporales.
- **G9 Dead Code**: código que no se ejecuta (ifs imposibles, catches que nunca saltan); bórralo.
- **G10 Vertical Separation**: variables y funciones cerca de su uso; locales justo antes del primer uso, funciones privadas justo debajo.
- **G11 Inconsistency**: haz las cosas similares del mismo modo (mismo nombre de variable para un mismo tipo, nombres análogos de métodos).
- **G12 Clutter**: elimina constructores vacíos, variables sin uso, funciones sin llamar y comentarios inútiles.
- **G13 Artificial Coupling**: no acoplar cosas que no dependen entre sí (enums generales dentro de clases específicas); coloca cada cosa donde corresponde.
- **G14 Feature Envy** (olor de Fowler): un método que usa accessors/mutators de otra clase envidia su ámbito. A veces es un mal necesario (p. ej. un reporte que no debe acoplar el formato a `HourlyEmployee`).
- **G15 Selector Arguments**: un `false` colgando al final de una llamada es abominable; mejor varias funciones que pasar código para seleccionar comportamiento.
- **G16 Obscured Intent**: expresiones amontonadas, notación húngara y números mágicos ocultan la intención.
- **G17 Misplaced Responsibility**: el código va donde el lector esperaría encontrarlo (p. ej. `PI` junto a las funciones trigonométricas); usa los nombres de funciones como guía.
- **G18 Inappropriate Static**: prefiere métodos no estáticos; `Math.max` es buen static, pero `calculatePay` podría necesitar polimorfismo. Ante la duda, no estático.
- **G19 Use Explanatory Variables**: divide los cálculos en valores intermedios con nombres significativos; difícil excederse.
- **G20 Function Names Should Say What They Do**: si hay que mirar la implementación para saber qué hace (`date.add(5)`), mejora el nombre (`addDaysTo`, `daysLater`).
- **G21 Understand the Algorithm**: no basta con que pase las pruebas; hay que saber que la solución es correcta, a menudo refactorizando hasta que sea evidente.
- **G22 Make Logical Dependencies Physical**: toda dependencia lógica debe hacerse física. Ejemplo (Listing 17-1): `HourlyReporter` conoce `PAGE_SIZE`, que debería pedirle a `HourlyReportFormatter` vía `getMaxPageSize()`.
- **G23 Prefer Polymorphism to If/Else or Switch/Case**: todo `switch` es sospechoso. Regla "ONE SWITCH": a lo sumo un switch por tipo de selección, que cree objetos polimórficos.
- **G24 Follow Standard Conventions**: el equipo sigue un estándar basado en normas de la industria; el propio código sirve de ejemplo.
- **G25 Replace Magic Numbers with Named Constants**: oculta números crudos tras constantes (86 400 → `SECONDS_PER_DAY`). Algunos (5280, `Math.PI`) son tan conocidos que a veces no hace falta. "Número mágico" aplica a cualquier token no autodescriptivo (`7777`, `"John Doe"`).
- **G26 Be Precise**: decide con precisión (no usar floats para dinero, comprobar null, gestionar concurrencia). La imprecisión es desacuerdo o pereza.
- **G27 Structure over Convention**: refuerza decisiones con estructura, no solo convención (clases base con métodos abstractos > switch con enums).
- **G28 Encapsulate Conditionals**: extrae funciones que expliquen la condición (`shouldBeDeleted(timer)`).
- **G29 Avoid Negative Conditionals**: expresa condicionales en positivo.
- **G30 Functions Should Do One Thing**: divide funciones con varias secciones en funciones pequeñas que hagan una sola cosa.
- **G31 Hidden Temporal Couplings**: no ocultes el acoplamiento temporal; estructura los argumentos como una "bucket brigade" donde cada función produce lo que la siguiente necesita.
- **G32 Don't Be Arbitrary**: ten una razón para la estructura y comunícala; lo arbitrario invita a cambiarlo.
- **G33 Encapsulate Boundary Conditions**: concentra las condiciones límite en un lugar (`int nextLevel = level + 1;`) sin esparcir `+1` y `-1`.
- **G34 Functions Should Descend Only One Level of Abstraction**: todas las sentencias de una función en el mismo nivel, uno por debajo del nombre (ejemplo `HruleWidget`/`HtmlTag`); de las más difíciles de seguir.
- **G35 Keep Configurable Data at High Levels**: las constantes de configuración residen en niveles altos (clase `Arguments` de FitNesse) y se pasan hacia abajo.
- **G36 Avoid Transitive Navigation**: Ley de Demeter / "Writing Shy Code": evita `a.getB().getC()`; los colaboradores inmediatos ofrecen lo que necesitas.

## Java (J)

- **J1 Avoid Long Import Lists by Using Wildcards**: si usas dos o más clases de un paquete, importa `package.*`; los comodines no crean dependencias duras y reducen acoplamiento.
- **J2 Don't Inherit Constants**: no escondas constantes en lo alto de la jerarquía heredando una interfaz; usa `import static`.
- **J3 Constants versus Enums**: con enums en el lenguaje (Java 5), úsalos; pueden tener métodos y campos, son más expresivos que `public static final int`.

## Nombres (N)

- **N1 Choose Descriptive Names**: los nombres son el 90 % de lo que hace legible el software (ejemplo del "Bowling Game": `score`, `isStrike`, `isSpare` frente a `q`, `z`, `l`).
- **N2 Choose Names at the Appropriate Level of Abstraction**: nombres que reflejen el nivel de abstracción, no la implementación (`Modem` con `connect`/`connectionLocator` en vez de números de teléfono).
- **N3 Use Standard Nomenclature Where Possible**: apóyate en convenciones y patrones (`Decorator`, `toString`); Evans lo llama lenguaje ubicuo.
- **N4 Unambiguous Names**: nombres inequívocos (`renamePageAndOptionallyAllReferences` mejor que `doRename`).
- **N5 Use Long Names for Long Scopes**: la longitud del nombre va con la del ámbito; `i`, `j` sirven en ámbitos pequeños.
- **N6 Avoid Encodings**: sin prefijos de tipo/ámbito (`m_`, `f`, `vis_`) ni "contaminación húngara".
- **N7 Names Should Describe Side-Effects**: el nombre describe todo lo que hace (`getOos` que además crea → `createOrReturnOos`).

## Pruebas (T)

- **T1 Insufficient Tests**: una suite debe probar todo lo que pueda romperse, no "parece suficiente".
- **T2 Use a Coverage Tool!**: revelan huecos (líneas verdes/rojas en el IDE).
- **T3 Don't Skip Trivial Tests**: baratos y de alto valor documental.
- **T4 An Ignored Test Is a Question about an Ambiguity**: expresa dudas de requisitos como test comentado o con `@Ignore`.
- **T5 Test Boundary Conditions**: cuida especialmente los límites.
- **T6 Exhaustively Test Near Bugs**: los bugs se agrupan; prueba a fondo la función donde aparece uno.
- **T7 Patterns of Failure Are Revealing**: los patrones de fallo (p. ej. toda entrada mayor de cinco caracteres falla) dan pistas.
- **T8 Test Coverage Patterns Can Be Revealing**: ver qué código ejecutan las pruebas que pasan aclara por qué fallan otras.
- **T9 Tests Should Be Fast**: una prueba lenta acaba sin ejecutarse.

## Ideas clave

- Es un catálogo de referencia, no una lista exhaustiva; su valor real es implicar un sistema de valores, no dictar reglas.
- G5 (Duplication/DRY) es una de las reglas más importantes del libro: cada duplicación es una abstracción perdida.
- El principio de mínima sorpresa recorre varias heurísticas (G2, G11, G17): el código va donde el lector lo espera.
- Separar niveles de abstracción (G6, G34, N2) es de lo más difícil y valioso al refactorizar.
- Los números y tokens mágicos deben esconderse tras constantes o nombres con significado (G16, G25, N1).
- En Java: comodines sobre listas largas de imports, `import static` en vez de heredar constantes, y enums sobre `int`.
- El código limpio surge de valores y disciplina, no de memorizar heurísticas.
