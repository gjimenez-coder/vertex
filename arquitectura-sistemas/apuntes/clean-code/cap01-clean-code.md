# Clean Code: A Handbook of Agile Software Craftsmanship — Robert C. Martin (Prentice Hall, 2008)
## Capítulo 1 — Clean Code (Código limpio)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas usan la página del PDF `(PDF p. N)`.

## Lo que necesitas saber

El capítulo abre el libro planteando una tesis simple y rotunda: el código limpio importa y seguirá importando. Frente a quienes imaginan un futuro sin código (donde todo se genere desde especificaciones), Martin responde que el código es, en el fondo, la expresión precisa de los requisitos: por alto que sea el nivel de abstracción del lenguaje, siempre habrá que especificar los detalles con el rigor suficiente para que una máquina los ejecute, y eso es programar. Por tanto, "siempre habrá código".

La segunda tesis central es económica y profesional: el código malo frena. El desorden acumulado reduce la productividad de un equipo asintóticamente hacia cero, hasta volver inmanejable un sistema. El autor sostiene que la única forma de ir rápido es mantener el código limpio en todo momento; apresurarse ensuciando el código no cumple plazos, los incumple de inmediato.

Finalmente, el capítulo define qué es el código limpio recogiendo las voces de varios programadores reconocidos, y cierra con dos ideas prácticas: somos autores que escribimos para lectores, y la regla del Boy Scout para evitar la degradación. Sales sabiendo por qué el código importa, qué cuesta el desorden, de quién es la responsabilidad y qué cualidades definen el código limpio.

## There Will Be Code (Siempre habrá código)

El código representa los detalles de los requisitos; esos detalles no pueden ignorarse ni abstraerse del todo, hay que especificarlos. Especificar requisitos con tanto detalle que una máquina pueda ejecutarlos es programar, y esa especificación es código. Aunque crezcan los lenguajes de alto nivel y los lenguajes específicos de dominio (DSL), sus especificaciones seguirán siendo código: riguroso, preciso y formal. La idea de que el código desaparecerá se compara con esperar máquinas que hagan lo que queremos en lugar de lo que decimos; los requisitos bien especificados son tan formales como el código y pueden actuar como pruebas ejecutables de este.

## Bad Code (Código malo)

Martin discrepa de Kent Beck en que "el buen código importa" sea una premisa frágil: la considera de las más robustas del oficio, porque hemos sufrido su ausencia. Relata una empresa que a finales de los 80 lanzó una aplicación exitosa pero, por haberla sacado al mercado con prisas y con el código hecho un desastre, vio crecer los tiempos de carga y los fallos hasta quebrar. Al lidiar con código malo hacemos *wading* (vadear): avanzamos a duras penas entre un lodazal de maleza enredada. Todos hemos escrito código malo por ir rápido, y lo hemos dejado "para otro día", ignorando la ley de LeBlanc: *Later equals never* ("después es igual a nunca").

## The Total Cost of Owning a Mess (El coste total de poseer un desastre)

Con el tiempo, cada cambio rompe dos o tres partes más del código; nada es trivial. La productividad del equipo tiende asintóticamente a cero (Figura 1-1, productividad vs. tiempo). La dirección añade más personal, pero el nuevo equipo no conoce la intención del diseño y genera más desorden bajo presión.

- **The Grand Redesign in the Sky** (el gran rediseño en el cielo): harto, el equipo exige rehacer todo. Se forma un *tiger team* para construir un sistema nuevo que iguale al viejo mientras este sigue cambiando. La carrera puede durar años (el autor vio tardar 10); al terminar, el nuevo sistema ya es, a su vez, un desastre. Mantener el código limpio no es solo rentable: es una cuestión de supervivencia profesional.
- **Attitude** (actitud): el deterioro no es culpa de requisitos, plazos o jefes, sino nuestra; somos poco profesionales si lo permitimos. Los gestores buscan en nosotros la información para comprometerse; es su trabajo defender plazo y requisitos, y el nuestro defender el código con igual pasión. Analogía: un médico no deja de lavarse las manos porque el paciente lo exija (Semmelweis, 1847); el médico sabe más de los riesgos de infección. Igual de poco profesional es ceder ante gestores que no entienden el riesgo del desorden.
- **The Primal Conundrum** (el dilema primordial): todos saben que el desorden frena, y aun así sienten la presión de ensuciar para cumplir plazos. Los verdaderos profesionales saben que esa segunda parte es falsa: no se toman tiempo para ir rápido.

## The Art of Clean Code? (¿El arte del código limpio?)

Reconocer código limpio no equivale a saber escribirlo, igual que distinguir buena de mala pintura no nos hace pintores. Escribir código limpio requiere la disciplina de aplicar un sinfín de técnicas pequeñas guiadas por un "code-sense" (sentido del código), penosamente adquirido. Ese sentido no solo detecta si el código es bueno o malo: muestra la estrategia de transformaciones que preservan el comportamiento para pasar del desorden al orden. El programador que escribe código limpio es un artista que lleva una pantalla en blanco, mediante una serie de transformaciones, hasta un sistema elegantemente codificado.

## What Is Clean Code? (¿Qué es el código limpio?)

Opiniones de programadores reconocidos:

- **Bjarne Stroustrup** (inventor de C++): le gusta el código elegante y eficiente; lógica directa para que los bugs no se oculten, dependencias mínimas, manejo de errores completo según una estrategia articulada, y rendimiento casi óptimo para no tentar a ensuciar con optimizaciones. "Clean code does one thing well" (el código limpio hace una cosa bien). El código malo *tienta* a crecer el desorden; metáfora de las *broken windows* (ventanas rotas) de Dave Thomas y Andy Hunt: una ventana rota inicia la decadencia.
- **Grady Booch** (autor de *Object Oriented Analysis and Design with Applications*): el código limpio es simple y directo, "reads like well-written prose" (se lee como prosa bien escrita), nunca oscurece la intención del diseñador; lleno de *crisp abstractions* (abstracciones nítidas) y líneas de control directas.
- **"Big" Dave Thomas** (fundador de OTI, padrino de la estrategia Eclipse): otro desarrollador debe poder leerlo y mejorarlo; tiene pruebas unitarias y de aceptación, nombres significativos, una sola manera de hacer cada cosa, dependencias mínimas y explícitas, y una API clara y mínima. El código debe ser *literate* (alfabetizado), legible por humanos. Sin pruebas, el código no es limpio.
- **Michael Feathers** (autor de *Working Effectively with Legacy Code*): la cualidad que engloba a todas es el *care* (cuidado): el código limpio siempre parece escrito por alguien a quien le importa. Un subtítulo apropiado sería "How to Care for Code".
- **Ron Jeffries** (autor de libros de Extreme Programming): parte y casi termina con las reglas de código simple de Beck, por orden de prioridad: pasa todas las pruebas; no contiene duplicación; expresa todas las ideas de diseño del sistema; minimiza el número de entidades (clases, métodos, funciones). Se centra en duplicación y expresividad (nombres significativos, método haciendo una sola cosa, usar *Extract Method*) y en construir pronto abstracciones simples.
- **Ward Cunningham** (inventor del Wiki y de Fit, coinventor de XP): sabes que trabajas con código limpio cuando cada rutina resulta ser más o menos lo que esperabas; es bello cuando además hace que el lenguaje parezca hecho para el problema. Es responsabilidad del programador, no del lenguaje, hacer que el programa parezca simple.

## Schools of Thought (Escuelas de pensamiento)

El libro expone la "Object Mentor School of Clean Code": opiniones presentadas como absolutas dentro de esa escuela, con analogía a las artes marciales (Gracie Jiu Jitsu, Hakkoryu Jiu Jitsu, Jeet Kune Do). Ninguna escuela es absolutamente correcta; muchas recomendaciones del libro son controvertibles, pero fruto de décadas de experiencia y de prueba y error.

## We Are Authors (Somos autores)

El campo `@author` del Javadoc lo dice: somos autores con lectores y responsables de comunicar bien. La proporción de tiempo leyendo frente a escribiendo supera con creces 10:1 (ilustrado con la sesión de edición reproducida: navegar, dudar, escribir y borrar). Como leemos sin cesar código viejo para escribir el nuevo, queremos que leer sea fácil aunque escribir cueste más; y hacerlo fácil de leer en realidad lo hace más fácil de escribir. Si quieres ir rápido, haz que el código sea fácil de leer.

## The Boy Scout Rule (La regla del Boy Scout)

No basta con escribir bien el código: hay que mantenerlo limpio en el tiempo para frenar su deterioro. Regla adaptada de los Boy Scouts: "Leave the campground cleaner than you found it" (deja el campamento más limpio de como lo encontraste). Si cada quien devuelve el código un poco más limpio de como lo tomó, no podrá pudrirse. La limpieza puede ser mínima: mejorar un nombre, partir una función demasiado larga, eliminar un poco de duplicación o aclarar un `if` compuesto. La mejora continua es parte intrínseca del profesionalismo.

## Prequel and Principles / Conclusion (Precuela y principios / Conclusión)

El libro es una "precuela" de *Agile Software Development: Principles, Patterns, and Practices* (PPP, 2002) y referencia principios de diseño como SRP (Single Responsibility Principle), OCP (Open Closed Principle) y DIP (Dependency Inversion Principle), descritos a fondo en PPP. Como los libros de arte, este no promete convertirte en buen programador ni darte "code-sense": solo muestra procesos de pensamiento, técnicas y herramientas de buenos programadores, con muchos ejemplos de código bueno, malo y transformado. Lo demás depende de ti. Como el violinista que preguntó cómo llegar a Carnegie Hall: "Practica, hijo. ¡Practica!".

## Ideas clave

- Siempre habrá código: es la expresión precisa de los requisitos, por alto que sea el nivel de abstracción del lenguaje.
- El desorden frena; la única manera de ir rápido es mantener el código limpio en todo momento. *Later equals never*.
- El coste de un desastre lleva la productividad asintóticamente a cero; el gran rediseño rara vez salva el día.
- La responsabilidad del código es del programador, no de plazos ni gestores; defiende el código con pasión profesional.
- Código limpio: hace una cosa bien, se lee como prosa, nombres significativos, mínimas dependencias, sin duplicación y con pruebas.
- Reglas de código simple de Beck: pasa las pruebas, sin duplicación, expresa el diseño, minimiza entidades.
- Leemos código más de 10 veces por cada vez que escribimos; somos autores que escribimos para lectores.
- Regla del Boy Scout: deja el código más limpio de como lo encontraste; la mejora continua es profesionalismo.
