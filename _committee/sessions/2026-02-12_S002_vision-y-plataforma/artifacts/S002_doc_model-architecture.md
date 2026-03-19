# Arquitectura del Modelo de IA — EcoSort IA

**Sesion:** S002  
**Autores:** ML Researcher, Edge Inference Specialist, Model Optimization Engineer  
**Fecha:** 2026-02-12

---

## Decision: Inferencia en el dispositivo (Edge), no en la nube

### Por que NO en la nube

| Factor | Nube | Edge (RPi 5) |
|--------|------|---------------|
| Latencia | 200-2000ms (depende de internet) | 50-150ms (local) |
| Dependencia de internet | SI — falla sin WiFi | NO — funciona offline |
| Costo operativo | Pago por uso (API) | $0 despues de comprar |
| Privacidad | Datos salen del dispositivo | Todo queda local |
| Complejidad | Necesitas backend cloud | Todo en una placa |
| Demo ante jurado | Riesgo de falla por WiFi | Funciona sin red |

**Veredicto: Edge. El modelo se descarga y vive en la RPi 5.**

---

## Modelo seleccionado: MobileNetV2 + Transfer Learning

### Que es MobileNetV2

MobileNetV2 es una red neuronal convolucional (CNN) disenada por Google especificamente para dispositivos moviles y embebidos. Es liviana, rapida, y suficientemente precisa.

### Por que MobileNetV2 y no otro

| Modelo | Precision (ImageNet) | Tamano | Latencia RPi 5 (TFLite INT8) | Veredicto |
|--------|---------------------|--------|-------------------------------|-----------|
| MobileNetV2 | 72% top-1 | ~3.4 MB (INT8) | ~50-100ms | ELEGIDO |
| EfficientNet-Lite0 | 75% top-1 | ~4.4 MB | ~80-150ms | Alternativa |
| YOLOv8-nano | 37% mAP (deteccion) | ~6 MB | ~200-400ms | Overkill para clasificacion |
| ResNet50 | 76% top-1 | ~25 MB (FP32) | ~500-800ms | Demasiado pesado |

MobileNetV2 da el mejor balance entre velocidad y precision para nuestra placa.

---

## Como funciona paso a paso

### Fase 1: Transfer Learning (entrenamiento en tu computadora)

```
                    TU COMPUTADORA (laptop/PC)
┌──────────────────────────────────────────────────────┐
│                                                       │
│  MobileNetV2 pre-entrenado (ImageNet = 1000 clases)  │
│  ┌─────────────────────────────────────────────┐     │
│  │  Capas convolucionales (CONGELADAS)          │     │
│  │  Ya saben detectar bordes, texturas, formas  │     │
│  │  NO se modifican                             │     │
│  └──────────────────────┬──────────────────────┘     │
│                         │                             │
│                         ▼                             │
│  ┌─────────────────────────────────────────────┐     │
│  │  Capa de clasificacion (NUEVA — 5 clases)   │     │
│  │  Plastico | Metal | Papel | Organico | Otro  │     │
│  │  ESTA se entrena con TUS fotos               │     │
│  └─────────────────────────────────────────────┘     │
│                                                       │
│  Dataset: ~200-500 fotos por clase = 1000-2500 total  │
│  Framework: TensorFlow / Keras                        │
│  Epocas: ~10-30                                       │
│  Tiempo: ~30-60 min en laptop con GPU                 │
│                                                       │
│  Resultado: modelo.tflite (archivo de ~3-4 MB)        │
└──────────────────────────────────────────────────────┘
```

**Que significa Transfer Learning?**  
En vez de entrenar una red desde cero (necesitarias millones de fotos), tomas un modelo que ya aprendio a "ver" (MobileNetV2 entreno con 14 millones de imagenes) y solo le ensenas la ultima capa: "estas 5 categorias son las que me importan".

### Fase 2: Optimizacion (convertir para RPi)

```
modelo_keras.h5  ──▶  TFLite Converter  ──▶  modelo.tflite
   (~14 MB)              + Quantizacion          (~3-4 MB)
   (FP32)                INT8                    (INT8)
                                                 4x mas chico
                                                 2-3x mas rapido
```

**Quantizacion INT8:** Los numeros dentro del modelo pasan de 32 bits a 8 bits. Se pierde ~1-2% de precision pero se gana mucha velocidad.

### Fase 3: Inferencia en la RPi 5 (lo que corre en vivo)

```
              RASPBERRY PI 5 (en vivo)
┌──────────────────────────────────────────────┐
│                                               │
│  1. Camara captura frame (imagen 224x224 px)  │
│           │                                   │
│           ▼                                   │
│  2. Preprocesamiento                          │
│     - Resize a 224x224                        │
│     - Normalizar pixeles (0-1)                │
│           │                                   │
│           ▼                                   │
│  3. TFLite Interpreter carga modelo.tflite    │
│     - Pasa la imagen por la red               │
│     - Tarda ~50-100ms                         │
│           │                                   │
│           ▼                                   │
│  4. Output: [0.02, 0.91, 0.03, 0.01, 0.03]   │
│              PET  Metal Papel Org   Otro      │
│              ─────▲─────                      │
│              "Es METAL con 91% confianza"     │
│           │                                   │
│           ▼                                   │
│  5. Decision → GPIO pin → Servo → Desvio     │
│     + Log → Dashboard                         │
│                                               │
└──────────────────────────────────────────────┘
```

---

## El codigo simplificado (Python)

```python
import tflite_runtime.interpreter as tflite
import cv2
import numpy as np

# Cargar modelo (una sola vez al iniciar)
interpreter = tflite.Interpreter(model_path="modelo_ecosort.tflite")
interpreter.allocate_tensors()

# Clases
CLASES = ["plastico", "metal", "papel", "organico", "no_reciclable"]

# Loop principal
while True:
    # 1. Capturar imagen
    frame = camara.capture()
    
    # 2. Preprocesar
    img = cv2.resize(frame, (224, 224))
    img = img.astype(np.float32) / 255.0
    img = np.expand_dims(img, axis=0)
    
    # 3. Inferencia
    interpreter.set_tensor(input_index, img)
    interpreter.invoke()
    output = interpreter.get_tensor(output_index)
    
    # 4. Resultado
    clase_idx = np.argmax(output)
    confianza = output[0][clase_idx]
    clase = CLASES[clase_idx]
    
    # 5. Actuar
    if confianza > 0.7:  # umbral de confianza
        activar_servo(clase_idx)
        log_clasificacion(clase, confianza)
    else:
        log_clasificacion("incierto", confianza)
```

---

## Pipeline completo de desarrollo

```
SEMANA 1-2: Dataset
├── Tomar 200-500 fotos por clase (celular o camara RPi)
├── Organizar en carpetas: plastico/ metal/ papel/ organico/ otro/
├── Aumentar con data augmentation (rotacion, brillo, flip)
└── Split: 80% train / 10% validation / 10% test

SEMANA 2-3: Entrenamiento
├── Transfer Learning con MobileNetV2 en laptop/Colab
├── Fine-tuning de ultima capa
├── Evaluar: precision, recall, F1, confusion matrix
└── Iterar si hay clases problematicas

SEMANA 3: Optimizacion
├── Convertir a TFLite
├── Quantizar a INT8
├── Benchmark en RPi 5 (latencia, precision post-quantizacion)
└── Ajustar umbral de confianza

SEMANA 3-4: Integracion
├── Pipeline de camara en RPi
├── Conectar inferencia → GPIO → servos
├── Dashboard basico
└── Testing end-to-end
```
