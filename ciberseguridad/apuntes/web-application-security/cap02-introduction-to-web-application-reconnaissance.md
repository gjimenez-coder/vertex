# Web Application Security (2nd Edition) — Andrew Hoffman (O'Reilly Media, 2024)
## Capítulo 2 — Introduction to Web Application Reconnaissance (Introducción al reconocimiento de aplicaciones web)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas usan la página del PDF.

## Lo que necesitas saber
La *web application reconnaissance* (recon) es la fase exploratoria de recopilación de datos que suele ocurrir antes de intentar hackear una aplicación web. La realizan hackers, pen testers o bug bounty hunters, pero también sirve a los security engineers para encontrar mecanismos mal protegidos y parchearlos antes de que lo haga un actor malicioso. El capítulo sostiene que las habilidades de recon por sí solas tienen poco valor, pero se vuelven muy valiosas combinadas con conocimiento ofensivo de hacking y experiencia defensiva en ingeniería de seguridad.

La tesis central es que el recon consiste en construir un entendimiento profundo de una aplicación antes de atacarla, y que una UI pública nunca revela la totalidad de la aplicación: solo expone un subconjunto de la funcionalidad. Mediante recon se pueden descubrir APIs y endpoints destinados a usuarios con permisos elevados (admins, moderadores) que no son visibles desde la interfaz.

Sales sabiendo por qué el recon importa, cómo razonar sobre los distintos niveles de acceso de una aplicación, qué es el modelo de permisos RBAC y cómo documentar los hallazgos construyendo un "mapa" de la aplicación con una estructura jerárquica fácil de recorrer.

## El ejemplo que recorre el capítulo
El hilo conductor es un banco ("MegaBank"). Al abrir una cuenta corriente recibes credenciales para consultar tu cuenta por web, pero la información la introduce manualmente un empleado: alguien tuvo acceso a una aplicación capaz de crear cuentas en las bases de datos del banco. Si pides por teléfono abrir una cuenta de ahorro, un empleado la crea en remoto y queda accesible con tus mismas credenciales, lo que implica otra aplicación que edita cuentas existentes. No puedes cerrar una cuenta online, pero sí en la sucursal.

Como cliente solo tienes acceso de lectura (read-only) al saldo; algunos bancos permiten pagar o transferir, pero ningún cliente puede crear, modificar o eliminar cuentas online. Ese subconjunto limitado de acceso de escritura contrasta con el del personal interno.

| User Type | | Permissions |
|---|---|---|
| Customer | External | Log in to website. Read account balance via web UI. |
| Teller | Internal | Create new accounts when provided paperwork from a customer. |
| Banker | Internal | Modify existing accounts on behalf of customers. |

## Information Gathering (recopilación de información)
El recon se puede lograr de muchas formas. A veces basta con navegar la aplicación y anotar las peticiones de red para familiarizarse con su funcionamiento interno. Pero no todas las aplicaciones tienen una UI que permita explorar visualmente, y aunque exista una UI pública (típica en apps B2C como redes sociales), no hay que asumir que da acceso a toda la interfaz: hasta investigar más, se asume acceso a un subconjunto.

Una advertencia clave del libro: muchas técnicas de recon pueden hacer que tu IP sea marcada (flagged), con bans o incluso acciones legales. "Most recon techniques should only be performed against applications you own or have written permission to test" (PDF p. 52).

No es viable que un banco grande contrate desarrolladores para crear consultas manuales por cada operación sobre una cuenta, así que existe automatización aunque los usuarios externos no puedan acceder a ella. La mayoría de aplicaciones que automatizan el acceso a datos usan estructuras de permisos por niveles: son aplicaciones con *role-based access controlled* (RBAC). Muy pocas aplicaciones actuales usan un único nivel de permisos para todos los usuarios. Ejemplos cotidianos: pedir credenciales de admin al invocar un comando peligroso del SO, o los moderadores de redes sociales con permisos por encima del usuario estándar pero por debajo del admin.

Recorrer solo la UI puede ocultar endpoints de API para usuarios con permisos elevados; con dominio del recon suelen poder encontrarse. Se puede incluso construir un mapa de los permisos de un admin o moderador y compararlo con el de un usuario estándar, descubriendo a veces *glitches* que permiten a usuarios no privilegiados aprovechar funcionalidad reservada a los privilegiados.

El recon también sirve para aplicaciones a las que literalmente no se tiene acceso (una red interna de una escuela, un file server corporativo): no hace falta UI si se sabe hacer reverse engineering de la estructura de las APIs y de los payloads que aceptan. A veces se encuentran servidores o APIs sin protección alguna: olvidar una sola línea de configuración de red o firewall puede exponer un servidor HTTP a una red pública en lugar de confinarlo a la interna. Al construir el mapa de tecnología y arquitectura, además, se pueden priorizar mejor los ataques.

## Web Application Mapping (mapeo de la aplicación web)
Construir un mapa que represente la estructura, organización y funcionalidad de la aplicación debería ser el primer paso antes de intentar hackearla. El término *topography* alude al estudio de las características, formas y superficies del terreno; las aplicaciones web también las tienen, muy distintas de las de la naturaleza. Aquí "mapa" designa los datos recopilados sobre el código, la estructura de red y el conjunto de funcionalidades de una aplicación.

Según la complejidad de la aplicación y la duración de las pruebas, pueden bastar notas simples; para aplicaciones robustas o pruebas prolongadas conviene una solución más robusta. El formato es libre siempre que sea fácilmente recorrible y capaz de almacenar la información y las relaciones relevantes. El autor prefiere un formato tipo JSON porque las estructuras de datos jerárquicas abundan en las aplicaciones web y facilitan ordenar y buscar las notas.

Ejemplo de notas de recon tipo JSON describiendo endpoints de API (reproducido del libro):

```
{
  api_endpoints: {
    sign_up: {
      url: 'mywebsite.com/auth/sign_up',
      method: 'POST',
      shape: {
        username: { type: String, required: true, min: 6, max: 18 },
        password: { type: String, required: true, min: 6: max 32 },
        referralCode: { type: String, required: false, min: 64, max: 64 }
      }
    },
   sign_in: {
     url: 'mywebsite.com/auth/sign_in',
     method: 'POST',
     shape: {
        username: { type: String, required: true, min: 6, max: 18 },
        password: { type: String, required: true, min: 6: max 32 }
     }
   },
   reset_password: {
    url: 'mywebsite.com/auth/reset',
    method: 'POST',
    shape: {
     username: { type: String, required: true, min: 6, max: 18 },
     password: { type: String, required: true, min: 6: max 32 },
     newPassword: { type: String, required: true, min: 6: max 32 }
    }
   }
  },

 features: {
   comments: {},
   uploads: {
    file_sharing: {}
   },
  },

  integrations: {
   oath: {
    twitter: {},
    facebook: {},
    youtube: {}
   }
  }
}
```

También son útiles herramientas de notas jerárquicas como Notion o de mind-mapping como XMind. Lo importante es encontrar un método que mantenga la organización y escale más allá de aplicaciones simples cuando haga falta.

## Summary (resumen del capítulo)
Las técnicas de recon sirven para desarrollar un entendimiento profundo de la tecnología, la estructura y los servicios que sostienen una aplicación web. Además de ejecutar el recon, hay que prestar atención a los hallazgos y documentarlos de forma organizada y fácil de recorrer después. Las notas tipo JSON son el estilo que prefiere el autor, pero lo más importante es preservar relaciones y jerarquías manteniéndolas legibles y recorribles manualmente. Cada quien debe hallar un estilo que escale de aplicaciones pequeñas a grandes: el contenido y la estructura importan más que la herramienta o el formato.

## Ideas clave
- El recon es la fase de recopilación de datos previa al hackeo; su valor se multiplica combinada con hacking ofensivo e ingeniería de seguridad defensiva.
- Muchas técnicas de recon pueden provocar bans o acciones legales: solo contra aplicaciones propias o con permiso escrito.
- Una UI pública solo expone un subconjunto de la aplicación; con recon se pueden descubrir APIs de usuarios con permisos elevados.
- Casi todas las aplicaciones usan permisos por niveles (RBAC); rara vez un único nivel para todos.
- Comparar permisos de admin/moderador con los de un usuario estándar puede revelar *glitches* que permiten escalado de privilegios.
- No se necesita UI: con reverse engineering de APIs y payloads se puede mapear una aplicación sin acceso directo.
- Un error de configuración de red o firewall puede exponer servidores internos a redes públicas.
- Documentar el recon como un "mapa" jerárquico (p. ej. JSON, Notion, XMind) que preserve relaciones y sea fácil de recorrer.
