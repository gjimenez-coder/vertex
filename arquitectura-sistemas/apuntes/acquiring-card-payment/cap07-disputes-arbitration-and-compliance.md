# Acquiring Card Payments — Ilya Dubinsky (CRC Press, Taylor & Francis, 2019)
## Capítulo 7 — Disputes, Arbitration and Compliance (Disputas, arbitraje y cumplimiento)

> Nota de extracción: el texto se obtuvo de la capa de texto del PDF; las citas usan la página del PDF `(PDF p. N)`.

## Lo que necesitas saber

Todos los miembros de un scheme están sujetos a los términos y condiciones de membresía y pasan pruebas de certificación antes del go-live y al introducir nuevos servicios o dispositivos, lo que asegura la conformidad técnica de sus sistemas. Además de ese testing (puntual o periódico), los schemes refuerzan la validez de las transacciones de autorización, clearing y disputa rechazando automáticamente las mal formateadas o reportando a los miembros sobre validez e integridad de datos.

Esos medios técnicos no pueden cubrir todos los comportamientos de miembros, titulares o comercios, incluyendo desviaciones intencionadas y errores honestos. Para gestionar estas desviaciones, los schemes soportan dos grandes procesos: la gestión de disputas y arbitraje (para resolver disputas entre participantes) y el compliance de scheme (para tratar el incumplimiento de las reglas).

Sales sabiendo cómo fluye una disputa iniciada por el issuer: retrieval request, chargeback, representment, second chargeback y, si no hay acuerdo, pre-arbitraje y arbitraje. También entiendes variantes modernas como allocation vs. collaboration, el streamlined lifecycle para problemas técnicos, los liability shifts y cómo funciona el proceso de compliance entre miembros.

## Ciclo de vida genérico de la disputa (7.1.1)

El proceso varía ligeramente entre schemes, pero en general es un subconjunto del flujo no arbitrado descrito en la tabla 7.1, iniciado por el issuer:

- **Retrieval request** (issuer): solicitud de documentación de soporte de una transacción. El acquirer responde con fulfillment, non-fulfillment explícito o sin respuesta.
- **Chargeback** (issuer): disputa real de la transacción original. El acquirer responde con representment, acknowledgement o nada; si no responde, el chargeback se considera aceptado por el acquirer.
- **Second chargeback** (issuer): nuevo desafío con documentación adicional. El acquirer responde con nada, pre-arbitraje o arbitraje; si no responde, el chargeback se considera aceptado.

El flujo arbitrado puede incluir presentar un caso de pre-arbitraje con el scheme, dando a la otra parte la opción de ceder y evitar el riesgo de una decisión desfavorable, lo que conlleva una tarifa relativamente alta. Suele ser posible saltar ese paso e ir directo a arbitraje, acudiendo al equipo de resolución de disputas del scheme.

## Retrieval requests y fulfillments (7.1.2)

Herramienta opcional del issuer para investigar disputas potenciales: pide al acquirer documentación de soporte de una transacción. El acquirer puede no responder, responder aportando documentos (fulfillment) o responder sin documentos (non-fulfillment); no es obligatorio responder. La documentación suele incluir el sales draft. En e-commerce o EMV, donde el titular no firma recibo, los datos ya están en los sistemas del acquirer o en la red; cuando sistemas legacy exigen un sales draft, el acquirer genera un "substitute draft" o sub-draft con los detalles en una imagen. Suele convenir al acquirer aportar evidencia para evitar un chargeback posterior.

## Chargebacks y representments (7.1.3)

Un chargeback es una demanda para resarcir la pérdida del titular en una transacción fraudulenta o disputada. Lo inicia el issuer en nombre del titular y llega al acquirer como registro financiero (en un archivo de settlement entrante) o como caso en el sistema online de gestión de disputas del scheme.

Cada chargeback indica la razón (fraude, problema técnico o disputa comercio-titular) y, si la regla lo exige, el issuer aporta documentación. Puede ser por el importe total o parcial; caben múltiples chargebacks parciales sobre una misma transacción siempre que su suma no exceda la compra original. Antes había decenas de reason codes muy específicos; luego se redujeron a unos pocos, simplificando el trabajo del issuer y cargando más al equipo de disputas del acquirer.

Al entregarse el chargeback, su importe se cobra al acquirer deduciéndolo del settlement correspondiente. Si el acquirer está de acuerdo o cree que el coste de seguir supera el beneficio, puede enviar un acknowledgement o no hacer nada. El acquirer puede absorber el coste o trasladarlo al comercio. Razones posibles de chargeback:

- Fallos técnicos, errores en el punto de venta, tipos de conversión de divisa erróneos y presentments tardíos de la transacción original.
- Fraude, transacción no autorizada por el titular, facturación recurrente de un servicio ya cancelado.
- Bienes o servicios no entregados o prestados, total o parcialmente.
- Disputas especiales o específicas de industria (p. ej., reglas para cargos de alquiler de coches; derecho automático de chargeback por bienes falsificados).

Si el acquirer discrepa, hace un **representment** (o second presentment): envía detalles o documentos al issuer vía scheme más un registro financiero, y el scheme le acredita el importe. A veces basta el registro financiero (chargeback duplicado, o aportar el número de referencia de un refund ya efectuado). Otras veces hacen falta documentos: sales drafts con firma o evidencia de envío/prestación. En card-not-present (e-commerce, autorizaciones por PIN) sin firma, los schemes suelen exigir igualmente un sales draft, generado desde la base de datos del acquirer (substitute draft/sub-draft). El representment es parcial si no cubre el importe total y completo si lo cubre. En una transacción de 100 EUR, un representment de 50 EUR es parcial tanto frente a un chargeback de 50 como de 100; uno de 100 EUR es completo frente a un chargeback de 100 (ver tabla 7.2).

## Second chargeback (7.1.4)

Si el issuer discrepa de los materiales del representment, ciertos schemes permiten un chargeback adicional, llamado second chargeback o arbitration chargeback: el issuer es acreditado y el acquirer debitado por el importe disputado. Algunos schemes lo usan como paso extra del proceso no arbitrado, pero el número de schemes que lo soportan disminuye con los años.

## Allocation vs. collaboration (7.1.5)

En años recientes los schemes introdujeron un proceso "cortocircuitado" para chargebacks técnicos y de fraude: en ciertos casos no hay proceso adversarial y el scheme asigna (allocation) la parte que soporta la responsabilidad. No se puede seguir de forma no arbitrada más allá de ese punto; desafiarlo requiere pre-arbitraje o arbitraje, mucho más caros. Se usa el término allocation (decisión del scheme sobre la responsabilidad) frente a collaboration (intercambio no arbitrado completo).

## Pre-arbitraje y arbitraje (7.1.6)

Si los miembros no llegan a una conclusión por la vía no arbitrada, acuden al scheme para análisis y decisión del caso: eso es el arbitraje, disparado por la última parte del flujo. En algunas soluciones lo precede el pre-arbitraje, cuando la parte notifica a su contraparte que va a acudir al scheme, dando una última oportunidad de acordar. Al ser un proceso manual con especialistas del scheme, se desanima a los miembros de recurrir a él innecesariamente y su esfuerzo se compensa con tarifas.

## Liability shift (7.1.7)

Reglas que niegan a una parte sus derechos habituales de disputa, usadas para motivar la adopción de funciones tecnológicas de prevención de fraude, autenticación y protección del titular (las reglas concretas varían):

- Si una transacción se autenticó con 3D Secure o EMV 3D-Secure, el issuer no puede disputarla alegando que el titular no la reconoce; si llega tal disputa, el acquirer la rebate (representment) sobre la base del liability shift.
- La implementación de EMV vino con un liability shift a favor de la parte que lo implementa: una transacción en terminal solo-magstripe con tarjeta con chip puede ser disputada por el issuer por no estar autorizada por el titular, y el acquirer no puede rebatirla salvo por un tecnicismo en el propio mensaje de chargeback.

## Streamlined lifecycle (7.1.8)

Originalmente el ciclo era idéntico para problemas técnicos (p. ej., discrepancia de atributos entre autorización y clearing), fraude y disputas genuinas comercio-titular. Con la evolución de los sistemas de red hacia más validaciones e integridad de datos, los schemes introdujeron un proceso más ligero para problemas técnicos resolubles solo por atributos de la transacción. El streamlined implica la allocation de responsabilidad al presentarse la disputa: el scheme decide la parte ganadora y ejecuta los movimientos financieros sin intercambio de mensajes. Tras esa allocation, issuer y acquirer pueden apelar y llevar el caso a arbitraje.

## Compliance (7.2)

En cualquier momento del ciclo de disputa, o al margen de él, un miembro puede plantear una queja de cumplimiento de reglas contra otro miembro o contra el propio scheme. El procedimiento típico permite (pero no exige) notificar primero al complainee con una pre-compliance notification describiendo el comportamiento no conforme y dándole oportunidad de resolverlo antes de que intervenga el equipo de compliance del scheme. Si la respuesta no satisface al complainer, este abre un caso de compliance gestionado por personal del scheme. Escenarios ilustrativos:

- **Escenario 1:** un acquirer reenviaba repetidamente transacciones card-not-present y card-on-file pese a que el result code del issuer indicaba que la autorización de la tarjeta había sido revocada; cada decline genera una tarifa que el issuer paga al scheme. Como el servicio de autorización del scheme no bloqueaba esas transacciones, el issuer abrió un caso de compliance contra el acquirer.
- **Escenario 2:** un acquirer recibió varios chargebacks de un issuer sobre transacciones que, al estar plenamente autenticadas con 3D Secure, debían gozar del liability shift. La investigación con las herramientas y el apoyo del scheme mostró que se habían enviado correctamente pero llegaron al issuer con el indicador de autenticación completa eliminado. Para forzar acción del scheme, el acquirer abrió un caso de compliance contra el scheme.

## Ideas clave

- Los schemes combinan certificación/validación técnica con dos procesos de gobierno: gestión de disputas/arbitraje y compliance.
- El flujo no arbitrado de disputa va retrieval request → chargeback → representment → second chargeback, siempre iniciado por el issuer.
- No responder a un chargeback equivale a aceptarlo; responder a un retrieval request es opcional pero conviene al acquirer para evitar chargebacks.
- Chargebacks y representments pueden ser parciales o totales; la suma de chargebacks parciales no puede superar el importe original.
- Los reason codes se redujeron de decenas a unos pocos, trasladando carga del issuer al acquirer.
- Allocation (el scheme decide la responsabilidad) frente a collaboration (intercambio no arbitrado completo); el streamlined lifecycle aplica allocation a problemas técnicos.
- Pre-arbitraje y arbitraje son el último recurso, manuales y con tarifas altas que desincentivan su uso innecesario.
- Los liability shifts (3D Secure, EMV) premian la adopción tecnológica negando derechos de disputa a quien no la implementa.
- El compliance permite a un miembro reclamar contra otro miembro o contra el propio scheme, con pre-compliance notification opcional previa.
