# Arquitectura EcoSort IA

Diagrama de flujo de alto nivel del sistema:

```mermaid
flowchart TD
    dataset[DatasetTrashNet] --> downloadDataset[src/training/download_dataset.py]
    downloadDataset --> localDataset[dataset/]
    localDataset --> trainModel[src/training/train_model.py]
    trainModel --> kerasModel[models/ecosort_model.keras]
    trainModel --> tfliteModel[models/ecosort_model.tflite]
    trainModel --> int8Model[models/ecosort_model_int8.tflite]
    tfliteModel --> classify[src/inference/classify.py]
    int8Model --> classify
    webcam[WebcamorRPiCamera] --> classify
    classify --> result[PrediccionClaseConfianza]
    result --> action[LEDoSimulacionMecanismo]
    result --> log[logs/clasificaciones.json]
```

## Componentes
- `src/training/`: descarga de dataset y entrenamiento del modelo.
- `scripts/`: utilidades para exportacion y compatibilidad TFLite.
- `src/inference/`: clasificacion en tiempo real.
- `src/config.py`: constantes globales del proyecto.

