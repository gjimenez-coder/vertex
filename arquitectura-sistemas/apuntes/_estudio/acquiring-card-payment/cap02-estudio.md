# Payment Flow and Basics of Technology (Flujo de pago y fundamentos de la tecnología) — Estudio

## Tarjetas de repaso

P: ¿Qué estándares rigen los atributos físicos de la tarjeta? / R: ISO/IEC 7813 (tamaño, forma y ubicación de la banda), 7816 (chip embebido) y 14443 (contactless con antena).

P: ¿De qué tres componentes se compone un PAN y cuántos dígitos tiene? / R: IIN/BIN, IAN y check digit (CD); tiene entre 13 y 19 dígitos (16 es lo más común) y se rige por ISO/IEC 7812.

P: ¿Qué es el MII y qué problema tiene usarlo para identificar la marca? / R: Es el primer dígito del BIN (Major Industry Identifier) que indica la industria del emisor; no conviene basarse solo en él porque algunos MII se comparten y los rangos de IIN cambian de manos por fusiones y adquisiciones.

P: ¿Qué diferencia a charge, credit, debit y prepaid cards? / R: Charge: liquidar la deuda completa al final del período; credit: permite crédito revolvente; debit: deduce fondos de inmediato del saldo; prepaid: open-to-buy limitado por el saldo asociado, a menudo uso anónimo.

P: ¿Cuáles son las tres pistas de la banda magnética y sus estándares/longitudes? / R: Track 1 (alfanumérica, máx. 79, ISO/IEC 7813), Track 2 (numérica, máx. 40, ISO/IEC 7813) y Track 3 (máx. 107, ISO/IEC 4909, hoy en desuso).

P: ¿Qué define cada uno de los tres dígitos del service code? / R: El primero el tipo de interchange y uso de ICC; el segundo el modo de autorización; el tercero los servicios permitidos y el método de verificación.

P: ¿Cuáles son los cuatro tipos de CVV y para qué sirve cada uno? / R: CVV1 (en banda, valida su autenticidad), CVV2 (impreso, valida card-not-present), iCVV (en el ICC, interoperabilidad/transición) y dCVV (dinámico, asegura contactless magstripe).

P: ¿Cómo se calcula el CVV? / R: Es un hash de una vía en tres pasos: preparación del vector de datos (PAN, expiry date y service code en nibbles, 128 bits), cifrado 3-DES con una CVK secreta del emisor y decimalización; se valida en HSM.

P: ¿Por qué firmar el service code dentro del CVV1 es importante? / R: Impide burlar las restricciones del emisor, por ejemplo cambiar un 520 por 101, además de evitar duplicados de banda.

P: ¿Qué Cardholder Verification Methods existen en card-present según EMV? / R: Failed CVM, No CVM, signature, offline PIN (plaintext o enciphered, ISO/IEC 9564 formato 2) y online PIN (empaquetado en EPB enviado al emisor).

P: ¿Qué exige la Strong Customer Authentication de la UE? / R: Desde septiembre de 2019, al menos dos factores dinámicamente enlazados de "algo que eres", "algo que tienes" y "algo que sabes" (con exenciones).

P: ¿Cuáles son los dos métodos de verificación del PIN a elección del emisor? / R: Almacenar el PIN cifrado en base de datos y delegar la validación al HSM, o apoyarse en el PVV (PIN verification value), donde solo la clave de verificación (PVK) es secreta.

P: ¿Qué diferencia a un refund de un reversal? / R: El refund acredita fondos (limitado al monto original) y aparece como línea en el estado; el reversal cancela la transacción original, puede ser automático por motivos técnicos y, si es oportuno, no aparece en el estado.

P: ¿Qué distingue full-grade de part-grade EMV en el mensaje posterior? / R: En full-grade, tarjeta y terminal usan EMV y el mensaje viaja con todos los valores en ISO 55 (ARQC); en part-grade, el mensaje tiene formato de banda y el emisor usa iCVV o dCVV para confirmar autenticidad.

P: ¿Qué categorías existen en card-not-present? / R: Mail/fax order, telephony order (ambas forman MOTO), e-commerce y merchant-initiated transactions (standing authorization, recurring e installment).

## Preguntas de autoevaluación

P: ¿Para qué sirven las BIN tables y qué información distribuyen los schemes en ellas? / R: Facilitan el enrutamiento y aplicar reglas por marca y producto; incluyen inicio y fin del rango de PAN, marca, longitud completa del PAN, issuer member ID e indicadores de tipo y producto. Los three-party schemes no suelen proveer BIN tables elaboradas; los four-party sí. (Sección 2.2)

P: ¿Qué es el iCVV y qué ataque busca contrarrestar? / R: Es un CVV guardado en el chip calculado con service code `999` para distinguir lecturas de chip de lecturas de banda (CVV1). En part-grade EMV el terminal transmite datos de banda al host, lo que permitiría clonar el Track 2 leído del chip; el iCVV lo contrarresta. (Sección 2.5.4)

P: ¿En qué consiste el account-level management y cómo afecta la relación PAN-producto? / R: Permite promover una cuenta a un producto distinto (normalmente premium) según el gasto, de modo que un PAN de un rango básico puede corresponder a otro producto. (Sección 2.3)

P: ¿Qué es un account validation y cómo se implementa típicamente? / R: Una transacción sin intención de compra, hecha como pre-autorización de monto cero, con respuesta 85 ("No reason to decline") además de 00 ("Success"); la peor alternativa es pre-autorizar un monto mínimo ($0.01). (Sección 2.9.1)

P: ¿Qué diferencia a las business-to-cardholder de las cardholder-to-cardholder payment transactions? / R: Las business-to-cardholder son fund disbursements (rebates, pagos de juego, salarios, pensiones, préstamos); las cardholder-to-cardholder constan de dos partes (funding transaction del remitente al merchant y luego payment transaction a los destinatarios) y tienen límites legales estrictos por lavado y fraude. (Sección 2.9.3)

P: ¿Qué cuatro formatos/combinaciones de datos surgen al cruzar métodos de transferencia y formato de datos en el POS? / R: EMV contact ("chip and dip", ICC en DE 55 y Track 2 en DE 35), EMV contactless (ICC en DE 55), Magstripe contact (datos en DE 35, DE 45 o ambos) y Magstripe contactless (Track 2 con elementos criptográficos dinámicos en DE 35 y opc. DE 45). (Sección 2.10.2)

P: ¿Qué estándares y pruebas debe superar un terminal antes de operar en vivo? / R: PCI PTS si entra PIN, CE marking en Europa, prueba FCC en EE.UU. para inalámbrico, y una prueba de integración end-to-end ("card scheme certification") que incluye la conexión al host adquirente y al scheme; un cambio de host o terminal exige recertificación. (Sección 2.10.3)

P: ¿Qué prohíbe PCI DSS respecto a los datos de banda y CVV? / R: Ni el CVV1 ni las pistas completas deben almacenarse. (Sección 2.5.2)

## Puntos a dominar

- Identificar la familia de estándares ISO/IEC (7811/7812/7813, 7816, 14443, 4909, 9564) y EMV, y qué rige cada uno.
- Descomponer un PAN en IIN/BIN, IAN y check digit (Luhn), y explicar el papel del MII y las BIN tables.
- Distinguir los tipos y productos de tarjeta (consumer vs corporate; charge, credit, debit, prepaid) y el account-level management.
- Describir las tres pistas de la banda y descomponer la estructura de Track 1 y Track 2, incluyendo el service code de tres dígitos.
- Explicar los cuatro CVV (CVV1, CVV2, iCVV, dCVV) y las tres fases del algoritmo (vector de datos, 3-DES, decimalización).
- Enumerar los Cardholder Verification Methods de card-present y los factores exigidos por la SCA.
- Diferenciar la verificación del PIN por almacenamiento cifrado (HSM) frente a PVV/PVK y el recorrido del online PIN como EPB con "PIN translations".
- Clasificar los tipos de transacción (retail, efectivo, payment transactions) y distinguir refund de reversal, y withdrawal de cash advance.
- Determinar el POS entry mode a partir de capacidades del terminal, de la tarjeta y condiciones transitorias, y distinguir full-grade de part-grade EMV.
- Clasificar las transacciones card-not-present (MOTO, e-commerce, merchant-initiated) y sus subtipos.
