# Acquiring Card Payments — Ilya Dubinsky (CRC Press, Taylor & Francis, 2019)

Autor: Ilya Dubinsky.

Libro centrado en el lado adquirente (acquiring) del procesamiento de pagos con tarjeta. Nace de la ausencia de material formativo adecuado para ingenieros de sistemas de pago: recorre el panorama de la industria, el flujo de una transacción y sus fundamentos técnicos, los servicios y protocolos (ISO 8583), el entorno card-not-present, las transacciones EMV de contacto y contactless, las disputas y el compliance, los estándares de seguridad PCI y otros métodos de pago. Incluye apéndices de referencia sobre algoritmos de validación, tablas de códigos, criptografía y formatos de bloque de PIN. Es complementario a los estándares y manuales de las card schemes, no un sustituto.

## Capítulos

- [Capítulo 0 — Prólogo (Preface)](cap00-preface.md): justifica la obra ante la falta de material formativo para ingenieros de pagos y acota su alcance al lado adquirente.
- [Capítulo 1 — Overview of Card Payments Industry](cap01-overview-of-card-payments-industry.md): historia y ecosistema de los pagos con tarjeta, con sus actores y los modelos three-party y four-party.
- [Capítulo 2 — Payment Flow and Basics of Technology](cap02-payment-flow-and-basics-of-technology.md): fundamentos técnicos de la tarjeta y del flujo de transacción sobre la pila de estándares ISO/IEC y EMV.
- [Capítulo 3 — Payment Services and Protocols](cap03-payment-services-and-protocols.md): fases de autorización, clearing, settlement y disputa, con SMS/DMS y dialectos de ISO 8583.
- [Capítulo 4 — Card-Not-Present Environment](cap04-card-not-present-environment.md): seguridad por capas del entorno CNP: cifrado de canal, 3D Secure/EMV 3DS, AVS y tokenización.
- [Capítulo 5 — Contact Chip Transactions](cap05-contact-chip-transactions.md): funcionamiento de una transacción EMV con chip de contacto, de la selección de aplicación a la finalización.
- [Capítulo 6 — EMV Contactless Transactions](cap06-emv-contactless-transactions.md): adaptación recortada de EMV a RFID/NFC (ISO/IEC 14443) con Kernels, Entry Point y Outcomes.
- [Capítulo 7 — Disputes, Arbitration and Compliance](cap07-disputes-arbitration-and-compliance.md): certificación, gestión de disputas/arbitraje, liability shifts y compliance entre miembros del scheme.
- [Capítulo 8 — Data Security Standards in the Payment Card Industry](cap08-data-security-standards-in-the-payment-card-industry.md): marco del PCI SSC (PCI DSS, PA DSS, PTS), datos CHD/SAD, HSM y gestión de claves.
- [Capítulo 9 — Other Payment Methods](cap09-other-payment-methods.md): métodos alternativos: monederos, basados en efectivo, telco billing, transferencias bancarias, factura y monedas digitales.
- [Capítulo 10 — Validation Algorithms](cap10-validation-algorithms.md): algoritmos de validación no criptográficos: Luhn, LRC y KCV.
- [Capítulo 11 — Code Tables](cap11-code-tables.md): apéndice de referencia con formatos de codificación de caracteres y datos (ALPHA, BCD, ASCII, EBCDIC, Base64, BER-TLV).
- [Capítulo 12 — Cryptography 101](cap12-cryptography-101.md): introducción a los términos criptográficos relevantes para el procesamiento de pagos.
- [Capítulo 13 — PIN Block Formats and Algorithms](cap13-pin-block-formats-and-algorithms.md): empaquetado y cifrado del PIN en bloques EPB según ISO 9564 (formatos 0-4).
