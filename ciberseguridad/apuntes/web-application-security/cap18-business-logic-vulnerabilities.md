# Web Application Security (2nd Edition) — Andrew Hoffman (O'Reilly Media, 2024)
## Capítulo 18 — Business Logic Vulnerabilities (Vulnerabilidades de lógica de negocio)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF y las citas usan la página del PDF.

## Lo que necesitas saber
Hasta ahora el libro estudió vulnerabilidades arquetípicas (injection, denial of service) que tienen una forma consistente, aparecen en muchas aplicaciones y permiten estrategias ofensivas y defensivas uniformes. Este capítulo cambia de registro: ¿qué ocurre cuando una vulnerabilidad es única de una sola aplicación? Eso sucede cuando una aplicación implementa reglas de negocio propias y un atacante aprende a usar esas reglas programadas para obtener resultados no previstos.

El capítulo distingue dos conceptos. La *application logic* combina información e instrucciones para tareas comunes (renderizar una imagen, hacer una llamada de red). Las *business rules* son específicas de la empresa que las implementa; el ejemplo que da es permitir cancelar una reserva solo si faltan más de 24 horas para el vuelo. Una vulnerabilidad en la implementación de una regla de negocio se denomina *business logic vulnerability*.

La tesis central: estas vulnerabilidades son las más difíciles de encontrar y explotar porque exigen comprender un conjunto de reglas único de cada aplicación, pero suelen tener el mayor impacto y las mayores recompensas. Además son casi imposibles de detectar con herramientas automáticas, porque esas herramientas se configuran para atacar frameworks, lenguajes y diseños compartidos, no la lógica concreta de un negocio.

Sales sabiendo cuatro familias de ejemplos (matemática personalizada, efectos secundarios programados, quasi-cash, y errores por estándares como IEEE754) y un método práctico para descubrirlas: mapear cada caso de uso previsto y buscar edge cases mal manejados.

## El ejemplo que recorre el capítulo
El hilo conductor son las empresas ficticias del libro —MegaBank y sus productos (MegaCrypto, MegaCard)— y el atacante recurrente Henry Hacker, que reaparece en cada escenario. Cada producto ilustra una clase distinta de vulnerabilidad de lógica de negocio.

## Custom Math Vulnerabilities (vulnerabilidades matemáticas personalizadas)
Son una de las formas más comunes. Casi todas las aplicaciones hacen cálculos para sus usuarios, pero la lógica detrás difiere entre ellas.

El ejemplo es una transferencia en MegaBank: el usuario A quiere enviar $500 al usuario B. El servidor valida que B existe, pide confirmación a A, resta 500 del saldo de A y suma 500 al saldo de B. El fallo clave: el servidor comprueba que B existe pero no comprueba que A tenga fondos suficientes.

En el mejor caso, las validaciones del esquema de la base de datos cancelan la transacción. En el peor, el saldo de A se queda en $0 mientras el de B sigue incrementándose $500 por transacción, permitiendo que A y B colaboren y retiren miles de dólares antes de que el banco lo note.

Una aplicación es un gran objetivo si no implementa ambos requisitos:
- La matemática adecuada para cumplir sus expectativas de lógica de negocio.
- Las validaciones adecuadas sobre las entradas de una función matemática.

El análisis estático difícilmente lo detecta porque depende del modelo de negocio concreto del banco. El ataque se describe como encontrar la forma de saltarse la funcionalidad prevista manteniéndose dentro de las reglas programadas.

## Programmed Side Effects (efectos secundarios programados)
A medida que una aplicación crece en complejidad, aparecen *side effects*: cambios no intencionados que surgen al usar funcionalidad programada de una forma no prevista por el desarrollador.

El caso es MegaCrypto, un portal donde los usuarios compran, venden y convierten criptomonedas. Ofrece cinco monedas (MegaCoin $1, ByteCoin $50.000, DoggoCoin $5, GhostCoin $2.000, HardDriveCoin $10) a precios fijados por la demanda del mercado. Cada noche a medianoche MegaCrypto rellena sus pools de liquidez comprando primero a sus propios usuarios (para reducir comisiones) y después a otro exchange.

Henry Hacker revisa registros públicos, hace ingeniería inversa de esa lógica y observa que la liquidez total ronda solo $1 millón. Reúne $1 millón con amigos adinerados. Nota que ByteCoin tiene una demanda media de 20 compras diarias y que MegaCrypto crea cada tarde órdenes de compra de 20 ByteCoins al precio local. Escribe un algoritmo que compra 20 ByteCoins por noche a $50.000 (precio global) y acto seguido los lista a $100.000. Invirtiendo $1 millón, amanece con $2 millones.

Lo que hizo quizá no era ilegal, pero sí una vulnerabilidad para MegaCrypto que podía costar millones por día. El problema: la lógica no previó que un pool de liquidez local y pequeño no basta para imitar precios globales y permite que individuos muy ricos manipulen el mercado. La defensa era recomprar monedas locales solo si el precio estaba dentro de un umbral porcentual respecto al precio medio del mercado global (edge-case detection).

> "What appears on the outside to be an economic issue is actually also a business logic vulnerability." (PDF p. 275)

## Quasi-Cash Attacks (ataques quasi-cash)
A veces la funcionalidad primaria es vulnerable, sobre todo cuando interactúan varios sistemas. En la industria de tarjetas de crédito, una de las más comunes y caras es la *quasi-cash transaction vulnerability*.

MegaBank lanza MegaCard: 25% APR, $0 de cuota anual y 5% de cashback en todas las compras durante los primeros tres años. Henry Hacker, tras ser despedido de EvilCorp, recuerda PayBuddy, un portal donde los vendedores crean facturas, cobran y depositan en su banco, cobrando solo 1% por transacción. Ya tenía una cuenta de comerciante conectada a su banco.

Su esquema:
1. Crea en PayBuddy una factura de $1.000 por un minuto de consultoría.
2. Paga esa factura con su MegaCard.
3. Queda con un crédito de $1.000 en la MegaCard y un abono de $990 en su cuenta de comerciante ($1.000 menos el 1%).
4. Recibe el 5% de reward ($50) en su cuenta personal.
5. Transfiere los $990 de PayBuddy a su cuenta personal.
6. Termina con $1.040, es decir $40 más por ciclo.

Automatiza el ciclo una vez por minuto: $2.400/hora en rewards, $57.600 en 24 horas. Retira el saldo antes de que MegaBank lo note; técnicamente no violó el acuerdo de servicio.

La tarjeta funcionó por diseño; lo que no se contempló fue que un cliente de MegaCard fuera también vendedor y pudiera hacer compras automatizadas contra sí mismo. Se llama quasi-cash porque PayBuddy no era una cuenta bancaria sino un intermediario financiero: transacciones que acabarían liquidándose en dinero real pero que por el momento eran solo campos en una base de datos. Faltaron checks and balances en la lógica de la aplicación.

## Vulnerable Standards and Conventions (estándares y convenciones vulnerables)
Un truco para hallar estas vulnerabilidades es buscar edge cases que surgen de anti-patrones comunes. El capítulo detalla la *numeric precision loss* (pérdida de precisión numérica).

Casi todos los lenguajes mayores (JavaScript, Java, Ruby, Python, etc.) usan el formato de punto flotante IEEE754, elegido por ser eficiente en memoria mediante notación científica y coma flotante. El coste: compromete precisión a cambio de espacio, de modo que cualquier cálculo con decimales puede dar un valor aproximado, no idéntico al resultado matemático real.

Demostración en la consola de Chrome (v8):

```javascript
0.1 + 0.2
// 0.30000000000000004
```

La pérdida de precisión es 0.0000000000000004, insignificante en la mayoría de casos. Pero en cálculos financieros —sobre todo automatizados y repetidos millones de veces, o cuando las sumas se multiplican o exponencian— las diferencias entre saldo real y registrado pueden dispararse. Conocer cómo los lenguajes manejan los números por defecto da superficie de ataque para pruebas manuales.

## Exploiting Business Logic Vulnerabilities (explotación)
Como estas vulnerabilidades están ligadas al caso de uso específico, el primer paso es familiarizarse íntimamente con el uso previsto de la aplicación. Con MegaCard, piensa como el cliente arquetípico: comprar comida, ir al cine, comer fuera.

Método:
1. Anota todos los casos de uso previstos que se te ocurran.
2. Para cada uno, detalla cómo imaginas que funciona en el backend (application logic). Ejemplo MegaCard: compras en FoodCo, se hace un handshake de red entre MegaBank y FoodCo, MegaBank añade un crédito por el valor comprado, y en una transacción separada debita el 5% contra tu cuenta.
3. Mapeada la funcionalidad, considera edge cases no contemplados. Ejemplos del libro:
   - Comprar $1.000 en CAD: ¿el 5% llega en USD o se aplica conversión de divisa?
   - Con una tienda en PayBuddy (1% fee vs 5% reward): ¿se puede netear 4% en transacciones de coste cero?
   - ¿Puedo emitir una factura negativa de –$1.000, sumando saldo a la tarjeta en vez de restarlo?
   - Si compro e inmediatamente reembolso, ¿conservo el 5% de reward?

Esos edge cases son los vectores de ataque iniciales. El método más común para explotar estas vulnerabilidades es encontrar un edge case de lógica de negocio no manejado correctamente en el código.

## Summary (resumen)
Son de las vulnerabilidades más avanzadas de hallar, pero las que más exhiben pen testers y bug bounty hunters. Tienen impacto significativo y son difíciles o imposibles de detectar de forma automática. Encontrarlas requiere ingenio, creatividad y pensar fuera de la caja; dominarlas pone tu perfil en altísima demanda.

## Ideas clave
- Distingue application logic (tareas comunes) de business rules (reglas propias de la empresa); la vulnerabilidad vive en la implementación de estas últimas.
- Son únicas por aplicación, difíciles de encontrar y casi imposibles de detectar con tooling automático, pero con el mayor impacto y recompensa.
- Custom math: faltan la matemática correcta y las validaciones sobre las entradas (p. ej. no comprobar fondos antes de transferir).
- Programmed side effects: usos no previstos de la funcionalidad; un pool de liquidez local pequeño se manipula con capital grande.
- Quasi-cash: cliente que también es comerciante abusa del 5% cashback vía un intermediario financiero (PayBuddy) con transacciones automatizadas contra sí mismo.
- IEEE754 provoca pérdida de precisión (0.1 + 0.2 = 0.30000000000000004); peligroso en cálculos financieros automatizados y repetidos.
- Para explotarlas: mapea cada caso de uso previsto, infiere el backend y busca edge cases mal manejados.
