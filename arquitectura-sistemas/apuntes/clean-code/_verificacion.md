# Verificación de fidelidad — clean-code

Reporte generado por el agente `notes-verifier`: contrasta cada apunte con el texto fuente del capítulo.

| Capítulo | Hallazgos | Alta | Media | Baja |
|---|---|---|---|---|
| cap00 | 0 | 0 | 0 | 0 |
| cap01 | 0 | 0 | 0 | 0 |
| cap02 | 0 | 0 | 0 | 0 |
| cap03 | 0 | 0 | 0 | 0 |
| cap04 | 1 | 0 | 0 | 1 |
| cap05 | 0 | 0 | 0 | 0 |
| cap06 | 0 | 0 | 0 | 0 |
| cap07 | 0 | 0 | 0 | 0 |
| cap08 | 0 | 0 | 0 | 0 |
| cap09 | 0 | 0 | 0 | 0 |
| cap10 | 0 | 0 | 0 | 0 |
| cap11 | 1 | 0 | 0 | 1 |
| cap12 | 0 | 0 | 0 | 0 |
| cap13 | 0 | 0 | 0 | 0 |
| cap14 | 0 | 0 | 0 | 0 |
| cap15 | 1 | 1 | 0 | 0 |
| cap16 | 0 | 0 | 0 | 0 |
| cap17 | 0 | 0 | 0 | 0 |
| cap18 | 0 | 0 | 0 | 0 |
| cap19 | 1 | 0 | 0 | 1 |

**Total:** 4 hallazgos (alta 1, media 0, baja 3) en 20 capítulos.

## Detalle

## cap00 — Introduction
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap01 — Clean Code
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap02 — Meaningful Names
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap03 — Functions (Funciones)
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap04 — Comments (Comentarios)
Hallazgos: 1 (alta 0, media 0, baja 1)
- [baja] «Los comentarios son un mal necesario... (PDF p. 85)» → la afirmación del "mal necesario" aparece en la p. 84, no en la 85; la cita lleva la página incorrecta; evidencia: «comments are, at best, a necessary evil» (PDF p. 84)

## cap05 — Formatting (Formato)
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap06 — Objects and Data Structures
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap07 — Error Handling (Manejo de errores)
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap08 — Boundaries (Límites)
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap09 — Unit Tests
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap10 — Classes (Clases)
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap11 — Systems (Sistemas)
Hallazgos: 1 (alta 0, media 0, baja 1)
- [baja] «"Una arquitectura óptima consiste en dominios de concern modularizados, cada uno implementado con POJOs" (PDF p. 198)» → la cita aparece en la página anterior; evidencia: «An optimal system architecture consists of modularized domains of concern, each of which is implemented with Plain Old Java (or other) Objects.» (PDF p. 197)

## cap12 — Emergence (Emergencia)
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap13 — Concurrency (Concurrencia)
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap14 — Successive Refinement (Refinamiento sucesivo)
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap15 — JUnit Internals (Interioridades de JUnit)
Hallazgos: 1 (alta 1, media 0, baja 0)
- [alta] «escribiendo JUnit en tres horas durante un vuelo a Atlanta (PDF p. 283)» → el nombre del coautor se copió como «Erich Gamma», pero la fuente escribe «Eric Gamma»; evidencia: «it began with Kent Beck and Eric Gamma together on a plane to Atlanta» (PDF p. 283)

## cap16 — Refactoring SerialDate
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap17 — Smells and Heuristics
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap18 — Appendix A: Concurrency II
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap19 — Epilogue (Epílogo)
Hallazgos: 1 (alta 0, media 0, baja 1)
- [baja] «Elisabeth Hendrickson» → el apellido en la fuente aparece escrito sin la primera «n»; evidencia: «Elisabeth Hedrickson1 handed me a green wrist band» (PDF p. 442)

## Estado de correcciones

El único hallazgo de severidad alta (cap15, «Erich Gamma» frente a «Eric Gamma») es un falso positivo: el libro tiene una errata en el nombre y el apunte usa el nombre correcto, Erich Gamma. No se modificó.
