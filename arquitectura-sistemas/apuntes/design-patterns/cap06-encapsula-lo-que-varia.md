# Dive Into Design Patterns — Alexander Shvets (Refactoring.Guru, 2021)
## Capítulo 6 — Encapsula lo que varía (Encapsulate What Varies)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF (con palabras pegadas por la justificación); las citas usan la página del PDF.

## Lo que necesitas saber

Este capítulo presenta el primer principio de diseño del libro: identifica los aspectos de tu aplicación que varían y sepáralos de los que se mantienen inalterables. Su objetivo principal es minimizar el efecto provocado por los cambios.

El texto usa la metáfora del barco: el programa es un barco y los cambios son minas escondidas bajo el agua; si el barco golpea una mina, se hunde. La defensa consiste en dividir el casco en compartimentos individuales que puedan sellarse para limitar los daños a un único compartimento, de modo que el barco pueda permanecer a flote. Del mismo modo, aíslas las partes del programa que varían en módulos independientes, protegiendo el resto del código frente a efectos adversos.

El beneficio práctico es de tiempo: al aislar lo que varía, dedicas menos tiempo a lograr que el programa vuelva a funcionar cuando implementas y pruebas los cambios. Cuanto menos tiempo dediques a realizar cambios, más tiempo tendrás para implementar funciones. El principio se ilustra en dos niveles de granularidad: a nivel del método y a nivel de la clase.

## El ejemplo que recorre el capítulo

El hilo conductor es un sitio web de comercio electrónico con un método `obtenerTotaldelPedido` (`getOrderTotal`) que calcula el total del pedido, impuestos incluidos. El código relacionado con los impuestos es el aspecto que se anticipa que variará: la tasa impositiva depende del país, estado o incluso ciudad del cliente, y la fórmula puede cambiar con el tiempo según nuevas leyes o regulaciones. Eso obligaría a modificar `obtenerTotaldelPedido` con frecuencia, aunque el nombre del método sugiere que no le importa cómo se calcula el impuesto.

## Encapsulación a nivel del método

Antes, el código de cálculo del impuesto está mezclado con el resto del código del método: el total se acumula iterando sobre las líneas del pedido y, a continuación, se aplica la tasa según el país dentro del mismo método.

```
method getOrderTotal(order) is
    total = 0
    foreach item in order.lineItems
        total += item.price * item.quantity

    if (order.country == "US")
        total += total * 0.07 // Impuesto sobre la venta de EUA
    else if (order.country == "EU"):
        total += total * 0.20 // IVA europeo

    return total
```

La solución consiste en extraer la lógica de cálculo del impuesto a un método separado, escondiéndola del método original, de modo que puedas obtener la tasa impositiva invocando un método designado.

```
method getOrderTotal(order) is
    total = 0
    foreach item in order.lineItems
        total += item.price * item.quantity

    total += total * getTaxRate(order.country)

    return total

method getTaxRate(country) is
    if (country == "US")
        return 0.07 // Impuesto sobre la venta de EUA
    else if (country == "EU")
        return 0.20 // IVA europeo
    else
        return 0
```

Después, los cambios relacionados con el impuesto quedan aislados dentro de un único método. Además, si la lógica de cálculo del impuesto se complica demasiado, ahora es más sencillo moverla a una clase separada.

## Encapsulación a nivel de la clase

Con el tiempo puedes añadir más y más responsabilidades a un método que solía hacer algo sencillo. Estos comportamientos añadidos suelen venir con sus propios campos y métodos de ayuda que acaban nublando la responsabilidad principal de la clase contenedora. Si se extrae todo a una nueva clase se puede conseguir mayor claridad y sencillez.

En el ejemplo, antes el cálculo del impuesto reside en la propia clase `Pedido` (`Order`). Después, los objetos de la clase `Pedido` delegan todo el trabajo relacionado con el impuesto a un objeto especial dedicado justo a eso, de forma que el cálculo del impuesto se esconde de la clase `Pedido`.

## Ideas clave

- El principio: identifica los aspectos que varían y sepáralos de los que se mantienen inalterables.
- El objetivo principal es minimizar el efecto provocado por los cambios.
- Metáfora del barco: compartimentos sellados limitan los daños de una mina a un solo compartimento, igual que módulos aislados contienen el impacto de un cambio.
- Aislar lo que varía reduce el tiempo de implementar y probar cambios, dejando más tiempo para nuevas funciones.
- Nivel del método: extraer la lógica cambiante (el cálculo del impuesto) a un método designado como `getTaxRate`.
- Nivel de la clase: cuando un método acumula responsabilidades, campos y métodos de ayuda, extraerlos a una clase dedicada mejora la claridad.
- En el ejemplo, la clase `Pedido` delega el trabajo del impuesto a un objeto dedicado, ocultándole ese cálculo.
