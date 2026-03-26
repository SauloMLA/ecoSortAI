#!/usr/bin/env python3
"""
EcoSort IA — Vista de cámara + clasificación automática + LEDs (RPi)
====================================================================
Muestra en vivo lo que ve la webcam, clasifica con el mismo modelo TFLite/Keras
que el resto del proyecto y, si la confianza supera el umbral (`config.py`),
enciende el LED correspondiente a la clase — igual que `activar_mecanismo` en
`src/inference/classify.py` (sin teclas manuales para los LEDs).

El pulso del LED va en un hilo para no congelar el video durante
`TIEMPO_LED_ENCENDIDO`.

Uso:
  python src/preview_webcam_leds.py
  python src/preview_webcam_leds.py --camera 1 --interval 0.5

  q — salir
"""
from __future__ import annotations

import argparse
import os
import sys
import threading
import time

import cv2
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from config import (
    CLASES,
    CONFIDENCE_THRESHOLD,
    IMG_SIZE,
    LED_PINS,
    MODEL_SAVE_PATH,
    TIEMPO_LED_ENCENDIDO,
    TFLITE_INT8_PATH,
    TFLITE_MODEL_PATH,
)
from test_with_webcam import ClasificadorKeras, ClasificadorSimulado, ClasificadorTFLite

IS_RPI = os.path.exists("/proc/device-tree/model")


def _tflite_candidates_laptop():
    c = []
    if os.path.exists(TFLITE_INT8_PATH):
        c.append(os.path.abspath(TFLITE_INT8_PATH))
    if os.path.exists(TFLITE_MODEL_PATH):
        p = os.path.abspath(TFLITE_MODEL_PATH)
        if p not in c:
            c.append(p)
    return c


def _tflite_candidates_pi():
    fp32 = os.path.abspath(TFLITE_MODEL_PATH)
    int8 = os.path.abspath(TFLITE_INT8_PATH)
    c = []
    if os.path.exists(fp32):
        c.append(fp32)
    if os.path.exists(int8) and int8 not in c:
        c.append(int8)
    return c


def build_clasificador():
    """Prioridad TFLite (FP32 primero en Pi), luego Keras, luego simulado."""
    tflite_paths = _tflite_candidates_pi() if IS_RPI else _tflite_candidates_laptop()
    for path in tflite_paths:
        try:
            clf = ClasificadorTFLite(path)
            print(f"  Clasificador: TFLite ({path})")
            return clf, True
        except Exception as e:
            print(f"  TFLite falló ({path}): {e}")

    if os.path.exists(MODEL_SAVE_PATH):
        try:
            clf = ClasificadorKeras(MODEL_SAVE_PATH)
            print(f"  Clasificador: Keras ({MODEL_SAVE_PATH})")
            return clf, True
        except Exception as e:
            print(f"  Keras falló: {e}")

    print("  Sin modelo: modo simulado.")
    return ClasificadorSimulado(), False


def setup_led_gpio():
    import RPi.GPIO as GPIO

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    for pin in LED_PINS.values():
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)
    return GPIO


def pulse_led_thread_fn(gpio_mod, lock: threading.Lock, clase: str, busy: threading.Event):
    """Igual idea que classify.activar_mecanismo (solo LEDs)."""
    if clase not in LED_PINS:
        busy.clear()
        return
    pin = LED_PINS[clase]
    try:
        with lock:
            for p in LED_PINS.values():
                gpio_mod.output(p, gpio_mod.LOW)
            gpio_mod.output(pin, gpio_mod.HIGH)
        print(f"  [LED] {clase.upper()} (GPIO {pin})")
        time.sleep(TIEMPO_LED_ENCENDIDO)
        with lock:
            gpio_mod.output(pin, gpio_mod.LOW)
    finally:
        busy.clear()


def roi_center_box(frame):
    h, w = frame.shape[:2]
    cx, cy = w // 2, h // 2
    box_size = min(w, h) // 2
    x1 = cx - box_size // 2
    y1 = cy - box_size // 2
    x2 = cx + box_size // 2
    y2 = cy + box_size // 2
    return frame[y1:y2, x1:x2], (x1, y1, x2, y2)


def main():
    parser = argparse.ArgumentParser(
        description="Webcam + clasificación EcoSort + LEDs automáticos (RPi)"
    )
    parser.add_argument("--camera", type=int, default=0, help="Índice de cámara OpenCV")
    parser.add_argument(
        "--interval",
        type=float,
        default=0.35,
        help="Segundos entre inferencias (default 0.35)",
    )
    parser.add_argument(
        "--cooldown",
        type=float,
        default=None,
        help="Mínimo segundos entre activaciones de LED (default: max(2, TIEMPO_LED_ENCENDIDO))",
    )
    args = parser.parse_args()

    cooldown = args.cooldown
    if cooldown is None:
        cooldown = max(2.0, float(TIEMPO_LED_ENCENDIDO))

    print("=" * 55)
    print("  EcoSort IA — Cámara + auto-clasificación + LEDs")
    print(f"  Umbral: {CONFIDENCE_THRESHOLD*100:.0f}%  |  GPIO: {'sí' if IS_RPI else 'no (SIM)'}")
    print("=" * 55)

    clasificador, modo_real = build_clasificador()

    gpio = None
    gpio_lock = threading.Lock()
    led_busy = threading.Event()
    if IS_RPI:
        gpio = setup_led_gpio()
        print(f"  LEDs listos: {LED_PINS}")

    cap = cv2.VideoCapture(args.camera)
    if not cap.isOpened():
        print(f"ERROR: no se abrió la cámara {args.camera}")
        if gpio:
            import RPi.GPIO as GPIO

            GPIO.cleanup()
        sys.exit(1)

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    win = "EcoSort IA — cámara + detección → LED"
    last_infer = 0.0
    last_led_trigger = 0.0
    ultima_clase = ""
    ultima_conf = 0.0
    ultima_lat = 0.0

    colores = {
        "plastico": (255, 165, 0),
        "papel": (255, 255, 100),
        "carton": (139, 90, 43),
        "aluminio": (200, 200, 200),
    }

    print("\n  q = salir\n")

    try:
        while True:
            ok, frame = cap.read()
            if not ok:
                break

            display = frame.copy()
            roi, (x1, y1, x2, y2) = roi_center_box(frame)
            cv2.rectangle(display, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(
                display,
                "Zona de clasificación",
                (x1, max(20, y1 - 8)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                1,
            )

            now = time.time()
            if roi.size > 0 and (now - last_infer) >= args.interval:
                last_infer = now
                clase, conf, _probs, lat = clasificador.clasificar(roi)
                ultima_clase, ultima_conf, ultima_lat = clase, conf, lat

                actuar = conf >= CONFIDENCE_THRESHOLD
                if actuar and (now - last_led_trigger) >= cooldown and not led_busy.is_set():
                    last_led_trigger = now
                    if gpio:
                        led_busy.set()
                        threading.Thread(
                            target=pulse_led_thread_fn,
                            args=(gpio, gpio_lock, clase, led_busy),
                            daemon=True,
                        ).start()
                    else:
                        print(f"  [SIM] LED → {clase.upper()} ({conf*100:.1f}%)")

            color = colores.get(ultima_clase, (255, 255, 255))
            estado = "LED" if ultima_conf >= CONFIDENCE_THRESHOLD else "bajo umbral"
            if led_busy.is_set():
                estado += " | LED activo"

            y0 = 28
            cv2.putText(
                display,
                f"{ultima_clase.upper()} {ultima_conf*100:.1f}%  ({estado})",
                (10, y0),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                color,
                2,
            )
            cv2.putText(
                display,
                f"lat {ultima_lat:.0f}ms  {'REAL' if modo_real else 'SIM'}  q=salir",
                (10, y0 + 22),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.45,
                (220, 220, 220),
                1,
            )

            ph = 112
            if roi.size > 0:
                preview_small = cv2.resize(cv2.resize(roi, IMG_SIZE), (ph, ph))
                h, w = display.shape[:2]
                display[10 : 10 + ph, w - ph - 10 : w - 10] = preview_small

            cv2.imshow(win, display)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()
        if led_busy.is_set():
            time.sleep(0.05)
        if gpio:
            import RPi.GPIO as GPIO

            with gpio_lock:
                for p in LED_PINS.values():
                    GPIO.output(p, GPIO.LOW)
            GPIO.cleanup()
            print("GPIO liberado.")


if __name__ == "__main__":
    main()
