# Verificación de fidelidad — release-it

Reporte generado por el agente `notes-verifier`: contrasta cada apunte con el texto fuente del capítulo.

| Capítulo | Hallazgos | Alta | Media | Baja |
|---|---|---|---|---|
| cap00 | 0 | 0 | 0 | 0 |
| cap01 | 0 | 0 | 0 | 0 |
| cap02 | 0 | 0 | 0 | 0 |
| cap03 | 2 | 0 | 0 | 2 |
| cap04 | 0 | 0 | 0 | 0 |
| cap05 | 1 | 0 | 0 | 1 |
| cap06 | 0 | 0 | 0 | 0 |
| cap07 | 0 | 0 | 0 | 0 |
| cap08 | 1 | 0 | 0 | 1 |
| cap09 | 0 | 0 | 0 | 0 |
| cap10 | 0 | 0 | 0 | 0 |
| cap11 | 0 | 0 | 0 | 0 |
| cap12 | 1 | 0 | 1 | 0 |
| cap13 | 0 | 0 | 0 | 0 |
| cap14 | 0 | 0 | 0 | 0 |
| cap15 | 1 | 0 | 0 | 1 |
| cap16 | 0 | 0 | 0 | 0 |
| cap17 | 0 | 0 | 0 | 0 |

**Total:** 6 hallazgos (alta 0, media 1, baja 5) en 18 capítulos.

## Detalle

## cap00 — Preface (Prefacio)
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap01 — Living in Production (Vivir en producción)
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap02 — Case Study: The Exception That Grounded an Airline
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap03 — Stabilize Your System
Hallazgos: 2 (alta 0, media 0, baja 2)
- [baja] «volcar doce millones de mensajes en una cola a medianoche» → omite la fecha concreta del ejemplo; evidencia: «Dumping twelve million messages into a queue at midnight on November 21 is an impulse» (PDF p. 37)
- [baja] sección «Wrapping Up» omitida → el apunte no recoge el cierre que anticipa antipatrones y patrones de estabilidad (caps. 4 y 5); evidencia: «These are the stability antipatterns... deals with design and architecture patterns to defeat the antipatterns» (PDF p. 42)

## cap04 — Stability Antipatterns (Antipatrones de estabilidad)
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap05 — Stability Patterns (Patrones de estabilidad)
Hallazgos: 1 (alta 0, media 0, baja 1)
- [baja] «"you can't out-scale the world", PDF p.131» → la cita textual exacta aparece en el bloque Remember This de la p.132, no en la p.131 (donde la idea se parafrasea como "the world can always make more load than you can handle"); evidencia: «You can't out-scale the world.» (PDF p. 132)

## cap06 — Case Study: Phenomenal Cosmic Powers, Itty-Bitty Living Space
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap07 — Foundations
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap08 — Processes on Machines (Procesos en las máquinas)
Hallazgos: 1 (alta 0, media 0, baja 1)
- [baja] «una administradora hacía failovers semanales de BD durante seis meses» → omite que eran en horas pico, matiz presente en la fuente; evidencia: «weekly database failovers during peak hours for six months» (PDF p. 178)

## cap09 — Interconnect (Interconexión)
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap10 — Control Plane (Plano de control)
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap11 — Security (Seguridad)
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap12 — Case Study: Waiting for Godot (Caso de estudio: Esperando a Godot)
Hallazgos: 1 (alta 0, media 1, baja 0)
- [media] «Dos días después empiezan a planear el segundo intento» → invierte los tiempos: el relato dice que la planificación empieza esa misma tarde y es el segundo intento el que se programa para dos días después; evidencia: «That afternoon, we started planning the second attempt scheduled for two days hence» (PDF p. 246)

## cap13 — Design for Deployment (Diseñar para el despliegue)
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap14 — Handling Versions
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap15 — Case Study: Trampled by Your Own Customers (Caso de estudio: pisoteado por tus propios clientes)
Hallazgos: 1 (alta 0, media 0, baja 1)
- [baja] «El autor la usa de forma prescriptiva (crear la estructura de comunicación que quiere...)» → el texto fuente usa el término «proscriptive», no «prescriptive/prescriptiva»; la paráfrasis del sentido es fiel, pero el término difiere; evidencia: «I've since found Conway's law useful in a proscriptive mode—creating the communication structure that I wanted the software to embody» (PDF p. 283)

## cap16 — Adaptation (Adaptación)
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap17 — Chaos Engineering
Hallazgos: 0 (alta 0, media 0, baja 0)

## Estado de correcciones

El hallazgo de severidad media (cap12, orden temporal del segundo intento) se confirmó contra el texto fuente y se corrigió en el apunte. Los de severidad baja no se han modificado.
