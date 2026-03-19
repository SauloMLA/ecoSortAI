# Subcomité 01 — AI & Computer Vision

**Estado:** CONSTITUIDO  
**Sesión de creación:** S001  
**Enlace con equipo real:** Software Lead

---

## Objetivo

Lograr **clasificación funcional** de residuos con métricas reales y reducción de errores. El modelo debe funcionar en hardware embebido con latencia aceptable para el mecanismo de desvío.

## Alcance

- Selección y entrenamiento de modelo de clasificación
- Estrategia de dataset (recolección, etiquetado, aumentación)
- Optimización para inferencia en edge
- Evaluación rigurosa con métricas reales
- Identificación y reducción de errores sistemáticos

## Entregables esperados

| Entregable | Prioridad | Sesión objetivo |
|------------|-----------|-----------------|
| Estrategia de dataset | ALTA | S002–S003 |
| Selección de modelo base | ALTA | S002–S003 |
| Pipeline de entrenamiento | ALTA | S003–S004 |
| Métricas de evaluación definidas | ALTA | S002 |
| Modelo optimizado para edge | MEDIA | S004–S005 |
| Reporte de evaluación | ALTA | S005+ |

## Preguntas críticas que debe resolver

1. ¿Cuántas clases de residuos son viables con los datos disponibles?
2. ¿Qué modelo base es óptimo para el hardware objetivo?
3. ¿Cuál es la latencia de inferencia aceptable?
4. ¿Cómo se manejan objetos ambiguos o desconocidos?
5. ¿Cuál es el tamaño mínimo viable de dataset?

## Miembros

Ver `MEMBERS.md` para perfiles detallados.
