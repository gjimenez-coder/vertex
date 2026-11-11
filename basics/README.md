# Principios de Ingeniería (reutilizables)

Documentación de **principios genéricos por dominio**, destilados de proyectos reales pero **desacoplados de cualquier stack**. Son reglas que viajan entre proyectos; la implementación concreta se re-ancla en cada uno.

## Diferencia con los steering de proyecto

- Los MDs de la **raíz** (`01-frontend.md`, `02-backend.md`, …) son steering **atados a un proyecto** (`kardex/**`, `soliana/**`), con `inclusion: fileMatch`. Contienen la *implementación* específica.
- Los MDs de **esta carpeta** son los *principios* detrás de esos steering, en forma genérica y reutilizable, con `inclusion: manual`.

## Índice

**Diseño y estructura**
| Dominio | Documento |
|---|---|
| Arquitectura de software | [arquitectura-software.md](arquitectura-software.md) |
| Modelado de dominio y schemas | [modelado-dominio.md](modelado-dominio.md) |

**Capas de aplicación**
| Dominio | Documento |
|---|---|
| Backend | [backend.md](backend.md) |
| Frontend | [frontend.md](frontend.md) |
| APIs HTTP | [apis.md](apis.md) |

**Transversales (cross-cutting)**
| Dominio | Documento |
|---|---|
| Seguridad | [seguridad.md](seguridad.md) |
| Manejo de errores y resiliencia | [manejo-errores.md](manejo-errores.md) |
| Observabilidad | [observabilidad.md](observabilidad.md) |
| Performance | [performance.md](performance.md) |
| Fechas y zonas horarias | [fechas-timezones.md](fechas-timezones.md) |

**Proceso y entrega**
| Dominio | Documento |
|---|---|
| Testing | [testing.md](testing.md) |
| CI/CD | [cicd.md](cicd.md) |

## Molde común

Todos los documentos siguen el mismo formato:

```markdown
---
inclusion: manual
---

# <Dominio> — Principios Reutilizables

> Alcance: <qué cubre>. Los ejemplos son ilustrativos.

## <N. Principio>
- Regla imperativa y corta.
  ✅ ejemplo correcto
  ❌ antipatrón

## Prohibido
- Antipatrones concretos.

## Checklist
- [ ] ...

## Cuándo aplicar
- **Siempre / hoy (nivel 1):** ...
- **Al crecer (nivel 2):** ...
- **Con varios servicios o equipos (nivel 3):** ...
```

**Convenciones:**
- Reglas cortas e imperativas ("nunca", "siempre", "debe").
- Bloques `✅ / ❌` con ejemplos.
- Tablas de contrato cuando aplique.
- Secciones "Prohibido", "Checklist" y **"Cuándo aplicar"** al cierre, en ese orden y en todos los documentos.

## Una regla, una fuente

- Cada regla se **define en un solo documento**. Los demás la enlazan con una línea (`Ver backend.md §6`) y no la repiten.
- Antes de añadir una regla, busca si ya existe (`grep` de la frase clave). Si existe, amplíala en su sitio.
- Prohibido y Checklist solo listan lo que el propio documento define; lo enlazado no se repite.

| Regla | Fuente única |
|---|---|
| Capas, dependencias entre módulos, transacciones, handlers solo con Services | `arquitectura-software.md` |
| Autoría `'system'` en procesos automáticos, configuración y TTLs, migraciones | `backend.md` |
| Fechas e instantes | `fechas-timezones.md` |
| Formato de error HTTP y versionado de API | `apis.md` |
| Resiliencia (timeouts, reintentos, límites de carga) | `manejo-errores.md` |
| Sesión, XSS, inyección, CORS, secretos | `seguridad.md` |

## "Cuándo aplicar": la escala del negocio

No todo principio aplica desde el primer día. Cada documento cierra con una sección "Cuándo aplicar" que dice qué es obligatorio hoy y qué se pospone, usando estos niveles:

| Nivel | Situación típica |
|---|---|
| **1 — Hoy** | Una persona desarrollando, un servicio, una instancia o pocas, un solo entorno de producción, cientos de usuarios al día. |
| **2 — Al crecer** | Varias instancias o más de una persona, entorno de staging, miles de usuarios al día, primeros clientes que dependen de la API. |
| **3 — Varios servicios o equipos** | Más de un servicio desplegable, más de un equipo, consumidores externos de la API, tráfico alto y sostenido. |

Reglas de uso:
- Lo marcado **Siempre / hoy** es obligatorio en cualquier proyecto.
- Lo marcado **Al crecer** o **Con varios servicios** se adopta cuando se cumple el umbral; antes es sobreingeniería (YAGNI). Si te acercas al umbral, planifícalo, no lo adelantes.
- Si una regla de un nivel superior es barata y evita un riesgo caro (por ejemplo timeouts), se adopta antes y la sección lo dice.

## Cómo re-anclar un principio en un proyecto

1. Crea o edita el steering del proyecto (`fileMatch` con el patrón del proyecto).
2. Copia solo la **implementación** (nombres de archivos, librerías, comandos) y enlaza el principio: `Principio base: vertex/basics/<documento>.md`.
3. No dupliques el principio en el steering; si el proyecto lo contradice, documenta la excepción con motivo y fecha de revisión.
4. Al cambiar un principio aquí, revisa los steering que lo referencian.

**Qué cargar automáticamente:** `seguridad.md` y `manejo-errores.md` son los candidatos a `inclusion: fileMatch`, porque su omisión es la que más cuesta (secretos, timeouts, XSS). El resto queda `manual` para no inflar el contexto en cada edición.
