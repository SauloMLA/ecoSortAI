"""
EcoSort IA — Script de entrenamiento
=====================================
Ejecutar en laptop/PC o Google Colab (NO en la Raspberry Pi).

Uso:
    python src/training/train_model.py

Prerequisitos:
    1. Tener las fotos organizadas en:
       dataset/
       ├── plastico/   (200+ fotos)
       ├── papel/      (200+ fotos)
       ├── carton/     (200+ fotos)
       └── aluminio/   (200+ fotos)

    2. pip install tensorflow numpy matplotlib scikit-learn Pillow
"""

import os
import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Backend sin GUI — evita crashes en macOS
import matplotlib.pyplot as plt

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Agregar ruta del proyecto
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from config import (
    CLASES, NUM_CLASES, IMG_SIZE, BATCH_SIZE, EPOCHS,
    LEARNING_RATE, VALIDATION_SPLIT, DATASET_DIR,
    MODEL_SAVE_PATH, TFLITE_MODEL_PATH, TFLITE_INT8_PATH
)


def crear_generadores_datos(dataset_dir):
    """
    Crea generadores de datos con data augmentation para entrenamiento
    y un generador limpio para validacion.
    """
    # Data augmentation para entrenamiento
    # Esto multiplica artificialmente tu dataset con variaciones
    train_datagen = ImageDataGenerator(
        rescale=1.0 / 255.0,              # Normalizar pixeles a 0-1
        rotation_range=20,                  # Rotar hasta 20 grados
        width_shift_range=0.2,              # Mover horizontalmente
        height_shift_range=0.2,             # Mover verticalmente
        shear_range=0.15,                   # Deformacion
        zoom_range=0.2,                     # Zoom in/out
        horizontal_flip=True,               # Espejo horizontal
        brightness_range=[0.8, 1.2],        # Variar brillo
        fill_mode='nearest',
        validation_split=VALIDATION_SPLIT   # Separar validacion
    )

    # Para validacion: solo normalizar, sin augmentation
    val_datagen = ImageDataGenerator(
        rescale=1.0 / 255.0,
        validation_split=VALIDATION_SPLIT
    )

    print(f"\nCargando dataset desde: {dataset_dir}")
    print(f"Clases esperadas: {CLASES}")
    print(f"Tamaño de imagen: {IMG_SIZE}")
    print(f"Batch size: {BATCH_SIZE}")

    # Generador de entrenamiento
    train_generator = train_datagen.flow_from_directory(
        dataset_dir,
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        subset='training',
        classes=CLASES,
        shuffle=True
    )

    # Generador de validacion
    val_generator = val_datagen.flow_from_directory(
        dataset_dir,
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        subset='validation',
        classes=CLASES,
        shuffle=False
    )

    return train_generator, val_generator


def construir_modelo():
    """
    Construye el modelo usando Transfer Learning con MobileNetV2.
    Usa Functional API (mas estable para serializar/cargar que Sequential).

    Arquitectura:
    - MobileNetV2 pre-entrenado (capas congeladas — ya sabe "ver")
    - + GlobalAveragePooling (comprimir features)
    - + Dropout (evitar overfitting)
    - + Dense 128 (capa intermedia)
    - + Dense 4 con softmax (una neurona por clase)
    """
    # Cargar MobileNetV2 sin la cabeza de clasificacion original
    base_model = MobileNetV2(
        input_shape=(*IMG_SIZE, 3),
        include_top=False,           # Sin la ultima capa (la reemplazamos)
        weights='imagenet'           # Pesos pre-entrenados con 14M imagenes
    )

    # CONGELAR las capas pre-entrenadas
    # Estas capas ya saben detectar bordes, texturas, formas
    # No las modificamos — solo entrenamos nuestra capa nueva
    base_model.trainable = False

    # Construir modelo con Functional API
    inputs = layers.Input(shape=(*IMG_SIZE, 3))
    x = base_model(inputs, training=False)
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.Dropout(0.3)(x)
    x = layers.Dense(128, activation='relu')(x)
    x = layers.Dropout(0.2)(x)
    outputs = layers.Dense(NUM_CLASES, activation='softmax')(x)

    model = keras.Model(inputs=inputs, outputs=outputs)

    # Compilar modelo
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=LEARNING_RATE),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )

    print("\n--- ARQUITECTURA DEL MODELO ---")
    model.summary()

    total_params = model.count_params()
    trainable = sum([tf.reduce_prod(v.shape) for v in model.trainable_variables])
    print(f"\nParametros totales: {total_params:,}")
    print(f"Parametros entrenables: {int(trainable):,}")
    print(f"Parametros congelados: {total_params - int(trainable):,}")

    return model


def entrenar(model, train_gen, val_gen):
    """
    Entrena el modelo con early stopping y guarda el mejor resultado.
    """
    # Early stopping: si la validacion no mejora en 5 epocas, para
    early_stop = keras.callbacks.EarlyStopping(
        monitor='val_loss',
        patience=5,
        restore_best_weights=True
    )

    # Guardar el mejor modelo automaticamente
    os.makedirs(os.path.dirname(MODEL_SAVE_PATH), exist_ok=True)
    checkpoint = keras.callbacks.ModelCheckpoint(
        MODEL_SAVE_PATH,
        monitor='val_accuracy',
        save_best_only=True,
        verbose=1
    )

    print(f"\n{'='*60}")
    print(f"INICIANDO ENTRENAMIENTO")
    print(f"Epocas maximas: {EPOCHS}")
    print(f"Early stopping: patience=5")
    print(f"{'='*60}\n")

    history = model.fit(
        train_gen,
        epochs=EPOCHS,
        validation_data=val_gen,
        callbacks=[early_stop, checkpoint],
        verbose=1
    )

    return history


def graficar_resultados(history):
    """Grafica accuracy y loss del entrenamiento."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    # Accuracy
    ax1.plot(history.history['accuracy'], label='Train', linewidth=2)
    ax1.plot(history.history['val_accuracy'], label='Validation', linewidth=2)
    ax1.set_title('Accuracy por Epoca', fontsize=14)
    ax1.set_xlabel('Epoca')
    ax1.set_ylabel('Accuracy')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # Loss
    ax2.plot(history.history['loss'], label='Train', linewidth=2)
    ax2.plot(history.history['val_loss'], label='Validation', linewidth=2)
    ax2.set_title('Loss por Epoca', fontsize=14)
    ax2.set_xlabel('Epoca')
    ax2.set_ylabel('Loss')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('models/training_history.png', dpi=150)
    print("\nGrafica guardada en: models/training_history.png")
    plt.close()  # Cerrar figura (no abrir ventana GUI)


def convertir_a_tflite(model):
    """
    Convierte el modelo a TFLite y a TFLite INT8 (cuantizado).
    Estos son los archivos que se copian a la Raspberry Pi.
    Primero exporta como SavedModel, luego convierte desde ahi.
    """
    print(f"\n{'='*60}")
    print("CONVIRTIENDO A TFLITE")
    print(f"{'='*60}")

    os.makedirs(os.path.dirname(TFLITE_MODEL_PATH), exist_ok=True)

    # Paso 1: Exportar como SavedModel (formato mas estable para conversion)
    saved_model_dir = "models/ecosort_saved_model"
    print(f"Exportando SavedModel a: {saved_model_dir}")
    try:
        model.export(saved_model_dir)
    except Exception:
        # Fallback: usar tf.saved_model.save
        tf.saved_model.save(model, saved_model_dir)
    print("  SavedModel OK")

    # Paso 2: Convertir a TFLite FP32
    try:
        print("Convirtiendo a TFLite (FP32)...")
        converter = tf.lite.TFLiteConverter.from_saved_model(saved_model_dir)
        tflite_model = converter.convert()
        with open(TFLITE_MODEL_PATH, 'wb') as f:
            f.write(tflite_model)
        size_mb = len(tflite_model) / (1024 * 1024)
        print(f"  Modelo TFLite (FP32): {TFLITE_MODEL_PATH} ({size_mb:.1f} MB)")
    except Exception as e:
        print(f"  ERROR en conversion FP32: {e}")
        print("  (La conversion TFLite puede hacerse en otra maquina o Colab)")
        size_mb = 0

    # Paso 3: Convertir a TFLite INT8
    try:
        print("Convirtiendo a TFLite (INT8)...")
        converter_int8 = tf.lite.TFLiteConverter.from_saved_model(saved_model_dir)
        converter_int8.optimizations = [tf.lite.Optimize.DEFAULT]
        tflite_int8 = converter_int8.convert()
        with open(TFLITE_INT8_PATH, 'wb') as f:
            f.write(tflite_int8)
        size_int8_mb = len(tflite_int8) / (1024 * 1024)
        print(f"  Modelo TFLite (INT8): {TFLITE_INT8_PATH} ({size_int8_mb:.1f} MB)")
        if size_mb > 0:
            print(f"  Reduccion: {size_mb:.1f} MB -> {size_int8_mb:.1f} MB "
                  f"({(1 - size_int8_mb/size_mb)*100:.0f}% mas chico)")
    except Exception as e:
        print(f"  ERROR en conversion INT8: {e}")
        print("  (La conversion TFLite puede hacerse en otra maquina o Colab)")


def main():
    print("=" * 60)
    print("  EcoSort IA — Entrenamiento del Modelo")
    print("  Categorias:", CLASES)
    print("=" * 60)

    # Verificar que el dataset existe
    if not os.path.exists(DATASET_DIR):
        print(f"\nERROR: No se encuentra la carpeta '{DATASET_DIR}'")
        print(f"\nCrea la siguiente estructura:")
        print(f"  {DATASET_DIR}/")
        for clase in CLASES:
            print(f"  ├── {clase}/   (minimo 200 fotos)")
        print(f"\nLuego ejecuta este script de nuevo.")
        sys.exit(1)

    # Verificar subcarpetas
    for clase in CLASES:
        clase_dir = os.path.join(DATASET_DIR, clase)
        if not os.path.exists(clase_dir):
            print(f"ERROR: Falta la carpeta '{clase_dir}'")
            sys.exit(1)
        num_imgs = len([f for f in os.listdir(clase_dir)
                       if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
        print(f"  {clase}: {num_imgs} imagenes")
        if num_imgs < 50:
            print(f"  ADVERTENCIA: {clase} tiene pocas imagenes. "
                  f"Recomendado: 200+")

    # Crear generadores
    train_gen, val_gen = crear_generadores_datos(DATASET_DIR)

    # Construir modelo
    model = construir_modelo()

    # Entrenar
    history = entrenar(model, train_gen, val_gen)

    # Graficar
    graficar_resultados(history)

    # Convertir a TFLite
    convertir_a_tflite(model)

    print(f"\n{'='*60}")
    print("ENTRENAMIENTO COMPLETADO")
    print(f"{'='*60}")
    print(f"\nArchivos generados:")
    print(f"  Modelo Keras:     {MODEL_SAVE_PATH}")
    print(f"  Modelo TFLite:    {TFLITE_MODEL_PATH}")
    print(f"  Modelo INT8:      {TFLITE_INT8_PATH}")
    print(f"  Grafica:          models/training_history.png")
    print(f"\nSiguiente paso:")
    print(f"  Copia '{TFLITE_INT8_PATH}' a la Raspberry Pi")
    print(f"  y ejecuta: python src/inference/classify.py")


if __name__ == "__main__":
    main()
