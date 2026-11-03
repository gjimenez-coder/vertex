# Acquiring Card Payments — Ilya Dubinsky (CRC Press, Taylor & Francis, 2019)
## Capítulo 12 — Cryptography 101 (Criptografía 101)

> Nota de extracción: texto obtenido de la capa de texto del PDF; las citas usan la página del PDF `(PDF p. N)`.

## Lo que necesitas saber

El capítulo es una introducción a los términos criptográficos básicos, acotada a lo relevante para entender la tecnología de procesamiento de pagos. Como el procesamiento de pagos implica mover datos sensibles entre partes y no es factible controlar el acceso físico a todos los hosts, dispositivos, elementos de red y cables involucrados, la industria recurre a medios criptográficos para proteger los mensajes durante su intercambio.

Sales sabiendo el vocabulario central: un mensaje crudo es plaintext o cleartext; ocultarlo (encrypt/encipher) produce ciphertext; y el proceso inverso es decryption o deciphering. También conocerás las cuatro funciones mayores de la criptografía y la clasificación de algoritmos en cifradores de flujo/bloque y simétricos/asimétricos.

La tesis central: con estos ladrillos (DES/3-DES, AES, MAC y cifrado asimétrico) se construyen las garantías de seguridad que usan EMV y los estándares de la industria de pagos.

## Funciones de la criptografía

- Confidentiality (confidencialidad): asegura que solo el emisor y el receptor vean el mensaje, impidiendo que un tercero que espíe el canal discierna su contenido. Se usa para mantener seguros los canales entre partes del pago.
- Authentication (autenticación): permite al receptor confirmar el origen del mensaje para que un tercero no pueda hacerse pasar por el emisor; por ejemplo, confirmar que el chip de la tarjeta es genuino tal como lo emitió el banco.
- Integrity (integridad): permite verificar que el mensaje no fue alterado en tránsito; por ejemplo, en una transacción EMV con chip de grado completo, asegura que su importe no se modificó.
- Nonrepudiation (no repudio): impide que el emisor niegue haber enviado el mensaje.

Un algoritmo criptográfico típico recibe dos parámetros: los datos (cleartext a cifrar o ciphertext a descifrar) y la clave. La clave puede mantenerse secreta mientras el algoritmo se expone al escrutinio independiente.

Clasificaciones:
- Stream cipher: opera sobre un byte o bit de cleartext a la vez. Block cipher: opera sobre un vector de tamaño fijo (típicamente 8 bytes/64 bits o 16 bytes/128 bits).
- Simétrico: la misma clave cifra y descifra. Asimétrico: pares de claves distintas; en cifrado de datos, la de cifrado suele llamarse public key y la de descifrado private key.

### Funciones hash de una vía, MAC y firma digital

Una one-way hash function convierte una entrada de longitud variable (el mensaje) en una salida de longitud fija (el message digest); no es factible recuperar el mensaje original a partir del digest. Sirve como herramienta para generar un MAC (message authentication code), donde se añade una clave secreta al mensaje antes de aplicar la función hash.

Para generar una firma digital, el emisor produce un hash del mensaje (añadiéndole un timestamp para evitar replay attacks) y cifra el digest con su private key, enviando el mensaje y la firma. El receptor genera el mismo hash, descifra la firma con la public key del emisor y compara; si coinciden, la firma es válida.

### Modos de cifrado por bloques

Para datos más largos que el bloque del cifrador, primero se rellenan (padding) a una longitud divisible por el tamaño de bloque. Los dos modos más comunes:
- ECB (electronic code book): cada bloque se cifra de forma independiente, lo que aumenta la vulnerabilidad porque entradas idénticas producen salidas idénticas.
- CBC (cipher block chaining): se cifra secuencialmente; el valor cifrado de un bloque se XOR-ea con el plaintext del bloque siguiente antes de cifrarlo. El primer bloque se XOR-ea con un valor especial que debe comunicarse al receptor para poder descifrar.

## DES y 3-DES

DES (Data Encryption Standard) es un block cipher simétrico desarrollado a inicios de los años 80 por investigadores de IBM junto con la NSA, definido como estándar de cifrado simétrico para agencias del gobierno de EE. UU. (FIPS). Sus pasos previenen la mayoría de ataques criptográficos y se prestan a implementación en hardware especializado más rápido que el software.

DES opera sobre bloques de 64 bits (8 bytes de plaintext a 8 bytes de ciphertext). El bloque se permuta, se parte en mitades de 32 bits y se combina con la clave repetidamente durante 16 rondas; al final las mitades se recombinan y se hace una permutación final. La clave original era de 8 bytes/64 bits, con un bit por byte reservado como control de paridad.

Al crecer la potencia de cómputo, se diseñó 3-DES (o T-DES), que usa tres claves K1, K2, K3 aplicadas en sucesión: cifra con K1 y K3 y descifra con K2.

```
C = EK1(DK2(EK3(M)))
M = DK1(EK2(DK3(C)))
```

Según reciba una, dos o tres claves se denota 1TDES, 2TDES o 3TDES. Con una clave (K1 = K2 = K3) se reduce a DES estándar; con dos, se asume K1 = K3. Las claves se transmiten y registran como un array concatenado de 8, 16 o 24 bytes, equivalentes a tamaños efectivos de 56, 112 y 168 bits.

## Algoritmo AES

Hacia finales del siglo XX surgieron preocupaciones con DES y TDES: el hardware especializado podía forzar por fuerza bruta un cifrado DES en muy poco tiempo, ambos corrían lentos en software y el bloque de 64 bits se consideraba demasiado pequeño. Por ello NIST inició el proceso de selección del Advanced Encryption Standard (AES), que eligió el algoritmo Rijndael como nuevo estándar oficial de cifrado simétrico.

AES trabaja sobre bloques de 128 bits con claves de 128, 192 o 256 bits. Representa los 16 bytes de entrada como una matriz 4 × 4 en orden column-major y ejecuta 10, 12 o 14 rondas según la longitud de clave. Se deriva una round key por ronda y el algoritmo:

- XOR-ea la round key con la matriz de entrada.
- Durante 9, 11 o 13 rondas sustituye bytes según una tabla de sustitución, desplaza las filas (mezclando bytes entre columnas), multiplica cada columna por una matriz de coeficientes (combinación lineal de los bytes) y XOR-ea el resultado con la round key correspondiente.
- En la ronda final sustituye bytes y desplaza filas, y XOR-ea con la round key final.

Se considera muy seguro. El estándar EMV describe su uso en la generación de criptogramas y el estándar PIN Transaction Security 3.0 obliga a migrar a él para el cifrado de EPB.

## Message Authentication Code

Un MAC es un valor corto (relativo al tamaño del mensaje) usado para autenticar un mensaje; se diferencia de un checksum o hash porque se calcula con una clave secreta. En pagos se usa típicamente la variante CBC-MAC: un block cipher en modo CBC sobre el mensaje con un vector de inicialización de 0, enviando solo la salida de la última ronda de cifrado.

Ejemplo con TDES y un mensaje de 24 bytes tras el padding, IV de ceros: los primeros 8 bytes se cifran con la clave TDES dando H1; H1 se XOR-ea con los segundos 8 bytes y se cifra dando H2; H2 se XOR-ea con los últimos 8 bytes y se cifra dando H3, que es la salida del algoritmo.

## Cifrado asimétrico

El cifrado asimétrico usa dos claves distintas (un par). La public key cifra datos o verifica una firma digital; la private key descifra datos o calcula una firma digital. Hay dos escenarios mayores: cifrado de mensaje y firma no repudiable.

El capítulo lo ilustra con un banco y un scheme, cada uno con su par de claves (KE/KD), que comparten la parte pública con la otra parte:

- Mensaje secreto: el banco tiene problemas con ciertos PANs y quiere compartirlos de forma segura con el equipo de soporte del scheme. Forma Mclear y lo cifra con la public key del scheme (KE Scheme) obteniendo Menc Scheme. Solo el scheme, que posee la private key relevante, puede descifrarlo aplicando KD Scheme.
- Firma: el scheme emite una instrucción a ciertos bancos para limitar transacciones. Para evitar una declaración falsificada (que podría causar pánico o incluso un bank run), el scheme firma la notificación Nclear con su private key KD Scheme y publica la notificación en claro junto con la firma Nsign Scheme; el banco la verifica con KE Scheme.
- Combinado: el banco cifra Mclear en Menc Scheme y aporta una firma Msign Bank usando KE Scheme y KD Bank respectivamente; envía ambos valores. El scheme usa su private KD Scheme para obtener Mclear y la public key del banco KE Bank para verificar Msign Bank.

## Ideas clave

- El procesamiento de pagos depende de la criptografía porque no es factible proteger físicamente todo el canal de extremo a extremo.
- Las cuatro funciones son confidencialidad, autenticación, integridad y no repudio.
- Los algoritmos se clasifican en stream/block cipher y en simétricos/asimétricos; el algoritmo puede ser público, la clave se mantiene secreta.
- DES es simétrico de 64 bits y 16 rondas; 3-DES encadena tres claves (E-D-E) con tamaños efectivos de 56, 112 o 168 bits.
- AES (Rijndael) usa bloques de 128 bits y claves de 128/192/256 bits con 10/12/14 rondas; EMV y PTS 3.0 lo adoptan.
- El MAC se calcula con clave secreta; en pagos se usa CBC-MAC (IV de 0, se envía solo la última salida).
- El cifrado asimétrico habilita confidencialidad (cifrar con la public key del destinatario) y no repudio (firmar con la private key propia), y ambas pueden combinarse.
- Modos de bloque: ECB cifra cada bloque independiente (riesgoso); CBC encadena vía XOR con el bloque previo y requiere comunicar el valor inicial.
