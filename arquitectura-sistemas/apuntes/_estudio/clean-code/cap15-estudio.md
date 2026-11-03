# JUnit Internals (Interioridades de JUnit) — Estudio

## Tarjetas de repaso

P: ¿Qué módulo de JUnit se usa como banco de pruebas en el capítulo? / R: `ComparisonCompactor`, un trozo ingenioso que ayuda a identificar errores de comparación de strings.

P: ¿Qué hace `ComparisonCompactor` ante dos strings que difieren como `ABCDE` y `ABXDE`? / R: Expone la diferencia generando un string como `<...B[X]D...>`.

P: ¿Cómo describe Martin el código original de JUnit? / R: Como «simple en concepción, preciso en definición y elegante en implementación» (PDF p. 282).

P: ¿Cuál es la tesis central del capítulo? / R: Que ningún módulo es inmune a la mejora y que cada quien tiene la responsabilidad de dejar el código mejor de como lo encontró.

P: ¿Por qué se elimina el prefijo `f` de las variables miembro? / R: Porque es una codificación de ámbito redundante [N6]; `fExpected` pasa a `expected`.

P: ¿Por qué se renombra `compact` a `formatCompactedComparison`? / R: Porque `compact` oculta un efecto (puede no compactar) y además formatea; el nombre correcto refleja lo que hace [N7].

P: ¿Qué se gana al invertir el condicional negativo mediante `canBeCompacted()`? / R: Mejorar la lectura, ya que los negativos cuestan más de leer [G29].

P: ¿Qué es el acoplamiento temporal detectado en `findCommonSuffix`? / R: Depende de que `prefixIndex` ya se haya calculado en `findCommonPrefix` [G31].

P: ¿Cómo se resuelve ese acoplamiento temporal? / R: Fusionando en `findCommonPrefixAndSuffix`, que llama internamente a `findCommonPrefix` primero, haciendo el orden evidente.

P: ¿Cuál era el verdadero origen de los `+1` dispersos? / R: `suffixIndex` no era base cero sino base uno, por lo que no era una longitud real [G33]; se renombra a `suffixLength`.

P: ¿Cómo queda particionado el módulo en el Listado 15-5? / R: En funciones de análisis (`findCommonPrefix`, `findCommonPrefixAndSuffix`, `charFromEnd`, `suffixOverlapsPrefix`) y de síntesis (`compact`, `startingEllipsis`, etc.), ordenadas topológicamente.

P: ¿Qué muestra el Listado 15-3 por contraste? / R: Una versión «defactored» (deteriorada) con nombres como `ctxt`, `s1`, `s2`, `pfx`, `sfx`.

P: ¿Qué es la Regla del Boy Scout aplicada aquí? / R: Dejar el código un poco más limpio de como lo encontraste, aunque ya estuviera bien.

P: ¿Por qué correr los tests tras cada cambio permite eliminar código muerto con confianza? / R: Porque la cobertura es del 100%, así se verifica que los `if` que ya no hacían nada pueden comentarse sin romper nada.

## Preguntas de autoevaluación

P: ¿De dónde proviene `ComparisonCompactor` según el capítulo? / R: De Kent Beck y Erich Gamma escribiendo JUnit en tres horas durante un vuelo a Atlanta (PDF p. 283). (Sección: El ejemplo que recorre el capítulo.)

P: ¿Qué cobertura dan los tests sobre el código original y por qué importa? / R: 100%, lo que permite refactorizar y eliminar código muerto con confianza. (Secciones: El ejemplo que recorre el capítulo; Los cambios aplicados.)

P: ¿Por qué deshacer `this.expected`/`this.actual` y usar `compactExpected`/`compactActual`? / R: Porque las variables locales deben tener nombres propios en lugar de desambiguarse con `this` [N4]. (Sección: Los cambios aplicados.)

P: ¿Cómo se separan las responsabilidades de formateo y compactado? / R: `formatCompactedComparison` hace todo el formateo y una nueva `compactExpectedAndActual` hace solo el compactado [G30]. (Sección: Los cambios aplicados.)

P: ¿Qué destapó la corrección de `suffixIndex` a `suffixLength` dentro de `compactString`? / R: Que los dos `if` ya no hacían nada funcional (uno casi un bug), por lo que se comentaron y, tras pasar los tests, se reestructuró como composición de fragmentos [G9]. (Sección: Acoplamiento temporal y aritmética de índices.)

P: ¿Por qué Martin revierte varias decisiones tomadas antes en el capítulo? / R: Porque el refactoring es iterativo y a menudo un refactoring lleva a otro que deshace el primero; por ejemplo, vuelve a inlinear métodos extraídos. (Sección: El resultado final.)

P: ¿Cuál es la conclusión sobre la calidad del código original? / R: No es que no estuviera limpio —los autores hicieron un trabajo excelente—, sino que ningún módulo es inmune a la mejora. (Sección: Conclusión.)

## Puntos a dominar

- Explicar qué es `ComparisonCompactor` y cómo expone diferencias entre strings (`<...B[X]D...>`).
- Reconocer la Regla del Boy Scout y cómo guía el refactoring del capítulo.
- Identificar los code smells aplicados: `f` redundante [N6], encapsular condicional [G28], nombres locales propios [N4], invertir negativo [G29], nombre preciso de función [N7], separar responsabilidades [G30], convenciones unificadas [G11], índices como nombres [N1].
- Entender el acoplamiento temporal [G31], por qué pasar `prefixIndex` resulta arbitrario [G32] y cómo lo resuelve `findCommonPrefixAndSuffix`.
- Explicar el origen de los `+1`: confusión base cero vs base uno (`suffixIndex` → `suffixLength`) [G33].
- Describir la partición final en funciones de análisis y de síntesis ordenadas topológicamente.
- Asumir que el refactoring es iterativo y que puede deshacer pasos previos.
