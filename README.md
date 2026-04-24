# EcoSort IA

Sistema escolar de clasificacion automatica de residuos reciclables con vision por computadora (MobileNetV2 + TFLite), pensado para pruebas en laptop y despliegue en Raspberry Pi 5.

## Equipo
- Saulo Alaniz
- Mauricio Fernandes
- Luis Chaires
- Emilio Faz
- David Martinez

## Demo
- Pendiente: agregar link de video o deploy.
- Recomendado: incluir 2-3 screenshots del flujo de clasificacion y dashboard.

## Features
- Clasificacion de `plastico`, `papel`, `carton` y `aluminio`.
- Entrenamiento con transfer learning usando MobileNetV2.
- Exportacion a `.tflite` e INT8 para Raspberry Pi.
- Inferencia en tiempo real con webcam.
- Modo simulacion para pruebas sin hardware fisico.

## Tech Stack
- Python 3.10+
- TensorFlow / Keras
- TFLite Runtime
- OpenCV
- Flask (dashboard)

## Estructura del proyecto
```text
ecoSortAI/
├─ README.md
├─ src/
│  ├─ config.py
│  ├─ inference/
│  ├─ training/
│  └─ ...
├─ scripts/
│  └─ export_tflite_compatible.py
├─ tests/
├─ docs/
├─ .env.example
├─ .gitignore
└─ requirements.txt
```

## Instalacion local (Python + venv)
```bash
git clone <TU-REPO-URL>
cd ecoSortAI
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Uso rapido

1) Descargar dataset base (TrashNet):
```bash
python src/training/download_dataset.py
```

2) Entrenar modelo y exportar artefactos:
```bash
python src/training/train_model.py
```

3) Re-exportar TFLite compatible para Raspberry Pi (opcional):
```bash
python scripts/export_tflite_compatible.py
```

4) Ejecutar inferencia:
```bash
python src/inference/classify.py --keyboard
```

## Tests basicos
```bash
python -m unittest discover -s tests -p "test_*.py"
```

## Decisiones tecnicas
- **MobileNetV2** por buen balance entre precision y costo computacional.
- **TFLite** para facilitar despliegue en hardware embebido (Raspberry Pi).
- **Configuracion centralizada** en `src/config.py` para mantener consistencia.
- **Separacion por modulos** (`training`, `inference`, `scripts`) para mantenibilidad.

## Problemas resueltos y tradeoffs
- Se priorizo compatibilidad en Raspberry Pi sobre modelos mas pesados.
- Se usa umbral de confianza para evitar acciones fisicas con baja certeza.
- El dataset inicial se automatiza, pero puede requerir limpieza y augmentations adicionales.

## Roadmap
- Agregar screenshots/GIFs y video demo.
- Integrar CI completo (lint + tests + checks de formato).
- Publicar dashboard con un deploy ligero.
- Agregar seed data y script de setup de extremo a extremo.

## Seguridad y buenas practicas
- No subir secretos ni `.env` reales.
- Usar `.env.example` como plantilla.
- Mantener commits pequenos y descriptivos.

