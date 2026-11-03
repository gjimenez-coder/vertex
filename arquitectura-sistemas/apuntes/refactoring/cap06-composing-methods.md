# Refactoring: Improving the Design of Existing Code — Martin Fowler (con Kent Beck, John Brant, William Opdyke y Don Roberts) (Addison-Wesley, 1999)
## Capítulo 6 — Composing Methods (Componer métodos)

> Nota de extracción: el texto se obtuvo de la capa de texto del PDF; las citas indican la página del PDF como `(PDF p. N)`.

## Lo que necesitas saber

Buena parte de la refactorización consiste en componer métodos para empaquetar bien el código. Casi siempre los problemas vienen de métodos demasiado largos: acumulan mucha información que queda sepultada por la lógica compleja que arrastran. El capítulo reúne las refactorizaciones que trocean y reorganizan métodos para hacerlos cortos y con nombres que expresen su intención.

La refactorización central es Extract Method: tomar un trozo de código y convertirlo en un método propio. Su opuesta es Inline Method: sustituir una llamada por el cuerpo del método. El mayor obstáculo de Extract Method son las variables locales, y los temporales (temps) son la principal fuente del problema. Para eliminarlos se usan Replace Temp with Query y, cuando un temp sirve para varias cosas, primero Split Temporary Variable. Si los temporales están demasiado enredados, se recurre a Replace Method with Method Object, que descompone incluso el método más enmarañado a costa de introducir una clase nueva.

Los parámetros dan menos problemas que los temps, siempre que no se les asigne; si se les asigna, hay que aplicar Remove Assignments to Parameters. Una vez troceado el método se entiende mucho mejor, y a veces se descubre un algoritmo más claro que se introduce con Substitute Algorithm. Sales sabiendo cómo convertir métodos largos en conjuntos de métodos cortos y bien nombrados, y cómo lidiar con las variables locales que lo dificultan.

## Extract Method

Tienes un fragmento de código que puede agruparse: conviértelo en un método cuyo nombre explique su propósito. Es una de las refactorizaciones más frecuentes de Fowler. Se nombra el método por lo que hace, no por cómo lo hace. La clave no es la longitud, sino la distancia semántica entre el nombre y el cuerpo: "If extracting improves clarity, do it, even if the name is longer than the code you have extracted" (PDF p. 90). Los métodos cortos aumentan la reutilización, hacen que los métodos de alto nivel se lean como una serie de comentarios y facilitan el override.

El problema son las variables locales:
- Variables solo leídas: se pasan como parámetros.
- Objeto local al que se invoca un método modificador: también se pasa como parámetro; solo hay trabajo extra si se reasigna la variable.
- Temp asignado usado solo dentro del código extraído: se mueve al método extraído.
- Temp asignado que se usa después: el método extraído debe devolver el valor cambiado.

Si hace falta devolver más de un valor, lo mejor suele ser elegir otro trozo que extraer; Fowler prefiere métodos que devuelvan un único valor. Cuando los temps son tan abundantes que la extracción resulta incómoda, se reducen con Replace Temp with Query o, en último término, con Replace Method with Method Object.

```java
void printOwing() {
    printBanner();
    double outstanding = getOutstanding();
    printDetails(outstanding);
}
```

## Inline Method

Cuando el cuerpo de un método es tan claro como su nombre, se mete el cuerpo en el de quienes lo llaman y se elimina el método. "Indirection can be helpful, but needless indirection is irritating" (PDF p. 96). También se usa para reagrupar métodos mal factorizados: se hace inline de todos en un método grande y luego se vuelve a extraer; Kent Beck suele hacer esto antes de Replace Method with Method Object. Mecánica: comprobar que el método no es polimórfico (no hacer inline si las subclases lo redefinen), hallar todas las llamadas, reemplazarlas por el cuerpo, compilar, probar y borrar la definición.

## Inline Temp

Tienes un temp asignado una sola vez con una expresión simple que estorba a otras refactorizaciones: reemplaza todas las referencias por la expresión. Casi siempre se usa como parte de Replace Temp with Query. Por sí solo se aplica cuando un temp recibe el resultado de una llamada a método y entorpece, por ejemplo, un Extract Method. Se declara el temp como `final` para confirmar que solo se asigna una vez, se sustituyen las referencias por el lado derecho y se elimina la declaración.

## Replace Temp with Query

Usas un temp para guardar el resultado de una expresión: extrae la expresión a un método y reemplaza las referencias al temp por la llamada; así cualquier método de la clase puede acceder a esa información. Los temps son temporales y locales, por lo que fomentan métodos largos. Esta refactorización es un paso vital antes de Extract Method, porque las variables locales dificultan la extracción.

Los casos sencillos son temps asignados una sola vez con expresiones sin efectos secundarios. El método extraído debe estar libre de efectos secundarios; si no, se aplica antes Separate Query from Modifier. Si el temp acumula un resultado en un bucle, se puede extraer el bucle entero; si un bucle suma varios valores, se duplica el bucle para cada temp. Sobre el rendimiento: dejarlo pasar de momento; nueve de cada diez veces no importará, y el código mejor factorizado habilita optimizaciones más potentes.

```java
double getPrice() {
    return basePrice() * discountFactor();
}
```

## Introduce Explaining Variable

Tienes una expresión complicada: pon el resultado, o partes de ella, en un temporal con un nombre que explique su propósito. Es especialmente útil con lógica condicional, donde cada cláusula se explica con un temp bien nombrado, o con un algoritmo largo donde cada paso se explica con un temp.

Fowler confiesa que casi siempre prefiere Extract Method, porque un temp solo sirve dentro de un método mientras que un método es reutilizable por todo el objeto. Reserva Introduce Explaining Variable para cuando Extract Method cuesta más: por ejemplo, un algoritmo con muchas variables locales. Una vez desenredada la lógica, puede aplicar Replace Temp with Query. El temp también es valioso si acaba necesitando Replace Method with Method Object.

## Split Temporary Variable

Tienes un temp asignado más de una vez que no es variable de bucle ni temporal de acumulación: crea un temporal separado para cada asignación. Un temp con más de una responsabilidad confunde al lector. No se dividen las variables de bucle (loop variables) ni las de acumulación (collecting temporary variables), cuya forma suele ser `i = i + expresión` (suma, concatenación, escritura a stream o adición a colección). La mecánica: renombrar el temp en su declaración y primera asignación, declararlo `final`, cambiar las referencias hasta la segunda asignación, y repetir por etapas. El ejemplo del "haggis" divide `acc`, que cargaba primero la aceleración inicial y luego la aceleración con ambas fuerzas, en `primaryAcc` y `secondaryAcc`.

## Remove Assignments to Parameters

El código asigna a un parámetro: usa una variable temporal en su lugar. "Asignar a un parámetro" significa cambiar la referencia (p. ej. `foo = anotherObject`), no modificar el objeto recibido (`foo.modifyInSomeWay()`), que es correcto. La motivación es la claridad y evitar la confusión entre paso por valor y por referencia. Java usa siempre paso por valor: cualquier cambio del parámetro no se refleja en el llamador; la referencia del objeto se pasa por valor, lo que permite modificar el objeto pero no tiene efecto al reasignar el parámetro. Fowler trata sus parámetros como `final` aunque rara vez los marca así en métodos cortos; usa `final` en métodos largos para ver si algo cambia el parámetro.

```java
int discount(int inputVal, int quantity, int yearToDate) {
    int result = inputVal;
    if (inputVal > 50) result -= 2;
    // ...
    return result;
}
```

## Replace Method with Method Object

Tienes un método largo que usa variables locales de tal modo que no puedes aplicar Extract Method: conviértelo en un objeto propio, de forma que todas las variables locales pasen a ser campos de ese objeto; luego puedes descomponerlo libremente con Extract Method sin pasar parámetros. Técnica tomada de Beck. Mecánica: crear una clase con el nombre del método; darle un campo `final` para el objeto anfitrión original (source object) y un campo por cada temporal y parámetro; un constructor que reciba el source object y los parámetros; un método `compute` con el cuerpo original (usando el campo del source object para invocar sus métodos); y reemplazar el método antiguo por uno que cree el objeto y llame a `compute`. En el ejemplo, `gamma` de `Account` delega en `new Gamma(this, ...).compute()`.

## Substitute Algorithm

Quieres reemplazar un algoritmo por otro más claro: sustituye el cuerpo del método por el nuevo algoritmo. Ocurre al aprender más sobre el problema o al empezar a usar una biblioteca que duplica tu código. Antes de sustituir hay que descomponer el método tanto como sea posible: sustituir un algoritmo grande y complejo es muy difícil, solo simplificándolo se hace tratable. Mecánica: preparar el algoritmo alternativo hasta que compile, ejecutarlo contra los tests, y si los resultados difieren usar el algoritmo antiguo como comparación en las pruebas, ejecutando cada caso con ambos. El ejemplo reemplaza una cadena de `if` por una búsqueda en una lista de candidatos con `candidates.contains(people[i])`.

## Ideas clave

- Los métodos largos son la fuente habitual de problemas; componer métodos cortos y bien nombrados es el remedio central.
- Extract Method e Inline Method son opuestas: extraer para dar nombre a la intención, hacer inline para eliminar indirección innecesaria o reagrupar antes de re-extraer.
- Las variables locales, sobre todo los temps, son el mayor obstáculo de Extract Method.
- Replace Temp with Query suele ser paso previo imprescindible a Extract Method; Fowler lo prefiere a dejar temps.
- Split Temporary Variable: un temp con más de una responsabilidad debe dividirse; nunca se dividen bucles ni temporales de acumulación.
- No asignar a parámetros en Java; su paso por valor confunde entre modificar el objeto y reasignar la referencia.
- Replace Method with Method Object convierte los locales en campos y permite descomponer el método más enredado, a costa de una clase nueva.
- Substitute Algorithm exige descomponer primero el método; conviene validar el nuevo algoritmo comparándolo con el antiguo en los tests.
