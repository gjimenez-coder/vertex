# Acquiring Card Payments — Ilya Dubinsky (CRC Press / Taylor & Francis, 2019)
## Capítulo 9 — Other Payment Methods (Otros métodos de pago)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas usan la página del PDF.

## Lo que necesitas saber

Más allá del efectivo físico y de los pagos "puros" con tarjeta tratados en el libro, han surgido con los años varios métodos de pago alternativos. Algunos funcionan como alternativa completa a las tarjetas, otros imitan la tecnología de tarjeta o la complementan. Las monedas criptográficas destacan como un método enteramente distinto, prácticamente denominado en una moneda propia.

El capítulo recorre, de forma breve, los grandes grupos en que pueden dividirse estos métodos: monederos electrónicos (staged o pass-through), métodos basados en efectivo, facturación por operador de telecomunicaciones (telco billing), transferencias bancarias, factura (invoice) y monedas digitales. Para cada grupo se explica su mecánica básica, el tipo de mercado donde prevalece y ejemplos concretos por región.

Sales sabiendo cómo encaja cada familia de métodos en el ecosistema de pagos, qué problemas resuelve (baja penetración de tarjetas, pagos online, financiación al consumidor) y qué tensiones regulatorias y fiscales plantea para los card schemes y los bancos.

## 9.1 Monederos electrónicos (Electronic Wallets)

Los monederos electrónicos o digitales imitan a un monedero físico (que se recarga con efectivo y puede contener tarjetas). Se dividen en dos subgrupos:

- **Staged wallet (monedero por etapas):** se usa en etapas, análogo a meter y sacar efectivo. La primera etapa es la recarga (top-up), que puede hacerse con una transacción de tarjeta, una transferencia bancaria, un depósito de efectivo en un kiosco o tienda adherida, o una transferencia peer-to-peer desde otro titular del mismo tipo de monedero. Se usan sobre todo para compras card-not-present, aunque las tiendas físicas los aceptan cada vez más.
- **Pass-through wallet (monedero de paso):** tiene una o varias tarjetas subyacentes; cada transacción se traduce en una transacción con una de esas tarjetas.

Desde la perspectiva de los card schemes, el staged wallet tiene inconvenientes regulatorios y fiscales. En lo regulatorio, ya no es posible rastrear cada transacción individual originada vía una tarjeta de marca de scheme: una vez recargado el dinero, puede usarse para cualquier fin permitido por el proveedor, incluidas transferencias ilegales y blanqueo. En lo fiscal, cada transacción que evita las redes de los schemes supone menores comisiones para el scheme y menos interchange para los bancos participantes. Por eso los schemes imponen comisiones adicionales y exigen datos extra sobre estas transacciones.

Los pass-through wallets llegaron al espacio card-present con Apple Pay. Allí, una o varias tarjetas se vinculan a la cuenta de la persona con Apple; aprovechando la tokenización de tarjeta, un consumidor con iPhone y NFC puede transmitir los datos de pago a un terminal contactless sin que el comercio deba actualizar hardware o software del terminal. Otros monederos como AliPay o WeChatPay se basan en el escaneo de un código QR para transferir fondos entre los monederos del consumidor y del comercio.

Ejemplos de staged wallets: WebMoney (Rusia), Osaifu-Keitai (Japón), Skrill y PayPal (globales). Ejemplos de pass-through wallets: Amazon Payments, PayPal, Apple Pay, Samsung Pay, AliPay (globales) y proveedores locales como BKM Express (Turquía). Los schemes también han incursionado con Visa Checkout y MasterPass. Los dos modos no son mutuamente excluyentes: PayPal puede recargarse como staged y usarse como pass-through según la preferencia del usuario.

## 9.2 Métodos basados en efectivo (Cash-based Methods)

Se usan para pagos online en mercados con baja penetración de tarjetas. El consumidor elige "cash voucher" como método de pago en una tienda de e-commerce y obtiene un documento imprimible con un identificador único. Luego lleva el documento a un punto de servicio adherido o a un kiosco automatizado y deposita efectivo por el importe total especificado. Una vez pagado el voucher en efectivo, la tienda online envía los bienes o presta los servicios.

Ejemplos en mercados en desarrollo: Efecty (Colombia), ESAPAY (Malasia y Brunéi) y Fawry (Egipto).

## 9.3 Facturación por operador (Telco Billing)

En muchos mercados con bajo acceso bancario y baja penetración de tarjetas, los consumidores usan ampliamente a las telecos como clientes post-pago o pre-pago. En consecuencia, muchas tiendas online y físicas permiten pagar desde el saldo del móvil o incluyendo el pago en la siguiente factura de telecomunicaciones.

El método es habitual en mercados en desarrollo donde la penetración del acceso móvil es muy superior al porcentaje de población bancarizada. Ejemplos: Flooz (Togo y Benín) y FNB Cell Pay Point (Sudáfrica).

## 9.4 Transferencias bancarias (Bank Transfers)

En mercados maduros con acceso bancario ubicuo (EE. UU., Reino Unido, Unión Europea) existen métodos que facilitan la transferencia de fondos entre las cuentas bancarias del consumidor y del comercio. El consumidor podría ir a una sucursal y ordenar la transferencia, pero ese enfoque no sirve para compras online; por eso han surgido numerosos métodos que simplifican la autorización de la transferencia en línea y aceleran el propio movimiento de fondos.

Ejemplos: ACH (EE. UU.), Faster Payments (Reino Unido), Sofort (Alemania), iDEAL (zona Bélgica/Países Bajos/Luxemburgo), eDankort (Dinamarca), SEPA Direct Debit (resto de la Unión Europea), eNETS (Singapur), entre otros.

## 9.5 Facturas (Invoices)

En ciertos mercados hay proveedores de servicios de pago que permiten pagar por factura. Con este método el comercio suele recibir el importe completo del pago, mientras que al consumidor se le factura periódicamente a lo largo de varios meses. El método traslada los riesgos de iliquidez del comercio al proveedor de servicios y, a la vez, ofrece financiación al consumidor en forma de pagos a plazos sobre lo que originalmente era un pago único.

## 9.6 Monedas digitales (Digital Currencies)

Las monedas digitales, en especial la pionera Bitcoin, son una familia enteramente nueva de método de pago, no relacionada con ninguna moneda o tecnología existente. En una moneda digital basada en blockchain no hay una autoridad única que emita o controle el instrumento de pago: ese rol se distribuye entre múltiples nodos en una red de baja confianza de "coin miners".

La conversión entre moneda digital y tradicional no forma parte de los mecanismos de la moneda digital (a diferencia de los monederos electrónicos); se realiza de forma similar a un cambio de divisas, mediante un broker de moneda digital. Como estas monedas se construyen de manera inherentemente anónima e imposible de rastrear, aceptar o adquirir pagos con ellas conlleva un riesgo legal significativo, al ser un canal cómodo para actividades ilegales y blanqueo; además, el marco legal de la mayoría de países no está preparado para este tipo de instrumento financiero. Estos factores contribuyen a la volatilidad de las monedas digitales. Pese a ello, los consumidores están cada vez más dispuestos a usarlas y los comercios, a su vez, esperan poder aceptarlas.

## Ideas clave

- Los métodos de pago alternativos se agrupan en: monederos electrónicos, basados en efectivo, telco billing, transferencias bancarias, factura y monedas digitales.
- Un staged wallet se recarga por etapas y luego se gasta; un pass-through wallet traduce cada operación a una transacción con una tarjeta subyacente.
- Los staged wallets preocupan a los card schemes por la pérdida de trazabilidad (riesgo de blanqueo) y por la reducción de comisiones e interchange; de ahí los cargos y datos extra que imponen.
- Apple Pay llevó el pass-through al mundo card-present vía tokenización y NFC; AliPay y WeChatPay usan códigos QR.
- Los métodos basados en efectivo y el telco billing prosperan en mercados con baja penetración de tarjetas y alta penetración móvil.
- Las transferencias bancarias (ACH, Faster Payments, Sofort, iDEAL, SEPA Direct Debit, eNETS) dominan en mercados maduros y resuelven el pago online entre cuentas.
- El pago por factura traslada el riesgo de iliquidez del comercio al proveedor y financia al consumidor a plazos.
- Las monedas digitales como Bitcoin carecen de autoridad central, su conversión la hacen brokers externos, y su anonimato acarrea riesgo legal y volatilidad pese a la creciente demanda.
