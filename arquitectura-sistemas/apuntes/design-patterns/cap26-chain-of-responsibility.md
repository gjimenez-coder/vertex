# Dive Into Design Patterns — Alexander Shvets (Refactoring.Guru, 2021)
## Capítulo 26 — Chain of Responsibility (Cadena de responsabilidad)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF (con palabras pegadas por la justificación) y las citas usan la página del PDF.

## Lo que necesitas saber

Chain of Responsibility (CoR) es un patrón de diseño de comportamiento que permite pasar solicitudes a lo largo de una cadena de manejadores. Al recibir una solicitud, cada manejador decide si la procesa o si la pasa al siguiente manejador de la cadena. También se le conoce como Cadena de responsabilidad, CoR o Chain of Command.

La tesis central es transformar comportamientos particulares en objetos autónomos llamados manejadores, cada uno encapsulado en su propia clase con un único método de procesamiento. Esos manejadores se vinculan en una cadena: cada uno guarda una referencia al siguiente, de modo que la solicitud viaja por la cadena hasta que todos han tenido oportunidad de procesarla, o hasta que un manejador decide detener el procesamiento.

Sales sabiendo cuándo conviene desacoplar quien emite una solicitud de quien la gestiona, cómo componer cadenas en tiempo de ejecución sin acoplar el código a clases concretas, y cuál es la estructura mínima (interfaz manejadora, clase base opcional, manejadores concretos y cliente).

## El ejemplo que recorre el capítulo

El hilo conductor es un sistema de pedidos online. Se quiere que solo los usuarios autenticados generen pedidos y que los usuarios con permisos administrativos tengan pleno acceso. Las comprobaciones deben realizarse secuencialmente: si la autenticación falla, no hay razón para proceder con las demás.

Con el tiempo se añaden más comprobaciones: un paso de validación para sanear los datos de la solicitud, un filtro contra el descifrado de contraseñas por fuerza bruta que bloquea solicitudes fallidas repetidas desde la misma dirección IP, y una caché que deja pasar la solicitud al sistema solo cuando no hay una respuesta adecuada en caché.

Cuanto más crece el código, más se complica: un cambio en una comprobación afecta a las demás y reutilizar las comprobaciones en otros componentes obliga a duplicar código, porque cada componente necesita parte de las comprobaciones pero no todas. El sistema se vuelve difícil de comprender y costoso de mantener, hasta que se decide refactorizar con CoR.

## Solución

Cada comprobación se coloca en su propia clase con un único método que recibe la solicitud como argumento. Los manejadores se vinculan en cadena mediante un campo de referencia al siguiente, y además de procesar la solicitud la pasan a lo largo de la cadena. La mejor parte: un manejador puede decidir no pasar la solicitud más allá y detener así el procesamiento.

Hay una variante ligeramente distinta y más estandarizada en la que, al recibir una solicitud, el manejador decide si puede procesarla; si puede, no la pasa más allá. Así un único manejador procesa la solicitud o no la procesa ninguno. Esta variante es habitual con eventos en interfaces gráficas (GUI): al hacer clic en un botón, el evento se propaga por la cadena de elementos GUI (botón, contenedores, ventana principal) y lo gestiona el primer elemento capaz de hacerlo. El ejemplo muestra que siempre se puede extraer una cadena de un árbol de objetos. Es fundamental que todas las clases manejadoras implementen la misma interfaz.

## Analogía en el mundo real

Una llamada al soporte técnico puede pasar por muchos operadores: primero un contestador automático con soluciones populares, luego un operador humano que recita el manual, y finalmente un ingeniero que da la solución real (dónde descargar los drivers adecuados). Cada eslabón procesa la solicitud o la pasa al siguiente.

## Estructura

1. La clase **Manejadora** declara la interfaz común a todos los manejadores concretos. Normalmente contiene un único método para manejar solicitudes; a veces también un método para establecer el siguiente manejador.
2. La clase **ManejadoraBase** es opcional y aloja el código boilerplate común. Suele definir el campo de referencia al siguiente manejador y puede implementar el comportamiento por defecto: pasar la ejecución al siguiente manejador tras comprobar su existencia.
3. Los **Manejadores Concretos** contienen el código para procesar las solicitudes. Al recibir una, deciden si procesarla y si pasarla a lo largo de la cadena. Habitualmente son autónomos e inmutables, y reciben toda la información por el constructor.
4. El **Cliente** compone cadenas una sola vez o dinámicamente. Puede enviar una solicitud a cualquier manejador de la cadena; no tiene por qué ser el primero.

## Pseudocódigo

El ejemplo usa CoR para mostrar ayuda contextual de elementos GUI, creados con el patrón Composite. La GUI se estructura como un árbol: `Diálogo` (ventana principal, raíz) contiene `Paneles`, que contienen otros paneles o elementos de bajo nivel como `Botones` y `CamposDeTexto`. Cada elemento se vincula a su contenedor.

Un componente simple muestra una pista si tiene texto de ayuda asignado; si no, reenvía la llamada a su contenedor. Los componentes complejos sobrescriben la implementación por defecto (ventana modal, página wiki) y pueden invocar la base con `super.showHelp()`.

```
interface ComponentWithContextualHelp is
    method showHelp()

abstract class Component implements ComponentWithContextualHelp is
    field tooltipText: string
    protected field container: Container
    method showHelp() is
        if (tooltipText != null)
            // Muestra la pista.
        else
            container.showHelp()

abstract class Container extends Component is
    protected field children: array of Component
    method add(child) is
        children.add(child)
        child.container = this
```

Cuando el usuario apunta a un elemento y pulsa `F1`, la aplicación detecta el componente bajo el puntero y le envía una solicitud de ayuda; la solicitud emerge por todos los contenedores hasta el elemento capaz de mostrar la ayuda.

## Aplicabilidad

- Cuando el programa deba procesar distintos tipos de solicitudes de varias maneras, pero los tipos exactos y sus secuencias no se conozcan de antemano: se encadenan manejadores y se "pregunta" a cada uno si puede procesar la solicitud.
- Cuando sea fundamental ejecutar varios manejadores en un orden específico: al vincularlos en cualquier orden, las solicitudes recorren la cadena como se planee.
- Cuando el grupo de manejadores y su orden deban cambiar durante el tiempo de ejecución: con setters en el campo de referencia se insertan, eliminan o reordenan manejadores dinámicamente.

## Cómo implementarlo

1. Declara la interfaz manejadora y la firma del método para manejar solicitudes; lo más flexible es convertir la solicitud en un objeto y pasarlo como argumento.
2. Para eliminar boilerplate duplicado, crea una clase manejadora abstracta base con el campo de referencia al siguiente manejador (considera hacerla inmutable, o añade un setter si cambiarás la cadena en ejecución) y el comportamiento por defecto de reenvío.
3. Crea las subclases manejadoras concretas; cada una decide si procesa la solicitud y si la pasa al siguiente eslabón.
4. El cliente ensambla las cadenas o las recibe prefabricadas (en ese caso, clases fábrica según configuración o entorno).
5. El cliente puede activar cualquier manejador, no solo el primero; la solicitud se pasa hasta que algún manejador se rehúse a pasarla o se llegue al final.
6. Por la naturaleza dinámica de la cadena, el cliente debe prever: cadenas de un único vínculo, solicitudes que no llegan al final y solicitudes que llegan al final sin ser gestionadas.

## Pros y contras

- **A favor:** controlas el orden de control de solicitudes.
- **A favor:** Principio de responsabilidad única: desacoplas las clases que invocan operaciones de las que las realizan.
- **A favor:** Principio de abierto/cerrado: introduces nuevos manejadores sin descomponer el código cliente existente.
- **En contra:** algunas solicitudes pueden acabar sin ser gestionadas.

## Relaciones con otros patrones

- CoR, Command, Mediator y Observer conectan emisores y receptores de distintas formas: CoR pasa la solicitud secuencialmente por una cadena dinámica hasta que uno la gestiona; Command establece conexiones unidireccionales; Mediator comunica indirectamente a través de un mediador; Observer permite suscribirse o darse de baja dinámicamente.
- CoR se usa a menudo con Composite: un componente hoja puede pasar la solicitud por la cadena de componentes padre hasta la raíz del árbol.
- Los manejadores de CoR pueden implementarse como Comandos; también la propia solicitud puede ser un objeto Command ejecutado sobre contextos distintos vinculados en cadena.
- CoR y Decorator tienen estructuras muy similares (composición recursiva), pero los manejadores de CoR ejecutan operaciones arbitrarias e independientes y pueden dejar de pasar la solicitud; los decoradores extienden el comportamiento manteniendo la interfaz base y no pueden romper el flujo de la solicitud.

## Ideas clave

- CoR pasa una solicitud por una cadena de manejadores; cada uno decide si la procesa y si la reenvía.
- Cada comprobación o comportamiento se encapsula en un manejador autónomo con una interfaz común.
- Un manejador puede detener la cadena en cualquier momento.
- Existe una variante donde un único manejador procesa la solicitud o ninguno (típica en eventos GUI).
- La estructura la forman: interfaz Manejadora, ManejadoraBase opcional, Manejadores Concretos y Cliente.
- El cliente puede componer la cadena estática o dinámicamente, y enviar la solicitud a cualquier eslabón.
- Favorece responsabilidad única y abierto/cerrado, pero una solicitud puede quedar sin gestionar.
- Se combina con Composite (ayuda contextual en árbol de objetos) y se distingue de Decorator por poder romper el flujo.
