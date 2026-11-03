# PIN Block Formats and Algorithms (Formatos y algoritmos de bloque de PIN) — Estudio

## Tarjetas de repaso

P: ¿En qué estándar se definen los formatos de EPB (Encrypted PIN Block)? / R: En el estándar ISO 9564.

P: ¿Qué tamaño de bloque usan los formatos 0, 1, 2 y 3, y para qué cifrado están pensados? / R: Bloques de 64 bits, pensados para algún tipo de cifrado DES.

P: ¿Qué tamaño de bloque usa el formato 4 y con qué algoritmo de cifrado se definió? / R: Un bloque de 128 bits, definido para usarse con el algoritmo AES.

P: ¿Qué indican el primer y el segundo nibble de un bloque de PIN? / R: El primer nibble indica el formato (0, 1, 2 o 3) y el segundo la longitud del PIN.

P: ¿Qué rango de longitud puede tener el PIN y cuál es lo habitual? / R: De 4 a 14 dígitos, aunque los PIN de más de 6 dígitos no se usan a menudo.

P: ¿Cómo se almacenan los valores en todos los formatos? / R: Como decimal codificado en binario (BCD) empaquetado.

P: ¿Qué requiere el formato 0 y cómo combina sus vectores? / R: Requiere PIN y PAN; combina dos vectores mediante XOR y luego cifra el resultado.

P: ¿Cómo se construye el vector 2 del formato 0? / R: Con las 12 posiciones de la derecha del PAN sin el dígito de control, rellenadas por la izquierda con 4 ceros.

P: ¿Cuándo se usa el formato 1 y con qué se rellena? / R: Cuando el PAN no está disponible; se rellena con un identificador único de transacción o un número aleatorio.

P: ¿Qué caracteriza al formato 2? / R: Es solo offline (p. ej., validación offline del PIN en la tarjeta de circuito integrado) y rellena con el valor 15 (`0xF`).

P: ¿En qué se diferencia el formato 3 del formato 0? / R: En lugar de relleno constante `0xF`, rellena el vector 1 con valores aleatorios en el rango `0xA` a `0xF`.

P: ¿Cómo se rellenan las dos mitades del bloque en el formato 4? / R: Los primeros 8 bytes con `0xF` (como el formato 0) y los segundos 8 bytes con valores aleatorios (como el formato 3).

P: ¿Qué indica el primer nibble del vector 2 en el formato 4? / R: Cuántos dígitos tiene el PAN más allá de los primeros 12 (0 para 13 dígitos, 3 para 16 dígitos).

P: ¿Cómo combina el formato 4 sus vectores, a diferencia de los formatos 0 a 3? / R: No usa un simple XOR: cifra el vector 1 con AES, hace XOR con el vector 2 y cifra de nuevo (modo CBC con IV de ceros).

P: En caso de tokenización EMV, ¿qué se usa en lugar del PAN? / R: El número de token.

## Preguntas de autoevaluación

P: ¿Cuál es la diferencia de cifrado fundamental entre los formatos 0-3 y el formato 4? / R: Los formatos 0 a 3 están pensados para cifrado DES (bloques de 64 bits) y el formato 4 se definió para AES (bloque de 128 bits). (Sección "Lo que necesitas saber" / 13.1)

P: ¿Por qué el formato 1 no incluye el PAN en su construcción? / R: Porque se usa precisamente cuando el PAN no está disponible por algún motivo; en su lugar rellena con un identificador único de transacción o un número aleatorio. (Sección 13.1)

P: ¿Qué formato elegirías para la validación offline del PIN en la tarjeta de circuito integrado y por qué? / R: El formato 2, porque se usa para comunicaciones locales y es solo offline, rellenando con `0xF`. (Sección 13.1)

P: Con PIN `4321`, ¿cómo queda el vector 1 del formato 0 y por qué? / R: `04 43 21 FF FF FF FF FF`: el nibble de formato (0), la longitud (4) y el PIN empaquetados, rellenados con `0xF` hasta 16 nibbles. (Sección "Ejemplos que recorren el capítulo")

P: Para el PAN `9999990123456788`, ¿cómo se obtiene el vector 2 del formato 0? / R: Se toman los últimos 12 dígitos sin el dígito de control y se rellena por la izquierda con ceros, dando `00 00 99 90 12 34 56 78`. (Sección "Ejemplos que recorren el capítulo")

P: ¿Qué hace que el formato 4 no pueda combinar sus vectores con un simple XOR como los demás? / R: Aplica doble cifrado AES en modo CBC con IV de ceros: cifra el vector 1, hace XOR con el vector 2 y cifra el resultado de nuevo. (Sección "Ejemplos que recorren el capítulo" / Ideas clave)

P: ¿A qué formatos reemplaza el formato 4 y en qué contexto? / R: A los formatos 0 y 3 en comunicaciones entre hosts, tras la transición al cifrado de PIN con AES. (Sección 13.1)

## Puntos a dominar

- Distinguir cuándo se usa cada formato (0: PIN+PAN entre hosts; 1: sin PAN; 2: offline local; 3: entre hosts con relleno aleatorio; 4: AES entre hosts).
- Identificar el significado del primer y segundo nibble de un bloque y el rango de longitud del PIN (4 a 14).
- Reconocer que todos los valores se almacenan en BCD empaquetado.
- Construir el vector 1 y el vector 2 del formato 0 a partir de un PIN y un PAN dados.
- Explicar el relleno de cada formato: `0xF` (formatos 0 y 2), identificador/aleatorio (formato 1), aleatorio `0xA`-`0xF` (formato 3), mitad `0xF` + mitad aleatoria (formato 4).
- Explicar la combinación de vectores con XOR en los formatos 0-3 frente al doble cifrado AES en modo CBC (IV de ceros) del formato 4.
- Recordar el uso del número de token en lugar del PAN bajo tokenización EMV.
