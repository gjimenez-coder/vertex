# Payment Services and Protocols (Servicios y protocolos de pago) — Estudio

## Tarjetas de repaso

P: ¿Cuáles son las fases del procesamiento de un pago? / R: Tres obligatorias —autorización, clearing y settlement— y una opcional pero frecuente: la disputa.

P: ¿Qué diferencia a SMS de DMS? / R: En SMS un único mensaje solicita autorización y presenta a clearing a la vez (atómico, típico en ATM); en DMS la autorización va en un mensaje y el clearing se hace aparte, a menudo en ficheros batch.

P: ¿Por qué el SMS es habitual en cajeros (ATM)? / R: Porque la entrega de efectivo es irreversible, y conviene autorizar y presentar a clearing de forma atómica en un solo mensaje y protocolo.

P: En DMS, ¿qué significa que una transacción esté "autorizada"? / R: Que puede presentarse a clearing, donde aún puede ser honrada o rechazada; autorizar no equivale a aprobar.

P: ¿Qué es el "Processing Day" o "Central Processing Date"? / R: El día hábil en que se consideran presentadas las transacciones, fijado por el momento del envío de los ficheros de clearing respecto al cut-off.

P: ¿En qué se diferencian los mensajes de titular (cardholder) y de red (network) en ISO 8583? / R: Los de red establecen o cierran sesiones, intercambian claves, comprueban disponibilidad o comunican actualizaciones de ficheros; los de titular cubren compras, preautorizaciones, retiradas, reembolsos, reversals, consultas de saldo, pagos y transferencias.

P: ¿De qué partes consta un mensaje ISO 8583? / R: Header (metainformación), MTI/MTID, bitmap (qué campos esperar) y data elements (los datos).

P: ¿Qué codifica cada dígito del MTID de cuatro dígitos? / R: 1º versión del protocolo (0=1978, 1=1993, 2=2003), 2º clase (1 autorización, 2 financiero, 4 reversal, 8 network management), 3º función (0 request, 1 response, 2 advice, 3 advice response) y 4º origen (0 acquirer-originated, 1 acquirer repeat).

P: ¿Qué diferencia hay entre request y advice? / R: Request es "preguntar" (pedir autorización) y advice es "avisar"; por ejemplo, en una preautorización de hotel el pago final puede ir como advice.

P: ¿Para qué sirve el bitmap y qué indican los bits 1 y 65? / R: Indica qué data elements están presentes; cada bitmap son 8 bytes, y los bits 1 y 65 no son campos sino que señalan la presencia del bitmap siguiente (secundario y extendido).

P: ¿Cuál es la regla general de padding de los campos? / R: Si el valor es alfanumérico o especial se trata como cadena y se rellena con espacios por la derecha; si es solo numérico se rellena con ceros por la izquierda.

P: ¿Qué codificaciones aparecen en el cable y cómo se representa el espacio en ASCII y EBCDIC? / R: ASCII, EBCDIC, BCD empaquetado y BER-TLV (EMV); el espacio es 0x20 en ASCII y 0x40 en EBCDIC, y a veces se mezclan en un mismo mensaje.

P: ¿Qué representan los data elements DE 2, DE 3 y DE 11? / R: DE 2 es el PAN (LLVAR en BCD), DE 3 el Processing Code (n-6 BCD con tres subelementos) y DE 11 el STAN, que identifica de forma única la transacción del titular (no puede ser todo ceros).

P: ¿Cómo se representa el decimal en los campos de importe (DE 4/5/6)? / R: Son enteros sin signo en BCD con ceros a la izquierda; el decimal lo implica el exponente de la moneda (ISO 4217): 2 en la mayoría, 3 en algunas de Oriente Medio y 0 cuando no hay unidad menor (yen).

P: ¿Qué es el Stand-in Processing (STIP)? / R: Un servicio del esquema (en esquemas de cuatro partes) que actúa cuando el emisor no está disponible; usa tablas de parámetros y claves precompartidas para validar tarjeta y PIN y aprobar o declinar, comunicando luego los resultados como advices.

## Preguntas de autoevaluación

P: ¿Por qué se dice que, pese a la diversidad de medios de pago, existe una sola familia de protocolos técnicos? / R: Porque en el fondo los protocolos son muy parecidos, basados en el estándar ISO 8583 y sus dialectos propietarios. (Lo que necesitas saber)

P: ¿Cuándo surge una disputa y cómo se gestiona? / R: Cuando el titular o el emisor consideran que una transacción se presentó por error (fallo técnico que duplica el envío) o no es legítima (tarjeta clonada, comercio que no entrega pero cobra); la gestionan los bancos con intercambio de documentación y posibilidad de apelar al esquema. (Fases del procesamiento: SMS frente a DMS)

P: ¿Qué información útil suele traer la respuesta de un SMS y para qué sirve? / R: Información para la reconciliación del acquirer, como comisiones de intercambio precisas y tasas de conversión. (Fases del procesamiento: SMS frente a DMS)

P: Dado el bitmap `82 20 00 00 0A 00 00 00`, ¿qué se puede deducir? / R: Tiene activos los bits 1, 7, 11, 37 y 39; como el bit 1 está activo hay bitmap secundario; al faltar el DE 2 (PAN) probablemente sea un mensaje de network management, y la presencia del DE 39 sugiere un mensaje de respuesta. (Bitmap)

P: ¿Qué secuencia de MTIDs corresponde a una preautorización con completion y a una cancelación de compra? / R: Preautorización/completion: 0100 → 0110 y luego 0220 → 0230; cancelación: tras 0100 → 0110, el acquirer envía 0400 → 0410. (MTID)

P: ¿Qué indican las notaciones LLVAR y LLLVAR en la longitud de un campo? / R: LLVAR/HLVAR usa un byte de longitud en BCD (hasta 99 unidades) y LLLVAR/HLLVAR usa dos bytes de longitud en BCD (hasta 999; p. ej. un campo 55 de 125 bytes lleva longitud 0x0125). (Data elements: formatos, longitud, padding y codificación)

P: ¿Qué validaciones realiza el servicio de Data Integrity? / R: Valida formatos y la coherencia entre autorización y clearing, por ejemplo que una transacción marcada como e-commerce en el POS entry mode no llegue con Track 2. (Otros servicios del card scheme)

P: ¿Para qué sirven el Account Updater y la Recurring Payment Revocation? / R: El Account Updater intercambia datos de cuenta entre instituciones cuando cambia el PAN o la expiración (lo inicia el acquirer enviando la lista de PANs); la Recurring Payment Revocation permite al emisor comunicar a la red revocaciones de autorizaciones recurrentes para que la red las decline. (Otros servicios del card scheme)

## Puntos a dominar

- Distinguir las tres fases obligatorias (autorización, clearing, settlement) y la opcional (disputa), y cuándo interviene cada una.
- Explicar la diferencia entre SMS (un mensaje, atómico, típico en ATM) y DMS (clearing aparte, a menudo en ficheros batch con cut-off y Processing Day).
- Interpretar un MTID de cuatro dígitos (versión, clase, función, origen) y reconocer secuencias como 0100/0110, 0220/0230, 0400/0410 y 0800/0810.
- Leer un bitmap de 8 bytes para saber qué data elements vienen y reconocer el papel de los bits 1 y 65.
- Identificar las codificaciones (ASCII, EBCDIC, BCD empaquetado, BER-TLV) y aplicar la regla de padding según el tipo de valor.
- Reconocer los campos clave y su formato: DE 2 (PAN), DE 3 (processing code), DE 4/5/6 (importes con exponente ISO 4217), DE 7 (fecha/hora de transmisión), DE 11 (STAN), DE 14 (expiración), DE 18 (MCC), DE 22 (POS entry mode), DE 37 (RRN), DE 39 (response code), DE 52 (PIN block), DE 55 (ICC data).
- Describir los servicios adicionales del esquema: STIP, settlement por niveles, prevención de fraude, data integrity, tokenización, account-level product management, account updater y revocación de pagos recurrentes.
