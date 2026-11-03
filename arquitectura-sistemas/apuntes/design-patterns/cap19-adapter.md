# Dive Into Design Patterns — Alexander Shvets (Refactoring.Guru, 2021)
## Capítulo 19 — Adapter (Adaptador)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF (con palabras pegadas por la justificación de párrafos) y las citas usan la página del PDF.

## Lo que necesitas saber

Adapter es un patrón de diseño estructural que permite la colaboración entre objetos con interfaces incompatibles. También se le llama Adaptador, Envoltorio o Wrapper. Su idea central es introducir un objeto intermedio —el adaptador— que convierte la interfaz de un objeto en otra que un segundo objeto pueda comprender, ocultando la complejidad de esa conversión.

El patrón resuelve el problema de reutilizar una clase existente (a menudo de un tercero o heredada) cuya interfaz no encaja con el resto del código, sin tener que modificar esa clase ni el código cliente. Al terminar sabrás distinguir las dos variantes del patrón —adaptador de objetos (por composición) y clase adaptadora (por herencia)— y cómo implementarlo paso a paso.

## El ejemplo que recorre el capítulo

Una aplicación de monitoreo del mercado de valores descarga información de bolsa en formato XML para presentarla con gráficos. Al integrar una biblioteca de análisis de un tercero surge un conflicto: la biblioteca solo funciona con datos en formato JSON. No puede usarse "tal cual", y cambiar la biblioteca podría descomponer el código existente o ser imposible por falta de acceso al código fuente.

La solución es crear adaptadores de XML a JSON para cada clase de la biblioteca de análisis. El código se ajusta para comunicarse con la biblioteca únicamente a través de estos adaptadores: cuando un adaptador recibe una llamada, traduce los datos XML entrantes a una estructura JSON y la pasa a los métodos del objeto de análisis envuelto.

## Problema

Al integrar una biblioteca que espera un formato de datos incompatible con la aplicación, las opciones directas fallan. Modificar la biblioteca para que acepte XML podría romper el código que depende de ella, y frecuentemente ni siquiera se tiene acceso a su código fuente, lo que descarta esa vía.

## Solución

El adaptador es un objeto especial que convierte la interfaz de un objeto para que otro la comprenda. Envuelve uno de los objetos para esconder la complejidad de la conversión que ocurre tras bambalinas; el objeto envuelto ni siquiera es consciente del adaptador (por ejemplo, envolver un objeto que opera en metros y kilómetros con un adaptador que convierte todo al sistema anglosajón, pies y millas).

Los adaptadores no solo convierten datos a varios formatos, sino que ayudan a objetos con distintas interfaces a colaborar. El funcionamiento es:

1. El adaptador obtiene una interfaz compatible con uno de los objetos existentes.
2. Usando esa interfaz, el objeto existente invoca con seguridad los métodos del adaptador.
3. Al recibir la llamada, el adaptador la pasa al segundo objeto, en el formato y orden que ese objeto espera.

En ocasiones puede crearse un adaptador de dos direcciones, capaz de convertir las llamadas en ambos sentidos.

## Analogía en el mundo real

Al viajar de Europa a Estados Unidos surge una sorpresa al cargar la computadora portátil: los tipos de enchufe son diferentes en cada país y un enchufe español no sirve en Estados Unidos. El problema se soluciona con un adaptador que incluye el enchufe americano y el europeo.

## Estructura

Hay dos implementaciones.

Adaptador de objetos. Usa el principio de composición de objetos: el adaptador implementa la interfaz de un objeto y envuelve el otro. Puede implementarse en todos los lenguajes de programación populares. Sus participantes:

1. Cliente: contiene la lógica de negocio existente del programa.
2. Interfaz con el Cliente: describe el protocolo que otras clases deben seguir para colaborar con el código cliente.
3. Servicio: clase útil (normalmente de un tercero o heredada) que el cliente no puede usar directamente por tener una interfaz incompatible.
4. Clase Adaptadora: trabaja tanto con el cliente como con el servicio; implementa la interfaz con el cliente mientras envuelve el objeto de servicio. Recibe llamadas del cliente a través de la interfaz adaptadora y las traduce en llamadas al objeto envuelto, en un formato que este pueda comprender.
5. El código cliente no se acopla a la clase adaptadora concreta mientras trabaje a través de la interfaz con el cliente. Así pueden introducirse nuevos tipos de adaptadores sin descomponer el código cliente existente, útil cuando la interfaz del servicio cambia o se sustituye.

Clase adaptadora. Usa la herencia: la clase adaptadora hereda interfaces de ambos objetos al mismo tiempo. Solo puede implementarse en lenguajes que soporten herencia múltiple, como C++. No necesita envolver objetos porque hereda comportamientos tanto de la clase cliente como del servicio; la adaptación ocurre dentro de los métodos sobrescritos, y la clase resultante puede utilizarse en lugar de una clase cliente existente.

## Pseudocódigo

El ejemplo se basa en el clásico conflicto entre piezas cuadradas y agujeros redondos. El adaptador finge ser una pieza redonda con un radio igual a la mitad del diámetro del cuadrado (el radio del círculo más pequeño en el que quepa la pieza cuadrada).

Existen dos clases compatibles, `RoundHole` (con `fits(peg)` que compara radios) y `RoundPeg`. La clase incompatible es `SquarePeg`, que expone `getWidth()`. La clase `SquarePegAdapter` extiende `RoundPeg`, contiene una instancia de `SquarePeg` y sobrescribe `getRadius()`:

```
method getRadius() is
  // Simula una pieza redonda con radio que alberga la pieza cuadrada.
  return peg.getWidth() * Math.sqrt(2) / 2
```

Así, `hole.fits(small_sqpeg)` no compila (tipos incompatibles), pero `hole.fits(small_sqpeg_adapter)` devuelve verdadero y `hole.fits(large_sqpeg_adapter)` devuelve falso.

## Aplicabilidad

- Usa la clase adaptadora cuando quieras usar una clase existente cuya interfaz no sea compatible con el resto del código. Crea una clase intermedia que traduzca entre tu código y una clase heredada, de un tercero o con una interfaz extraña.
- Úsalo cuando quieras reutilizar varias subclases existentes que carezcan de alguna funcionalidad común que no pueda añadirse a la superclase. En lugar de extender cada subclase y duplicar código (lo cual "huele muy mal"), coloca la funcionalidad que falta en una clase adaptadora y envuelve los objetos a los que les faltan funciones, obteniéndolas de modo dinámico. Las clases deben tener una interfaz común; el procedimiento es similar al del patrón Decorator.

## Cómo implementarlo

1. Asegúrate de tener al menos dos clases con interfaces incompatibles: una clase servicio que no puedes cambiar y una o varias clases cliente que se beneficiarían de ella.
2. Declara la interfaz con el cliente y describe cómo las clases cliente se comunican con el servicio.
3. Crea la clase adaptadora y haz que siga la interfaz con el cliente, con los métodos vacíos por ahora.
4. Añade un campo a la clase adaptadora para almacenar una referencia al objeto de servicio, normalmente inicializado por el constructor (a veces conviene pasarlo al invocar los métodos).
5. Implementa uno por uno los métodos de la interfaz con el cliente, delegando el trabajo real al objeto de servicio y gestionando solo la interfaz o la conversión de formato de los datos.
6. Las clases cliente deben usar la clase adaptadora a través de la interfaz con el cliente, para poder cambiar o extender los adaptadores sin afectar al código cliente.

## Pros y contras

- Principio de responsabilidad única: separa la interfaz o el código de conversión de datos de la lógica de negocio primaria.
- Principio de abierto/cerrado: introduce nuevos tipos de adaptadores sin descomponer el código cliente, siempre que trabaje a través de la interfaz con el cliente.
- Contra: la complejidad general del código aumenta, ya que se introduce un grupo de nuevas interfaces y clases. A veces es más sencillo cambiar la clase de servicio para que coincida con el resto del código.

## Relaciones con otros patrones

- Bridge suele diseñarse por anticipado para desarrollar partes de forma independiente; Adapter se usa con una aplicación existente para hacer que clases incompatibles trabajen juntas.
- Adapter cambia la interfaz de un objeto existente, mientras que Decorator la mejora sin cambiarla; además Decorator soporta composición recursiva, lo cual no es posible con Adapter.
- Adapter da una interfaz diferente al objeto envuelto, Proxy le da la misma interfaz y Decorator una mejorada.
- Facade define una nueva interfaz para objetos existentes, mientras que Adapter intenta hacer utilizable la interfaz existente; Adapter suele envolver un objeto y Facade trabaja con todo un subsistema.
- Bridge, State, Strategy (y en parte Adapter) tienen estructuras similares basadas en la composición, pero resuelven problemas diferentes.

## Ideas clave

- Adapter permite colaborar a objetos con interfaces incompatibles mediante un objeto traductor intermedio.
- El objeto envuelto no es consciente del adaptador; la conversión queda oculta.
- Hay dos variantes: adaptador de objetos (composición, cualquier lenguaje) y clase adaptadora (herencia múltiple, p. ej. C++).
- El ejemplo canónico encaja piezas cuadradas en agujeros redondos simulando un radio equivalente.
- Favorece los principios de responsabilidad única y abierto/cerrado, a costa de mayor complejidad de código.
- Úsalo para reutilizar clases de terceros o heredadas sin modificarlas, o para dotar de funcionalidad común a subclases mediante envoltura dinámica.
- Se distingue de Bridge, Decorator, Proxy y Facade por qué le hace a la interfaz y por el alcance de lo que envuelve.
