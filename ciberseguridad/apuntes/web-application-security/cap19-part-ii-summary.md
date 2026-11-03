# Web Application Security (2nd Edition) — Andrew Hoffman (O'Reilly Media, 2024)
## Capítulo 19 — Part II Summary (Resumen de la Parte II)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF y las citas usan la página del PDF.

## Lo que necesitas saber
Este capítulo cierra la Parte II del libro (la dedicada al ataque u offensive hacking) con una reflexión breve sobre lo aprendido y cómo aplicarlo en el mundo real. La tesis central es que probar a fondo una aplicación web exige tres cosas combinadas: conocimiento de los arquetipos de vulnerabilidad más comunes, pensamiento crítico y conocimiento del dominio (domain knowledge). Solo con esa combinación se pueden hallar las vulnerabilidades de lógica profunda que quedan fuera de los arquetipos habituales.

El autor insiste en que las habilidades de las Partes I y II bastan para empezar en cualquier proyecto de pen-testing de aplicaciones web. A partir de aquí, la clave está en atender al modelo de negocio: todas las aplicaciones corren riesgo frente a vulnerabilidades como XSS, CSRF o XXE, pero solo entendiendo a fondo la lógica de negocio subyacente se identifican fallos más avanzados y específicos de cada aplicación.

También advierte que, si estos ataques parecen difíciles de aplicar en un escenario real, lo más probable no es que la aplicación esté perfectamente endurecida, sino que haga falta mejorar las habilidades de recon para localizar los puntos débiles donde desplegarlos con éxito. Sales sabiendo cómo encadenar recon y técnicas ofensivas, y con la mentalidad adecuada para afrontar la Parte III sobre defensas.

## Puente hacia la Parte III (defensas)
- Las habilidades de la Parte II se apoyan directamente en las de la Parte I y preparan la Parte III, centrada en los mecanismos defensivos.
- Al estudiar las defensas conviene pensar continuamente cómo un atacante encontraría y explotaría una aplicación con y sin defensas adecuadas.
- Las defensas web suelen estar rotas, por eso se las llama a menudo "mitigaciones" en lugar de "arreglos": *"web application defenses are often broken... referred to as 'mitigations' rather than 'fixes'"* (PDF p. 282).
- Con lo aprendido en las Partes I y II puede ser posible saltarse o debilitar defensas concretas de la Parte III.
- Las defensas de la Parte III son en su mayoría best practices del sector, pero muchas no son infalibles: conviene combinar varias defensas en lugar de depender de una sola.

## Ética y uso responsable
- Las técnicas de la Parte II son peligrosas: son ataques reales usados por atacantes reales de forma habitual.
- Se pueden probar contra aplicaciones propias, pero nunca contra aplicaciones de terceros sin permiso escrito explícito del propietario.
- Las técnicas sirven tanto para el bien como para el mal, por lo que su aplicación debe meditarse a fondo y no desplegarse a la ligera.
- Varias técnicas pueden comprometer servidores o máquinas cliente incluso con permiso del propietario; hay que considerar el impacto de cada ataque y asegurarse de que el propietario entiende los riesgos del live testing antes de empezar.

## Ideas clave
- El testing exhaustivo requiere arquetipos de vulnerabilidad + pensamiento crítico + conocimiento del dominio.
- Las habilidades fundacionales de las Partes I y II bastan para arrancar en proyectos de pen-testing.
- Toda aplicación es vulnerable a XSS, CSRF o XXE, pero las fallas avanzadas se hallan entendiendo el modelo y la lógica de negocio.
- Si los ataques cuestan en lo real, suele faltar recon más que sobrar hardening.
- La Parte II se construye sobre la Parte I y prepara la Parte III de defensas.
- Las defensas se llaman "mitigaciones" porque a menudo se pueden romper; combínalas en vez de confiar en una sola.
- Prueba estos ataques solo con permiso escrito explícito del propietario; pueden comprometer servidores y clientes.
