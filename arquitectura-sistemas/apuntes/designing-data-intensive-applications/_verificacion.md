# Verificación de fidelidad — designing-data-intensive-applications

Reporte generado por el agente `notes-verifier`: contrasta cada apunte con el texto fuente del capítulo.

| Capítulo | Hallazgos | Alta | Media | Baja |
|---|---|---|---|---|
| cap00 | 0 | 0 | 0 | 0 |
| cap01 | 1 | 0 | 1 | 0 |
| cap02 | 0 | 0 | 0 | 0 |
| cap03 | 0 | 0 | 0 | 0 |
| cap04 | 0 | 0 | 0 | 0 |
| cap05 | 0 | 0 | 0 | 0 |
| cap06 | 0 | 0 | 0 | 0 |
| cap07 | 0 | 0 | 0 | 0 |
| cap08 | 1 | 0 | 0 | 1 |
| cap09 | 0 | 0 | 0 | 0 |
| cap10 | 0 | 0 | 0 | 0 |
| cap11 | 0 | 0 | 0 | 0 |
| cap12 | 1 | 0 | 1 | 0 |

**Total:** 3 hallazgos (alta 0, media 2, baja 1) en 13 capítulos.

## Detalle

## cap00 — Preface (Prólogo)
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap01 — Reliable, Scalable, and Maintainable Applications
Hallazgos: 1 (alta 0, media 1, baja 0)
- [media] «"Las buenas operaciones pueden sortear las limitaciones de un software malo..." (PDF p. 19)» → cita con página incorrecta: el folio impreso es 19, pero la cita aparece en la página marcada [[PDF p.41]]; evidencia: «good operations can often work around the limitations of bad (or incomplete) software, but good software cannot run reliably with bad operations» (PDF p. 41)

## cap02 — Data Models and Query Languages
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap03 — Storage and Retrieval (Almacenamiento y recuperación)
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap04 — Encoding and Evolution
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap05 — Replication
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap06 — Partitioning (Particionamiento)
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap07 — Transactions (Transacciones)
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap08 — The Trouble with Distributed Systems (Los problemas de los sistemas distribuidos)
Hallazgos: 1 (alta 0, media 0, baja 1)
- [baja] «unos 12 fallos de red al mes … (PDF p. 279)» → cita con página incorrecta: usa el folio impreso (279) en vez del marcador de página del PDF; evidencia: «One study in a medium-sized datacenter found about 12 network faults per month» (PDF p. 301)

## cap09 — Consistency and Consensus (Consistencia y consenso)
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap10 — Batch Processing (Procesamiento por lotes)
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap11 — Stream Processing (Procesamiento de flujos)
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap12 — The Future of Data Systems (El futuro de los sistemas de datos)
Hallazgos: 1 (alta 0, media 1, baja 0)
- [media] «árboles de Merkle (usados en certificate transparency y en blockchains como Bitcoin o Ethereum)» → la fuente atribuye los árboles de Merkle a certificate transparency y al chequeo de integridad, pero no afirma que Bitcoin o Ethereum usen árboles de Merkle; esa atribución no está respaldada; evidencia: «certificate transparency is a security technology that relies on Merkle trees» (PDF p. 554)

## Estado de correcciones

Los dos hallazgos de severidad media (cap01, página de una cita; cap12, atribución de los árboles de Merkle) se confirmaron contra el texto fuente y se corrigieron en los apuntes. El de severidad baja no se ha modificado.
