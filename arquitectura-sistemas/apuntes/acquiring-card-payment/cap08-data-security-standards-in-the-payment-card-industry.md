# Acquiring Card Payments — Ilya Dubinsky (CRC Press / Taylor & Francis, 2019)
## Capítulo 8 — Data Security Standards in the Payment Card Industry (Estándares de seguridad de datos en la industria de tarjetas de pago)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas usan la página del PDF `(PDF p. N)`.

## Lo que necesitas saber

El capítulo describe el marco de estándares de seguridad de datos de la industria de tarjetas, creado y mantenido por el PCI Security Standards Council (PCI SSC), fundado en 2006 por American Express, Discover, JCB, MasterCard y Visa tras numerosas brechas de datos. Dado lo pocos datos que hacen falta para ejecutar un pago con tarjeta, proteger los datos de tarjeta y de titular es esencial contra el fraude.

Se explican tres bloques. Primero, el PCI DSS (Payment Card Industry Data Security Standard): qué es dato de cuenta, cómo se certifica el cumplimiento (auditoría QSA o cuestionario de autoevaluación SAQ), los tipos de SAQ y los seis principios centrales con sus doce requisitos. Segundo, el PCI PA DSS (Payment Application Data Security Standard), aplicable a los desarrolladores de aplicaciones de pago, con sus 14 requisitos. Tercero, la gestión de claves con módulos de seguridad hardware (HSM): jerarquía de claves, variantes y key blocks, zonas de confianza, componentes de clave, requisitos PCI PIN Security (PTS v3.0) y la ceremonia de claves con custodios.

Sales sabiendo cómo encaja el ecosistema de estándares PCI, qué datos se pueden o no almacenar, cómo se asignan niveles de cumplimiento, y cómo se protegen y gestionan las claves criptográficas de PIN mediante HSM bajo principios de control dual y conocimiento repartido.

## PCI Data Security Standard (PCI DSS)

El PCI DSS cubre requisitos técnicos y operativos para proteger los datos de cuenta. Define el cardholder data environment (CDE) como las personas, procesos y tecnologías que almacenan, procesan o transmiten datos de titular o datos de autenticación sensibles. Sus requisitos alcanzan a todos los componentes incluidos o conectados al CDE: si una máquina no maneja datos de cuenta pero reside en el mismo segmento de red que otra que sí lo hace, el estándar también le aplica.

### Dato de cuenta

El dato de cuenta se compone de datos de titular (CHD) y datos de autenticación sensibles (SAD).

- Cardholder data (CHD): el Primary Account Number (PAN), el nombre del titular, el service code y la fecha de expiración. Los tres últimos solo se consideran CHD si se almacenan junto al PAN. Está permitido almacenar CHD (con requisitos adicionales). El estándar exige volver ilegible el PAN, lo habitual es enmascarar todo salvo el BIN (primeros seis) y los últimos cuatro dígitos; el Requisito 3.3 prohíbe mostrar más dígitos a quien no tenga una necesidad legítima de negocio.
- Sensitive authentication data (SAD): track completo (tracks 1, 2 y 3), datos CVV2, el PIN y el PIN block. A diferencia del CHD, está prohibido almacenar SAD, incluso cifrado con fuerza.

### Niveles de cumplimiento y proceso de evaluación

El PCI DSS no define "niveles de cumplimiento": una entidad cumple o no cumple. Sí hay dos vías para certificar el cumplimiento: una auditoría por un Qualified Security Auditor (QSA), o completar un Self-Assessment Questionnaire (SAQ). Al completar un SAQ, el personal autorizado firma una Attestation of Compliance (AOC). Tras una auditoría QSA, el auditor prepara un Report of Compliance (ROC), que puede incluir planes de acción con fechas y controles compensatorios bien definidos. Un QSA también puede participar en un SAQ si la entidad lo desea.

Los esquemas de pago agrupan a las entidades en "niveles" que no forman parte del estándar y se fijan a discreción de cada esquema. El nivel 1 (el más alto) suele exigir auditoría anual por QSA; niveles inferiores pueden requerir auditoría inicial y luego autoevaluación, o solo SAQ anuales. Los niveles se asignan según volúmenes anuales de transacciones card-present y card-not-present (un esquema puede contar el volumen total de todos los esquemas). Es típico tolerar más transacciones card-present que card-not-present para un mismo nivel. Además, se exigen escaneos de vulnerabilidades internos y externos al menos trimestralmente y tras cada cambio mayor; los externos los realiza un Approved Scanning Vendor (ASV).

### Cuestionarios de autoevaluación (SAQ)

El tipo de SAQ depende del entorno de procesamiento del comercio. La mayoría no admiten almacenamiento de CHD; quien almacena CHD pasa automáticamente al SAQ D, el de mayor alcance.

- SAQ A: comercios no presenciales que han externalizado todo el procesamiento a una entidad PCI DSS compliant y no procesan, transmiten ni almacenan CHD.
- SAQ A-EP: igual que A pero con un sitio web que puede afectar a la seguridad del pago.
- SAQ B: comercios card-present con imprinters o conexión dial-up al procesador.
- SAQ B-IP: comercios card-present con terminales PCI PTS aprobados y conexión IP, sin almacenar CHD.
- SAQ C: comercios card-present con sistemas de pago conectados a internet.
- SAQ C-VT: comercios que teclean tarjetas (en entorno card-present) en un terminal virtual de un tercero.
- SAQ P2PE: comercios card-present con terminal P2PE gestionado y listado por PCI SSC.
- SAQ D: el más completo, en dos variantes (SAQ D for Merchants y SAQ D for Service Providers). Lo usan las entidades que almacenan CHD, con independencia de la presencia de tarjeta.

### Principios del PCI DSS

El estándar se estructura en seis principios centrales divididos en doce requisitos con subrequisitos, procedimientos de prueba y criterios de cumplimiento. Todo aspecto debe desplegarse de forma segura, cualquier cambio debe tener razón de negocio documentada y dejar rastro, y debe evaluarse periódicamente.

Build and Maintain a Secure Network and Systems:
- Requisito 1: instalar y mantener configuración de firewall para proteger CHD (segmentación, procesos de cambio documentados, sincronización de routers/firewalls, dispositivos portátiles conectados al CDE).
- Requisito 2: no usar valores por defecto del proveedor para contraseñas y parámetros; cada host debe ofrecer un solo servicio mayor (p. ej. NTP o DNS) y deshabilitar el resto.

Protect Cardholder Data:
- Requisito 3: proteger el CHD almacenado; no almacenar SAD, minimizar el almacenamiento con políticas de retención, hashear/truncar/cifrar el PAN y gestionar y rotar claves con seguridad.
- Requisito 4: cifrar la transmisión de CHD por redes públicas abiertas con criptografía fuerte; nunca enviar un PAN completo sin cifrar por SMS o mensajería.

Maintain a Vulnerability Management Program:
- Requisito 5: proteger los sistemas contra malware con antivirus actualizado que el usuario no pueda deshabilitar.
- Requisito 6: desarrollar y mantener sistemas y aplicaciones seguros; parchear vulnerabilidades de terceros con plazos, separar desarrollo/pruebas de producción, deshabilitar cuentas de desarrollo/prueba antes de desplegar y someter el código a revisión de seguridad por un revisor formado.

Implement Strong Access Control Measures:
- Requisito 7: restringir el acceso al CHD por necesidad de negocio, con nivel por defecto "deny all".
- Requisito 8: identificar y autenticar el acceso; identificador único por usuario, prohibición de cuentas de grupo y contraseñas compartidas, acceso directo a la base de datos solo para DBA, y MFA para todo acceso administrativo no-console.
- Requisito 9: restringir el acceso físico al CHD; control de entrada a instalaciones, gestión de visitantes, clasificación/almacenamiento/envío/destrucción de medios, y protección de dispositivos frente a manipulación.

Regularly Monitor and Test Networks:
- Requisito 10: rastrear y monitorizar todo acceso creando un audit trail revisado periódicamente.
- Requisito 11: probar regularmente sistemas y procesos; escaneo de puntos de acceso inalámbricos no autorizados, escaneos trimestrales internos y externos, y pruebas de penetración.

Maintain an Information Security Policy:
- Requisito 12: mantener una política de seguridad publicada a todo el personal (empleados, contratistas, consultores), con evaluación de riesgos periódica y plan de respuesta a incidentes.

## PCI Payment Applications Data Security Standard (PCI PA DSS)

El PCI PA DSS aplica a los proveedores de software que desarrollan aplicaciones de pago, definidas como las que "almacenan, procesan o transmiten datos de titular y/o datos de autenticación sensibles". La diferencia clave con PCI DSS es el alcance: PA DSS cubre una aplicación individual, mientras que DSS cubre la solución o los sistemas completos de la empresa. Una aplicación puede ser PA DSS compliant y desplegarse de forma que incumpla PCI DSS; a la inversa, se puede usar una aplicación no compliant pero cumplir PCI DSS con controles compensatorios (por ejemplo, una aplicación de terminal no compliant sobre un dispositivo que cumple PCI PTS). Tener certificación PA DSS de todas las aplicaciones relevantes acorta mucho la auditoría PCI DSS, por lo que es muy recomendable.

El estándar contiene 14 requisitos, mapeados a los correspondientes de PCI DSS:

- Requisito 1: no retener track completo, códigos de verificación (CAV2, CID, CVC2, CVV2) ni PIN block; con excepción para software de emisores; eliminar SAD tras la autorización y durante actualizaciones.
- Requisito 2: proteger el CHD almacenado; guía de limpieza tras retención, enmascarado del PAN, volverlo ilegible, proteger las claves criptográficas y poder inutilizar claves obsoletas (preferiblemente con HSM).
- Requisito 3: autenticación segura; cuentas individuales, políticas de contraseña, expiración de sesión, bloqueos, acceso de grano fino y prohibición de cuentas por defecto/grupo/genéricas.
- Requisito 4: registrar la actividad de la aplicación; todo acceso a CHD (con éxito o fallido), acciones de administradores y cualquier intento de acceder o alterar los logs.
- Requisito 5: desarrollar aplicaciones de forma segura; considerar todo el alcance de PCI DSS, evitar vulnerabilidades comunes, formación y revisiones de seguridad, control de versiones, gestión de cambios, documentar cómo se guarda SAD en memoria y nunca usar PAN reales en pruebas.
- Requisito 6: proteger transmisiones inalámbricas; cambiar valores por defecto y usar buena autenticación/cifrado (WEP prohibido).
- Requisito 7: probar la aplicación frente a vulnerabilidades y mantener actualizaciones, con parcheo oportuno y documentación en las notas de versión.
- Requisito 8: facilitar una implementación de red segura; no exigir desactivar el antivirus, no depender de procesos inseguros ni usar puertos de protocolos de seguridad estándar.
- Requisito 9: el CHD nunca debe almacenarse en un servidor conectado a internet; permitir desplegar el servidor de datos en otro segmento de red.
- Requisito 10: facilitar el acceso remoto seguro; MFA para todo el personal y activar el acceso solo justo antes/después de la descarga si no hay VPN.
- Requisito 11: cifrar el tráfico sensible por redes públicas, con criptografía fuerte también para PAN enviados por canales de usuario final (p. ej. email).
- Requisito 12: asegurar todo acceso administrativo no-console con cifrado fuerte (SSH en lugar de telnet) y MFA.
- Requisito 13: mantener una PA-DSS Implementation Guide para clientes, revendedores e integradores.
- Requisito 14: asignar responsabilidades PA-DSS y mantener programas de formación revisados anualmente.

## Gestión de claves con módulos de seguridad hardware (HSM)

Los HSM realizan todas las operaciones criptográficas en un entorno protegido. Tienen sensores (incluso de vibración) y destruyen su contenido ante manipulaciones; existen líneas específicas para zonas sísmicas. Todos los datos sensibles dentro del HSM se protegen con una o varias master keys, llamadas Local Master Key (LMK) o Master File Key (MFK); pueden coexistir varias LMK. Para el acceso administrativo, la LMK se escribe en al menos dos smart cards que, de perderse, inutilizan ese slot. Se usan al menos dos llaves físicas para pasar el HSM a modo administración. Una vez desplegado, incluso el propietario tiene control limitado.

Los HSM usan dos tipos de claves: data encryption keys (para calcular valores de validación de tarjeta y de PIN, descifrar y traducir PIN blocks) y key encryption keys (KEK), usadas solo para cifrar claves de datos. Las KEK se almacenan fuera del HSM bajo LMK, y las claves de datos bajo KEK; ambas pueden guardarse en una base de datos o sistema de ficheros externos. Ejemplo (validación de CVV): la CVK se cifra bajo LMK (CVK_LMK) y se guarda externamente asociada a un rango de PAN; al llegar la transacción, se envía al HSM el dato CVV y la CVK_LMK, el HSM descifra la CVK y valida. En la traducción de PIN, un EPB cifrado con una acquirer worker key (AWK1) se reencripta bajo otra (AWK2); los parámetros son EPB_AWK1, AWK1_LMK, AWK2_LMK, y los valores en claro nunca existen fuera del HSM.

Tipos de clave (Tabla 8.1): master key (LMK/MFK/KKM), usada para derivar y cifrar otras claves, nunca datos; zone master key (ZMK, también KEK/KK), para establecer confianza en una zona; PIN key (ZPK, PEK, AWK, IWK), para cifrar/descifrar el PIN en un PIN block; data key (DEK/DK), genérica para cifrar datos.

Para proteger PIN blocks y claves de PIN se usa 3-DES con claves de longitud simple, doble o triple (binarios de 8, 16 o 24 bytes). Como la "criptografía fuerte" de PCI DSS exige un mínimo efectivo de 112 bits, las claves DES de longitud simple no son compliant y solo deben usarse, si acaso, en desarrollo/pruebas; los HSM detectan y prohíben claves simples "disfrazadas" de doble/triple. Como DES es un cifrador de bloque de 8 bytes, las claves se cifran sin padding; el estándar ANSI X9.17 (asumido por defecto) solo requiere 3-DES con la KEK adecuada.

### Variantes y key blocks

Para limitar el uso de una clave a su propósito y reducir superficie de ataque, las representaciones propietarias aplican una variante (un valor predefinido que se hace XOR con la clave durante su cifrado 3-DES). Como un bit de cada byte de la clave 3-DES es de paridad, usar una clave con variante donde se espera una X9.17 suele dar error de paridad; aun así el método está obsoleto y se reemplaza por el key block. En un key block la clave se envuelve en una estructura con su propósito, longitud, la clave cifrada y una firma (hash fuerte, el key block authenticator); así el dispositivo seguro no permite usar la clave fuera de lo definido en su cabecera.

### Zonas de confianza y componentes de clave

Cuando dos HSM deben compartir una clave (p. ej. en la traducción de PIN entre segmentos de red o el intercambio de CVK entre emisores y esquemas para stand-in), se usa la noción de zona, con separación entre KEK y claves de datos. Establecer una zona tiene dos pasos. Primero se comparte una Zone Master Key (ZMK): los custodios de la Parte A generan la ZMK en componentes en claro, la combinan bajo la LMK de A, entregan sus componentes a los custodios de la Parte B, y B los combina bajo su propia LMK. Ambas partes quedan con una KEK compartida. Después se generan e intercambian las worker keys (ZPK/AWK): A genera la ZPK bajo LMK y bajo ZMK, retiene la versión bajo LMK y envía la versión bajo ZMK (que al ir cifrada puede enviarse por red pública, incluso por email) a B, que la importa a su HSM.

El intercambio de secretos de zona en claro sigue el principio de conocimiento repartido multiparte (multi-party split knowledge): al menos tres oficiales generan cada uno componentes en claro durante una key ceremony. Los componentes son cadenas binarias en hexadecimal escritas en formularios; su longitud iguala la de la futura clave (32 para doble longitud, 48 para triple). Se reimportan para formar la ZMK bajo LMK del emisor y generar un key check value (KCV). Los custodios envían los componentes y el KCV a la otra institución en sobres tamper-evident, por tres métodos de entrega distintos y en fechas distintas. El receptor recombina los componentes mediante XOR y compara el KCV para confirmar el proceso.

### Requisitos de seguridad de PIN (PCI PTS v3.0)

Los esquemas imponen requisitos y procedimientos de prueba para proteger los PIN, hoy convergentes en las PIN Security Requirements v3.0. Principios generales: se distingue entre entidades que validan PIN (emisor, PIN online) y las que solo lo transportan (acquirer puro, no validante); todo hardware que maneje PIN en claro (ATM, HSM, PIN pads) debe ser tamper-resistant; no se registran PIN blocks y el store-and-forward suele prohibirse; las claves se generan con un RNG que satisface FIPS 140-2; rigen el control dual y el conocimiento repartido; las claves fuera del HSM van en contenedores tamper-evident bajo supervisión; cada clave es única, suficientemente larga y de un solo propósito; todo el ciclo de vida de claves y equipos se registra y documenta.

El estándar PTS 3.0 se organiza en siete control objectives con 33 requisitos. CO 1 (Req. 1–5): PIN procesados por dispositivos criptográficos seguros (ISO 13491, PCI PTS o FIPS), sin pedir nunca el PIN al cliente, validación offline según EMV, formatos de EPB permitidos (0, 1, 3 y 4 host-a-host; 2 para lector-a-tarjeta) y RNG para generación de claves. CO 2 (Req. 6–8): generación de claves sin colusión de menos de dos individuos, procedimientos documentados y transmisión segura de claves públicas y privadas. CO 3 (Req. 9–11): transporte seguro de componentes en claro en sobres tamper-evident, con KEK al menos tan fuertes como las claves que protegen. CO 4 (Req. 12–16): carga de claves bajo control dual y conocimiento repartido, protección frente a monitorización y validación por KCV. CO 5 (Req. 17–20): claves secretas únicas por enlace (origen de las zonas de confianza), detección de sustitución, uso de único propósito y sin mezclar test/producción, y unicidad en dispositivos de origen. CO 6 (Req. 21–28): claves solo dentro de un dispositivo seguro, cifradas, o en claro repartidas en componentes; procedimientos de reemplazo ante compromiso, destrucción de claves obsoletas, acceso need-to-know, logs y backups mínimos. CO 7 (Req. 29–33): equipos verificados contra manipulación, protegidos física y lógicamente, con destrucción segura y generación de claves bajo acceso dual.

### Custodios y ceremonia de claves

Una institución nombra al menos tres custodios de clave, formados y de departamentos distintos, con custodios de respaldo. Cada uno recibe una caja fuerte donde guarda su material criptográfico en sobres tamper-evident, con inventario y log de acceso. La generación de claves exige la presencia de los tres. En el ejemplo de un acquirer puro con PIN online: los HSM se compran a un proveedor certificado, se inspecciona el embalaje y se documenta su manejo hasta el despliegue en una jaula cerrada con doble cerradura. Los custodios inicializan las master keys en smart cards asignadas a distintos custodios, cada uno con su PIN en reclusión. Para generar una ZMK, se reparten las llaves físicas (custodios 1 y 3) y las smart cards (custodios 1 y 2) de modo que ningún par pueda coludir. Cada custodio genera y anota su componente sin que otros lo vean, luego se reintroducen para formar la ZMK, se anota la ZMK bajo LMK y se sellan los componentes. Finalmente cada custodio envía su componente a su contraparte en fechas y métodos distintos; si un sobre muestra manipulación, no coincide con el manifiesto o el número de serie es erróneo, la clave se considera comprometida y se reinicia el proceso.

## Ideas clave

- El PCI SSC (fundado en 2006 por Amex, Discover, JCB, MasterCard y Visa) mantiene PCI DSS, PCI PA DSS y PCI PTS, entre otros estándares.
- El dato de cuenta son CHD (PAN y, junto a él, nombre, service code y expiración) y SAD (track completo, CVV2, PIN, PIN block); el CHD puede almacenarse (con el PAN ilegible), el SAD nunca.
- El cumplimiento de PCI DSS se certifica por auditoría QSA (con ROC) o por SAQ (con AOC); los "niveles" los fijan los esquemas según volumen, no el estándar.
- Los seis principios de PCI DSS se concretan en doce requisitos que cubren red segura, protección del CHD, gestión de vulnerabilidades, control de acceso, monitorización y política de seguridad.
- PCI PA DSS aplica a aplicaciones individuales (14 requisitos mapeados a PCI DSS); la certificación acorta la auditoría DSS pero no la sustituye.
- Los HSM protegen todas las claves bajo LMK; separan KEK (cifran claves) de data keys (cifran datos), usan 3-DES y limitan el uso de claves con variantes o key blocks.
- Las zonas de confianza comparten una ZMK para intercambiar worker keys (ZPK/AWK) entre HSM mediante componentes en claro intercambiados por conocimiento repartido.
- PCI PTS v3.0 define 7 objetivos de control y 33 requisitos; la ceremonia de claves con al menos tres custodios aplica control dual y conocimiento repartido para que ninguna persona pueda comprometer las claves por sí sola.
