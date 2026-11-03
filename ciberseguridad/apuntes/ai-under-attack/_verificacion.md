# Verificación de fidelidad — ai-under-attack

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
| cap08 | 0 | 0 | 0 | 0 |
| cap09 | 0 | 0 | 0 | 0 |
| cap10 | 0 | 0 | 0 | 0 |
| cap11 | 0 | 0 | 0 | 0 |
| cap12 | 0 | 0 | 0 | 0 |
| cap13 | 0 | 0 | 0 | 0 |
| cap14 | 0 | 0 | 0 | 0 |
| cap15 | 0 | 0 | 0 | 0 |
| cap16 | 0 | 0 | 0 | 0 |
| cap17 | 0 | 0 | 0 | 0 |
| cap18 | 0 | 0 | 0 | 0 |
| cap19 | 1 | 0 | 0 | 1 |
| cap20 | 0 | 0 | 0 | 0 |
| cap21 | 1 | 0 | 1 | 0 |
| cap22 | 0 | 0 | 0 | 0 |
| cap23 | 0 | 0 | 0 | 0 |
| cap25 | 0 | 0 | 0 | 0 |

**Total:** 5 hallazgos (alta 0, media 1, baja 4) en 25 capítulos.

## Detalle

## cap00 — Preface (Prefacio)
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap01 — Why AI Security Is Different
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap02 — Threat Modeling AI Systems
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap03 — The AI Attack Surface
Hallazgos: 2 (alta 0, media 0, baja 2)
- [baja] «en febrero de 2026 OpenAI informó a un comité de la Cámara de EE. UU.» → omite el paso intermedio de que el patrón "había pasado a la disputa OpenAI/DeepSeek" a comienzos de 2025 antes del informe de 2026; evidencia: «By early 2025, that pattern had moved into the OpenAI/DeepSeek dispute» (PDF p. 116)
- [baja] «Model extraction vía API» → no menciona la investigación de extracción estructural que muestra que algunas funciones de la API pueden filtrar propiedades más profundas del modelo; evidencia: «Structural extraction research has also shown that some API features can leak deeper model properties.» (PDF p. 116)

## cap04 — Foundations of AI Defense
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap05 — Anatomy of an AI System
Hallazgos: 1 (alta 0, media 0, baja 1)
- [baja] «el primer lugar donde la entrada externa se encuentra con el modelo» (PDF p. 148) → la cita es fiel pero la página es incorrecta: la frase aparece en la p. 149, no en la 148; evidencia: «the tokenizer is the first place where external input meets the model» (PDF p. 149)

## cap06 — Prompt Injection and Jailbreaking
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap07 — Memory, Context, and State Abuse
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap08 — Attacks on RAG Systems
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap09 — Agent Architecture and Vulnerabilities
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap10 — Agent Exploitation Techniques
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap11 — Attacks on Training Data and Model Integrity (Ataques a los datos de entrenamiento y la integridad del modelo)
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap12 — AI Red Teaming and Evaluation
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap13 — Securing AI Infrastructure, MLOps, and Runtime Environments
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap14 — Building Secure AI Applications and APIs
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap15 — Defensive Prompt Engineering
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap16 — Guardrails and Human Oversight
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap17 — External Dependencies, Supply Chain Integrity and Multi-Tenant Risk
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap18 — Securing AI Agents with Zero Trust Architecture
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap19 — AI Governance, Risk, and Compliance
Hallazgos: 1 (alta 0, media 0, baja 1)
- [baja] «"You cannot outsource accountability by buying an AI feature" (PDF p. 411)» → la cita se atribuye a la p.411, pero la frase completa aparece a caballo entre p.411 y p.412, de modo que el texto citado está en la p.412; evidencia: p.411 termina en «You» y p.412 comienza «cannot outsource accountability by buying an AI feature» (PDF p. 412)

## cap20 — AI Security Engineering
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap21 — AI Security Operations
Hallazgos: 1 (alta 0, media 1, baja 0)
- [media] «La mejora continua ... apoyada en MITRE ATLAS, OWASP, NIST AI RMF y madurez SANS» → en la sección de mejora continua la fuente no incluye NIST AI RMF entre las fuentes consumidas (solo aparece en las referencias); evidencia: «Consume MITRE ATLAS, OWASP, vendor reports, ISAC intelligence, and internal incident findings» (PDF p. 465)

## cap22 — Building Sustainable AI Security Programs
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap23 — The Future of AI Security
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap25 — Practitioner Toolkit
Hallazgos: 0 (alta 0, media 0, baja 0)

## Estado de correcciones

El único hallazgo de severidad media (cap22) es un matiz sobre las fuentes citadas en la mejora continua; se deja como está. Los de severidad baja no se han modificado.
