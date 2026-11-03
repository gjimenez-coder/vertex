# Refactoring: Improving the Design of Existing Code — Martin Fowler (con Kent Beck, John Brant, William Opdyke y Don Roberts) (Addison-Wesley, 1999)
## Capítulo 9 — Simplifying Conditional Expressions (Simplificación de expresiones condicionales)

> Nota de extracción: el texto se obtuvo de la capa de texto del PDF; las citas usan la página del PDF `(PDF p. N)`.

## Lo que necesitas saber
La lógica condicional tiende a volverse enrevesada, y este capítulo reúne un conjunto de refactorizaciones para simplificarla. La refactorización central es Decompose Conditional, que descompone un condicional en piezas para separar la lógica de conmutación (el *switch*) de los detalles de lo que ocurre en cada rama. El resto de técnicas atacan casos concretos: cuando varias pruebas producen el mismo efecto, cuando hay duplicación dentro del condicional, cuando aparecen banderas de control heredadas del estilo "un único punto de salida", y cuando el condicional elige comportamiento según el tipo de un objeto.

La tesis de fondo es que el código condicional suele decir *qué* pasa pero oscurece *por qué* pasa; extraer condiciones y ramas a métodos con nombres intencionales hace explícito el motivo de la bifurcación. En programas orientados a objetos buena parte del comportamiento condicional lo absorbe el polimorfismo, por lo que los `switch`/`case` sobre códigos de tipo son candidatos a desaparecer. Un uso menos obvio pero muy útil del polimorfismo es eliminar comprobaciones de `null` mediante un objeto nulo.

Sales sabiendo cuándo y cómo aplicar cada técnica, y por qué la regla de "un solo punto de salida" no es útil: la claridad manda, y a veces salir temprano con una guard clause comunica mejor la intención.

## Decompose Conditional
Ante un `if-then-else` complejo, se extraen métodos de la condición, de la rama *then* y de la rama *else*. Aunque las condiciones suelen ser cortas, hay una brecha grande entre la intención del código y su cuerpo; leer `notSummer(date)` comunica un mensaje más claro que la expresión original, que obliga a descifrar qué hace. Los nombres extraídos se leen casi como un comentario.

```java
// Antes
if (date.before(SUMMER_START) || date.after(SUMMER_END))
    charge = quantity * _winterRate + _winterServiceCharge;
else charge = quantity * _summerRate;

// Después
if (notSummer(date)) charge = winterCharge(quantity);
else charge = summerCharge(quantity);
```

Mecánica: extraer la condición a su propio método; extraer *then* y *else* a sus propios métodos. En la práctica cada extracción se hace por separado, compilando y probando tras cada una. Ante condicionales anidados, Fowler mira primero si procede Replace Nested Conditional with Guard Clauses antes de descomponer.

## Consolidate Conditional Expression
Cuando hay una secuencia de comprobaciones distintas que producen el mismo resultado, se combinan en una sola expresión con `and`/`or` y se extrae. Esto aclara que en realidad se hace una única comprobación y prepara el terreno para Extract Method, sustituyendo un *qué haces* por un *por qué lo haces*.

```java
double disabilityAmount() {
    if (isNotEligibleForDisability()) return 0;
    // compute the disability amount
}
boolean isNotEligibleForDisability() {
    return ((_seniority < 2) || (_monthsDisabled > 12) || (_isPartTime));
}
```

Mecánica: comprobar que ningún condicional tiene efectos secundarios (si los tiene, no se puede refactorizar); reemplazar la cadena por un único condicional con operadores lógicos; compilar y probar; considerar Extract Method. Funciona igual con `and` (anidamientos que combinan). Si la rutina solo prueba la condición y devuelve un valor, puede convertirse en un único `return` con operador ternario:

```java
return (onVacation() && lengthOfService() > 10) ? 1 : 0.5;
```

Advertencia: si las comprobaciones son realmente independientes y no deben pensarse como una sola, no se consolida; el código ya comunica su intención.

## Consolidate Duplicate Conditional Fragments
Si el mismo fragmento aparece en todas las ramas del condicional, se mueve fuera de él para dejar claro qué varía y qué permanece igual.

```java
if (isSpecialDeal()) total = price * 0.95;
else                 total = price * 0.98;
send();
```

Mecánica: si el código común está al principio, moverlo antes del condicional; si está al final, después; si está en medio, ver si el código anterior o posterior cambia algo y desplazarlo hacia un extremo. Con más de una sentencia, extraerlas a un método. La misma situación aplica a excepciones: código repetido tras una sentencia en el `try` y en todos los `catch` puede moverse al bloque `finally`.

## Remove Control Flag
Una variable que actúa como bandera de control de una serie de expresiones booleanas se reemplaza por `break`, `continue` o `return`. Estas banderas vienen de la regla de un único punto de salida; Fowler acepta un único punto de entrada (que los lenguajes modernos imponen), pero la regla del único punto de salida produce condicionales retorcidos. A menudo sorprende lo que se consigue al eliminar la bandera: el propósito real del condicional se vuelve mucho más claro.

Mecánica (opción con `break`/`continue`): hallar el valor de la bandera que saca de la lógica y reemplazar las asignaciones de ese valor por `break`/`continue`, compilando y probando tras cada reemplazo. Opción alternativa (también válida sin `break`/`continue`): extraer la lógica a un método y reemplazar por `return`. Fowler prefiere la extracción con `return`, porque señala claramente que no se ejecuta más código. Hay que vigilar si la bandera también transporta información de resultado: en ese caso se conserva la bandera con `break`, o se devuelve el valor con el método extraído. El ejemplo con efectos secundarios (`sendAlert`) se continúa en Separate Query from Modifier.

## Replace Nested Conditional with Guard Clauses
Cuando un método tiene comportamiento condicional que no deja claro el camino normal de ejecución, se usan guard clauses para los casos especiales. Los condicionales vienen en dos formas: una en la que ambos caminos son comportamiento normal (usa `if`/`else`, dando igual peso a ambas ramas), y otra en la que una respuesta es normal y la otra es una condición inusual. La guard clause dice: "esto es raro; si pasa, haz algo y sal".

```java
double getPayAmount() {
    if (_isDead)      return deadAmount();
    if (_isSeparated) return separatedAmount();
    if (_isRetired)   return retiredAmount();
    return normalPayAmount();
}
```

Mecánica: por cada comprobación, poner la guard clause (que devuelve o lanza excepción), compilando y probando tras cada una; si todas dan el mismo resultado, usar Consolidate Conditional Expressions. Joshua Kerievsky aportó un ejemplo donde la guard clause se introduce invirtiendo la condición; Fowler evita dejar `not` dentro del condicional porque "retuerce la mente", y prefiere poner un valor explícito en los `return` de las guardas (considerando también Replace Magic Number with Symbolic Constant).

## Replace Conditional with Polymorphism
Cuando un condicional elige comportamiento según el tipo de un objeto, cada rama se mueve a un método sobrescrito en una subclase y el método original se hace abstracto. La esencia del polimorfismo es evitar escribir un condicional explícito cuando el comportamiento varía según el tipo. La mayor ganancia aparece cuando el mismo conjunto de condiciones se repite en muchos sitios: para añadir un tipo basta crear una subclase, sin tener que localizar y actualizar todos los condicionales; además, los clientes no necesitan conocer las subclases, lo que reduce dependencias.

Antes hay que tener la estructura de herencia, creada con Replace Type Code with Subclasses (la opción más simple) o Replace Type Code with State/Strategy (obligatoria si el código de tipo cambia tras crear el objeto o si ya se subclasifica por otro motivo). Mecánica: extraer el condicional a método si es parte de uno mayor; mover el método al tope de la jerarquía; por cada subclase, sobrescribir copiando y ajustando la rama correspondiente, compilar y probar, y eliminar esa rama del original; repetir hasta convertir todas las ramas; finalmente declarar abstracto el método de la superclase. En el ejemplo del pago a empleados (Engineer/Salesman/Manager), Fowler "mata una pata cada vez" y a veces deja una trampa `RuntimeException` en el `case` mientras avanza.

## Introduce Null Object
Ante comprobaciones repetidas de `null`, se reemplaza el valor nulo por un objeto nulo. En lugar de preguntar a un objeto qué tipo es y actuar según la respuesta, se invoca el comportamiento y el objeto hace lo correcto. Ron Jeffries relata que empezaron a usar el patrón al ver mucho código comprobando la presencia de objetos antes de enviarles un mensaje; implementaron objetos "missing" (persona ausente con tarifa cero, sesión de Gemstone ausente, bin ausente) y llegaron a más de 80 clases de objeto nulo. Los objetos nulos son constantes e inmutables, por lo que se implementan con el patrón Singleton.

Mecánica: crear una subclase que actúe como versión nula y una operación `isNull` (que devuelve `false` en la clase fuente y `true` en la nula); encontrar los sitios que pueden devolver `null` y hacer que devuelvan el objeto nulo; reemplazar las comparaciones `== null` por `isNull()`; luego, caso por caso, mover el comportamiento por defecto al objeto nulo (p. ej. `getName()` devuelve `"occupant"`) y eliminar el condicional. La ganancia aparece al mover comportamiento y suprimir condicionales, y solo tiene sentido cuando la mayoría —no todos— de los clientes quieren la misma respuesta; quien quiera otra sigue pudiendo usar `isNull`.

```java
// Antes
if (customer == null) plan = BillingPlan.basic();
else                  plan = customer.getPlan();
```

Alternativa: la *testing interface*, una interfaz `Null {}` vacía implementada por los objetos nulos, probada con `instanceof`; útil cuando no se puede modificar la clase fuente. Los objetos nulos suelen devolver otros objetos nulos (p. ej. `NullPaymentHistory`). Existe un patrón mayor, *special case*, donde `UnknownCustomer` y `NoCustomer` serían casos especiales de `Customer`; también ocurre con números (infinitos positivo/negativo y NaN en coma flotante).

## Introduce Assertion
Cuando una sección de código asume algo sobre el estado del programa, se hace explícita la suposición con una aserción. Una aserción es una sentencia condicional que se asume siempre verdadera; su fallo indica error del programador y debe producir excepciones no comprobadas. Las aserciones no deben ser usadas por otras partes del sistema y suelen eliminarse en producción, así que conviene señalarlas con una clase `Assert`. Actúan como ayuda de comunicación y de depuración; con código autoprobado la ayuda de depuración pesa menos, pero sigue valiendo la de comunicación.

```java
double getExpenseLimit() {
    Assert.isTrue(_expenseLimit != NULL_EXPENSE || _primaryProject != null);
    return (_expenseLimit != NULL_EXPENSE) ?
        _expenseLimit : _primaryProject.getMemberExpenseLimit();
}
```

Añadir una aserción preserva el comportamiento. Advertencias: no usarlas para comprobar todo lo que crees cierto, solo lo que necesita serlo; si el código funciona sin la aserción, esta confunde y debe quitarse; evitar código duplicado en las aserciones usando Extract Method. En Java no hay mecanismo simple para insertarlas y deben ser fácilmente removibles para no afectar al rendimiento; un truco es `Assert.ON` como constante para que el compilador elimine el código muerto, o filtrar las líneas de aserción en producción. La clase `Assert` puede ofrecer métodos como `isTrue`, `equals` y `shouldNeverReachHere`.

## Ideas clave
- Decompose Conditional separa la lógica de conmutación de los detalles y revela el *por qué* detrás del *qué*.
- Consolidate Conditional Expression une pruebas con el mismo resultado (solo si no tienen efectos secundarios) y prepara Extract Method; si solo devuelve un valor, considera el ternario.
- Consolidate Duplicate Conditional Fragments saca fuera el código común a todas las ramas, incluido el `finally` para excepciones.
- Remove Control Flag sustituye banderas de control por `break`/`continue`/`return`; la regla de un único punto de salida no es útil.
- Replace Nested Conditional with Guard Clauses destaca el camino normal; las guardas comunican "esto es raro, sal pronto".
- Replace Conditional with Polymorphism elimina `switch`/`if` sobre tipos; requiere estructura de herencia (subclasses o state/strategy) y facilita añadir tipos.
- Introduce Null Object reemplaza comprobaciones repetidas de `null` por un objeto inmutable (Singleton) que responde con el comportamiento por defecto.
- Introduce Assertion hace explícitas las suposiciones del código; preserva el comportamiento, comunica intención y debe poder eliminarse en producción.
