# Estándares de seguridad de datos en la industria de tarjetas de pago — Estudio

## Tarjetas de repaso

P: ¿Qué es el PCI SSC y quién lo fundó? / R: El PCI Security Standards Council, organismo que crea y mantiene los estándares de seguridad; fundado en 2006 por American Express, Discover, JCB, MasterCard y Visa.

P: ¿En qué se dividen los datos de cuenta? / R: En cardholder data (CHD) y sensitive authentication data (SAD).

P: ¿Qué incluye el CHD y qué puede almacenarse? / R: El PAN y, solo si se almacenan junto al PAN, el nombre del titular, el service code y la fecha de expiración; el CHD puede almacenarse con requisitos adicionales y el PAN debe volverse ilegible.

P: ¿Qué incluye el SAD y qué política de almacenamiento tiene? / R: Track completo (tracks 1, 2 y 3), CVV2, PIN y PIN block; está prohibido almacenarlo, incluso cifrado con fuerza.

P: ¿Cuáles son las dos vías para certificar el cumplimiento de PCI DSS? / R: Una auditoría por un Qualified Security Auditor (QSA), que produce un Report of Compliance (ROC), o completar un Self-Assessment Questionnaire (SAQ), que se firma con una Attestation of Compliance (AOC).

P: ¿Qué es el CDE (cardholder data environment)? / R: Las personas, procesos y tecnologías que almacenan, procesan o transmiten datos de titular o datos de autenticación sensibles; el estándar alcanza también a los componentes conectados al mismo segmento de red.

P: ¿Quién define los "niveles" de cumplimiento y según qué criterio? / R: No los define el estándar (una entidad cumple o no); los fijan los esquemas de pago a su discreción según el volumen anual de transacciones card-present y card-not-present.

P: ¿Cuáles son los seis principios centrales de PCI DSS? / R: Construir y mantener una red segura, proteger el cardholder data, mantener un programa de gestión de vulnerabilidades, implementar control de acceso fuerte, monitorizar y probar redes regularmente, y mantener una política de seguridad de la información.

P: ¿En qué se diferencia PCI PA DSS de PCI DSS? / R: PA DSS cubre una aplicación de pago individual (14 requisitos mapeados a DSS), mientras que DSS cubre la solución o los sistemas completos de la empresa.

P: ¿Qué protege todos los datos sensibles dentro de un HSM? / R: Una o varias master keys llamadas Local Master Key (LMK) o Master File Key (MFK).

P: ¿Qué diferencia hay entre data encryption keys y key encryption keys (KEK)? / R: Las data keys calculan valores de validación y descifran/traducen PIN blocks; las KEK se usan solo para cifrar claves de datos, y se almacenan fuera del HSM bajo LMK.

P: ¿Qué es un key block y qué ventaja aporta frente a las variantes? / R: Una estructura que envuelve la clave con su propósito, longitud, la clave cifrada y una firma (key block authenticator), de modo que el dispositivo no permite usar la clave fuera de lo definido en su cabecera; reemplaza al método obsoleto de variantes.

P: ¿Para qué sirve una Zone Master Key (ZMK)? / R: Para establecer una zona de confianza entre dos HSM: ambas partes quedan con una KEK compartida con la que luego intercambian worker keys (ZPK/AWK).

P: ¿Qué principio rige el intercambio de secretos de zona en claro? / R: El conocimiento repartido multiparte (multi-party split knowledge): al menos tres oficiales generan cada uno componentes en claro durante una key ceremony, junto con el control dual.

P: ¿Cómo se organiza el estándar PCI PTS v3.0? / R: En siete control objectives con 33 requisitos para proteger los PIN.

## Preguntas de autoevaluación

P: ¿Por qué un equipo que no maneja datos de cuenta puede quedar igualmente sujeto a PCI DSS? / R: Porque el estándar alcanza a todos los componentes incluidos o conectados al CDE; si reside en el mismo segmento de red que otra máquina que sí maneja datos de cuenta, también le aplica. (Sección: PCI Data Security Standard)

P: Si un comercio almacena CHD, ¿qué SAQ debe usar y por qué? / R: El SAQ D, el de mayor alcance, porque quien almacena CHD pasa automáticamente a él con independencia de la presencia de tarjeta. (Sección: Cuestionarios de autoevaluación)

P: ¿Cómo se suele volver ilegible el PAN y qué exige el Requisito 3.3? / R: Enmascarando todo salvo el BIN (primeros seis) y los últimos cuatro dígitos; el Requisito 3.3 prohíbe mostrar más dígitos a quien no tenga necesidad legítima de negocio. (Sección: Dato de cuenta)

P: ¿Puede una aplicación PA DSS compliant desplegarse de forma que incumpla PCI DSS? / R: Sí; a la inversa, se puede usar una aplicación no compliant y aun así cumplir PCI DSS con controles compensatorios (p. ej. una aplicación de terminal no compliant sobre un dispositivo que cumple PCI PTS). (Sección: PCI Payment Applications Data Security Standard)

P: En la validación de CVV con HSM, ¿por qué los valores en claro nunca salen del módulo? / R: Porque la CVK viaja cifrada bajo LMK (CVK_LMK) y se envía al HSM junto al dato CVV; el HSM descifra la CVK internamente y valida, sin exponer la clave en claro. (Sección: Gestión de claves con módulos de seguridad hardware)

P: ¿Por qué las claves DES de longitud simple no son PCI DSS compliant? / R: Porque la "criptografía fuerte" de PCI DSS exige un mínimo efectivo de 112 bits; las simples no lo alcanzan y solo deberían usarse, si acaso, en desarrollo/pruebas, y los HSM prohíben claves simples disfrazadas de doble/triple. (Sección: Gestión de claves con módulos de seguridad hardware)

P: ¿Cuáles son los dos pasos para establecer una zona de confianza entre dos HSM? / R: Primero compartir una ZMK mediante componentes en claro que cada parte combina bajo su LMK; después generar e intercambiar las worker keys (ZPK/AWK), enviando la versión cifrada bajo ZMK. (Sección: Zonas de confianza y componentes de clave)

P: ¿Cómo confirma el receptor que un componente de clave llegó íntegro en la ceremonia de claves? / R: Recombina los componentes mediante XOR y compara el key check value (KCV); si un sobre muestra manipulación, no coincide con el manifiesto o el número de serie es erróneo, la clave se considera comprometida y se reinicia. (Sección: Custodios y ceremonia de claves)

## Puntos a dominar

- Distinguir CHD de SAD y recordar la regla de almacenamiento: el CHD puede guardarse con el PAN ilegible; el SAD nunca, ni siquiera cifrado.
- Explicar la diferencia entre certificación (QSA/ROC o SAQ/AOC) y los "niveles" que fijan los esquemas según volumen de transacciones.
- Identificar qué SAQ corresponde a cada entorno (A, A-EP, B, B-IP, C, C-VT, P2PE, D) y por qué almacenar CHD lleva al SAQ D.
- Enumerar los seis principios de PCI DSS y asociar cada uno de los doce requisitos a su principio.
- Diferenciar el alcance de PCI DSS (sistemas completos) frente a PCI PA DSS (aplicación individual) y el valor de la certificación PA DSS para acortar la auditoría.
- Describir la jerarquía de claves del HSM: LMK protege KEK, y KEK protege data keys; reconocer los tipos de clave (LMK/MFK, ZMK, PIN key, data key).
- Comparar variantes frente a key blocks como mecanismos para limitar el uso de una clave a su propósito.
- Dominar los principios de control dual y conocimiento repartido en la ceremonia de claves con al menos tres custodios de departamentos distintos.
- Situar PCI PTS v3.0 como 7 control objectives y 33 requisitos para la protección de PIN.
