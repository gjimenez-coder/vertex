# Disputes, Arbitration and Compliance (Disputas, arbitraje y cumplimiento) — Estudio

## Tarjetas de repaso

P: ¿Qué dos grandes procesos de gobierno soportan los schemes para gestionar desviaciones de comportamiento que el testing técnico no cubre? / R: La gestión de disputas y arbitraje (para resolver disputas entre participantes) y el compliance de scheme (para tratar el incumplimiento de las reglas).

P: ¿Cuál es el orden del flujo no arbitrado de disputa y quién lo inicia siempre? / R: Retrieval request → chargeback → representment → second chargeback, siempre iniciado por el issuer.

P: ¿Qué es un retrieval request y es obligatorio responderlo? / R: Es una solicitud opcional del issuer de documentación de soporte de una transacción; el acquirer no está obligado a responder, pero suele convenirle aportar evidencia para evitar un chargeback posterior.

P: ¿Qué es un chargeback? / R: Una demanda para resarcir la pérdida del titular en una transacción fraudulenta o disputada, iniciada por el issuer en nombre del titular.

P: ¿Qué ocurre si el acquirer no responde a un chargeback? / R: El chargeback se considera aceptado por el acquirer; su importe se le cobra deduciéndolo del settlement correspondiente.

P: ¿Qué es un representment (second presentment)? / R: La respuesta del acquirer que discrepa del chargeback, enviando detalles o documentos al issuer vía scheme junto a un registro financiero, con lo que el scheme le acredita el importe.

P: ¿Qué es un substitute draft o sub-draft y cuándo se usa? / R: Un sales draft generado desde la base de datos del acquirer (con los detalles en una imagen), usado en e-commerce/EMV sin firma cuando los schemes o sistemas legacy exigen igualmente un sales draft.

P: ¿Qué es el second chargeback (arbitration chargeback)? / R: Un chargeback adicional que permiten ciertos schemes cuando el issuer discrepa del representment: el issuer es acreditado y el acquirer debitado; el número de schemes que lo soportan disminuye con los años.

P: ¿Cuál es la diferencia entre allocation y collaboration? / R: Allocation es la decisión del scheme sobre qué parte soporta la responsabilidad; collaboration es el intercambio no arbitrado completo entre las partes.

P: ¿Qué es el arbitraje y qué lo precede a veces? / R: Es el análisis y decisión del caso por el scheme cuando los miembros no concluyen por la vía no arbitrada; a veces lo precede el pre-arbitraje, en el que la parte notifica a su contraparte que acudirá al scheme, dándole una última oportunidad de acordar.

P: ¿Qué es un liability shift? / R: Reglas que niegan a una parte sus derechos habituales de disputa para motivar la adopción de funciones tecnológicas de prevención de fraude, autenticación y protección del titular.

P: ¿Cómo afecta el liability shift a una transacción autenticada con 3D Secure o EMV 3D-Secure? / R: El issuer no puede disputarla alegando que el titular no la reconoce; si llega tal disputa, el acquirer la rebate (representment) sobre la base del liability shift.

P: ¿Qué caracteriza al streamlined lifecycle? / R: Un proceso más ligero para problemas técnicos resolubles solo por atributos de la transacción, que aplica allocation de responsabilidad al presentarse la disputa; el scheme decide y ejecuta los movimientos financieros sin intercambio de mensajes, y después las partes pueden apelar a arbitraje.

P: ¿Pueden los chargebacks y representments ser parciales? / R: Sí; caben múltiples chargebacks parciales sobre una misma transacción siempre que su suma no exceda la compra original, y un representment es parcial si no cubre el importe total y completo si lo cubre.

P: ¿Contra quién puede un miembro plantear una queja de compliance y qué paso opcional la precede? / R: Contra otro miembro o contra el propio scheme; opcionalmente precede una pre-compliance notification que describe el comportamiento no conforme y da oportunidad de resolverlo antes de que intervenga el equipo de compliance.

## Preguntas de autoevaluación

P: ¿Por qué los medios técnicos (certificación y validación de transacciones) no bastan para gobernar el ecosistema del scheme? / R: Porque no pueden cubrir todos los comportamientos de miembros, titulares o comercios, incluidas desviaciones intencionadas y errores honestos; para eso existen la gestión de disputas/arbitraje y el compliance. (Lo que necesitas saber)

P: ¿Qué tres tipos de respuesta puede dar el acquirer a un retrieval request? / R: No responder, responder aportando documentos (fulfillment) o responder sin documentos (non-fulfillment). (7.1.2)

P: ¿Qué efecto tuvo la reducción de reason codes de decenas a unos pocos? / R: Simplificó el trabajo del issuer y cargó más trabajo al equipo de disputas del acquirer. (7.1.3)

P: En una transacción de 100 EUR, ¿por qué un representment de 50 EUR es parcial tanto frente a un chargeback de 50 como de 100? / R: Porque un representment es parcial si no cubre el importe total; 50 EUR no cubre el total de la transacción, por lo que es parcial en ambos casos, mientras que uno de 100 EUR sería completo frente a un chargeback de 100. (7.1.3, tabla 7.2)

P: ¿Qué limitación impone el proceso de allocation respecto a seguir disputando? / R: No se puede continuar de forma no arbitrada más allá de ese punto; desafiar la allocation requiere pre-arbitraje o arbitraje, mucho más caros. (7.1.5)

P: ¿Por qué los schemes desincentivan el uso innecesario del arbitraje? / R: Porque es un proceso manual con especialistas del scheme; se desanima a los miembros de recurrir a él innecesariamente y el esfuerzo se compensa con tarifas (relativamente altas). (7.1.6)

P: En el escenario 1 de compliance, ¿por qué el issuer abrió un caso contra el acquirer? / R: Porque el acquirer reenviaba repetidamente transacciones card-not-present y card-on-file pese a que el result code indicaba autorización revocada, generando tarifas de decline que el issuer pagaba, y el servicio de autorización del scheme no las bloqueaba. (7.2)

P: En el escenario 2, ¿por qué el acquirer abrió un caso de compliance contra el propio scheme? / R: Porque transacciones plenamente autenticadas con 3D Secure, que debían gozar del liability shift, llegaron al issuer con el indicador de autenticación completa eliminado pese a haberse enviado correctamente, de modo que para forzar acción abrió el caso contra el scheme. (7.2)

## Puntos a dominar

- Distinguir los dos procesos de gobierno del scheme (disputas/arbitraje y compliance) frente a la certificación y validación técnica.
- Reproducir de memoria el flujo no arbitrado: retrieval request → chargeback → representment → second chargeback, siempre iniciado por el issuer.
- Recordar que no responder a un chargeback equivale a aceptarlo, y que responder a un retrieval request es opcional pero conviene al acquirer.
- Diferenciar chargeback/representment parcial vs. completo y la regla de que la suma de parciales no supera el importe original.
- Separar allocation (decisión del scheme) de collaboration (intercambio no arbitrado completo) y ubicar el streamlined lifecycle como allocation para problemas técnicos.
- Explicar pre-arbitraje y arbitraje como último recurso manual, con tarifas que desincentivan su uso.
- Relacionar los liability shifts (3D Secure, EMV) con el incentivo a adoptar tecnología de autenticación.
- Identificar que el compliance puede dirigirse contra otro miembro o contra el propio scheme, con pre-compliance notification opcional.
