# The Data Science Handbook — Field Cady (Wiley, 2017)
## Capítulo 15 — Software Engineering Best Practices (Buenas prácticas de ingeniería de software)

> Nota de extracción: texto extraído de la capa de texto del PDF; las citas indican la página como (PDF p. N).

## Lo que necesitas saber

Cady sostiene que la habilidad que más falta a los data scientists es escribir código decente: no rutinas numéricas optimizadas ni librerías sofisticadas, sino mantener unos cientos de líneas claras y manejables durante un proyecto (PDF p. 217). Es una destreza aprendida que muchos genios de física o matemáticas nunca desarrollaron porque jamás escribieron más de unas docenas de líneas ni tuvieron que volver a su código a actualizarlo. El mensaje central del capítulo es que todo el que escribe código es responsable de que sea claro.

El otro motivo del capítulo es que, en la práctica, al data scientist se le pide mucho más que mantener su código legible. En algunas empresas se centran solo en analítica; en muchas otras les toca convertir scripts de un solo uso en paquetes de análisis reutilizables, o actuar como miembros junior de un equipo de ingeniería escribiendo código de producción que implementa sus ideas en un producto en tiempo real.

Sales sabiendo qué distingue el código de producción del código de análisis, los principios del buen estilo, cómo funciona el control de versiones con Git, los tipos de prueba (unitarias e integración), la filosofía de test-driven development (TDD) y las ideas básicas de la metodología AGILE.

## Estilo de código (Coding Style)

El estilo no trata de escribir rápido ni siquiera de que el código sea correcto (aunque a largo plazo habilita ambas cosas), sino de hacerlo fácil de leer y entender. Esto facilita que otros —sobre todo tu yo futuro, que ya olvidó cómo funciona— puedan comprenderlo, modificarlo y depurarlo. Suele costar un poco más escribir bien el código, pero casi siempre vale la pena.

Cady contrasta un fragmento bien escrito con el mismo código cometiendo "pecados" de estilo. Entre los errores que enumera (PDF p. 219):

- Nombres de variables sin significado.
- Hard-codear la URL en lugar de exponer el tema del artículo como parámetro propio.
- `Parser` como nombre de clase poco útil.
- Variables internas (`inp`, `lc`) creadas sobre la marcha en vez de declararse arriba con valores por defecto.
- Usar un `try–except` para comprobar si una variable ya existe: un uso perverso que confunde.
- Tres `if` mutuamente excluyentes que deberían haber sido `elif`.
- Indentación irregular.

El buen estilo no es un conjunto de reglas, sino una mentalidad: impaciencia ante el código difícil de leer, que solo se aprende leyendo y escribiendo mucho código. Aun así, da algunos principios básicos:

- Usar siempre nombres descriptivos para variables y funciones.
- Modularidad: dividir el programa en partes autocontenidas con funciones claras.
- Evitar indentación excesiva (bucles dentro de bucles); extraer las partes internas a funciones o subrutinas.
- Usar comentarios cuando corresponda (explicar lo extraño; un comentario inicial por archivo que diga qué hace).
- No abusar de los comentarios: distraen, pueden quedar desactualizados o ser erróneos; si el código habla por sí mismo, omítelos.
- Refactorizar en una sola rutina varios bloques que hacen cosas muy parecidas.
- Separar la información de "boilerplate" (como el formato de los datos) de la lógica central (p. ej., el orden de columnas de una tabla se especifica aparte del código).

La diferencia entre código de data science y código de producción, según Cady: el objetivo de la calidad general del código es que alguien pueda leerlo y entenderlo; el del código de producción es hacer innecesaria esa comprensión. El código de producción consiste sobre todo en crear APIs intuitivas, bien documentadas y flexibles para varios casos de uso: quien lo usa debería poder llamarlo como librería sin preocuparse de su funcionamiento interno. En cambio, con el código de análisis, es razonable esperar que quien quiera modificar tu script se arremangue y se meta en el propio código.

## Control de versiones y Git para data scientists

Un rasgo central del software de producción es un buen sistema de control de versiones: un marco que rastrea los cambios hechos a una base de código y los sincroniza con una copia maestra alojada en un servidor. Ventajas clave: si se destruye tu máquina, el código está respaldado; en equipo, todos sincronizan sus cambios leyéndolos del servidor; si algo se rompe, puedes volver a una versión anterior que funcionaba. Cuanto más grande y complejo el proyecto, más indispensables resultan.

Funciona descargando la base de código como un directorio en tu máquina; editas sus contenidos y luego pides al sistema que sincronice. Un sistema de control de versiones ofrece al menos: descargar la copia maestra ("checkout"/"clone"); refrescar el código local incorporando cambios posteriores ("pull"); escribir tus cambios de vuelta al servidor ("commit"/"push"); fusionar ("merge") cuando hay conflictos; adjuntar comentarios a cada commit; permitir que varios usuarios trabajen desde varias máquinas; llevar el historial de todos los cambios; y revertir conjuntos de cambios si algo se rompe.

Los sistemas modernos permiten crear ramas (branches) de toda la base de código. Si hay mucho trabajo por hacer, conviene bifurcar una rama nueva para trabajar sin contaminar la rama master y fusionar al final resolviendo conflictos. Las ramas también sirven para versiones puntuales con fines especiales (p. ej., un cliente que quiere una versión personalizada del producto).

El sistema más popular hoy es Git. Comandos esenciales (PDF p. 221-222):

```
git clone https://github.com/someproject.git   # clona la rama master del repo
git status                                      # qué archivos modificaste o añadiste
git add myfile.py                               # añade un archivo nuevo
git rm myfile.py                                # elimina un archivo
git mv dir1/file.py dir2/file.py                # mueve un archivo
git commit myfile.py -m "mensaje"               # prepara los cambios para el push
git push                                        # sube los commits a la copia maestra
git diff myfile.txt                             # muestra cambios aún no commiteados
git branch                                      # lista las ramas conocidas
git checkout my_branch                          # cambia a la rama my_branch
git branch my_new_branch                        # crea y usa una rama nueva
git merge other_branch                          # fusiona other_branch en la rama actual
```

Mención aparte para github.com, donde la copia maestra se aloja en los servidores de Github. Es gratuito si la base de código es pública (de ahí tantos proyectos interesantes); por una tarifa, mantiene repositorios privados, lo que da a empresas pequeñas control de versiones de primer nivel.

## Probar el código (Testing Code)

Hay un espectro de rigor en las pruebas: científicos y matemáticos suelen "probar" de forma casual con un par de sanity checks, mientras que los grandes proyectos dependen de frameworks de pruebas que a veces son tan complejos como el propio código fuente. El data science tiende a lo primero, pero en la práctica abarca todo el rango. La ventaja obvia de las pruebas es comprobar que el código es correcto; una menos obvia es que el código de prueba suele ser la mejor documentación: muestra cómo llamar al código, qué entra y qué sale, y basta ejecutarlo para verificar que esa "documentación" está al día.

### Pruebas unitarias (Unit Tests)

Cubren piezas pequeñas y autocontenidas de lógica. Para un trozo de código, sus pruebas unitarias deberían cubrir todos los casos límite conocidos más varios casos generales. Muchos lenguajes tienen librerías dedicadas. Ejemplo mínimo con `unittest` de Python, sobre una función `fib` que calcula el n-ésimo número de Fibonacci (PDF p. 223):

```python
import unittest
from mymath import fib

class TestFibonacci(unittest.TestCase):
  def test0(self):  self.assertEqual(0, fib(0))
  def test1(self):  self.assertEqual(1, fib(1))
  def test2(self):  self.assertEqual(fib(0)+fib(1), fib(2))
  def test10(self): self.assertEqual(fib(8)+fib(9), fib(10))

unittest.main()
```

Se crea una clase que hereda de `TestCase`; cada prueba es un método cuyo nombre empieza por `test` y usa `assertEqual`, que registra los fallos. `main()` busca todos los test cases del namespace, los ejecuta e informa. Otros métodos de `TestCase`: `assertNotEqual`, `assertTrue`, `assertFalse` y `assertRaises` (comprueba que una llamada lanza un error).

La aplicación más útil es el mantenimiento a largo plazo: ante un fallo, conservas las pruebas antiguas y añades una para el nuevo caso límite; cuando la nueva pasa y las anteriores siguen pasando, confías en que arreglaste el problema sin romper nada. También ayuda en equipo con Git: tras un `git pull` de los cambios ajenos, recompilas y relanzas las pruebas; si pasan, haces push con confianza. Cady ve el código fuente y el de prueba como dos mitades simbióticas "en sync" cuando todas las pruebas pasan: que ambas tengan un bug y se cancelen es minúsculamente improbable.

La limitación clave: cada módulo se prueba aislado. Las pruebas unitarias no están pensadas para código que accede a recursos externos (Internet, un MySQL remoto, otros procesos). Para eso se usa un "mock": un objeto que imita esa API de forma predefinida (p. ej., un mock de MySQL que recibe queries y devuelve siempre un resultado fijo sin acceder al servidor). Acceder a recursos externos reales desde las pruebas es mala práctica, porque pueden fallar por motivos ajenos al código; aunque para pruebas manuales propias a veces es más fácil que crear mocks.

### Pruebas de integración (Integration Tests)

Los módulos se enlazan entre sí, se ponen en su sitio los recursos externos y el sistema se ejecuta de forma realista. Aquí aparecen timeouts de red, fallos de permisos, desbordamientos de memoria y otros errores que solo surgen a escala; es también la prueba de fuego de si cada módulo entiende la API de los demás. No suele haber una librería estándar porque es muy específica de cada proyecto: es más bien una etapa del desarrollo de un software serio.

## Desarrollo guiado por pruebas (Test-Driven Development)

TDD lleva al extremo la idea de usar pruebas para no romper lo que ya funciona: escribes las pruebas unitarias del módulo antes de empezar el código fuente, y tu objetivo al programar es solo hacer que todas pasen, abordándolas de una en una sin romper las anteriores e ignorando las que aún no tocas.

Dos grandes ventajas: (1) te obliga a pensar de antemano la funcionalidad deseada, a decidir una API preliminar y a escribir código que la llame para ver si resulta torpe de usar; (2) al escribir el código fuente puedes concentrarte en una sola prueba en vez de sostener todo el sistema en la cabeza, lo que resulta casi meditativo.

TDD solo es apropiado si sabes más o menos qué debe hacer tu software, lo que a menudo no ocurre en data science, donde no sabes qué extracciones de features y preprocesamiento funcionarán hasta jugar con los datos. En la experiencia de Cady, el data science sirve para averiguar qué análisis hacer y cómo, y luego se usa TDD para implementar la versión de producción. Otro problema: su miopía no siempre es práctica; cuanto más interactúan los módulos, más importa planificar la arquitectura de antemano, o cada nueva prueba puede obligar a rehacer casi toda la base de código.

## Metodología AGILE

Si TDD es cómo trabaja el programador individual, AGILE es cómo se organizan los equipos de desarrolladores. El término se acuñó en 2001 en "The Manifesto for Agile Software Development", escrito por programadores hartos de que los planes de arriba abajo y a largo plazo terminaran en proyectos fallidos. Alguna variante de agile es hoy omnipresente en data science y software.

La idea clave es hacer los proyectos más flexibles acortando el ciclo de desarrollo y estrechando los bucles de feedback. Principios destacados:

- Colaboración y toma de decisiones frecuentes por los propios miembros del equipo, en vez de mandatos desde arriba.
- Comunicación igualmente frecuente con clientes y stakeholders.
- Asegurar que siempre haya un producto funcional de extremo a extremo, aunque no incluya todas las features finales.

Rasgo típico: una reunión matinal diaria ("stand-up" o "scrum") donde cada miembro dice (1) qué logró ayer, (2) qué planea hacer hoy y (3) qué obstáculos tiene. Agile no está exento de inconvenientes: puede ir en detrimento de la planificación a largo plazo y la dirección clara, y el foco en iterar features rápido suele acumular "technical debt" (desorganización e inestabilidades que vuelven a morderte después).

## Ideas clave

- La habilidad más escasa en data scientists es escribir código claro y mantenible; todo el que escribe código es responsable de su claridad.
- El buen estilo es una mentalidad (nombres descriptivos, modularidad, poca indentación, comentarios justos, refactorizar duplicados, separar boilerplate de la lógica).
- Código de producción ≠ código de análisis: el primero crea APIs intuitivas que hacen innecesario entender el interior; el segundo espera que quien lo modifique se meta en el código.
- El control de versiones (Git) respalda el código, sincroniza equipos, permite volver atrás y trabajar en ramas; Github aloja la copia maestra, gratis si es pública.
- Las pruebas unitarias cubren piezas aisladas y sus casos límite; para recursos externos se usan mocks, no accesos reales.
- Las pruebas de integración enlazan módulos y recursos reales para detectar errores que solo surgen a escala.
- TDD escribe primero las pruebas y luego el código; útil para implementar versiones de producción, menos para la exploración inicial de datos.
- AGILE organiza equipos con ciclos cortos, feedback frecuente, un producto siempre funcional y stand-ups diarios, a costa de posible technical debt.
