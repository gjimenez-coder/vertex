---
inclusion: manual
---

# Observabilidad — Principios Reutilizables

> Alcance: logs, métricas, trazas y alertas para entender un sistema en producción. Independiente de stack. Complementa `manejo-errores.md`, `seguridad.md` (logging seguro) y `performance.md`.

Observabilidad = poder responder *"¿qué está pasando y por qué?"* sin desplegar código nuevo. Se apoya en tres pilares: **logs, métricas y trazas**.

---

## 1. Logs estructurados

- Emite logs **estructurados** (clave-valor / JSON), no texto libre: son consultables y agregables.
- Usa niveles con criterio: `debug` (desarrollo), `info` (hitos de negocio), `warn` (anomalía recuperable), `error` (fallo que requiere atención).
- **Nunca `console.*` directo**: usa un logger central que decida formato y destino según el entorno. (Ver `seguridad.md` §5.)
- Incluye contexto útil (ids de correlación, recurso afectado) pero **nunca secretos ni PII** en claro. Redacta los campos sensibles conocidos en el propio logger.

```
✅  logger.info('order_confirmed', { orderId, tenantId, amountCents })
❌  console.log('Order ' + id + ' confirmed for ' + email)   // texto libre + PII
```

---

## 2. Correlación de requests

- Propaga un **ID de correlación / trace ID** por toda la vida de un request (entrada → servicios → jobs → logs). Permite reconstruir qué pasó en una operación concreta.
- Si no viene del cliente/gateway, genéralo al entrar y pásalo hacia abajo. Inclúyelo en cada log de esa operación y devuélvelo en las respuestas de error (`requestId`) para poder buscarlo.

---

## 3. Métricas que importan

Mide lo que refleja la salud y el negocio, no todo por medir:

- **Las cuatro señales doradas**: latencia, tráfico, errores y saturación (uso de recursos).
- **Métricas de negocio**: pedidos/min, conversión, pagos fallidos — detectan problemas que las técnicas no ven.
- Distingue **tipos de métrica**: contadores (eventos acumulados), gauges (valor instantáneo), histogramas (distribución de latencias).
- Para latencia, mira **percentiles (p95/p99)**, no solo el promedio: la media esconde la cola lenta que sufren los usuarios. Mide del lado del cliente cuando puedas: es lo que realmente vive el usuario.
- No promedies percentiles de distintas instancias; agrega los histogramas.

---

## 4. Jobs y procesos asíncronos

Lo que corre fuera de un request (outbox, crons, colas, limpiezas) también falla y se degrada, y nadie lo ve.

- Registra para cada ejecución: **inicio, duración, resultado y cantidad procesada**. Un job que antes tardaba 2 segundos y ahora 2 minutos es una alerta temprana.
- Mide el **retraso** (edad del evento más viejo pendiente) y el tamaño de las colas.
- Alerta cuando un job **deja de ejecutarse**, no solo cuando falla.
- Los eventos que agotan reintentos quedan visibles para revisión (no se descartan en silencio).

---

## 5. Trazas distribuidas

- En sistemas con varios servicios, instrumenta **trazas** que sigan un request a través de los saltos, con *spans* por operación.
- Una traza responde *dónde* se fue el tiempo y *qué* servicio falló, algo que los logs sueltos no muestran.

---

## 6. Alertas accionables

- Alerta sobre **síntomas que afectan al usuario** (errores, latencia alta, caída de throughput), no sobre causas internas ruidosas.
- Cada alerta debe ser **accionable**: si no hay nada que hacer cuando se dispara, no debería existir. La fatiga de alertas hace que se ignoren las reales.
- Define umbrales sobre percentiles y ventanas de tiempo, no sobre picos puntuales.
- Acompaña la alerta con contexto (qué, desde cuándo, enlace al dashboard/traza).
- Define un **objetivo de nivel de servicio (SLO)** simple (por ejemplo "99% de checkouts responden en menos de 2 s") y alerta cuando se consume su presupuesto de error.

---

## 7. Health checks

- Expón endpoints de salud: **liveness** (¿el proceso está vivo?) y **readiness** (¿puede recibir tráfico, con sus dependencias listas?).
- Úsalos para orquestación (reinicios, balanceo) y como primera señal de un incidente.
- El health check de readiness verifica las dependencias imprescindibles (base de datos); **no** debe llamar a terceros opcionales (un tercero caído no debe sacar al servicio de rotación).

---

## 8. Auditoría

La auditoría responde *quién hizo qué y cuándo*, y es distinta del log de aplicación.

- Registra las **acciones de negocio sensibles** (cambios de permisos, anulaciones, pagos, accesos privilegiados) con actor, objeto, instante y resultado. Los procesos automáticos usan el actor `'system'` (ver `backend.md` §4).
- La auditoría es **append-only**: ni el usuario que actuó ni un administrador pueden editar o borrar sus propios registros. Idealmente se escribe también a un destino externo que el actor no controla.
- Mantén sus datos separados de los logs de aplicación (distinta retención y distinto acceso) y sin PII innecesaria.
- Respeta la retención legal aplicable.

---

## Prohibido

- Logs de texto libre no estructurados en servicios.
- `console.*` directo en producción.
- Secretos o PII en logs, métricas o trazas.
- Alertar sobre métricas no accionables (ruido).
- Medir latencia solo por promedio, ignorando p95/p99.
- Requests sin ID de correlación en sistemas multi-servicio.
- Jobs asíncronos sin registro de duración y resultado.
- Registros de auditoría editables por quien los generó.
- Un readiness que depende de un tercero opcional.

---

## Checklist

- [ ] ¿Los logs son estructurados, con nivel adecuado y vía logger central?
- [ ] ¿Hay ID de correlación propagado por toda la operación?
- [ ] ¿Sin secretos ni PII en logs/métricas/trazas?
- [ ] ¿Se miden las señales doradas (latencia, tráfico, errores, saturación)?
- [ ] ¿Hay métricas de negocio además de las técnicas?
- [ ] ¿La latencia se observa por percentiles (p95/p99)?
- [ ] ¿Cada job registra duración, resultado y retraso, y hay alerta si deja de correr?
- [ ] ¿Las alertas son accionables y basadas en síntomas al usuario?
- [ ] ¿Existen health checks de liveness y readiness?
- [ ] ¿Las acciones sensibles se auditan en un registro append-only?

---

## Cuándo aplicar

- **Siempre / hoy (nivel 1):** logs estructurados con logger central, ID de correlación, sin PII ni secretos, registro de duración y resultado de cada job, liveness y readiness, auditoría de las acciones sensibles, alerta cuando falla un job o suben los errores. Con una instancia, un panel simple de errores y latencia p95 ya aporta casi todo el valor.
- **Al crecer (nivel 2):** métricas de negocio, SLO simple del flujo crítico (checkout), alertas sobre percentiles y saturación, retención definida para logs y auditoría.
- **Con varios servicios o equipos (nivel 3):** trazas distribuidas con spans, correlación entre servicios obligatoria, auditoría enviada a un destino externo inalterable, guardias y runbooks por alerta. Antes de ese punto, las trazas distribuidas son más costo que valor.
