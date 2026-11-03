# Cryptography 101 (Criptografía 101) — Estudio

## Tarjetas de repaso

P: ¿Por qué el procesamiento de pagos depende de medios criptográficos?
R: Porque no es factible controlar el acceso físico a todos los hosts, dispositivos, elementos de red y cables involucrados, así que se protege criptográficamente los mensajes durante su intercambio.

P: ¿Cómo se llama el mensaje crudo, el proceso de ocultarlo y el resultado?
R: El mensaje crudo es plaintext o cleartext; ocultarlo es encrypt/encipher; el resultado es ciphertext. El proceso inverso es decryption o deciphering.

P: ¿Cuáles son las cuatro funciones mayores de la criptografía?
R: Confidentiality (confidencialidad), authentication (autenticación), integrity (integridad) y nonrepudiation (no repudio).

P: ¿Qué dos parámetros recibe un algoritmo criptográfico típico y qué se mantiene secreto?
R: Recibe los datos (cleartext o ciphertext) y la clave. La clave puede mantenerse secreta mientras el algoritmo se expone al escrutinio independiente.

P: ¿Cuál es la diferencia entre stream cipher y block cipher?
R: El stream cipher opera sobre un byte o bit de cleartext a la vez; el block cipher opera sobre un vector de tamaño fijo (típicamente 8 bytes/64 bits o 16 bytes/128 bits).

P: ¿En qué se diferencian el cifrado simétrico y el asimétrico?
R: En el simétrico la misma clave cifra y descifra; en el asimétrico se usan pares de claves distintas (public key para cifrar, private key para descifrar).

P: ¿Qué es una one-way hash function y qué produce?
R: Convierte una entrada de longitud variable (el mensaje) en una salida de longitud fija (el message digest), sin que sea factible recuperar el mensaje original a partir del digest.

P: ¿Qué distingue a un MAC de un checksum o hash normal?
R: El MAC se calcula añadiendo una clave secreta al mensaje antes de aplicar la función hash; es un valor corto para autenticar el mensaje.

P: ¿Cómo se genera y verifica una firma digital?
R: El emisor hace un hash del mensaje (con timestamp contra replay attacks) y lo cifra con su private key; el receptor rehace el hash, descifra la firma con la public key del emisor y compara.

P: ¿Qué diferencia a los modos ECB y CBC?
R: En ECB cada bloque se cifra de forma independiente (entradas idénticas dan salidas idénticas, más vulnerable); en CBC se cifra secuencialmente, XOR-eando el bloque cifrado previo con el plaintext siguiente, y el primer bloque usa un valor inicial comunicado al receptor.

P: ¿Cómo opera DES y cómo lo extiende 3-DES?
R: DES es un block cipher simétrico de 64 bits con 16 rondas. 3-DES usa tres claves K1, K2, K3 en sucesión: cifra con K1 y K3 y descifra con K2.

P: ¿Qué significan 1TDES, 2TDES y 3TDES y sus tamaños efectivos?
R: Según se reciban una, dos o tres claves. Las claves se concatenan en arrays de 8, 16 o 24 bytes, equivalentes a 56, 112 y 168 bits efectivos; con una clave se reduce a DES y con dos se asume K1 = K3.

P: ¿Qué características tiene AES y qué algoritmo lo implementa?
R: AES (algoritmo Rijndael) trabaja sobre bloques de 128 bits con claves de 128, 192 o 256 bits y ejecuta 10, 12 o 14 rondas según la longitud de clave.

P: ¿Qué variante de MAC se usa típicamente en pagos y cómo se configura?
R: CBC-MAC: un block cipher en modo CBC sobre el mensaje con un vector de inicialización de 0, enviando solo la salida de la última ronda de cifrado.

P: ¿Qué funciones de seguridad habilita el cifrado asimétrico y cómo?
R: Confidencialidad, cifrando con la public key del destinatario, y no repudio, firmando con la private key propia; ambas pueden combinarse.

## Preguntas de autoevaluación

P: ¿Para qué sirve la autenticación como función criptográfica en el contexto de una tarjeta de pago?
R: Permite al receptor confirmar el origen del mensaje para que un tercero no pueda hacerse pasar por el emisor; por ejemplo, confirmar que el chip de la tarjeta es genuino tal como lo emitió el banco. (Sección "Funciones de la criptografía")

P: En una transacción EMV con chip de grado completo, ¿qué garantiza la integridad?
R: Que el mensaje no fue alterado en tránsito; por ejemplo, asegura que el importe de la transacción no se modificó. (Sección "Funciones de la criptografía")

P: ¿Por qué se diseñó 3-DES y qué problema de DES resolvía?
R: Al crecer la potencia de cómputo, DES resultaba vulnerable; 3-DES encadena tres claves (E-D-E) para reforzar el cifrado. (Sección "DES y 3-DES")

P: ¿Qué preocupaciones sobre DES/TDES motivaron la selección de AES por NIST?
R: El hardware especializado podía forzar por fuerza bruta un cifrado DES en muy poco tiempo, ambos corrían lentos en software y el bloque de 64 bits se consideraba demasiado pequeño. (Sección "Algoritmo AES")

P: ¿Dónde adoptan AES los estándares de la industria de pagos?
R: El estándar EMV lo describe en la generación de criptogramas y PIN Transaction Security 3.0 obliga a migrar a él para el cifrado de EPB. (Sección "Algoritmo AES")

P: En el ejemplo de mensaje secreto entre banco y scheme, ¿cómo se logra la confidencialidad?
R: El banco cifra Mclear con la public key del scheme (KE Scheme) obteniendo Menc Scheme, y solo el scheme, que posee la private key, puede descifrarlo aplicando KD Scheme. (Sección "Cifrado asimétrico")

P: ¿Por qué el scheme firma una notificación antes de publicarla a los bancos?
R: Para evitar una declaración falsificada que podría causar pánico o incluso un bank run; firma Nclear con su private key KD Scheme y el banco la verifica con KE Scheme. (Sección "Cifrado asimétrico")

P: En el ejemplo de CBC-MAC con TDES y mensaje de 24 bytes, ¿cómo se obtiene la salida H3?
R: Se cifran los primeros 8 bytes dando H1; H1 se XOR-ea con los segundos 8 bytes y se cifra dando H2; H2 se XOR-ea con los últimos 8 bytes y se cifra dando H3, que es la salida. (Sección "Message Authentication Code")

## Puntos a dominar

- Distinguir plaintext/cleartext, ciphertext y los procesos de encrypt/encipher y decrypt/decipher.
- Enumerar y explicar las cuatro funciones: confidencialidad, autenticación, integridad y no repudio.
- Clasificar algoritmos por stream/block cipher y por simétrico/asimétrico, recordando que el algoritmo puede ser público y la clave secreta.
- Relacionar one-way hash function, message digest, MAC y firma digital, incluyendo el uso del timestamp contra replay attacks.
- Diferenciar los modos de bloque ECB y CBC y por qué ECB es más vulnerable.
- Recordar los parámetros de DES (64 bits, 16 rondas) y el esquema E-D-E de 3-DES con tamaños efectivos 56/112/168 bits.
- Recordar los parámetros de AES (bloques de 128 bits; claves de 128/192/256 bits; 10/12/14 rondas) y su adopción en EMV y PTS 3.0.
- Reconstruir el cálculo de un CBC-MAC con IV de 0 enviando solo la última salida.
- Explicar los escenarios de cifrado asimétrico: mensaje secreto, firma no repudiable y el caso combinado entre banco y scheme.
