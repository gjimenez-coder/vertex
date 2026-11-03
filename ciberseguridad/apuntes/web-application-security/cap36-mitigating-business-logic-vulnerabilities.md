# Web Application Security (2nd Edition) — Andrew Hoffman (O'Reilly Media, 2024)
## Capítulo 36 — Mitigating Business Logic Vulnerabilities (Mitigación de vulnerabilidades de lógica de negocio)

> Nota de extracción: el texto se obtuvo de la capa de texto del PDF y las citas usan la página del PDF.

## Lo que necesitas saber
Este capítulo cierra el ciclo abierto en el Capítulo 18 sobre la escurridiza business logic vulnerability. Son vulnerabilidades avanzadas que no se detectan fácilmente con automatización ni con penetration testing, porque requieren conocimiento profundo de la lógica de negocio de la aplicación. Eso las hace difíciles de atacar.

La tesis central es optimista: justamente porque atacarlas exige profundo conocimiento de ingeniería, defenderse de ellas es bastante más fácil que atacarlas. Si el equipo de seguridad trabaja estrechamente con los equipos de ingeniería, se tiene ventaja a la hora de mitigarlas y proteger la aplicación.

Sales sabiendo tres enfoques de mitigación: mitigaciones a nivel de arquitectura (worst-case design), modelado estadístico (combinando fuzzing, data science y automatización de navegador), y el análisis de los resultados de ese modelado para localizar errores que conducen a vulnerabilidades. La idea rectora que atraviesa todo es empezar a pensar cómo la funcionalidad programada puede usarse de formas no intencionadas.

## Mitigaciones a nivel de arquitectura
El paso más importante ocurre en la fase de arquitectura, antes de escribir código. El diseño tradicional de aplicaciones web considera al usuario previsto junto con el caso de uso previsto; otros dominios técnicos ya identificaron el valor del diseño de peor caso (worst-case scenario design).

El libro ilustra la diferencia con dos algoritmos:
- A1: mediana de tiempo 5, pero 1 de cada 10 ejecuciones corre en n² (tiempo 25). Promedio sobre 10 corridas: (9 × 5 + 25)/10 = 7 (Tabla 36-1).
- A2: corre siempre a velocidad constante de 6.

Evaluando por la mediana, A1 (5) parece mejor que A2 (6). Pero al analizar los edge cases, A1 tiende a 7 con el tiempo, volviéndose menos eficiente que A2. Elegir A1 es best-case design.

> "Good security architects never use best-case design and always use worst-case design." (PDF p. 440)

Considerar desde el inicio el uso malicioso de cada componente funcional evita la mayoría de las business logic vulnerabilities. La mayoría surge de usuarios usando la aplicación de maneras no intencionadas o inesperadas; contemplar el peor caso en cada arquitectura permite encontrar esos escenarios antes de escribir código o exponer a los usuarios. Es el método más efectivo en términos de tiempo: después de la arquitectura, estas vulnerabilidades son mucho más caras y lentas de resolver.

## Modelado estadístico (Statistical Modeling)
En el extremo más matemático de la detección está el modelado estadístico, que combina fuzzing (probar la aplicación con entradas de datos aleatorias) con data science y automatización de navegador, para podar, seleccionar e iterar mucho más rápido que con fuzzing aleatorio solo.

El primer paso: el desarrollador integra analytics en la aplicación o produce una hipótesis sobre cómo los usuarios la usan. El modelo debe incluir tanto entradas (inputs) como flujos de página direccionales (acciones).

### Modelado de entradas (Modeling Inputs)
Para cada input se consideran los valores más probables:
- Dropdown: ordenar los ítems por frecuencia de elección.
- Texto libre: ordenar las entradas más comunes.
- Radio button: considerar cuál se selecciona más a menudo.

También deben considerarse entradas poco comunes e inesperadas. Por ejemplo, en un campo "name" la mayoría usará un nombre del top mil de nombres populares, pero un porcentaje menor elegirá nombres fuera de la lista, con caracteres y longitudes poco comunes. Estos edge cases importan porque tienen más probabilidad de evidenciar vulnerabilidades de lógica donde el código no contempló adecuadamente ese valor. Se modelan todos los campos interactivos y se almacenan en un formato fácil de procesar programáticamente: JSON, YAML, CSV o XML.

### Modelado de acciones (Modeling Actions)
En aplicaciones legacy, las acciones son típicamente flujos de página direccionales. En aplicaciones modernas incluyen además clics en botones, enlaces y formularios que generan peticiones AJAX en segundo plano, elementos interactivos que abren modales, llamadas websocket o RTC (real-time communication), o invocaciones directas de funciones JavaScript. Las rutas de acción son fáciles de obtener con herramientas de analytics que muchas empresas ya usan, por lo que es probable que el dato ya exista. Se registran en el mismo formato que las entradas para facilitar la automatización.

### Desarrollo del modelo (Model Development)
El siguiente paso es automatizar los flujos de usuario de forma programática en un entorno de pruebas local seguro. Técnicamente, un usuario es solo un conjunto de bits en una base de datos, así que poblar la base con usuarios modelo es sencillo; lo complejo es simular la traversía de la app y el uso de acciones.

Para ello se usan los headless browsers: navegadores que implementan el DOM, ejecutan JavaScript y hacen peticiones de red como un navegador normal, pero se controlan programáticamente en lugar de por UI. El más popular es Google's Headless Chrome, que adoptó una API similar a Phantom.js y Slimer.js (las herramientas de control de navegador más usadas la década anterior).

Ejemplo con la librería wrapper Puppeteer sobre Headless Chrome:

```javascript
import puppeteer from 'puppeteer';
import data from 'model';
import tools from 'tools';

(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();

  await page.goto(data.startURL);

  // Configure headless browser
  await page.setViewport({width: 1080, height: 1024});

  // Create user
  await page.type('.sign-up-username', data[0].username);
  await page.type('.sign-up-username', data[0].password);
  await page.click('.sign-up');
  await tools.logSignUpStatus()

  // Add comment when signed up
  const commentBox = '.comment-box';
  await page.waitForSelector(commentBox);
  await page.type('.comment-box', data[0].messages[0]);
  await page.click('.submit-comment');
  await tools.logCommentStatus()

  // Close browser and end automation
  await browser.close();
})();
```

El ejemplo toma datos del modelo y ejecuta programáticamente entradas, clics y transiciones de página contra el sitio objetivo. La diferencia con una implementación real es que las automatizaciones dependen de la lógica de negocio específica, pero el modelo de programación será muy similar.

### Análisis del modelo (Model Analysis)
Al correr el modelo contra el headless browser, se debe registrar cada petición de red en términos de payload, respuesta y código de estado HTTP. El objetivo es que los errores o fallos inesperados del servidor sean fáciles de hallar tras una muestra significativa; esos errores suelen conducir a business logic vulnerabilities, que luego los equipos de ingeniería remedian. Si se encuentra un error que no puede explotarse, igualmente aporta valor: revela bugs no relacionados con seguridad cuya resolución mejora la experiencia de usuario.

## Resumen
Las business logic vulnerabilities surgen cuando los arquitectos no consideran un edge case específico o olvidan implementar los controles adecuados dentro de la lógica. Son problemáticas porque difieren entre aplicaciones; aunque haya similitudes entre apps de una misma industria, las formas de atacarlas (lógica y técnicamente) suelen diferir, lo que las hace difíciles de atacar, detectar, mitigar y remediar.

Lo más importante para prepararse es empezar a pensar cómo la funcionalidad puede usarse de formas no intencionadas. Con ese patrón de pensamiento, la arquitectura se diseña de forma más segura y los sistemas de defensa automatizados se vuelven factibles. No deben descuidarse estas vulnerabilidades aunque parezcan bugs de programación en lugar de fallos de seguridad; la lógica de negocio suele ser el activo digital más crítico del negocio.

> "1 minute of fixing architecture bugs saves 10 minutes of resolving implementation bugs." (PDF p. 444)

## Ideas clave
- Las business logic vulnerabilities requieren conocimiento profundo de la aplicación: difíciles de atacar, pero más fáciles de defender si seguridad e ingeniería colaboran.
- La mitigación más efectiva ocurre en la arquitectura: usar worst-case design en vez de best-case design.
- El ejemplo A1/A2 muestra que evaluar por la mediana engaña; los edge cases degradan el rendimiento real (A1 tiende a 7 frente al constante 6 de A2).
- El modelado estadístico une fuzzing, data science y automatización de navegador para detectar más rápido que el fuzzing aleatorio.
- Modelar entradas y acciones por frecuencia, incluyendo edge cases poco comunes, y guardarlas en formatos como JSON, YAML, CSV o XML.
- Los headless browsers (Google's Headless Chrome, controlado vía Puppeteer) automatizan la traversía de la app en un entorno de pruebas seguro.
- Loguear payload, respuesta y código HTTP de cada petición; los errores inesperados suelen señalar vulnerabilidades (y los no explotables revelan bugs útiles).
- La clave transversal: pensar cómo la funcionalidad puede usarse de formas no intencionadas.
