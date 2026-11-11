---
inclusion: manual
---

# Modelado de Dominio y Schemas — Principios Reutilizables

> Alcance: cómo documentar un dominio de negocio y organizar los schemas de datos. Independiente de ORM/DB. Complementa `arquitectura-software.md` y `backend.md`.

---

## 1. Documenta el dominio antes del código

Un documento de dominio responde *qué es el sistema y cómo funciona el negocio*, no cómo está implementado. Debe incluir:

- **Qué es** el sistema, en una frase.
- **Componentes principales** y su rol (ej. tienda pública, panel admin, API).
- **Modelo de datos clave** como jerarquía de entidades (no como DDL).
- **Flujos de negocio** como secuencia de estados (ej. el ciclo de vida de un pedido).
- **Conceptos propios del dominio** (modos, estados, reglas) con su significado.

```
Tenant (negocio)
├─ Business Units
│   ├─ Tienda virtual (venta online)
│   └─ Almacén (inventario)
├─ Products → SKUs (variantes)
├─ Orders
└─ Inventory (balances + movimientos)
```

El valor de este doc es que **cualquiera entienda el negocio sin leer código**. Mantenlo en lenguaje de negocio, con los términos que usa el equipo.

---

## 2. Modela los estados como un flujo explícito

Las entidades con ciclo de vida (pedido, pago, envío) se documentan como una **máquina de estados**: qué estados existen, qué transición los conecta y quién/qué la dispara.

```
pending → payment_confirmed → preparing → shipped → delivered
```

- Nombra los estados con el vocabulario del negocio y en el mismo idioma que el resto del dominio.
- Declara las transiciones **permitidas** en un solo lugar; una transición no declarada se rechaza.
- Los estados terminales son inmutables.

---

## 3. Una tabla por archivo de schema

- Cada archivo de schema define **exactamente una tabla**. Dos tablas relacionadas (ej. `orders` y `order_items`) van en archivos separados.
- Las **constantes y enums de dominio NO viven en el schema**: van en el archivo de constantes del módulo (ver `arquitectura-software.md` §4).

---

## 4. Agrupa las columnas por correlación

Dentro de una tabla, agrupa las columnas en secciones comentadas, en un orden consistente:

```
1. Core fields         — id, tenant/org id, campos de identificación
2. Classification      — tipos, categorías, estados
3. Grupos de dominio   — info de cliente, envío, pago, etc.
4. Configuration       — opciones, límites, umbrales
5. Status & Timestamps — active, status, createdAt, updatedAt
```

```
// ── Core fields ──────────────
id, tenantId, name
// ── Customer info ────────────
customerFirstName, customerLastName
// ── Timestamps ───────────────
createdAt, updatedAt
```

Esto hace que todas las tablas se "lean igual" y que encontrar un campo sea predecible.

---

## 5. Tipos de dato canónicos

- **Dinero**: entero en la unidad menor (centavos) o decimal exacto. **Nunca float** (los números de punto flotante acumulan error: `0.1 + 0.2 ≠ 0.3`).
- **Fechas**: instante en UTC (`timestamp with timezone`) o día calendario (`date`). Distínguelos (ver `fechas-timezones.md`).
- **IDs**: estables y opacos; exponlos como string hacia afuera (ver `apis.md` §8). No secuenciales cuando se exponen.
- **Multi-tenant**: toda tabla de negocio lleva su identificador de tenant/organización desde el inicio.

---

## 6. Invariantes y ledgers

### Invariantes que cuida la aplicación

La base de datos garantiza integridad **estructural** (tipos, `NOT NULL`, unicidad, claves foráneas dentro de un módulo). Las reglas de **negocio** ("el saldo nunca es negativo", "los débitos igualan los créditos", "una reserva no excede el stock") las define la aplicación.

- Escribe cada invariante como una regla explícita y dónde se hace cumplir (restricción de la DB, validación del Service, o ambas).
- Prefiere que la **base de datos** haga cumplir lo que pueda (`CHECK`, `UNIQUE`, índices parciales) como última barrera, sin sustituir la validación del Service.
- Una invariante que abarca **varias filas** necesita bloqueo o una operación atómica (ver `backend.md` §9).

### Ledger append-only y saldos derivados

Para dinero, inventario y contabilidad, registra **hechos inmutables** y deriva el saldo de ellos.

- El **ledger** (movimientos) es append-only: no se edita ni se borra; una corrección es un **movimiento inverso**.
- El **saldo** es una vista derivada. Si lo materializas por rendimiento, actualízalo en la misma transacción que inserta el movimiento y **reconcílialo** periódicamente contra la suma del ledger (detecta y repara deriva).
- Cada movimiento lleva quién, cuándo (instante), por qué (referencia al origen) y un ID **determinístico** para que un reintento no duplique.
- Nunca escribas el saldo directamente: siempre a través de un movimiento.

```
✅  INSERT INTO movements (...)   +  UPDATE balance SET qty = qty + $1   -- misma transacción
❌  UPDATE balance SET qty = 17      -- sin rastro de por qué ni de dónde vino
```

### Datos desnormalizados

Una copia de un dato en otra tabla (un contador, un total, un nombre) debe actualizarse **en la misma transacción** que el dato original, o tener un proceso explícito de reconciliación. Sin eso, acaban desincronizados.

---

## 7. Referencias entre módulos

- Entre **módulos** (y más aún entre servicios) no hay claves foráneas: se referencia por **ID semántico** (`tenantId`, `skuId`).
- La existencia y la autorización del objeto referenciado se valida en el **Service** del módulo dueño, no con una FK entre módulos.
- Dentro de un mismo módulo sí puedes usar claves foráneas para integridad.
- Cada módulo (o servicio) es dueño de sus tablas; los demás las consultan a través de su Service o API (ver `arquitectura-software.md` §1 y §9).
- Una tabla compartida entre servicios acopla sus despliegues: evítala.

---

## Prohibido

- Documentar el dominio en términos de implementación en vez de negocio.
- Más de una tabla por archivo de schema.
- Constantes o enums de dominio dentro del schema.
- Columnas sin agrupar / orden arbitrario entre tablas.
- Dinero como float.
- Editar o borrar movimientos de un ledger; escribir un saldo sin movimiento.
- Invariantes de negocio sin dueño explícito.
- Claves foráneas entre módulos o tablas compartidas entre servicios.

---

## Checklist

- [ ] ¿Existe un doc de dominio en lenguaje de negocio (componentes, modelo, flujos, conceptos)?
- [ ] ¿Los ciclos de vida están modelados como estados con transiciones declaradas?
- [ ] ¿Cada schema define una sola tabla?
- [ ] ¿Las constantes/enums están fuera del schema?
- [ ] ¿Las columnas están agrupadas por secciones en el orden estándar?
- [ ] ¿Dinero sin float, fechas tipadas, IDs estables, tenant id presente?
- [ ] ¿Las invariantes de negocio están escritas y tienen dónde hacerse cumplir?
- [ ] ¿Los saldos se derivan de un ledger append-only y se reconcilian?
- [ ] ¿Las referencias entre módulos son por ID, sin FK?

---

## Cuándo aplicar

- **Siempre / hoy (nivel 1):** documento de dominio y estados, una tabla por schema, columnas agrupadas, tipos canónicos, tenant id desde el inicio, ledger append-only para dinero e inventario, referencias entre módulos por ID.
- **Al crecer (nivel 2):** reconciliación programada de saldos contra el ledger, `CHECK` y restricciones únicas parciales como segunda barrera de las invariantes críticas.
- **Con varios servicios o equipos (nivel 3):** cada servicio es dueño exclusivo de sus tablas (nada compartido); los datos replicados entre servicios se mantienen por eventos con reconciliación explícita.
