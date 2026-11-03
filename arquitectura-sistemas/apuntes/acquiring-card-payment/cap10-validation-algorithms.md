# Acquiring Card Payments — Ilya Dubinsky (CRC Press / Taylor & Francis, 2019)
## Capítulo 10 — Validation Algorithms (Algoritmos de validación)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF y las citas usan la página del PDF `(PDF p. N)`.

## Lo que necesitas saber

El capítulo recopila tres algoritmos de validación de uso común en el mundo de los pagos con tarjeta: el algoritmo de Luhn, el Longitudinal Redundancy Check (LRC) y el Key Check Value (KCV). No son mecanismos criptográficos de seguridad, sino comprobaciones diseñadas para detectar errores de captura, de transmisión o de manipulación de claves.

La tesis implícita es que cada algoritmo resuelve un problema distinto: Luhn protege el número de cuenta (PAN) frente a errores humanos de tecleo; el LRC protege los datos de la banda magnética frente a errores de ruido en el soporte; y el KCV confirma la validez de una clave de cifrado sin exponerla. Al terminar sabrás cómo se calcula y se valida cada uno, con sus respectivos ejemplos numéricos.

## 10.1 Luhn Algorithm (Algoritmo de Luhn)

Está especificado por el estándar ISO/IEC 7812-1. La validación de un número de cuenta sigue estos pasos:

1. Separar (truncar) el dígito de control del número a validar.
2. De derecha a izquierda, duplicar todos los dígitos en posiciones impares (el más a la derecha y uno de cada dos hacia la izquierda).
3. Si el producto de duplicar un dígito es mayor que 9, se reemplaza por la suma de sus dígitos.
4. Sumar el resultado y añadir el dígito de control.
5. El resultado, módulo 10, debe ser 0.

El ejemplo del número de cuenta 491023693576 (figura 10.1) produce una suma de todos los dígitos de 8 + 9 + 2 + 0 + 4 + 3 + 3 + 9 + 6 + 5 + 5 + 6 = 60, que es divisible por 10; por tanto, 6 es un dígito de control válido.

Para calcular el dígito de control se siguen los pasos 1 a 4 asumiendo un dígito de control de 0. Si el total ya es divisible por 10, entonces el dígito de control es 0 y se termina. En caso contrario, se reemplaza el dígito de control por 10 menos la suma módulo 10.

Un error en cualquier dígito del número de cuenta invalida la suma de comprobación de Luhn. También detecta casi cualquier transposición de dos dígitos adyacentes, con la excepción de 09 convirtiéndose en 90 o viceversa. Esto hace de Luhn un método fácil y práctico para validar PAN en pedidos por correo o teléfono y en comercio electrónico, es decir, cuando la tarjeta es tecleada o escrita por una persona y resulta más propensa a este tipo de errores.

## 10.2 Longitudinal Redundancy Check (LRC)

El LRC se usa como valor final de los datos almacenados en la banda magnética. Es un tipo de algoritmo de comprobación de redundancia fácil de implementar en hardware binario y especialmente bueno para detectar errores relacionados con el ruido.

Se define como el valor de complemento a dos de 8 bits de la suma de todos los bytes módulo 2⁸, de modo que la suma de todos los valores más el LRC da 0.

El cálculo se realiza así: aplicar XOR a todos los bytes del array, calcular el complemento a dos invirtiendo el resultado (XOR con 0xFF), sumar uno y volver a tomar módulo 2⁸ (lo que equivale a aplicar un AND con 0xFF).

Ejemplo con FA 13 58 A0 C5:

- XOR de 0xFA, 0x13, 0x58, 0xA0 y 0xC5 → 0x8C.
- Complemento a dos: XOR con 0xFF → 0x73.
- Sumar 1 → 0x74, que es el valor LRC buscado.

Para validar, se suma el conjunto de valores con el LRC calculado: el resultado es 0x100, que al aplicarle AND con 0xFF da 0.

## 10.3 Key Check Value (KCV)

El KCV sirve para confirmar la validez de una clave y se utiliza para validar claves de cifrado en la industria de pagos.

Es típicamente un valor de control de 3 bytes (6 dígitos) que se transmite junto a una clave cifrada o con componentes en texto claro. Se obtiene cifrando un bloque de entrada de ceros con el algoritmo apropiado (ver secciones 12.2 y 12.3); del resultado se conservan solo los primeros bytes y se descarta el resto.

Es posible usar un valor más largo o más corto empleando menos o más bytes, pero el valor de 3 bytes es el estándar de facto en la industria.

## Ideas clave

- Luhn (ISO/IEC 7812-1) valida el PAN: duplica dígitos en posiciones impares de derecha a izquierda y verifica que la suma total sea divisible por 10.
- Luhn detecta cualquier error de un solo dígito y casi toda transposición de dígitos adyacentes, salvo el intercambio 09 ↔ 90.
- Luhn es idóneo cuando el PAN lo introduce un humano (MOTO y comercio electrónico), donde abundan los errores de tecleo.
- El LRC cierra los datos de la banda magnética y detecta bien errores por ruido; es sencillo de implementar en hardware binario.
- El LRC es el complemento a dos de 8 bits de la suma de bytes: XOR de todos los bytes, invertir con 0xFF, sumar 1 y aplicar AND con 0xFF.
- La validación del LRC se confirma cuando la suma de los valores más el LRC, con AND 0xFF, da 0.
- El KCV confirma la validez de una clave de cifrado sin exponerla: se cifra un bloque de ceros y se conservan los primeros bytes.
- El KCV estándar de facto es de 3 bytes (6 dígitos) y acompaña a la clave cifrada o a sus componentes en claro.
