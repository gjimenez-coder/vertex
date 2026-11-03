# EMV Contactless Transactions (Transacciones EMV sin contacto) — Estudio

## Tarjetas de repaso

P: ¿Qué es una transacción contactless respecto al EMV de contacto? / R: Una versión recortada y optimizada del EMV de contacto, condicionada por el breve tiempo que la tarjeta permanece en el campo del lector (ISO/IEC 14443).

P: ¿Cuáles son las dos consecuencias clave de la limitación temporal del campo? / R: La tarjeta ya no está presente cuando llega la respuesta del emisor (puede exigir un segundo tap) y el protocolo debe condensarse en menos comandos.

P: ¿Qué puede ser una "tarjeta" en contactless? / R: Cualquier objeto compatible con el enlace físico ISO/IEC 14443 (móvil, llavero, pulsera).

P: ¿Qué es un Kernel? / R: Cada implementación del protocolo de pago sobre ISO/IEC 14443; el lector elige una combinación de aplicación y Kernel, y activa el Kernel.

P: ¿Qué esquema corresponde a cada Kernel? / R: Kernel 1 (JCB, Visa como fallback de Kernel 3), Kernel 2 (MasterCard), Kernel 3 (Visa, preferida), Kernel 4 (American Express), Kernel 5 (JCB), Kernel 6 (Discover), Kernel 7 (UnionPay).

P: ¿Cuáles son los cinco pasos del Entry Point? / R: Pre-Processing, Protocol Activation, Combination Selection, Kernel Activation y Outcome Processing.

P: ¿A qué corresponden los Starts A–D del Entry Point? / R: Start A a Pre-Processing, Start B a Protocol Activation, Start C a Combination Selection y Start D a Kernel Activation.

P: ¿Qué archivo usa la Combination Selection y bajo qué nombre está en la tarjeta? / R: El PPSE (Proximity Payment System Environment), presente como `2PAY.SYS.DDF01`, que lista aplicaciones, identificadores de Kernel y prioridades.

P: ¿Cuáles son los siete Kernel Outcomes? / R: Select Next, Try Again, Approved, Declined, Online Request, Try Another Interface y End Application.

P: ¿A qué equivale cada outcome de resultado respecto al EMV de contacto? / R: Approved a un TC, Declined a un AAC y Online Request a un ARQC (del primer o segundo GENERATE AC).

P: ¿Qué es el modo Contactless Magstripe? / R: El terminal dialoga con la tarjeta según EMV Contactless pero codifica el resultado en formato de banda magnética (normalmente Track 2) con un valor de verificación dinámico (dynamic CVC) en lugar de un ARQC completo.

P: ¿Qué métodos de verificación del titular existen en contactless? / R: No CVM (con firma), Online PIN, Obtain Signature y, en dispositivos de consumo, Confirmation Code Verified; no hay PIN offline.

P: ¿Por qué no hay PIN offline en contactless? / R: Porque el titular no puede mantener la tarjeta en el campo mientras teclea el PIN.

P: ¿Cuándo es habitual el segundo tap? / R: Con móviles (que requieren PIN móvil o biometría entre el primer y el segundo tap) y a veces para procesar scripts del emisor.

P: ¿Qué distingue a Kernel 3 (Visa) de Kernels 1 y 2? / R: Kernel 3 sí admite segundo tap para scripts del emisor, usa el elemento propietario TTQ (tag 9F66) recibiendo el CTQ (tag 9F6C) y usa EXTERNAL AUTHENTICATE para la autenticación del emisor.

## Preguntas de autoevaluación

P: ¿Qué diferencia hay en quién inicia la transacción entre el EMV de contacto y el contactless? / R: En el EMV de contacto la inicia siempre el lector; en contactless puede iniciarla la propia tarjeta al entrar en el campo de polling (transporte, parkings, peajes). (El contexto del campo de polling)

P: ¿Qué dos modos de operación admite el estándar contactless? / R: EMV de grado completo (full-grade) y Contactless Magstripe, este último similar a un EMV parcial. (El contexto del campo de polling)

P: ¿Qué papeles cumplen el terminal y el reader dentro del sistema POS? / R: El lector dialoga con la tarjeta, muestra mensajes, pita y enciende LEDs hasta entregar un Final Outcome al terminal. (Conceptos principales)

P: ¿Para qué sirve el paso Pre-Processing y cuándo es necesario? / R: Está presente cuando el terminal inicia la transacción y es necesario en transacciones de valor variable para fijar el importe; si la inicia la tarjeta se llama "AutoRun" (Start B). (Entry Point 6.3)

P: ¿Qué significa el outcome Select Next y qué ocurre si se agotan las opciones? / R: Indica que la combinación Kernel-aplicación no sirve y se prueba otra de forma transparente al POS; si no hay más, devuelve End Application. (Kernel Outcomes 6.4)

P: ¿Por qué surgió el modo Contactless Magstripe? / R: Porque los datos capturados viajan por la infraestructura existente, no siempre apta para EMV full-grade, de modo que el resultado se empaqueta en banda magnética. (Contactless Magstripe 6.5)

P: ¿Cómo maneja Kernel 2 (MasterCard) las transacciones interrumpidas ("tearing")? / R: Con recuperación de tearing usando RECOVER AC para transacciones torn; en magstripe usa COMPUTE CRYPTOGRAPHIC CHECKSUM para obtener CVC3/dCVV. (Entendiendo los Kernels 6.7)

P: ¿Qué particularidad tiene Kernel 7 (UnionPay) con móviles? / R: Solo opera en modo EMV sin scripts del emisor; para móviles el GPO devuelve 6986 y el Kernel emite Try Again (reinicio a Start B). (Entendiendo los Kernels 6.7)

## Puntos a dominar

- La transacción contactless como EMV de contacto recortado y la restricción temporal del campo ISO/IEC 14443.
- La relación Kernel–esquema de tarjeta (tabla 6.1) y que el Entry Point elige una combinación AID + Kernel.
- Los cinco pasos del Entry Point, los Starts A–D y el uso del PPSE (`2PAY.SYS.DDF01`) en la Combination Selection.
- Los siete Outcomes y su correspondencia con TC, AAC y ARQC del EMV de contacto.
- El modo Contactless Magstripe y el dynamic CVC/dCVV embebido en el Track 2.
- Los métodos de verificación del titular (No CVM, Online PIN, Obtain Signature, Confirmation Code Verified) y la ausencia de PIN offline.
- Cuándo aplica el segundo tap (móviles y scripts del emisor).
- Las diferencias entre Kernels en modos, comandos propietarios, segundo tap, almacenamiento de datos y autenticación offline.
