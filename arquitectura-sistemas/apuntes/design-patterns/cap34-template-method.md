# Dive Into Design Patterns — Alexander Shvets (Refactoring.Guru, 2021)
## Capítulo 34 — Template Method (Método plantilla)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF (que presentaba palabras pegadas por la justificación de párrafos) y las citas usan la página del PDF.

## Lo que necesitas saber

Template Method es un patrón de diseño de comportamiento que define el esqueleto de un algoritmo en la superclase, pero permite que las subclases sobrescriban pasos del algoritmo sin cambiar su estructura (PDF p. 407). La idea central es separar lo invariable (el orden y la coordinación de los pasos) de lo variable (la implementación concreta de cada paso).

El patrón divide un algoritmo en una serie de pasos convertidos en métodos, y coloca una serie de llamadas a esos métodos dentro de un único método plantilla. Los pasos pueden ser abstractos o tener una implementación por defecto. Para usar el algoritmo, el cliente aporta su propia subclase, implementa los pasos abstractos y sobrescribe los opcionales si hace falta, pero nunca el propio método plantilla (PDF p. 409).

Sales sabiendo cuándo conviene elevar código común a una superclase para eliminar duplicación, cómo distinguir pasos abstractos, opcionales y ganchos, y la diferencia clave frente a Strategy: Template Method trabaja a nivel de clase mediante herencia (estático), mientras Strategy trabaja a nivel de objeto mediante composición (cambiable en ejecución).

## El ejemplo que recorre el capítulo

Una aplicación de minería de datos que analiza documentos corporativos. Los usuarios suben documentos en varios formatos (PDF, DOC, CSV) y la aplicación extrae la información relevante en un formato uniforme. La primera versión sólo soportaba DOC; luego se añadió CSV y, un mes después, PDF (PDF p. 408).

El problema: las tres clases de minería contenían mucho código duplicado. Aunque el código para gestionar distintos formatos es totalmente diferente, el código para procesar y analizar los datos es casi idéntico. Además, el código cliente tenía muchos condicionales para elegir la acción según la clase del objeto de procesamiento (PDF p. 409).

La solución con Template Method: crear una clase base para los tres algoritmos de análisis, con un método plantilla que encadena las llamadas a los pasos de procesamiento. Los pasos de abrir/cerrar archivos y extraer/analizar información quedan en las subclases (son diferentes por formato); los pasos de analizar los datos sin procesar y generar informes, al ser muy similares, suben a la clase base para compartirse (PDF p. 410-411). Con una clase base común desaparecen también los condicionales del cliente gracias al polimorfismo.

## Tipos de pasos

Según el capítulo hay dos tipos principales de pasos, más un tercero (PDF p. 411):

- Pasos abstractos: deben ser implementados por todas las subclases.
- Pasos opcionales: ya tienen cierta implementación por defecto, pero aún pueden sobrescribirse si es necesario.
- Ganchos (hooks): un gancho es un paso opcional con un cuerpo vacío. El método plantilla funciona aunque el gancho no se sobrescriba. Normalmente se colocan antes y después de pasos cruciales, aportando a las subclases puntos adicionales de extensión.

## Analogía en el mundo real

La construcción de viviendas en masa. El plan arquitectónico para una casa estándar contiene varios puntos de extensión que permiten a un potencial propietario ajustar detalles. Cada paso (cimientos, armazón, paredes, tuberías de agua, cableado eléctrico, etc.) puede cambiarse ligeramente para que la casa resultante sea un poco diferente de las demás (PDF p. 412).

## Estructura

1. La Clase Abstracta declara métodos que actúan como pasos del algoritmo, así como el propio método plantilla que los invoca en un orden específico. Los pasos pueden ser abstractos o tener implementación por defecto.
2. Las Clases Concretas pueden sobrescribir todos los pasos, pero no el propio método plantilla (PDF p. 413).

## Pseudocódigo

El ejemplo proporciona un "esqueleto" para varias ramas de IA en un sencillo videojuego de estrategia. Todas las razas tienen tipos de unidades y edificios casi iguales, así que se reutiliza la misma estructura de IA, sobrescribiendo detalles: orcos más agresivos, humanos más defensivos y monstruos que no construyen nada. Añadir una nueva raza implica crear una subclase de la IA base y sobrescribir los métodos por defecto (PDF p. 414-415).

```
class GameAI is
    // El método plantilla define el esqueleto del algoritmo.
    method turn() is
        collectResources()
        buildStructures()
        buildUnits()
        attack()

    // Algunos pasos se implementan directamente en la clase base.
    method collectResources() is
        foreach (s in this.builtStructures) do
            s.collect()

    // Otros se declaran abstractos.
    abstract method buildStructures()
    abstract method buildUnits()

    // Una clase puede tener varios métodos plantilla.
    method attack() is
        enemy = closestEnemy()
        if (enemy == null)
            sendScouts(map.center)
        else
            sendWarriors(enemy.position)

    abstract method sendScouts(position)
    abstract method sendWarriors(position)

class OrcsAI extends GameAI is
    method buildStructures() is // granjas, cuarteles, fortaleza
    method buildUnits() is      // peones/exploradores o soldados/guerreros
    method sendScouts(position) is
    method sendWarriors(position) is

// Las subclases también pueden sobrescribir operaciones por defecto.
class MonstersAI extends GameAI is
    method collectResources() is // los monstruos no recopilan recursos
    method buildStructures() is  // los monstruos no construyen estructuras
    method buildUnits() is       // los monstruos no construyen unidades
```

## Aplicabilidad

- Cuando quieras permitir a tus clientes que extiendan únicamente pasos particulares de un algoritmo, pero no todo el algoritmo ni su estructura. El patrón convierte un algoritmo monolítico en pasos individuales extensibles por subclases, manteniendo intacta la estructura de la superclase (PDF p. 417).
- Cuando tengas muchas clases con algoritmos casi idénticos salvo diferencias mínimas; al convertirlos en método plantilla puedes elevar los pasos similares a una superclase y eliminar la duplicación, dejando en las subclases el código que varía (PDF p. 417-418).

## Cómo implementarlo

1. Analiza el algoritmo para ver si puedes dividirlo en pasos; distingue los comunes de los que siempre serán únicos.
2. Crea la clase base abstracta, declara el método plantilla y los métodos abstractos de los pasos, perfilando la estructura ejecutando los pasos. Considera declarar el método plantilla como `final` para evitar que las subclases lo sobrescriban.
3. No hay problema en que todos los pasos sean abstractos, pero a algunos les vendría bien una implementación por defecto.
4. Piensa en añadir ganchos entre los pasos cruciales.
5. Para cada variación del algoritmo, crea una nueva subclase concreta que implemente todos los pasos abstractos y pueda sobrescribir algunos opcionales (PDF p. 416-419).

## Pros y contras

- Pro: los clientes pueden sobrescribir sólo ciertas partes de un algoritmo grande, afectándoles menos los cambios en otras partes.
- Pro: puedes colocar el código duplicado dentro de una superclase.
- Contra: algunos clientes pueden verse limitados por el esqueleto proporcionado.
- Contra: puedes violar el principio de sustitución de Liskov al suprimir una implementación por defecto de un paso en una subclase.
- Contra: los métodos plantilla tienden a ser más difíciles de mantener cuantos más pasos tengan (PDF p. 419).

## Relaciones con otros patrones

- Factory Method es una especialización de Template Method; a la vez, un Factory Method puede servir como paso de un gran Template Method.
- Template Method se basa en la herencia (altera partes de un algoritmo extendiéndolas en subclases); Strategy se basa en la composición (altera el comportamiento suministrando distintas estrategias). Template Method trabaja a nivel de clase, por lo que es estático; Strategy trabaja a nivel de objeto, permitiendo cambiar comportamientos en tiempo de ejecución (PDF p. 419-420).

## Ideas clave

- Template Method define el esqueleto de un algoritmo en la superclase y deja que las subclases rellenen pasos sin alterar la estructura.
- El método plantilla encadena las llamadas a los pasos y no debe sobrescribirse (idealmente `final`).
- Tres tipos de pasos: abstractos (obligatorios), opcionales (con valor por defecto) y ganchos (opcionales con cuerpo vacío).
- El caso guía (minería de datos PDF/DOC/CSV) muestra cómo elevar el código común y eliminar duplicación y condicionales del cliente.
- El pseudocódigo de la IA del videojuego ilustra reutilizar una estructura y sobrescribir detalles por raza.
- Riesgos: esqueleto rígido, posibles violaciones de Liskov y peor mantenibilidad con muchos pasos.
- Frente a Strategy: Template Method usa herencia (estático, nivel de clase); Strategy usa composición (dinámico, nivel de objeto).
