# Contact Chip Transactions (Transacciones con chip de contacto) — Estudio

## Tarjetas de repaso

P: ¿Por qué se justificó la migración de banda magnética a chip (ICC)?
R: Para combatir el fraude (la banda es fácil de clonar) y permitir autorizaciones offline más inteligentes mediante un computador seguro con contadores y criptografía propios.

P: ¿Qué diferencia hay entre un "ICC" y una "EMV card"?
R: Un ICC es cualquier smartcard compatible con ISO/IEC 7816; una EMV card cumple además la especificación EMV. Toda EMV card es un ICC, pero no al revés (SIMs, IDs, monederos, transporte).

P: ¿Cómo se organiza el sistema de ficheros del chip y cómo se referencia un DF?
R: Es jerárquico (ISO/IEC 7816-4) con el master file (MF, FID 0x3F00) como raíz, dedicated files (DF, carpetas) y elementary files (EF). Un DF se referencia por FID, por AID/DF Name o por ruta de FIDs; el AID favorece la interoperabilidad.

P: ¿Qué campos componen un C-APDU y qué valores toma CLA en EMV?
R: CLA, INS, P1, P2 obligatorios y Lc, Data, Le opcionales. En EMV el nibble alto de CLA solo vale 0 (ISO 7816) u 8 (propietario EMV), por lo que CLA solo toma 04, 0C, 84 y 8C.

P: ¿Qué son los DOL y cuáles define EMV?
R: Son data object lists para datos de formato fijo: la tarjeta da la lista de tags y longitudes y el terminal devuelve los valores concatenados. EMV define PDOL, CDOL1, CDOL2, TDOL y DDOL.

P: ¿Qué guardan el TSI y el TVR?
R: El TSI (2 bytes, 6 bits) indica a alto nivel las etapas completadas; el TVR (5 bytes) detalla por byte el resultado de cada etapa (autenticación offline, restricciones, CVM, riesgo del terminal, autenticación del emisor y scripts).

P: ¿Cuál es el flujo completo de una transacción con chip?
R: Selección de aplicación → GPO (AIP/AFL) → lectura de datos → autenticación offline → restricciones de procesamiento → CVM → riesgo del terminal → análisis de acción de terminal y tarjeta → GENERATE AC → autenticación del emisor → scripts → finalización.

P: ¿Qué devuelve la tarjeta al comando GET PROCESSING OPTIONS?
R: El AIP (Application Interchange Profile) y el AFL (Application File Locator), bajo tag 80 (concatenado) o tag 77 (82 para AIP, 94 para AFL).

P: ¿Cuáles son los tres métodos de autenticación offline y cómo se priorizan?
R: SDA (estática, vulnerable a replay), DDA (dinámica) y CDA (combinada con el criptograma). Si varios son mutuamente soportados se prefiere CDA, luego DDA, luego SDA.

P: ¿Cómo resuelve EMV el problema de escala de la autenticación offline?
R: Con una cadena de confianza (key chain of trust): el esquema es CA raíz y distribuye su clave pública a los terminales, cada emisor firma su clave con la del esquema y cada tarjeta lleva su clave firmada por el emisor.

P: ¿Qué determina la CVM List y qué estructura tiene?
R: Determina el método de verificación del titular. Tiene dos importes X e Y (en Application Currency Code 9F42) y una lista de reglas (CVR) de 2 bytes, cada una con un CVM code y un CVM Condition code.

P: ¿Cuáles son los tres chequeos de la gestión de riesgo del terminal?
R: Floor limit (importe para ir online), selección aleatoria de transacciones (random transaction selection bajo umbral BRS) y velocity checking (transacciones desde la última autorización online).

P: ¿Qué son TC, ARQC y AAC y cuál es su jerarquía?
R: Criptogramas que pide la tarjeta: TC (autorización offline), ARQC (intento online) y AAC (declinación offline), en jerarquía TC > ARQC > AAC; la tarjeta puede degradar lo que pide el terminal.

P: ¿Cómo autentica el terminal al emisor?
R: Con EXTERNAL AUTHENTICATE (si el bit 3 del AIP está activo) o combinándolo con el segundo GENERATE AC: el ICC descifra el ARPC, lo XOR con el ARQC, extrae el ARC y lo compara; si coincide, el emisor queda autenticado.

P: ¿Para qué sirven los issuer scripts y qué plantillas existen?
R: Permiten al emisor modificar la tarjeta de forma segura (p. ej. bloquear una tarjeta perdida). Hay dos plantillas: Issuer Script Template 1 (tag 71, antes del segundo GAC) e Issuer Script Template 2 (tag 72, después).

## Preguntas de autoevaluación

P: ¿Qué hace un terminal con lector de chip si la banda tiene código de servicio 2 o 6, y cuándo se permite el magstripe fallback?
R: Debe pedir el uso del chip; solo tras fallar el chip se permite el magstripe fallback. (Sección: Arquitectura del ICC y selección de tecnología)

P: Explica cómo se recupera una clave pública mediante certificado en la autenticación offline.
R: Se descifra el certificado con la clave pública que se posee; el resultado debe empezar por 0x6A y terminar en 0xBC, se separa el certificado descifrado (MR) y el hash (H, últimos 20 bytes) y se valida combinando con el key remainder y recalculando el hash. (Sección: Autenticación offline de la tarjeta)

P: ¿Qué ventaja tiene CDA frente a SDA y DDA?
R: CDA no usa comando dedicado: la tarjeta firma los datos del paso GENERATE AC, por lo que es casi tan rápida como SDA y tan segura como DDA. (Sección: Autenticación offline de la tarjeta)

P: ¿Qué tres comprobaciones realiza el terminal en las restricciones de procesamiento?
R: Versión (Application Version Number 9F08), Application Usage Control (9F07, con Issuer Country Code para doméstica/internacional) y fechas (Application Effective Date 5F25 ≤ hoy y Application Expiration Date 5F24 no excedida). Cualquier fallo activa el bit correspondiente del TVR. (Sección: Restricciones de procesamiento)

P: ¿Cómo combina el terminal los action codes para su análisis de acción?
R: Usa action codes del emisor (Denial 9F0E, Online 9F0F, Default 9F0D) y del acquirer (Terminal Action Codes); aplica OR a cada par emisor/acquirer y AND con el TVR; si el resultado no es cero, dispara la acción (declinar offline, ir online o default si falla el online). (Sección: Análisis de acción de terminal y de tarjeta)

P: ¿Cómo diferencia el terminal el primer GENERATE AC para pedir TC, ARQC o AAC?
R: Con los bits 8–7 de P1 (0x00 AAC, 0x01 TC, 0x10 ARQC) y el bit 5 para solicitar CDA junto al criptograma si no es AAC; un tercer GENERATE AC da 6985. (Sección: Generación de criptogramas y autenticación del emisor)

P: ¿Qué dos vías existen para la selección de aplicación y cómo se distinguen por el PSE?
R: Selección indirecta leyendo el PSE (DF Name 1PAY.SYS.DDF01) parseando ADFs (tag 61) y DDFs (tag 9D), o selección directa consultando los AID uno a uno con SELECT. Si el PSE existe, SELECT devuelve 9000 con el FCI (tag 6F); si no, devuelve 6A82. (Sección: Selección de aplicación e inicio de procesamiento)

P: ¿Cómo valida la tarjeta el PIN offline y qué códigos de respuesta indica VERIFY?
R: El PIN se valida entre terminal y tarjeta sin el emisor, en claro (P2 0x80) o cifrado (P2 0x88); la tarjeta cuenta los intentos. VERIFY devuelve 9000 (éxito), 6983/6984 (bloqueado o fallo de descifrado) y 63Cn (intento fallido con n intentos restantes). (Sección: Verificación del titular (CVM))

## Puntos a dominar

- Distinguir ICC de EMV card y describir el sistema de ficheros DF/EF (MF, ADF, DDF) y sus modos de referencia (FID, AID/DF Name, SFI).
- Explicar la estructura del APDU (CLA, INS, P1, P2, SW1/SW2), los valores de CLA en EMV y los grupos de SW1/SW2.
- Reconocer el formato BER-TLV y el papel de los DOL (PDOL, CDOL1, CDOL2, TDOL, DDOL).
- Reproducir de memoria el flujo completo de la transacción con chip y qué registra el TVR/TSI en cada etapa.
- Comparar SDA, DDA y CDA y describir la cadena de confianza esquema → emisor → tarjeta.
- Interpretar la CVM List (importes X/Y, CVM code y Condition code) y los métodos de verificación del titular.
- Enumerar los tres chequeos de riesgo del terminal (floor limit, selección aleatoria, velocity checking) y quién los fija.
- Relacionar los criptogramas TC/ARQC/AAC y el ARPC con la autenticación mutua tarjeta-emisor y el papel de los issuer scripts.
