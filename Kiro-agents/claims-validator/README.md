# Claims Validator

Sistema pequeño que recibe el **reclamo** de un cliente sobre una compra retail,
lo evalúa contra reglas de negocio y devuelve un **veredicto**: `valid`,
`invalid` o `needs_review`.

Construido como demo de las prácticas de Kiro/Firehorse: **spec primero**
(dominio → requisitos → diseño), **build después** (implementa exactamente el
spec) y **gate local** (tests en verde antes de entregar).

## Estructura

```
.kiro/steering/      Estándares siempre activos (vocabulario, capas, reglas)
.kiro/agents/        Conductor + autor + revisor del proyecto
.kiro/specs/
  claims-mvp/        El spec del MVP (una carpeta por feature)
    requirements.md  Requisitos EARS (REQ-001..030)
    design.md        Diseño + decisiones note/concern/block + constraints
    tasks.md         Plan de implementación trazable a los REQ
docs/
  01-domain.md       Dominio en lenguaje de negocio (transversal)
src/
  constants.js       Enums de dominio y umbrales
  errors.js          Errores tipados
  schemas.js         Validación de borde (objeto -> Claim)
  models.js          Order, Claim, Evaluation
  repository.js      Catálogo de órdenes (en memoria)
  rules.js           Reglas puras (una por requisito)
  service.js         Orquesta la evaluación (precedencia REQ-030)
  cli.js             Entrypoint
test/                Un test por regla + flujo + borde (node:test)
```

Stack: Node.js (>=20), ESM, test runner nativo `node:test`. Sin dependencias externas.

## Uso

```bash
# correr ejemplos sembrados
node src/cli.js --demo
# o: npm run demo

# evaluar un reclamo inline
node src/cli.js '{
  "claimId": "CLM-1", "orderId": "ORD-1001", "customerId": "CUST-1",
  "category": "damaged", "resolution": "replacement",
  "submittedAt": "2026-09-25T10:00:00Z"
}'
```

Salida (ejemplo):

```json
{
  "claimId": "CLM-1",
  "verdict": "valid",
  "reasons": ["ALL_CHECKS_PASSED"],
  "decisionLog": [{"level": "note", "message": "All checks passed"}]
}
```

## Reglas (resumen)

| Veredicto      | Cuándo |
|----------------|--------|
| `invalid`      | orden no existe, cliente no coincide, fuera de ventana (30 días), reclamo antes de la compra |
| `needs_review` | reembolso mayor al total de la orden, categoría `other` |
| `valid`        | pasa todas las reglas |

Precedencia: `invalid` > `needs_review` > `valid`. Un `invalid` corta la evaluación.

## Verificación local (gate antes de entregar)

```bash
node --test
# o: npm test
```

No requiere `npm install`: todo corre con la librería estándar de Node.
