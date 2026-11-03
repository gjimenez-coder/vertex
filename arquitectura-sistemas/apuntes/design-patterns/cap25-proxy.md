# Dive Into Design Patterns — Alexander Shvets (Refactoring.Guru, 2021)
## Capítulo 25 — Proxy (Proxy)

> Nota de extracción: texto tomado de la capa de texto del PDF; las citas usan la página del PDF.

## Lo que necesitas saber

Proxy es un patrón de diseño estructural que te permite proporcionar un sustituto o marcador de posición para otro objeto. El proxy controla el acceso al objeto original y te permite hacer algo antes o después de que la solicitud llegue al objeto real (PDF p. 253).

La tesis es que, al implementar la misma interfaz que el objeto de servicio original, el proxy puede pasarse a cualquier cliente que espere ese servicio. Esto habilita añadir comportamiento alrededor de la lógica principal de la clase sin modificarla, algo especialmente útil cuando la clase pertenece a una biblioteca cerrada de un tercero que no puedes tocar.

Sales sabiendo cuándo interponer un intermediario con la misma interfaz que un servicio: para diferir la creación de objetos pesados, cachear resultados, controlar el acceso, registrar solicitudes, trabajar con servicios remotos o gestionar referencias inteligentes.

## El ejemplo que recorre el capítulo

Una biblioteca de integración de YouTube de un tercero ofrece una clase de descarga de videos que es muy ineficiente: si la aplicación solicita el mismo video muchas veces, la biblioteca lo descarga una y otra vez en lugar de cachearlo (PDF p. 258-259). La solución es una clase proxy que implementa la misma interfaz que el descargador original y le delega todo el trabajo, pero mantiene un seguimiento de los archivos descargados y devuelve resultados en caché cuando se solicita el mismo video varias veces.

## Problema

¿Por qué controlar el acceso a un objeto? Imagina un objeto enorme que consume muchos recursos del sistema y que solo necesitas de vez en cuando; por ejemplo, las consultas a bases de datos pueden ser muy lentas. Una implementación diferida (crear el objeto solo cuando sea realmente necesario) obliga a cada cliente a ejecutar código de inicialización diferida, lo que genera código duplicado. Lo ideal sería meter ese código dentro de la clase del objeto, pero no siempre es posible: la clase puede ser parte de una biblioteca cerrada de un tercero (PDF p. 254).

## Solución

El patrón sugiere crear una nueva clase proxy con la misma interfaz que el objeto de servicio original, y actualizar la aplicación para que pase el objeto proxy a todos los clientes del original. Al recibir una solicitud, el proxy crea un objeto de servicio real y le delega el trabajo. Como implementa la misma interfaz, puede ejecutar algo antes o después de la lógica primaria sin cambiar la clase original (PDF p. 255).

## Analogía en el mundo real

Una tarjeta de crédito es un proxy de una cuenta bancaria, que a su vez es un proxy de un manojo de billetes. Ambos implementan la misma interfaz y pueden usarse para realizar un pago. El consumidor no necesita llevar efectivo y el dueño de la tienda recibe los ingresos electrónicamente, sin el riesgo de perder el depósito o sufrir un robo camino al banco (PDF p. 256).

## Estructura

1. La **Interfaz de Servicio** declara la interfaz del Servicio; el proxy debe seguirla para camuflarse como objeto de servicio.
2. El **Servicio** es una clase que proporciona una lógica de negocio útil.
3. La clase **Proxy** tiene un campo de referencia que apunta a un objeto de servicio. Cuando finaliza su procesamiento (inicialización diferida, registro, control de acceso, caché, etc.), pasa la solicitud al servicio. Normalmente los proxies gestionan el ciclo de vida completo de sus objetos de servicio.
4. El **Cliente** debe funcionar con servicios y proxies a través de la misma interfaz, para poder pasar un proxy a cualquier código que espere un objeto de servicio (PDF p. 257-258).

## Pseudocódigo

La interfaz `ThirdPartyYouTubeLib` declara `listVideos()`, `getVideoInfo(id)` y `downloadVideo(id)`. La clase concreta `ThirdPartyYouTubeClass` la implementa enviando solicitudes reales a YouTube. El proxy `CachedYouTubeClass` implementa la misma interfaz, guarda una referencia al servicio y mantiene `listCache`, `videoCache` y `needReset`; solo delega al servicio real cuando el caché está vacío o debe refrescarse (PDF p. 258-260):

```
class CachedYouTubeClass implements ThirdPartyYouTubeLib is
    private field service: ThirdPartyYouTubeLib
    private field listCache, videoCache
    field needReset

    constructor CachedYouTubeClass(service) is
        this.service = service

    method listVideos() is
        if (listCache == null || needReset)
            listCache = service.listVideos()
        return listCache
```

La GUI `YouTubeManager` permanece sin cambios mientras trabaje con el servicio a través de la interfaz. La `Application` configura los proxies sobre la marcha: crea el servicio real, lo envuelve en el proxy de caché y se lo pasa al manager (PDF p. 260-261).

## Aplicabilidad

- **Inicialización diferida (proxy virtual):** retrasar la creación de un objeto pesado hasta que sea realmente necesario, en lugar de crearlo al lanzar la aplicación.
- **Control de acceso (proxy de protección):** permitir que solo clientes específicos usen el servicio; el proxy pasa la solicitud únicamente si las credenciales cumplen ciertos criterios.
- **Ejecución local de un servicio remoto (proxy remoto):** el proxy pasa la solicitud por la red y gestiona los detalles de trabajar con ella.
- **Solicitudes de registro (proxy de registro):** mantener un historial registrando cada solicitud antes de pasarla al servicio.
- **Resultados en caché (proxy de caché):** cachear resultados de solicitudes recurrentes usando los parámetros de la solicitud como claves de caché.
- **Referencia inteligente:** rastrear clientes para desechar un objeto pesado cuando ya nadie lo usa y liberar recursos; también detectar si el cliente modificó el servicio para reutilizar objetos sin cambios (PDF p. 262-263).

## Cómo implementarlo

1. Si no hay interfaz de servicio preexistente, crea una para que proxy y servicio sean intercambiables; como plan B, convierte el proxy en subclase de la clase servicio para heredar su interfaz.
2. Crea la clase proxy con un campo para la referencia al servicio. Normalmente el proxy crea y gestiona el ciclo de vida del servicio; en raras ocasiones el cliente se lo pasa por el constructor.
3. Implementa los métodos del proxy según su propósito; tras cierta labor, debería delegar en el servicio.
4. Considera un método de creación (estático o de fábrica) que decida si el cliente obtiene un proxy o un servicio real.
5. Considera implementar la inicialización diferida del servicio (PDF p. 264).

## Pros y contras

Pros: controlas el objeto de servicio sin que los clientes lo sepan; gestionas su ciclo de vida cuando a los clientes no les importa; el proxy funciona aunque el servicio no esté listo o disponible; respeta el principio de abierto/cerrado, ya que puedes introducir nuevos proxies sin cambiar servicio ni clientes. Contras: el código puede complicarse por la gran cantidad de clases nuevas y la respuesta del servicio puede retrasarse (PDF p. 265).

## Relaciones con otros patrones

- **Adapter** da una interfaz diferente al objeto envuelto, **Proxy** la misma interfaz y **Decorator** una interfaz mejorada.
- **Facade** es similar a Proxy porque ambos pueden almacenar temporalmente una entidad compleja e inicializarla por su cuenta; a diferencia de Facade, Proxy tiene la misma interfaz que su servicio, lo que los hace intercambiables.
- **Decorator** y Proxy tienen estructuras similares pero propósitos distintos: ambos se basan en composición, pero el Proxy suele gestionar el ciclo de vida de su servicio por su cuenta, mientras que la composición de los Decoradores siempre la controla el cliente (PDF p. 265-266).

## Ideas clave

- Proxy es un patrón estructural que interpone un sustituto con la misma interfaz que el objeto de servicio para controlar su acceso.
- Al compartir interfaz con el original, el proxy se pasa de forma transparente a cualquier cliente y añade comportamiento sin modificar la clase real.
- Resuelve el problema de no poder (o no querer) tocar la clase de servicio, por ejemplo una biblioteca cerrada de un tercero.
- Usos típicos: proxy virtual (inicialización diferida), de protección (control de acceso), remoto, de registro, de caché y referencia inteligente.
- El ejemplo del descargador de YouTube muestra un proxy de caché que evita descargas repetidas delegando al servicio solo cuando hace falta.
- Ventaja clave: respeta abierto/cerrado; costo: más clases y posible latencia añadida.
- Normalmente el proxy gestiona el ciclo de vida completo de su objeto de servicio.
