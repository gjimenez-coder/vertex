# Programa a una interfaz, no a una implementación — Estudio

## Tarjetas de repaso

P: ¿Cómo se enuncia el principio del capítulo? / R: "Programa a una interfaz, no a una implementación. Depende de abstracciones, no de clases concretas" (PDF p. 46).

P: ¿Cuándo se considera flexible un diseño? / R: Cuando puedes extenderlo con facilidad sin descomponer el código existente.

P: ¿Qué ilustra la analogía del gato? / R: Que una abstracción ("cualquier comida") admite más casos que una implementación concreta ("salchichas"); el gato que come cualquier comida es más flexible (PDF p. 46).

P: ¿Por qué depender de abstracciones hace más flexible la colaboración? / R: Porque la conexión entre objetos deja de atarse a una clase concreta y puede trabajar con cualquier objeto que cumpla la interfaz (PDF p. 47).

P: ¿Cuál es el primer paso para establecer una colaboración flexible? / R: Determinar qué necesita exactamente un objeto del otro: qué métodos ejecuta.

P: ¿Cuáles son los cuatro pasos para una colaboración flexible? / R: 1) Identificar los métodos necesarios; 2) describirlos en una interfaz o clase abstracta; 3) hacer que la dependencia la implemente; 4) hacer que la segunda clase dependa de la interfaz, no de la clase concreta (PDF p. 47).

P: ¿Qué coste tiene extraer una interfaz? / R: El código se vuelve más complicado y al principio no se nota un beneficio inmediato (PDF p. 47).

P: ¿Cuándo merece la pena extraer una interfaz? / R: Solo si prevés que ese punto es un buen lugar de extensión o si otras personas que usan tu código podrían querer extenderlo ahí (PDF p. 47).

P: ¿Qué ejemplo hilo conductor usa el capítulo? / R: Un simulador de una empresa de desarrollo de software con distintas clases de empleados.

P: En la etapa ANTES, ¿cuál es el problema de la clase `Empresa`? / R: Está fuertemente acoplada a clases de empleados concretos (PDF p. 48–49).

P: En la etapa MEJOR, ¿qué se logra y qué limitación queda? / R: Se extrae la interfaz `Empleado` y se aplica polimorfismo, pero el resto de `Empresa` sigue dependiendo de las clases de empleado concretas (PDF p. 49).

P: ¿Cuál es la solución de la etapa DESPUÉS? / R: Declarar abstracto el método que obtiene los empleados, para que cada empresa concreta cree solo los empleados que necesita en sus subclases (PDF p. 49–50).

P: ¿Qué se gana al declarar abstracto el método de creación? / R: `Empresa` se vuelve independiente de las clases de empleado concretas y puede extenderse sin descomponer el código existente (PDF p. 50).

P: ¿A qué patrón de diseño conduce este ejemplo? / R: Al patrón Factory Method (PDF p. 50).

## Preguntas de autoevaluación

P1: ¿Qué significa "programa a una interfaz, no a una implementación" y qué busca lograr?
R: Significa depender de abstracciones y no de clases concretas, para que el diseño sea flexible y extensible sin descomponer el código existente. (Sección "Lo que necesitas saber")

P2: ¿Por qué el gato que come "cualquier comida" es más flexible que el que solo come salchichas?
R: Porque la abstracción admite más casos: incluye las salchichas y además permite extender el menú con cualquier otra comida. (Sección "La analogía del gato", PDF p. 46)

P3: Enumera los cuatro pasos para convertir una dependencia concreta en una dependencia sobre una interfaz.
R: Identificar los métodos necesarios, describirlos en una interfaz o clase abstracta, hacer que la dependencia la implemente y hacer que la segunda clase dependa de la interfaz. (Sección "Cómo establecer una colaboración flexible", PDF p. 47)

P4: ¿Por qué aplicar polimorfismo en la clase `Empresa` no basta para eliminar el acoplamiento?
R: Porque, aunque trata a los empleados a través de la interfaz, el resto de la clase sigue dependiendo de las clases de empleado concretas y habría que reescribir casi toda `Empresa` para nuevos tipos. (Sección "MEJOR: polimorfismo con la interfaz Empleado", PDF p. 49)

P5: ¿Cómo se elimina el acoplamiento restante en la etapa DESPUÉS?
R: Declarando abstracto el método que obtiene los empleados, de modo que cada subclase de empresa lo implemente creando solo los empleados que necesita. (Sección "DESPUÉS: método para obtener empleados declarado como abstracto", PDF p. 49–50)

P6: ¿Qué desventaja tiene aplicar este principio y cuándo se justifica asumirla?
R: Hace el código más complicado sin beneficio inmediato; se justifica cuando prevés un punto de extensión real o que otros querrán extender tu código. (Sección "Cómo establecer una colaboración flexible", PDF p. 47)

P7: ¿Qué patrón de diseño aparece al aplicar este principio al simulador de empresa?
R: El patrón Factory Method, al delegar la creación de empleados en las subclases de empresa. (Sección "El ejemplo que recorre el capítulo", PDF p. 50)

## Checklist

- [ ] Identificar qué métodos necesita realmente un objeto de otro antes de acoplarlos.
- [ ] Describir esos métodos en una interfaz o clase abstracta común.
- [ ] Hacer que la clase dependencia implemente la interfaz extraída.
- [ ] Hacer que la clase consumidora dependa de la interfaz y no de la clase concreta.
- [ ] Extraer la interfaz solo cuando exista un punto de extensión previsible o extensión por terceros.
- [ ] Usar polimorfismo para tratar las implementaciones a través de la interfaz común.
- [ ] Declarar abstracto el método de creación de objetos y delegarlo a las subclases cuando persista el acoplamiento por la creación de objetos concretos.
