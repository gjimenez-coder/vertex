# Verificación de fidelidad — design-patterns

Reporte generado por el agente `notes-verifier`: contrasta cada apunte con el texto fuente del capítulo.

| Capítulo | Hallazgos | Alta | Media | Baja |
|---|---|---|---|---|
| cap01 | 0 | 0 | 0 | 0 |
| cap02 | 1 | 0 | 0 | 1 |
| cap03 | 0 | 0 | 0 | 0 |
| cap04 | 0 | 0 | 0 | 0 |
| cap05 | 0 | 0 | 0 | 0 |
| cap06 | 0 | 0 | 0 | 0 |
| cap07 | 0 | 0 | 0 | 0 |
| cap08 | 0 | 0 | 0 | 0 |
| cap09 | 1 | 0 | 0 | 1 |
| cap10 | 0 | 0 | 0 | 0 |
| cap11 | 0 | 0 | 0 | 0 |
| cap12 | 0 | 0 | 0 | 0 |
| cap13 | 0 | 0 | 0 | 0 |
| cap14 | 1 | 0 | 0 | 1 |
| cap15 | 0 | 0 | 0 | 0 |
| cap16 | 0 | 0 | 0 | 0 |
| cap17 | 0 | 0 | 0 | 0 |
| cap18 | 0 | 0 | 0 | 0 |
| cap19 | 0 | 0 | 0 | 0 |
| cap20 | 0 | 0 | 0 | 0 |
| cap21 | 1 | 0 | 0 | 1 |
| cap22 | 0 | 0 | 0 | 0 |
| cap23 | 0 | 0 | 0 | 0 |
| cap24 | 1 | 0 | 0 | 1 |
| cap25 | 0 | 0 | 0 | 0 |
| cap26 | 0 | 0 | 0 | 0 |
| cap27 | 0 | 0 | 0 | 0 |
| cap28 | 0 | 0 | 0 | 0 |
| cap29 | 0 | 0 | 0 | 0 |
| cap30 | 1 | 0 | 0 | 1 |
| cap31 | 0 | 0 | 0 | 0 |
| cap32 | 0 | 0 | 0 | 0 |
| cap33 | 0 | 0 | 0 | 0 |
| cap34 | 0 | 0 | 0 | 0 |
| cap35 | 0 | 0 | 0 | 0 |

**Total:** 6 hallazgos (alta 0, media 0, baja 6) en 35 capítulos.

## Detalle

## cap01 — Conceptos básicos de POO (Basics of OOP)
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap02 — Los pilares de la POO (The Pillars of OOP)
Hallazgos: 1 (alta 0, media 0, baja 1)
- [baja] «La Abstracción es el modelo de un objeto o fenómeno del mundo real, limitado a un contexto específico» → la cita se corta y omite el cierre de la definición; evidencia: «limitado a un contexto específico, que representa todos los datos relevantes a este contexto con gran precisión, omitiendo el resto» (PDF p. 15)

## cap03 — Relaciones entre objetos
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap04 — ¿Qué es un patrón de diseño?
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap05 — Características del buen diseño (Features of good design)
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap06 — Encapsula lo que varía (Encapsulate What Varies)
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap07 — Programa a una interfaz, no a una implementación (Program to an interface, not an implementation)
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap08 — Favorece la composición sobre la herencia (Favor composition over inheritance)
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap09 — S: Single Responsibility Principle (S: Principio de responsabilidad única)
Hallazgos: 1 (alta 0, media 0, baja 1)
- [baja] «DESPUÉS: el comportamiento adicional queda en su propia clase, y cada clase tiene una sola razón para cambiar» → añade una coletilla no presente en la fuente; evidencia: «DESPUÉS: el comportamiento adicional está en su propia clase.» (PDF p. 57)

## cap10 — O: Principio de abierto/cerrado (Open/Closed Principle)
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap11 — L: Principio de sustitución de Liskov (Liskov Substitution Principle)
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap12 — I: Interface Segregation Principle (Principio de segregación de la interfaz)
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap13 — Dependency Inversion Principle (D: Principio de inversión de la dependencia)
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap14 — Factory Method (Método fábrica)
Hallazgos: 1 (alta 0, media 0, baja 1)
- [baja] «sabe que tienen `entrega`, pero no necesita conocer cómo funciona exactamente (PDF p. 84)» → página de la cita incorrecta: el pasaje aparece en la p. 83, no en la 84; evidencia: «El cliente sabe que todos los objetos de transporte deben tener el método entrega, pero no necesita saber cómo funciona exactamente» (PDF p. 83)

## cap15 — Abstract Factory (Fábrica abstracta)
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap16 — Builder (Constructor)
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap17 — Prototype (Prototipo)
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap18 — Singleton
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap19 — Adapter (Adaptador)
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap20 — Bridge (Puente)
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap21 — Composite (Objeto compuesto)
Hallazgos: 1 (alta 0, media 0, baja 1)
- [baja] «Relaciones con otros patrones ... (PDF p. 206)» → la cita atribuye todo el bloque a la p.206, pero Builder, Chain of Responsibility e Iteradores aparecen en la p.205; solo Visitor, Flyweight, Decorator y Prototype están en la p.206; evidencia: «Puedes utilizar Builder al crear árboles Composite complejos» (PDF p. 205)

## cap22 — Decorator (Decorador)
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap23 — Facade (Fachada)
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap24 — Flyweight (Peso mosca)
Hallazgos: 1 (alta 0, media 0, baja 1)
- [baja] «El código se complica: los nuevos miembros del equipo se preguntarán por qué el estado de una entidad se separó de tal manera (PDF p. 250-251)» → la cita de página es incorrecta para este punto; el texto sobre la complicación del código aparece en la p. 252, no en 250-251; evidencia: «El código se complica mucho. Los nuevos miembros del equipo siempre estarán preguntándose por qué el estado de una entidad se separó de tal manera» (PDF p. 252)

## cap25 — Proxy (Proxy)
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap26 — Chain of Responsibility (Cadena de responsabilidad)
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap27 — Command (Comando)
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap28 — Iterator (Iterador)
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap29 — Mediator (Mediador)
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap30 — Memento (Recuerdo)
Hallazgos: 1 (alta 0, media 0, baja 1)
- [baja] El apunte no incluye un apartado propio para la sección «Aplicabilidad» del capítulo → sección titulada omitida como apartado (su contenido sobre transacciones y violación de encapsulación sí aparece disperso en «Lo que necesitas saber» e «Ideas clave»); evidencia: «Aplicabilidad — Utiliza el patrón Memento cuando quieras producir instantáneas del estado del objeto» (PDF p. 355)

## cap31 — Observer (Observador)
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap32 — State (Estado)
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap33 — Strategy (Estrategia)
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap34 — Template Method (Método plantilla)
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap35 — Visitor (Visitante)
Hallazgos: 0 (alta 0, media 0, baja 0)
