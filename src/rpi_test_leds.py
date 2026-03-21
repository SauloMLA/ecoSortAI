#!/usr/bin/env python3
"""
EcoSort IA — Prueba de LEDs en Raspberry Pi (sin cámara ni modelo)
==================================================================
Sirve para comprobar cableado en protoboard ANTES de tener cámara o TFLite.

Solo depende de: RPi.GPIO (y config.py para los pines).

Uso en la Pi:
  cd ~/tu-proyecto
  source venv/bin/activate
  pip install RPi.GPIO   # si aún no está
  python src/rpi_test_leds.py
"""

import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
from config import LED_PINS, TIEMPO_LED_ENCENDIDO

IS_RPI = os.path.exists("/proc/device-tree/model")


def main():
    if not IS_RPI:
        print("Este script solo debe ejecutarse en una Raspberry Pi.")
        print("En tu Mac usa la simulación: python src/test_simulation.py")
        sys.exit(1)

    import RPi.GPIO as GPIO

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    for pin in LED_PINS.values():
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)

    print("=" * 55)
    print("  EcoSort IA — PRUEBA DE LEDs (sin cámara)")
    print("=" * 55)
    print(f"  Pines: {LED_PINS}")
    print()
    print("  Comandos:")
    print("    1-4  Enciende el LED de esa clase (1=plastico ... 4=aluminio)")
    print("    a    Enciende todos uno por uno (secuencia)")
    print("    q    Salir")
    print()

    try:
        while True:
            cmd = input("LED [1-4 / a / q] > ").strip().lower()

            if cmd == "q":
                break

            if cmd == "a":
                for clase, pin in LED_PINS.items():
                    for p in LED_PINS.values():
                        GPIO.output(p, GPIO.LOW)
                    GPIO.output(pin, GPIO.HIGH)
                    print(f"  → {clase.upper()} (GPIO {pin})")
                    time.sleep(TIEMPO_LED_ENCENDIDO)
                for p in LED_PINS.values():
                    GPIO.output(p, GPIO.LOW)
                print("  Secuencia terminada.\n")
                continue

            mapping = {"1": "plastico", "2": "papel", "3": "carton", "4": "aluminio"}
            if cmd not in mapping:
                print("  Opción no válida.\n")
                continue

            clase = mapping[cmd]
            pin = LED_PINS[clase]
            for p in LED_PINS.values():
                GPIO.output(p, GPIO.LOW)
            GPIO.output(pin, GPIO.HIGH)
            print(f"  Encendido: {clase.upper()} (GPIO {pin}) — {TIEMPO_LED_ENCENDIDO}s")
            time.sleep(TIEMPO_LED_ENCENDIDO)
            GPIO.output(pin, GPIO.LOW)
            print("  Apagado.\n")

    finally:
        for p in LED_PINS.values():
            GPIO.output(p, GPIO.LOW)
        GPIO.cleanup()
        print("GPIO liberado. Hasta luego.")


if __name__ == "__main__":
    main()
