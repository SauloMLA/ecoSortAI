# CIERRE DE SESION — S003

**Fecha:** 2026-02-13  
**Codigo:** S003  
**Nombre:** Modelo de IA y pruebas en laptop  
**Chair:** Chair del Comite EcoSort IA

---

## Resumen de la sesion

Sesion enfocada en hacer funcional el pipeline de clasificacion de IA y demostrar que el sistema puede probarse en una laptop comun sin hardware especializado.

## Decisiones tomadas

### D-009 — Correccion de config mismatch (v2 → v3)
- **Descripcion:** Se corrigieron los imports rotos en `test_simulation.py`, `test_with_webcam.py` y `classify.py` que referenciaban variables del diseno v2 (servos) que ya no existen en `config.py` (actualizado a v3).
- **Justificacion:** Ningun script podia ejecutarse.
- **Responsable:** Chair (ejecucion directa)

### D-010 — Codigo del mecanismo fisico queda como TODO
- **Descripcion:** El codigo de `classify.py` relacionado con el mecanismo fisico (motores, servos, GPIO) queda marcado como `TODO` hasta que el diseno mecanico este finalizado y se haya decidido que motores usar.
- **Justificacion:** Solicitud directa del equipo real. No hay decision sobre motores todavia (D-008 establece flaps con SG90, pero el config se actualizo a stepper — hay inconsistencia pendiente de resolver).
- **Responsable:** Mechanical Lead / equipo real

### D-011 — Dataset TrashNet como base de entrenamiento
- **Descripcion:** Se adopta el dataset TrashNet (Stanford/garythung) descargado de Hugging Face como dataset base para el entrenamiento inicial. Se descargaron 3,778 imagenes mapeadas a las 4 categorias del proyecto.
- **Mapeo:**
  - cardboard (806 imgs) → carton
  - paper (1,188 imgs) → papel
  - plastic (964 imgs) → plastico
  - metal (820 imgs) → aluminio
  - glass, trash → ignorados
- **Justificacion:** Dataset publico gratuito con categorias compatibles. Permite entrenar un modelo funcional sin recoleccion manual inmediata.
- **Nota:** Este dataset es un punto de partida. Para el prototipo final se recomienda complementar con fotos propias tomadas con el hardware real.
- **Responsable:** Software Lead

### D-012 — Entorno virtual Python como estandar
- **Descripcion:** Se establece el uso de un entorno virtual (`venv/`) como forma estandar de ejecutar el proyecto.
- **Activacion:** `source venv/bin/activate`
- **Justificacion:** macOS no permite instalar paquetes globalmente (PEP 668).
- **Responsable:** Software Lead / equipo real

### D-013 — Prioridad: IA primero, mecanismo despues
- **Descripcion:** El orden de trabajo del proyecto es: (1) modelo de IA funcional y validado, (2) diseno mecanico, (3) integracion hardware. No se escribe codigo de mecanismo hasta tener diseno aprobado.
- **Justificacion:** Solicitud del equipo real. Permite demostrar avances en clasificacion antes de tener hardware fisico.
- **Responsable:** Chair / equipo real

## Artefactos producidos

- [x] Script `src/training/download_dataset.py` — descarga automatica de dataset
- [x] Dataset descargado en `dataset/` (3,778 imagenes, 4 categorias)
- [x] Modelo entrenado `models/ecosort_model.keras` (~95.8% val accuracy)
- [x] Modelos TFLite: `models/ecosort_model.tflite` y `models/ecosort_model_int8.tflite`
- [x] Grafica de entrenamiento `models/training_history.png`
- [x] Script `test_with_webcam.py` actualizado con clasificacion real
- [x] Entorno virtual configurado en `venv/`
- [x] Bugs corregidos en todos los scripts

## Resultados del entrenamiento

| Metrica | Valor |
|---------|-------|
| Accuracy de validacion | ~95.8% |
| Epochs completados | 20 (best en epoch 18) |
| Tiempo de entrenamiento | ~20 minutos (MacBook, CPU) |
| Tamano modelo Keras | ~11 MB |
| Tamano modelo TFLite INT8 | ~3-4 MB (estimado) |
| Categorias | 4 (plastico, papel, carton, aluminio) |
| Imagenes de entrenamiento | 3,024 (80%) |
| Imagenes de validacion | 754 (20%) |

## Proximos pasos

1. **Equipo real:** Probar `test_with_webcam.py` con objetos reales para validar la clasificacion
2. **Software Lead:** Complementar dataset con fotos propias si la precision no es suficiente con objetos reales
3. **S004:** Definir diseno mecanico — tipo de motor, mecanismo de desvio, prototipo fisico
4. **S004:** Evaluar precision del modelo con objetos reales (no solo dataset)
5. **Compras:** Continua pendiente la compra de RPi 5 y componentes

## Como probar el sistema

```bash
# Activar entorno virtual
cd "practice folder/trash-bot"
source venv/bin/activate

# Opcion 1: Simulacion pura (sin camara, sin modelo)
python src/test_simulation.py

# Opcion 2: Webcam con clasificacion real
python src/test_with_webcam.py

# Opcion 3: Inferencia por consola (con camara o sin ella)
python src/inference/classify.py
```

---

*Sesion cerrada por el Chair — 2026-02-13*
