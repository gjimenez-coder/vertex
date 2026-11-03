# Web Application Security (2nd Edition) — Andrew Hoffman (O'Reilly Media, 2024)
## Capítulo 9 — Introduction to Hacking Web Applications (Introducción al hacking de aplicaciones web)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas usan la página del PDF.

## Lo que necesitas saber

Este capítulo abre la Parte II del libro y hace de puente entre las habilidades de reconocimiento (recon) de la Parte I y las técnicas ofensivas que vienen a continuación. Su tesis es sencilla: recon y hacking van de la mano, y juntos valen mucho más que por separado. Aquí no se enseñan exploits todavía, sino la mentalidad y el enfoque con los que se debe abordar el ataque a una aplicación web.

El objetivo de la Parte II es aprender a explotar vulnerabilidades construyendo y desplegando payloads contra la aplicación hipotética del libro, mega-bank.com, usando exploits comunes y presentes en muchas aplicaciones actuales. El autor subraya que estas habilidades son transferibles a otras aplicaciones siempre que se combinen con las técnicas de la Parte I.

Sales sabiendo dos cosas: en qué consiste "la mentalidad del hacker" y por qué cada pieza del reconocimiento (tipo de API, endpoints, esquema de autenticación, dependencias de terceros y arquitectura) será directamente aprovechable en la fase ofensiva. Al final de la Parte II tendrás tanto las habilidades de recon para encontrar bugs explotables como las habilidades ofensivas para construir y desplegar payloads que los aprovechen.

## El ejemplo que recorre el capítulo

El hilo conductor es la aplicación hipotética mega-bank.com, presentada en la Parte I, que será el blanco de los ataques en los capítulos siguientes. El capítulo la usa como referencia para explicar cómo se encadenan recon y explotación, aunque todavía no desarrolla ataques concretos sobre ella.

## The Hacker's Mindset (La mentalidad del hacker)

Ser un hacker exitoso requiere más que habilidades medibles: requiere una mentalidad particular. El autor la contrasta con la del ingeniero de software, que mide su productividad en valor añadido (features o mejoras de rendimiento), algo cuantificable. El hacker, en cambio, mide su productividad de forma mucho más difícil de discernir, porque la mayor parte del hacking es recolección y análisis de datos, un proceso plagado de falsos positivos que a un observador no formado puede parecerle tiempo perdido.

La mayoría de los hackers no deconstruyen ni modifican el software, sino que lo analizan para trabajar con el código existente, buscando puntos de entrada en lugar de crearlos. Las habilidades para ese análisis son similares, si no idénticas, a las de la primera parte del libro.

Todo código está lleno de bugs potencialmente explotables, y un buen hacker está siempre atento a pistas que lleven a una vulnerabilidad. El trabajo es lento: se pueden pasar semanas o meses analizando una aplicación antes de encontrar un punto de entrada adecuado y diseñar y entregar un exploit. Por eso son cruciales dos hábitos: reforzar constantemente la importancia de encontrar y entregar un payload, y llevar un registro detallado de los intentos previos y sus lecciones aprendidas, algo que gana importancia al pasar de aplicaciones pequeñas a aplicaciones grandes con funcionalidad o datos clave como objetivo.

El hacker también debe aprender y mejorar de forma continua, porque las técnicas antiguas pierden valor a medida que la web se adapta. El capítulo cierra esta sección con una progresión:

> "A hacker is first and foremost a detective." (PDF p. 157)

Un buen hacker es un detective bien organizado; un gran hacker suma excelente conocimiento y habilidad técnica; y un hacker maestro, además de todo lo anterior, aprende y adapta constantemente su conjunto de habilidades frente a quienes intentan frenarlo.

## Applied Recon (Reconocimiento aplicado)

La Parte I enseñó a explorar una aplicación web y conocer su tecnología y estructura; la Parte II trata de aprovechar los agujeros de seguridad de esas mismas aplicaciones. Las lecciones de recon no deben olvidarse porque serán decisivas en la explotación. Los puntos concretos que el capítulo conecta:

- Tipo de API: la mayoría de las aplicaciones web modernas usan REST APIs, y los ejemplos de los capítulos siguientes consisten mayormente en enviar un payload sobre una REST API. Saber determinar el tipo de API del objetivo será importante.
- Descubrimiento de endpoints: con registros públicos y scripts de red se descubren endpoints de API no documentados. Un mismo exploit puede probarse contra varias aplicaciones del mismo propietario, ya que por reutilización de código un exploit encontrado en una aplicación puede replicarse en aplicaciones internas. Además, endpoints con payloads de estructura similar pueden rendir resultados distintos: quizá un ataque contra `/users/1234/friends` no devuelva datos sensibles, pero `/users/1234/settings` sí.
- Esquema de autenticación: la mayoría de aplicaciones ofrecen a los usuarios autenticados un superconjunto de la funcionalidad de invitado. Con un token de autenticación aumenta el número de APIs atacables y, probablemente, los privilegios de los procesos que ejecutan esas peticiones.
- Dependencias de terceros (a menudo OSS): en esta parte se aprenderá a encontrar y personalizar exploits públicamente documentados contra dependencias de terceros, e incluso a hallar agujeros surgidos de la integración entre código propio y código de terceros.
- Arquitectura de la aplicación: puede que la aplicación A no sea explotable pero la B sí. Si no se puede desplegar un exploit directamente sobre B, se puede estudiar cómo A se comunica con B para entregar el payload a A y que luego llegue a B.

La conclusión del capítulo reitera que las habilidades de recon de los capítulos previos y las de hacking de los siguientes van de la mano y son mucho más valiosas combinadas.

## Ideas clave

- La Parte II construye sobre el recon de la Parte I para explotar vulnerabilidades; recon y hacking se refuerzan mutuamente.
- Todos los ataques se practican sobre la aplicación hipotética mega-bank.com con exploits comunes y transferibles.
- La mentalidad del hacker se basa en análisis y recolección de datos, no en modificar el software: se buscan puntos de entrada, no se crean.
- El hacking exige paciencia (semanas o meses sin éxito) y disciplina para registrar intentos y lecciones aprendidas.
- Un hacker es ante todo un detective; el nivel sube con organización, conocimiento técnico y aprendizaje continuo.
- Identificar el tipo de API (REST en la mayoría de casos) es clave porque los exploits se entregan como payloads sobre esa API.
- El descubrimiento de endpoints y la reutilización de código permiten replicar un exploit en varias aplicaciones del mismo propietario.
- Un token de autenticación amplía la superficie de ataque y los privilegios; las dependencias de terceros y la arquitectura abren vías adicionales de explotación.
