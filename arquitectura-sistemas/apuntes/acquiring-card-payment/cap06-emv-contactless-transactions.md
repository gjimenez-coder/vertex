# Acquiring Card Payments — Ilya Dubinsky (CRC Press, Taylor & Francis, 2019)
## Capítulo 6 — EMV Contactless Transactions (Transacciones EMV sin contacto)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas usan la página del PDF.

## Lo que necesitas saber

El capítulo explica cómo el pago sin contacto (contactless) adapta el estándar EMV de contacto a la tecnología RFID/NFC definida por ISO/IEC 14443. La tesis central es que una transacción contactless es una versión recortada y optimizada de la transacción EMV de contacto, condicionada por el hecho de que la tarjeta (o dispositivo) permanece muy poco tiempo en el campo del lector.

Esa limitación temporal tiene dos consecuencias clave: la tarjeta ya no está presente cuando llega la respuesta del emisor (lo que a veces obliga a un segundo "tap") y el protocolo debe condensarse en menos comandos. Además, la "tarjeta" puede ser cualquier objeto compatible con el enlace físico ISO/IEC 14443 (móvil, llavero, pulsera).

EMV Contactless unifica bajo un mismo paraguas varias implementaciones previas de los esquemas, cada una en forma de un Kernel. Sales sabiendo cómo funciona el Entry Point (los cinco pasos, los Starts y los Outcomes), qué es el modo Contactless Magstripe, qué métodos de verificación del titular existen y las particularidades de los siete Kernels.

## El contexto del campo de polling

A diferencia del EMV de contacto, donde la transacción la inicia siempre el lector, una transacción contactless puede iniciarla la propia tarjeta al entrar en el campo de polling del lector (escenarios de transporte, parkings, peajes). La tarjeta se retira pronto, antes incluso de que llegue la respuesta del emisor. El estándar admite dos modos de operación: EMV de grado completo (full-grade) y contactless magstripe, este último similar a un EMV parcial.

## Conceptos principales (Main Concepts)

El Book A "Architecture and General Requirements" describe tarjeta, transacción y sistema POS. Una tarjeta es cualquier dispositivo compatible con ISO/IEC 14443. El sistema POS está compuesto por un terminal y un reader (lector): el lector dialoga con la tarjeta, muestra mensajes, pita y enciende LEDs, hasta entregar un Final Outcome al terminal.

Cada implementación del protocolo de pago sobre ISO/IEC 14443 se llama Kernel. El lector no elige solo una aplicación, sino una combinación de aplicación y Kernel, y activa el Kernel. Ese conjunto de funciones es el Entry Point functionality (Book B). Correspondencia Kernel-esquema (Entry Point Specification v2.6, tabla 6.1):

| Kernel | Esquema de tarjeta |
|---|---|
| Kernel 1 | JCB, Visa (caso especial, fallback de Kernel 3) |
| Kernel 2 | MasterCard |
| Kernel 3 | Visa (opción preferida) |
| Kernel 4 | American Express |
| Kernel 5 | JCB |
| Kernel 6 | Discover |
| Kernel 7 | UnionPay |

Los Outcomes son las instrucciones del Kernel al Entry Point. El Entry Point puede gestionarlos o reenviarlos al terminal como Final Outcome, y en ciertos casos generar él mismo un outcome final (normalmente cuando no encuentra una aplicación compatible).

## Entry Point (6.3)

El Entry Point ejecuta hasta cinco pasos: Pre-Processing, Protocol Activation, Combination Selection, Kernel Activation y Outcome Processing. Según las condiciones puede arrancar desde cualquiera de los cuatro primeros, mediante los Starts A, B, C y D.

- Pre-Processing (Start A): presente cuando el terminal inicia la transacción; necesario en transacciones de valor variable para fijar el importe. Si la inicia la tarjeta al entrar en el campo se llama "AutoRun" y usa Start B.
- Protocol Activation (Start B): el lector hace polling del campo, pide presentar la tarjeta, detecta colisiones y establece el enlace físico determinando el tipo (Type A o Type B). Equivale, a grandes rasgos, al reset y answer-to-reset (ATR) del chip. Puede volver aquí cuando se requiere un segundo tap de un móvil.
- Combination Selection (Start C): selecciona la combinación de AID y versión de Kernel. Usa selección indirecta de aplicación leyendo el archivo PPSE (Proximity Payment System Environment), presente en la tarjeta bajo el nombre `2PAY.SYS.DDF01`. El PPSE lista aplicaciones, identificadores de Kernel y prioridades; si no hay Kernel ID, se usa el nombre del ADF.
- Kernel Activation (Start D): el Entry Point cede el control de la comunicación al Kernel activado.
- Outcome Processing: procesa el Outcome; si es final, lo reenvía al terminal.

## Kernel Outcomes (6.4)

El estándar define siete outcomes, algunos emitibles también por el propio Entry Point:

- Select Next: la combinación Kernel-aplicación no sirve; se prueba otra de forma transparente al POS. Si no hay más, devuelve End Application.
- Try Again: el Kernel pide volver a presentar la tarjeta (p. ej. tras "tearing", retirada demasiado rápida, o para verificación adicional en móviles). Transparente al POS.
- Approved: transacción aprobada. Análogo a un TC del primer o segundo GENERATE AC del EMV de contacto.
- Declined: transacción rechazada. Análogo a un AAC del primer o segundo GENERATE AC.
- Online Request: se requiere petición online. Análogo a un ARQC. Con un parámetro, el Kernel puede pedir reinicio (segundo tap para autenticación del emisor y/o scripts del emisor).
- Try Another Interface: el Kernel o el Entry Point no pueden completar la transacción contactless pero hay otras interfaces (chip, magstripe).
- End Application: error irrecuperable o fin de procesamiento; puede indicar el siguiente Start (útil con móviles para autenticación en el dispositivo).

## Contactless Magstripe (6.5)

Como los datos capturados viajan por la infraestructura existente (no siempre apta para EMV full-grade), surge el modo Contactless Magstripe: el terminal dialoga con la tarjeta según EMV Contactless, pero codifica el resultado en formato de banda magnética, empaquetado normalmente en el Track 2 (a veces Track 1). Se genera un valor de verificación, a menudo llamado dynamic CVC, embebido en los datos discrecionales del Track 2, en lugar de un ARQC completo. Lo soportan MasterCard, American Express y uno de los Kernels de JCB.

## Métodos de verificación del titular (6.6)

El titular no puede mantener la tarjeta en el campo mientras teclea el PIN, así que no hay PIN offline en contactless. Con tarjeta física, el terminal puede renunciar a la verificación (No CVM) y pedir firma, o exigir PIN online (se pide, cifra y envía al emisor tras salir la tarjeta del campo). El Kernel indica la acción CVM al Entry Point mediante un valor: Online PIN, Obtain Signature, No CVM, o ninguno. En dispositivos de consumo puede indicar Confirmation Code Verified cuando el titular se ha verificado con código o biometría en el dispositivo.

## Entendiendo los Kernels (6.7)

Salvo el contactless magstripe, una transacción sin incidencias produce un criptograma (aprobado offline o ARQC). Cada Kernel resuelve a su modo la restricción de tiempo; muchos añaden campos y comandos propietarios (formalmente parte del estándar). El segundo tap es raro con plástico pero común con móviles (que requieren PIN móvil o biometría entre el primer y el segundo tap).

- Kernel 1 (Visa, JCB): decide offline/online según el Reader Contactless Floor Limit y omite CVM bajo el Reader CVM Required Limit. Exige un VLP Issuer Authorisation Code personalizado. Usa fDDA (fast DDA) con INTERNAL AUTHENTICATE; sin segundo GAC ni scripts del emisor.
- Kernel 2 (MasterCard): modos Magstripe y EMV; recuperación de "tearing" y almacenamiento de datos (SDS independiente o IDS integrado, no interoperables entre Kernels). En magstripe usa COMPUTE CRYPTOGRAPHIC CHECKSUM para obtener CVC3/dCVV. Usa RECOVER AC para transacciones torn. No soporta segundo GAC ni scripts del emisor.
- Kernel 3 (Visa, preferido): sí admite segundo tap para scripts del emisor; IDS similar al de Kernel 2 pero incompatible. Usa un único GET PROCESSING OPTIONS con el elemento propietario TTQ (tag 9F66) y recibe el CTQ (tag 9F6C). En modo IDS usa EXTENDED GPO (EGPO). Usa EXTERNAL AUTHENTICATE para los datos de autenticación del emisor.
- Kernel 4 (American Express): modos EMV y magstripe (AIP byte 2 bit 8). Modos Offline, Delayed y Partial Online (sin segundo GAC). Soporta Mobile CVM (devuelve Try Again). CDOL-Switch: distintos CDOL en EMV y magstripe. Solo SDA o CDA (sin INTERNAL AUTHENTICATE). En magstripe, un TC provoca rechazo; el criptograma se codifica en el Track 2.
- Kernel 5 (JCB): modos EMV, magstripe y Legacy (sin autenticación/autorización offline ni scripts). Dos modos de issuer update: segundo tap o mantener la tarjeta en el campo ("Present and Hold"). Solo CDA. Usa Issuer Update Parameter (tag 9F60), MDOL (tag 9F5C) y GET MAGSTRIPE DATA; recuperación de torn con comando ECHO.
- Kernel 6 (Discover): modos EMV, magstripe y Legacy Magstripe (distinguidos por AID). Un único GPO que trae el criptograma; segundo tap para scripts en modo EMV; Try Again para mobile CVM. Soporta Dynamic CVV (DCVV, tag 9F7E) colocado junto a dígitos del Unpredictable Number en Track 1 y 2.
- Kernel 7 (UnionPay): solo modo EMV, sin scripts del emisor. Único GPO para el criptograma; solo CDA en forma fDDA offline. Para móviles el GPO devuelve 6986 y el Kernel emite Try Again (reinicio a Start B).

## Ideas clave

- La transacción contactless es un EMV de contacto recortado, condicionado por el breve tiempo de la tarjeta en el campo del lector (ISO/IEC 14443).
- Cada esquema se implementa como un Kernel; el Entry Point elige una combinación de AID + Kernel, no solo una aplicación.
- El Entry Point ejecuta hasta cinco pasos con Starts A–D; la selección de combinación usa el PPSE (`2PAY.SYS.DDF01`).
- Los siete Outcomes (Select Next, Try Again, Approved, Declined, Online Request, Try Another Interface, End Application) guían al Entry Point y al terminal.
- El modo Contactless Magstripe empaqueta el resultado en banda magnética con un CVC/dCVV dinámico para infraestructuras antiguas.
- No hay PIN offline en contactless: solo No CVM, Online PIN, Obtain Signature o Confirmation Code Verified.
- El segundo tap es habitual con móviles (verificación en el dispositivo) y a veces necesario para procesar scripts del emisor.
- Los Kernels difieren en modos, comandos propietarios, soporte de segundo tap, almacenamiento de datos y método de autenticación offline.
