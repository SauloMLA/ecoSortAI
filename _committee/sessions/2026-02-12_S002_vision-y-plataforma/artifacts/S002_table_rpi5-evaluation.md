# Evaluacion de Plataforma — Raspberry Pi 5

**Sesion:** S002  
**Autores:** Embedded Engineer, Edge Inference Specialist, Reliability Skeptic

---

## Especificaciones relevantes

| Especificacion | RPi 5 (4GB) | RPi 5 (8GB) |
|---------------|-------------|-------------|
| CPU | Cortex-A76 4-core 2.4GHz | Mismo |
| RAM | 4GB LPDDR4X | 8GB LPDDR4X |
| GPU | VideoCore VII | Mismo |
| Camara | MIPI CSI-2 | Mismo |
| GPIO | 40 pines | Mismo |
| USB | 2x 3.0 + 2x 2.0 | Mismo |
| Precio aprox. | ~$60 USD | ~$80 USD |

## Latencia de inferencia estimada

| Modelo | Framework | Latencia en RPi 5 | Aceptable? |
|--------|-----------|-------------------|------------|
| MobileNetV2 | TFLite INT8 | ~50-100ms | SI |
| EfficientNet-Lite0 | TFLite INT8 | ~80-150ms | SI |
| YOLOv8n | ONNX/NCNN | ~200-400ms | LIMITE |
| ResNet50 | TFLite FP32 | ~500-800ms | NO |

## Alternativas evaluadas

| Plataforma | Ventaja | Desventaja | Precio |
|-----------|---------|------------|--------|
| RPi 5 sola | Simple, barata, suficiente | Sin acelerador IA | ~$60 |
| RPi 5 + AI HAT | NPU dedicado, 13 TOPS | Costo extra | ~$85 |
| Jetson Nano Orin | GPU CUDA, muy potente | Complejo, caro | ~$200 |

## Riesgos identificados

| Riesgo | Mitigacion |
|--------|------------|
| Reinicio por mala alimentacion | Fuente oficial 5V/5A |
| Sobrecalentamiento en operacion continua | Cooler activo oficial |
| Fallo de MicroSD | SD de calidad + backup |

## Decision

**RPi 5 de 4GB recomendada para el MVP** con ruta de escape a AI HAT si se requiere.

## BOM preliminar

| Componente | Estimado USD | Prioridad |
|-----------|-------------|-----------|
| Raspberry Pi 5 (4GB) | ~$60 | CRITICA |
| Fuente oficial USB-C 5V/5A | ~$12 | CRITICA |
| Cooler activo oficial | ~$5 | ALTA |
| MicroSD 32GB (Samsung EVO) | ~$10 | CRITICA |
| Camara RPi Module 3 o USB cam | ~$15-35 | CRITICA |
| 2-3 Servomotores SG90/MG996R | ~$5-15 | ALTA |
| LEDs + resistencias | ~$3 | BAJA |
| **Total** | **~$110-140** | — |
