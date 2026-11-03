# Clean Code: A Handbook of Agile Software Craftsmanship — Robert C. Martin (Prentice Hall, 2008)
## Prólogo — Introduction (Introducción)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF y las citas usan la página del PDF.

## Lo que necesitas saber

La introducción plantea una imagen inicial —dos puertas y una habitación— para preguntar qué representa tu código, tu equipo y tu empresa, y cómo asegurarte de quedar del lado correcto cuando las cosas se ponen difíciles: revisiones, depuración en pánico, clientes que se marchan y jefes presionando. La respuesta que ofrece el autor es una sola: *craftsmanship* (artesanía).

La tesis central es que aprender a escribir código limpio es trabajo duro y no basta con conocer principios. El aprendizaje de la artesanía tiene dos partes: conocimiento y trabajo. Hay que adquirir el conocimiento de principios, patrones, prácticas y heurísticas que conoce un artesano, y además incorporarlo "a los dedos, los ojos y las entrañas" mediante práctica y esfuerzo.

Sales sabiendo cómo está organizado el libro y qué se espera de ti como lector: este no es un libro "feel good" que se lee en un avión. Hay que leer mucho código, pensar qué está bien y qué está mal en él, y seguir el desmontaje y rearmado de módulos. Requiere tiempo y esfuerzo, pero el autor sostiene que vale la pena.

## La analogía de la bicicleta

El autor compara aprender a programar con aprender a montar en bicicleta. Puede enseñarte la física —gravedad, fricción, momento angular, centro de masa— con menos de una página de ecuaciones y probarte que andar en bici es practicable. Aun así, te caerías la primera vez que subieras a la bici. Con el código ocurre lo mismo: se podrían escribir todos los principios "feel good" del código limpio y confiar en que hagas el trabajo (es decir, dejarte caer), pero eso no serviría ni como enseñanza ni como aprendizaje. Hay que sudarlo, practicar, verse fallar, ver a otros fallar, tropezar y rehacer el camino, y observar el precio de las decisiones equivocadas.

## La estructura del libro en tres partes

El libro se divide en tres partes:

- **Primera parte**: varios capítulos que describen los principios, patrones y prácticas para escribir código limpio. Contienen bastante código y son exigentes de leer; preparan para la segunda sección. El autor advierte: si dejas el libro tras esta sección, "buena suerte".
- **Segunda parte**: el trabajo más duro. Consiste en varios casos de estudio de complejidad creciente. Cada caso es un ejercicio de limpiar código: transformar código con problemas en código con menos problemas. El detalle es intenso; hay que ir y volver entre la narrativa y los listados de código, analizar y entender el código, y seguir el razonamiento de cada cambio. Debería llevar días.
- **Tercera parte**: la recompensa. Es un único capítulo con una lista de heurísticas y *smells* reunidos mientras se creaban los casos de estudio. Al limpiar el código, se documentó cada razón de las acciones como una heurística o un smell, tratando de entender las propias reacciones ante el código leído y cambiado. El resultado es una base de conocimiento que describe la forma de pensar al escribir, leer y limpiar código.

## Las heurísticas y las referencias cruzadas

La base de conocimiento tiene valor limitado si no se hace el trabajo de leer con cuidado los casos de estudio. Allí se anota cada cambio con referencias hacia adelante a las heurísticas, que aparecen entre corchetes, por ejemplo `[H22]`. Esto permite ver el contexto en que se aplicaron y escribieron esas heurísticas. Lo valioso no son las heurísticas en sí, sino la relación entre ellas y las decisiones concretas tomadas al limpiar el código. Para reforzar esas relaciones, al final del libro hay una referencia cruzada con el número de página de cada referencia hacia adelante, para localizar dónde se aplicó cada heurística.

El autor insiste: quien lea solo la primera y la tercera sección y se salte los casos de estudio habrá leído "otro libro feel good" sobre buen software. Pero quien se tome el tiempo de trabajar los casos, siguiendo cada paso y cada decisión mínima, poniéndose en el lugar de los autores, obtendrá una comprensión mucho más rica de los principios, patrones, prácticas y heurísticas. Dejarán de ser conocimiento "feel good" y se volverán parte de ti, como la bicicleta se convierte en extensión de tu voluntad cuando dominas cómo montarla.

## Agradecimientos

El autor agradece a sus dos artistas, Jeniffer Kohnke y Angela Brooks. Jennifer es responsable de las imágenes del inicio de cada capítulo y de los retratos de Kent Beck, Ward Cunningham, Bjarne Stroustrup, Ron Jeffries, Grady Booch, Dave Thomas, Michael Feathers y el propio autor. Angela es responsable de las imágenes del interior de cada capítulo y ha realizado muchas a lo largo de los años, incluyendo varias en *Agile Software Development: Principles, Patterns, and Practices*.

## Ideas clave

- La respuesta a cómo quedar del lado correcto cuando el software se complica es la artesanía (*craftsmanship*).
- Aprender la artesanía tiene dos partes inseparables: conocimiento y trabajo (práctica).
- La analogía de la bicicleta: conocer la teoría no basta; hay que practicar y caerse para aprender.
- No es un libro "feel good": exige leer mucho código y pensar qué está bien y qué está mal en él.
- El libro tiene tres partes: principios y prácticas, casos de estudio, y una lista de heurísticas y smells.
- Los casos de estudio son el núcleo del trabajo; sin ellos, la base de conocimiento vale poco.
- Las referencias hacia adelante tipo `[H22]` conectan cada decisión de limpieza con su heurística; lo valioso es esa relación.
- El objetivo es que principios, patrones, prácticas y heurísticas dejen de ser teoría y se integren en el lector.
