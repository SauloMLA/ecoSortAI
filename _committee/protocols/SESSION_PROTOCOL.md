# Protocolo de Sesiones — Comité EcoSort IA

> Protocolo completo para apertura, desarrollo y cierre de sesiones formales.

---

## 1. Pre-sesión

### Responsable: Chair + Session Clerk

| Paso | Acción | Responsable |
|------|--------|-------------|
| 1 | Definir objetivo de la sesión | Chair |
| 2 | Crear carpeta de sesión `YYYY-MM-DD_SXXX_nombre/` | Session Clerk |
| 3 | Generar `OPENING.md` desde template | Session Clerk |
| 4 | Identificar miembros/subcomités a convocar | Chair |
| 5 | Revisar `CURRENT_STATE.md` para contexto | Chair |

## 2. Apertura

### Responsable: Chair

El Chair abre formalmente la sesión con la siguiente declaración:

```
"Declaro abierta la sesión [SXXX].
Fecha: [fecha].
Objetivo: [objetivo claro].
Miembros convocados: [lista].
Procederemos con [agenda resumida]."
```

**Requisitos de apertura:**
- Objetivo claro y específico
- Agenda definida
- Miembros convocados identificados
- Contexto establecido (referencia a estado actual)

## 3. Desarrollo

### Dinámica

Durante el desarrollo, el comité opera en **modo dinámico**:

- El Chair dirige el flujo general
- Los miembros se anuncian antes de hablar (ver `INTERACTION_RULES.md`)
- Se permiten debates intensos y pensamiento crítico
- Se genera evidencia, artefactos y propuestas
- El Chair puede redirigir si se pierde el foco

### Bloques de trabajo típicos

```
Bloque 1: Presentación del problema/tema
  └→ Miembro presenta análisis
  └→ Postura crítica responde
  └→ Debate y convergencia
  └→ Chair resume posición

Bloque 2: Propuestas de solución
  └→ Subcomité presenta opciones
  └→ Technical Director valida
  └→ Product Strategist evalúa alcance
  └→ Debate y selección
  └→ Chair registra decisión

Bloque 3: Asignación y próximos pasos
  └→ Chair asigna responsables
  └→ Se definen fechas y criterios
  └→ Se documentan artefactos
```

## 4. Cierre

### Responsable: Chair + Session Clerk + State Keeper

El Chair cierra formalmente la sesión:

```
"Declaro cerrada la sesión [SXXX].
Se tomaron [N] decisiones.
Se asignaron [N] tareas.
Próxima sesión prevista: [SXXX+1] — [tema tentativo]."
```

### Checklist de cierre obligatorio

| # | Verificación | Responsable |
|---|-------------|-------------|
| 1 | ¿Se registraron todas las decisiones? | Session Clerk |
| 2 | ¿Se asignaron responsables a cada decisión/tarea? | Chair |
| 3 | ¿Se definieron próximos pasos? | Chair |
| 4 | ¿Se guardaron artefactos en `artifacts/`? | Artifact Manager |
| 5 | ¿Se generó `CLOSING.md`? | Session Clerk |
| 6 | ¿Se actualizó `DECISION_LOG.md`? | Session Clerk |
| 7 | ¿Se actualizó `CURRENT_STATE.md`? | State Keeper |

**Ninguna sesión puede cerrarse sin cumplir TODOS los puntos del checklist.**

## 5. Post-sesión

| Paso | Acción | Responsable |
|------|--------|-------------|
| 1 | Verificar integridad de artefactos | Artifact Manager |
| 2 | Confirmar coherencia de CURRENT_STATE.md | State Keeper |
| 3 | Actualizar README de sesiones con nueva entrada | Session Clerk |
