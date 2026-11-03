# Overview of Card Payments Industry (Panorama de la industria de pagos con tarjeta) — Estudio

## Tarjetas de repaso

P: ¿Qué expectativas distintas tienen consumidores, comerciantes y gobiernos sobre los medios de pago?
R: Disponibilidad, conveniencia, garantía de cobro, bajo coste, seguridad frente al fraude y trazabilidad fiscal.

P: ¿Qué fue el "First Supper" y qué originó?
R: En 1950, McNamara y Schneider fueron los primeros en decir "charge it"; ese arreglo se convirtió en Diners Club, el primer card scheme del mundo.

P: ¿Por qué el efectivo puntúa mal como medio de pago?
R: Se agota en el peor momento, se olvida, se roba, se falsifica y es difícil de rastrear y gravar.

P: ¿Cuáles son los pasos del flujo de un cheque?
R: El cliente lo rellena y firma, el merchant lo lleva al payee bank, y este lo lleva a una clearinghouse donde el drawee bank reembolsa al payee bank; si comparten banco se ahorra el clearing.

P: ¿Qué es un card scheme y quién puede gestionarlo?
R: Tarjetas y redes asociadas (infraestructura técnica, membresía, riesgo, compliance, marca, garantías); lo gestiona un consorcio de bancos, una empresa con ánimo de lucro o una empresa estatal.

P: ¿Qué funciones cumple el issuer?
R: Emite tarjetas según la marca, gestiona al cardholder, controla el open-to-pay amount, paga las transacciones de los acquirers, gestiona fraude, da crédito, cobra facturas y gestiona disputas por el titular.

P: ¿Qué funciones cumple el acquirer?
R: Gestiona la relación con el merchant, procesa transacciones según el scheme, presenta las autorizadas a los issuers para clearing, remite fondos y gestiona disputas por el comercio.

P: ¿Qué es un PSP (Payment Services Provider)?
R: Da una interfaz uniforme a todos los schemes soportados y gestiona las relaciones y conexiones técnicas con schemes y acquirer banks; muchos añaden servicios de valor.

P: ¿Qué diferencia a un PF (Payment Facilitator) de un PSP?
R: Un PF es un PSP que además da de alta a los comercios en nombre del acquirer y les desembolsa fondos.

P: ¿Qué es un ISO (Independent Sales Organization)?
R: Un agente que encuentra y da de alta nuevos clientes para acquirers y PSPs.

P: ¿En qué consiste el modelo three-party (cerrado)?
R: El propio card scheme adquiere las transacciones, liquida con merchants, emite tarjetas y factura a los cardholders; ejemplos: American Express, Diners Club, Discover.

P: ¿En qué consiste el modelo four-party (abierto)?
R: El card scheme actúa como rule setter y facilitador, pero delega issuing y acquiring a otras instituciones; ejemplos: Visa, MasterCard, UnionPay.

P: ¿Cuál es la diferencia clave de liquidación entre los dos modelos?
R: La ausencia o presencia de interchange fees como medio principal de liquidación mutua entre entidades de acquiring e issuing.

P: ¿Cuáles son los cinco pasos comunes de una transacción?
R: Identificación de la cuenta, verificación de la tarjeta, verificación del titular, mensaje de solicitud y respuesta.

P: ¿Qué organismos rigen la estandarización y el gobierno técnico?
R: ISO/IEC (protocolos y banda magnética), PCI Security Standards Council (seguridad) y EMVCo (chip y contactless).

## Preguntas de autoevaluación

P: ¿Por qué pagar con cheque, pese a sus medidas antifalsificación y datos legibles por máquina, no desplazó al efectivo?
R: Porque pagar con cheque exige más tiempo y esfuerzo que el efectivo. (Sección 1.1)

P: ¿Puede un business ser cardholder y un merchant no ser una empresa comercial? Explica.
R: Sí: un business puede ser cardholder con tarjeta corporativa, y un merchant puede ser una entidad municipal, gubernamental o una persona física. (Sección 1.2)

P: ¿Qué implica que una misma entidad asuma los roles de issuer y acquirer, y qué cambia si además es retail o commercial bank?
R: Es frecuente que coincidan; si el issuer es retail bank mantiene la checking account y debita directamente, y un acquirer que es commercial bank abona directamente las cuentas de sus comercios en lugar de usar wire transfers por un correspondent bank. (Sección 1.2)

P: ¿Qué ventajas y qué limitación tiene el modelo three-party frente al four-party?
R: Ventajas: máximo control de la experiencia, despliegue de cambios más simple y sin competencia in-brand; limitación: la expansión a nuevas geografías es difícil y recurre a franquicias y partnerships. (Sección 1.3)

P: ¿Por qué el panorama de esquemas puede resultar confuso?
R: Porque las franquicias representan esquemas three-party y a la vez actúan como acquirers e issuers de esquemas four-party. (Sección 1.3)

P: En el paso de verificación del titular, ¿cómo difieren card-present y card-not-present?
R: Present: la tarjeta pide PIN, cifrado por el terminal; CNP: el plug-in redirige a la página del issuer, que confirma identidad con contraseña estática o, más común, one-time password por SMS, y genera evidencia criptográfica. (Sección 1.4)

P: ¿Qué valida la red o el issuer en el paso de respuesta según sea present o CNP?
R: Cryptogram/PIN en card-present, o la evidencia criptográfica y el card check value en card-not-present, antes de aprobar o denegar. (Sección 1.4)

P: ¿Qué llevó a los gobiernos a ver los pagos como infraestructura pública?
R: La ubicuidad de las redes de pago e interbancarias, lo que impulsó estandarización, licencias más simples y regulación de precios. (Sección 1.1)

## Puntos a dominar

- Explicar por qué efectivo y cheques no cubren bien conveniencia, garantía, coste, seguridad frente al fraude y trazabilidad.
- Reconstruir el origen histórico: del "First Supper" y Diners Club a Amex, Visa, MasterCard, JCB, UnionPay, RuPay y Mir.
- Identificar cada actor del ecosistema (cardholder, merchant, card scheme, issuer, acquirer, PSP, PF, third-party processor, ISO, marketplace) y su función.
- Distinguir las responsabilidades del issuer frente a las del acquirer.
- Diferenciar esquemas three-party y four-party, sus ventajas y el papel de las interchange fees.
- Enumerar los cinco pasos de una transacción y contrastar sus mecanismos en card-present y card-not-present.
- Asociar cada organismo de gobierno (ISO/IEC, PCI Security Standards Council, EMVCo) con su ámbito.
