# Smells and Heuristics (Olores y heurísticas) — Estudio

## Tarjetas de repaso

P: ¿Qué es este capítulo y cómo nació la lista de olores y heurísticas?
R: Es un catálogo de referencia que el autor recopiló refactorizando programas, anotando en cada cambio por qué lo hacía; toma muchos olores de *Refactoring* de Fowler y añade otros propios.

P: ¿Cuál es la tesis de cierre del capítulo?
R: La lista no es completa ni sustituye al juicio; lo que importa es que implica un sistema de valores. El código limpio surge de valores y disciplina, no de memorizar heurísticas.

P: ¿Qué dice la heurística G5 (Duplication) y con qué principios se relaciona?
R: Es una de las reglas más importantes; corresponde al principio DRY (Don't Repeat Yourself) de Hunt y Thomas y al "Once, and only once" de Beck. Cada duplicación es una abstracción perdida.

P: Según C5, ¿qué hacer con el código comentado (commented-out)?
R: Borrarlo, porque se pudre y nadie lo elimina; el control de versiones lo recuerda.

P: ¿Qué establecen E1 y E2 sobre compilación y pruebas?
R: Compilar debe ser una operación trivial de un solo paso y todas las pruebas unitarias deben ejecutarse con un solo comando o botón.

P: ¿Qué número de argumentos es ideal en una función (F1) y qué indica un flag argument (F3)?
R: Cero argumentos es lo mejor, luego uno, dos y tres; más de tres es muy cuestionable. Un booleano (flag) declara que la función hace más de una cosa, por lo que debe eliminarse.

P: ¿Qué propone G23 frente a los switch/case y qué es la regla "ONE SWITCH"?
R: Prefiere polimorfismo; todo switch es sospechoso. La regla ONE SWITCH admite a lo sumo un switch por tipo de selección, y este debe crear objetos polimórficos.

P: ¿Qué dice G25 sobre los números mágicos y cuándo se permiten tokens crudos?
R: Oculta los números crudos tras constantes con nombre (86 400 → SECONDS_PER_DAY). Algunos tan conocidos (5280, Math.PI) a veces no hacen falta. "Número mágico" aplica a cualquier token no autodescriptivo.

P: ¿Qué principio recorre G2, G11 y G17?
R: El principio de mínima sorpresa: implementar lo esperable, hacer las cosas similares del mismo modo y poner el código donde el lector espera encontrarlo.

P: ¿En qué consiste G36 y con qué ley/estilo se asocia?
R: Evitar la navegación transitiva (a.getB().getC()); se asocia a la Ley de Demeter y a "Writing Shy Code": los colaboradores inmediatos deben ofrecer lo necesario.

P: ¿Qué recomiendan J1, J2 y J3 en Java?
R: J1: usar comodines (package.*) ante dos o más clases de un paquete para reducir acoplamiento; J2: no heredar constantes, usar import static; J3: preferir enums sobre public static final int por ser más expresivos.

P: Según N1, ¿qué peso tienen los nombres en la legibilidad?
R: Los nombres son el 90 % de lo que hace legible el software (ejemplo del Bowling Game: score, isStrike, isSpare frente a q, z, l).

P: ¿Qué diferencia a G6/G34/N2 como grupo y por qué importan?
R: Tratan la separación de niveles de abstracción (ubicación correcta, descender solo un nivel, nombres al nivel adecuado); es de lo más difícil y valioso al refactorizar.

P: ¿Qué pide T1 y qué papel juega T2 (cobertura)?
R: T1: la suite debe probar todo lo que pueda romperse, no lo que "parece suficiente". T2: usar una herramienta de cobertura que revele huecos (líneas verdes/rojas en el IDE).

P: ¿Qué revelan T6 y T7 sobre los bugs?
R: T6: los bugs se agrupan, así que hay que probar a fondo la función donde aparece uno. T7: los patrones de fallo (p. ej. toda entrada mayor de cinco caracteres falla) dan pistas.

## Preguntas de autoevaluación

P: ¿Por qué no deben guardarse historiales de cambios ni metadatos como autor o fecha en los comentarios?
R: Porque esa información corresponde a otros sistemas como el control de versiones y el seguimiento de incidencias (C1, sección Comentarios).

P: ¿Qué relación tienen entre sí Feature Envy (G14) y Misplaced Responsibility (G17), y cuándo puede justificarse acoplar código ajeno?
R: Ambas tratan de colocar el código donde corresponde. Feature Envy es un método que usa accessors/mutators de otra clase; a veces es un mal necesario, como un reporte que no debe acoplar el formato a HourlyEmployee (sección Generales).

P: ¿Qué significa G22 "Make Logical Dependencies Physical" y qué ejemplo lo ilustra?
R: Toda dependencia lógica debe hacerse física. En el Listing 17-1, HourlyReporter conoce PAGE_SIZE, que debería pedir a HourlyReportFormatter mediante getMaxPageSize() (sección Generales).

P: ¿Cuál es la diferencia entre reforzar una decisión por convención y por estructura (G27)?
R: La convención depende de que se cumpla un acuerdo; la estructura la refuerza en el diseño. Es mejor usar clases base con métodos abstractos que un switch con enums (sección Generales).

P: ¿Por qué G4 compara desactivar seguridades con Chernobyl?
R: Porque apagar advertencias del compilador o ignorar pruebas que fallan desactiva salvaguardas y trae problemas, igual que anular seguridades es arriesgado (G4, sección Generales).

P: ¿Qué debe describir el nombre de una función según N7 y G20?
R: N7: el nombre debe describir todos sus efectos secundarios (getOos que además crea → createOrReturnOos). G20: si hay que leer la implementación para saber qué hace (date.add(5)), el nombre debe mejorarse (addDaysTo, daysLater).

P: ¿Qué recomienda T4 cuando hay ambigüedad en los requisitos?
R: Expresar la duda como un test comentado o con @Ignore; una prueba ignorada es una pregunta sobre una ambigüedad (sección Pruebas).

P: ¿Por qué deben ser rápidas las pruebas (T9) y de un solo paso (E2)?
R: Una prueba lenta acaba sin ejecutarse (T9), y si ejecutar las pruebas no es trivial de un solo paso (E2) también se dejan de correr, perdiendo su valor.

## Puntos a dominar

- Reconocer que el capítulo es un catálogo de referencia cuyo valor real es implicar un sistema de valores, no dictar reglas.
- Dominar G5 (Duplication/DRY) como una de las reglas centrales: cada duplicación es una abstracción perdida.
- Entender el principio de mínima sorpresa que recorre G2, G11 y G17: el código va donde el lector lo espera.
- Saber separar niveles de abstracción (G6, G34, N2) al refactorizar.
- Esconder números y tokens mágicos tras constantes o nombres con significado (G16, G25, N1).
- Aplicar las heurísticas de Java: comodines sobre listas largas de imports, import static en vez de heredar constantes y enums sobre int.
- Interiorizar que el código limpio surge de valores y disciplina, no de memorizar heurísticas.
