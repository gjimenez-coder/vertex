# Acquiring Card Payments — Ilya Dubinsky (CRC Press, Taylor & Francis, 2019)
## Capítulo 3 — Payment Services and Protocols (Servicios y protocolos de pago)

> Nota de extracción: el texto se obtuvo de la capa de texto del PDF; las citas referencian la página del PDF como (PDF p. N).

## Lo que necesitas saber

El capítulo sostiene que, pese a la diversidad de medios de pago, en el fondo existe una sola familia de protocolos técnicos muy parecidos. El procesamiento de un pago tiene tres fases obligatorias —autorización, clearing y settlement— y una opcional pero frecuente: la disputa. La autorización y el clearing se realizan con un único mensaje (SMS, Single Message Service) o con dos mensajes (DMS, Dual Message Service).

El grueso del capítulo describe el protocolo ISO 8583 y sus "dialectos" propietarios: la estructura del mensaje (header, MTI/MTID, bitmap y data elements), las convenciones de formato, longitud, padding y codificación (ASCII, EBCDIC, BCD y BER-TLV), y un recorrido por los campos (data elements) más comunes con su significado y formato.

Al terminar sabes distinguir SMS de DMS, interpretar un MTID de cuatro dígitos, leer un bitmap para saber qué campos vienen, reconocer las codificaciones en el cable y conocer el papel de campos clave (PAN, processing code, importes, STAN, MCC, POS entry mode, response code, etc.). El capítulo cierra con los servicios adicionales que ofrecen los card schemes.

## Fases del procesamiento: SMS frente a DMS

En el SMS un único mensaje solicita la autorización de un importe y lo presenta a clearing a la vez. Es atómico (un mensaje, una transacción) y usa un solo protocolo técnico; es habitual en cajeros (ATM), donde la entrega de efectivo es irreversible. Su respuesta suele traer información útil para la reconciliación del acquirer (comisiones de intercambio precisas y tasas de conversión).

En el DMS un mensaje solicita la autorización de una compra pero no la presenta a clearing; el clearing se hace aparte, con un mensaje online o, más a menudo, enviando los presentments en un fichero por lotes (batch). Las autorizaciones online siguen un estándar compartido (un dialecto de ISO 8583), pero los ficheros de clearing varían mucho entre esquemas. Para presentar a clearing se envían ficheros antes de un cut-off; el momento del envío fija el día hábil en que se consideran presentados (el "Processing Day" o "Central Processing Date").

El settlement implica transferencias bancarias e intercambio de informes, con reglas muy variables: un esquema puede liquidar una remesa diaria en cinco o siete días hábiles, o liquidar a distinta velocidad las transacciones intra-país, intra-región e inter-regionales. Por ejemplo, la liquidación doméstica en Islandia es el mismo día, mientras que un pago de un titular estadounidense podría liquidarse en tres días hábiles.

La disputa surge cuando el titular o el emisor consideran que una transacción se presentó por error (por un fallo técnico que duplica un envío) o que no es legítima (tarjeta clonada, o comercio que no entrega los bienes pero cobra). Es, literalmente, una disputa entre titular y comercio gestionada por los bancos, con intercambio de documentación y posibilidad de apelar al esquema. En lugares como Japón, mientras el interchange doméstico quede fuera de los esquemas globales, las partes prefieren resolver la transacción discutida directamente (llamándose emisor y acquirer) antes que recurrir a una disputa formal mediada por el esquema.

## Mensajes del servicio de autorización

Que el emisor o el esquema autoricen una transacción no equivale a aprobarla: en DMS, una transacción autorizada solo significa que puede presentarse a clearing, donde aún puede ser honrada o rechazada. La mayoría de esquemas usan dialectos de ISO 8583. Sus mensajes se agrupan en dos categorías: de titular (cardholder) y de red (network). Los mensajes de red sirven para establecer o cerrar sesiones, intercambiar claves, comprobar la disponibilidad del interlocutor o comunicar actualizaciones de ficheros (usado en el stand-in processing). Los mensajes de titular cubren compras, preautorizaciones, retiradas, depósitos, reembolsos, reversals, consultas de saldo, pagos y transferencias entre cuentas.

## Estructura del mensaje ISO 8583

Los esquemas usan modificaciones del estándar ("dialectos ISO"). Un mensaje ISO consta de:

- header: metainformación del mensaje.
- message type indicator (MTI o MTID): clase, tipo y origen del mensaje.
- bitmap: indica qué campos de datos esperar.
- data fields (data elements): encapsulan los datos.

El header puede ser trivial (solo la longitud total del mensaje en bytes) o no trivial, con identificadores de estación/institución, longitudes de header y cuerpo, y un campo de reject code. Ante un mensaje mal formado pero con header legible, algunos esquemas devuelven el mensaje ofensivo rellenando el reject code que señala el campo erróneo; otros exigen una respuesta válida completa con un campo que detalla el error.

### MTID

El MTID es un código de cuatro dígitos en BCD. Es práctico verlo como la concatenación de clase y función. El primer dígito indica la versión del protocolo (0 = revisión 1978, la más común en la industria y usada en todos los ejemplos; 1 = 1993; 2 = 2003). El segundo dígito es la clase del mensaje: 1 autorización (DMS; una sola no basta para mover fondos), 2 financiero (mensaje completo, puede mover fondos; usado en SMS), 4 reversal (revierte otras clases; en SMS y DMS), 8 network management (sesión, keepalive, intercambio de claves). El tercer dígito es la función: 0 request, 1 request response, 2 advice, 3 advice response. La diferencia entre request y advice es la de "preguntar" frente a "avisar": en una preautorización de hotel, el pago final puede ir como advice. El cuarto dígito es el origen: 0 acquirer-originated, 1 acquirer repeat (reenvío de un mensaje sin respuesta).

Ejemplos de escenarios (ISO 1978):

- Sesión: el acquirer envía 0800 (network management request) y recibe 0810 (response) al conectar y al desconectar.
- Compra (DMS): 0100 (authorization request) → 0110 (authorization response).
- Preautorización y completion: 0100 → 0110; luego 0220 (financial advice) → 0230 (financial advice response).
- Cancelación de compra: tras 0100 → 0110, el acquirer envía 0400 (reversal request) → 0410 (reversal response).

### Bitmap

La presencia de cada data element se define mediante un bitmap. Un mensaje puede tener uno, dos o tres bitmaps (primario, secundario y terciario/extendido); los grandes esquemas usan hasta dos y el primario siempre está presente. Cada bitmap ocupa 8 bytes con bits numerados de izquierda a derecha desde 1: el primario cubre los bits 1–64, el secundario 65–128 y el extendido 129–192. Los bits 1 y 65 no corresponden a un campo, sino que indican la presencia del bitmap siguiente. Ejemplo: `82 20 00 00 0A 00 00 00` tiene activos los bits 1, 7, 11, 37 y 39; como el bit 1 está activo hay bitmap secundario. Al faltar el data element 2 (PAN) probablemente sea un mensaje de network management, y la presencia del DE 39 (result code) sugiere un mensaje de respuesta.

### Data elements: formatos, longitud, padding y codificación

Los campos pueden llevar tipos de datos muy diversos. Algunos los define el estándar; otros son propietarios, con subformato de subcampos fijos o tag-length-value (TLV). No es raro que un mensaje mezcle ASCII y EBCDIC a la vez.

Notación de valores válidos: `a` alfabético (Latin, sin caracteres nacionales en autorizaciones online), `n` dígitos decimales, `s` caracteres especiales imprimibles, `b` binario (los datos EMV del campo 55 son `b`), `z` formatos de Track 1/Track 2. Se combinan cuando tiene sentido (`an`, `ans`), pero `b` y `z` no.

Longitud: fija rellena siempre (p. ej. campo 14, expiración, `n-4`), fija con padding de espacios (campo 38, approval code, `an-6`) o variable. Notaciones: `-N` longitud fija; `..N`/`…N` variable con máximo; `LLVAR`/`HLVAR` con un byte de longitud BCD (hasta 99 unidades); `LLLVAR`/`HLLVAR` con dos bytes de longitud BCD (hasta 999; p. ej. un campo 55 de 125 bytes lleva longitud `0x0125`).

Padding (regla general): si el valor es alfanumérico o especial se trata como cadena y se rellena con espacios por la derecha; si es solo numérico se trata como número y se rellena con ceros por la izquierda. Así, "ABC" en un campo de longitud 4 queda "ABC " y el numérico 123 en BCD se transmite `01 23`.

Codificaciones: ASCII (7 bits en la práctica; espacio `0x20`, dígitos `0x30`–`0x39`), EBCDIC (formato de IBM System/360; espacio `0x40`, dígitos `0xF0`–`0xF9`, mayúsculas en rangos `0xC1`–`0xC9`, `0xD1`–`0xD9`, `0xE2`–`0xE9`), BCD empaquetado (un dígito por nibble) y BER-TLV (X.690 de ITU-T) para EMV. Ejemplo: el decimal 17471 es `443F` en hexadecimal (dos bytes en big-endian), `01 74 71` en BCD empaquetado, `F1 F7 F4 F7 F1` en EBCDIC y `31 37 34 37 31` en ASCII. En BER-TLV, el tag 5F34 (PAN sequence number, longitud 1 byte) con valor 2 se codifica `5F 34 01 02`.

### Data elements clave

- DE 1 — Bitmap: siempre presente; necesario para parsear el resto.
- DE 2 — PAN: `LLVAR` con PAN en BCD; longitud en dígitos y en BCD. Si el PAN tiene dígitos impares se rellena con cero por la izquierda (sin contar en la longitud). Máximo 19 dígitos, hasta 11 bytes.
- DE 3 — Processing Code: `n-6` BCD con tres subelementos de 2 dígitos (tipo de transacción, cuenta origen, cuenta destino). 00/20/30 = compra POS, reembolso y consulta de saldo; valores típicos 000000, 200000, 300000.
- DE 4, 5, 6 — Importes (transaction, settlement, cardholder billing): `n-12` BCD con cero por la izquierda, enteros sin signo; el decimal lo implica el exponente de la moneda (ISO 4217): 2 para la mayoría, 3 para algunas de Oriente Medio (rial omaní, dinar kuwaití), 0 cuando no hay unidad menor (yen). DE 4 lo rellena el acquirer; DE 6 y DE 5, normalmente la red.
- DE 7 — Transmission Date and Time: `n-10` BCD en formato `MMDDhhmmss`; es el instante de transmisión, no el de la transacción.
- DE 9, 10 — Conversion rates (settlement y cardholder billing): `n-8` BCD; el primer dígito es el "decimal indicator" (0–7, posición del punto desde la derecha).
- DE 11 — STAN: `n-6` (o alfanumérico en versiones nuevas); identifica de forma única la transacción del titular y todos sus mensajes; no puede ser todo ceros. Junto con DE 7 identifica transacciones del mismo día.
- DE 12, 13 — Time/Date local: DE 12 `n-6` BCD `hhmmss`, DE 13 `n-4` BCD `MMDD`; hora y fecha locales del card acceptor (a diferencia del DE 7, en huso del esquema).
- DE 14 — Expiración: `n-4` BCD en `YYMM`; válida hasta el último día del mes.
- DE 18 — Merchant Type: el MCC de 4 dígitos (`n-4`), coincide en parte con los SIC; hay MCC genéricos y específicos (p. ej. ATM 6011, pero 4829 en transferencias).
- DE 22 — POS Entry Mode: método de captura del PAN/expiración. Valores habituales: 00 desconocido, 01 manual (incluye MOTO), 02/90 banda magnética, 80 magstripe fallback, 05 chip de contacto, 09/81 comercio electrónico, 07 contactless chip, 91 contactless magstripe.
- DE 23 — Card Sequence Number: `n-3` BCD (obligatorio en EMV full-grade).
- DE 25 — POS Condition Code: uso inconsistente entre implementaciones.
- DE 35/36/45 — Track 2/Track 3/Track 1: datos de pista sin sentinels ni LRC.
- DE 37 — RRN: normalmente `an-12`; se recomienda solo numérico. Formato popular `YDDDnnxxxxxx` (dígito de año, día ordinal/juliano, hora del DE 7 y STAN del DE 11).
- DE 38 — Authorization Code: `an-6` (2 a 6 caracteres), devuelto por el emisor en aprobaciones; no todo espacios ni ceros.
- DE 39 — Response Code: `an-2` (o `an-3`). 00 aprobación total; 85 "No reason to decline"; 08 "Honor with ID"; 10/87 aprobación parcial; 01/02 "Refer to card issuer"; 04 "Capture card"; 41 "Lost card"; 43 "Stolen card".
- DE 41 — Terminal ID: `ans-8`, con DE 42 identifica el terminal; space-padded a la derecha.
- DE 42 — Merchant ID: `ans-15` (Card Acceptor ID); mejor solo numérico por los programas de los esquemas.
- DE 43 — Card Acceptor Name/Location: `ans-40` ("Billing Descriptor"); nombre DBA, ciudad y país (o teléfono en CNP).
- DE 52 — PIN Block: binario de 8 bytes con el bloque de PIN cifrado.
- DE 54 — Additional Amounts: variable (`an-20` a `an-120`); bloques de 20 con tipo de cuenta, tipo de importe, moneda, signo (C/D) e importe.
- DE 55 — ICC Data: variable, hasta 255 bytes binarios con BER-TLV generado por el chip.

## Otros servicios del card scheme

Además de enrutar mensajes de autorización y clearing, los esquemas ofrecen:

- Stand-in Processing (STIP): en esquemas de cuatro partes, actúa cuando el emisor no está disponible; usa tablas de parámetros del emisor y claves de validación precompartidas para comprobar la tarjeta, validar PIN y aprobar o declinar. Puede llevar conteos/importes y listas blancas bajo umbrales; al volver el emisor, comunica aprobaciones y declinaciones como advices.
- Settlement internacional, regional y nacional: recauda y distribuye fondos; mismo día en ciertos países (Islandia, por ley), siguiente día en euros en la Eurozona; los internacionales hacen conversión de moneda (no todas las monedas se admiten como de liquidación).
- Fraud Prevention: scoring de fraude online e intercambio de información sobre transacciones fraudulentas y tarjetas perdidas/robadas.
- Data Integrity: valida formatos y coherencia entre autorización y clearing (p. ej. que una transacción marcada como e-commerce en el POS entry mode no llegue con Track 2).
- Payment Network Tokenization (descrito en 4.6.3).
- Account-Level Product Management: cambia el producto asociado a una tarjeta (p. ej. emitir una VIP) sin cambiar el PAN.
- Account Updater: intercambia datos de cuenta entre instituciones cuando cambia el PAN o la expiración; lo inicia el acquirer enviando la lista de PANs.
- Recurring Payment Revocation: el emisor comunica a la red las revocaciones de autorizaciones recurrentes para que la red las decline.
- Address Verification (descrito en 4.5).

## Ideas clave

- El pago tiene tres fases obligatorias (autorización, clearing, settlement) y una opcional (disputa); SMS usa un mensaje y DMS usa dos.
- SMS es atómico y con un solo protocolo (típico en ATM); en DMS el clearing va aparte, a menudo en ficheros batch con cut-off y Processing Day.
- La mayoría de esquemas usan dialectos de ISO 8583, con mensajes de titular y de red.
- El MTID de cuatro dígitos codifica versión, clase (1/2/4/8), función (0/1/2/3) y origen; request es "preguntar" y advice es "avisar".
- El bitmap (primario obligatorio, 8 bytes) indica qué data elements están presentes; los bits 1 y 65 señalan el bitmap siguiente.
- Los campos combinan formatos (a, n, s, b, z), longitudes (fija, LLVAR, LLLVAR) y codificaciones (ASCII, EBCDIC, BCD, BER-TLV), a veces mezcladas en el mismo mensaje.
- Campos clave: DE 2 (PAN), DE 3 (processing code), DE 4/5/6 (importes con exponente ISO 4217), DE 11 (STAN), DE 18 (MCC), DE 22 (POS entry mode), DE 39 (response code).
- Los esquemas añaden servicios como STIP, settlement por niveles, prevención de fraude, data integrity, account updater y revocación de pagos recurrentes.
