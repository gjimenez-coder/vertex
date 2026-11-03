# Securing Third-Party Dependencies (Protegiendo las dependencias de terceros) — Estudio

## Tarjetas de repaso

P: ¿Qué son las fourth-party dependencies? / R: Las propias dependencias que arrastra una dependencia de terceros; el conjunto completo forma el dependency tree.

P: ¿Qué es un dependency tree? / R: El conjunto de una dependencia, sus dependencias, las dependencias de esas, etc.; en apps grandes alcanza miles o decenas de miles de subdependencias y versiones únicas.

P: ¿Qué comando de npm lista el árbol completo de dependencias? / R: `npm ls`, que revela cuántas subdependencias tiene realmente la aplicación, muchas que nunca consideras conscientemente.

P: ¿Por qué no basta con evaluar cada dependencia única? / R: Porque hay que evaluar también cada versión única: la 2.2.1 puede tener vulnerabilidades críticas que la 3.4.0 no tiene.

P: ¿Por qué la evaluación manual no escala? / R: Es prácticamente imposible revisar de forma exhaustiva una dependencia que depende de otras que a su vez dependen de otras, en cadenas de miles de elementos.

P: ¿Cómo se empieza a encontrar vulnerabilidades de forma automatizada? / R: Comparando el árbol contra una base de datos de CVE conocida, con un escáner como Snyk o un script propio que convierta el árbol en lista.

P: ¿Qué base de datos de CVE sugiere empezar el libro y por qué? / R: La del NIST, por longevidad, ya que está financiada por el gobierno de EE. UU. y es probable que perdure.

P: ¿En qué consiste la separación de responsabilidades (separation of concerns)? / R: Ejecutar la dependencia en su propio servidor (idealmente mantenido por tu organización) y comunicarte vía HTTP enviando y recibiendo payloads JSON.

P: ¿Qué garantiza usar JSON en la comunicación con el servidor de la dependencia? / R: Que no es posible ejecutar scripts en el servidor de aplicación sin vulnerabilidades adicionales (vulnerability chaining), tratando la dependencia casi como una "pure function".

P: ¿Qué desventajas tiene aislar una dependencia en su propio servidor? / R: Pérdida de rendimiento por mayor tiempo de tránsito, y los datos confidenciales podrían modificarse o registrarse si el paquete está comprometido y el firewall mal configurado.

P: ¿Qué significan los tres números del semantic versioning? / R: Major, minor y patch; por defecto los gestores mantienen la dependencia en el último patch.

P: ¿Qué hace el caret (`^`) en npm y cómo se fija la versión exacta? / R: El `^` mantiene el último patch (`^1.0.24`); al quitarlo se fija la versión exacta (`1.0.24`).

P: ¿Qué limitación tiene el version-locking de nivel superior? / R: Solo aplica a la dependencia de nivel superior, no a las descendientes, y no protege si el mantenedor reutiliza un número de versión existente.

P: ¿Qué hace `npm shrinkwrap`? / R: Genera `npm-shrinkwrap.json`, que fija la versión exacta de cada dependencia y subdependencia del árbol.

P: ¿Cómo se elimina el riesgo de reutilización de número de versión? / R: Modificando el shrinkwrap para referenciar Git SHAs o desplegando tu propio npm mirror con las versiones correctas.

## Preguntas de autoevaluación

P: ¿Cuál es la tesis central del capítulo sobre el riesgo de las dependencias de terceros? / R: Toda integración de terceros trae un riesgo aceptado a cambio de ahorrar tiempo de desarrollo; ese riesgo no se elimina pero sí se mitiga. (Lo que necesitas saber)

P: ¿Qué doble valor tiene modelar un árbol de dependencias? / R: En ingeniería de software permite reducir tamaño de archivo y memoria (p. ej. importar JQuery una sola vez); en ingeniería de seguridad es necesario para poder evaluar cada dependencia del first-party. (Modelar un árbol de dependencias)

P: ¿Por qué un árbol real casi nunca usa la misma versión de una dependencia en todos sus componentes? / R: Porque cada eslabón depende de detalles de implementación que cambian entre versiones y cada organización tiene su propia filosofía de actualización. (Los árboles de dependencias en el mundo real)

P: ¿Cómo debe evaluarse una cadena de diez mil elementos y por qué? / R: De forma automatizada: cargada en memoria con estructura de árbol, iterar sobre ella es simple y eficiente; toda dependencia y sus subárboles deben evaluarse automáticamente al incorporarse. (Evaluación automatizada)

P: ¿Cuáles son las dos grandes estrategias de integración segura que presenta el capítulo? / R: La separación de responsabilidades (aislar la dependencia en su propio servidor o entorno) y la gestión segura de paquetes (version-locking, shrinkwrapping y Git SHAs o un mirror propio). (Técnicas de integración segura)

P: ¿Por qué el version-locking por sí solo no basta para proteger el árbol completo? / R: Porque solo aplica a la dependencia de nivel superior y no a las descendientes, y no protege si el mantenedor despliega código nuevo reutilizando un número de versión existente. (Gestión segura de paquetes)

P: ¿Qué principio de seguridad fundamenta ejecutar dependencias en su propio servidor o entorno aislado? / R: El principle of least authority / least privilege; aislar reduce el impacto de un bug grave o un script malicioso sobre la aplicación principal. (Separación de responsabilidades / Resumen del capítulo)

## Checklist

- [ ] Ejecutar `npm ls` para listar el árbol completo de dependencias y descubrir subdependencias no consideradas.
- [ ] Modelar el árbol para identificar cada dependencia única y cada versión única a evaluar.
- [ ] Evaluar el árbol de forma automatizada comparándolo contra una base de datos de CVE (Snyk o script propio), empezando por la del NIST; usar `npm list --depth=[depth]`.
- [ ] Cuando sea posible, aislar las dependencias en su propio servidor o entorno y comunicarse vía HTTP con payloads JSON, sin persistir estado en el servidor de la dependencia.
- [ ] Verificar la configuración del firewall del servidor de la dependencia para proteger los datos confidenciales en tránsito.
- [ ] Auditar la versión concreta de cada dependencia acoplada al core y fijar la versión exacta quitando el caret (`^`) en npm.
- [ ] Ejecutar `npm shrinkwrap` para fijar la versión exacta de todo el árbol.
- [ ] Para eliminar el riesgo de reutilización de número de versión, referenciar Git SHAs en el shrinkwrap o desplegar un npm mirror propio.
