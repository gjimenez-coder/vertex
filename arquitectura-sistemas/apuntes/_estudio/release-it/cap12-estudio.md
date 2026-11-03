# Case Study: Waiting for Godot (Caso de estudio: Esperando a Godot) — Estudio

## Tarjetas de repaso

P: ¿Cuál es la tesis central del capítulo sobre el trabajo "terminado"? / R: No basta con escribir el código; nada está hecho hasta que corre en producción, y en sistemas antiguos ese camino suele ser penoso.

P: ¿Qué es el "ejército de despliegue" (deployment army)? / R: Un antipatrón en el que decenas de personas participan en un despliegue manual y ritualizado; cuanto más viejo es el software, más probable es tenerlo.

P: ¿Qué es el playbook del despliegue? / R: Un guion fila por fila que marca qué ocurre y cuándo durante el despliegue.

P: ¿Qué es el "proceso para actualizar el proceso"? / R: Dos días antes, el release commander recorre cada fila del playbook con el equipo para confirmar o actualizar cada paso para esa versión; cada reunión dura dos o tres horas.

P: ¿Qué es la reunión de go/no-go y cuándo ocurrió? / R: Una reunión a las 3 p.m. donde cada área da luz verde o roja; QA dio luz verde pero avisó de que podía aún aparecer un showstopper.

P: ¿Qué es la ventana de UAT en este relato? / R: El "smoke test" de las funciones nuevas que hacen los stakeholders de negocio de 1 a 3 a.m. tras levantarse.

P: ¿Qué rol desempeña el autor en el despliegue? / R: Sys Ops; "DevOps" aún no existiría hasta un año después.

P: ¿Qué es el jumphost? / R: La única máquina desde la que las demás aceptan conexiones SSH; el autor se conecta a él por PuTTY.

P: ¿Qué tres cosas hace en cada máquina el script del autor? / R: Actualiza un enlace simbólico para que apunte al nuevo code drop, ejecuta el precompilador de JSP y arranca los procesos de servidor.

P: ¿Cuánto cuesta aproximadamente cada despliegue y con qué frecuencia se hace? / R: Alrededor de 100.000 dólares (unos 100 dólares/hora por persona más ventas perdidas), entre cuatro y seis veces al año.

P: ¿Por qué el equipo "B" se va a dormir? / R: Para estar fresco y arreglar por la mañana los problemas que queden; es una regla del playbook porque una vez un error de operador se achacó a la fatiga.

P: ¿Por qué falló el despliegue en la UAT? / R: Una función pasó QA porque los datos de QA no coincidían con producción; producción tenía contenido extra con JavaScript que no funcionó con la nueva estructura de página.

P: ¿Qué es el "deployinator" de Etsy? / R: Un botón que despliega de forma rutinaria; un inversor de visita lo pulsó como parte normal del proceso, en contraste con el ejército de despliegue.

P: ¿Qué ejemplo ilustra que el playbook acumula pasos obsoletos? / R: Monitorizar unos números en una gráfica porque fueron mal hace años, aunque el código causante ya se reescribió; el paso sigue ahí.

## Preguntas de autoevaluación

P: ¿Qué quiere transmitir el autor con la narración de una sola noche de despliegue? / R: Lo doloroso, caro e improductivo que es poner código en producción cuando el proceso es manual y ritualizado. (Sección: Lo que necesitas saber / El ejemplo que recorre el capítulo)

P: ¿Cómo describe la escala humana del despliegue? / R: Más de veinte personas alrededor de una mesa y otras tantas por puente de conferencia desde cuatro lugares; en total más de cuarenta personas durante 24 horas. (Sección: El ejemplo que recorre el capítulo)

P: ¿Qué relación hay entre la antigüedad del software y el ejército de despliegue? / R: Cuanto más tiempo lleva el software en producción, más probable es tener el antipatrón del ejército de despliegue. (Sección: Lo que necesitas saber / Ideas clave)

P: ¿Qué causa recurrente de fallo en UAT ilustra este caso? / R: La divergencia entre el entorno de QA y producción: datos y contenido distintos hacen que una función pase QA pero falle en producción. (Sección: Por qué falló)

P: ¿Qué contraste económico y emocional plantea el episodio de Etsy? / R: El despliegue automatizado tiene beneficio financiero inmediato y rutinario; frente al coste de ~100.000 dólares y el desperdicio de potencial humano del ejército de despliegue. (Sección: El coste y el contraste con Etsy)

P: ¿Qué función cumple este capítulo dentro del libro? / R: Sirve de gancho emocional y económico para los capítulos siguientes, donde se analizan las fuerzas del antipatrón y cómo salir del "pozo de la desesperación". (Sección: Lo que necesitas saber)

P: ¿Por qué el playbook incluye pasos que ya no sirven? / R: Porque se añaden reglas defensivas por experiencias pasadas y no se retiran aunque la causa desaparezca, como monitorizar números cuyo código ya se reescribió. (Sección: El playbook y el proceso ritualizado / Ideas clave)

## Puntos a dominar

- Comprender la tesis: nada está hecho hasta que corre en producción.
- Reconocer el antipatrón del "ejército de despliegue" y su relación con la antigüedad del software.
- Entender qué es un playbook y cómo acumula pasos defensivos obsoletos.
- Identificar la divergencia QA/producción como causa recurrente de fallos en UAT.
- Captar el coste (~100.000 dólares, varias veces al año) y el desperdicio de potencial humano del despliegue manual.
- Contrastar el proceso ritualizado con el despliegue automatizado y rutinario (deployinator de Etsy).
