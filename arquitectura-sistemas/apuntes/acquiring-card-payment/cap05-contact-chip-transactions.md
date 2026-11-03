# Acquiring Card Payments — Ilya Dubinsky (CRC Press, Taylor & Francis, 2019)
## Capítulo 5 — Contact Chip Transactions (Transacciones con chip de contacto)

> Nota de extracción: el texto se obtuvo de la capa de texto del PDF; las citas usan la página del PDF como `(PDF p. N)`.

## Lo que necesitas saber

El capítulo explica cómo funciona una transacción EMV con chip de contacto, desde que la tarjeta se inserta hasta que se completa. La tesis es que migrar de la banda magnética al circuito integrado (ICC) se justificó por dos motivos: combatir el fraude (una banda magnética es fácil de clonar) y permitir autorizaciones offline más inteligentes. El chip es un pequeño computador seguro que mantiene contadores internos independientes del terminal y usa criptografía para autenticar tarjeta y transacción.

Se distingue "ICC" (cualquier smartcard compatible con ISO/IEC 7816) de "EMV card" (compatible con la especificación EMV): toda tarjeta EMV es un ICC, pero no al revés (SIMs, IDs gubernamentales, monederos, transporte). Sales sabiendo la arquitectura del chip (hardware de contactos, sistema de ficheros DF/EF), el protocolo de comandos (APDU: CLA, INS, P1, P2, SW1/SW2) y el formato de datos EMV (BER-TLV, tags, plantillas y DOLs).

El grueso del capítulo recorre el flujo completo de una transacción con chip: selección de aplicación, inicio de procesamiento (GPO, AIP, AFL), lectura de datos, autenticación offline (SDA/DDA/CDA), restricciones de procesamiento, verificación del titular (CVM), gestión de riesgo del terminal, análisis de acción de terminal y de tarjeta, generación de criptogramas (GENERATE AC), autenticación del emisor, procesamiento de scripts y finalización. A lo largo del texto se usan dos registros clave, TVR y TSI, que acumulan resultados y decisiones.

## Arquitectura del ICC y selección de tecnología

Un ICC es un computador embebido en el plástico que ejecuta una o varias aplicaciones. En contacto, el terminal alimenta el chip y se comunica por los contactos físicos; en contactless, energía y comunicación son inalámbricas. El framework destacado es JavaCard. El chip aloja un sistema de ficheros con "dedicated files" (DF, carpetas) y "elementary files" (EF, ficheros).

El hardware de contacto sigue ISO 7816 con 8 contactos C1–C8: C1 Vcc (alimentación), C2 RST (reset), C3 CLK (reloj), C5 GND (tierra), C7 I/O (comunicación half-duplex). C4 y C8 son RFU y C6 (Vpp) está obsoleto. El circuito contiene ROM (pregrabada en fabricación), RAM (se borra entre activaciones) y EEPROM (reescribible). La tarjeta contactless (PICC) sigue ISO/IEC 14443, opera a 13,56 MHz, es parcialmente compatible con NFC y se alimenta por inducción; hay tipos A y B.

El sistema de ficheros (ISO/IEC 7816-4) es jerárquico: el DF raíz es el master file (MF, FID 0x3F00). EMV define ADF (contenedor de una aplicación) y DDF (carpeta de carpetas/aplicaciones). Un DF se referencia por FID (2 bytes, ligado a ubicación física), por AID / "DF Name" (hasta 16 bytes, independiente de la ubicación) o por ruta de FIDs; el AID favorece la interoperabilidad. Un AID registrado se compone de RID (identificador del proveedor) y PIX opcional; CAT indica la categoría (A internacional, D nacional). Ejemplo: `A0000000031010` (Visa). Los EF pueden ser transparentes, lineales fijos, lineales variables o cíclicos, y se referencian por FID o por SFI (número 1–30), prefiriéndose el SFI en entornos EMV.

En la interacción tarjeta-terminal, un terminal con lector de chip debe pedir el uso del chip si la banda tiene código de servicio 2 o 6; solo tras fallar el chip se permite el magstripe fallback. La tarjeta no tiene batería: el terminal da energía, envía señal en RST y la tarjeta responde con el ATR. A partir de ahí el terminal controla la comunicación.

## Interfaz de la tarjeta: APDU, CLA, INS, SW y SFI

Tras el reset la tarjeta envía el ATR, que lista los protocolos soportados (valor T): T=0 (protocolo de caracteres, hardware más débil) y T=1 (protocolo de bloques, sin restricción de datos en comando y respuesta). La comunicación aplicativa son comandos y respuestas llamados APDU: el terminal envía C-APDU y la tarjeta responde con R-APDU. El C-APDU tiene campos CLA (clase, 1 byte), INS (instrucción, 1 byte), P1 y P2 (parámetros obligatorios), Lc y Data (opcionales) y Le (longitud máxima esperada). El R-APDU tiene Data opcional y el trailer obligatorio SW1/SW2.

En EMV el nibble alto de CLA solo vale 0 (comandos inter-industria ISO 7816) u 8 (propietarios EMV); con mensajería segura Formato 1 (BER-TLV) o Formato 2 (propietario, MAC en los últimos 4–8 bytes) y un único canal lógico. Así CLA solo toma 04, 0C, 84 y 8C. Ejemplos de INS: SELECT (`0X A4`, ISO) y GET PROCESSING OPTIONS (`8X A8`, EMV). Grupos de SW1/SW2: `9000` éxito, `62xx`/`63xx` advertencia, `64xx`/`65xx` error de ejecución, `67xx`–`6Fxx` error de verificación. El SFI permite leer el Application Elementary File (AEF, registros con plantilla tag 70) con READ RECORD; EMV reserva SFI 1–10 para datos EMV, 11–20 para datos propietarios del esquema y 21–30 para datos del emisor.

## DOLs y tags EMV

Los datos EMV usan BER-TLV, flexible e interoperable. Para datos de formato fijo (más rápidos) EMV define los DOL (data object list): la tarjeta entrega la lista de tags y longitudes (TL1||TL2||…) y el terminal devuelve los valores concatenados (V1||V2||…), truncando o rellenando con ceros. DOLs definidos: PDOL (con GET PROCESSING OPTIONS), CDOL1 y CDOL2 (con GENERATE AC), TDOL (hash de certificado de transacción) y DDOL (con INTERNAL AUTHENTICATE). Los tags se agrupan en plantillas (tipos compuestos); el Data Elements Dictionary de EMV Book 3 lista nombre, descripción, fuente (ICC/terminal/emisor), formato, plantilla y tag. Ejemplo: tag `9F42` es Application Currency Code (ISO 4217), origen ICC, en plantillas 70 o 77.

## TVR y TSI

Durante la transacción el terminal guarda resultados en dos registros. El TSI (Transaction Status Information, 2 bytes, solo 6 bits) indica a alto nivel las etapas completadas: autenticación offline de datos, verificación del titular, gestión de riesgo de la tarjeta, autenticación del emisor, gestión de riesgo del terminal y procesamiento de scripts. El TVR (Terminal Verification Results, 5 bytes) detalla cada etapa: byte 1 autenticación offline de datos (p. ej. "SDA failed"), byte 2 restricciones de procesamiento, byte 3 verificación del titular, byte 4 gestión de riesgo del terminal, byte 5 autenticación del emisor y scripts. Aplicando máscaras de bits al TVR se decide declinar offline, autorizar offline o ir online; EMV recomienda incluir el TVR en CDOL1/CDOL2.

## Selección de aplicación e inicio de procesamiento

El terminal construye una lista de candidatas y elige una. Hay dos vías: selección indirecta leyendo el PSE (fichero opcional con DF Name `1PAY.SYS.DDF01`) mediante READ RECORD, parseando ADFs (AID en tag 61) y DDFs (tag 9D); o selección directa, consultando uno a uno con SELECT los AID que el terminal soporta (full name matching), con la opción de partial name matching enviando un prefijo. Si el PSE existe, el SELECT devuelve `9000` con el FCI (tag 6F); si no, devuelve `6A82`. En la selección final, el "Application Priority Indicator" (tag 87) define orden y si requiere confirmación del titular; un SELECT final devuelve el FCI de la aplicación. Seleccionar bien no garantiza compatibilidad total: las restricciones de procesamiento pueden revelar una versión incompatible. El FCI puede incluir "Language Preference" (5F2D), "Application Preferred Name" (9F12), "Issuer Code Table Index" (9F11) y el PDOL (9F38).

Para iniciar procesamiento el terminal resetea TVR y TSI y envía GET PROCESSING OPTIONS (GPO) con un objeto tag 83 (vacío si no hay PDOL). La tarjeta responde con el AIP (Application Interchange Profile) y el AFL (Application File Locator), bajo tag 80 (concatenado) o tag 77 (82 para AIP, 94 para AFL). El AIP (2 bytes, solo el primero en uso) indica soporte de SDA (bit 7), DDA (bit 6), verificación del titular (bit 5), gestión de riesgo del terminal (bit 4), autenticación del emisor (bit 3) y CDA (bit 1). El AFL es un array de entradas de 4 bytes: byte 1 el SFI, bytes 2–3 primer y último registro a leer, byte 4 el último registro usado para autenticación offline de datos. Ejemplo: `0D 01 06 04` lee registros 1–6 del SFI 0D y usa 1–4 para autenticación.

## Lectura de datos de la aplicación

El terminal itera sobre las entradas del AFL y emite READ RECORD por cada registro; la tarjeta devuelve la plantilla tag 70. El terminal apila todos los objetos en un heap común, descartando los desconocidos y conservando los opcionales. Luego verifica los objetos obligatorios: Application Expiry Date (5F24), PAN (5A), CDOL1 (8C) y CDOL2 (8D). Según el AIP, también exige otros: si soporta verificación del titular (bit 5), debe estar la CVM List (tag 8E); según el soporte de SDA/DDA/CDA, los objetos correspondientes.

## Autenticación offline de la tarjeta

Antes del chip solo existía el holograma. Con EMV el terminal autentica la tarjeta criptográficamente: se cargan claves públicas del esquema y la tarjeta entrega una firma que el terminal valida. El esquema puede omitir este paso confiando en la autenticación online del emisor. Hay tres métodos, y si varios son mutuamente soportados se prefiere CDA, luego DDA, luego SDA:

- SDA (estática): el emisor precalcula un valor estático escrito en la tarjeta; confirma autenticidad de los datos personalizados pero es vulnerable a replay y permite hardware más débil.
- DDA (dinámica): la tarjeta calcula el valor en cada transacción con datos aleatorios de tarjeta y terminal; prueba origen válido y que no se modificó tras la personalización.
- CDA (combinada): como DDA, pero el valor de autenticación se genera junto al criptograma de aplicación.

Todos comparten pasos: recuperar claves, calcular una firma de forma independiente y validar. La cadena de confianza (key chain of trust) resuelve el problema de escala: el esquema actúa como CA raíz y distribuye su clave pública a terminales; cada emisor firma su clave pública con el esquema; cada tarjeta lleva su clave firmada por el emisor. El terminal, con la clave pública del esquema, confirma que la tarjeta la emitió un banco de confianza.

La recuperación de claves públicas (emisor e ICC) usa un certificado: se descifra con la clave pública que se tiene, el resultado debe empezar por `0x6A` y terminar en `0xBC`, se separa en el certificado descifrado (MR) y el hash (H, últimos 20 bytes), y se valida combinando con el key remainder y recalculando el hash. El índice de la clave CA lo indica el tag 8F ("Certification Authority Public Key Index"). En la validación de datos firmados el terminal arma un data authentication input vector, obtiene los datos firmados S y la clave K, descifra, comprueba cabecera/trailer y compara el hash H.

SDA recupera la clave del emisor con los tags 90 (certificado), 92 (remainder) y 9F32 (exponente), y valida "Signed Static Application Data" (tag 93). DDA añade dinamismo: el DDOL (tag 9F49) define el input e incluye siempre el "Unpredictable Number" (9F37); el terminal recupera además la clave pública del ICC (tags 9F46, 9F48, 9F47) y obtiene la firma con el comando INTERNAL AUTHENTICATE, recibiendo "ICC Dynamic Data" (9F4C). CDA no usa comando dedicado: la tarjeta firma los datos del paso GENERATE AC (PDOL, CDOL1/CDOL2 y los valores de respuesta), por lo que es casi tan rápida como SDA y tan segura como DDA; requiere "Unpredictable Number" en ambos CDOLs. En contactless el método equivalente es fDDA (fast DDA).

## Restricciones de procesamiento

El terminal comprueba tres cosas. Versión: compara "Application Version Number" (9F08); si difiere, marca el TVR. Application Usage Control (9F07, 2 bytes): valida flags de uso (cash doméstico, servicios internacionales, cajeros u otros terminales); según "Issuer Country Code" (5F28/5F55/5F56) decide si la transacción es doméstica o internacional. Fechas: "Application Effective Date" (5F25) debe ser ≤ fecha actual (si no, "Application not yet effective"); "Application Expiration Date" (5F24) no debe estar excedida ("Expired application"). Cualquier fallo activa el bit correspondiente del TVR.

## Verificación del titular (CVM)

La CVM List (tag 8E) tiene dos importes X e Y (en "Application Currency Code" 9F42) y una lista de reglas (CVR) de 2 bytes. Cada regla tiene un CVM code (método + bit 7: si es 0 se detiene al fallar, si es 1 se pasa a la siguiente) y un CVM Condition code (cuándo aplica). Métodos: fallo forzado (000000), PIN offline en claro (000001), PIN online (000010), PIN offline en claro y firma (000011), PIN offline cifrado (000100), PIN offline cifrado y firma, firma (011110) y sin CVM (011111). Condiciones: siempre (0x00), si el terminal lo soporta (0x03), escenarios de efectivo (0x01/0x04/0x05), sin efectivo (0x02) y bajo/sobre valor X o Y (0x06–0x09). El resultado se guarda en "CVM Results" (9F34, 3 bytes: código, condición y estado: 0 desconocido, 1 fallido, 2 exitoso); sin CVM realizado el código es 0x3F.

El PIN offline se valida entre terminal y tarjeta sin el emisor, en claro o cifrado; la tarjeta cuenta los intentos. Se puede consultar el "PIN Try Counter" (9F17) con GET DATA y verificar con VERIFY (P2 0x80 en claro, 0x88 cifrado): `9000` éxito, `6983`/`6984` bloqueado o fallo de descifrado, `63Cn` intento fallido con n intentos restantes. El PIN en claro va en bloque ISO-9564 Formato 2. Para el cifrado se recupera la clave de cifrado de PIN del ICC (tags 9F2D/9F2E/9F2F, o la clave pública del ICC) y se usa GET CHALLENGE para obtener el número impredecible antes de cifrar el bloque. El PIN online se transmite al emisor en bloque cifrado; al llegar a la red del esquema el bloque debe usar formatos 0, 1 o 4 y cifrarse con una Zone PIN Key.

## Gestión de riesgo del terminal

La autorización offline permite a la tarjeta decidir sin el emisor según umbrales y contadores. La gestión de riesgo del terminal reúne resultados en bits del TVR para forzar selectivamente la autorización online. Tres chequeos: floor limit (importe mínimo por encima del cual se va online; el acquirer lo fija y puede bajarlo a cero; se puede sumar un log para evitar "split sales"); selección aleatoria de transacciones (random transaction selection) bajo un umbral BRS, con un número aleatorio 1–99 comparado contra un porcentaje objetivo que crece linealmente hacia el floor limit; y velocity checking (número de transacciones desde la última autorización online), con "Lower Consecutive Offline Limit" (9F14) y "Upper Consecutive Offline Limit" (9F23), restando "Last Online ATC Register" (9F13) del ATC (9F36) y marcando el TVR si se exceden los límites o si es tarjeta nueva (ATC = 0). Floor limit y selección aleatoria los fija el acquirer; velocity lo fija el emisor.

## Análisis de acción de terminal y de tarjeta

El terminal toma una decisión preliminar (declinar offline, autorizar offline o ir online) combinando action codes del emisor (personalizados en la tarjeta: Issuer Action Code Denial 9F0E, Online 9F0F, Default 9F0D) y del acquirer (Terminal Action Codes en el terminal), cada registro de 5 bytes como el TVR. Los "Denial" fuerzan declinación offline, los "Online" fuerzan ir online y los "Default" definen qué hacer si falla el intento online. El terminal aplica OR a cada par emisor/acquirer y AND con el TVR; si el resultado no es cero, se dispara la acción.

Luego la tarjeta hace su análisis de acción pidiendo un criptograma: TC (Transaction Certificate, autorización offline), ARQC (Authorization ReQuest Cryptogram, intento online) o AAC (Application Authentication Cryptogram, declinación offline), en jerarquía TC > ARQC > AAC. La tarjeta puede degradar lo que pide el terminal. Si devuelve TC o AAC, la transacción se completa.

## Generación de criptogramas y autenticación del emisor

El terminal emite hasta dos GENERATE AC (GAC); un tercero da `6985`. En el primer GAC pide TC/ARQC/AAC por los bits 8–7 de P1 (0x00 AAC, 0x01 TC, 0x10 ARQC) y el bit 5 para solicitar CDA junto al criptograma (si no es AAC). El input se arma con CDOL1 (primer GAC) y CDOL2 (segundo), incluyendo típicamente importes, fecha, tipo y moneda, datos del terminal (Terminal Country Code 9F1A, TVR tag 95) y obligatoriamente el "Unpredictable Number" (9F37). El tag 98 (TC Hash Value) hace que el terminal calcule un hash sobre el TDOL (tag 97).

El criptograma de aplicación es un MAC de ciertos campos con una clave de sesión derivada del ICC Application Cryptogram Master Key usando el ATC (recomendación EMV con 3DES: bloques F1/F2 con tercer byte 0xF0 y 0x0F, cifrados y concatenados en clave de doble longitud). La respuesta del GAC va en Formato 1 (tag 80) o Formato 2 (tag 77, obligatorio para CDA), con el Cryptogram Information Data (CID, 9F27), ATC (9F36) y Application Cryptogram (9F26).

El emisor valida el ARQC (derivando la master key por PAN y la session key por ATC) y calcula el ARPC (XOR del ARC con el ARQC, cifrado con la misma session key). Devuelve "Issuer Authentication Data" (tag 91) con ARPC y, opcionalmente, "Authorization Response Code". El terminal autentica al emisor con EXTERNAL AUTHENTICATE (si el bit 3 del AIP está activo) o combinándolo con el segundo GAC: el ICC descifra el ARPC, lo XOR con el ARQC, extrae el ARC y lo compara; si coincide, el emisor queda autenticado. Un fallo del EXTERNAL AUTHENTICATE marca "Issuer authentication failed" en el TVR.

## Procesamiento de scripts y finalización

El emisor puede enviar issuer scripts junto a la respuesta online para modificar la tarjeta de forma segura (p. ej. bloquear una tarjeta perdida). Hay dos plantillas: "Issuer Script Template 1" (tag 71), enviada antes del segundo GAC, y "Issuer Script Template 2" (tag 72), después. Cada plantilla lleva un identificador opcional (9F18) y comandos (tag 86) que el terminal transmite tal cual; ante un error deja de enviar y marca el TVR ("Script processing failed before/after final GENERATE AC"). Los resultados se guardan en 5 bytes por comando. El segundo GAC con la generación de TC o AAC concluye la transacción EMV; el TC se envía al emisor como evidencia.

## Ideas clave

- La migración a chip busca frenar el fraude de clonado de banda magnética y habilitar autorizaciones offline fiables mediante un computador seguro con contadores y criptografía propios.
- Todo EMV card es un ICC (ISO/IEC 7816), pero no al revés; el ICC usa un sistema de ficheros DF/EF referenciable por FID, AID/DF Name o SFI.
- La comunicación es por APDU (CLA, INS, P1, P2, SW1/SW2); en EMV CLA solo vale 04, 0C, 84, 8C y los datos siguen BER-TLV con DOLs para formato fijo.
- El flujo es: selección de aplicación → GPO (AIP/AFL) → lectura de datos → autenticación offline → restricciones → CVM → riesgo del terminal → análisis de acción → GENERATE AC → autenticación del emisor → scripts → finalización.
- La autenticación offline tiene tres niveles: SDA (estática, vulnerable a replay), DDA (dinámica) y CDA (combinada con el criptograma, la más segura); se apoyan en una cadena de confianza esquema → emisor → tarjeta.
- La CVM List decide el método de verificación del titular (PIN offline en claro/cifrado, PIN online, firma o ninguno) según importes X/Y y condiciones.
- TVR y TSI acumulan resultados; los action codes del emisor y del acquirer (Denial/Online/Default) y el TVR determinan si se declina offline, se autoriza offline o se va online.
- Los criptogramas TC/ARQC/AAC (jerárquicos, degradables por la tarjeta) y el ARPC permiten autenticación mutua tarjeta-emisor; los issuer scripts actualizan la tarjeta de forma segura.
