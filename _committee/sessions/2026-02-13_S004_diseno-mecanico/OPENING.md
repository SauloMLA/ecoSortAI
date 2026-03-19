# APERTURA DE SESION — S004

**Fecha:** 2026-02-13  
**Codigo:** S004  
**Nombre:** Diseño mecánico — del concepto al CAD  
**Chair:** Chair del Comité EcoSort IA

---

## Declaracion de apertura

> "Declaro abierta la sesión S004.  
> Fecha: 13 de febrero de 2026.  
> Objetivo: Finalizar el diseño mecánico del EcoSort IA — resolver todas las preguntas abiertas del diseño v4, producir especificaciones CAD-ready, y generar un FMEA del mecanismo.  
> Miembros convocados: Subcomité completo de Diseño Mecánico & Materiales, Technical Director, Mechanical Lead.  
> Procederemos con: (1) revisión crítica del diseño v4, (2) resolución de problemas dimensionales y de montaje, (3) especificaciones de corte y ensamblaje, (4) FMEA del mecanismo, (5) plan de fabricación."

## Objetivo de la sesion

Transformar el diseño conceptual v4 (documento `S002_doc_mechanism-design-v4.md`) en especificaciones precisas y fabricables. Al cierre de esta sesión debemos tener:

1. Dimensiones finales verificadas por ingeniería
2. Detalles de montaje de servos resueltos (posición exacta del eje, agujero en pared, horn)
3. Geometría exacta de las 4 solapas triangulares
4. Diseño del arco de cámara
5. Sistema de contenedores internos
6. Análisis FMEA del mecanismo
7. Lista de cortes para fabricación en MDF
8. BOM final actualizado

## Agenda

1. **Bloque 1:** Revisión crítica del diseño v4 — ¿qué funciona y qué tiene problemas?
2. **Bloque 2:** Ingeniería de detalle — dimensiones, tolerancias, montaje de servos
3. **Bloque 3:** Geometría de solapas y cinemática de apertura/cierre
4. **Bloque 4:** Arco de cámara y montaje de electrónica
5. **Bloque 5:** Contenedores internos y acceso para vaciado
6. **Bloque 6:** FMEA — modos de fallo y mitigaciones
7. **Bloque 7:** Plan de cortes y lista de materiales final
8. Cierre: decisiones, responsables, próximos pasos

## Miembros convocados

| Rol / Subcomité | Razón de convocatoria |
|-----------------|----------------------|
| CAD Architect | Diseño paramétrico, planos de corte, ensamblaje |
| Mechanical Engineer | Análisis de torque, cinemática de solapas, montaje de servos |
| Materials Scientist | Selección final de materiales (MDF vs acrílico vs PLA) |
| Anti-Jam Specialist | Geometría anti-atasco, ángulos de deslizamiento |
| Structural Analyst | Estabilidad del bote, peso, puntos de estrés |
| Rapid Prototyping Expert | Viabilidad de fabricación, optimización de cortes |
| Failure Mode Analyst | FMEA completo del mecanismo |
| Technical Director | Validación técnica general |
| Mechanical Lead (equipo real) | Enlace con capacidades reales de fabricación |

## Contexto

- **Diseño vigente:** v4 — Bote cuadrado 40x40x70 cm, pirámide invertida con 4 solapas, 4 servos SG90 (D-009)
- **Documento base:** `S002_doc_mechanism-design-v4.md`
- **IA lista:** Modelo entrenado con ~95.8% accuracy, TFLite INT8 listo para RPi 5
- **Pendientes clave:** Confirmación de motores (SG90 vs otro), diseño CAD, detalles de montaje
- **Presupuesto estructura:** $750 - $1,340 MXN

## Restricciones / Notas

- El equipo real tiene acceso a cortadora láser (posible) e impresión 3D
- Prioridad: diseño simple, fabricable, sin herramientas especializadas
- Los servos SG90 están en el BOM pero no se han comprado — hay oportunidad de cambiar si se justifica
- El diseño debe ser presentable ante jurado académico
