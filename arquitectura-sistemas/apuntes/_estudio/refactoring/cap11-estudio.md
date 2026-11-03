# Dealing with Generalization (Tratar con la generalización) — Estudio

## Tarjetas de repaso

P: ¿Sobre qué estructura trabajan las refactorizaciones de este capítulo?
R: Sobre la generalización, es decir, las jerarquías de herencia: mover métodos y campos arriba y abajo, crear jerarquías nuevas y cambiar entre herencia y delegación.

P: ¿Por qué es peligrosa la duplicación entre clases relacionadas?
R: Es un criadero de errores: si lo mismo se dice en varios sitios, cualquier cambio obliga a tocar más puntos de los necesarios.

P: ¿Qué hace Pull Up Field?
R: Mueve a la superclase un campo que dos subclases comparten (aunque con nombres distintos), renombrándolo para unificarlo, creándolo en la superclase y borrándolo de las subclases.

P: En Pull Up Method, ¿qué complicación aparece cuando el cuerpo referencia features presentes solo en la subclase?
R: Se generaliza ese otro método o se declara abstracto en la superclase (por ejemplo, declarar `chargeFor` abstracto en `Customer`).

P: ¿Por qué los constructores requieren Pull Up Constructor Body en vez de Pull Up Method?
R: Porque no son métodos normales y no se heredan; se crea un constructor en la superclase (a menudo `protected`) y se invoca con `super` como primer paso.

P: ¿Para qué sirven Push Down Method y Push Down Field?
R: Son los inversos de subir: se usan cuando un comportamiento o campo de la superclase solo tiene sentido para algunas subclases, y son frecuentes tras Extract Subclass.

P: ¿Cuál es la alternativa principal a Extract Subclass y qué representa esa elección?
R: Extract Class; la elección entre Extract Subclass y Extract Class es la elección entre herencia y delegación.

P: ¿Qué limitaciones tiene Extract Subclass?
R: No puedes cambiar el comportamiento basado en clase una vez creado el objeto, y solo sirve para representar un conjunto de variaciones.

P: ¿En qué se diferencia Extract Interface de Extract Superclass?
R: Extract Interface solo saca interfaces comunes (no código común) y puede generar duplicación, mientras que Extract Superclass sube también los elementos comunes.

P: ¿Qué es un Form Template Method?
R: Cuando dos métodos de subclases hacen pasos similares en el mismo orden pero con pasos distintos, se mueve la secuencia a la superclase y el polimorfismo diferencia los pasos: un template method (Gang of Four).

P: ¿Cuándo se aplica Collapse Hierarchy?
R: Cuando una superclase y su subclase ya no se diferencian lo suficiente: se fusionan moviendo comportamiento y datos y se borra la clase vacía.

P: ¿Qué señala la necesidad de Replace Inheritance with Delegation?
R: Que la subclase usa solo parte de la interfaz de la superclase o no quiere heredar sus datos: la herencia dice una cosa mientras la intención es otra.

P: ¿Cuándo conviene Replace Delegation with Inheritance?
R: Cuando escribes muchos delegadores simples para toda la interfaz del delegado; entonces conviertes la clase delegante en subclase del delegado.

P: ¿Qué dos advertencias tiene Replace Delegation with Inheritance?
R: No aplicarlo si no usas todos los métodos del delegado, ni si el delegado es mutable y compartido por varios objetos (perderías el compartido de datos).

## Preguntas de autoevaluación

P: ¿Por qué suele crearse la estructura de herencia después de tener varias clases? (sección "Lo que necesitas saber")
R: Porque las comunalidades a menudo no se notan hasta tener ya varias clases, por lo que la jerarquía hay que crearla después.

P: En el ejemplo de `Customer` con `createBill`, ¿por qué no se puede subir el método directamente y qué se hace primero? (sección "Pull Up Field / Pull Up Method")
R: Porque `chargeFor` difiere en cada subclase; primero se declara `chargeFor` abstracto en `Customer` y luego se copia `createBill` a la superclase.

P: ¿Cómo se maneja el código común que debe ejecutarse después de asignar campos de la subclase en un constructor? (sección "Pull Up Constructor Body")
R: Se extrae a un método (como `initialize()`) con Extract Method y se sube con Pull Up Method; si se complica, considerar Replace Constructor with Factory Method.

P: En Extract Subclass de `LaborItem`, ¿cómo se elimina el campo `_isLabor`? (sección "Extract Subclass")
R: Sustituyendo su getter por métodos constantes polimórficos (`isLabor()` devuelve false en `JobItem` y true en `LaborItem`) y refactorizando los usos con Replace Conditional with Polymorphism.

P: En Extract Superclass de `Party`, ¿qué se unifica y cómo se trata el coste anual? (sección "Extract Superclass")
R: Se suben `_name` y `getName` y el cuerpo del constructor; `getAnnualCost` se unifica por nombre y se declara abstracto en `Party` porque se calcula de forma distinta.

P: ¿Qué ganancia concreta aporta Extract Interface en el ejemplo de `Billable`? (sección "Extract Interface")
R: Que se pueda facturar también a computadoras: basta con que implementen `Billable`, ya que el cargo pasa a declararse `charge(Billable emp, int days)`.

P: En Form Template Method sobre `statement()` y `htmlStatement()`, ¿qué pasos se siguen? (sección "Form Template Method")
R: Se crea una jerarquía de estrategia con un method object, se renombran a `value`, se extraen `headerString`, `eachRentalString` y `footerString` con la misma firma hasta que los dos `value` quedan idénticos y se sube uno.

P: En el ejemplo `MyStack extends Vector`, ¿cuáles son los pasos para reemplazar herencia por delegación? (sección "Replace Inheritance with Delegation")
R: Crear un campo `Vector`, reescribir `push` y `pop` para delegar, romper la herencia (`_vector = new Vector()`) y añadir delegadores `size` e `isEmpty`.

## Puntos a dominar

- Identificar duplicación entre clases relacionadas como criterio para actuar sobre la jerarquía.
- Distinguir cuándo subir (`Pull Up`) lo común y cuándo bajar (`Push Down`) lo específico.
- Tratar el caso especial de los constructores con Pull Up Constructor Body y saber cuándo pasar a Replace Constructor with Factory Method.
- Reconocer que Extract Subclass/Extract Superclass frente a Extract Class es siempre la elección entre herencia y delegación.
- Diferenciar Extract Interface (interfaces comunes, sin código) de Extract Superclass (sube código común).
- Aplicar Form Template Method separando pasos variables (abstractos) de los invariables.
- Saber conmutar entre herencia y delegación en ambos sentidos, respetando sus advertencias.
- Compilar y probar después de cada movimiento, avanzando en pasos pequeños y verificables.
