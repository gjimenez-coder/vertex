# Web Application Security (2nd Edition) — Andrew Hoffman (O'Reilly Media, 2024)
## Capítulo 1 — The History of Software Security (La historia de la seguridad del software)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF y las citas usan la página del PDF.

## Lo que necesitas saber
El capítulo recorre unos cien años de historia de la seguridad del software para dar contexto antes de entrar en técnicas ofensivas y defensivas. La tesis central es que existe una relación cíclica y continua entre hackers que buscan romper los mecanismos de seguridad y los ingenieros que los diseñan: cada vez que una capa se vuelve más segura, los atacantes migran a una nueva superficie de ataque.

El autor aclara que no es historiador sino profesional de seguridad, y que el recorrido es una referencia de eventos críticos, no una cronología exhaustiva. La línea de tiempo empieza en los años 1930 con la máquina Enigma y llega hasta las aplicaciones web modernas.

Sales sabiendo cómo el cifrado, la automatización del hacking, el phreaking telefónico, los virus informáticos y la llegada de la Web 2.0 fueron moldeando tanto las defensas como las técnicas de ataque. También queda clara una lección de diseño recurrente: siempre hay que considerar el peor escenario, no el mejor, al diseñar sistemas a escala.

## El ejemplo que recorre el capítulo
El hilo conductor es una línea de tiempo de eventos históricos. Cada era aporta una lección que sigue vigente hoy: el cifrado simétrico (Enigma), la automatización del descifrado (Turing), el abuso de sistemas mal diseñados (phreaking), la propagación y camuflaje de código malicioso (virus) y el giro hacia atacar al usuario y la aplicación (Web 2.0).

## Los orígenes del hacking
Aunque el hacking ganó notoriedad con la World Wide Web, existe desde mediados del siglo XX e incluso antes. En los años 1910 y 1920 hubo incidentes aislados que hoy calificarían como hacking, en su mayoría manipulando emisores y receptores de código Morse o interfiriendo ondas de radio, aunque no eran comunes ni a gran escala.

## La máquina Enigma, hacia 1930
Enigma usaba rotores mecánicos eléctricos para cifrar y descifrar mensajes de texto enviados por radio. De origen alemán, fue popularizada por la empresa Chiffriermaschinen AG y adoptada por el ejército alemán en 1928. Cualquier máquina con una configuración idéntica podía descifrar los mensajes de otra, lo que la hacía muy valiosa para evitar la interceptación.

Hoy esa interceptación de mensajes se conoce como ataque man-in-the-middle. Enigma usaba lo que ahora llamamos un symmetric key algorithm: un cifrado que usa una sola clave para cifrar y descifrar, familia aún empleada para proteger datos en tránsito.

Debilidades y lecciones:
- Una sola configuración comprometida (una private key, en términos actuales) inutilizaba toda la red de máquinas.
- Los logs de configuración se intercambiaban en persona; cuantas más máquinas, mayor probabilidad de fuga o robo.
- Reconfigurar exigía personal especializado y ajuste físico del cableado del plugboard; las actualizaciones solían ser mensuales (diarias en líneas críticas).

En software las claves pueden ser mucho más complejas: un brute force attack con el hardware más rápido podría tardar más de un millón de años, y las claves pueden regenerarse por sesión (login), por request de red o en intervalos programados.

Primeros hackers: en septiembre de 1932 el matemático polaco Marian Rejewski recibió una Enigma robada y configuraciones válidas aportadas por el espía francés Hans-Thilo Schmidt. Junto a Jerzy Różycki y Henryk Zygalski hizo ingeniería inversa del sistema y hacia 1933 descifraban tráfico Enigma a diario. Alemania fue aumentando el número de rotores hasta que el descifrado manual dejó de ser viable en tiempo razonable.

## Descifrado automatizado de Enigma, hacia 1940
Alan Turing, matemático inglés, trabajó desde septiembre de 1938 en la Government Code and Cypher School (GC&CS) en Bletchley Park, junto a su mentor Dilly Knox. Gracias a la colaboración con el Polish Cipher Bureau partieron de la investigación de Marian.

Como el número de rotores crecía (hasta diez veces más), las conjeturas manuales ya no escalaban. Turing buscaba una solución general en lugar de especializada. Una bombe era un dispositivo electromecánico que intentaba revertir automáticamente la posición de los rotores. Las primeras bombes polacas fallaban con máquinas de más de tres rotores.

Turing partió de un supuesto: para diseñar un algoritmo de descifrado hay que conocer una palabra o frase presente en el mensaje y su posición. Aprovechó que el ejército alemán enviaba a diario un parte meteorológico cifrado. Con el budget aprobado construyó una bombe de 108 drums que giraban hasta 120 RPM y probaba cerca de 20.000 configuraciones en 20 minutos.

> "one of the first automated hacking tools ever built" (PDF p. 38)

Esta estrategia se conoce hoy como known plaintext attack (KPA): un algoritmo más eficiente al disponer de pares de entrada/salida previos.

## "Phreaking" telefónico, hacia 1950
A finales de los años 50, telecos como AT&T implementaron el tone dialing: cada tecla emitía una frecuencia de audio interpretada por una máquina en el centro de conmutación, eliminando la conexión manual de cada llamada.

Pronto se descubrió que cualquier sistema basado en interpretar tonos de audio podía manipularse reproduciendo las frecuencias junto al receptor. Los aficionados que lo hacían se llamaron phreakers. El autor sugiere que el término viene de "audio frequency", cercano cronológicamente al tone dialing.

El caso más notorio fue el tono de 2600 Hz, usado internamente por AT&T para señalar fin de llamada (una especie de "admin command"). Emitirlo mantenía el circuito abierto sin registrar la facturación, permitiendo llamadas internacionales gratuitas. Se atribuye a Joe Engressia (que lo silbaba) y a John Draper, quien descubrió que un silbato del cereal Cap'n Crunch imitaba los 2600 Hz. Luego llegó la blue box, que generaba el tono con un botón, y hardware posterior que falsificaba el caller ID y manipulaba teléfonos públicos.

Lección de diseño: los arquitectos solo consideraron al usuario normal, lo que hoy se llama diseño "best-case scenario". La enseñanza es considerar siempre el peor escenario primero.

## Tecnología anti-phreaking, hacia 1960
En los años 60 llegó el dual-tone multifrequency (DTMF), lenguaje de señalización desarrollado por Bell Systems y patentado como "Touch Tones". Cada tecla emitía dos frecuencias simultáneas (una por fila, otra por columna), difíciles de replicar con la voz o un silbato.

```
    1209 Hz 1336 Hz 1477 Hz
697   1       2       3
770   4       5       6
852   7       8       9
941   *       0       #
```

DTMF fue adoptado como estándar por la International Telecommunication Union (ITU) y luego usado también en TV por cable. Aunque los tonos acabaron duplicándose, el esfuerzo era mucho mayor; el paso a entradas digitales (en vez de analógicas) eliminó casi todo el phreaking.

## Los orígenes del hacking informático, hacia 1980
Apple lanzó el Apple 1 en 1976 (unos pocos cientos, requería ensamblaje). En 1982 Commodore International sacó el Commodore 64, listo para usar, que vendió casi 500.000 unidades al mes hasta inicios de los 90.

En 1983 Fred Cohen creó el primer virus informático: se copiaba a sí mismo, se propagaba por floppy disk y se ocultaba dentro de un programa legítimo. Demostró que detectar virus dentro de software válido mediante algoritmos era casi imposible.

En 1988 Robert Morris desplegó el primer virus fuera de un laboratorio, el Morris Worm ("worm" para un virus autorreplicante), que infectó unos 15.000 ordenadores en red el primer día. La GAO estimó el daño en 10.000.000 de dólares; Morris recibió tres años de probation, 400 horas de servicio comunitario y multa de 10.050 dólares, convirtiéndose en el primer hacker condenado en EE. UU.

Paralelismos con hoy: la escalabilidad (saltar de un usuario a otro) y el camuflaje (esconder código malicioso en un programa legítimo) siguen vigentes, aunque ahora el objetivo suele ser el navegador. Hoy los ataques escalan por email, redes sociales o mensajería, y el phishing roba credenciales en sitios idénticos a los de banca o redes sociales. Los navegadores modernos ofrecen sandboxing robusto.

## El auge de la World Wide Web, hacia 2000
En los 90 la web servía casi exclusivamente para compartir documentos HTML, sin apenas inputs del usuario. A inicios de los 2000 los sitios empezaron a almacenar datos enviados por el usuario sobre HTTP y a modificar su funcionamiento según esos inputs: la Web 2.0, que dio origen a blogs, wikis, sitios de medios y redes sociales.

La web pasó de plataforma de documentos a plataforma de distribución de aplicaciones. Con ello, el usuario se volvió el objetivo perfecto para los hackers, justo cuando funciones críticas (comunicaciones militares, transferencias bancarias) migraban a web applications y existían pocos controles de seguridad.

Eventos: los primeros ataques DoS masivos tumbaron Yahoo!, Amazon y eBay; en 2002 el plug-in ActiveX de Microsoft permitió subidas/descargas remotas desde sitios maliciosos; a mediados de los 2000 proliferaron sitios de phishing. Las vulnerabilidades de Cross-Site Scripting (XSS), que ejecutan el código del atacante en la sesión del navegador dentro de un sitio legítimo, se dispararon porque los navegadores aún no tenían defensas.

## Hackers en la era moderna, hacia 2015+
Hacia 2019 (inicio de la primera edición) había miles de webs respaldadas por empresas de miles de millones; muchas (Google, Facebook, Yahoo!, Reddit) obtenían todos sus ingresos de sus sitios. YouTube es un ejemplo de Web 2.0: comentarios, subidas con permisos variables, datos persistentes entre sesiones y mucha lógica en el cliente. Empresas de escritorio migraron a la nube (Adobe Creative Cloud, Microsoft Office web).

Avances de seguridad en navegadores y protocolos:
- Same Origin Policy (SOP): aísla sitios de orígenes distintos; el sitio A no puede acceder al B aunque estén abiertos a la vez o uno esté en un iframe.
- Content Security Policy (CSP): permite al desarrollador fijar niveles de seguridad, como si los scripts pueden ejecutarse inline.
- HTTP adoptó SSL y TLS, que fuerzan cifrado y dificultan los ataques man-in-the-middle.

Como el navegador es más seguro, los hackers más exitosos atacan hoy la lógica escrita por los desarrolladores. Las aplicaciones actuales son más grandes y complejas, con cientos de dependencias open source, integraciones y varias bases de datos, y sus logic bugs son la superficie más explotable.

## Ideas clave
- La seguridad del software y el hacking tienen al menos un siglo de historia; es una relación cíclica entre atacantes e ingenieros.
- Enigma popularizó el cifrado simétrico (symmetric key algorithm) y su debilidad era la gestión de claves; hoy las claves son más complejas y se rotan con frecuencia.
- La bombe de Turing fue una de las primeras herramientas de hacking automatizado y ejemplifica el known plaintext attack (KPA).
- El phreaking (tono 2600 Hz, blue box) enseñó a diseñar para el peor escenario, no el mejor; DTMF fue la respuesta defensiva.
- Fred Cohen creó el primer virus (1983) y el Morris Worm (1988) llevó a la primera condena por hacking en EE. UU.
- La Web 2.0 trasladó el objetivo del servidor y la red hacia el usuario y la aplicación, popularizando phishing, DoS y XSS.
- Defensas modernas del navegador: Same Origin Policy (SOP), Content Security Policy (CSP) y SSL/TLS sobre HTTP.
- Cada nueva tecnología trae su propia superficie de ataque; mantenerse al día con lo nuevo es clave para encontrar agujeros aún no publicados.
