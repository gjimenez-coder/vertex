# Web Application Security (2nd Edition) — Andrew Hoffman (O'Reilly Media, 2024)
## Capítulo 7 — Identifying Weak Points in Application Architecture (Identificación de puntos débiles en la arquitectura de la aplicación)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas indican la página del PDF.

## Lo que necesitas saber

El capítulo cierra la fase de reconocimiento (recon) uniendo todo lo recopilado antes —tecnologías, API endpoints, funcionalidad, dominios, configuraciones y sistemas de autenticación/sesión— en un conjunto de notas organizado que permite priorizar dónde buscar vulnerabilidades. La documentación es clave: aplicaciones muy grandes pueden requerir meses de exploración, y aunque más datos es mejor que ninguno, el valor depende de priorizar correctamente.

La tesis central va contra la creencia popular: la mayoría de las vulnerabilidades no surgen de métodos mal escritos, sino de una arquitectura de aplicación mal diseñada. Un solo XSS puede ser un método descuidado, pero vulnerabilidades múltiples delatan arquitectura débil. La arquitectura de la aplicación y la de sus módulos/dependencias son excelentes marcadores de puntos débiles.

Sales sabiendo reconocer señales de arquitectura segura frente a insegura, entender por qué la defensa debe aplicarse en múltiples capas, y evaluar el riesgo de "reinventar" tecnología existente. El análisis arquitectónico es una técnica de recon útil: las funcionalidades mal arquitecturadas deben atacarse primero, porque las bien diseñadas se mantienen consistentes al saltar de un endpoint a otro.

## El ejemplo que recorre el capítulo

El hilo conductor es una aplicación de mensajería directa (IM) entre usuarios, usada para comparar una versión segura y una insegura. El autor plantea que si un desarrollador escribe 10 variaciones del sistema de IM a lo largo de 5 años, cada implementación será estructuralmente distinta, pero los riesgos de seguridad serán en su mayoría los mismos.

Toda versión incluye la misma funcionalidad (PDF p. 143-144):

- UI para escribir un mensaje
- API endpoint que recibe el mensaje enviado
- Tabla de base de datos para almacenar el mensaje
- API endpoint para recuperar uno o más mensajes
- Código UI para mostrar los mensajes

El código mínimo abarca `client/write.html`, `client/send.js`, `server/postMessage.js`, `server/messageModel.js`, `server/getMessage.js`, `client/displayMessage.html` y `client/displayMessage.js`. La versión insegura no rechaza scripts en el POST, ni en la escritura/lectura de base de datos, ni filtra el mensaje, de modo que termina cargándose en el DOM como `message <script> alert('hacked');</script>` y se ejecuta.

## Señales de arquitectura segura vs. insegura

La diferencia no es escribir protecciones caso por caso (costoso en tiempo de desarrollo y fácil de pasar por alto), sino abstraer los mecanismos de seguridad dentro de la arquitectura. Una aplicación segura implementa seguridad antes y durante el desarrollo de features; una mediocre lo hace en el momento del feature; una insegura puede no implementar nada.

> "Even an application written by engineers skilled in application security would likely have security holes eventually if its application architecture was inherently insecure." (PDF p. 143)

Ejemplo de mecanismo que elimina la mayor parte del riesgo de XSS, construido en la UI usando DOMPurify:

```javascript
import { DOMPurify } from '../utils/DOMPurify';

// makes use of: https://github.com/cure53/DOMPurify
const appendToDOM = function(data, selector, unsafe = false) {
  const element = document.querySelector(selector);

  // for cases where DOM injection is required (not default)
  if (unsafe) {
   element.innerHTML = DOMPurify.sanitize(data);
  } else { // standard cases (default)
   element.innerText = data;
  }
};
```

La implementación importa: el flag `unsafe` está desactivado por defecto y es el último parámetro de la firma, así es poco probable activarlo por accidente. Métodos como `appendToDOM` son indicadores de arquitectura segura; su ausencia hace más probable la presencia de vulnerabilidades.

## Múltiples capas de seguridad

En el servicio de mensajería, el riesgo de XSS podía aparecer en varias capas (PDF p. 149):

- API POST
- Database Write
- Database Read
- API GET
- Client Read

Lo mismo aplica a otros ataques como XXE o CSRF: cada uno puede surgir por mecanismos insuficientes en más de una capa. Si solo se sanitiza en el API POST, un nuevo endpoint (por ejemplo, uno de mensajería masiva que acepta listas de mensajes) con menos saneamiento podría introducir scripts en la base de datos, saltándose la protección original.

> "an application is only as secure as the weakest link in its architecture." (PDF p. 149)

Distintas capas admiten distintos mecanismos: el API POST podría invocar un headless browser para simular el renderizado y rechazar el payload si detecta ejecución de script, algo imposible en la capa de base de datos o cliente. Pero cada mecanismo detecta payloads diferentes; un bug en una API específica del headless browser podría permitir que el script pase y solo se ejecute en el navegador vulnerable de un usuario real.

Conclusión: las aplicaciones más seguras introducen mecanismos en muchas capas; las inseguras, en solo una o dos. Al testear, busca funcionalidad con pocos mecanismos de seguridad o con muchas capas (baja proporción de mecanismos por capa): es más probable que sea explotable y debe priorizarse.

## Adopción y reinvención

Un último factor de riesgo es el deseo de reinventar tecnología existente. No suele nacer como problema de arquitectura, sino organizativo, pero se refleja en la arquitectura. Reinventar tiene ventajas: evitar licencias complicadas, añadir funcionalidad extra y generar publicidad; además suele ser más entretenido que reutilizar una herramienta existente. No siempre es malo, así que cada caso se evalúa individualmente (p. ej., licencias con comisiones que dan márgenes negativos o que prohíben alteraciones esenciales).

Desde la seguridad, reinventar es riesgoso, con riesgo que va de moderado a extremo según la funcionalidad. La regla de oro: nunca implementar tu propia criptografía ("never rolling your own cryptography", PDF p. 150). SHA-3 es un algoritmo de hashing open source de la familia SHA, en desarrollo durante casi 20 años, probado robustamente por el NIST y por las mayores firmas de seguridad de EE. UU. Los hashes son atacados constantemente (combinator attacks, Markov attacks, etc.); replicar ese nivel de pruebas costaría decenas de millones de dólares, mientras que por cero dólares se puede adoptar una implementación de SHA-3 de una fuente como OpenJDK y obtener todos los beneficios de ese testing.

Criterio para decidir qué adoptar y qué reinventar: una aplicación bien arquitecturada solo reinventa features puramente funcionales (un esquema para almacenar comentarios, un sistema de notificaciones). Las funcionalidades que requieren experiencia profunda en matemáticas, sistemas operativos o hardware —bases de datos, aislamiento de procesos, gestión de memoria— deben dejarse en paz. Las aplicaciones llenas de bases de datos, criptografía y optimizaciones de hardware a medida suelen ser las más fáciles de vulnerar.

## Ideas clave

- Reúne las notas de recon (tecnologías, endpoints por verbo HTTP, shapes de API, funcionalidad, dominios, configuraciones, auth/sesión) para priorizar dónde atacar.
- La mayoría de vulnerabilidades provienen de arquitectura mal diseñada, no de métodos mal escritos; múltiples vulnerabilidades indican arquitectura débil.
- La seguridad debe abstraerse en la arquitectura, no implementarse caso por caso; mecanismos como `appendToDOM` (con `unsafe` desactivado por defecto) señalan arquitectura segura.
- Una aplicación es tan segura como su eslabón más débil; defender en una sola capa deja hueco a nuevos endpoints menos protegidos.
- Las aplicaciones seguras aplican mecanismos en muchas capas (API POST, DB Write/Read, API GET, Client Read); prioriza las funcionalidades con baja proporción de mecanismos por capa.
- Distintas capas y mecanismos (p. ej., headless browser en el POST) detectan distintos payloads; ninguno es infalible por sí solo.
- Reinventar tecnología es sobre todo un problema organizativo con impacto en seguridad; nunca implementes tu propia criptografía (usa SHA-3 probado por NIST, vía OpenJDK).
- Reinventa solo features puramente funcionales; deja bases de datos, aislamiento de procesos, gestión de memoria y cripto a los expertos.
