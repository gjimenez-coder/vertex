# Code Tables (Tablas de códigos) — Estudio

## Tarjetas de repaso

P: ¿Qué codificaciones usan las pistas de banda magnética y con cuántos bits? / R: El formato ANSI/ISO ALPHA para Track 1 (vectores de 7 bits) y el formato BCD para Tracks 2 y 3 (vectores de 5 bits); en ambos el bit menos significativo es la paridad.

P: ¿Cómo se almacena el carácter ' ' en ALPHA y el dígito 0 en BCD? / R: El espacio se almacena como 0000001 en ALPHA y el dígito 0 como 00001 en BCD.

P: ¿Qué es ASCII y de cuántos bits es en su tabla original? / R: American Standard Code for Information Interchange, una tabla de codificación de caracteres de 7 bits publicada en 1963.

P: ¿Qué atajo aritmético convierte un dígito decimal a su código ASCII? / R: Sumarle 0x30, ya que los dígitos van de 0x30 (48) a 0x39 (57); por ejemplo "3790" se codifica como 33 37 39 30.

P: ¿Cómo se convierte entre mayúsculas y minúsculas en ASCII? / R: Activando o desactivando el 6º bit (sumar/restar 0x20): mayúsculas en 0x41–0x5A y minúsculas en 0x61–0x7A.

P: ¿Qué es EBCDIC y quién lo desarrolló? / R: Extended Binary Coded Decimal Interchange Code, una codificación propietaria de 8 bits desarrollada por IBM para mainframes, anunciada en 1963.

P: ¿Cómo se codifican los dígitos decimales en EBCDIC? / R: Van de 0xF0 (240) a 0xF9 (249), así que basta sumar 0xF0 a un dígito; por ejemplo 3790 se codifica como F3 F7 F9 F0.

P: ¿Cuántos caracteres de espacio tiene EBCDIC y cuáles son? / R: Tres: 0x40 (espacio, equivale al 0x20 de ASCII), 0x41 (espacio requerido/no-break) y 0xE1 (espacio numérico).

P: ¿Por qué perdura EBCDIC en el mundo de los pagos? / R: Por la popularidad de los mainframes IBM en instituciones financieras; otro legado de las tarjetas perforadas son los ficheros de 80 bytes.

P: ¿Cuáles son los pasos para codificar en Base64? / R: Rellenar la secuencia binaria con octetos 0x00 hasta que su longitud sea divisible por 3, convertirla en valores de 6 bits y mapear cada valor a un carácter, sustituyendo los ceros de relleno finales por '='.

P: ¿Por qué el valor binario 0 puede codificarse distinto en Base64? / R: Porque un cero de datos originales se mapea a 'A', mientras que un byte de relleno final se codifica como '='.

P: ¿Qué significa BER-TLV y dónde se usa? / R: Basic Encoding Rules — Tag Length Value, la codificación BER de ASN.1, usada en pagos como parte de la tecnología chip y contactless EMV.

P: ¿Cómo se estructura un elemento BER-TLV? / R: Como identificador de tipo (tag), seguido de la longitud del elemento, seguido de los datos (valor), y opcionalmente un marcador de fin de contenido no usado en pagos.

P: ¿Qué tamaño y clases de tag usa EMV? / R: Tags de 1 o 2 bytes, con clase 1 (aplicación específica) o 2 (dependiente del contexto), de modo que empiezan por los bits 01 o 10.

P: ¿Qué formas de longitud existen en TLV y sus límites? / R: Forma corta (bit más significativo a 0, hasta 127 bytes en 1 byte) y forma larga (bit a 1 indicando la "longitud de la longitud"); EMV se limita a 255 bytes, que en forma larga ocupan 2 bytes.

## Preguntas de autoevaluación

P: ¿Qué papel cumple el bit menos significativo en los formatos ALPHA y BCD de las pistas magnéticas? / R: Es el bit de paridad en ambos formatos. (Sección "ANSI/ISO ALPHA y BCD")

P: Si quieres interpretar bytes crudos y ves 33 37 39 30, ¿qué representa y cómo lo deduces? / R: Representa "3790" en ASCII, porque a cada dígito decimal se le suma 0x30 (dígitos en 0x30–0x39). (Sección "ASCII")

P: ¿En qué se diferencian ASCII y EBCDIC en cuanto a ancho de bits y compatibilidad interna? / R: ASCII es de 7 bits (ampliable a 8); EBCDIC usa códigos completos de 8 bits y tiene múltiples páginas de código que no son totalmente compatibles entre sí. (Secciones "ASCII" y "EBCDIC")

P: ¿Por qué la secuencia de 5 octetos DE AD BE EF 00 produce 8 caracteres en Base64? / R: Se rellena a 6 octetos para que la longitud sea divisible por tres, lo que da 48 bits; a razón de una palabra de 6 bits por carácter resultan 8 caracteres (3q2+7wA=). (Sección "Base64")

P: En EMV, ¿cómo se sabe si un tag ocupa un segundo byte? / R: Cuando el número de tag no cabe en 5 bits, los 5 bits menos significativos del primer byte se ponen a 1 (número 31) y el número continúa en el segundo byte; EMV no supera los 2 bytes. (Sección "BER-TLV / Tag")

P: ¿Qué indica el bit P/C de un tag y qué valores de clase utiliza EMV? / R: El bit P/C distingue elementos primitivos (contienen el valor real) de constructed (compuestos de sub-elementos TLV, P/C = 1); EMV usa solo las clases 1 y 2. (Sección "BER-TLV / Tag")

P: ¿Cómo se codifica una longitud de 140 bytes en TLV y por qué no cabe en forma corta? / R: La forma corta solo llega a 127 bytes (bit más significativo a 0), así que 140 usa forma larga en 2 bytes: el primero indica forma larga y que sigue 1 byte, y el segundo contiene la longitud completa. (Sección "BER-TLV / Longitud")

P: ¿Cuál es el propósito general de este capítulo dentro del libro? / R: Es un apéndice de referencia que cataloga las tablas y esquemas de codificación de caracteres y datos usados a lo largo del libro, para interpretar pistas magnéticas, mensajes ISO y datos de chip EMV. (Sección "Lo que necesitas saber")

## Puntos a dominar

- Distinguir ALPHA (7 bits, Track 1) de BCD (5 bits, Tracks 2 y 3) y recordar que la paridad va en el bit menos significativo.
- Aplicar los atajos aritméticos: sumar 0x30 para dígitos ASCII, sumar 0xF0 para dígitos EBCDIC y alternar el 6º bit (0x20) para mayúsculas/minúsculas en ASCII.
- Reconocer los rangos de control, espacio y letras en ASCII y EBCDIC, incluyendo los tres espacios de EBCDIC.
- Explicar el relleno a múltiplo de 3 octetos en Base64 y diferenciar el cero de datos ('A') del byte de relleno ('=').
- Descomponer un elemento BER-TLV en tag, longitud y valor, y reconocer las clases y tamaños de tag que usa EMV (1 o 2 bytes, clases 1 y 2, bit P/C).
- Codificar y leer longitudes TLV en forma corta (hasta 127) y larga (EMV hasta 255 bytes, 2 bytes).
