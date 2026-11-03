# Validation Algorithms (Algoritmos de validación) — Estudio

## Tarjetas de repaso

P: ¿Qué tres algoritmos de validación recopila el capítulo?
R: El algoritmo de Luhn, el Longitudinal Redundancy Check (LRC) y el Key Check Value (KCV).

P: ¿Son estos algoritmos mecanismos criptográficos de seguridad?
R: No; son comprobaciones para detectar errores de captura, de transmisión o de manipulación de claves.

P: ¿Qué problema resuelve cada algoritmo?
R: Luhn protege el PAN frente a errores humanos de tecleo, el LRC protege los datos de la banda magnética frente a errores de ruido y el KCV confirma la validez de una clave sin exponerla.

P: ¿Qué estándar especifica el algoritmo de Luhn?
R: ISO/IEC 7812-1.

P: ¿Cómo se duplican los dígitos en Luhn?
R: De derecha a izquierda se duplican los dígitos en posiciones impares (el más a la derecha y uno de cada dos hacia la izquierda).

P: En Luhn, ¿qué se hace si al duplicar un dígito el producto es mayor que 9?
R: Se reemplaza por la suma de sus dígitos.

P: ¿Qué condición debe cumplir el resultado final en Luhn para que el número sea válido?
R: El resultado, módulo 10, debe ser 0 (la suma total divisible por 10).

P: ¿Qué transposición de dígitos adyacentes NO detecta Luhn?
R: El intercambio de 09 por 90 o viceversa; detecta casi cualquier otra transposición adyacente y todo error de un solo dígito.

P: ¿Para qué escenarios es idóneo Luhn?
R: Cuando el PAN lo introduce un humano, como pedidos por correo o teléfono (MOTO) y comercio electrónico, donde abundan los errores de tecleo.

P: ¿Cómo se define el LRC?
R: Como el valor de complemento a dos de 8 bits de la suma de todos los bytes módulo 2⁸, de modo que la suma de todos los valores más el LRC da 0.

P: ¿Cuáles son los pasos para calcular el LRC?
R: Aplicar XOR a todos los bytes, invertir el resultado (XOR con 0xFF), sumar uno y aplicar módulo 2⁸ (AND con 0xFF).

P: ¿Cómo se valida el LRC?
R: Se suma el conjunto de valores con el LRC calculado y, al aplicar AND con 0xFF, el resultado debe ser 0.

P: ¿Qué es el KCV y para qué se usa?
R: Un valor de control que confirma la validez de una clave; se utiliza para validar claves de cifrado en la industria de pagos sin exponer la clave.

P: ¿Cómo se obtiene el KCV y cuál es su tamaño estándar?
R: Cifrando un bloque de entrada de ceros con el algoritmo apropiado y conservando los primeros bytes; el valor estándar de facto es de 3 bytes (6 dígitos).

## Preguntas de autoevaluación

P: ¿Por qué el capítulo insiste en que estos algoritmos no son de seguridad criptográfica? (Lo que necesitas saber)
R: Porque están diseñados para detectar errores de captura, transmisión o manipulación de claves, no para proteger frente a ataques; cada uno resuelve un problema de detección de errores distinto.

P: En el ejemplo del número 491023693576, ¿por qué 6 es un dígito de control válido? (10.1 Luhn Algorithm)
R: Porque la suma de todos los dígitos tras aplicar Luhn es 60, que es divisible por 10, por lo que el resultado módulo 10 es 0.

P: ¿Cómo se calcula el dígito de control de Luhn cuando el total no es divisible por 10? (10.1 Luhn Algorithm)
R: Se siguen los pasos 1 a 4 asumiendo un dígito de control de 0 y, si el total no es divisible por 10, se reemplaza el dígito de control por 10 menos la suma módulo 10.

P: En el ejemplo del LRC con FA 13 58 A0 C5, ¿cuál es el LRC resultante y cómo se llega a él? (10.2 Longitudinal Redundancy Check)
R: El LRC es 0x74: el XOR de los bytes da 0x8C, su complemento a dos (XOR con 0xFF) da 0x73 y al sumar 1 se obtiene 0x74.

P: ¿Cómo se demuestra que el LRC del ejemplo es correcto al validarlo? (10.2 Longitudinal Redundancy Check)
R: Sumando el conjunto de valores con el LRC calculado se obtiene 0x100, que al aplicarle AND con 0xFF da 0.

P: ¿Por qué el KCV permite confirmar una clave sin exponerla? (10.3 Key Check Value)
R: Porque se cifra un bloque de ceros y solo se conservan los primeros bytes del resultado, transmitiéndose junto a la clave cifrada o a sus componentes en claro, sin revelar la clave.

P: ¿Qué ventaja ofrece el LRC para los datos de la banda magnética? (10.2 Longitudinal Redundancy Check)
R: Es fácil de implementar en hardware binario y especialmente bueno para detectar errores relacionados con el ruido, cerrando los datos almacenados en la banda.

## Puntos a dominar

- Explicar los cinco pasos de validación del algoritmo de Luhn y verificar un PAN de ejemplo.
- Calcular el dígito de control de Luhn, incluido el caso en que el dígito resultante es 0.
- Reconocer qué errores detecta Luhn (todo error de un solo dígito, casi toda transposición adyacente) y su única excepción (09 ↔ 90).
- Calcular y validar un LRC siguiendo XOR, complemento a dos (XOR con 0xFF), suma de 1 y AND con 0xFF.
- Describir cómo se genera un KCV cifrando un bloque de ceros y por qué el estándar es de 3 bytes.
- Asociar cada algoritmo con su caso de uso: PAN tecleado (Luhn), banda magnética (LRC), validación de clave de cifrado (KCV).
