# Business Logic Vulnerabilities (Vulnerabilidades de lógica de negocio) — Estudio

## Tarjetas de repaso

P: ¿Qué es la application logic?
R: La combinación de información e instrucciones para tareas comunes, como renderizar una imagen o hacer una llamada de red.

P: ¿Qué son las business rules?
R: Reglas específicas de la empresa que las implementa; por ejemplo, permitir cancelar una reserva solo si faltan más de 24 horas para el vuelo.

P: ¿Qué es una business logic vulnerability?
R: Una vulnerabilidad en la implementación de una regla de negocio, que un atacante usa para obtener resultados no previstos.

P: ¿Por qué son difíciles de encontrar y explotar estas vulnerabilidades?
R: Porque exigen comprender un conjunto de reglas único de cada aplicación, pero suelen tener el mayor impacto y las mayores recompensas.

P: ¿Por qué el tooling automático casi no detecta estas vulnerabilidades?
R: Porque las herramientas se configuran para atacar frameworks, lenguajes y diseños compartidos, no la lógica concreta de un negocio.

P: ¿Cuáles son las cuatro familias de ejemplos que presenta el capítulo?
R: Matemática personalizada (custom math), efectos secundarios programados (programmed side effects), quasi-cash y errores por estándares como IEEE754.

P: ¿Cuál es el fallo clave en el ejemplo de transferencia de MegaBank?
R: El servidor comprueba que el usuario B existe, pero no comprueba que el usuario A tenga fondos suficientes.

P: ¿Qué dos requisitos debe implementar una aplicación para no ser un gran objetivo en cálculos?
R: La matemática adecuada a sus expectativas de negocio y las validaciones adecuadas sobre las entradas de una función matemática.

P: ¿Qué es un programmed side effect?
R: Un cambio no intencionado que surge al usar funcionalidad programada de una forma no prevista por el desarrollador.

P: ¿Cómo manipuló Henry Hacker a MegaCrypto?
R: Reunió $1 millón, compró 20 ByteCoins por noche a $50.000 (precio global) y los listó a $100.000, amaneciendo con $2 millones.

P: ¿Cuál era la defensa propuesta para MegaCrypto?
R: Recomprar monedas locales solo si el precio estaba dentro de un umbral porcentual respecto al precio medio del mercado global (edge-case detection).

P: ¿Por qué se llama quasi-cash al ataque con PayBuddy?
R: Porque PayBuddy no era una cuenta bancaria sino un intermediario financiero; las transacciones acabarían liquidándose en dinero real pero por el momento eran solo campos en una base de datos.

P: ¿Cómo obtenía beneficio Henry Hacker con MegaCard y PayBuddy por ciclo?
R: Cobraba $1.000 con su MegaCard, recibía $990 de comerciante (menos 1%) y $50 de reward (5%), terminando con $1.040, es decir $40 más por ciclo.

P: ¿Qué formato numérico usan JavaScript, Java, Ruby o Python y qué coste tiene?
R: El formato de punto flotante IEEE754; es eficiente en memoria pero compromete precisión, dando valores aproximados, no idénticos al resultado matemático real.

P: ¿Qué resultado da `0.1 + 0.2` en la consola de Chrome (v8)?
R: 0.30000000000000004, una pérdida de precisión de 0.0000000000000004.

## Preguntas de autoevaluación

P: ¿Qué diferencia a las business logic vulnerabilities de las vulnerabilidades arquetípicas estudiadas antes en el libro?
R: Las arquetípicas (injection, denial of service) tienen forma consistente, aparecen en muchas aplicaciones y permiten estrategias uniformes; las de lógica de negocio son únicas de una sola aplicación y exigen comprender sus reglas propias. (Sección "Lo que necesitas saber")

P: En el ataque de custom math a MegaBank, ¿qué puede ocurrir en el mejor y en el peor caso?
R: En el mejor caso, las validaciones del esquema de la base de datos cancelan la transacción; en el peor, el saldo de A queda en $0 mientras el de B crece $500 por transacción y ambos retiran miles de dólares antes de que el banco lo note. (Sección "Custom Math Vulnerabilities")

P: ¿Qué defecto de diseño permitió el ataque de efectos secundarios en MegaCrypto?
R: Que un pool de liquidez local y pequeño (alrededor de $1 millón) no basta para imitar precios globales y permite que individuos muy ricos manipulen el mercado. (Sección "Programmed Side Effects")

P: ¿Qué supuesto no contempló MegaBank en el diseño de MegaCard?
R: Que un cliente de MegaCard fuera también vendedor y pudiera hacer compras automatizadas contra sí mismo; faltaron checks and balances en la lógica. (Sección "Quasi-Cash Attacks")

P: ¿Por qué la pérdida de precisión de IEEE754 es peligrosa en aplicaciones financieras?
R: Porque en cálculos automatizados y repetidos millones de veces, o cuando las sumas se multiplican o exponencian, las diferencias entre saldo real y registrado pueden dispararse. (Sección "Vulnerable Standards and Conventions")

P: ¿Cuál es el primer paso para explotar una business logic vulnerability?
R: Familiarizarse íntimamente con el uso previsto de la aplicación, pensando como el cliente arquetípico. (Sección "Exploiting Business Logic Vulnerabilities")

P: ¿Cuál es el método más común para explotar estas vulnerabilidades?
R: Encontrar un edge case de lógica de negocio que no se maneja correctamente en el código. (Sección "Exploiting Business Logic Vulnerabilities")

## Checklist

- [ ] Mapea todos los casos de uso previstos de la aplicación que se te ocurran.
- [ ] Para cada caso, detalla cómo imaginas que funciona en el backend (application logic).
- [ ] Verifica que cada función matemática implemente la matemática correcta y las validaciones sobre sus entradas (p. ej. comprobar fondos antes de transferir).
- [ ] Busca edge cases no contemplados: conversiones de divisa, neteo de comisiones vs rewards, importes negativos, compra seguida de reembolso.
- [ ] Comprueba si usos no previstos de la funcionalidad producen efectos secundarios (side effects) aprovechables.
- [ ] Revisa cálculos financieros automatizados y repetidos frente a la pérdida de precisión de IEEE754.
- [ ] Añade detección de edge cases (p. ej. umbrales porcentuales respecto a precios de mercado globales) donde una regla local pueda ser manipulada.
