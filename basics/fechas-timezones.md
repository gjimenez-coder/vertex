---
inclusion: manual
---

# Fechas y Timezones — Principios Reutilizables

> Alcance: manejo de fechas en aplicaciones cliente-servidor con usuarios en distintas zonas horarias. Independiente de stack. Evita el bug clásico de "un día de diferencia".

Premisa: el negocio opera en una zona horaria local (ej. `America/Lima`), pero los datos se **almacenan y transportan en UTC**.

---

## 1. Dos tipos de fecha — nunca los mezcles

Antes de tocar una fecha, identifica cuál es:

### Instante (timestamp con hora)
Un momento exacto. Ej: `createdAt`, `updatedAt`, `reviewedAt`.
- **Backend/DB**: `timestamp with timezone`, en **UTC** (ISO 8601 con `Z`).
- **Frontend**: convertir a la TZ local **solo al presentar**.

### Día calendario (date-only)
Un día, sin hora ni zona. Ej: `businessDate`, fecha de un cierre, `nextOccurrence`.
- **Backend/DB**: columna `date`, expuesta como string **`YYYY-MM-DD`** sin conversión.
- **Frontend**: mostrar sin aplicar timezone.

```
✅  formatDate(instante, tz)      // instante → TZ local al mostrar
✅  formatDateOnly(diaCalendario) // date-only → sin TZ, tal cual
❌  formatDate(diaCalendario, tz) // aplicar TZ a un date-only → lo corre un día
```

---

## 2. Regla de oro

**La conversión a la TZ local *para presentar* vive SOLO en el frontend.** El backend nunca devuelve fechas pre-formateadas ni pre-convertidas: expone UTC crudo (instantes) o `YYYY-MM-DD` (días).

```
❌  return { date: '25 set. 2026' }           // backend formateando para humanos
❌  return { createdAt: toLocalTime(row.createdAt) }
✅  return { createdAt: row.createdAt.toISOString(), businessDate: row.businessDate }
```

---

## 3. Dónde el backend SÍ usa la TZ (es lógica de negocio)

### Filtrar por rango de días
El usuario elige "del 25 al 25" en su día local. El backend traduce ese día a un **rango UTC** antes de comparar contra columnas de instante.

```
localDateToUTCStart('2026-09-25', tz) → '2026-09-25T05:00:00.000Z'
localDateToUTCEnd('2026-09-25', tz)   → '2026-09-26T04:59:59.999Z'
```

### Derivar el día contable de un registro nuevo
"¿A qué día pertenece este movimiento?" depende de la TZ. Se calcula en el backend y se persiste como date-only; de ahí en adelante es un día puro.

```
businessDate = getTodayInTimezone(tz)  // 'YYYY-MM-DD' en la TZ del negocio
```

No derives el día cortando el ISO de un instante (`now.toISOString().slice(0,10)`): después de las 19:00 en Lima eso ya es "mañana" en UTC.

---

## 4. Relojes y tests

- No asumas que el reloj del sistema es **monótono ni exacto**: en máquinas virtuales puede saltar, pausarse o diferir entre instancias. No ordenes eventos por el reloj local de dos máquinas distintas; usa un orden causal (un contador, un ID secuencial de la base de datos, la hora de la base).
- Si el tiempo humano importa, usa una fuente sincronizada (NTP).
- En los tests, **inyecta el reloj** (una función `now()` o un reloj falso). Nunca dependas de la hora real (ver `testing.md` §3).

---

## Prohibido

- `iso.slice(0, 10)` para obtener "el día" de un instante: corta en UTC, desfasa cerca de medianoche.
- `new Date('YYYY-MM-DD')` esperando fecha local: se interpreta como medianoche UTC. (Excepción: columnas `date` que el ORM mapea a UTC medianoche; ahí es la representación correcta.)
- Usar la TZ del navegador (`getTimezoneOffset`) para lógica de negocio: usa siempre la TZ del negocio/tenant.
- Que el backend devuelva strings de fecha ya formateados para humanos.
- Aplicar timezone a un valor date-only.
- Derivar el día contable de un registro nuevo con UTC en vez de la TZ del negocio.

---

## Checklist al tocar una fecha

- [ ] ¿Es instante o día calendario? El tratamiento difiere.
- [ ] Si se muestra un date-only en el front → ¿sin TZ?
- [ ] Si se muestra un instante → ¿convertido a la TZ local al presentar?
- [ ] Si se filtra por rango de días → ¿se convierte a rango UTC con la TZ del negocio?
- [ ] Si se crea un registro con día contable → ¿se calcula con la TZ del negocio?
- [ ] ¿Ningún `iso.slice(0,10)` ni `new Date('YYYY-MM-DD')` colado?
- [ ] ¿El backend expone UTC / `YYYY-MM-DD` crudo, sin pre-formatear?
- [ ] ¿Los tests inyectan el reloj?

---

## Cuándo aplicar

- **Siempre / hoy (nivel 1):** todo este documento. Un negocio con una sola zona horaria ya sufre el bug del "día de diferencia" cada noche, porque el servidor corre en UTC; es la regla más barata y más frecuentemente violada.
- **Al crecer (nivel 2):** una zona horaria **por tenant** (configurada en el tenant, con un valor por defecto), y un helper compartido para rango de días y día contable en vez de copias locales.
- **Con varios servicios o equipos (nivel 3):** orden de eventos entre servicios por identificadores causales o relojes lógicos, no por la hora local de cada máquina; contratos de eventos que transportan siempre UTC.
