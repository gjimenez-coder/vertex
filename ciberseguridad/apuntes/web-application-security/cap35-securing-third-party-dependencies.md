# Web Application Security (2nd Edition) — Andrew Hoffman (O'Reilly Media, 2024)
## Capítulo 35 — Securing Third-Party Dependencies (Protegiendo las dependencias de terceros)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF y las citas usan la página del PDF.

## Lo que necesitas saber
Este capítulo pertenece a la Parte III (técnicas defensivas) y cierra el hilo iniciado en capítulos anteriores: el Capítulo 6 enseñó a identificar dependencias de terceros en una aplicación first-party y el Capítulo 17 analizó cómo se integran y qué vectores de ataque abren. Aquí el objetivo es defensivo: proteger tu aplicación de las vulnerabilidades que surgen al integrar third-party dependencies.

La tesis central es que toda integración de terceros trae consigo un riesgo aceptado a cambio de ahorrar tiempo de desarrollo, y que ese riesgo no se elimina pero sí se mitiga. El problema se agrava porque cada dependencia suele tener sus propias dependencias (fourth-party dependencies), formando un dependency tree que puede llegar a miles o decenas de miles de subdependencias y versiones únicas en una aplicación grande.

Sales sabiendo cómo modelar y evaluar árboles de dependencias de forma automatizada (comparándolos contra bases de datos de CVE), y conociendo las dos grandes estrategias de integración segura: la separación de responsabilidades (aislar la dependencia en su propio servidor o entorno) y la gestión segura de paquetes (version-locking, shrinkwrapping y referencias a Git SHA o un mirror propio).

## Evaluación de árboles de dependencias (dependency trees)
Una dependencia de terceros rara vez está sola: arrastra sus propias dependencias, a veces llamadas fourth-party dependencies. Evaluar manualmente a nivel de código una única dependencia sin subdependencias es viable e incluso ideal en muchos casos, pero las revisiones manuales no escalan: es prácticamente imposible revisar de forma exhaustiva una dependencia que depende de otras, que a su vez dependen de otras.

El conjunto de una dependencia, sus dependencias, las dependencias de esas, etc., forma el dependency tree. En un proyecto npm, el comando `npm ls` lista el árbol completo y revela cuántas subdependencias tiene realmente la aplicación, muchas de las cuales nunca consideras conscientemente.

### Modelar un árbol de dependencias
Modelar el árbol tiene valor doble. En ingeniería de software permite reducir tamaño de archivo y memoria. Por ejemplo:

```
Primary Application → JQuery
Primary Application → SPA Framework → JQuery
Primary Application → UI Component Library → JQuery
```

Si tres partes del árbol dependen de JQuery, puede importarse una sola vez en lugar de tres (evitando almacenamiento redundante). En ingeniería de seguridad, sin un modelado correcto es muy difícil evaluar cada dependencia del first-party.

### Los árboles de dependencias en el mundo real
En un mundo ideal cada componente usaría la misma versión de una dependencia, pero en la práctica casi nunca ocurre. Una aplicación first-party puede estandarizar versiones internamente, pero difícilmente lo logre con el resto de la cadena, porque cada eslabón depende de detalles de implementación que cambian entre versiones y cada organización tiene su propia filosofía de actualización. Un árbol real se parece más a:

```
Primary Application v1.6 → JQuery 3.4.0
Primary Application v1.6 → SPA Framework v1.3.2 → JQuery v2.2.1
Primary Application v1.6 → UI Component Library v4.5.0 → JQuery v2.2.1
```

La versión 2.2.1 puede tener vulnerabilidades críticas que la 3.4.0 no tiene. Por eso hay que evaluar cada dependencia única y además cada versión única de cada dependencia.

## Evaluación automatizada (Automated Evaluation)
Una cadena de diez mil elementos es imposible de evaluar manualmente, así que el árbol debe evaluarse de forma automatizada. Si se carga en memoria con una estructura de árbol, iterar sobre él resulta simple y eficiente; toda dependencia y sus subárboles deben evaluarse automáticamente al incorporarse.

La forma más fácil de empezar a encontrar vulnerabilidades es comparar el árbol contra una base de datos de CVE conocida, que alojan listas y reproducciones de vulnerabilidades halladas en paquetes OSS y de terceros. Se puede usar un escáner como Snyk o un script propio que convierta el árbol en una lista y la compare con una base de datos remota. En npm el proceso puede arrancar con:

```
npm list --depth=[depth]
```

Entre las bases de datos disponibles, el libro sugiere empezar por la del NIST por longevidad, ya que está financiada por el gobierno de EE. UU. y es probable que perdure.

## Técnicas de integración segura (Secure Integration Techniques)
Mientras que en "Methods of Integration" se analizaron las integraciones desde la óptica del observador o atacante, aquí se adopta la perspectiva del propietario de la aplicación: ¿cuáles son las formas más seguras de integrar una dependencia de terceros?

### Separación de responsabilidades (Separation of Concerns)
Un riesgo de integrar código de terceros en tu servidor principal es que ese código tenga efectos secundarios o, si se ve comprometido, llegue a tomar recursos y funcionalidad del sistema cuando no se aplica correctamente el principle of least authority. Una mitigación es ejecutar la integración en su propio servidor (idealmente mantenido por tu organización) y comunicarte con él vía HTTP enviando y recibiendo payloads JSON.

El formato JSON garantiza que no es posible ejecutar scripts en el servidor de aplicación sin vulnerabilidades adicionales (vulnerability chaining) y permite tratar la dependencia casi como una "pure function", siempre que no persistas estado en el servidor de la dependencia. Advertencias: los datos confidenciales enviados al servidor de la dependencia podrían ser modificados o registrados si el paquete está comprometido y el firewall está mal configurado; además hay pérdida de rendimiento por el mayor tiempo de tránsito. El mismo concepto puede aplicarse en un solo servidor usando módulos con límites de proceso y memoria definidos por hardware, de modo que un paquete "riesgoso" no alcance los recursos de la aplicación principal.

### Gestión segura de paquetes (Secure Package Management)
Sistemas como npm o Maven implican un riesgo aceptado según sus límites y su revisión de publicación. Una mitigación es auditar versiones concretas de la dependencia y "bloquear" (lock) la versión semántica a la auditada.

El semantic versioning usa tres números: major, minor y patch. Por defecto, los gestores intentan mantener la dependencia en el último patch; así, `myLib 1.0.23` podría actualizarse a `myLib 1.0.24` sin que lo sepas. npm antepone un caret (`^`) por defecto; al quitarlo se fija la versión exacta:

```
1.0.24   (versión exacta)
^1.0.24  (último patch)
```

Esta técnica no protege si el mantenedor despliega código nuevo reutilizando un número de versión existente (la regla "nuevo código → nuevo número de versión" depende del mantenedor), y solo aplica a la dependencia de nivel superior, no a las descendientes.

Ahí entra el shrinkwrapping. Ejecutar `npm shrinkwrap` genera un archivo `npm-shrinkwrap.json` que fija la versión exacta de cada dependencia y subdependencia del árbol. Esto elimina el riesgo de que una dependencia se actualice al último patch y arrastre código vulnerable, pero no el raro caso de reutilización de número de versión. Para eliminar ese riesgo, modifica el shrinkwrap para referenciar Git SHAs o despliega tu propio npm mirror con las versiones correctas.

## Resumen del capítulo
Las aplicaciones web actuales tienen miles de dependencias, y asegurar cada script es una tarea enorme; debe asumirse que toda integración de terceros conlleva algún riesgo esperado. Aplicando el principle of least privilege, dependencias concretas pueden correr en su propio servidor o entorno aislado, reduciendo el impacto de un bug grave o un script malicioso, aunque para algunas la aislación es difícil o imposible. Las dependencias muy acopladas al core deben evaluarse de forma independiente en un número de versión concreto y, si vienen por un gestor como npm, version-lock + shrinkwrap, con Git SHAs o un mirror propio para mayor seguridad. Las mismas técnicas aplican a gestores de paquetes de otros lenguajes.

## Ideas clave
- Una dependencia arrastra fourth-party dependencies; el conjunto forma un dependency tree que en apps grandes alcanza miles o decenas de miles de versiones únicas.
- `npm ls` lista el árbol completo y revela subdependencias que normalmente no consideras.
- Hay que evaluar cada dependencia única y cada versión única: la 2.2.1 puede ser vulnerable aunque la 3.4.0 no lo sea.
- La evaluación manual no escala; automatiza comparando el árbol contra una base de datos de CVE (Snyk o script propio); el libro sugiere empezar por la del NIST.
- Separación de responsabilidades: ejecuta la dependencia en su propio servidor y comunícate vía HTTP/JSON para evitar ejecución de scripts y tratarla como "pure function".
- Aislar reduce el riesgo en el servidor principal, pero añade latencia y los datos confidenciales siguen expuestos si el paquete está comprometido.
- El caret (`^`) de npm mantiene el último patch; quitarlo fija la versión exacta, pero solo protege la dependencia de nivel superior.
- `npm shrinkwrap` fija todo el árbol; para el riesgo de reutilización de versión, usa Git SHAs o un npm mirror propio.
