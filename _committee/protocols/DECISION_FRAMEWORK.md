# Marco de Toma de Decisiones — Comité EcoSort IA

> Cómo se toman, registran y ejecutan las decisiones del comité.

---

## 1. Tipos de decisiones

| Tipo | Ejemplos | Quién decide | Registro |
|------|----------|-------------|----------|
| **Estratégica** | Alcance del MVP, fases del proyecto | Chair + Leadership | DECISION_LOG.md |
| **Técnica** | Selección de modelo, hardware, materiales | Subcomité + Technical Director | DECISION_LOG.md |
| **Operativa** | Asignación de tareas, fechas límite | Chair | DECISION_LOG.md |
| **De diseño** | UX, estructura mecánica, dashboard | Subcomité relevante | Sesión + artifacts |

## 2. Proceso de decisión

```
┌─────────────────────────────────────────────────┐
│  1. IDENTIFICACIÓN                               │
│     ¿Qué se necesita decidir?                    │
│     ¿Por qué es necesario ahora?                 │
│     ¿Quién debe participar?                      │
├─────────────────────────────────────────────────┤
│  2. ANÁLISIS                                     │
│     Opciones identificadas                       │
│     Evidencia técnica presentada                 │
│     Riesgos evaluados por cada opción            │
│     Postura crítica incluida                     │
├─────────────────────────────────────────────────┤
│  3. DELIBERACIÓN                                 │
│     Debate entre miembros                        │
│     Contraargumentos considerados                │
│     Trade-offs explícitos                        │
│     Métricas de éxito definidas                  │
├─────────────────────────────────────────────────┤
│  4. DECISIÓN                                     │
│     Chair sintetiza y declara decisión           │
│     Justificación documentada                    │
│     Responsable asignado                         │
│     Métricas de éxito confirmadas                │
├─────────────────────────────────────────────────┤
│  5. REGISTRO                                     │
│     Entrada en DECISION_LOG.md                   │
│     CURRENT_STATE.md actualizado                 │
│     Equipo real notificado si aplica             │
└─────────────────────────────────────────────────┘
```

## 3. Criterios de evaluación

Toda decisión técnica debe evaluarse contra estos criterios:

| Criterio | Peso | Descripción |
|----------|------|-------------|
| Viabilidad | ALTO | ¿El equipo real puede ejecutar esto? |
| Impacto en MVP | ALTO | ¿Contribuye directamente al prototipo funcional? |
| Riesgo | ALTO | ¿Cuál es la probabilidad y severidad de fallo? |
| Costo | MEDIO | ¿Es viable con el presupuesto disponible? |
| Tiempo | MEDIO | ¿Se puede completar en el timeline del proyecto? |
| Complejidad | MEDIO | ¿Es proporcionalmente simple para el valor que agrega? |
| Defendibilidad | MEDIO | ¿Fortalece la defensa académica? |

## 4. Formato de registro

Toda decisión se registra en `DECISION_LOG.md` con:

```markdown
### D-XXX — [Título]
- **Sesión:** SXXX
- **Fecha:** YYYY-MM-DD
- **Decisión:** [Qué se decidió]
- **Justificación:** [Por qué]
- **Alternativas descartadas:** [Qué se consideró y por qué no]
- **Responsable:** [Quién ejecuta]
- **Métricas de éxito:** [Cómo se mide si fue buena decisión]
- **Estado:** VIGENTE | SUPERSEDIDA | REVOCADA
```

## 5. Revisión de decisiones

Una decisión vigente puede ser **revisada** si:

1. Nueva evidencia contradice la justificación original
2. Las circunstancias del proyecto cambiaron significativamente
3. La métrica de éxito no se cumple

La revisión requiere:
- Sesión formal
- Presentación de evidencia nueva
- Decisión de superceder o revocar registrada en DECISION_LOG.md
- La decisión original se marca como SUPERSEDIDA o REVOCADA

## 6. Decisiones de emergencia

Si se requiere una decisión fuera de sesión formal:

1. El Chair puede tomar decisiones operativas urgentes
2. Se documenta en la siguiente sesión formal
3. Se registra con nota: "Decisión de emergencia — ratificada en SXXX"
