# Sesiones del Comité — Protocolo General

> Cada sesión es una unidad formal de trabajo del comité. Tiene apertura, desarrollo, cierre, y produce artefactos.

---

## Formato de sesión

### Código
```
SXXX — Secuencial (S001, S002, S003...)
```

### Carpeta
```
YYYY-MM-DD_SXXX_nombre-corto/
├── OPENING.md          ← Apertura formal por el Chair
├── CLOSING.md          ← Cierre formal por el Chair
└── artifacts/          ← Artefactos generados en la sesión
    └── [archivos]
```

### Nombre corto
Un identificador breve y descriptivo del objetivo de la sesión. Ejemplos:
- `inauguracion`
- `definicion-mvp`
- `arquitectura-sistema`
- `seleccion-hardware`
- `evaluacion-modelo`

---

## Ciclo de vida de una sesión

```
1. APERTURA      ← Chair declara abierta la sesión
   │               Objetivo definido
   │               Miembros convocados
   │
2. DESARROLLO    ← Discusión, análisis, debate
   │               Miembros se anuncian
   │               Se generan artefactos
   │
3. CIERRE        ← Chair declara cerrada la sesión
                    Decisiones registradas
                    Responsables asignados
                    Próximos pasos definidos
                    CURRENT_STATE.md actualizado
                    DECISION_LOG.md actualizado
```

## Requisitos obligatorios para cerrar

- [ ] Al menos una decisión registrada
- [ ] Responsables asignados a cada decisión/tarea
- [ ] Próximos pasos definidos
- [ ] Artefactos guardados en `artifacts/`
- [ ] `CURRENT_STATE.md` actualizado
- [ ] `DECISION_LOG.md` actualizado

## Sesiones existentes

| Código | Fecha | Nombre | Estado |
|--------|-------|--------|--------|
| S001 | 2026-02-12 | Inauguración | CERRADA |

## Plantilla

Ver `_template/` para la plantilla de apertura y cierre.
