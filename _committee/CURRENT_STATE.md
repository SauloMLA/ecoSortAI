# ESTADO ACTUAL — Comité EcoSort IA

> Este archivo refleja el **estado presente** del comité. Se actualiza al cierre de cada sesión.  
> No es un log — es un snapshot del momento actual.

**Última actualización:** 2026-02-13 (S003)  
**Sesión más reciente:** S003 — Modelo de IA y pruebas en laptop  
**Estado del comité:** ACTIVO — Modelo de IA entrenado y funcional

---

## Fase actual

| Campo | Valor |
|-------|-------|
| Fase del proyecto | 2 — Modelo funcional + validación en laptop |
| Fase siguiente | 3 — Validación con objetos reales + diseño mecánico confirmado |
| Bloqueos activos | Compra de hardware (pendiente), confirmación de motores para mecanismo |
| Riesgo principal | Precisión del modelo con objetos reales (entrenado con TrashNet, no con fotos propias) |

## Decisiones activas

| ID | Decisión | Sesión | Responsable | Estado |
|----|----------|--------|-------------|--------|
| D-001 | Constitución formal del comité | S001 | Chair | VIGENTE |
| D-002 | Estructura de 6 subcomités | S001 | Chair | VIGENTE |
| D-003 | Protocolo de sesiones | S001 | Chair | VIGENTE |
| D-004 | 4 categorías: plástico, papel, cartón, aluminio | S002 | Product Strategist | VIGENTE |
| D-005 | Raspberry Pi 5 (4GB) como plataforma | S002 | Software Lead | VIGENTE |
| D-006 | Inferencia edge (no nube) | S002 | Software Lead | VIGENTE |
| D-007 | MobileNetV2 + Transfer Learning + TFLite INT8 | S002 | Software Lead | VIGENTE |
| D-008 | Mecanismo flaps con servos SG90 | S002 | Mechanical Lead | SUPERSEDIDA por D-009 |
| D-009 | Rediseño v4: bote cuadrado + pirámide invertida | S002 | Mechanical Lead | VIGENTE |
| D-010 | Corrección de config mismatch en scripts | S003 | Chair | VIGENTE |
| D-011 | Código del mecanismo como TODO hasta diseño final | S003 | Mechanical Lead | VIGENTE |
| D-012 | Dataset TrashNet como base de entrenamiento | S003 | Software Lead | VIGENTE |
| D-013 | Entorno virtual Python (venv/) como estándar | S003 | Software Lead | VIGENTE |
| D-014 | Prioridad: IA primero, mecanismo después | S003 | Chair / equipo | VIGENTE |

## Equipo real — Estado de asignaciones

| Rol | Asignación actual | Estado |
|-----|-------------------|--------|
| Software Lead | Modelo entrenado, test con webcam listo, probar con objetos reales | LISTO PARA VALIDAR |
| Mechanical Lead | Confirmar motores del diseño v4, diseño CAD | PENDIENTE |
| Physical Integrator | Pendiente hasta que llegue hardware | ESPERANDO |
| Documentation Ops | Pendiente de definir en S004 | ESPERANDO |
| QA / Red Team | Puede comenzar validación del modelo con objetos reales | DISPONIBLE |

## Artefactos producidos

### Sesiones anteriores (S001-S002)
- [x] Diagrama de visión general del sistema
- [x] Evaluación de RPi 5 con BOM
- [x] Listas de compras Amazon México y USA
- [x] Documento de arquitectura del modelo de IA
- [x] Diseño de mecanismo v4 (bote cuadrado + pirámide invertida)

### Sesión S003
- [x] Script `src/training/download_dataset.py` — descarga automática de dataset
- [x] Dataset descargado en `dataset/` (3,778 imágenes, 4 categorías)
- [x] Modelo entrenado `models/ecosort_model.keras` (~95.8% val accuracy)
- [x] Modelos TFLite: `ecosort_model.tflite` y `ecosort_model_int8.tflite`
- [x] Gráfica de entrenamiento `models/training_history.png`
- [x] Script `test_with_webcam.py` con clasificación real (modelo TFLite)
- [x] Entorno virtual `venv/` configurado
- [x] Bugs corregidos en todos los scripts

### Pendientes
- [ ] Validación del modelo con objetos reales (no solo dataset)
- [ ] Diseño CAD del mecanismo v4
- [ ] Confirmación de motores (equipo real)
- [ ] Documento de definición formal del MVP
- [ ] Plan de testing formal

## Cómo probar el sistema (laptop)

```bash
# 1. Activar entorno virtual
cd "practice folder/trash-bot"
source venv/bin/activate

# 2. Simulación pura (sin cámara, sin modelo)
python src/test_simulation.py

# 3. Webcam con clasificación REAL
python src/test_with_webcam.py

# 4. Inferencia completa (con o sin cámara)
python src/inference/classify.py
```

## Próximos pasos

1. **Equipo real:** Probar clasificación con webcam usando objetos reales de reciclaje
2. **Software Lead:** Si la precisión no es suficiente, complementar dataset con fotos propias
3. **Mechanical Lead:** Confirmar motores del diseño v4 y comenzar diseño CAD
4. **S004:** Revisión de resultados de pruebas + diseño mecánico

## Presupuesto estimado

| Concepto | Rango MXN |
|----------|-----------|
| Hardware + electrónica | $2,960 – $4,150 |
| Materiales mecánicos | $500 – $1,000 (estimado) |
| **Total** | **$3,460 – $5,150 MXN** |
