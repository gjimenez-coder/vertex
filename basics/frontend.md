---
inclusion: manual
---

# Frontend — Principios Reutilizables

> Alcance: aplicaciones web de UI (SPA/componentes), independiente de framework. Complementa `seguridad.md` (sesión, CSP, **XSS en §9**, logging), `apis.md` (contrato con el backend) y `performance.md` §5 (bundle y render).

---

## 1. Reutilizar antes de crear

Antes de escribir un componente, hook, helper o estilo nuevo, **busca si ya existe**. Orden de prioridad:

1. **Librería de UI compartida** — componentes de presentación (`Button`, `Input`, `Modal`, `Table`, `Toast`…). Úsalos en vez de maquetar a mano con elementos crudos.
2. **Librería de lógica compartida** — helpers (formateo de moneda/fecha, validadores, pricing), hooks (debounce, paginación, polling), tipos y contratos.
3. **Componente local del app** — solo si no existe nada reutilizable y es específico de ese app.
4. **Desde cero** — última opción. Si es genérico, créalo en el paquete compartido, no dentro de un app.

```
✅  import { Button } from '@ui/Button';  import { formatCurrency } from '@shared/format';
❌  <button className="rounded-lg bg-indigo-600 px-4 py-2 text-white">Guardar</button>
❌  const fmt = (c) => `$ ${(c/100).toFixed(2)}`   // reinventa formatCurrency
```

Si un componente existe pero le falta una variante/prop, **extiéndelo ahí**, no crees un duplicado local.

---

## 2. Theme — nunca colores hardcodeados

- Los colores viven como **tokens** del theme (CSS custom properties) expuestos como clases. Usa siempre las clases del theme, nunca hex crudos ni la paleta genérica del framework de estilos.
- Sombras y radios estandarizados también salen del theme.
- ¿Color nuevo recurrente? Agrégalo como token y mapéalo, no lo dejes suelto en el markup.

```
✅  <div className="bg-brand-primary text-white shadow-card">
    <span className="text-status-critical">
❌  <div className="bg-[#4f46e5] shadow-[0_1px_3px_rgba(0,0,0,0.1)]">
    <span className="text-red-600">   // para estado, usa el token semántico
```

---

## 3. Consistencia visual por contrato

Elementos repetidos (tablas, formularios, cards) usan **las mismas medidas** de tipografía, espaciado y forma, para que se vean como una sola familia. No inventes tamaños ni pesos por instancia.

- Define un **contrato base** (clases obligatorias) y cópialo tal cual.
- La densidad alternativa (compacta) se aplica **uniforme** en todo el elemento, nunca mezclando densidades entre columnas o filas.

```
✅  // mismo padding y tipografía en todas las tablas
    <td className="px-4 py-3 text-sm text-slate-600">
❌  // tamaños/pesos ad-hoc por tabla
    <td className="p-2 text-base font-bold">
```

---

## 4. El cliente es UX, no autoridad

- La validación, el control de acceso y el filtrado del frontend son para **experiencia de usuario**; la decisión real la toma y re-valida el servidor (ver `seguridad.md` y `apis.md`).
- El filtrado de listas se hace **server-side** (query params → backend), no descargando todo y filtrando en memoria. (Ver `apis.md`.)

---

## 5. Validación de formularios

Todo formulario que envía datos al backend valida **antes de enviar**:

1. Marca los campos requeridos visualmente (`required` → asterisco).
2. Una función de validación que retorna `{ field, message } | null`.
3. Valida contra el DTO/schema del backend: obligatorios no vacíos, formatos (email, URL…), rangos, enums.
4. Muestra el error **debajo del campo** afectado y haz **focus automático** al primero con error.
5. Los tipos del formulario reflejan fielmente los contratos del backend: requerido en backend = requerido en frontend.

```
✅  const err = validateForm(data); if (err) { setError(err); focus(err.field); return; }
❌  await createResource(data)   // enviar sin validar
```

---

## 6. Logging y datos sensibles en el cliente

- **Nunca `console.*` directo**: usa un logger que decida qué emitir según el entorno. En producción, mensajes opacos sin estructura interna. (Ver `seguridad.md`.)
- Nada sensible (tokens, IDs derivados de sesión, PII) en estructuras inspeccionables desde DevTools (ej. `dataLayer` de analytics).
- Asume que **todo lo que llega al bundle es público**: no incrustes secretos en variables de build.

---

## Prohibido

- Reinventar un componente/helper que ya existe en los paquetes compartidos.
- Colores hex o paleta genérica hardcodeados para marca o estado.
- Tamaños/pesos ad-hoc que rompen la consistencia de tablas/formularios.
- Filtrar listas en memoria en vez de server-side.
- Enviar un formulario sin validación previa.
- `console.*` directo; secretos en el bundle; datos sensibles en `dataLayer`.

---

## Checklist al agregar una feature de UI

- [ ] ¿Se reutilizó un componente de la librería compartida en vez de maquetar a mano?
- [ ] ¿Se reutilizaron helpers/hooks compartidos (formateo, validación, debounce)?
- [ ] ¿Un componente/helper genérico nuevo se creó en el paquete compartido, no en un app?
- [ ] ¿Los colores usan clases del theme (sin hex ni paleta genérica)?
- [ ] ¿Las tablas/formularios siguen el contrato visual estándar?
- [ ] ¿El filtrado de listas es server-side?
- [ ] ¿El formulario valida antes de enviar, con focus al primer error?
- [ ] ¿Los campos requeridos reflejan los del backend?
- [ ] ¿No hay `console.*` directo ni secretos/PII en el cliente?
- [ ] ¿Ningún dato de usuario entra como HTML sin sanear (ver `seguridad.md` §9)?

---

## Cuándo aplicar

- **Siempre / hoy (nivel 1):** validación de formularios antes de enviar, filtrado server-side, logger central sin `console.*`, sin secretos en el bundle, sin HTML de usuario sin sanear, reutilizar componentes y helpers compartidos, colores desde el theme.
- **Al crecer (nivel 2):** contrato visual de tablas y formularios documentado y revisado (cuando entra una segunda persona o una segunda app), librería de UI compartida con variantes, medición del tamaño de bundle.
- **Con varios servicios o equipos (nivel 3):** paquetes compartidos versionados entre apps, design tokens como fuente única, pruebas visuales automatizadas. Antes de ese punto, extraer un paquete compartido por cada componente es más costo que valor: promueve a compartido a la segunda aparición.
