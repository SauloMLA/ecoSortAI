# REGISTRO CENTRAL DE DECISIONES — Comité EcoSort IA

> Toda decisión tomada en sesión formal se registra aquí.  
> Las decisiones son vinculantes salvo revisión formal en sesión posterior.

---

## Formato de registro

```
### D-XXX — [Título breve]
- **Sesión:** SXXX
- **Fecha:** YYYY-MM-DD
- **Decisión:** [Descripción clara]
- **Justificación:** [Por qué se tomó]
- **Responsable:** [Quién ejecuta o supervisa]
- **Estado:** VIGENTE | SUPERSEDIDA | REVOCADA
- **Notas:** [Opcional]
```

---

## Decisiones registradas

### D-001 — Constitución formal del comité
- **Sesión:** S001
- **Fecha:** 2026-02-12
- **Decisión:** Se constituye formalmente el Comité Ejecutivo Híbrido para el Desarrollo del Prototipo EcoSort IA
- **Justificación:** Necesidad de estructura de gobernanza para coordinar el desarrollo del prototipo
- **Responsable:** Chair
- **Estado:** VIGENTE

### D-002 — Adopción de estructura de 6 subcomités
- **Sesión:** S001
- **Fecha:** 2026-02-12
- **Decisión:** Se adopta la estructura de 6 subcomités especializados: AI & CV, Hardware & Embedded, Diseño Mecánico, Software & Dashboard, Testing & Red Team, Estrategia Académica
- **Justificación:** Cobertura completa de las dimensiones técnicas del prototipo
- **Responsable:** Chair
- **Estado:** VIGENTE

### D-003 — Adopción de protocolo de sesiones
- **Sesión:** S001
- **Fecha:** 2026-02-12
- **Decisión:** Se adopta el protocolo formal de sesiones con apertura/cierre por el Chair, registro obligatorio de decisiones, y actualización de estado
- **Justificación:** Garantizar trazabilidad y rigor en el proceso de toma de decisiones
- **Responsable:** Chair / Session Clerk
- **Estado:** VIGENTE

### D-004 — Categorías de clasificación: 4 tipos
- **Sesión:** S002
- **Fecha:** 2026-02-12
- **Decisión:** Las categorías de clasificación del MVP son: plástico, papel, cartón, aluminio (4 categorías)
- **Justificación:** Son los materiales reciclables más comunes en contexto universitario mexicano, visualmente distinguibles, y 4 categorías es viable para el modelo y el mecanismo
- **Alternativas descartadas:** 5 categorías (orgánico + no reciclable añadían complejidad mecánica y de dataset sin valor proporcional para el MVP)
- **Responsable:** Product Strategist / Software Lead
- **Estado:** VIGENTE

### D-005 — Raspberry Pi 5 (4GB) como plataforma
- **Sesión:** S002
- **Fecha:** 2026-02-12
- **Decisión:** Se adopta Raspberry Pi 5 de 4GB como plataforma embebida del prototipo
- **Justificación:** Suficiente para MobileNetV2 INT8 (~50-100ms), precio accesible (~$1,800 MXN), GPIO disponible, ruta de escape con AI HAT
- **Alternativas descartadas:** Jetson Nano (caro, complejo), RPi 4 (más lenta), ESP32 (insuficiente para IA)
- **Responsable:** Software Lead / Embedded Engineer
- **Estado:** VIGENTE

### D-006 — Inferencia en edge (no en la nube)
- **Sesión:** S002
- **Fecha:** 2026-02-12
- **Decisión:** El modelo de IA se ejecuta localmente en la Raspberry Pi 5, no en la nube
- **Justificación:** Independencia de WiFi, latencia baja (~100ms vs ~1-2s), cero costo operativo, robustez en demo ante jurado
- **Responsable:** Software Lead
- **Estado:** VIGENTE

### D-007 — MobileNetV2 + Transfer Learning como modelo base
- **Sesión:** S002
- **Fecha:** 2026-02-12
- **Decisión:** Se usará MobileNetV2 pre-entrenado con Transfer Learning, cuantizado a INT8 vía TFLite
- **Justificación:** Mejor balance precisión/velocidad para RPi 5 (~3-4 MB, ~50-100ms), ampliamente documentado, compatible con TFLite
- **Alternativas descartadas:** EfficientNet (más lento), YOLOv8 (overkill para clasificación), ResNet50 (demasiado pesado)
- **Responsable:** Software Lead / ML Researcher
- **Estado:** VIGENTE

### D-008 — Mecanismo de desvío por flaps con servos
- **Sesión:** S002
- **Fecha:** 2026-02-12
- **Decisión:** El mecanismo de desvío usa 4 flaps servo-accionados (SG90) que dirigen objetos por gravedad a 4 contenedores
- **Justificación:** Simple, barato, suficiente para objetos ligeros de reciclaje, fácil de prototipar
- **Responsable:** Mechanical Lead / Physical Integrator
- **Estado:** SUPERSEDIDA por D-009

### D-009 — Rediseño: Bote cuadrado con pirámide invertida (v4)
- **Sesión:** S002 (revisión del Chair)
- **Fecha:** 2026-02-13
- **Decisión:** Se adopta diseño v4: bote de forma cuadrada (50×50×80 cm) con 4 compuertas inclinadas a 45° formando una pirámide invertida. Cada compuerta es controlada por un servo SG90 independiente (4 servos total). Movimiento simple: 0° cerrado, 90° abierto. Sustituye diseños v1-v3.
- **Justificación:** Los diseños anteriores (v1: flaps laterales, v2: rampa giratoria cilíndrica, v3: bandeja giratoria Ameru) presentaron dificultades para que el equipo mecánico comprendiera el movimiento de los servos. El diseño v4 prioriza claridad mecánica (movimiento de 0° a 90°), facilidad de fabricación (forma cuadrada = cortes rectos en MDF), y menor costo.
- **Alternativas descartadas:** v2 cilíndrica con MG996R (difícil fabricar cilindro, movimiento complejo), v3 Ameru con NEMA 17 (stepper costoso, rotación continua innecesaria)
- **Responsable:** Mechanical Lead / Physical Integrator
- **Estado:** VIGENTE
- **Artefacto:** `S002_doc_mechanism-design-v4.md`

### D-010 — Corrección de config mismatch v2→v3 en scripts
- **Sesión:** S003
- **Fecha:** 2026-02-13
- **Decisión:** Se corrigieron los imports rotos en `test_simulation.py`, `test_with_webcam.py` y `classify.py` que referenciaban variables del diseño v2 (SERVO_RAMPA_*, SERVO_PLATAFORMA_*) eliminadas de config.py
- **Justificación:** Ningún script podía ejecutarse debido a ImportError
- **Responsable:** Chair
- **Estado:** VIGENTE

### D-011 — Código del mecanismo físico queda como TODO
- **Sesión:** S003
- **Fecha:** 2026-02-13
- **Decisión:** Todo el código de mecanismo físico (motores, servos, GPIO) en classify.py queda como TODO. No se implementa hasta que el diseño mecánico esté aprobado y se confirme qué motores se usarán.
- **Justificación:** Solicitud directa del equipo real. El diseño mecánico (D-009 v4) está definido pero el equipo aún no confirma los motores finales.
- **Responsable:** Mechanical Lead / equipo real
- **Estado:** VIGENTE

### D-012 — Dataset TrashNet como base de entrenamiento
- **Sesión:** S003
- **Fecha:** 2026-02-13
- **Decisión:** Se adopta el dataset TrashNet (Stanford/garythung) descargado desde Hugging Face como dataset base. 3,778 imágenes mapeadas a las 4 categorías del proyecto (cardboard→cartón, paper→papel, plastic→plástico, metal→aluminio). Glass y trash ignorados.
- **Justificación:** Dataset público gratuito, categorías compatibles, permite entrenar modelo funcional sin recolección manual. Se complementará con fotos propias más adelante.
- **Responsable:** Software Lead
- **Estado:** VIGENTE

### D-013 — Entorno virtual Python como estándar
- **Sesión:** S003
- **Fecha:** 2026-02-13
- **Decisión:** Se usa `venv/` como entorno virtual estándar del proyecto. Activar con `source venv/bin/activate`.
- **Justificación:** macOS requiere entornos virtuales (PEP 668). Garantiza reproducibilidad.
- **Responsable:** Software Lead
- **Estado:** VIGENTE

### D-014 — Prioridad: IA primero, mecanismo después
- **Sesión:** S003
- **Fecha:** 2026-02-13
- **Decisión:** El orden de trabajo es: (1) modelo de IA funcional y validado, (2) diseño mecánico confirmado, (3) integración hardware. No se escribe código de mecanismo hasta tener diseño aprobado por el equipo.
- **Justificación:** Solicitud del equipo real. Permite demostrar avances en clasificación antes de tener hardware físico.
- **Responsable:** Chair / equipo real
- **Estado:** VIGENTE
