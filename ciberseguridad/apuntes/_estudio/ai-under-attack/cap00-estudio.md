# Prólogo — Preface (Prefacio) — Estudio

## Tarjetas de repaso

P: ¿Por qué los sistemas de IA se defienden distinto de las aplicaciones deterministas?
R: Porque aceptan lenguaje natural, recuperan contexto externo, mantienen estado, invocan herramientas y operan mediante autoridad delegada.

P: ¿Cuál es la tesis central del libro?
R: Que esa diferencia de los sistemas de IA requiere un mapa práctico que vaya de fundamentos a ataques, a defensa y a gobernanza/operación.

P: Según el texto, ¿cuándo importa un control?
R: Cuando cambia el comportamiento del sistema, deja registro, sobrevive a las pruebas y puede explicarse a quienes son dueños del riesgo (PDF p. 33).

P: ¿Para quién está dirigido el libro?
R: Para profesionales que aseguran sistemas de IA: ingenieros de application y cloud security, arquitectos, red teamers, ingenieros de IA y de plataforma, líderes de gobernanza y riesgo, product security, respondedores de incidentes y líderes técnicos.

P: ¿Qué conocimientos previos se asumen?
R: Comodidad con conceptos básicos de seguridad (autenticación, autorización, threat modeling, logging, APIs, infraestructura cloud e incident response); no hace falta ser investigador de machine learning.

P: ¿Qué rutas de ataque relevantes recorre el libro?
R: Prompt injection, jailbreaks, contaminación de memoria, envenenamiento de recuperación (retrieval poisoning), explotación de agentes, compromiso de la cadena de suministro del modelo y uso inseguro de herramientas.

P: ¿Cómo se organizan los 23 capítulos en bloques?
R: Caps. 1–5 fundamentos; caps. 6–11 ataques; caps. 12–18 defensa; caps. 19–23 gobernanza y operación.

P: ¿Qué técnicas de explotación de agentes cubren los caps. 6–11?
R: Confused deputy, parameter injection, uso indebido de herramientas, reemplazo de objetivos y propagación agente-a-agente.

P: ¿Qué es el Field Artifact?
R: Un recurso práctico por capítulo (actividad de seguridad, paquete de revisión, plan de pruebas, registro de evidencia o artefacto de programa) que da forma estructurada para aplicar el concepto del capítulo.

P: ¿Qué es el AI Under Attack Practitioner Toolkit?
R: Una guía complementaria en línea que acompaña al libro y en la que se alojan los Field Artifacts y labs de cada capítulo.

P: ¿Dónde se alojan los labs del libro?
R: En el repositorio de GitHub de Packt: https://github.com/PacktPublishing/AI-Under-Attack/tree/main.

P: ¿Qué recomienda el libro para aprovecharlo mejor?
R: Tener presente un sistema concreto al leer (chatbot, asistente RAG, flujo con modelo, agente interno, asistente de código o función de IA de un proveedor) y preguntarse por instrucciones, contexto, herramientas, identidad, estado y evidencia.

P: ¿Dónde deben ejecutarse las pruebas de mayor riesgo?
R: En un entorno aislado, con datos aprobados y reglas de enfrentamiento claras.

P: ¿Qué denota el estilo `CodeInText` en las convenciones?
R: Palabras de código, nombres de tablas/carpetas/archivos, extensiones, rutas, URLs ficticias, entrada de usuario y handles de X.

## Preguntas de autoevaluación

P: ¿Qué cinco comportamientos hacen distintos a los sistemas de IA frente a lo que los programas de seguridad clásicos defienden?
R: Aceptan lenguaje natural, recuperan contexto externo, mantienen estado, invocan herramientas y operan con autoridad delegada. (Lo que necesitas saber / Ideas clave)

P: ¿Qué criterio de "evidencia práctica" recorre toda la obra para juzgar un control?
R: Que cambie el comportamiento del sistema, deje registro, sobreviva a las pruebas y pueda explicarse a los dueños del riesgo. (Lo que necesitas saber / Ideas clave, PDF p. 33)

P: Si no eres investigador de ML, ¿puedes seguir el libro y qué bases necesitas?
R: Sí; basta con estar cómodo con autenticación, autorización, threat modeling, logging, APIs, infraestructura cloud e incident response, ya que el libro explica sobre la marcha los comportamientos de seguridad propios de la IA. (Para quién es el libro)

P: ¿Cómo progresan temáticamente los 23 capítulos?
R: De fundamentos a ataques, de ataques a defensa y de defensa a gobernanza y operación. (Qué cubre el libro)

P: ¿Qué preguntas conviene hacerse sobre un sistema de IA mientras se lee?
R: Dónde recibe instrucciones, dónde recupera contexto, qué herramientas puede invocar, bajo qué identidad actúa, qué estado recuerda y qué evidencia deja. (Cómo aprovechar el libro)

P: ¿Necesitas una plataforma de IA en producción para hacer los labs?
R: No; hay actividades que pueden hacerse como revisiones de diseño, ejercicios de tabletop o pruebas locales contra un sistema de demostración pequeño. (Cómo aprovechar el libro)

P: ¿Qué relación hay entre el capítulo impreso y su Field Artifact?
R: El capítulo explica el concepto, ruta de ataque, patrón de defensa o modelo de programa, y el Field Artifact da una forma estructurada de aplicarlo. (El AI Under Attack Practitioner Toolkit)

## Checklist

- [ ] Elegir un sistema de IA concreto (chatbot, asistente RAG, flujo con modelo, agente interno, asistente de código o función de proveedor) para tenerlo presente durante toda la lectura.
- [ ] Mapear en ese sistema: dónde recibe instrucciones, dónde recupera contexto, qué herramientas invoca, bajo qué identidad actúa, qué estado recuerda y qué evidencia deja.
- [ ] Verificar que los conocimientos previos de seguridad están cubiertos (autenticación, autorización, threat modeling, logging, APIs, cloud, incident response).
- [ ] Ejecutar cualquier prueba de mayor riesgo solo en un entorno aislado, con datos aprobados y reglas de enfrentamiento claras.
- [ ] Preparar actividades de bajo riesgo (revisión de diseño, tabletop o prueba local contra una demo pequeña) cuando no haya plataforma en producción.
- [ ] Localizar y usar el Field Artifact de cada capítulo en el Practitioner Toolkit para pasar de concepto a actividad operativa.
- [ ] Acceder al repositorio de labs en GitHub: https://github.com/PacktPublishing/AI-Under-Attack/tree/main.
- [ ] Al evaluar un control, comprobar que cambia el comportamiento del sistema, deja registro, sobrevive a pruebas y es explicable a los dueños del riesgo.
