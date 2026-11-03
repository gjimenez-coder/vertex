# Proxy (Proxy) — Estudio

## Tarjetas de repaso

P: ¿Qué es el patrón Proxy? / R: Un patrón de diseño estructural que proporciona un sustituto o marcador de posición de otro objeto para controlar el acceso a él y hacer algo antes o después de que la solicitud llegue al objeto real.

P: ¿Qué requisito clave permite que un proxy se pase de forma transparente a cualquier cliente? / R: Que implemente la misma interfaz que el objeto de servicio original, camuflándose como ese servicio.

P: ¿Qué problema resuelve el Proxy cuando no puedes modificar la clase de servicio? / R: Permite añadir comportamiento alrededor de la lógica principal sin cambiar la clase, útil cuando pertenece a una biblioteca cerrada de un tercero.

P: ¿Qué problema concreto presenta el ejemplo de la biblioteca de YouTube? / R: La clase de descarga es ineficiente: ante el mismo video repetido lo descarga una y otra vez en lugar de cachearlo.

P: ¿Cómo lo resuelve el proxy en ese ejemplo? / R: Con una clase proxy que implementa la misma interfaz, delega el trabajo al descargador real y mantiene un seguimiento de los archivos para devolver resultados en caché.

P: ¿Qué cuatro elementos componen la estructura del patrón? / R: Interfaz de Servicio, Servicio, Proxy (con referencia al servicio) y Cliente, que trabaja con ambos a través de la misma interfaz.

P: ¿Qué analogía del mundo real usa el capítulo? / R: Una tarjeta de crédito como proxy de una cuenta bancaria, que a su vez es proxy de un manojo de billetes; todos comparten interfaz para realizar un pago.

P: ¿Qué es un proxy virtual? / R: Un proxy de inicialización diferida que retrasa la creación de un objeto pesado hasta que es realmente necesario, en lugar de crearlo al lanzar la aplicación.

P: ¿Qué es un proxy de protección? / R: Un proxy de control de acceso que pasa la solicitud solo si las credenciales del cliente cumplen ciertos criterios.

P: ¿Qué es un proxy remoto? / R: Un proxy que ejecuta localmente un servicio remoto pasando la solicitud por la red y gestionando los detalles de trabajar con ella.

P: ¿Qué es una referencia inteligente en este patrón? / R: Un proxy que rastrea clientes para desechar un objeto pesado cuando ya nadie lo usa y liberar recursos, y puede detectar si el cliente modificó el servicio.

P: ¿Quién gestiona normalmente el ciclo de vida del objeto de servicio? / R: El propio proxy gestiona típicamente el ciclo de vida completo de su objeto de servicio.

P: ¿Qué diferencia a Proxy de Adapter y Decorator en cuanto a interfaz? / R: Adapter da una interfaz diferente, Proxy la misma interfaz y Decorator una interfaz mejorada.

P: ¿Qué distingue a Proxy de Decorator pese a su estructura similar? / R: Ambos se basan en composición, pero el Proxy suele gestionar por su cuenta el ciclo de vida de su servicio, mientras que la composición del Decorator siempre la controla el cliente.

P: ¿Qué principio de diseño respeta el Proxy y por qué? / R: El principio abierto/cerrado, porque puedes introducir nuevos proxies sin cambiar el servicio ni los clientes.

## Preguntas de autoevaluación

P: ¿Por qué meter el código de inicialización diferida dentro de la propia clase del objeto no siempre es posible? / R: Porque la clase puede ser parte de una biblioteca cerrada de un tercero que no puedes tocar; la alternativa de hacerlo en cada cliente genera código duplicado. (Sección "Problema")

P: Al recibir una solicitud, ¿qué hace el proxy según la solución propuesta? / R: Crea un objeto de servicio real y le delega el trabajo, pudiendo ejecutar algo antes o después de la lógica primaria sin cambiar la clase original. (Sección "Solución")

P: En el pseudocódigo, ¿cuándo delega `CachedYouTubeClass` al servicio real? / R: Solo cuando el caché está vacío o debe refrescarse (`listCache == null || needReset`); si no, devuelve el resultado cacheado. (Sección "Pseudocódigo")

P: ¿Por qué la GUI `YouTubeManager` puede permanecer sin cambios al introducir el proxy? / R: Porque trabaja con el servicio a través de la interfaz, y la `Application` crea el servicio real, lo envuelve en el proxy de caché y se lo pasa al manager. (Sección "Pseudocódigo")

P: ¿Cuál es el plan B si no existe una interfaz de servicio preexistente? / R: Convertir el proxy en subclase de la clase servicio para heredar su interfaz. (Sección "Cómo implementarlo")

P: ¿Para qué sirve un método de creación estático o de fábrica al implementar el patrón? / R: Para decidir si el cliente obtiene un proxy o un servicio real. (Sección "Cómo implementarlo")

P: ¿Cuáles son las principales contras del patrón Proxy? / R: El código puede complicarse por la gran cantidad de clases nuevas y la respuesta del servicio puede retrasarse. (Sección "Pros y contras")

P: ¿En qué se parece y en qué se diferencia Proxy de Facade? / R: Ambos pueden almacenar temporalmente una entidad compleja e inicializarla por su cuenta, pero el Proxy tiene la misma interfaz que su servicio, lo que los hace intercambiables. (Sección "Relaciones con otros patrones")

## Puntos a dominar

- Definir Proxy como patrón estructural que controla el acceso a un objeto mediante un sustituto con la misma interfaz.
- Explicar por qué compartir interfaz hace al proxy intercambiable y transparente para el cliente.
- Identificar los cuatro elementos de la estructura: Interfaz de Servicio, Servicio, Proxy y Cliente.
- Reconocer los seis usos típicos: proxy virtual, de protección, remoto, de registro, de caché y referencia inteligente.
- Reproducir la lógica de delegación condicional del proxy de caché del ejemplo de YouTube.
- Enumerar los pros (control del servicio, gestión del ciclo de vida, funcionamiento sin servicio listo, principio abierto/cerrado) y las contras (más clases, posible latencia).
- Distinguir Proxy de Adapter, Decorator y Facade según interfaz y control del ciclo de vida.
