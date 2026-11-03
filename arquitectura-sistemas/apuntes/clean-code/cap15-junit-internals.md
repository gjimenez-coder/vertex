# Clean Code: A Handbook of Agile Software Craftsmanship — Robert C. Martin (Prentice Hall, 2008)
## Capítulo 15 — JUnit Internals (Interioridades de JUnit)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas usan la página del PDF `(PDF p. N)`.

## Lo que necesitas saber

Este capítulo aplica una crítica de código real a un fragmento del propio framework JUnit. Martin lo describe como «simple en concepción, preciso en definición y elegante en implementación» (PDF p. 282), y lo usa como banco de pruebas para demostrar el refactoring incremental guiado por la Regla del Boy Scout: dejar el código un poco más limpio de como se encontró.

El módulo elegido es `ComparisonCompactor`, un trozo ingenioso que ayuda a identificar errores de comparación de strings. Dados dos strings que difieren, como `ABCDE` y `ABXDE`, expone la diferencia generando un string como `<...B[X]D...>`. La tesis central no es que el código original esté mal —los autores hicieron un trabajo excelente—, sino que ningún módulo es inmune a la mejora y que cada quien tiene la responsabilidad de dejar el código mejor de como lo encontró.

Sales sabiendo cómo se encadena una serie de pequeñas transformaciones (renombrar, encapsular condicionales, eliminar acoplamiento temporal, simplificar aritmética de índices) hasta converger en un diseño claramente particionado. También sales viendo que el refactoring es un proceso iterativo de ensayo y error en el que a veces una decisión posterior deshace una anterior.

## El ejemplo que recorre el capítulo

`ComparisonCompactor` nace de Kent Beck y Erich Gamma escribiendo JUnit en tres horas durante un vuelo a Atlanta (PDF p. 283). El capítulo parte del Listado 15-1 (la suite de tests `ComparisonCompactorTest`) y del Listado 15-2 (el código original), señala que un análisis de cobertura da 100% con esos tests, y refactoriza paso a paso hasta el Listado 15-5 (versión final). El Listado 15-3 muestra, por contraste, una versión «defactored» (deteriorada) con nombres como `ctxt`, `s1`, `s2`, `pfx`, `sfx` para ilustrar en qué podría haber degenerado.

## El framework JUnit y el punto de partida

Los tests describen el comportamiento mejor que la prosa: casos como `compact("a")` con `ComparisonCompactor(0, "b", "c")` producen `a expected:<[b]> but was:<[c]>`. El código original ya está «bien particionado, razonablemente expresivo y simple» (PDF p. 285), aunque con expresiones largas y varios `+1` extraños. Martin invita a «quitar las pelusas» (pick the nits) una por una.

## Los cambios aplicados

Cada mejora se anota con las referencias a la lista de code smells del libro (N, G):

- Eliminar el prefijo `f` de las variables miembro: hoy es una codificación de ámbito redundante [N6]. `fExpected` pasa a `expected`, etc.
- Encapsular el condicional inicial de `compact` en un método que explique la intención [G28]: `shouldNotCompact()`.
- Deshacer la notación `this.expected`/`this.actual`: las variables locales deben tener nombres propios como `compactExpected` y `compactActual` [N4].
- Invertir el sentido del condicional negativo porque los negativos cuestan más de leer [G29]: `canBeCompacted()`.
- Renombrar la función: `compact` oculta un efecto (puede no compactar) y además formatea; el nombre correcto es `formatCompactedComparison` [N7].
- Separar responsabilidades: `formatCompactedComparison` hace todo el formateo y una nueva `compactExpectedAndActual` hace solo el compactado [G30].
- Unificar convenciones: hacer que `findCommonPrefix`/`findCommonSuffix` devuelvan sus valores en lugar de mezclar estilos [G11], y renombrar las variables miembro para reflejar que son índices [N1].

## Acoplamiento temporal y aritmética de índices

Una inspección cuidadosa revela un acoplamiento temporal oculto [G31]: `findCommonSuffix` depende de que `prefixIndex` ya se haya calculado en `findCommonPrefix`. Pasar `prefixIndex` como argumento expone la dependencia, pero resulta arbitrario [G32]. La solución elegida es fusionar en `findCommonPrefixAndSuffix`, que llama internamente a `findCommonPrefix` primero, haciendo el orden evidente de forma dramática.

Al limpiar esa función aparece el verdadero origen de los `+1`: `suffixIndex` no era base cero sino base uno, por lo que no era una longitud real [G33]. Al corregirlo (renombrando a `suffixLength`, con `-1` en `charFromEnd` y `<=` en `suffixOverlapsPrefix`) el código se vuelve legible. El ajuste destapa que los dos `if` dentro de `compactString` ya no hacían nada funcional (uno era de hecho casi un bug, porque `suffixIndex` nunca podía ser menor que uno). Comentarlos y correr los tests: pasan. Así se reestructura `compactString` a una simple composición de fragmentos [G9].

## El resultado final

El Listado 15-5 queda «bastante bonito» (PDF p. 296): el módulo se separa en un grupo de funciones de análisis (`findCommonPrefix`, `findCommonPrefixAndSuffix`, `charFromEnd`, `suffixOverlapsPrefix`) y otro de síntesis (`compact`, `startingEllipsis`, `startingContext`, `delta`, `endingContext`, `endingEllipsis`), ordenadas topológicamente de modo que cada función aparece justo después de su primer uso. Martin señala que revirtió varias decisiones tomadas antes en el capítulo —por ejemplo, volvió a inlinear métodos extraídos y cambió el sentido de `shouldNotBeCompacted`—, lo cual es típico: a menudo un refactoring lleva a otro que deshace el primero.

## Conclusión

Se cumple la Regla del Boy Scout: el módulo quedó un poco más limpio de como se encontró. No es que no estuviera ya limpio —los autores hicieron un trabajo excelente—, sino que ningún módulo es inmune a la mejora y todos tenemos la responsabilidad de dejar el código algo mejor de lo que estaba.

## Ideas clave

- El refactoring es iterativo: ensayo y error que converge en algo digno de un profesional, incluso deshaciendo pasos previos.
- Encapsular condicionales en métodos con nombre revela la intención; invertir negativos mejora la lectura.
- Los nombres deben ser precisos: una función que puede no compactar y que además formatea no debe llamarse `compact`.
- El acoplamiento temporal debe hacerse visible estructuralmente (una función llama a la otra), no esconderse.
- Nombres erróneos de variables (`suffixIndex` vs `suffixLength`) delatan aritmética confusa como los `+1` dispersos.
- Correr los tests tras cada cambio permite eliminar código muerto con confianza (cobertura 100%).
- Un buen módulo se particiona en funciones de análisis y de síntesis, ordenadas topológicamente.
- La Regla del Boy Scout: deja el código un poco más limpio de como lo encontraste, aunque ya estuviera bien.
