"""
EcoSort IA — Test de clasificacion en terminal (sin ventana grafica)
====================================================================
Usa tu webcam para clasificar objetos, pero muestra los resultados
directo en la terminal. No necesita ventana grafica (cv2.imshow).

Util cuando macOS bloquea las ventanas de OpenCV.

Uso:
    source venv/bin/activate
    python src/test_terminal.py

Controles:
    ENTER  → Tomar foto y clasificar
    Q      → Salir
"""

import os
import sys
import time
import numpy as np

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

sys.path.append(os.path.join(os.path.dirname(__file__)))
from config import (
    CLASES, IMG_SIZE, CONFIDENCE_THRESHOLD,
    TFLITE_MODEL_PATH, TFLITE_INT8_PATH, MODEL_SAVE_PATH
)


def cargar_modelo():
    """Carga el mejor modelo disponible."""
    import tensorflow as tf

    for path, nombre in [(TFLITE_INT8_PATH, 'TFLite INT8'),
                          (TFLITE_MODEL_PATH, 'TFLite FP32')]:
        if os.path.exists(path):
            interpreter = tf.lite.Interpreter(model_path=path)
            interpreter.allocate_tensors()
            size_kb = os.path.getsize(path) / 1024
            print(f"  Modelo: {nombre} ({size_kb:.0f} KB)")
            return interpreter

    print("ERROR: No se encuentra ningun modelo entrenado.")
    print("  Entrena primero: python src/training/train_model.py")
    sys.exit(1)


def clasificar(interpreter, frame):
    """Clasifica un frame con el modelo TFLite."""
    import cv2

    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    img = cv2.resize(frame, IMG_SIZE)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = img.astype(np.float32) / 255.0
    img = np.expand_dims(img, axis=0)

    t_start = time.time()
    interpreter.set_tensor(input_details[0]['index'], img)
    interpreter.invoke()
    output = interpreter.get_tensor(output_details[0]['index'])
    latencia = (time.time() - t_start) * 1000

    probs = output[0]
    clase_idx = np.argmax(probs)
    return CLASES[clase_idx], float(probs[clase_idx]), probs, latencia


def main():
    import cv2

    print("=" * 55)
    print("  EcoSort IA — CLASIFICACION EN TERMINAL")
    print("  (sin ventana grafica)")
    print("=" * 55)

    # Cargar modelo
    interpreter = cargar_modelo()

    # Abrir webcam
    print("\n  Abriendo webcam...")
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("\n  ERROR: No se pudo abrir la webcam.")
        print("  Posibles soluciones:")
        print("    1. Ajustes > Privacidad > Camara > activar Terminal")
        print("    2. Cerrar Terminal (Cmd+Q) y volver a abrir")
        print("    3. Reiniciar la Mac")
        print("\n  Mientras tanto, puedes probar con imagenes del dataset:")
        print("    python src/test_terminal.py --dataset")
        
        if len(sys.argv) > 1 and sys.argv[1] == '--dataset':
            probar_con_dataset(interpreter)
        sys.exit(1)

    print(f"  Webcam activa: {int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))}x"
          f"{int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))}")
    print(f"\n  ENTER = tomar foto y clasificar")
    print(f"  Q     = salir")
    print()

    colores_terminal = {
        "plastico": "\033[94m",   # Azul
        "papel":    "\033[93m",   # Amarillo
        "carton":   "\033[33m",   # Naranja
        "aluminio": "\033[37m",   # Gris claro
    }
    RESET = "\033[0m"
    GREEN = "\033[92m"
    RED = "\033[91m"

    contador = 0

    while True:
        entrada = input("─── Presiona ENTER para clasificar (q=salir) ───> ")

        if entrada.strip().lower() == 'q':
            break

        # Capturar varios frames para que la camara se estabilice
        for _ in range(5):
            ret, frame = cap.read()

        if not ret:
            print("  Error capturando imagen")
            continue

        # Clasificar
        clase, confianza, probs, latencia = clasificar(interpreter, frame)
        contador += 1

        # Guardar la foto capturada
        os.makedirs("capturas", exist_ok=True)
        foto_path = f"capturas/captura_{contador:03d}.jpg"
        cv2.imwrite(foto_path, frame)

        # Mostrar resultado
        color = colores_terminal.get(clase, "")
        print(f"\n  ╔═══════════════════════════════╗")
        print(f"  ║  CLASIFICACION #{contador:3d}             ║")
        print(f"  ╠═══════════════════════════════╣")
        print(f"  ║  Resultado: {color}{clase.upper():12s}{RESET}       ║")
        print(f"  ║  Confianza: {confianza*100:5.1f}%              ║")
        print(f"  ║  Latencia:  {latencia:5.1f} ms             ║")
        print(f"  ╠═══════════════════════════════╣")

        for i, c in enumerate(CLASES):
            bar_len = int(probs[i] * 25)
            bar = "█" * bar_len + "░" * (25 - bar_len)
            marker = " ◄" if c == clase else ""
            c_color = colores_terminal.get(c, "")
            print(f"  ║  {c_color}{c:10s}{RESET} {bar} {probs[i]*100:5.1f}%{marker}")

        accion = f"{GREEN}DESVIAR{RESET}" if confianza >= CONFIDENCE_THRESHOLD else f"{RED}RECHAZAR{RESET}"
        print(f"  ╠═══════════════════════════════╣")
        print(f"  ║  Accion: {accion}                  ║")
        print(f"  ║  Foto:   {foto_path:21s} ║")
        print(f"  ╚═══════════════════════════════╝\n")

    cap.release()
    print(f"\n  {contador} clasificaciones realizadas.")
    print(f"  Fotos guardadas en: capturas/")


def probar_con_dataset(interpreter):
    """Prueba el modelo con imagenes del dataset (sin webcam)."""
    import cv2

    print(f"\n{'='*55}")
    print(f"  PROBANDO CON IMAGENES DEL DATASET")
    print(f"{'='*55}\n")

    dataset_dir = "dataset"
    if not os.path.exists(dataset_dir):
        print("  No hay dataset descargado.")
        print("  Corre: python src/training/download_dataset.py")
        return

    correctas = 0
    total = 0

    for clase_real in CLASES:
        clase_dir = os.path.join(dataset_dir, clase_real)
        imgs = sorted([f for f in os.listdir(clase_dir) if f.endswith('.jpg')])[:5]

        for img_file in imgs:
            img = cv2.imread(os.path.join(clase_dir, img_file))
            clase_pred, conf, probs, lat = clasificar(interpreter, img)
            total += 1
            ok = clase_pred == clase_real
            if ok:
                correctas += 1

            status = "\033[92mOK\033[0m" if ok else "\033[91mFAIL\033[0m"
            print(f"  {clase_real:10s} → {clase_pred:10s} ({conf*100:5.1f}%) [{status}]")

    print(f"\n  Resultado: {correctas}/{total} = {correctas/total*100:.1f}%")


if __name__ == "__main__":
    # Si se pasa --dataset, probar con imagenes del dataset directamente
    if len(sys.argv) > 1 and sys.argv[1] == '--dataset':
        print("=" * 55)
        print("  EcoSort IA — PRUEBA CON DATASET")
        print("=" * 55)
        interpreter = cargar_modelo()
        probar_con_dataset(interpreter)
    else:
        main()
