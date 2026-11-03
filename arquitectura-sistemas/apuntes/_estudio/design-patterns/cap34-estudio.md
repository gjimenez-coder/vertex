# Template Method (Método plantilla) — Estudio

## Tarjetas de repaso

P: ¿Qué es el patrón Template Method?
R: Un patrón de diseño de comportamiento que define el esqueleto de un algoritmo en la superclase, pero permite que las subclases sobrescriban pasos del algoritmo sin cambiar su estructura.

P: ¿Cuál es la idea central del patrón?
R: Separar lo invariable (el orden y la coordinación de los pasos) de lo variable (la implementación concreta de cada paso).

P: ¿Qué es el método plantilla?
R: Un único método que contiene una serie de llamadas a los pasos del algoritmo en un orden específico; los pasos pueden ser abstractos o tener implementación por defecto.

P: ¿Qué método nunca debe sobrescribir el cliente?
R: El propio método plantilla; idealmente se declara como `final` para evitarlo.

P: ¿Qué son los pasos abstractos?
R: Pasos que deben ser implementados por todas las subclases.

P: ¿Qué son los pasos opcionales?
R: Pasos que ya tienen cierta implementación por defecto, pero que aún pueden sobrescribirse si es necesario.

P: ¿Qué es un gancho (hook)?
R: Un paso opcional con un cuerpo vacío; el método plantilla funciona aunque no se sobrescriba. Suelen colocarse antes y después de pasos cruciales como puntos adicionales de extensión.

P: ¿Cuál es la diferencia clave entre Template Method y Strategy?
R: Template Method se basa en la herencia y trabaja a nivel de clase (estático); Strategy se basa en la composición y trabaja a nivel de objeto, permitiendo cambiar comportamientos en tiempo de ejecución.

P: ¿Qué relación tiene Factory Method con Template Method?
R: Factory Method es una especialización de Template Method; a la vez, un Factory Method puede servir como paso de un gran Template Method.

P: ¿Qué problema tenían las clases de minería en el ejemplo guía?
R: Mucho código duplicado (el procesamiento y análisis de datos era casi idéntico) y condicionales en el cliente para elegir la acción según la clase del objeto de procesamiento.

P: ¿Cómo resuelve Template Method la duplicación del ejemplo?
R: Eleva los pasos similares (analizar datos y generar informes) a la clase base y deja en las subclases el código que varía (abrir/cerrar archivos, extraer/analizar por formato), eliminando también los condicionales del cliente gracias al polimorfismo.

P: ¿Cuáles son los componentes de la estructura del patrón?
R: La Clase Abstracta declara los métodos de los pasos y el método plantilla que los invoca; las Clases Concretas pueden sobrescribir todos los pasos salvo el método plantilla.

P: ¿Cuáles son los contras del patrón?
R: El esqueleto puede limitar a algunos clientes; se puede violar el principio de sustitución de Liskov al suprimir una implementación por defecto en una subclase; y los métodos plantilla son más difíciles de mantener cuantos más pasos tengan.

## Preguntas de autoevaluación

P: ¿Por qué la aplicación de minería de datos acumuló código duplicado y cómo lo corrige el patrón?
R: Porque el código para procesar y analizar los datos era casi idéntico entre formatos. El patrón crea una clase base con un método plantilla que encadena los pasos, sube lo común y deja lo variable en las subclases. (Sección: El ejemplo que recorre el capítulo)

P: ¿En qué se diferencia un gancho de un paso opcional corriente?
R: Un gancho es un paso opcional con un cuerpo vacío, de modo que el método plantilla funciona aunque no se sobrescriba; se usa como punto de extensión antes o después de pasos cruciales. (Sección: Tipos de pasos)

P: ¿Cuándo conviene aplicar Template Method según la aplicabilidad del capítulo?
R: Cuando quieres que los clientes extiendan solo pasos concretos sin alterar la estructura del algoritmo, y cuando tienes muchas clases con algoritmos casi idénticos y quieres elevar lo común a una superclase para eliminar duplicación. (Sección: Aplicabilidad)

P: ¿Qué ilustra el pseudocódigo de la IA del videojuego?
R: Que se reutiliza una misma estructura de IA sobrescribiendo detalles por raza (orcos agresivos, humanos defensivos, monstruos que no construyen); añadir una raza implica crear una subclase y sobrescribir métodos. (Sección: Pseudocódigo)

P: ¿Por qué el método plantilla no debe sobrescribirse y cómo se protege?
R: Porque define la estructura invariable del algoritmo; se protege declarándolo `final` para que las subclases no lo cambien. (Secciones: Lo que necesitas saber, Cómo implementarlo)

P: ¿Cómo puede el patrón llevar a violar el principio de sustitución de Liskov?
R: Al suprimir en una subclase una implementación por defecto de un paso, lo que altera el comportamiento esperado por la superclase. (Sección: Pros y contras)

P: ¿Qué analogía del mundo real usa el capítulo y qué representa?
R: La construcción de viviendas en masa: un plan arquitectónico estándar con puntos de extensión donde cada paso (cimientos, armazón, paredes, tuberías, cableado) puede ajustarse ligeramente. (Sección: Analogía en el mundo real)

## Puntos a dominar

- Definir Template Method y su objetivo de separar lo invariable de lo variable en un algoritmo.
- Distinguir los tres tipos de pasos: abstractos, opcionales y ganchos.
- Explicar por qué el método plantilla no se sobrescribe y cuándo declararlo `final`.
- Reconstruir el ejemplo guía de minería de datos: duplicación eliminada y condicionales del cliente suprimidos por polimorfismo.
- Describir la estructura: Clase Abstracta con método plantilla y pasos, Clases Concretas que los implementan.
- Enumerar pros y contras del patrón (reutilización vs. rigidez, riesgo de Liskov, mantenibilidad).
- Contrastar Template Method (herencia, nivel de clase, estático) con Strategy (composición, nivel de objeto, dinámico) y su relación con Factory Method.
