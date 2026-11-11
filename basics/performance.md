---
inclusion: manual
---

# Performance — Principios Reutilizables

> Alcance: rendimiento de aplicaciones web (backend, acceso a datos y frontend). Independiente de stack. Complementa `apis.md` (paginación/filtrado), `observabilidad.md`, `manejo-errores.md` (límites y carga) y `arquitectura-software.md`.

---

## 1. Mide antes de optimizar

- No optimices por intuición: **perfila** y actúa sobre el cuello de botella real. La mayoría del tiempo se concentra en una fracción del código.
- Establece una **línea base** y objetivos (ej. p95 de latencia) antes de tocar nada; compara contra ella. (Ver percentiles en `observabilidad.md` §3.)
- Evita la optimización prematura: código claro primero, optimización dirigida por datos después.

---

## 2. Base de datos: el sospechoso habitual

- **Indexa** las columnas usadas en filtros, joins y orden. Un filtro sin índice escanea toda la tabla. Una clave foránea sin índice puede bloquear la tabla en un borrado.
- Evita el problema **N+1**: no hagas una query por cada elemento de una lista; usa carga por lote o join.
- **Pide solo lo que necesitas**: columnas específicas en vez de `SELECT *`, y filtra/pagina en la DB, no en memoria. (Ver `apis.md`.)
- Prefiere **paginación por cursor** sobre offset en tablas grandes: `OFFSET 10000` lee y descarta 10k filas.
- Toda consulta lleva **límite** de filas (ver `manejo-errores.md` §7).
- Vigila consultas lentas con métricas/trazas y revisa el plan de ejecución de las costosas.
- Dimensiona el **pool de conexiones** de forma coherente: instancias × tamaño del pool no debe superar el máximo de conexiones de la base de datos (y deja margen para tareas administrativas).

```
✅  SELECT id, name FROM products WHERE status = $1 ORDER BY created_at LIMIT 50
❌  const all = await findAll(); all.filter(...).slice(0, 50)   // trae todo, filtra en memoria
❌  for (const o of orders) o.items = await getItems(o.id)      // N+1
```

---

## 3. Caching con criterio

- Cachea lo **caro de calcular y estable en el tiempo** (configuración, catálogos, resultados costosos).
- Toda caché necesita una **estrategia de invalidación** clara: una caché que nunca expira sirve datos obsoletos. Define el TTL desde configuración (no hardcodeado) o invalida por evento.
- Toda caché en memoria tiene **tamaño máximo**; sin límite acaba en fuga de memoria y reinicios.
- Una caché por proceso no se comparte entre instancias: no la uses para estado que debe ser consistente entre ellas.
- Ubica la caché donde más rinde (en memoria, distribuida, CDN para estáticos) y mide el **hit rate**.
- Una caché fría tras un arranque o despliegue puede generar un pico de carga sobre la base de datos (*dogpile*): añade jitter y precalienta lo crítico.
- No caches datos sensibles sin considerar su exposición (ver `seguridad.md`).

---

## 4. Trabajo asíncrono y diferido

- Lo que no necesita responder al usuario en línea (emails, reportes, side effects) va a un **job en background / outbox**, no en el request. (Ver `backend.md` §3.)
- Procesa en **lotes** cuando sea posible en vez de uno por uno.
- Protege recursos con **límites**: concurrencia, rate limiting, tamaño de payload y colas acotadas. Qué hacer al saturarse (rechazar con 503/429, back pressure): `manejo-errores.md` §7.

---

## 5. Frontend

- **Minimiza el bundle**: code splitting, lazy loading de rutas/vistas pesadas, tree-shaking. El usuario no debe descargar lo que no usa aún.
- **No bloquees el render**: trabajo pesado fuera del hilo principal; estados de carga (skeletons) para percibir fluidez.
- **Listas grandes**: virtualización/paginación, no renderizar miles de nodos.
- **Optimiza assets**: imágenes en formatos modernos y tamaños adecuados; difiere lo no crítico.
- Evita renders innecesarios (memoización donde haya evidencia de costo, no por defecto).
- Assets con hash en el nombre se sirven con caché larga e inmutable; el HTML de entrada nunca se cachea.

---

## 6. Costo asintótico y recursos

- Conoce la complejidad de lo que escribes: un bucle anidado sobre datos que crecen es una bomba de tiempo.
- Libera recursos (conexiones, archivos, listeners); vigila fugas de memoria en procesos largos.
- Dimensiona pools (conexiones a DB, hilos) y mide la **saturación** (ver `observabilidad.md`).

---

## Prohibido

- Optimizar sin medir / sin línea base.
- Filtros, joins u orden sobre columnas no indexadas en tablas grandes.
- Patrón N+1 de queries.
- `SELECT *` o traer colecciones completas para filtrar en memoria.
- Cachés sin estrategia de invalidación ni tamaño máximo.
- Trabajo pesado o diferible dentro del request del usuario.
- Enviar al cliente un bundle o assets sin optimizar.
- Pools cuya suma entre instancias supera el máximo de conexiones de la base de datos.

---

## Checklist

- [ ] ¿Se perfiló y hay línea base antes de optimizar?
- [ ] ¿Las columnas de filtro/join/orden (y las claves foráneas) están indexadas?
- [ ] ¿Sin N+1, sin `SELECT *`, filtrado y paginado en la DB (cursor en tablas grandes)?
- [ ] ¿instancias × pool ≤ conexiones máximas de la base de datos?
- [ ] ¿Las cachés tienen invalidación, tamaño máximo y TTL desde configuración, y se mide el hit rate?
- [ ] ¿El trabajo diferible corre en background/lotes, fuera del request?
- [ ] ¿Hay límites de concurrencia/rate/payload?
- [ ] ¿El frontend hace code splitting, lazy loading y virtualiza listas grandes?
- [ ] ¿Los assets están optimizados y no se bloquea el render?
- [ ] ¿Se liberan recursos y se vigila la saturación?

---

## Cuándo aplicar

- **Siempre / hoy (nivel 1):** índices en filtros y claves foráneas, sin N+1, `LIMIT` en toda consulta, paginación, pool de conexiones coherente con el máximo de la base, cachés con TTL y tamaño máximo, trabajo diferible fuera del request, code splitting básico. Con una sola persona y pocos cientos de usuarios, medir con la herramienta de consultas lentas de la base ya basta.
- **Al crecer (nivel 2):** línea base y objetivo de latencia (p95) por flujo crítico, paginación por cursor en tablas grandes, medición de hit rate, precalentamiento de cachés, virtualización de listas grandes.
- **Con varios servicios o equipos (nivel 3):** presupuestos de rendimiento por servicio, caché distribuida o CDN, pruebas de carga periódicas, trazas distribuidas para encontrar el salto lento. Antes de ese punto, una caché distribuida suele ser más complejidad que beneficio.
