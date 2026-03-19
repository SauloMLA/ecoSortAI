"""
EcoSort IA — Test con webcam de laptop
=======================================
Usa la webcam de tu laptop para clasificar objetos reciclables EN TIEMPO REAL.

Si el modelo entrenado existe (models/ecosort_model.tflite), usa clasificacion REAL.
Si no existe,C usa clasificacion simulada (aleatoria) como fallback.

Uso:
    source venv/bin/activate
    pip install opencv-python numpy tensorflow
    python src/test_with_webcam.py

Controles:
    ESPACIO  → Clasificar el objeto actual
    M        → Cambiar modo (real / simulado)
    Q        → Salir
"""

import sys
import os
import time
import random
import numpy as np
import cv2

sys.path.append(os.path.join(os.path.dirname(__file__)))
from config import (
    CLASES, IMG_SIZE, CONFIDENCE_THRESHOLD,
    TFLITE_MODEL_PATH, TFLITE_INT8_PATH,
    MODEL_SAVE_PATH
)


# --- Clasificador con modelo real ---

class ClasificadorTFLite:
    """Clasificador que usa un modelo TFLite."""

    def __init__(self, model_path):
        try:
            import tflite_runtime.interpreter as tflite_mod
        except ImportError:
            try:
                import tensorflow.lite as tflite_mod
            except (ImportError, AttributeError):
                import tensorflow as tf
                tflite_mod = tf.lite

        self.interpreter = tflite_mod.Interpreter(model_path=model_path)
        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()

        size_kb = os.path.getsize(model_path) / 1024
        print(f"  Modelo TFLite cargado: {model_path} ({size_kb:.0f} KB)")

    def clasificar(self, frame):
        """Clasifica un frame BGR de OpenCV."""
        img = cv2.resize(frame, IMG_SIZE)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = img.astype(np.float32) / 255.0
        img = np.expand_dims(img, axis=0)

        t_start = time.time()
        self.interpreter.set_tensor(self.input_details[0]['index'], img)
        self.interpreter.invoke()
        output = self.interpreter.get_tensor(self.output_details[0]['index'])
        latencia_ms = (time.time() - t_start) * 1000

        probs = output[0]
        clase_idx = np.argmax(probs)
        return CLASES[clase_idx], float(probs[clase_idx]), probs, latencia_ms


class ClasificadorKeras:
    """Clasificador que usa el modelo Keras directamente (para laptop)."""

    def __init__(self, model_path):
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
        import tensorflow as tf
        self.model = tf.keras.models.load_model(model_path)
        size_mb = os.path.getsize(model_path) / (1024 * 1024)
        print(f"  Modelo Keras cargado: {model_path} ({size_mb:.1f} MB)")

    def clasificar(self, frame):
        """Clasifica un frame BGR de OpenCV."""
        img = cv2.resize(frame, IMG_SIZE)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = img.astype(np.float32) / 255.0
        img = np.expand_dims(img, axis=0)

        t_start = time.time()
        output = self.model.predict(img, verbose=0)
        latencia_ms = (time.time() - t_start) * 1000

        probs = output[0]
        clase_idx = np.argmax(probs)
        return CLASES[clase_idx], float(probs[clase_idx]), probs, latencia_ms


# --- Clasificador simulado (fallback) ---

class ClasificadorSimulado:
    """Clasificador falso — genera resultados aleatorios."""

    def clasificar(self, frame):
        probs = np.random.dirichlet(np.ones(len(CLASES)) * 1.5)
        dominante = random.randint(0, len(CLASES) - 1)
        probs[dominante] += 0.6
        probs = probs / probs.sum()
        clase_idx = np.argmax(probs)
        latencia_ms = random.uniform(50, 150)
        return CLASES[clase_idx], float(probs[clase_idx]), probs, latencia_ms


def main():
    # Detectar modelo disponible (prioridad: TFLite INT8 > TFLite > Keras)
    modelo_disponible = False
    model_path = None
    model_type = None  # 'tflite' or 'keras'
    for path, mtype in [(TFLITE_INT8_PATH, 'tflite'),
                         (TFLITE_MODEL_PATH, 'tflite'),
                         (MODEL_SAVE_PATH, 'keras')]:
        if os.path.exists(path):
            model_path = path
            model_type = mtype
            modelo_disponible = True
            break

    print("=" * 55)
    print("  EcoSort IA — TEST CON WEBCAM")
    if modelo_disponible:
        print(f"  Modo: CLASIFICACION REAL ({model_type.upper()})")
    else:
        print("  Modo: CLASIFICACION SIMULADA (sin modelo)")
        print(f"  (entrena con: python src/training/train_model.py)")
    print("=" * 55)

    # Crear clasificador
    if modelo_disponible and model_type == 'tflite':
        clasificador = ClasificadorTFLite(model_path)
        modo_real = True
    elif modelo_disponible and model_type == 'keras':
        clasificador = ClasificadorKeras(model_path)
        modo_real = True
    else:
        clasificador = ClasificadorSimulado()
        modo_real = False

    # Abrir webcam
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("ERROR: No se pudo abrir la webcam")
        sys.exit(1)

    print(f"\n  Webcam activa.")
    print(f"  ESPACIO = clasificar | M = cambiar modo | Q = salir\n")

    ultimo_resultado = None
    colores = {
        "plastico": (255, 165, 0),    # Naranja
        "papel":    (255, 255, 100),   # Amarillo
        "carton":   (139, 90, 43),     # Cafe
        "aluminio": (200, 200, 200),   # Gris
    }

    clasificaciones = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        display = frame.copy()
        h, w = display.shape[:2]

        # Dibujar area de inspeccion (cuadrado central)
        cx, cy = w // 2, h // 2
        box_size = min(w, h) // 2
        x1, y1 = cx - box_size // 2, cy - box_size // 2
        x2, y2 = cx + box_size // 2, cy + box_size // 2
        cv2.rectangle(display, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(display, "Coloca objeto aqui", (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        # Mostrar preview preprocesada (224x224) en esquina
        roi = frame[y1:y2, x1:x2]
        if roi.size > 0:
            preview = cv2.resize(roi, IMG_SIZE)
            ph, pw = 112, 112
            preview_small = cv2.resize(preview, (pw, ph))
            display[10:10+ph, w-pw-10:w-10] = preview_small
            cv2.putText(display, f"{IMG_SIZE[0]}x{IMG_SIZE[1]}", (w-pw-10, 10+ph+15),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)

        # Indicador de modo
        modo_texto = "REAL" if modo_real else "SIMULADO"
        modo_color = (0, 255, 0) if modo_real else (0, 165, 255)
        cv2.putText(display, f"Modo: {modo_texto}", (w-180, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, modo_color, 2)

        # Mostrar ultimo resultado
        if ultimo_resultado:
            clase, conf, probs, lat = ultimo_resultado
            color = colores.get(clase, (255, 255, 255))

            # Panel de resultado
            cv2.rectangle(display, (10, h-180), (300, h-10), (0, 0, 0), -1)
            cv2.rectangle(display, (10, h-180), (300, h-10), color, 2)

            cv2.putText(display, f"RESULTADO #{clasificaciones}:", (20, h-155),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            cv2.putText(display, f"{clase.upper()}", (20, h-120),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.0, color, 2)
            cv2.putText(display, f"Confianza: {conf*100:.1f}%", (20, h-90),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            cv2.putText(display, f"Latencia: {lat:.0f} ms", (20, h-70),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

            # Barras de probabilidad
            bar_y = h - 55
            for i, c in enumerate(CLASES):
                bar_w = int(probs[i] * 120)
                c_color = colores.get(c, (200, 200, 200))
                cv2.rectangle(display, (20, bar_y), (20 + bar_w, bar_y + 8), c_color, -1)
                cv2.putText(display, f"{c[:4]} {probs[i]*100:.0f}%",
                            (145, bar_y + 8), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 255, 255), 1)
                bar_y += 12

            # Accion
            accion = "DESVIAR" if conf >= CONFIDENCE_THRESHOLD else "RECHAZAR"
            accion_color = (0, 255, 0) if conf >= CONFIDENCE_THRESHOLD else (0, 0, 255)
            cv2.putText(display, f">> {accion}", (170, h-120),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, accion_color, 2)

        # Instrucciones
        cv2.putText(display, "ESPACIO=clasificar  M=modo  Q=salir", (10, 25),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        cv2.imshow("EcoSort IA - Clasificador de Reciclaje", display)

        key = cv2.waitKey(1) & 0xFF

        if key == ord(' '):
            # Clasificar
            if roi.size > 0:
                clase, conf, probs, lat = clasificador.clasificar(roi)
                ultimo_resultado = (clase, conf, probs, lat)
                clasificaciones += 1

                print(f"\n  #{clasificaciones} | {clase.upper()} | {conf*100:.1f}% | {lat:.0f}ms")
                for i, c in enumerate(CLASES):
                    bar = "█" * int(probs[i] * 20)
                    print(f"    {c:12s} {probs[i]*100:5.1f}% {bar}")

        elif key == ord('m') or key == ord('M'):
            # Cambiar modo
            if modelo_disponible:
                modo_real = not modo_real
                if modo_real:
                    if model_type == 'tflite':
                        clasificador = ClasificadorTFLite(model_path)
                    else:
                        clasificador = ClasificadorKeras(model_path)
                    print("  Cambiado a modo REAL")
                else:
                    clasificador = ClasificadorSimulado()
                    print("  Cambiado a modo SIMULADO")
            else:
                print("  No hay modelo entrenado — solo modo simulado disponible")

        elif key == ord('q') or key == ord('Q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print(f"\nTest finalizado. {clasificaciones} clasificaciones realizadas.")


if __name__ == "__main__":
    main()
