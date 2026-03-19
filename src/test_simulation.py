"""
EcoSort IA — Test de simulacion (SIN hardware, SIN modelo)
===========================================================
Ejecuta este script en tu laptop para probar que todo funciona
ANTES de tener la Raspberry Pi o el modelo entrenado.

Simula:
- Deteccion de objetos (presionas Enter)
- Clasificacion (genera resultados aleatorios)
- Activacion de servos (muestra en consola)
- Log de clasificaciones

Uso:
    python src/test_simulation.py

No necesitas: Raspberry Pi, camara, servos, modelo entrenado.
Solo necesitas: Python 3 y numpy.
"""

import os
import sys
import time
import json
import random
import numpy as np
from datetime import datetime

sys.path.append(os.path.join(os.path.dirname(__file__)))
from config import (
    CLASES, CONFIDENCE_THRESHOLD,
    SERVO_PINS, SERVO_CERRADO, SERVO_ABIERTO,
    TIEMPO_APERTURA_SERVO, TIEMPO_ESPERA_CAIDA
)


def simular_clasificacion():
    """Simula una clasificacion con probabilidades aleatorias."""
    # Generar probabilidades que sumen 1
    probs = np.random.dirichlet(np.ones(len(CLASES)) * 2)
    # Hacer que una clase domine (simular modelo confiado)
    dominante = random.randint(0, len(CLASES) - 1)
    probs[dominante] += 0.5
    probs = probs / probs.sum()  # Re-normalizar

    clase_idx = np.argmax(probs)
    return CLASES[clase_idx], float(probs[clase_idx]), probs


def simular_mecanismo(clase, gpio):
    """Simula el mecanismo fisico v4 con arte ASCII."""
    compartimentos = {
        "plastico": ("S1", "FRENTE"),
        "papel":    ("S2", "ATRAS"),
        "carton":   ("S3", "DERECHA"),
        "aluminio": ("S4", "IZQUIERDA"),
    }

    servo, posicion = compartimentos[clase]

    plastico_mark = " ██" if clase == "plastico" else "   "
    papel_mark = "██ " if clase == "papel" else "   "
    carton_mark = "██ " if clase == "carton" else "   "
    aluminio_mark = " ██" if clase == "aluminio" else "   "

    print(f"\n  ┌───────────────────────┐")
    print(f"  │   MECANISMO v4 ACTIVO  │")
    print(f"  │                        │")
    print(f"  │  Servo {servo} (GPIO {gpio:2d})   │")
    print(f"  │  Solapa: {posicion:10s}     │")
    print(f"  │                        │")
    print(f"  │  {plastico_mark}  │  {papel_mark}  │")
    print(f"  │  PLAS │ PAPEL  │")
    print(f"  │ ──────┼─────── │")
    print(f"  │  ALUM │ CART   │")
    print(f"  │  {aluminio_mark}  │  {carton_mark}  │")
    print(f"  │                        │")
    print(f"  │  Servo {SERVO_CERRADO}° → {SERVO_ABIERTO}° ABRIENDO│")

    time.sleep(0.5)
    print(f"  │  ...objeto cayendo...  │")
    time.sleep(0.3)
    print(f"  │  Servo {SERVO_ABIERTO}° → {SERVO_CERRADO}° CERRADO │")
    print(f"  │  ✓ Listo               │")
    print(f"  └───────────────────────┘")


def main():
    print("=" * 55)
    print("  EcoSort IA — SIMULACION DE PRUEBA")
    print("  (sin hardware, sin modelo, sin camara)")
    print("=" * 55)
    print(f"\n  Categorias: {CLASES}")
    print(f"  Umbral de confianza: {CONFIDENCE_THRESHOLD*100:.0f}%")
    print(f"  Servos (GPIO): {SERVO_PINS}")
    print(f"\n  Presiona ENTER para simular un objeto")
    print(f"  Escribe 'q' para salir")
    print(f"  Escribe 'stats' para ver estadisticas")
    print()

    log = []
    stats = {clase: 0 for clase in CLASES}
    rechazados = 0
    total = 0

    while True:
        entrada = input("─── Depositar objeto [ENTER] / 'q' salir / 'stats' ───> ")

        if entrada.strip().lower() == 'q':
            break

        if entrada.strip().lower() == 'stats':
            print(f"\n  === ESTADISTICAS ===")
            print(f"  Total objetos: {total}")
            print(f"  Clasificados:  {total - rechazados}")
            print(f"  Rechazados:    {rechazados}")
            if total > 0:
                for clase in CLASES:
                    pct = stats[clase] / total * 100 if total > 0 else 0
                    bar = "█" * int(pct / 3)
                    print(f"    {clase:12s} {stats[clase]:3d} ({pct:4.1f}%) {bar}")
            print()
            continue

        total += 1
        print(f"\n  ▼ Objeto #{total} detectado por sensor IR")

        # Simular captura de imagen
        print(f"  📷 Capturando imagen...")
        time.sleep(0.2)

        # Simular clasificacion
        t_start = time.time()
        clase, confianza, probs = simular_clasificacion()
        latencia = random.uniform(50, 150)  # Simular latencia realista

        print(f"\n  === RESULTADO ===")
        print(f"  Clase:      {clase.upper()}")
        print(f"  Confianza:  {confianza*100:.1f}%")
        print(f"  Latencia:   {latencia:.0f} ms")
        print(f"\n  Probabilidades:")
        for i, c in enumerate(CLASES):
            bar = "█" * int(probs[i] * 30)
            marker = " ◄" if c == clase else ""
            print(f"    {c:12s} {probs[i]*100:5.1f}% {bar}{marker}")

        # Decidir si actuar
        if confianza >= CONFIDENCE_THRESHOLD:
            gpio = SERVO_PINS[clase]
            print(f"\n  ✓ Confianza suficiente — activando mecanismo")
            simular_mecanismo(clase, gpio)
            stats[clase] += 1
        else:
            print(f"\n  ✗ Confianza insuficiente ({confianza*100:.0f}% < "
                  f"{CONFIDENCE_THRESHOLD*100:.0f}%)")
            print(f"    Objeto no clasificado — se requiere intervencion manual")
            rechazados += 1

        # Log
        log.append({
            "timestamp": datetime.now().isoformat(),
            "objeto": total,
            "clase": clase,
            "confianza": round(confianza, 4),
            "latencia_ms": round(latencia, 1),
            "actuo": confianza >= CONFIDENCE_THRESHOLD
        })

        print()

    # Resumen final
    print(f"\n{'='*55}")
    print(f"  RESUMEN DE SESION")
    print(f"{'='*55}")
    print(f"  Objetos procesados:  {total}")
    print(f"  Clasificados OK:     {total - rechazados}")
    print(f"  Rechazados:          {rechazados}")
    if total > 0:
        print(f"  Tasa de aceptacion:  {(total-rechazados)/total*100:.1f}%")
    print(f"\n  Distribucion:")
    for clase in CLASES:
        print(f"    {clase:12s} → {stats[clase]} objetos")

    # Guardar log
    os.makedirs("logs", exist_ok=True)
    logfile = f"logs/simulacion_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(logfile, 'w') as f:
        json.dump(log, f, indent=2, ensure_ascii=False)
    print(f"\n  Log guardado: {logfile}")
    print(f"\n  Simulacion terminada.")


if __name__ == "__main__":
    main()
