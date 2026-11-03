# Verificación de fidelidad — web-application-security

Reporte generado por el agente `notes-verifier`: contrasta cada apunte con el texto fuente del capítulo.

| Capítulo | Hallazgos | Alta | Media | Baja |
|---|---|---|---|---|
| cap00 | 2 | 0 | 2 | 0 |
| cap01 | 0 | 0 | 0 | 0 |
| cap02 | 0 | 0 | 0 | 0 |
| cap03 | 0 | 0 | 0 | 0 |
| cap04 | 0 | 0 | 0 | 0 |
| cap05 | 1 | 0 | 0 | 1 |
| cap06 | 1 | 0 | 0 | 1 |
| cap07 | 0 | 0 | 0 | 0 |
| cap08 | 1 | 0 | 0 | 1 |
| cap09 | 0 | 0 | 0 | 0 |
| cap10 | 0 | 0 | 0 | 0 |
| cap11 | 0 | 0 | 0 | 0 |
| cap12 | 0 | 0 | 0 | 0 |
| cap13 | 0 | 0 | 0 | 0 |
| cap14 | 1 | 0 | 1 | 0 |
| cap15 | 1 | 1 | 0 | 0 |
| cap16 | 0 | 0 | 0 | 0 |
| cap17 | 0 | 0 | 0 | 0 |
| cap18 | 0 | 0 | 0 | 0 |
| cap19 | 0 | 0 | 0 | 0 |
| cap20 | 0 | 0 | 0 | 0 |
| cap21 | 0 | 0 | 0 | 0 |
| cap22 | 0 | 0 | 0 | 0 |
| cap23 | 1 | 0 | 0 | 1 |
| cap24 | 0 | 0 | 0 | 0 |
| cap25 | 0 | 0 | 0 | 0 |
| cap26 | 0 | 0 | 0 | 0 |
| cap27 | 0 | 0 | 0 | 0 |
| cap28 | 0 | 0 | 0 | 0 |
| cap29 | 0 | 0 | 0 | 0 |
| cap30 | 0 | 0 | 0 | 0 |
| cap31 | 1 | 0 | 0 | 1 |
| cap32 | 1 | 0 | 0 | 1 |
| cap33 | 0 | 0 | 0 | 0 |
| cap34 | 0 | 0 | 0 | 0 |
| cap35 | 0 | 0 | 0 | 0 |
| cap36 | 1 | 0 | 0 | 1 |
| cap37 | 0 | 0 | 0 | 0 |
| cap38 | 1 | 0 | 0 | 1 |

**Total:** 12 hallazgos (alta 1, media 3, baja 8) en 39 capítulos.

## Detalle

## cap00 — Preface (Prólogo)
Hallazgos: 2 (alta 0, media 2, baja 0)
- [media] «Las habilidades mínimas (PDF p. 15)» → página incorrecta; la lista de habilidades mínimas aparece en p. 9; evidencia: «Minimum Required Skills […] You can write basic CRUD (create, read, update, delete) programs» (PDF p. 9)
- [media] «"most software systems are easy to break into" sin defensas (PDF p. 14)» → página incorrecta; la cita está en p. 15; evidencia: «Without any defenses, most software systems are easy to break into» (PDF p. 15)

## cap01 — The History of Software Security
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap02 — Introduction to Web Application Reconnaissance
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap03 — The Structure of a Modern Web Application
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap04 — Finding Subdomains
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap05 — API Analysis (Análisis de APIs)
Hallazgos: 1 (alta 0, media 0, baja 1)
- [baja] «más allá de eso hay que hacer suposiciones informadas y probarlas manualmente» → omite el matiz de la fuente sobre que automatizar el descubrimiento sin analizar peticiones existentes sería fácil de detectar y registrar; evidencia: «It's possible to automate the discovery... would be very easy to detect and log» (PDF p. 124)

## cap06 — Identifying Third-Party Dependencies
Hallazgos: 1 (alta 0, media 0, baja 1)
- [baja] «"The page you were looking for doesn't exist", PDF p. 137» → cita con página incorrecta, aparece en la p. 138; evidencia: «a box with the words "The page you were looking for doesn't exist" (see Figure 6-4)» (PDF p. 138)

## cap07 — Identifying Weak Points in Application Architecture
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap08 — Part I Summary (Resumen de la Parte I)
Hallazgos: 1 (alta 0, media 0, baja 1)
- [baja] El apunte omite el cierre personal del autor → no recoge el párrafo final sobre que la forma de acumular, registrar y distribuir técnicas queda a criterio del lector y el deseo de que las bases del libro sean una piedra angular del toolkit; evidencia: «the way you choose to accumulate, record, and distribute these techniques is up to you» (PDF p. 153)

## cap09 — Introduction to Hacking Web Applications
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap10 — Cross-Site Scripting
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap11 — Cross-Site Request Forgery
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap12 — XML External Entity
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap13 — Injection
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap14 — Denial of Service
Hallazgos: 1 (alta 0, media 1, baja 0)
- [media] «cadenas de longitud par de `ababab...` tardan <1 ms» → la fuente muestra que la entrada de 28 caracteres (longitud par) tarda >1 ms, no <1 ms; la generalización cambia el matiz; evidencia: «ababababababababababababab (28 chars) >1 ms» (PDF p. 229)

## cap15 — Attacking Data and Objects
Hallazgos: 1 (alta 1, media 0, baja 0)
- [alta] «reconocer y explotar cuatro clases de ataque: mass assignment, IDOR, y los ataques de serialización» → cifra inventada e incoherente: enumera solo tres tipos y la fuente no menciona "cuatro clases"; evidencia: «methods of exploiting data while it is being stored in the form of objects and being operated on via functions» (PDF p. 238)

## cap16 — Client-Side Attacks
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap17 — Exploiting Third-Party Dependencies
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap18 — Business Logic Vulnerabilities
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap19 — Part II Summary
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap20 — Securing Modern Web Applications
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap21 — Secure Application Architecture
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap22 — Secure Application Configuration
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap23 — Secure User Experience
Hallazgos: 1 (alta 0, media 0, baja 1)
- [baja] El apunte omite la sección «Summary» del capítulo → sección de cierre no recogida como apartado; evidencia: «Summary … a good user experience can be used to guide end users toward employing an application in a more secure manner» (PDF p. 333)

## cap24 — Threat Modeling Applications
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap25 — Reviewing Code for Security (Revisión de código en busca de seguridad)
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap26 — Vulnerability Discovery
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap27 — Vulnerability Management (Gestión de vulnerabilidades)
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap28 — Defending Against XSS Attacks
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap29 — Defending Against CSRF Attacks
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap30 — Defending Against XXE
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap31 — Defending Against Injection
Hallazgos: 1 (alta 0, media 0, baja 1)
- [baja] «"each module in a software system should only have access to the data and functionality required for that module to operate correctly." (PDF p. 410)» → página de la cita incorrecta; evidencia: la cita aparece tras el marcador de página siguiente, «each module in a software system should only have access to the data and functionality required» (PDF p. 411)

## cap32 — Defending Against DoS
Hallazgos: 1 (alta 0, media 0, baja 1)
- [baja] «El regex DoS se previene con revisión de código […] apoyándote en herramientas OSS» → se omite la mitigación del resumen con herramienta de análisis estático tipo linter; evidencia: «implementing a static analysis tool (like a linter) to scan regular expressions» (PDF p. 417)

## cap33 — Defending Data and Objects
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap34 — Defense Against Client-Side Attacks
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap35 — Securing Third-Party Dependencies
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap36 — Mitigating Business Logic Vulnerabilities
Hallazgos: 1 (alta 0, media 0, baja 1)
- [baja] «A1 tiende a 7 frente al constante 6 de A2» → se omite la cifra de ineficiencia relativa que da la fuente; evidencia: «over time A1 trends toward 7, which makes it 16% less efficient» (PDF p. 440)

## cap37 — Part III Summary
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap38 — Conclusion (Conclusión)
Hallazgos: 1 (alta 0, media 0, baja 1)
- [baja] el apunte omite la intervención del gobierno al describir el hacking temprano → falta el hecho de que la US Government Accountability Office estableció por primera vez leyes oficiales sobre hacking; evidencia: «The US Government Accountability Office stepped in for the first time in history and set forth official laws concerning hacking» (PDF p. 447)

## Estado de correcciones

Los hallazgos de severidad alta y media (cap00, cap14, cap15) se revisaron contra el texto fuente, se confirmaron y se corrigieron en los apuntes. Los hallazgos de severidad baja no se han modificado.
