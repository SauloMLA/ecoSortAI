"""
EcoSort IA — Script de inferencia (clasificacion de residuos)
=============================================================
Clasifica objetos reciclables usando un modelo MobileNetV2 TFLite.

Puede correr en:
  - Laptop/PC: para pruebas con webcam (modo simulacion, sin GPIO)
  - Raspberry Pi 5: con camara + mecanismo fisico (cuando este listo)

Uso:
    python src/inference/classify.py

Prerequisitos:
    pip install opencv-python numpy
    + tensorflow (laptop) o tflite-runtime (RPi)

Archivos necesarios:
    models/ecosort_model.tflite       (modelo float32)
    o models/ecosort_model_int8.tflite (modelo cuantizado, mas rapido)
"""

import os
import sys
import time
import json
import numpy as np
import cv2
from datetime import datetime

# Agregar ruta del proyecto
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from config import (
    CLASES, IMG_SIZE, CONFIDENCE_THRESHOLD,
    TFLITE_MODEL_PATH, TFLITE_INT8_PATH, TRIGGER_PIN,
    LED_PINS, TIEMPO_LED_ENCENDIDO
)

# --- Detectar si estamos en Raspberry Pi ---
IS_RASPBERRY_PI = os.path.exists('/proc/device-tree/model')

if IS_RASPBERRY_PI:
    import RPi.GPIO as GPIO

# Importar TFLite interpreter (compatible con laptop y RPi)
try:
    import tflite_runtime.interpreter as tflite
except ImportError:
    try:
        import tensorflow.lite as tflite
    except (ImportError, AttributeError):
        # TF 2.x cambia la ruta
        import tensorflow as tf
        tflite = tf.lite


class EcoSortClassifier:
    """
    Clasificador principal de EcoSort IA.
    Carga el modelo TFLite, captura imagenes, y clasifica.

    El mecanismo fisico (motores/servos) se integrara cuando
    el diseno mecanico este finalizado.
    """

    def __init__(self, model_path=None):
        # Seleccionar modelo: preferir INT8 si existe, si no float32
        if model_path is None:
            if os.path.exists(TFLITE_INT8_PATH):
                model_path = TFLITE_INT8_PATH
            elif os.path.exists(TFLITE_MODEL_PATH):
                model_path = TFLITE_MODEL_PATH
            else:
                print("ERROR: No se encuentra ningun modelo entrenado.")
                print("  Buscado en:")
                print(f"    {TFLITE_INT8_PATH}")
                print(f"    {TFLITE_MODEL_PATH}")
                print("\nPrimero entrena el modelo:")
                print("  python src/training/download_dataset.py")
                print("  python src/training/train_model.py")
                sys.exit(1)

        print("=" * 50)
        print("  EcoSort IA — Iniciando sistema")
        print(f"  Modo: {'Raspberry Pi' if IS_RASPBERRY_PI else 'Laptop (sin GPIO)'}")
        print(f"  Clases: {CLASES}")
        print(f"  Umbral de confianza: {CONFIDENCE_THRESHOLD*100:.0f}%")
        print("=" * 50)

        # Cargar modelo TFLite
        self._cargar_modelo(model_path)

        # Inicializar camara
        self._iniciar_camara()

        # Inicializar sensor trigger y LEDs (solo en RPi)
        if IS_RASPBERRY_PI:
            self._iniciar_sensor()
            self._iniciar_leds()

        # Log de clasificaciones
        self.log = []

        print("\n[OK] Sistema listo. Esperando objetos...\n")

    def _cargar_modelo(self, model_path):
        """Carga el modelo TFLite en memoria."""
        print(f"\nCargando modelo: {model_path}")
        self.interpreter = tflite.Interpreter(model_path=model_path)
        self.interpreter.allocate_tensors()

        # Obtener indices de entrada y salida
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()

        input_shape = self.input_details[0]['shape']
        print(f"  Input shape:  {input_shape}")
        print(f"  Input dtype:  {self.input_details[0]['dtype']}")
        print(f"  Output shape: {self.output_details[0]['shape']}")

        # Verificar tamaño del modelo
        size_kb = os.path.getsize(model_path) / 1024
        print(f"  Tamaño:       {size_kb:.0f} KB")

    def _iniciar_camara(self):
        """Inicializa la camara (USB o CSI via OpenCV)."""
        print("\nInicializando camara...")
        self.cap = cv2.VideoCapture(0)  # 0 = camara default

        if not self.cap.isOpened():
            print("ADVERTENCIA: No se pudo abrir la camara.")
            print("Continuando en modo sin camara (para testing).")
            self.cap = None
            return

        # Configurar resolucion (640x480 es suficiente)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        print(f"  Camara activa: {int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))}x"
              f"{int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))}")

    def _iniciar_sensor(self):
        """Configura el sensor IR como trigger (solo RPi)."""
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(TRIGGER_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        print(f"  Sensor IR en GPIO {TRIGGER_PIN}")

    def _iniciar_leds(self):
        """Configura los LEDs como salidas GPIO (solo RPi)."""
        for clase, pin in LED_PINS.items():
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW)
        print(f"  LEDs en GPIO: {list(LED_PINS.values())}")

    def preprocesar_imagen(self, frame):
        """
        Preprocesa un frame de la camara para el modelo.
        - Resize a 224x224
        - Normalizar a 0-1
        - Expandir dimensiones para batch
        """
        img = cv2.resize(frame, IMG_SIZE)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # OpenCV usa BGR, modelo usa RGB
        img = img.astype(np.float32) / 255.0
        img = np.expand_dims(img, axis=0)  # (1, 224, 224, 3)
        return img

    def clasificar(self, frame):
        """
        Clasifica un frame y retorna (clase, confianza, todas_probabilidades, latencia_ms).
        """
        img = self.preprocesar_imagen(frame)

        # Inferencia
        t_start = time.time()
        self.interpreter.set_tensor(self.input_details[0]['index'], img)
        self.interpreter.invoke()
        output = self.interpreter.get_tensor(self.output_details[0]['index'])
        t_end = time.time()

        # Interpretar resultado
        probabilidades = output[0]
        clase_idx = np.argmax(probabilidades)
        confianza = float(probabilidades[clase_idx])
        clase = CLASES[clase_idx]
        latencia_ms = (t_end - t_start) * 1000

        return clase, confianza, probabilidades, latencia_ms

    def activar_mecanismo(self, clase):
        """
        Activa el mecanismo fisico de desvio.

        En RPi con LEDs: enciende el LED de la clase clasificada.
        En laptop: solo imprime (simulacion).
        """
        if IS_RASPBERRY_PI and LED_PINS:
            # Apagar todos los LEDs
            for pin in LED_PINS.values():
                GPIO.output(pin, GPIO.LOW)
            # Encender el LED de la clase
            if clase in LED_PINS:
                GPIO.output(LED_PINS[clase], GPIO.HIGH)
                print(f"  [LED] Encendido: {clase.upper()} (GPIO {LED_PINS[clase]})")
                time.sleep(TIEMPO_LED_ENCENDIDO)
                GPIO.output(LED_PINS[clase], GPIO.LOW)
        else:
            print(f"  [SIM] Desviaria a contenedor: {clase.upper()}")

    def esperar_objeto(self):
        """Espera a que el sensor IR detecte un objeto."""
        if IS_RASPBERRY_PI:
            print("Esperando objeto en sensor IR...", end='', flush=True)
            GPIO.wait_for_edge(TRIGGER_PIN, GPIO.FALLING)
            time.sleep(0.3)
            print(" DETECTADO!")
            return True
        else:
            input("Presiona ENTER para simular deteccion de objeto...")
            return True

    def capturar_frame(self):
        """Captura un frame de la camara."""
        if self.cap and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                return frame
        # Si no hay camara, generar imagen de prueba
        print("  [SIM] Generando imagen de prueba aleatoria")
        return np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)

    def registrar_clasificacion(self, clase, confianza, latencia_ms):
        """Registra la clasificacion en el log."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "clase": clase,
            "confianza": round(confianza, 4),
            "latencia_ms": round(latencia_ms, 1),
            "actuo": confianza >= CONFIDENCE_THRESHOLD
        }
        self.log.append(entry)
        return entry

    def guardar_log(self, filepath="logs/clasificaciones.json"):
        """Guarda el log de clasificaciones a disco."""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump(self.log, f, indent=2, ensure_ascii=False)
        print(f"\nLog guardado: {filepath} ({len(self.log)} entradas)")

    def loop_principal(self):
        """
        Loop principal del sistema.
        1. Esperar objeto (sensor IR en RPi, ENTER en laptop)
        2. Capturar imagen
        3. Clasificar
        4. Actuar si la confianza es suficiente
        5. Registrar
        """
        print("\n" + "=" * 50)
        print("  SISTEMA ACTIVO — Ctrl+C para salir")
        print("=" * 50 + "\n")

        contador = 0

        try:
            while True:
                self.esperar_objeto()

                frame = self.capturar_frame()

                clase, confianza, probs, latencia = self.clasificar(frame)

                contador += 1
                print(f"\n--- Objeto #{contador} ---")
                print(f"  Clasificacion: {clase.upper()}")
                print(f"  Confianza:     {confianza*100:.1f}%")
                print(f"  Latencia:      {latencia:.1f} ms")
                print(f"  Probabilidades:")
                for i, c in enumerate(CLASES):
                    bar = "█" * int(probs[i] * 30)
                    print(f"    {c:12s} {probs[i]*100:5.1f}% {bar}")

                if confianza >= CONFIDENCE_THRESHOLD:
                    print(f"\n  → Desviando a contenedor: {clase.upper()}")
                    self.activar_mecanismo(clase)
                else:
                    print(f"\n  → Confianza insuficiente ({confianza*100:.0f}% < "
                          f"{CONFIDENCE_THRESHOLD*100:.0f}%). No se actua.")

                self.registrar_clasificacion(clase, confianza, latencia)

        except KeyboardInterrupt:
            print("\n\nSistema detenido por el usuario.")
        finally:
            self.cleanup()

    def cleanup(self):
        """Limpia recursos al salir."""
        self.guardar_log()
        if self.cap:
            self.cap.release()
        if IS_RASPBERRY_PI:
            GPIO.cleanup()
        print("Recursos liberados. Hasta luego.")


def main():
    clasificador = EcoSortClassifier()
    clasificador.loop_principal()


if __name__ == "__main__":
    main()
