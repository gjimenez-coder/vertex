# Refactoring: Improving the Design of Existing Code — Martin Fowler (con Kent Beck, John Brant, William Opdyke y Don Roberts) (Addison-Wesley, 1999)
## Capítulo 14 — Refactoring Tools (Herramientas de refactorización)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas usan la página del PDF `(PDF p. N)`.

## Lo que necesitas saber

Este capítulo, escrito por Don Roberts y John Brant, defiende que uno de los mayores obstáculos a la refactorización ha sido la falta de soporte de herramientas. En lenguajes donde la refactorización forma parte de la cultura, como Smalltalk, existen entornos potentes que la apoyan; aun así, hasta hace poco el proceso estaba solo parcialmente soportado y la mayor parte del trabajo se hacía a mano.

La tesis central es que refactorizar con soporte automático de herramientas se siente distinto de hacerlo manualmente: al abaratar tanto la refactorización como ajustar el formato del código, la limpieza puede hacerse de forma similar, con efectos positivos profundos en la mantenibilidad, reutilización y comprensibilidad. Sales sabiendo cómo cambia la práctica de programar con estas herramientas y cuáles son los criterios técnicos y prácticos que una herramienta de refactorización debe cumplir para tener éxito.

Los autores subrayan que, aunque incluyen criterios técnicos, consideran los criterios prácticos mucho más importantes: una herramienta se crea para apoyar a una persona en una tarea, y si no encaja con su forma de trabajar, no se usará.

## Refactoring with a Tool (Refactorizar con una herramienta)

Incluso con una batería de pruebas como red de seguridad, refactorizar a mano consume mucho tiempo, y ese coste impide que los programadores hagan refactorizaciones que saben que deberían hacer. Kent Beck relata su experiencia con el Refactoring Browser: cambia por completo la forma de pensar la programación, porque pensamientos como «debería cambiar este nombre, pero…» desaparecen al existir siempre una opción de menú para hacerlo.

Beck cuenta que al empezar dedicó unas dos horas a refactorizar a su ritmo antiguo: hacía una refactorización y luego se quedaba mirando al vacío los cinco minutos que le habría costado hacerla a mano. Tuvo que aprender a pensar refactorizaciones más grandes y más rápido; ahora usa probablemente mitad refactorización y mitad código nuevo, todo a la misma velocidad.

Con este nivel de soporte, refactorizar deja de ser una actividad separada de programar. Como no hay que probar tras las refactorizaciones automáticas, las actividades fluyen entre sí y el cambio de sombrero se hace mucho menos evidente, aunque siga ocurriendo.

El capítulo usa **Extract Method** como ejemplo: al hacerlo a mano hay muchas cosas que comprobar. Con el Refactoring Browser basta con seleccionar el texto y elegir la opción de menú Extract Method. La herramienta determina si la selección es legal (puede contener solo parte de un identificador, o asignaciones a una variable sin todas sus referencias), calcula cuántos parámetros hay que pasar, pide un nombre y permite especificar el orden de los parámetros. Luego extrae el código, lo reemplaza por una llamada y crea el nuevo método en la misma clase. Todo el proceso dura unos 15 segundos.

A medida que refactorizar se abarata, los errores de diseño cuestan menos y se necesita menos diseño por adelantado. El diseño inicial es una actividad predictiva porque los requisitos están incompletos. Con herramientas automáticas, el diseño puede ser más fluido: se diseña al nivel del problema actual sabiendo que se puede extender después sin predecir cada cambio futuro. Si los *smells* del Capítulo 3 aparecen, se cambia el diseño rápidamente.

La refactorización asistida también afecta a las pruebas: se prueba menos porque muchas refactorizaciones se hacen automáticamente, aunque siempre habrá refactorizaciones no automatizables, por lo que el paso de pruebas nunca se elimina. La observación empírica es que las pruebas se ejecutan el mismo número de veces al día, pero se refactoriza más.

## Technical Criteria (Criterios técnicos)

El propósito principal de una herramienta de refactorización es permitir refactorizar sin tener que volver a probar el programa. Para transformar un programa preservando su comportamiento se necesitan varios requisitos técnicos.

- **Program Database (base de datos del programa)**: capacidad de buscar entidades del programa en todo el código (por ejemplo, todas las llamadas que pueden referirse a un método, o los métodos que leen o escriben una variable de instancia). En entornos integrados como Smalltalk esta información se mantiene de forma buscable gracias a la compilación dinámica: al cambiar una clase, se compila a bytecodes y la «base de datos» se actualiza. En entornos más estáticos como Java, el código se escribe en archivos de texto y la actualización requiere procesarlos, similar a compilar. Entornos como IBM VisualAge for Java imitan la actualización dinámica de Smalltalk. Un enfoque ingenuo con herramientas textuales como `grep` falla pronto porque no distingue una variable `foo` de una función `foo`; crear la base de datos requiere análisis semántico (parsing) para determinar la «parte del discurso» de cada token, tanto a nivel de definición de clase como de método.

- **Parse Trees (árboles de análisis)**: la mayoría de las refactorizaciones manipulan partes del sistema por debajo del nivel de método. Al renombrar una variable de instancia hay que actualizar todas las referencias en la clase y sus subclases; otras refactorizaciones (como extraer parte de un método) operan por debajo del método. Manipular la estructura de un método requiere árboles de análisis, estructuras de datos que representan la estructura interna del método. Ejemplo:

  ```java
  public void hello() {
    System.out.println("Hello World");
  }
  ```

  Su árbol de análisis corresponde a la Figura 14.1.

- **Accuracy (precisión)**: las refactorizaciones deben preservar razonablemente el comportamiento. La preservación total es imposible: por ejemplo, un cambio de unos milisegundos puede romper un programa con restricciones de tiempo real estricto. También puede romperse un programa que construye un string y usa la Java Reflection API para ejecutar el método nombrado por el string, pues renombrar el método lanzaría una excepción. Aun así, las refactorizaciones pueden ser razonablemente precisas para la mayoría; mientras se identifiquen los casos que las rompen, el programador puede evitarlas o corregir a mano lo que la herramienta no pueda.

## Practical Criteria (Criterios prácticos)

Los criterios más importantes son los que integran la refactorización con otras herramientas.

- **Speed (velocidad)**: el análisis y las transformaciones pueden ser costosos si son muy sofisticados. Siempre hay que sopesar tiempo frente a precisión; si una refactorización tarda demasiado, el programador la hará a mano. Al desarrollar el Refactoring Browser dejaron sin implementar algunas refactorizaciones por no poder hacerlas seguras en un tiempo razonable. Los informáticos tienden a fijarse en los casos límite, pero la mayoría de los programas no lo son, y enfoques más simples y rápidos funcionan asombrosamente bien. Si un análisis es demasiado lento, una opción es pedir la información al programador: no es demostrablemente seguro, pero traslada la responsabilidad a quien, a menudo, ya conoce ese dato, y paradójicamente aumenta el uso de la herramienta.

- **Undo (deshacer)**: la refactorización automática permite un enfoque exploratorio del diseño; como una refactorización preserva el comportamiento, su inversa también es una refactorización y lo preserva. Las primeras versiones del Refactoring Browser no tenían deshacer, lo que hacía todo más tentativo y a veces obligaba a recuperar una versión antigua. Con deshacer se puede explorar sin miedo, crear clases, mover métodos para ver cómo queda el código y cambiar de rumbo, todo muy rápido.

- **Integrated with Tools (integración con herramientas)**: el IDE integra editor, compilador, enlazador, depurador y demás. Una implementación temprana del Refactoring Browser para Smalltalk era una herramienta separada y nadie la usaba, ni siquiera sus autores. Al integrar las refactorizaciones directamente en el Smalltalk Browser, pasaron a usarlas intensamente: tenerlas a mano marcó la diferencia.

## Wrap Up (Cierre)

Tras años desarrollando y usando el Refactoring Browser —incluso para refactorizar su propio código—, los autores atribuyen su éxito a que, siendo programadores, intentaron que encajara con su forma de trabajar: implementaban refactorizaciones manuales que resultaban generales, aceleraban lo lento y mejoraban lo poco preciso. Creen que las herramientas automáticas de refactorización son la mejor forma de gestionar la complejidad que surge al evolucionar un proyecto; sin ellas el software se vuelve inflado, con errores y frágil. Como Java es mucho más simple que el lenguaje con el que comparte sintaxis, es más fácil desarrollar herramientas para refactorizarlo, y esperan evitar «los pecados de C++».

## Ideas clave

- El mayor freno a la refactorización ha sido la falta de soporte de herramientas; Smalltalk es la excepción cultural.
- Con soporte automático, refactorizar deja de ser una actividad separada de programar y las pruebas posteriores dejan de ser necesarias en las refactorizaciones automatizadas.
- Extract Method con el Refactoring Browser tarda unos 15 segundos y valida automáticamente si la selección es legal.
- Abaratar la refactorización reduce el coste de los errores de diseño y permite diseñar para el problema actual, no para cada cambio futuro.
- Criterios técnicos: base de datos del programa (vía análisis semántico, no `grep`), árboles de análisis y precisión razonable (no total).
- Criterios prácticos (más importantes): velocidad, deshacer e integración en el IDE.
- Pedir información al programador puede sustituir un análisis lento y, paradójicamente, aumenta el uso de la herramienta.
- Una herramienta de refactorización separada del entorno no se usa; integrarla en el IDE fue decisivo.
