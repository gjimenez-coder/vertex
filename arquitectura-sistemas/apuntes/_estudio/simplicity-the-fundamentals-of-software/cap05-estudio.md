# Change (Cambio) — Estudio

## Tarjetas de repaso

P: ¿Qué afirma la Ley del Cambio? / R: Cuanto más tiempo exista tu programa, más probable es que cualquier parte de él tenga que cambiar; hacia un futuro infinito la probabilidad de que cada línea cambie tiende al 100%.

P: ¿Cuál es la conclusión práctica de la Ley del Cambio? / R: No intentar adivinar qué cambiará, sino escribir software tan flexible como sea razonablemente posible para adaptarse a cualquier cambio.

P: ¿Qué muestran los datos de los cuatro archivos reales? / R: Que suele invertirse más trabajo en cambiar un archivo que en escribirlo originalmente, con ratios de cambio de hasta 36x.

P: ¿Qué tipo de líneas suelen quedar sin cambios en un archivo antiguo? / R: Casi siempre comentarios, documentación o líneas vacías.

P: ¿Cuáles son los tres errores al afrontar la Ley del Cambio? / R: Escribir código que no se necesita, no hacer el código fácil de cambiar y ser demasiado genérico.

P: ¿Qué significa YAGNI y cómo lo amplía el autor? / R: "You Ain't Gonna Need It": no escribas código hasta que realmente lo necesites, y elimina cualquier código que no se esté usando.

P: ¿Qué es el "bit rot"? / R: El código no usado se desincroniza con el resto con el tiempo y genera bugs silenciosos.

P: ¿De qué dos formas surge el "diseño rígido"? / R: De hacer demasiadas suposiciones sobre el futuro, o de escribir código sin suficiente diseño.

P: ¿Cuál es la regla contra el diseño rígido? / R: El código debe diseñarse según lo que sabes ahora, no según lo que crees que pasará en el futuro.

P: ¿Qué es el "overengineering"? / R: Diseñar o construir demasiado para la situación; la imagen del autor es construir un láser orbital para destruir un hormiguero.

P: ¿Cuál es la regla contra ser demasiado genérico? / R: Sé solo tan genérico como sepas que necesitas ser ahora mismo.

P: ¿Por qué el código demasiado genérico maneja mal los casos específicos? / R: Porque pierde el contexto: si todo son "bytes", el error es "pasaste bytes incorrectos" en vez de "pasaste una imagen incorrecta".

P: ¿Qué es el desarrollo y diseño incrementales? / R: Diseñar y construir el sistema pieza por pieza, en orden, eligiendo en cada paso lo más simple de trabajar; evita los tres errores por naturaleza.

P: ¿Qué combina el método incremental? / R: Desarrollo incremental (construir en pequeñas piezas, los pasos "Implementar") y diseño incremental (crear y mejorar el diseño en incrementos, los pasos "Planificar" y "Ajustar el diseño").

P: En el ejemplo de la calculadora, ¿por qué se deja la división al final? / R: Porque saltar de la suma a la división es demasiado complejo, mientras que de la multiplicación a la división es sencillo.

## Preguntas de autoevaluación

P: ¿Por qué no sirve de nada intentar predecir qué parte concreta del software cambiará? / R: Porque no podemos predecir el futuro; solo sabemos que el entorno cambiará, así que lo útil es hacer el software flexible, no adivinar. (Lo que necesitas saber)

P: Según los datos reales, ¿qué relación hay entre los cambios totales y las líneas actuales de un archivo antiguo? / R: El total de cambios siempre supera a las líneas actuales: una vez que el archivo lleva tiempo, es más probable haber cambiado una línea que tenerla. (Change in a Real-World Program)

P: ¿Qué enseña el caso del campo "active" en los drop-downs de "Max"? / R: Que escribir código/datos antes de necesitarlos provoca bugs, confusión en clientes y desarrolladores, y trabajo extra de rediseño cuando por fin se implementa. (Writing Code That Isn't Needed)

P: ¿Qué diferencia hubo entre el proyecto "The Healthcare System" y la alternativa que propone el autor? / R: El hospital escribió un documento exhaustivo y lo implementó durante años, entregando algo que nadie quería y que no se podía cambiar; la alternativa es especificar pocas funciones, implementarlas de inmediato y entrar en un ciclo de comunicación y pruebas con usuarios. (Not Making the Code Easy to Change)

P: ¿Qué problema ilustra el gestor de tareas con el campo "Status" (process_bug.cgi)? / R: El código sin suficiente diseño (un archivo de miles de líneas, validaciones específicas y copia-pega) impide cambiar una parte sin tocar muchas otras y bloquea funciones nuevas, exigiendo un año de rediseño. (Not Making the Code Easy to Change)

P: ¿Por qué ser demasiado genérico lleva de vuelta al primer error? / R: Porque implica escribir código innecesario, que es precisamente el primer error (escribir código que no se necesita). (Being Too Generic)

P: ¿Qué pasó con el código genérico añadido al "Email Sender"? / R: Se escribieron cientos de líneas para "enchufar" otros sistemas sin que nadie lo pidiera; el arquitecto jefe las eliminó por falta de evidencia y cuatro años después ningún cliente las había necesitado. (Being Too Generic)

P: ¿Cuál es la parte más difícil del desarrollo incremental y cómo se resuelve? / R: Decidir el orden; se resuelve eligiendo en cada paso lo más simple de trabajar y, si hace falta, dividiendo una función en pasos pequeños y lógicos. (Incremental Development and Design)

## Puntos a dominar

- Enunciar la Ley del Cambio y su consecuencia práctica: flexibilidad en vez de predicción.
- Interpretar la tabla de los cuatro archivos: ratio de cambio, líneas sin cambios, crecimiento frente a número de cambios.
- Nombrar los tres errores en orden de frecuencia y reconocer un ejemplo de cada uno.
- Aplicar YAGNI ampliado: no escribir código hasta necesitarlo y eliminar el que no se usa.
- Distinguir las dos causas del diseño rígido (demasiadas suposiciones vs. falta de diseño).
- Recitar las tres reglas: diseñar según lo que sabes ahora, mantener los cambios pequeños, y ser solo tan genérico como sepas que necesitas ser ahora.
- Explicar por qué el overengineering complica en lugar de simplificar.
- Describir el desarrollo y diseño incrementales con el ejemplo de la calculadora y el criterio de orden por simplicidad.
