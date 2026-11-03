# Acquiring Card Payments — Ilya Dubinsky (CRC Press, Taylor & Francis, 2019)
## Capítulo 1 — Overview of Card Payments Industry (Panorama de la industria de pagos con tarjeta)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas usan la página del PDF.

## Lo que necesitas saber

El capítulo introduce la industria de pagos con tarjeta desde su origen histórico hasta su ecosistema actual. La tesis es que el pago evolucionó junto con nuestra comprensión del dinero: consumidores, comerciantes y gobiernos tienen expectativas distintas (disponibilidad, conveniencia, garantía de cobro, bajo coste, seguridad frente al fraude y trazabilidad fiscal), y los medios de pago anteriores —efectivo, billetes, cheques y traveller's cheques— no las satisfacían bien del todo.

Sales sabiendo de dónde viene la industria (el "First Supper" y Diners Club), quiénes son los actores clave (cardholder, merchant, card scheme, issuer, acquirer, PSP, PF, procesadores, ISO, marketplace), la diferencia entre esquemas de tres y cuatro partes, y los pasos comunes de una transacción en escenarios card-present y card-not-present.

El capítulo también sitúa el marco de estandarización y gobierno: ISO/IEC para protocolos y bandas magnéticas, PCI Security Standards Council para seguridad, y EMVCo para chip y contactless.

## El ejemplo que recorre el capítulo

El hilo conductor es el "First Supper". En 1949, en Nueva York, el empresario Frank McNamara no pudo pagar la cena porque se dejó la cartera en otro traje. Junto con su abogado Frank Schneider ideó un club cuyos miembros firmaban sus cenas y liquidaban la cuenta más tarde. En febrero de 1950 ambos fueron los primeros en decir "charge it"; ese arreglo se convirtió en Diners Club, el primer card scheme del mundo. Despegó de inmediato: 20.000 miembros a fin de 1950, el doble en 1951, y presencia en Canadá, Cuba y Francia en dos años.

## 1.1 The First Supper

El efectivo puntúa mal en casi todas las métricas: se agota en el peor momento, se olvida, se roba (pickpocketing, atracos), se falsifica (monedas y billetes desde tiempos inmemoriales) y es difícil de rastrear y gravar, por lo que los gobiernos recelan de las operaciones de alto volumen en efectivo.

El cheque contiene indicación del drawee u obligor, identificación de la cuenta a debitar, medidas antifalsificación y una firma. El flujo: el cliente lo rellena y firma; el merchant lo lleva al payee bank para depositarlo o cobrarlo; el banco lo lleva a una clearinghouse donde el drawee bank reembolsa al payee bank. Si cliente y comerciante comparten banco, se ahorra el clearing. Los avances técnicos añadieron datos legibles por máquina y hoy basta una foto con el smartphone para depositarlo. Aun así, pagar con cheque exige más tiempo y esfuerzo que el efectivo.

Tras Diners siguieron otros: American Express (1958, tarjetas T&E, travel and entertainment); Bank of America (1959, intento de tarjeta de "revolving credit" que no exigía liquidar todo el saldo cada mes, después Visa). En 1961 se fundaron Japan Credit Bureau y Osaka Credit Bureau; en 1965 Eurocard International en Bruselas; en 1967 Cartes Bancaire (asociación de 6 bancos franceses) procesó su primera transacción y cuatro bancos de California crearon Master Charge: The Interbank Card, que a fines de los 70 pasó a ser MasterCard.

Movimientos posteriores: Eurocard International se convirtió en Europay International y en 1992 lanzó con MasterCard el joint venture Maestro; diez años después MasterCard adquirió Europay. Japan Credit Bureau se fusionó con Osaka Credit Bureau. Sears lanzó Discover, que luego adquirió Diners. En mercados emergentes: China Union Pay (2002, luego UnionPay) creció hasta volverse global, a la par o superando a Visa y Mastercard en volumen; RuPay en India (2012); y NSPK en Rusia (2014, tras sanciones occidentales), comercializada como Mir.

Con internet y el móvil surgieron PayPal, AliPay, service providers, ISOs, vendors tecnológicos, wallets digitales y móviles, marketplaces, crowdfunding y nuevas monedas electrónicas (Bitcoin). La ubicuidad de redes de pago e interbancarias llevó a los gobiernos a ver los pagos como infraestructura pública, impulsando estandarización, licencias más simples y regulación de precios.

Gobierno técnico: ISO/IEC rige protocolos y formatos de banda magnética; el PCI Security Standards Council rige la seguridad; EMVCo (Europay, MasterCard, Visa) estandariza chip y contactless, con MasterCard, American Express, Discover, JCB y UnionPay entre sus miembros, y reserva la marca EMV en EE. UU. para su tecnología Integrated Circuit Card (ICC).

## 1.2 Industry Actors

Los dos actores marco son customers y businesses. En una transacción típica, un customer (también cardholder o card member) paga dinero a cambio de bienes o servicios de un business (merchant), o recibe un refund. Un business puede ser cardholder (tarjeta corporativa) y un merchant puede ser una entidad municipal, gubernamental o una persona física. En todos los casos hay un payer y un payee, y el objetivo de la industria es facilitar el pago, mediante payment card o medios alternativos (digital wallet, soluciones móviles, cryptocurrency).

- Card schemes: tarjetas y redes asociadas, incluyendo infraestructura técnica, gobierno de membresía, gestión de riesgo y compliance, reglas de marca, seguros y garantías de remisión. Ejemplos: Visa, MasterCard, American Express, Discover, Diners, JCB, UnionPay. Puede gestionarlo un consorcio de bancos, una empresa con ánimo de lucro (Visa Inc., MasterCard) o una empresa estatal (NSPK). Una empresa puede poseer varios schemes (Discover posee Diners) o varias controlar uno (Maestro, gestionado por Europay y MasterCard).
- Issuer (a veces, impreciso, issuer bank): emite tarjetas según las guías de marca, gestiona la relación con el cardholder, controla el saldo o crédito permitido (open-to-pay amount), paga las transacciones que le presentan los acquirers, gestiona el riesgo de fraude, da crédito, cobra las facturas y gestiona disputas por el cardholder.
- Acquirer (o acquirer bank): gestiona la relación con el merchant. Algunos proveen terminales (práctica común en Rusia, Israel); otros delegan o dejan que el comercio traiga su dispositivo (EE. UU., Japón, Europa). Procesa transacciones según las guías del scheme, presenta las autorizadas a los issuers para clearing, remite fondos a los comercios y gestiona disputas por el merchant.

Los roles de issuer y acquirer pueden recaer en la misma entidad (algo frecuente). Cualquiera puede operar además como retail o commercial bank: un issuer que es retail bank mantiene la checking account del titular y debita directamente; si no lo es, exige depósitos y emite facturas. Un acquirer que es commercial bank abona directamente las cuentas de sus comercios en lugar de usar wire transfers por un correspondent bank.

El ecosistema esqueleto (figura 1.1) —merchant, card scheme (issuer/acquirer) y cardholder— se complementa con proveedores de servicios adicionales:

- PSP (Payment Services Provider): da una interfaz uniforme a todos los schemes soportados y gestiona relaciones y conexiones técnicas con schemes y acquirer banks; muchos añaden servicios de valor (risk management, métodos alternativos). Resuelven la dificultad técnica que para un comercio pequeño es irreal e imposible (figura 1.2).
- PF (Payment Facilitator) o Merchant Aggregator: un PSP que además da de alta a los comercios en nombre del acquirer y les desembolsa fondos.
- Third-party processor: procesamiento subcontratado por acquirer, issuer o PSP para centrarse en el negocio.
- ISO (Independent Sales Organization) o agente: encuentra y da de alta nuevos clientes para acquirers y PSPs.
- Marketplace: un PF que además ofrece un marketplace unificado para submerchants muy pequeños.

## 1.3 Three-party and Four-party Schemes

Hay dos tipos mayores: esquemas cerrados (three-party) y abiertos (four-party).

En el modelo three-party (figura 1.3) el propio card scheme adquiere las transacciones, liquida con los merchants, emite tarjetas y factura a los cardholders. Ventajas: máximo control de la experiencia de cliente, despliegue de cambios más simple por haber menos partes, y no hay competencia in-brand (solo compite con otros schemes). Es una bendición a medias: mejor gobierno, pero a veces se pierden oportunidades de crecimiento e innovación. Expandirse a nuevas geografías exige fuerte presencia local, no siempre viable, así que recurren a franquicias y partnerships. Ejemplos: American Express, Diners Club, Discover.

En el modelo four-party (figura 1.4) el card scheme actúa como rule setter y facilitador, pero delega issuing y acquiring a otras instituciones. Da menos control sobre la experiencia y exige coordinar el roll-out entre participantes, pero permite un crecimiento mucho más rápido de la base de clientes al asociarse con incumbentes locales. Ejemplos: Visa, MasterCard, UnionPay.

Como las franquicias representan esquemas three-party y a la vez actúan como acquirers e issuers de esquemas four-party, el panorama puede ser confuso. Otra diferencia clave es la ausencia o presencia de interchange fees como medio principal de liquidación mutua entre entidades de acquiring e issuing.

## 1.4 Payment Online and at the Store

El procesamiento se divide en una parte pequeña y evidente y otra mucho mayor entre bastidores. El cardholder inicia la compra; la tarjeta puede estar físicamente presente o no, el punto de venta puede ser virtual, el titular puede o no usar el número (el merchant puede guardarlo on file), y la verificación de identidad puede ser PIN, contraseñas fijas o generadas, o un tap sin verificación (transit terminal). Pese a las variantes, hay pasos comunes, ilustrados comparando card-present (chip EMV online PIN en tienda) y card-not-present (3D Secure en e-commerce), según la Tabla 1.1:

1. Identificación de la cuenta: present — se inserta la tarjeta y el chip comunica el número de cuenta y detalles al terminal; CNP — el titular teclea el número y campos de identificación en el formulario web.
2. Verificación de la tarjeta: present — intercambio criptográfico entre terminal y tarjeta; si falla, se cancela, y el chip produce valores capturados por el terminal; CNP — el titular introduce un valor de seguridad (CVV2 o CVC2) capturado por el software.
3. Verificación del titular: present — la tarjeta pide PIN, cifrado por el terminal; CNP — el plug-in redirige a la página del issuer, que confirma identidad con contraseña estática o, más común, one-time password enviada por SMS, y genera evidencia criptográfica.
4. Mensaje de solicitud: present — la tarjeta firma los detalles (amount, currency, fecha/hora) y el terminal arma el mensaje con datos del entorno (terminal ID, fecha/hora), transacción, PIN cifrado y datos del chip; CNP — el software arma el mensaje con datos del entorno (terminal ID, website), transacción, resultado de autenticación del issuer y número de seguridad de la tarjeta. Se reenvía a la red.
5. Respuesta: la red relaya la petición al issuer o la resuelve en su nombre; se validan cryptogram/PIN (present) o la evidencia criptográfica y el card check value (CNP) y se aprueba o deniega; el resultado vuelve al punto de venta o al e-commerce y se muestra.

De momento se asume que el terminal o la tienda online se conectan directamente a la red de pago; los intermediarios habituales no alteran la lógica del pago.

## Ideas clave

- El pago evolucionó con la idea del dinero; efectivo y cheques dejaban sin cubrir conveniencia, garantía, coste, seguridad frente al fraude y trazabilidad.
- El "First Supper" (McNamara y Schneider, 1950) dio origen a Diners Club, el primer card scheme; le siguieron American Express, Visa, MasterCard, JCB, UnionPay, RuPay y Mir.
- Actores clave: cardholder, merchant, card scheme, issuer, acquirer, PSP, PF/Merchant Aggregator, third-party processor, ISO y marketplace.
- El issuer gestiona al titular (crédito, fraude, facturación, disputas); el acquirer gestiona al comercio (procesa, presenta al issuer, remite fondos); ambos roles pueden recaer en la misma entidad.
- Three-party (cerrado): el scheme hace todo, con máximo control pero expansión difícil (Amex, Diners, Discover); four-party (abierto): delega issuing/acquiring, crece más rápido (Visa, MasterCard, UnionPay).
- La diferencia clave entre modelos es la presencia o ausencia de interchange fees como liquidación entre acquiring e issuing.
- Toda transacción comparte cinco pasos (identificación, verificación de tarjeta, verificación del titular, mensaje de solicitud y respuesta), con mecanismos distintos en card-present y card-not-present.
- Estandarización y gobierno: ISO/IEC, PCI Security Standards Council y EMVCo (chip/contactless, marca EMV para la tecnología ICC).
