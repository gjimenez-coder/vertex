---
inclusion: manual
---

# CI/CD — Principios Reutilizables

> Alcance: integración y entrega continua: pipeline, despliegue, versionado y rollback. Independiente de herramienta (GitHub Actions, GitLab CI, Cloud Build, etc.). Complementa `testing.md`, `seguridad.md` y `observabilidad.md`.

---

## 1. Build y pipeline reproducibles

- El build produce el **mismo artefacto** dado el mismo commit: dependencias **fijadas** (lockfile con instalación congelada: `--frozen-lockfile`, `npm ci`), sin estado oculto de la máquina.
- El pipeline corre en **cada push/PR** y es la fuente de verdad de "¿esto está sano?", no la máquina del dev.
- Ordena las etapas de rápida a lenta y **falla temprano**: lint → typecheck → build → tests → empaquetado. Un fallo detiene el pipeline.
- Mantén el pipeline **rápido**: cachea dependencias, paraleliza, y evita trabajo redundante. Un CI lento se evita o se saltea.
- Fija también las **imágenes base** (por versión o digest) y reconstrúyelas con regularidad para recibir parches.

```
✅  install (cache, frozen) → lint → typecheck → test → build → scan → deploy
❌  pipeline de 40 min que el equipo aprende a ignorar
```

---

## 2. Quality gates automáticos

- El merge a la rama principal exige que el pipeline esté **verde**: no se mergea en rojo.
- Automatiza las verificaciones que importan: linters, type checking, tests de la escala elegida (ver `testing.md`), **escaneo de secretos** y **auditoría de dependencias** contra bases de CVE (ver `seguridad.md` §13 y §14).
- Falla el build ante una vulnerabilidad de severidad alta o un secreto detectado; las excepciones se documentan con motivo y fecha.
- Prohíbe saltarse los checks (`--no-verify`, deshabilitar gates) salvo decisión explícita y documentada.

---

## 3. Un artefacto, muchos entornos

- **Compila una vez, promueve el mismo artefacto** por los entornos (dev → staging → prod). No recompiles por entorno: lo que probaste es lo que despliegas.
- La diferencia entre entornos es **configuración**, no código ni build distintos. (Manejo de config en `backend.md` §6.)
- Los **secretos** nunca viven en el repo ni en el artefacto: se inyectan en el entorno desde un gestor de secretos. (Ver `seguridad.md` §13.)
- **Si tienes un solo entorno** (producción), la regla se adapta, no se abandona: el artefacto sale del pipeline con tests en verde, se **etiqueta con el commit**, y conservas la revisión anterior para poder volver a ella.

---

## 4. Despliegues seguros y reversibles

- Prefiere estrategias **sin downtime** y de bajo riesgo: rolling, blue-green o canary según el caso. Para el usuario el "downtime planificado" es downtime.
- Todo despliegue debe tener un **rollback rápido** definido de antemano (revisión anterior, tag previo). Si no puedes revertir, no deberías desplegar.
- **Durante un despliegue conviven dos versiones del código.** El esquema de datos y los eventos deben funcionar con ambas.

### Migraciones: expand / contract

Las migraciones son compatibles hacia atrás y se separan del deploy de código cuando sea posible:

1. **Expand** (antes del código): solo cambios aditivos. Tablas nuevas, columnas **nullable**, índices, vistas. La versión actual del código no los usa y no se rompe.
2. **Despliega el código** que usa lo nuevo (y todavía tolera lo viejo).
3. **Contract** (después de que todas las instancias corren el código nuevo): elimina columnas y tablas en desuso, añade `NOT NULL` y restricciones nuevas.

- Para dividir una tabla o mover datos, la versión intermedia escribe en ambos lados (o usa triggers incondicionales) hasta completar el cambio.
- Prueba la migración con datos realistas (incluidos `NULL` y registros viejos).
- **Generar** una migración es una decisión revisada por una persona (ver `backend.md` §5). **Aplicarla** ya revisada puede automatizarse en el pipeline.

### Salud tras el deploy

- Verifica salud con health checks y métricas después de desplegar; automatiza el rollback si se degradan. (Ver `observabilidad.md`.)
- El servicio debe arrancar como "no disponible" hasta estar listo (readiness) y drenar las peticiones en curso al apagarse.

---

## 5. Versionado y trazabilidad

- Cada release es **trazable** a un commit y versionada (ej. SemVer o tag inmutable). Debes poder responder "¿qué código corre en producción?".
- Cambios pequeños y frecuentes antes que entregas grandes y riesgosas: menos superficie para fallar, rollback más simple. "Si duele, hazlo más seguido."
- Usa **feature flags** para separar *deploy* (poner el código) de *release* (activar la función) y para apagar algo sin redeploy. Los flags nuevos nacen apagados y se retiran cuando la función es estable.

---

## 6. Automatiza lo repetible

- Si un paso manual se repite (empaquetar, publicar, **aplicar** una migración ya revisada), **automatízalo** en el pipeline: lo manual es lento y propenso a error humano.
- Lo que requiere **juicio humano** (generar y revisar una migración, aprobar un cambio de infraestructura destructivo) no se automatiza a ciegas; se automatiza su ejecución una vez aprobado.
- Infraestructura como código cuando aplique: entornos reproducibles y versionados, no configurados a mano. Protege su estado (puede contener secretos).

---

## Prohibido

- Mergear a la rama principal con el pipeline en rojo.
- Saltarse los quality gates sin justificación documentada.
- Recompilar un artefacto distinto por entorno.
- Secretos en el repositorio o embebidos en el artefacto.
- Desplegar sin un rollback definido.
- Dependencias sin fijar (builds no reproducibles) o `install` que actualiza el lockfile en CI.
- Migraciones no compatibles hacia atrás desplegadas junto con el código que las necesita.
- Generar migraciones automáticamente sin revisión humana.

---

## Checklist

- [ ] ¿El build es reproducible (lockfile congelado, imágenes base fijadas)?
- [ ] ¿El pipeline corre en cada push/PR y falla temprano?
- [ ] ¿El merge exige pipeline verde, con lint/typecheck/test y escaneo de secretos y dependencias?
- [ ] ¿Se compila una vez y se promueve el mismo artefacto (o, con un solo entorno, se etiqueta y se conserva la revisión anterior)?
- [ ] ¿La diferencia entre entornos es solo configuración, con secretos inyectados?
- [ ] ¿El despliegue es sin downtime y con rollback rápido definido?
- [ ] ¿Las migraciones siguen expand/contract y toleran dos versiones del código?
- [ ] ¿Cada release es trazable a un commit y versionada?
- [ ] ¿Se usan feature flags para separar deploy de release?

---

## Cuándo aplicar

- **Siempre / hoy (nivel 1):** pipeline en cada push con lint, typecheck, tests de los caminos críticos y build; lockfile congelado; escaneo de secretos y de dependencias; imágenes etiquetadas por commit; rollback a la revisión anterior definido; migraciones expand/contract y revisión humana de cada migración. Aunque haya un solo entorno y una instancia, durante el deploy conviven dos versiones.
- **Al crecer (nivel 2):** entorno de staging, promoción del mismo artefacto, aplicación automática de migraciones ya revisadas en el pipeline, feature flags para funciones grandes, canary o rolling gradual, rollback automático por métricas.
- **Con varios servicios o equipos (nivel 3):** pipelines por servicio con contract tests entre ellos, despliegues independientes y versionado de contratos, orquestación de la ventana de compatibilidad entre versiones, infraestructura inmutable.
