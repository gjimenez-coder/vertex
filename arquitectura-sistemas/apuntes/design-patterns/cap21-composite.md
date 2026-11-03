# Dive Into Design Patterns — Alexander Shvets (Refactoring.Guru, 2021)
## Capítulo 21 — Composite (Objeto compuesto)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF (con palabras pegadas por la justificación) y las citas usan la página del PDF.

## Lo que necesitas saber

Composite es un patrón de diseño estructural que permite componer objetos en estructuras de árbol y trabajar con esas estructuras como si fueran objetos individuales (PDF p. 193). Solo tiene sentido aplicarlo cuando el modelo central de la aplicación puede representarse en forma de árbol.

La tesis central es que, al dar a los elementos simples y a los contenedores una interfaz común, el cliente puede invocar un comportamiento sobre toda la estructura sin conocer las clases concretas ni el nivel de anidación. Los propios objetos propagan la solicitud a lo largo del árbol de forma recursiva.

Sales sabiendo cómo modelar jerarquías anidadas (hojas y contenedores) tras una misma interfaz, cómo delegar el trabajo recursivamente desde los contenedores hacia sus hijos, y qué ventajas y costes implica generalizar esa interfaz común.

## El ejemplo que recorre el capítulo

El caso hilo conductor son **Productos** y **Cajas** de un sistema de pedidos. Una Caja puede contener varios Productos y también Cajas más pequeñas, que a su vez contienen más Productos o Cajas, formando un árbol (PDF p. 194).

El problema concreto es calcular el **precio total** de un pedido. La solución directa —desenvolver todas las cajas y recorrer los productos con un bucle— exige conocer de antemano las clases, el nivel de anidación y otros detalles, lo que la vuelve demasiado complicada o imposible (PDF p. 195).

Composite propone trabajar con Productos y Cajas a través de una interfaz común que declara un método para calcular el precio total. Para un producto, devuelve su precio; para una caja, recorre cada artículo, pregunta su precio y devuelve el total, descendiendo recursivamente por cada caja interna. Una caja puede incluso añadir costos extra, como los de empaquetado (PDF p. 195).

## Problema y solución

La gran ventaja es que no hay que preocuparse por las clases concretas de los objetos que componen el árbol: no importa si un objeto es un producto simple o una caja sofisticada, se tratan por igual a través de la interfaz común, y al invocar un método los objetos pasan la solicitud a lo largo del árbol (PDF p. 196). El patrón permite ejecutar un comportamiento de forma recursiva sobre todos los componentes del árbol de objetos.

## Analogía en el mundo real

Una estructura militar. Los ejércitos se organizan como jerarquías: un ejército se compone de divisiones, una división agrupa brigadas, una brigada está formada por pelotones, que se dividen en escuadrones, y un escuadrón es un pequeño grupo de soldados reales. Las órdenes se dan en la parte superior y se pasan hacia abajo por cada nivel hasta que todos los soldados saben qué hacer (PDF p. 197).

## Estructura

1. **Componente**: interfaz que describe operaciones comunes a elementos simples y complejos del árbol.
2. **Hoja (Leaf)**: elemento básico sin subelementos. Normalmente las hojas realizan la mayoría del trabajo real, ya que no tienen a quién delegar.
3. **Contenedor (compuesto)**: elemento que tiene subelementos (hojas u otros contenedores). No conoce las clases concretas de sus hijos y opera con ellos solo a través de la interfaz componente. Al recibir una solicitud, delega el trabajo a sus subelementos, procesa los resultados intermedios y devuelve el resultado final.
4. **Cliente**: funciona con todos los elementos a través de la interfaz componente, de modo que trata igual a elementos simples y complejos (PDF p. 198).

## Pseudocódigo

El ejemplo implementa el apilamiento (stacking) de formas geométricas en un editor gráfico. La clase `CompoundGraphic` es un contenedor que puede incluir cualquier cantidad de subformas, incluidas otras formas compuestas; tiene los mismos métodos que una forma simple, pero en lugar de actuar por su cuenta pasa la solicitud de forma recursiva a sus hijos y "suma" el resultado (PDF p. 199-200).

```
// La interfaz componente declara operaciones comunes.
interface Graphic is
    method move(x, y)
    method draw()

// La hoja representa objetos finales: no puede tener subobjetos.
class Dot implements Graphic is
    field x, y
    constructor Dot(x, y) { ... }
    method move(x, y) is
        this.x += x, this.y += y
    method draw() is
        // Dibuja un punto en X e Y.

class Circle extends Dot is
    field radius
    method draw() is
        // Dibuja un círculo en X e Y con radio R.

// La clase compuesta delega el trabajo a sus hijos y recapitula.
class CompoundGraphic implements Graphic is
    field children: array of Graphic
    method add(child: Graphic) is ...
    method remove(child: Graphic) is ...
    method move(x, y) is
        foreach (child in children) do
            child.move(x, y)
    method draw() is
        // 1. Para cada hijo: dibújalo y actualiza el rectángulo delimitador.
        // 2. Dibuja un rectángulo de línea punteada con las coordenadas.

// El cliente trabaja con todos a través de la interfaz base.
class ImageEditor is
    field all: array of Graphic
    method load() is
        all = new CompoundGraphic()
        all.add(new Dot(1, 2))
        all.add(new Circle(5, 3, 10))
    method groupSelected(components: array of Graphic) is
        group = new CompoundGraphic()
        foreach (component in components) do
            group.add(component)
            all.remove(component)
        all.add(group)
        all.draw()
```

Como el cliente usa la interfaz común, no sabe si trabaja con una forma simple o compuesta y puede manejar estructuras muy complejas sin acoplarse a las clases concretas (PDF p. 200).

## Aplicabilidad

- Cuando tengas que implementar una estructura de objetos con forma de árbol: el patrón ofrece hojas simples y contenedores complejos que comparten interfaz, y un contenedor puede componerse de hojas y de otros contenedores (PDF p. 203).
- Cuando quieras que el código cliente trate elementos simples y complejos de la misma forma, sin preocuparse por la clase concreta de los objetos.

## Cómo implementarlo

1. Asegúrate de que el modelo central puede representarse como árbol; divídelo en elementos simples y contenedores (estos deben poder contener ambos tipos).
2. Declara la interfaz componente con métodos que tengan sentido para componentes simples y complejos.
3. Crea una o varias clases hoja para los elementos simples.
4. Crea una clase contenedora con un campo matriz —declarado con el tipo de la interfaz componente— para almacenar subelementos; recuerda que el contenedor debe delegar la mayor parte del trabajo a sus hijos.
5. Define los métodos para añadir y eliminar hijos. Declararlos en la interfaz componente violaría el Principio de segregación de la interfaz (los métodos quedarían vacíos en la hoja), pero permite tratar todos los elementos igual (PDF p. 204-205).

## Pros y contras

- A favor: trabajas con estructuras de árbol complejas con más comodidad usando polimorfismo y recursión.
- A favor: cumple el Principio de abierto/cerrado; puedes introducir nuevos tipos de elemento sin descomponer el código existente.
- En contra: puede ser difícil dar una interfaz común a clases cuya funcionalidad difiere demasiado, obligando a generalizarla en exceso y volviéndola más difícil de comprender (PDF p. 205).

## Relaciones con otros patrones

- **Builder** puede usarse para construir árboles Composite complejos con pasos recursivos.
- **Chain of Responsibility** se usa a menudo con Composite: una hoja puede pasar una solicitud por la cadena de componentes padre hasta la raíz.
- **Iteradores** sirven para recorrer árboles Composite.
- **Visitor** permite ejecutar una operación sobre un árbol Composite entero.
- Los nodos hoja compartidos pueden implementarse como **Flyweights** para ahorrar RAM.
- **Composite y Decorator** tienen diagramas similares (ambos usan composición recursiva), pero un Decorator solo tiene un componente hijo y añade responsabilidades, mientras que Composite se limita a recapitular los resultados de sus hijos; además pueden colaborar.
- Diseños con uso amplio de Composite y Decorator se benefician de **Prototype**, que permite clonar estructuras complejas en vez de reconstruirlas (PDF p. 206).

## Ideas clave

- Composite es un patrón estructural para componer objetos en árboles y tratarlos como objetos individuales.
- Solo aplica cuando el modelo central se puede representar como árbol.
- Se basa en una interfaz común compartida por hojas y contenedores.
- Las hojas hacen el trabajo real; los contenedores delegan en sus hijos y recapitulan resultados.
- El cliente trata igual a elementos simples y complejos, sin acoplarse a clases concretas.
- Favorece polimorfismo, recursión y el Principio de abierto/cerrado.
- Su coste es la posible sobregeneralización de la interfaz cuando las clases difieren mucho.
- Se relaciona con Builder, Chain of Responsibility, Iterator, Visitor, Flyweight, Decorator y Prototype.
