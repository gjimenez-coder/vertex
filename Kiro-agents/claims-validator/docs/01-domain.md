# Dominio — Validador de reclamos retail

> Qué es el sistema y cómo funciona el negocio. Lenguaje de negocio, no implementación.

## Qué es

Un sistema que recibe el **reclamo** de un cliente sobre una compra en una tienda
retail, lo **evalúa** contra un conjunto de reglas de negocio y devuelve un
**veredicto**: si el reclamo es válido, inválido, o si necesita revisión humana.

## Componentes principales

| Componente        | Rol |
|-------------------|-----|
| Entrypoint (CLI)  | Recibe el reclamo (JSON), lo entrega al sistema y muestra el veredicto. |
| Evaluador (Service)| Aplica las reglas de negocio y produce el veredicto con sus motivos. |
| Catálogo de órdenes| Fuente de la compra referida por el reclamo (órdenes y sus ítems). |

## Modelo de datos clave (jerarquía, no DDL)

```
Order (compra)
├─ orderId
├─ customerId
├─ purchasedAt            (instante UTC de la compra)
├─ totalAmountCents       (entero, centavos)
└─ Items
    ├─ sku
    ├─ quantity
    └─ unitPriceCents     (entero, centavos)

Claim (reclamo)
├─ claimId
├─ orderId                 (apunta a una Order)
├─ customerId
├─ category                (damaged | not_delivered | wrong_item | late | other)
├─ resolution              (refund | replacement | repair)
├─ amountRequestedCents    (entero, centavos; solo relevante para refund)
├─ description             (texto del cliente)
└─ submittedAt             (instante UTC en que se envía el reclamo)

Evaluation (resultado)
├─ claimId
├─ verdict                 (valid | invalid | needs_review)
├─ reasons[]               (códigos estables)
└─ decisionLog[]           (note | concern | block)
```

## Conceptos propios del dominio

- **Ventana de reclamo**: período máximo tras la compra en el que se acepta un
  reclamo (ej. 30 días). Fuera de ventana → inválido.
- **Categoría del reclamo**: tipifica el problema; condiciona qué reglas aplican.
- **needs_review**: el sistema no puede decidir con confianza (ej. monto de reembolso
  mayor al pagado, o categoría `other`) y escala a un humano. No es un rechazo.
- **Decision log**: por cada decisión relevante el evaluador deja una entrada
  `note` (informativa), `concern` (sigue, pero mirar) o `block` (no puede decidir solo).

## Flujo de negocio (estados del veredicto)

```
recibido → evaluado → { valid | invalid | needs_review }
```

El reclamo no tiene ciclo de vida persistente en este demo: entra, se evalúa, sale.
`needs_review` es la salida que entrega el caso a una cola humana (fuera de alcance).
