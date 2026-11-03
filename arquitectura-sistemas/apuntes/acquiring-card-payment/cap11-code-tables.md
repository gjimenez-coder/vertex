# Acquiring Card Payments — Ilya Dubinsky (CRC Press / Taylor & Francis, 2019)
## Capítulo 11 — Code Tables (Tablas de códigos)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas usan la página del PDF.

## Lo que necesitas saber

Este capítulo es un apéndice de referencia que reúne las tablas y esquemas de codificación que aparecen a lo largo del libro al tratar con mensajes y datos de pago. No desarrolla una tesis: cataloga formatos de codificación de caracteres y de datos con sus propiedades y rangos de valores, para poder interpretar bytes crudos de pistas magnéticas, mensajes ISO y datos de chip EMV.

Cubre seis bloques: los formatos ANSI/ISO ALPHA y BCD de las pistas de banda magnética, las tablas de caracteres ASCII y EBCDIC, la codificación Base64 y, por último, la codificación BER-TLV usada en EMV. Para varias tablas (ASCII, EBCDIC, Base64) el autor no las reproduce completas porque son fáciles de encontrar; en su lugar explica sus propiedades clave y los trucos prácticos de interpretación.

Sales sabiendo cómo se almacenan los dígitos y caracteres en cada esquema, qué atajos aritméticos permiten convertir entre representaciones (sumar 0x30 en ASCII, 0xF0 en EBCDIC, alternar el 6º bit para mayúsculas/minúsculas) y cómo se descompone un elemento TLV en tag, longitud y valor dentro de EMV.

## ANSI/ISO ALPHA y BCD (pistas magnéticas)

- Formato ALPHA: codifica los valores de la Track 1. Los datos se almacenan en vectores de 7 bits, siendo el bit menos significativo la paridad (el carácter ' ' se almacena como 0000001).
- Formato BCD: codifica los valores de Track 2 y Track 3. Los datos se almacenan en vectores de 5 bits, siendo el bit menos significativo la paridad (el dígito 0 se almacena como 00001).

## ASCII

ASCII (American Standard Code for Information Interchange, o US-ASCII) es una tabla de codificación de caracteres de 7 bits. Su origen se remonta a un código de 5 bits inventado por Emile Baudot en 1870, primer código binario de ancho fijo legible por máquina, que evolucionó al ITA2 de 6 bits (con códigos de cambio de registro). La tabla ASCII se publicó en 1963 y eliminó la necesidad de caracteres de control de cambio de registro.

Propiedades clave:

- Los caracteres de control ocupan el rango 0x00 a 0x1F (0 a 31); 0x7F también es de control.
- Los dígitos van de 0x30 (48) a 0x39 (57): para formar el código ASCII de un dígito decimal basta sumarle 0x30. Ej.: "3790" se codifica como `33 37 39 30`.
- El espacio es 0x20 (32).
- Las mayúsculas van de 0x41 a 0x5A y las minúsculas de 0x61 a 0x7A, ambas en orden alfabético. Activar o desactivar el 6º bit (sumar/restar 0x20) convierte entre mayúsculas y minúsculas.

En revisiones posteriores ASCII se amplió a 8 bits (0x80–0xFF para caracteres nacionales), páginas de código hoy sustituidas en gran medida por UTF-8. En pagos, la mayoría de aplicaciones y todos los protocolos de autorización online usan solo el rango bajo de ASCII; las codificaciones nacionales a veces aparecen en ficheros de clearing. La tabla de 7 bits no se reproduce por ser fácil de encontrar.

## EBCDIC

EBCDIC (Extended Binary Coded Decimal Interchange Code) es una codificación propietaria de 8 bits desarrollada por IBM para mainframes y minicomputadoras, anunciada en 1963 (el mismo año que ASCII). Como IBM consideró inviable migrar todo el software y periféricos existentes al nuevo estándar de 7 bits, EBCDIC se mantuvo como extensión incremental de las codificaciones BCDIC previas de las tarjetas perforadas. Por la popularidad de los mainframes IBM en instituciones financieras, la codificación ha perdurado.

Propiedades notables:

- Usa códigos completos de 8 bits (frente a los 7 de ASCII).
- Existen múltiples páginas de código EBCDIC que no son totalmente compatibles.
- Los caracteres de control ocupan 0x00 a 0x3F; 0xFF también es de control.
- Hay tres caracteres de espacio: 0x40 (64, espacio), 0x41 (65, espacio requerido/no-break) y 0xE1 (225, espacio numérico). El 0x40 corresponde al 0x20 de ASCII.
- Los dígitos decimales van de 0xF0 (240) a 0xF9 (249): basta sumar 0xF0 a un dígito. Ej.: 3790 se codifica como `F3 F7 F9 F0`.
- Las mayúsculas latinas van en 0xC1–0xC9 (A a I), 0xD1–0xD9 (J a R) y 0xE2–0xE9 (S a Z); las minúsculas en los rangos paralelos 0x80–0x89, 0x90–0x99 y 0xA1–0xA9.

La tabla completa y los conversores no se reproducen por ser fáciles de encontrar.

## Base64

Base64 representa datos binarios usando 64 caracteres alfanuméricos y especiales. Pasos de conversión:

1. Se rellena la secuencia binaria original con octetos cero (0x00) hasta que su longitud total sea divisible por 3.
2. La secuencia se convierte en una cadena de valores de 6 bits.
3. Cada valor de 6 bits se mapea a un carácter según la tabla, salvo los ceros de relleno finales, que se sustituyen por el carácter de padding `=`.

Ejemplo: la secuencia de 5 octetos `DE AD BE EF 00` se rellena a 6 octetos (para que la longitud sea divisible por tres), lo que da 48 bits y, por tanto, 8 caracteres (uno por palabra de 6 bits). El resultado codificado es `3q2+7wA=`. Nótese que el mismo valor binario 0 se codifica distinto según sea dato original (se mapea a `A`) o byte de relleno (se mapea a `=`).

## BER-TLV

BER-TLV significa Basic Encoding Rules — Tag Length Value, y se refiere a la codificación BER de ASN.1. ASN.1 (Abstract Syntax Notation One) es un estándar que describe un lenguaje para la descripción abstracta de estructuras de datos arbitrarias y varios conjuntos de reglas de codificación. BER es uno de esos conjuntos y se usa en pagos como parte de la tecnología chip y contactless EMV. Cada elemento se codifica como identificador de tipo, seguido de la longitud del elemento, seguido de los datos, y opcionalmente un marcador de fin de contenido (no usado en pagos, por lo que no se cubre).

### Tag o identificador de tipo

Una estructura BER siempre empieza por el tag, que ocupa al menos 1 byte y es potencialmente ilimitado; en EMV los tags son de 1 o 2 bytes. Si el número de tag no cabe en 5 bits, los 5 bits menos significativos del primer byte se ponen a 1 y se forma un tag de 2 bytes. En el segundo byte, el bit más significativo (M) se pone a 1 si sigue otro octeto de número de tag (tag de al menos 3 bytes); en EMV ningún tag supera los 2 bytes.

Valores de clase del tag (tabla 11.3):

| Valor | Descripción |
|-------|-------------|
| 0 | Universal — nativo de ASN.1 |
| 1 | Válido para una aplicación específica |
| 2 | Tag dependiente del contexto |
| 3 | Definido en especificaciones privadas |

EMV solo utiliza los valores 1 y 2, por lo que todos sus tags estándar empiezan por la secuencia de bits `01` o `10`. El bit P/C indica si el elemento es primitivo (contiene el valor real) o constructed (compuesto de sub-elementos TLV); vale 1 para los constructed, y EMV usa ambos. El resto del tag es el número de tag: para un tag de un byte va de 0 a 30; si esos bits están todos a uno (número 31), el número continúa en el segundo byte.

### Longitud

La longitud se codifica en forma corta o larga:

- Forma corta: longitud en un solo byte con el bit más significativo a 0; permite valores de hasta 127 bytes. Ej.: 75 bytes se representa como `01001011`.
- Forma larga: el bit más a la izquierda del primer byte se pone a 1 y los otros 7 bits indican la "longitud de la longitud" (número de bytes que siguen y contienen la longitud real). EMV solo usa longitudes de hasta 255 bytes, por lo que la forma larga requiere 2 bytes en total. Ej.: el valor 140 (binario `10001100`) se codifica en dos bytes: el byte 1 indica forma larga y que sigue 1 byte, y el byte 2 contiene la longitud completa.

## Ideas clave

- Las pistas magnéticas usan ANSI/ISO ALPHA (7 bits, Track 1) y BCD (5 bits, Tracks 2 y 3), ambas con paridad en el bit menos significativo.
- ASCII es de 7 bits (1963): dígitos en 0x30–0x39 (sumar 0x30), espacio 0x20, y el 6º bit alterna mayúsculas/minúsculas.
- EBCDIC es la codificación propietaria de 8 bits de IBM, con varias páginas de código incompatibles; dígitos en 0xF0–0xF9 (sumar 0xF0) y tres caracteres de espacio.
- EBCDIC perdura en pagos por los mainframes IBM; otro legado de las tarjetas perforadas son los formatos de fichero de 80 bytes.
- Base64 agrupa en palabras de 6 bits tras rellenar a múltiplo de 3 octetos; el cero de relleno final se codifica como `=`, distinto del cero de datos (`A`).
- BER-TLV codifica cada elemento como tag, longitud y valor, y se usa en EMV chip/contactless.
- En EMV los tags son de 1 o 2 bytes, con clase 1 o 2 (prefijo de bits `01`/`10`) y un bit P/C que distingue elementos primitivos de constructed.
- La longitud TLV tiene forma corta (hasta 127 bytes, 1 byte) o larga; EMV se limita a longitudes de hasta 255 bytes (2 bytes en forma larga).
