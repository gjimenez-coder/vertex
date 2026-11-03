# Code Simplicity: The Fundamentals of Software — Max Kanat-Alexander (O'Reilly Media, 2012)
## Capítulo 5 — Change (Cambio)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas usan la página del PDF `(PDF p. N)`.

## Lo que necesitas saber

El capítulo parte de una certeza sobre el futuro: aunque no podamos predecir qué cambiará, sí sabemos que el entorno de nuestro software cambiará con el tiempo y que el software tendrá que adaptarse. De ahí surge la **Ley del Cambio**: cuanto más tiempo exista tu programa, más probable es que cualquier parte de él tenga que cambiar. Hacia un futuro infinito, la probabilidad de que cada línea cambie tiende al 100%.

La conclusión práctica no es intentar adivinar qué cambiará, sino escribir software tan flexible como sea razonablemente posible para adaptarse a cualquier cambio que llegue. El capítulo respalda esta ley con datos reales de evolución de archivos, identifica los tres errores habituales al enfrentar el cambio y propone el desarrollo y diseño incrementales como método que, por su propia naturaleza, evita esos errores.

Sales sabiendo tres reglas concretas: no escribir código antes de necesitarlo (y eliminar el que no se usa), diseñar según lo que sabes ahora y no según predicciones del futuro, y ser solo tan genérico como sepas que necesitas ser ahora mismo.

## Change in a Real-World Program (El cambio en un programa real)

Se analizan cuatro archivos de un programa real para ilustrar cuánto cambia el software con el tiempo (PDF p. 42).

| | Archivo 1 | Archivo 2 | Archivo 3 | Archivo 4 |
|---|---|---|---|---|
| Periodo analizado | 5 a 2 m | 8 a 3 m | 13 a 3 m | 13 a 4 m |
| Líneas originales | 423 | 192 | 227 | 309 |
| Líneas sin cambios | 271 | 101 | 4 | 8 |
| Líneas ahora | 664 | 948 | 388 | 414 |
| Veces cambiado | 47 | 99 | 194 | 459 |
| Cambios totales | 675 | 1,709 | 3,047 | 11,107 |
| Ratio de cambio | 1.6x | 8.9x | 13x | 36x |

Observaciones relevantes:
- Según el ratio de cambio, se invirtió más trabajo en cambiar cada archivo que en escribirlo originalmente (el archivo 4 tuvo 36 veces más cambios totales que líneas originales).
- Las líneas sin cambios son pocas; casi siempre son comentarios, documentación o líneas vacías.
- Puede haber mucho cambio aunque el archivo crezca poco: el archivo 3 creció solo 161 líneas en 13 años pero acumuló 3,047 cambios totales.
- El total de cambios siempre supera a las líneas actuales: es más probable haber cambiado una línea que tenerla una vez que el archivo lleva tiempo existiendo.
- En el archivo 3, las líneas modificadas superan a originales más añadidas: algunas líneas se cambiaron una y otra vez, algo común en proyectos de larga vida.

El autor recomienda revisar el historial de cambios de un archivo antiguo y preguntarse si cada cambio podría haberse previsto o si el archivo podría haberse escrito mejor originalmente para simplificar esos cambios (PDF p. 44).

## The Three Flaws (Los tres errores)

Tres errores amplios al afrontar la Ley del Cambio, por orden de frecuencia:
1. Escribir código que no se necesita.
2. No hacer el código fácil de cambiar.
3. Ser demasiado genérico.

### Writing Code That Isn't Needed (Escribir código innecesario)

Se apoya en la regla **YAGNI** ("You Ain't Gonna Need It"): no escribas código antes de necesitarlo. El autor matiza que el nombre es engañoso: quizá sí lo necesites en el futuro, pero como no puedes predecirlo, no sabes cómo debe funcionar; si lo escribes antes, tendrás que rediseñarlo. El código no usado además sufre "bit rot", desincronizándose y generando bugs silenciosos. La regla ampliada:

> No escribas código hasta que realmente lo necesites, y elimina cualquier código que no se esté usando. (PDF p. 44)

Ejemplo real ("Max"): en unos drop-downs guardó, además de la lista de valores, un campo "active" cuyo código nunca llegó a escribirse. Durante años el dato confundió a clientes y desarrolladores, provocó bugs, un desarrollador asumió erróneamente que estaba en uso, y cuando por fin alguien implementó la función tuvo que rediseñarlo. Resultado: bugs, confusión y trabajo extra.

### Not Making the Code Easy to Change (No hacer el código fácil de cambiar)

El "diseño rígido" mata proyectos. Surge de dos formas: hacer demasiadas suposiciones sobre el futuro, o escribir código sin suficiente diseño.

- **Demasiadas suposiciones:** el hospital de veteranos pasó un año escribiendo un documento con todas las decisiones de "The Healthcare System", tres años implementándolo según ese documento contradictorio e incompleto, y al entregarlo los usuarios querían algo completamente distinto. El sistema rígido no podía cambiarse sin meses o años. La alternativa: especificar una o pocas funciones, implementarlas de inmediato y entrar en un ciclo de comunicación y pruebas con usuarios.
- **Código sin suficiente diseño:** un gestor de tareas con un campo "Status" (y 10 campos similares con reglas propias) se implementó como un único archivo de 3,000 líneas sin estructura, con validaciones específicas y código copiado-pegado. El nuevo mantenedor no podía cambiar una parte sin tocar muchas otras; el archivo llegó a 5,000 líneas y no admitía funciones nuevas (p. ej., actualizar tareas por email). Dos desarrolladores necesitaron un año de rediseño (caso real: `process_bug.cgi` de Bugzilla).

Regla contra el diseño rígido:

> El código debe diseñarse según lo que sabes ahora, no según lo que crees que pasará en el futuro. (PDF p. 48)

Diseña solo para tus requisitos inmediatos y conocidos, sin excluir futuros requisitos. Mantener los cambios pequeños ayuda a aplicar diseño real en cada uno. Planificar no es malo; basta con mantener los cambios pequeños y el código adaptable.

### Being Too Generic (Ser demasiado genérico)

Diseñar una solución tan genérica que (se cree) cubrirá toda situación futura es "overengineering": diseñar o construir demasiado para la situación. La imagen del autor: construir un láser orbital para destruir un hormiguero. Problemas:
1. No puedes predecir el futuro, así que ninguna solución genérica será suficientemente genérica para los requisitos reales que llegarán.
2. El código demasiado genérico maneja mal los casos específicos: si todo son "bytes", el error es "pasaste bytes incorrectos" en vez de "pasaste una imagen incorrecta".
3. Ser demasiado genérico implica escribir código innecesario, lo que lleva de vuelta al primer error.

Regla:

> Sé solo tan genérico como sepas que necesitas ser ahora mismo. (PDF p. 49)

Ejemplo real: para enviar varios cientos de emails en segundo plano con el "Email Sender" existente, un desarrollador escribió cientos de líneas para que los clientes pudieran "enchufar" otros sistemas, sin que nadie lo hubiera pedido. El arquitecto jefe eliminó ese código por falta de evidencia de que se necesitara; cuatro años después, ningún cliente lo había necesitado.

## Incremental Development and Design (Desarrollo y diseño incrementales)

Método que evita los tres errores por naturaleza: diseñar y construir el sistema pieza por pieza, en orden. Ejemplo con una calculadora (suma, resta, multiplicación, división):
1. Planificar un sistema que solo sume.
2. Implementarlo.
3. Ajustar el diseño para facilitar la resta; implementarla.
4. Ajustar el diseño para la multiplicación; implementarla.
5. Ajustar el diseño para la división (que ya costará poco); implementarla.

Lo difícil es decidir el orden: elegir en cada paso lo más simple de trabajar. Se eligió la suma por ser la más simple y la resta después porque se apoya en ella; la división se dejó al final porque saltar de la suma a la división es demasiado complejo, mientras que de la multiplicación a la división es sencillo. A veces hay que dividir una función en pasos pequeños y lógicos.

Combina dos métodos: **desarrollo incremental** (construir el sistema en pequeñas piezas, los pasos "Implementar") y **diseño incremental** (crear y mejorar el diseño en incrementos, los pasos "Planificar" y "Ajustar el diseño"). No es el único método válido, pero sí uno que previene los tres errores.

## Ideas clave

- Ley del Cambio: cuanto más vive un programa, más probable es que cualquier parte deba cambiar; no predigas qué cambiará, hazlo flexible.
- Los datos reales muestran que suele invertirse más trabajo en cambiar un archivo que en escribirlo (ratios de hasta 36x).
- Tres errores frente al cambio: escribir código innecesario, no hacerlo fácil de cambiar y ser demasiado genérico.
- YAGNI ampliado: no escribas código hasta necesitarlo y elimina el que no se use; el código no usado sufre "bit rot".
- El diseño rígido nace de demasiadas suposiciones sobre el futuro o de código sin suficiente diseño.
- Diseña según lo que sabes ahora, no según predicciones; mantén los cambios pequeños.
- Sé solo tan genérico como sepas que necesitas ser ahora; el overengineering complica en vez de simplificar.
- El desarrollo y diseño incrementales (construir y rediseñar pieza por pieza, en orden de simplicidad) evita los tres errores.
