---
inclusion: manual
---

# Testing — Principios Reutilizables

> Alcance: estrategia de pruebas automatizadas, independiente de framework de test. Complementa `cicd.md` (los tests corren en el pipeline) y `arquitectura-software.md` (refactor).

---

## 1. La pirámide de tests

Más tests rápidos y baratos abajo, menos tests lentos y caros arriba:

- **Unit** (base): funciones puras y lógica aislada. Rápidos, sin I/O.
- **Integración** (medio): varios componentes juntos, con DB/servicios reales o dobles fieles.
- **End-to-end** (cima): flujos completos de usuario. Pocos, para los caminos críticos.

Invierte en el nivel que te dé más confianza por unidad de esfuerzo. Para lógica de negocio compleja, los tests de integración suelen rendir más que muchos unit tests frágiles.

---

## 2. Qué merece un test

- **Lógica de negocio y reglas** (cálculos, transiciones de estado, validaciones): sí.
- **Caminos críticos** (pago, autenticación, inventario, contabilidad): sí, con prioridad. **Nunca quedan en standby.**
- **Bugs corregidos**: añade un test que reproduzca el bug (test de regresión).
- **Código trivial** (getters, mapeos directos) o UI puramente visual: bajo retorno; no lo fuerces.

---

## 3. Buen test = claro y determinista

- **Arrange–Act–Assert**: prepara, ejecuta, verifica. Una intención por test.
- **Nombre descriptivo** que diga qué comportamiento se verifica, no el método.
- **Determinista**: mismo input → mismo resultado. Sin dependencia de fecha/hora real, orden de ejecución, red o estado compartido entre tests.
- **Aislado**: cada test monta y limpia su propio estado; el orden no debe importar.
- Inyecta el **reloj**: el reloj del sistema no es monótono ni confiable en máquinas virtuales (ver `fechas-timezones.md` §4).

```
✅  it('rechaza el checkout cuando el stock es insuficiente', ...)
❌  it('test checkout 2', ...)
❌  usar new Date() real → inyecta un reloj fijo
```

---

## 4. Prueba comportamiento, no implementación

- Verifica **resultados observables** (salida, estado, efectos), no detalles internos.
- Un refactor que no cambia el comportamiento no debería romper los tests. Si rompe muchos, probablemente estabas probando la implementación.
- Mockea solo las **fronteras** (red, reloj, servicios externos), no todo el interior.

---

## 5. Datos y dobles

- Usa **fixtures/factories** para datos de prueba; evita duplicar objetos enormes en cada test.
- Prefiere dobles **fieles** al contrato real; un mock que miente da confianza falsa.
- No compartas estado mutable entre tests.

---

## 6. Tests como parte del flujo

- Los tests de la escala elegida deben correr en **CI** y en la verificación local de cambios.
- Un test que falla de forma intermitente (*flaky*) se arregla o se aísla: erosiona la confianza en toda la suite.

---

## 7. Refactor con red de seguridad

Refactorizar es cambiar la estructura sin cambiar el comportamiento; sin tests no puedes saber si lo lograste.

- **Antes** de un refactor grande, asegura que el comportamiento que vas a tocar está cubierto (tests de caracterización si no existen).
- Avanza en **pasos pequeños**, verificando después de cada uno; un paso que rompe se revierte, no se arregla encima.
- No mezcles refactor y cambio de comportamiento en el mismo paso (los "dos sombreros").
- Si no hay tests ni se pueden escribir rápido, el compilador y el typecheck son una red mínima, **no** suficiente para lógica de dinero o inventario. Reduce el alcance del cambio.

---

## 8. Lo que depende de la base de datos real

- La lógica de **locks, índices parciales, restricciones, concurrencia y transacciones** no se prueba con mocks de la DB: un mock no reproduce un deadlock ni una violación de unicidad.
- Usa una **base de datos desechable** (contenedor o instancia efímera) para esos tests, con migraciones aplicadas y datos realistas (incluyendo `NULL` y registros viejos).
- Prueba la concurrencia con peticiones simultáneas reales sobre el mismo registro.

---

## 9. Contratos e integraciones que fallan

- **Contract tests** entre servicios y entre cliente y API: cada lado prueba su propia conformidad con el contrato.
  - **Lado request:** el consumidor construye las peticiones según lo que exige el proveedor.
  - **Lado response:** el consumidor sabe manejar **cualquier** respuesta permitida, no solo la del ejemplo.
  - Ninguna de las dos invoca al servicio real.
- Las pruebas de integración que arman una petición y afirman contra los mismos datos solo verifican el bucle actual; no el contrato.
- Para cada integración externa, ten un **harness o doble que simule fallas**: conexión rechazada, respuesta que nunca llega, respuesta lenta, contenido inesperado (HTML en vez de JSON), código de estado desconocido. Un mock que solo devuelve respuestas felices no ejercita el manejo de errores.

---

## 10. Standby de tests: solo con condiciones

En fases de cambio estructural intenso un proyecto puede **pausar** parte de los tests para no mantenerlos sincronizados. Es una decisión de contexto, no un principio. Si la tomas, documéntala en el steering del proyecto con:

- **Motivo** (qué cambia tan rápido que el mantenimiento no compensa).
- **Alcance** (qué se pausa: unit tests de UI y CRUD trivial). Los caminos críticos de §2 **no** se pausan.
- **Condición de salida o fecha de revisión** (por ejemplo "hasta estabilizar el modelo de datos", o revisar cada trimestre).
- **Qué reemplaza la red de seguridad** (tests de integración, build, typecheck) y sus límites.

Un standby sin motivo, alcance ni fecha de revisión es abandono de tests.

---

## Prohibido

- Tests que dependen de fecha/hora real, orden de ejecución o estado compartido.
- Probar detalles de implementación en vez de comportamiento.
- Tests sin assertions o con nombres que no dicen qué verifican.
- Dejar tests flaky "porque a veces pasan".
- Mockear todo el interior hasta que el test ya no prueba nada real.
- Mockear la base de datos para probar locks, restricciones o concurrencia.
- Refactor grande de lógica crítica sin tests que lo respalden.
- Pausar los tests de caminos críticos o pausar sin motivo, alcance y revisión.

---

## Checklist al escribir un test

- [ ] ¿Verifica comportamiento observable, no implementación?
- [ ] ¿Sigue Arrange–Act–Assert con una intención clara?
- [ ] ¿El nombre describe el comportamiento esperado?
- [ ] ¿Es determinista (reloj inyectado, sin red real, sin orden implícito)?
- [ ] ¿Monta y limpia su propio estado?
- [ ] ¿Mockea solo las fronteras, con dobles fieles al contrato?
- [ ] ¿Está en el nivel adecuado de la pirámide?
- [ ] ¿Usa DB real desechable si prueba locks, restricciones o concurrencia?
- [ ] ¿Las integraciones tienen contract tests y simulación de fallas?
- [ ] ¿Corre en CI y no es flaky?

---

## Cuándo aplicar

- **Siempre / hoy (nivel 1):** tests de los caminos críticos (pagos, inventario, contabilidad, autenticación) y de las reglas de negocio puras; test de regresión por cada bug; tests deterministas; typecheck y build en cada cambio. Con una sola persona y una instancia, el dinero y el inventario ya justifican tests sobre DB real.
- **Al crecer (nivel 2):** tests de integración en CI sobre una DB desechable, tests antes de refactors grandes, un e2e por flujo crítico (checkout), vigilancia de tests flaky.
- **Con varios servicios o equipos (nivel 3):** contract tests por lado entre servicios, harness de fallas por integración, pirámide completa con un entorno de pruebas fiel a producción.
