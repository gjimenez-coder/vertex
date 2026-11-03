# Acquiring Card Payments — Ilya Dubinsky (CRC Press / Taylor & Francis, 2019)
## Capítulo 2 — Payment Flow and Basics of Technology (Flujo de pago y fundamentos de la tecnología)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas usan la página del PDF `(PDF p. N)`.

## Lo que necesitas saber

El capítulo recorre los fundamentos técnicos de la tarjeta de pago y del flujo de una transacción: desde la física del plástico hasta cómo se codifican y validan los datos de la tarjeta. La tesis es que el procesamiento de pagos descansa sobre una pila de estándares (ISO/IEC 7810/7811/7812/7813, 7816, 14443, 4909, 9564 y EMV) que definen la forma de la tarjeta, la estructura del PAN, el contenido de la banda magnética, los valores criptográficos de verificación (CVV, PVV) y las reglas de interacción terminal-tarjeta.

Sales sabiendo cómo se estructura un PAN y qué es el BIN/IIN; qué contienen las tres pistas de la banda magnética y el service code; cómo se calculan y para qué sirven las variantes de CVV (CVV1, CVV2, iCVV, dCVV); qué métodos de verificación del tarjetahabiente existen (firma, PIN offline/online, No CVM) y qué exige la Strong Customer Authentication; cómo se maneja el PIN; qué tipos de transacción existen; y cómo las capacidades del terminal, la tarjeta y las condiciones transitorias determinan el modo de entrada (entry mode) y el procesamiento posterior.

El capítulo distingue sistemáticamente entre tres partes y cuatro partes (schemes), entre full-grade y part-grade EMV, y entre entornos card-present y card-not-present, marcos que reaparecen a lo largo del libro.

## 2.1 Forma de la tarjeta

Los atributos físicos del plástico se rigen por ISO/IEC 7813 (tamaño, forma y ubicación de la banda), 7816 (tarjeta inteligente con chip embebido) y 14443 (tarjetas contactless con antena). En el anverso aparecen: branding del card scheme, PAN (embossment según ISO/IEC 7811), fecha de expiración (MM/YY), nombre del tarjetahabiente (hasta 26 caracteres), card sequence number o CSN (se incrementa en cada renovación cuando el emisor conserva el PAN), chip integrado (EMV™), logo del emisor y card product. American Express añade el CID o 4DBC, variante de CVV. Antes de EMV, el holograma embebido servía como verificación de autenticidad en el POS.

## 2.2 Número de tarjeta (PAN)

El PAN tiene entre 13 y 19 dígitos y se rige por ISO/IEC 7812. Se compone de IIN/BIN, IAN y check digit (CD), este último una suma de paridad calculada con el algoritmo de Luhn (sección 10.1). El primer dígito del BIN es el MII (Major Industry Identifier), que identifica a muy alto nivel la industria del emisor:

| MII | Descripción | Notas |
|-----|-------------|-------|
| 2 | Aerolíneas, financieras y futuras asignaciones | MasterCard empezó a usar este MII; partes del rango las usa Diners |
| 3 | Viajes y entretenimiento | Diners, American Express y JCB |
| 4 | Banca y financiero | Visa |
| 5 | Banca y financiero | MasterCard y Diners |
| 6 | Comercio y banca/financiero | MasterCard (Maestro), Discover y UnionPay |

No conviene basarse solo en el MII para determinar scheme y marca, pues algunos MII se comparten y los rangos de IIN cambian de manos por fusiones y adquisiciones. Con un PAN, el software del PSP decide si la marca está soportada, aplica reglas de procesamiento y enruta la transacción. Para facilitar el enrutamiento, los schemes distribuyen BIN tables con: inicio y fin del rango de PAN, marca, longitud completa del PAN (13 a 19, siendo 16 lo más común), issuer member ID, e indicadores de tipo y producto. Los three-party schemes no suelen proveer BIN tables elaboradas; los four-party sí, en actualizaciones completas e incrementales.

## 2.3 Tipos y productos de tarjeta

Primera división: consumer cards (personas) frente a corporate cards (empresas). Por uso o patrón de conciliación:

- Charge cards (delayed debit): el emisor paga la compra y el tarjetahabiente debe liquidar la deuda completa al final del período (por ejemplo, el mes).
- Credit cards: similar, pero el tarjetahabiente puede liquidar una porción y mantener crédito revolvente.
- Debit cards: se compra contra el saldo depositado o la cuenta corriente; los fondos se deducen de inmediato.
- Prepaid / stored-value cards: open-to-buy limitado por el saldo asociado; con cuenta dedicada propia y a menudo uso anónimo.

En la práctica las líneas entre charge y credit se difuminan. Clasificar una tarjeta como "consumer credit" no basta: los emisores empaquetan términos específicos (premium, VIP, estudiantes) que, conformes a las reglas del scheme, se denominan card products. Los four-party schemes publican el product junto a los rangos de BIN; los códigos de producto de Visa suelen tener una o dos letras latinas mayúsculas y los de MasterCard tres. El account-level management permite promover una cuenta a un producto distinto (normalmente premium) según el gasto, de modo que un PAN de un rango básico puede corresponder a otro producto.

## 2.4 La banda magnética

El reverso contiene signature strip, banda magnética (magstripe) y card security code (CSC), aunque el CSC puede estar también en el anverso. La banda almacena datos en partículas de hierro leídas al deslizar la tarjeta (swipe); la física se describe en ISO/IEC 7811. El método de fijar la banda al plástico por calor lo ideó Forrest Parry (IBM, años 1960). Existe un estándar japonés competidor, JIS-U (banda en el anverso), siendo JIS-T la variante compatible con ISO; los lectores japoneses llevan doble cabezal.

La banda ISO tiene tres pistas: Track 1 y Track 2 según ISO/IEC 7813, Track 3 según ISO/IEC 4909. Los datos alfanuméricos usan ANSI/ISO ALPHA y los numéricos ANSI/ISO BCD. Track 1 y 2 son de solo lectura; Track 3 puede actualizarse por el terminal, pero ha caído en desuso con la llegada del chip y EMV. Las pistas contienen PAN, fecha de expiración, tarjetahabiente y discretionary data (que suele incluir una firma criptográfica de ciertos campos, el CVV/CVC, validada por el emisor).

### 2.4.1 Track 1

Longitud máxima 79 caracteres alfanuméricos. Estructura: SS (start sentinel, `%`), FC (format code, `B` para tarjeta internacional estándar), PAN (hasta 19 dígitos), FS (`^`), NM (nombre, 2 a 26 caracteres, con `/` separando nombre y apellido), FS (`^`), ED (expiry date, YY+MM), SC (service code), DD (discretionary data: PVKI, PVV, CVV/CVC), ES (end sentinel, `%`) y LRC (longitudinal redundancy check, sección 10.2).

### 2.4.2 Track 2

Longitud máxima 40 caracteres, solo numéricos salvo sentinels y separadores. Estructura: SS (`;`), PAN, FS (`=`), ED, SC, DD (mismas reglas que Track 1 pero no idéntico por límite de longitud), ES (`?`) y LRC.

### 2.4.3 Track 3

Longitud máxima 107 caracteres. Diseñado para sobrescribirse y controlar el gasto por período, hoy sin uso en los grandes schemes (algunas tarjetas ni tienen espacio físico). Incluye SS (`;`), FC (dos dígitos), PAN, FS (`=`) y campos de ISO/IEC 4909: country code (opc., 3), currency code (3), currency exponent (1, con lógica invertida: multiplica por 10), amount authorized/remaining per cycle, cycle begin, cycle length, retry count, PIN control, interchange controls, PAN y SAN-1/SAN-2 service restrictions (SAN = subsidiary account number, hasta dos cuentas subsidiarias), expiration date, card sequence number, card security number, cuentas subsidiarias, relay marker, CCD (cryptographic check digits, firma criptográfica), discretionary data, ES (`?`) y LRC. Proteger Track 3 exigía intercambio de material criptográfico entre adquirentes y emisor, lo que limitó su adopción.

### 2.4.4 Service code

Tres dígitos que definen geografía, proceso de autorización y servicios permitidos.

Primer dígito (tipo de interchange y uso de ICC):

| Valor | Descripción |
|-------|-------------|
| 1 | Interchange internacional permitido |
| 2 | Internacional permitido; usar chip IC cuando sea posible |
| 5 | Solo nacional; excepción por acuerdos bilaterales |
| 6 | Igual que 5, pero chip IC requerido cuando sea posible |
| 7 | Solo acuerdo bilateral |

Segundo dígito (modo de autorización): 1 = todas permitidas; 2 = solo online (contactar al emisor); 7 = online salvo acuerdo bilateral. EMV suplantó este valor.

Tercer dígito (servicios y método de verificación): 0 = sin restricciones, PIN obligatorio; 1 = sin restricciones; 2 = bienes y servicios, sin efectivo; 3 = solo ATM, PIN requerido; 4 = solo efectivo; 5 = bienes y servicios sin efectivo, PIN requerido; 6 = sin restricciones, preferir PIN; 7 = bienes y servicios, preferir PIN.

Service codes comunes: 101, 201, 106, 206 y, en débito, 226. Un primer dígito 2 indica preferir chip si hay lector.

## 2.5 Card Verification Values

Para frustrar la falsificación de tarjetas a partir de PAN y fecha de expiración (o la manipulación del service code), se ideó un valor de verificación criptográfico conocido como CSC, CID, CVC, CVV o CVN; el texto lo llama CVV. Hay cuatro tipos:

- CVV (o CVV1): en la banda magnética, valida su autenticidad.
- CVV2: impreso en la tarjeta, valida autenticidad en transacciones card-not-present.
- iCVV: en el ICC; facilita la transición e interoperabilidad con sistemas sin datos de chip.
- dCVV: dinámico, calculado por el chip con un contador de transacción y un número impredecible; asegura transacciones contactless magstripe.

### 2.5.1 Algoritmo de cálculo del CVV

El CVV es una función hash de una vía. Salvo el dinámico, todos usan los mismos principios con una CVK (Card Verification Key) secreta del emisor. Tres pasos: (1) preparación del vector de datos (PAN —últimos 16 dígitos, rellenado con ceros a la izquierda—, expiry date y service code, empaquetados en nibbles hexadecimales y rellenados a 128 bits en dos bloques de 64), (2) cifrado 3-DES y (3) decimalización. La CVK de 3-DES tiene dos partes KA y KB: B1 se cifra con KA → R1; R1 XOR B2 → R2; R2 se cifra con 3-DES (cifrar KA, descifrar KB, cifrar KA). La decimalización extrae primero los dígitos decimales izquierda-derecha, luego los hexadecimales módulo 10, y toma 3 o 4 posiciones. El compromiso de la CVK invalida el mecanismo; las claves se guardan en HSMs, que también validan el CVV. Para stand-in processing, las CVK y PVK se comparten con los schemes o las genera el scheme.

### 2.5.2 CVV1

Almacenado en discretionary data de Track 1 o 2. Evita duplicados de banda y, al firmar el service code, impide burlar las restricciones del emisor (por ejemplo, cambiar un 520 por 101). Ni el CVV1 ni las pistas completas deben almacenarse según PCI DSS (sección 8.1).

### 2.5.3 CVV2

Valida autenticidad en card-not-present; impreso al reverso, tres dígitos (en AmEx el 4DBC tiene cuatro y va al anverso). Mismo algoritmo que CVV1, pero como las restricciones del service code no aplican, se usa `000` en su lugar. El emisor puede usar CVKs distintas o las mismas para CVV1 y CVV2.

### 2.5.4 iCVV

En part-grade EMV, el terminal y el chip dialogan en EMV pero el terminal transmite datos de banda al host del adquirente, lo que permitiría clonar el Track 2 leído del chip. Para contrarrestarlo, el chip guarda un iCVV calculado con el mismo algoritmo pero con service code `999`, distinguiendo lecturas de chip (iCVV) de lecturas de banda (CVV1). El emisor puede calcularlo correctamente o colocar un valor inválido que haga fallar la validación de una banda clonada.

### 2.5.5 Dynamic CVV

En contactless EMV modo "Magstripe" (part-grade), el Kernel del POS genera Track 1/Track 2 a partir de los valores de la tarjeta. El Kernel entrega un número impredecible a la tarjeta, que devuelve un valor de verificación de un solo uso; ambos se embeben en la discretionary data. Este valor es el dynamic CVV o dCVV, también llamado CVV3.

## 2.6 Panorama de la tecnología card-present

Tecnologías principales en entornos card-present/cardholder-present:

- Magnetic stripe: en retirada gradual por sus limitaciones y vulnerabilidades.
- EMV chip: lector de contacto; la tarjeta se inserta y el chip dialoga con el terminal.
- EMV contactless: ICC con antena; el chip se alimenta por inducción electromagnética al acercarlo al lector.
- EMV tokenization: combina tokenización y chip EMV; transmite un token en vez del PAN (Apple Pay®, Android Pay®, Samsung Pay®, etc.).

Los terminales seguirán soportando banda durante años (compatibilidad y fallback). En full-grade EMV, tarjeta y terminal usan protocolos EMV y el mensaje (con todos los valores en el campo ISO 55) viaja hasta el emisor. En part-grade EMV, aunque el diálogo terminal-tarjeta sea EMV, el mensaje posterior tiene formato de banda: en lugar de un ARQC, el emisor usa iCVV o dCVV para confirmar autenticidad.

## 2.7 Métodos de verificación del tarjetahabiente

La tarjeta se identifica por PAN (y sequence number) y se autentica criptográficamente; luego ocurre la verificación del tarjetahabiente. En card-not-present (convergente con card-present en móviles) se aplican 3D Secure (Verified by Visa/SecureCode), su sucesor EMV 3DS 2.0 o digital wallets (Visa Checkout®, MasterPass®, AmEx Express CheckOut®), verificando la identidad con: static password, one-time password (habitualmente por SMS; variante más segura con app atada al dispositivo que expira en ~1 minuto) o mobile authentication (passcode, password, patrón de deslizamiento, huella, y métodos experimentales de gestos, voz y reconocimiento facial). Importa distinguir el passcode del dispositivo (a veces llamado mPIN) del PIN de tarjeta, con requisitos estrictos de entrada.

En card-present existe una lista cerrada de Cardholder Verification Methods codificada en EMV:

- Failed CVM: método técnico; indica que la tarjeta decidió fallar todos los chequeos (puede ponerse como última regla de la CVM list).
- No CVM: "hipótesis cero"; sin verificación adicional. Típico en terminales desatendidos (vending, transporte público).
- Signature: método heredado; el terminal imprime el sales draft y el atendedor debería comparar la firma. Deficiente y no depende de EMV.
- Offline PIN: parte de EMV, con variantes plaintext y enciphered; el chip confirma la validez del PIN. El cifrado del PIN entre chip y PIN pad se rige por ISO/IEC 9564 (formato 2).
- Online PIN: empaquetado en un encrypted PIN block (EPB), enviado al emisor; cifrado por el terminal con 3-DES y sometido a "PIN translations" (descifrado y recifrado) a lo largo de la cadena. Tampoco depende de EMV.

### 2.7.1 Strong Customer Authentication

Desde septiembre de 2019 la SCA es obligatoria por ley en la Unión Europea (con exenciones). Exige al menos dos factores dinámicamente enlazados de "algo que eres", "algo que tienes" y "algo que sabes". En card-present, la tarjeta es "algo que tienes" y los métodos basados en PIN cumplen; en card-not-present, solo la autenticación 3D Secure obligatoria, correctamente implementada por el emisor, ha dado el cumplimiento necesario.

## 2.8 Manejo del PIN

### 2.8.1 Verificación del PIN

Dos métodos a elección del emisor: almacenar el PIN cifrado en base de datos y delegar su validación a un HSM, o apoyarse en el PVV (PIN verification value), manejado como el CVV, donde solo la clave de verificación es secreta y el valor de validación llega junto al PIN cifrado.

### 2.8.2 Almacenar el PIN cifrado

El PIN ethalon se cifra dentro del HSM bajo una PEK (PIN encryption key) y se guarda en la base de datos del host del emisor, junto al índice de la clave o la clave cifrada bajo KEK (PEKKEK). Al llegar el payment message, el emisor entrega al HSM el EPB, el PIN ethalon y la información de clave, y el HSM indica si el PIN recibido es válido.

### 2.8.3 Apoyarse en el PVV

El PVV se calcula de forma muy similar al CVV y se codifica en la discretionary data de Track 1 y 2; su ubicación exacta y la PVK (compartida solo con el scheme relevante) son secretas. El emisor guarda las PVK cifradas bajo KEK; al recibir el mensaje, envía al HSM el EPB entrante, la PVK y los datos de clave para validar. El PVV sigue usándose para stand-in processing.

## 2.9 Tipos de transacción

Se dividen en retail, retiros/depósitos de efectivo y payment transactions.

### 2.9.1 Retail

- Purchase: la más frecuente; se autoriza online y se presenta a clearing (los schemes animan a hacerlo en ~3 días). Las transacciones de juego (gambling) se distinguen a veces como unique o quasi-cash por su mayor riesgo.
- Pre-authorization: cuando el monto final no se conoce o la entrega es posterior (hotelería, muebles a medida).
- Account validation: sin intención de compra; suele hacerse como pre-autorización de monto cero, con respuesta 85 ("No reason to decline") además de 00 ("Success"). Peor alternativa: pre-autorizar un monto mínimo ($0.01).
- Completion/capture: finaliza una pre-autorización.
- Refund: acredita fondos por devoluciones o ajustes; limitado al monto original (salvo diferencias de tipo de cambio); admite reembolsos parciales y múltiples.
- Reversal: cancela una transacción original (total o parcial); puede ser automática por motivos técnicos y aplica a más tipos (pre-auth, payment, refund, balance inquiry). Un purchase + refund aparece como dos líneas en el estado; un purchase + reversal oportuno no aparece.
- Balance inquiry: consulta saldos al emisor; útil en ATM y en POS con prepago. Alternativa: partial authorization, con código de decline que indica el monto parcial permitido, tras lo cual el POS pide otro medio de pago (split tender).
- Purchase with cashback: entrega efectivo junto a la compra (sobre todo en débito). También designa el arreglo promocional emisor-tarjetahabiente (puntos, descuentos, cheque), transparente al comercio e indistinguible de un purchase básico.

### 2.9.2 Retiros y depósitos de efectivo

- Withdrawal: retiro inmediato en efectivo, en ATM o por cajero con terminal; el tarjetahabiente puede elegir la cuenta. Difiere del cash advance/disbursement (adelanto sobre el saldo de crédito).
- Deposit: depósito de fondos, típicamente en ATM; alto riesgo de lavado o fraude.

### 2.9.3 Payment transactions

También llamadas original credit o credit fund transfer; envían fondos al destinatario. Dos tipos: business-to-cardholder (fund disbursements: rebates, pagos de juego, salarios, pensiones, préstamos) y cardholder-to-cardholder (dos partes: funding transaction del remitente al merchant y luego payment transaction a los destinatarios). Aunque refunds y fund disbursements debitan al comercio y acreditan al tarjetahabiente, difieren en uso, reglas de scheme y fees; los disbursements suelen requerir nombre y dirección del receptor. Las transferencias entre tarjetahabientes tienen límites legales estrictos por su potencial de lavado y fraude.

## 2.10 Tipos, condiciones y modos de entrada del POS (card-present)

Las capacidades del terminal y la tarjeta, la tecnología de transferencia y las condiciones de cada transacción determinan el procesamiento. Un terminal puede ser atendido o desatendido, estar dentro o fuera del local, capturar o no la tarjeta, y tener un PED que puede fallar en el momento. Las características se transmiten como campos opcionales u obligatorios.

### 2.10.1 Métodos de transferencia de datos

Por contacto (lector de chip y/o banda) o por proximidad (lector contactless). La tarjeta puede tener chip, banda y módulo NFC.

### 2.10.2 Formatos de datos

El dato se representa como "Magstripe" o "EMV" (full-grade), lo que, combinado con los métodos de transferencia, da cuatro opciones:

- EMV contact ("chip and dip"): no soportado por móviles; intercambio criptográfico completo; mensaje con ICC data en DE 55 y Track 2 en DE 35.
- EMV contactless: soportado por móviles NFC con secure element; ICC data en DE 55.
- Magstripe contact: no soportado por móviles; swipe; datos en DE 35 (Track 2), DE 45 (Track 1) o ambos.
- Magstripe contactless: soportado por móviles NFC; emula lectura de banda generando Track 2 con elementos criptográficos dinámicos; datos en DE 35 y opcionalmente DE 45.

#### 2.10.2.1 Capacidades y condiciones del terminal

Reguladas por PCI (por ejemplo, PEDs seguros) y reglas de marca. Capacidades de entrada de PAN: key entry (teclado, sin implicar PIN), magnetic stripe, chip reader (EMV contact), contactless reader (EMV contactless) y contactless magnetic stripe (algunos schemes la exigen en todo terminal contactless). La capacidad de PIN entry puede requerir indicar la longitud máxima (hasta 12 caracteres). Otras: card capture (retención, siempre en ATM), card data output (instrucciones al chip; escritura de Track 3) y terminal output (display, impresora; un terminal sin impresión no debería reportar signature).

Ubicación y atención: atendido/desatendido (CAT, cardholder-activated terminal); dentro o fuera del local; propiedad del merchant, card acceptor o tarjetahabiente. Las cuatro combinaciones típicas: atendido on-premises, atendido off-premises, desatendido on-premises y desatendido off-premises.

Categorías de terminal: mPOS (móvil/tablet + PED externo), terminales de compra a bordo de aviones (autorización offline por conectividad limitada), desatendidos clasificados por disponibilidad de PIN pad (límite de monto sin él), y surtidores de combustible, peajes y transporte masivo (requisitos estrictos de tiempo; riesgo calculado de blacklisting de tarjetas).

Condiciones transitorias: card y cardholder presentes o ausentes; "suspected fraud"; PIN pad presente pero no funcional (distinto de no tener la capacidad); lectura de chip completada pero no confiable, fallback a banda, etc. El conjunto de transferencia y condiciones se llama POS entry mode (valores comunes en el Data Element 22, sección 3.3.4).

### 2.10.3 Proceso de certificación del terminal

Un POS debe cumplir estándares según jurisdicción y tipo: PCI PTS (Pin Transaction Security) si entra PIN, CE marking en Europa, prueba FCC en EE.UU. para capacidades inalámbricas. Además, antes del despliegue en vivo, hay una prueba de integración end-to-end ("card scheme certification") que certifica el procesamiento correcto incluyendo la conexión al host adquirente y al scheme. Usa test cards y simuladores o entornos de prueba del scheme; un cambio de host o de terminal exige recertificación; los logs se envían al scheme y a veces hay una prueba en vivo con un ingeniero del scheme.

## 2.11 Tipos, condiciones y modos de entrada card-not-present

En card-not-present el POS es un concepto virtual; se refiere a transacciones donde la tarjeta no puede estar presente por definición. Categorías:

- Mail/fax order: PAN y expiry enviados por correo o fax.
- Telephony order: PAN comunicado a un representante o vía IVR/ARU (DTMF o voz). Junto al anterior forman MOTO (Mail Order/Telephony Order).
- e-commerce: PAN comunicado electrónicamente por Internet directamente a los sistemas del card acceptor (si lo teclea el comercio, es MOTO, no e-commerce).
- Merchant-initiated transactions: iniciadas por el sistema del comercio, no por el tarjetahabiente. Incluyen standing authorization ("card on file", cargos ad-hoc), recurring transaction (cobro periódico, como cuotas de membresía) e installment transaction (pago parte de una compra mayor, provisto por merchant, adquirente o emisor). No todo scheme o solución distingue estos casos entre sí.

## Ideas clave

- El plástico y su interacción se rigen por una familia de estándares ISO/IEC (7811/7812/7813, 7816, 14443, 4909, 9564) más EMV.
- El PAN (13 a 19 dígitos) se estructura en IIN/BIN, IAN y check digit (Luhn); el BIN y las BIN tables son clave para enrutar y aplicar reglas por marca y producto.
- La banda tiene tres pistas: Track 1 (alfanumérica, 79), Track 2 (numérica, 40) y Track 3 (en desuso); el service code de tres dígitos define interchange, modo de autorización y servicios.
- Hay cuatro CVV (CVV1, CVV2, iCVV, dCVV), calculados con CVK en HSM mediante 3-DES y decimalización; PCI DSS prohíbe almacenar CVV1 y las pistas.
- La verificación del tarjetahabiente abarca Failed CVM, No CVM, signature, offline PIN y online PIN; la SCA de la UE (desde 2019) exige dos factores dinámicamente enlazados.
- El PIN se valida almacenándolo cifrado (HSM) o vía PVV/PVK, y el online PIN viaja como EPB con "PIN translations" a lo largo de la cadena.
- Los tipos de transacción cubren retail (purchase, pre-auth, completion, refund, reversal, balance inquiry, cashback), efectivo (withdrawal, deposit) y payment transactions.
- Capacidades del terminal, de la tarjeta y condiciones transitorias determinan el POS entry mode; full-grade EMV usa ARQC e ISO 55, mientras part-grade cae a formato de banda con iCVV/dCVV.
