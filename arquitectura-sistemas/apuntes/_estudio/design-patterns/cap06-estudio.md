# Encapsula lo que varía (Encapsulate What Varies) — Estudio

## Tarjetas de repaso

P: ¿Qué enuncia el principio "Encapsula lo que varía"? / R: Identifica los aspectos de la aplicación que varían y sepáralos de los que se mantienen inalterables.

P: ¿Cuál es el objetivo principal del principio? / R: Minimizar el efecto provocado por los cambios.

P: ¿Qué representa el barco en la metáfora del capítulo? / R: El barco es el programa y los cambios son minas escondidas bajo el agua que pueden hundirlo.

P: ¿Cómo se defiende el barco de las minas según la metáfora? / R: Dividiendo el casco en compartimentos sellables, de modo que los daños quedan limitados a un único compartimento y el barco sigue a flote.

P: ¿Qué equivale a los compartimentos sellados en el código? / R: Aislar en módulos independientes las partes del programa que varían, protegiendo el resto del código.

P: ¿Cuál es el beneficio práctico de aislar lo que varía? / R: Se dedica menos tiempo a hacer que el programa vuelva a funcionar al implementar y probar cambios, dejando más tiempo para nuevas funciones.

P: ¿En qué dos niveles de granularidad se ilustra el principio? / R: A nivel del método y a nivel de la clase.

P: ¿Qué método es el hilo conductor del ejemplo? / R: `obtenerTotaldelPedido` (`getOrderTotal`), que calcula el total del pedido con impuestos incluidos.

P: ¿Por qué el cálculo del impuesto es el aspecto que se anticipa que variará? / R: La tasa depende del país, estado o ciudad del cliente, y la fórmula puede cambiar con nuevas leyes o regulaciones.

P: ¿En qué consiste la encapsulación a nivel del método en el ejemplo? / R: Extraer la lógica de cálculo del impuesto a un método separado (`getTaxRate`), ocultándola del método original.

P: ¿Qué método designado devuelve la tasa impositiva según el país? / R: `getTaxRate(country)`, que devuelve 0.07 para "US", 0.20 para "EU" y 0 en los demás casos.

P: ¿Qué ventaja adicional da extraer el impuesto a su propio método? / R: Si la lógica se complica demasiado, resulta más sencillo moverla a una clase separada.

P: ¿Cuándo conviene la encapsulación a nivel de la clase? / R: Cuando un método acumula responsabilidades, campos y métodos de ayuda que nublan la responsabilidad principal de la clase contenedora.

P: ¿Cómo queda la clase `Pedido` (`Order`) tras encapsular a nivel de clase? / R: Delega todo el trabajo relacionado con el impuesto a un objeto dedicado, ocultándose ese cálculo.

## Preguntas de autoevaluación

P: ¿Qué problema concreto motiva aplicar el principio en el ejemplo de comercio electrónico? / R: Que la lógica de impuestos obliga a modificar con frecuencia `obtenerTotaldelPedido`, aunque su nombre sugiere que no le importa cómo se calcula el impuesto. (Sección: El ejemplo que recorre el capítulo)

P: Explica con la metáfora del barco por qué aislar lo que varía protege el sistema. / R: Como los compartimentos sellados limitan el daño de una mina a un solo compartimento, los módulos aislados contienen el impacto de un cambio y protegen el resto del código. (Sección: Lo que necesitas saber)

P: ¿Cómo estaba organizado el código del impuesto "antes" de encapsularlo a nivel del método? / R: El cálculo del impuesto estaba mezclado con el resto del método: se acumulaba el total iterando las líneas del pedido y luego se aplicaba la tasa según el país dentro del mismo método. (Sección: Encapsulación a nivel del método)

P: ¿Qué cambio clave muestra el código "después" a nivel del método? / R: `getOrderTotal` suma `total * getTaxRate(order.country)`, delegando el cálculo de la tasa al método `getTaxRate`, que concentra las condiciones por país. (Sección: Encapsulación a nivel del método)

P: ¿Qué relación hay entre la encapsulación a nivel del método y a nivel de la clase? / R: Son dos niveles de granularidad del mismo principio; cuando la lógica extraída a un método crece demasiado, el siguiente paso es moverla a una clase dedicada. (Secciones: Encapsulación a nivel del método / Encapsulación a nivel de la clase)

P: ¿Por qué extraer responsabilidades a una nueva clase mejora el diseño? / R: Porque los comportamientos añadidos traen sus propios campos y métodos de ayuda que nublan la responsabilidad principal; extraerlos aporta mayor claridad y sencillez. (Sección: Encapsulación a nivel de la clase)

P: ¿Cómo se traduce el beneficio de tiempo del principio en valor para el desarrollo? / R: Cuanto menos tiempo se dedica a hacer cambios, más tiempo queda para implementar funciones. (Sección: Lo que necesitas saber)

## Puntos a dominar

- Enunciar el principio: separar lo que varía de lo que permanece inalterable, con el objetivo de minimizar el efecto de los cambios.
- Explicar la metáfora del barco y su correspondencia con módulos aislados en el código.
- Reconocer qué parte de un sistema "varía" (el cálculo del impuesto, dependiente de país y de regulaciones cambiantes).
- Aplicar la encapsulación a nivel del método: extraer la lógica cambiante a un método designado como `getTaxRate`.
- Aplicar la encapsulación a nivel de la clase: delegar un conjunto de responsabilidades a un objeto dedicado.
- Justificar el beneficio: menos tiempo arreglando cambios, más tiempo para nuevas funciones.
