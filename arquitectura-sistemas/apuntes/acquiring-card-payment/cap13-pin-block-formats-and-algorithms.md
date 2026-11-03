# Acquiring Card Payments — Ilya Dubinsky (CRC Press / Taylor & Francis, 2019)
## Capítulo 13 — PIN Block Formats and Algorithms (Formatos y algoritmos de bloque de PIN)

> Nota de extracción: el texto se obtuvo de la capa de texto del PDF; las citas usan la página del PDF como `(PDF p. N)`.

## Lo que necesitas saber

El capítulo describe cómo se empaqueta y cifra un PIN en un *bloque de PIN* (PIN block). Los formatos de EPB (Encrypted PIN Block) están definidos en el estándar ISO 9564. Existen varios formatos, muchos de ellos muy parecidos entre sí: los formatos 0, 1, 2 y 3 describen el empaquetado de un valor de PIN en un bloque de 64 bits, mientras que el formato 4 describe un bloque de 128 bits.

La diferencia de cifrado es clave: los formatos 0 a 3 están pensados para algún tipo de cifrado DES, y el formato 4 se definió para usarse con el algoritmo de cifrado AES. En todos los casos los valores se almacenan como decimal codificado en binario (BCD) empaquetado.

Al terminar, sabrás distinguir cuándo se usa cada formato, cómo se construye cada bloque (qué vectores intervienen y cómo se rellenan y combinan), y por qué el formato 4 cambia la forma de combinar los vectores respecto a los anteriores.

## Estructura común de los bloques

Los bloques comparten características comunes: el primer nibble indica siempre el formato del bloque (0, 1, 2 o 3), y el segundo nibble indica la longitud del PIN, que puede variar de 4 a 14, aunque los PIN de más de 6 dígitos no se usan a menudo.

La estructura genérica de un EPB de los formatos 1 a 3 aparece en la figura 13.1: `F` denota el nibble indicador de formato, `L` denota la longitud del PIN y los valores `X` quedan definidos por el formato concreto del bloque.

## 13.1 Formatos de EPB (Encrypted PIN Block)

Format 0 se usa entre hosts cuando se dispone del PIN y del número PAN. El bloque se calcula haciendo XOR de dos vectores:
- Vector 1: se empaquetan como nibbles el indicador de formato, la longitud y el PIN, y se rellena con el valor 15 (`0xF`) hasta completar los 16 nibbles.
- Vector 2: se toman las 12 posiciones de la derecha del PAN sin el dígito de control y se rellenan por la izquierda con 4 ceros. En caso de tokenización EMV (ver sección 4.6.3) se usa el número de token en lugar del PAN.

Luego se hace XOR de los valores y el resultado se cifra.

Format 1 se usa cuando el PAN no está disponible por algún motivo. En ese caso se empaquetan formato, longitud y valor del PIN en el bloque, y el resultado se rellena hasta los 16 dígitos con un identificador único de transacción o un número aleatorio.

Format 2 se usa para comunicaciones locales y es solo offline; por ejemplo, en la validación offline del PIN por la tarjeta de circuito integrado. Es similar al vector 1 del formato 0: el indicador de formato (2), la longitud y el valor del PIN se rellenan hasta la longitud total del bloque con el valor 15 (`0xF`). Ver sección 5.3.10.5 para sus usos.

Format 3 también se usa para comunicaciones entre hosts. Es similar al formato 0, pero en lugar de un valor de relleno constante 15 (`0xF`) se usa una cadena de valores aleatorios en el rango de 10 a 15 (hex `0xA` a `0xF`) para rellenar el vector 1 hasta la longitud completa del bloque.

Format 4 es un formato de 128 bits definido para suplantar a los formatos 0 y 3 en comunicaciones entre hosts tras la transición al cifrado de PIN con AES. Los primeros 8 bytes del bloque se rellenan con `0xF` como en el formato 0, y los segundos 8 bytes se llenan con valores aleatorios como en el formato 3.

## Ejemplos que recorren el capítulo

El texto asume el PAN `9999990123456788`, el PIN `4321` y un número único de transacción `750923` (base 10).

- Format 0: Vector 1 = `04 43 21 FF FF FF FF FF`; Vector 2 (últimos 12 dígitos del PAN sin dígito de control, con relleno izquierdo de ceros) = `00 00 99 90 12 34 56 78`. Al hacer XOR se obtiene `04 43 B8 6F ED CB A9 87` (los dos primeros bytes no se modifican).
- Format 1: los primeros 6 nibbles son formato, longitud y PIN; se rellenan con 10 nibbles del número de secuencia único. El número de transacción en hexadecimal es `0xB754B`, por lo que el bloque es `14 43 21 00 00 0B 75 4B`.
- Format 2: similar al vector 1 del formato 0, con relleno `0xF`: `24 43 21 FF FF FF FF FF`.
- Format 3: Vector 1 = `34 43 21 AF CE DB BB AC` (relleno aleatorio `0xA` a `0xF`); Vector 2 = `00 00 99 90 12 34 56 78`. XOR = `34 43 B8 3F DC EF ED D4`.
- Format 4: Vector 1 = indicador (4) y longitud (4) rellenos con `0xF` en la primera mitad y valores aleatorios en la segunda: `44 43 21 FF FF FF FF FF DE AD BE EF DE AD BE EF`.

En el formato 4 el vector 2 lleva el PAN: como la longitud lo permite, el PAN se empaqueta completo salvo el dígito de control. El primer nibble del vector 2 indica cuántos dígitos tiene el PAN más allá de los primeros 12: es 0 para una tarjeta de 13 dígitos y 3 para un PAN de 16 dígitos (el más común). El vector 2 se rellena además con ceros.

La diferencia esencial del formato 4: a diferencia de los formatos 0 a 3, los valores no se combinan con un simple XOR. El vector 1 se cifra primero con AES, luego se hace XOR con el vector 2 y el resultado se cifra de nuevo; es decir, se aplica modo CBC con un vector de inicialización de ceros.

## Ideas clave

- Los formatos de EPB se definen en ISO 9564; los formatos 0-3 usan bloques de 64 bits (DES) y el formato 4 usa 128 bits (AES).
- El primer nibble indica el formato y el segundo la longitud del PIN (de 4 a 14; rara vez más de 6 dígitos).
- El formato 0 requiere PIN y PAN, y combina dos vectores mediante XOR antes de cifrar.
- El formato 1 se usa cuando no hay PAN, rellenando con un identificador de transacción o número aleatorio.
- El formato 2 es solo offline (p. ej., validación de PIN offline en la tarjeta) y rellena con `0xF`.
- El formato 3 es como el 0, pero rellena el vector 1 con valores aleatorios de `0xA` a `0xF`.
- El formato 4 reemplaza a los formatos 0 y 3 bajo AES: en el vector 2 el primer nibble indica los dígitos del PAN más allá de 12, y combina los vectores con doble cifrado AES en modo CBC con IV de ceros, no con un simple XOR.
- En tokenización EMV se usa el número de token en lugar del PAN.
