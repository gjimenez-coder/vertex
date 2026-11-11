# Diseño — Validador de reclamos retail

> Cómo se implementa lo que piden los requisitos. Incluye decisiones marcadas como
> `note` / `concern` / `block` (práctica de los design loops de Firehorse) y los
> constraints que se pasan al build.

## Estructura

```
claims-validator/
├─ src/
│  ├─ constants.js      # enums de dominio y umbrales (REQ-022, ventana)
│  ├─ errors.js         # errores tipados (REQ-002)
│  ├─ schemas.js        # DTO + validación de borde (REQ-001..003)
│  ├─ models.js         # Order, Claim, Evaluation (dominio en memoria)
│  ├─ repository.js     # catálogo de órdenes (lee datos) (REQ-010)
│  ├─ rules.js          # reglas puras, sin I/O (REQ-010..016)
│  ├─ service.js        # orquesta: valida → aplica reglas → arma veredicto
│  └─ cli.js            # entrypoint: recibe JSON, delega, imprime veredicto
└─ test/
```

## Mapa requisito → componente

| Requisito        | Dónde vive |
|------------------|------------|
| REQ-001..003     | `schemas.js` (validación de borde) |
| REQ-010..011     | `rules.js` + `repository.js` |
| REQ-012..013     | `rules.js` (usa ventana de `constants.js`) |
| REQ-014..016     | `rules.js` |
| REQ-020..022     | `service.js` + `models.js` |
| REQ-030          | `service.js` (orden de evaluación y corte temprano) |

## Flujo del evaluador (service)

1. El schema valida y produce un `Claim` tipado (si falla, error tipado → corta).
2. El service busca la `Order` en el repository.
3. Aplica las reglas en el orden de REQ-030, acumulando `reasons` y `decisionLog`.
   El primer `invalid` corta; los `needs_review` no cortan pero marcan el veredicto.
4. Si nada se dispara, el veredicto es `valid`.

## Decisiones de diseño

- **[note] Catálogo en memoria.** El repository usa un dict en memoria sembrado con
  órdenes de ejemplo. Mantiene el demo autocontenido; la interfaz permite cambiarlo
  por una DB sin tocar el service.
- **[note] Reglas puras separadas del service.** `rules.js` no hace I/O; recibe
  `Claim` y `Order` y devuelve resultados. Facilita testear cada REQ aislado.
- **[concern] `needs_review` no corta la evaluación.** Un reclamo puede acumular
  varios motivos de revisión. Se decidió reportarlos todos para dar contexto al
  humano, en vez de cortar en el primero. Revisar si en producción conviene cortar.
- **[concern] Ventana de reclamo fija por configuración.** Se usa una sola ventana
  global (30 días) en `constants.js`. En retail real la ventana varía por categoría
  de producto; se deja como punto de extensión documentado.
- **[block → resuelto] Zona horaria de la ventana.** Duda inicial: ¿la ventana se
  cuenta en TZ de la tienda o del cliente? Decisión: todos los instantes son UTC y la
  ventana se cuenta en UTC (REQ-022). Si el negocio exige TZ de tienda, es un cambio
  de regla acotado a `rules.js`, no de arquitectura.

## Constraints para el build (handoff spec → build)

- C-1: Dinero siempre entero en centavos; prohibido float en montos.
- C-2: Instantes siempre `Date` desde ISO-8601 con zona (UTC); rechazar fechas sin tz en el borde.
- C-3: La ventana de reclamo y los enums vienen de `constants.js`, no literales en `rules`.
- C-4: El service no construye mensajes de error a mano; usa los errores tipados.
- C-5: Cada regla de `rules.js` debe ser testeable sin tocar I/O.
