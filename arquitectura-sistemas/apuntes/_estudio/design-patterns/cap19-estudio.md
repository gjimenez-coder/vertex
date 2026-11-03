# Adapter (Adaptador) — Estudio

## Tarjetas de repaso

P: ¿Qué tipo de patrón de diseño es Adapter y qué permite?
R: Es un patrón estructural que permite la colaboración entre objetos con interfaces incompatibles.

P: ¿Qué otros nombres recibe Adapter?
R: Adaptador, Envoltorio o Wrapper.

P: ¿Cuál es la idea central del patrón?
R: Introducir un objeto intermedio (el adaptador) que convierte la interfaz de un objeto en otra que un segundo objeto pueda comprender, ocultando la complejidad de la conversión.

P: ¿Qué problema resuelve Adapter?
R: Reutilizar una clase existente (de un tercero o heredada) cuya interfaz no encaja con el resto del código, sin modificar esa clase ni el código cliente.

P: ¿Cuáles son las dos variantes del patrón?
R: El adaptador de objetos (por composición, en cualquier lenguaje) y la clase adaptadora (por herencia múltiple, por ejemplo en C++).

P: En el adaptador de objetos, ¿cómo se relaciona el adaptador con los otros objetos?
R: Implementa la interfaz de un objeto (la interfaz con el cliente) y envuelve el otro (el servicio), delegando y traduciendo las llamadas.

P: ¿Es consciente del adaptador el objeto envuelto?
R: No; la conversión queda oculta tras bambalinas y el objeto de servicio no sabe del adaptador.

P: ¿Qué secuencia sigue el funcionamiento de un adaptador?
R: 1) Obtiene una interfaz compatible con un objeto existente; 2) ese objeto invoca los métodos del adaptador; 3) el adaptador pasa la llamada al segundo objeto en el formato y orden que espera.

P: ¿Qué hace el `SquarePegAdapter` del pseudocódigo?
R: Extiende `RoundPeg`, contiene una instancia de `SquarePeg` y sobrescribe `getRadius()` para simular una pieza redonda con radio `peg.getWidth() * Math.sqrt(2) / 2`.

P: ¿Qué diferencia a Adapter de Facade?
R: Adapter hace utilizable una interfaz existente y suele envolver un solo objeto; Facade define una nueva interfaz y trabaja con todo un subsistema.

P: ¿Qué diferencia a Adapter de Decorator y Proxy respecto a la interfaz?
R: Adapter da una interfaz diferente al objeto envuelto, Proxy le da la misma interfaz y Decorator una mejorada; además Decorator soporta composición recursiva.

P: ¿Qué principios de diseño favorece Adapter?
R: El principio de responsabilidad única (separa la conversión de la lógica de negocio) y el principio de abierto/cerrado (nuevos adaptadores sin romper el cliente).

P: ¿Cuál es la principal desventaja del patrón?
R: Aumenta la complejidad del código al introducir nuevas interfaces y clases; a veces es más simple cambiar la clase de servicio.

## Preguntas de autoevaluación

P: ¿Por qué no basta con modificar la biblioteca de terceros para que acepte XML en el ejemplo del capítulo?
R: Porque podría romper el código que depende de ella y, con frecuencia, no se tiene acceso a su código fuente. (Sección: Problema / El ejemplo que recorre el capítulo)

P: ¿Cómo resuelve la aplicación de monitoreo de bolsa el conflicto de formatos?
R: Crea adaptadores de XML a JSON para cada clase de la biblioteca de análisis; el código se comunica con la biblioteca solo a través de esos adaptadores, que traducen los datos XML a JSON. (Sección: El ejemplo que recorre el capítulo)

P: ¿En qué se diferencian el adaptador de objetos y la clase adaptadora?
R: El adaptador de objetos usa composición (implementa una interfaz y envuelve el otro objeto) y sirve en cualquier lenguaje; la clase adaptadora usa herencia múltiple, solo en lenguajes que la soportan como C++, y realiza la adaptación en métodos sobrescritos. (Sección: Estructura)

P: ¿Cuándo conviene usar Adapter para reutilizar subclases existentes?
R: Cuando varias subclases carecen de una funcionalidad común que no puede añadirse a la superclase; se coloca esa funcionalidad en un adaptador que envuelve los objetos, siempre que compartan una interfaz común. (Sección: Aplicabilidad)

P: ¿Cuáles son los pasos clave para implementar Adapter?
R: Tener al menos dos clases con interfaces incompatibles; declarar la interfaz con el cliente; crear la clase adaptadora que la siga; añadir un campo con referencia al servicio; implementar los métodos delegando y convirtiendo; y hacer que el cliente use el adaptador a través de la interfaz. (Sección: Cómo implementarlo)

P: ¿Por qué el código cliente no debe acoplarse a la clase adaptadora concreta?
R: Para poder introducir o sustituir adaptadores sin descomponer el código cliente existente, lo que es útil cuando la interfaz del servicio cambia o se reemplaza. (Sección: Estructura / Cómo implementarlo)

P: ¿Qué distingue a Adapter de Bridge?
R: Bridge suele diseñarse por anticipado para desarrollar partes de forma independiente; Adapter se aplica a una aplicación existente para hacer que clases incompatibles trabajen juntas. (Sección: Relaciones con otros patrones)

## Puntos a dominar

- Reconocer Adapter como patrón estructural que traduce interfaces incompatibles mediante un objeto intermedio.
- Explicar el ejemplo hilo conductor (monitoreo de bolsa XML a JSON) y la analogía del enchufe de viaje.
- Distinguir las dos variantes: adaptador de objetos (composición) y clase adaptadora (herencia múltiple).
- Identificar los participantes: Cliente, Interfaz con el Cliente, Servicio y Clase Adaptadora.
- Entender el pseudocódigo de piezas cuadradas en agujeros redondos y el cálculo del radio simulado.
- Enumerar los pasos de implementación y por qué el cliente trabaja a través de la interfaz.
- Contrastar Adapter con Bridge, Decorator, Proxy y Facade por qué hacen a la interfaz y su alcance.
- Valorar sus pros (responsabilidad única, abierto/cerrado) y su contra (mayor complejidad de código).
