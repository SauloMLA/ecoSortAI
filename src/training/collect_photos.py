"""
EcoSort IA — Herramienta de recoleccion de fotos
=================================================
Usa este script para tomar fotos con la camara y organizarlas
automaticamente en las carpetas del dataset.

Uso:
    python src/training/collect_photos.py plastico
    python src/training/collect_photos.py papel
    python src/training/collect_photos.py carton
    python src/training/collect_photos.py aluminio

Controles:
    ESPACIO  → Tomar foto
    Q        → Salir
"""

import os
import sys
import cv2
from datetime import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from config import CLASES, DATASET_DIR


def main():
    # Verificar argumento
    if len(sys.argv) < 2 or sys.argv[1] not in CLASES:
        print(f"Uso: python {sys.argv[0]} <clase>")
        print(f"Clases validas: {', '.join(CLASES)}")
        sys.exit(1)

    clase = sys.argv[1]
    output_dir = os.path.join(DATASET_DIR, clase)
    os.makedirs(output_dir, exist_ok=True)

    # Contar fotos existentes
    existing = len([f for f in os.listdir(output_dir)
                   if f.lower().endswith(('.jpg', '.jpeg', '.png'))])

    print(f"\n{'='*50}")
    print(f"  Recoleccion de fotos: {clase.upper()}")
    print(f"  Carpeta: {output_dir}")
    print(f"  Fotos existentes: {existing}")
    print(f"{'='*50}")
    print(f"\n  ESPACIO = tomar foto | Q = salir\n")

    # Abrir camara
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("ERROR: No se pudo abrir la camara")
        sys.exit(1)

    count = existing

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Mostrar preview con info
        display = frame.copy()
        cv2.putText(display, f"Clase: {clase.upper()}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(display, f"Fotos: {count}", (10, 65),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        cv2.putText(display, "ESPACIO=foto  Q=salir", (10, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

        cv2.imshow(f"EcoSort - Captura: {clase}", display)

        key = cv2.waitKey(1) & 0xFF

        if key == ord(' '):
            # Guardar foto
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            filename = f"{clase}_{timestamp}.jpg"
            filepath = os.path.join(output_dir, filename)
            cv2.imwrite(filepath, frame)
            count += 1
            print(f"  [{count}] Guardada: {filename}")

        elif key == ord('q') or key == ord('Q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    print(f"\nTotal fotos de '{clase}': {count}")
    print(f"Recomendado minimo: 200 fotos por clase")
    if count < 200:
        print(f"Faltan: {200 - count} fotos mas")


if __name__ == "__main__":
    main()
