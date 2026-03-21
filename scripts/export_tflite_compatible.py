#!/usr/bin/env python3
"""
Re-exporta el SavedModel a TFLite con ops compatibles con tflite_runtime en Raspberry Pi.
Usa esto si el modelo actual da SystemError al cargar en la Pi.
"""
import os
import sys

# Ruta del proyecto
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from src.config import TFLITE_MODEL_PATH, TFLITE_INT8_PATH
import tensorflow as tf

SAVED_MODEL_DIR = "models/ecosort_saved_model"


def main():
    if not os.path.exists(SAVED_MODEL_DIR):
        print(f"ERROR: No existe {SAVED_MODEL_DIR}")
        print("Primero entrena: python src/training/train_model.py")
        sys.exit(1)

    os.makedirs(os.path.dirname(TFLITE_MODEL_PATH), exist_ok=True)

    # FP32 con solo ops TFLite nativas (compatible con RPi)
    print("Convirtiendo a TFLite FP32 (compatible con RPi)...")
    converter = tf.lite.TFLiteConverter.from_saved_model(SAVED_MODEL_DIR)
    converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS]

    tflite_model = converter.convert()
    with open(TFLITE_MODEL_PATH, "wb") as f:
        f.write(tflite_model)
    print(f"  Guardado: {TFLITE_MODEL_PATH} ({len(tflite_model)/1024/1024:.1f} MB)")

    # INT8 opcional
    try:
        print("Convirtiendo a TFLite INT8...")
        converter_int8 = tf.lite.TFLiteConverter.from_saved_model(SAVED_MODEL_DIR)
        converter_int8.target_spec.supported_ops = [
            tf.lite.OpsSet.TFLITE_BUILTINS,
            tf.lite.OpsSet.TFLITE_BUILTINS_INT8,
        ]
        converter_int8.optimizations = [tf.lite.Optimize.DEFAULT]
        tflite_int8 = converter_int8.convert()
        with open(TFLITE_INT8_PATH, "wb") as f:
            f.write(tflite_int8)
        print(f"  Guardado: {TFLITE_INT8_PATH} ({len(tflite_int8)/1024/1024:.1f} MB)")
    except Exception as e:
        print(f"  INT8 fallo (usa FP32): {e}")

    print("\nCopia el .tflite a la Pi:")
    print(f"  scp {TFLITE_MODEL_PATH} admin@IP:~/ecoSortAI/models/")


if __name__ == "__main__":
    main()
