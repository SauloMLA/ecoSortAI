"""
EcoSort IA — Descarga automatica de dataset de imagenes
========================================================
Descarga imagenes del dataset TrashNet (Stanford/garythung) desde
Hugging Face (parquet) y las organiza en las carpetas del proyecto.

TrashNet contiene ~2,500 imagenes de materiales reciclables.
Mapeamos sus categorias a las nuestras:
    cardboard → carton
    paper     → papel
    plastic   → plastico
    metal     → aluminio
    glass     → [ignorado]
    trash     → [ignorado]

Uso:
    pip install pyarrow Pillow
    python src/training/download_dataset.py

El script crea:
    dataset/
    ├── plastico/   (~482 imagenes)
    ├── papel/      (~594 imagenes)
    ├── carton/     (~403 imagenes)
    └── aluminio/   (~410 imagenes)
"""

import os
import sys
import io
import json
import urllib.request
import tempfile

# Agregar ruta del proyecto
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from config import CLASES, DATASET_DIR

# --- Configuracion ---

# TrashNet labels: 0=cardboard, 1=glass, 2=metal, 3=paper, 4=plastic, 5=trash
TRASHNET_LABEL_MAP = {
    0: "carton",      # cardboard → carton
    2: "aluminio",    # metal → aluminio
    3: "papel",       # paper → papel
    4: "plastico",    # plastic → plastico
}

# Parquet files en Hugging Face
HF_PARQUET_API = "https://huggingface.co/api/datasets/garythung/trashnet/parquet/default/train"


def obtener_urls_parquet():
    """Obtiene las URLs de los archivos parquet del dataset."""
    req = urllib.request.Request(HF_PARQUET_API, headers={
        'User-Agent': 'EcoSort-IA/1.0'
    })
    resp = urllib.request.urlopen(req, timeout=30)
    urls = json.loads(resp.read().decode())
    return urls


def descargar_archivo(url, destino):
    """Descarga un archivo grande con barra de progreso simple."""
    req = urllib.request.Request(url, headers={
        'User-Agent': 'EcoSort-IA/1.0'
    })
    resp = urllib.request.urlopen(req, timeout=120)
    total = int(resp.headers.get('Content-Length', 0))
    descargado = 0
    chunk_size = 1024 * 256  # 256 KB

    with open(destino, 'wb') as f:
        while True:
            chunk = resp.read(chunk_size)
            if not chunk:
                break
            f.write(chunk)
            descargado += len(chunk)
            if total > 0:
                pct = descargado / total * 100
                mb = descargado / (1024 * 1024)
                print(f"\r    Descargando: {mb:.1f} MB ({pct:.0f}%)", end='', flush=True)

    print()  # Nueva linea


def main():
    print("=" * 60)
    print("  EcoSort IA — Descarga automatica de dataset")
    print("  Fuente: TrashNet (garythung) via Hugging Face")
    print("=" * 60)
    print(f"\n  Categorias EcoSort: {CLASES}")
    print(f"  Mapeo TrashNet → EcoSort:")
    nombres_tn = {0: "cardboard", 2: "metal", 3: "paper", 4: "plastic"}
    for idx, ecosort in TRASHNET_LABEL_MAP.items():
        print(f"    {nombres_tn[idx]:12s} → {ecosort}")
    print(f"  Ignorando: glass, trash")
    print(f"\n  Destino: {DATASET_DIR}/")

    # Crear carpetas del dataset
    for clase in CLASES:
        os.makedirs(os.path.join(DATASET_DIR, clase), exist_ok=True)

    # Contar imagenes existentes
    existentes_total = 0
    for clase in CLASES:
        clase_dir = os.path.join(DATASET_DIR, clase)
        n = len([f for f in os.listdir(clase_dir)
                if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
        existentes_total += n
        print(f"    {clase:12s} ya tiene {n} imagenes")

    if existentes_total > 1800:
        print(f"\n  Dataset ya parece completo ({existentes_total} imagenes).")
        print(f"  Para re-descargar, borra la carpeta '{DATASET_DIR}/' primero.")
        return

    # Importar dependencias
    try:
        import pyarrow.parquet as pq
        from PIL import Image
    except ImportError:
        print("\n  ERROR: Faltan dependencias.")
        print("    pip install pyarrow Pillow")
        sys.exit(1)

    # Obtener URLs de parquet
    print(f"\n  Obteniendo lista de archivos...")
    try:
        parquet_urls = obtener_urls_parquet()
    except Exception as e:
        print(f"\n  ERROR conectando con Hugging Face: {e}")
        sys.exit(1)

    print(f"  Encontrados {len(parquet_urls)} archivos parquet")

    # Contadores
    stats = {clase: 0 for clase in CLASES}
    ignoradas = 0

    # Procesar cada archivo parquet
    for file_idx, url in enumerate(parquet_urls):
        print(f"\n  Archivo {file_idx + 1}/{len(parquet_urls)}:")

        # Descargar parquet a archivo temporal
        with tempfile.NamedTemporaryFile(suffix='.parquet', delete=False) as tmp:
            tmp_path = tmp.name

        try:
            descargar_archivo(url, tmp_path)

            # Leer parquet
            table = pq.read_table(tmp_path)
            df = table.to_pandas()
            print(f"    Filas en este archivo: {len(df)}")

            for _, row in df.iterrows():
                label = row.get("label")

                # Verificar si es una categoria que nos interesa
                if label not in TRASHNET_LABEL_MAP:
                    ignoradas += 1
                    continue

                clase_ecosort = TRASHNET_LABEL_MAP[label]

                # Extraer imagen (viene como dict con 'bytes')
                image_data = row.get("image")
                if image_data is None:
                    ignoradas += 1
                    continue

                # La imagen puede venir como dict {'bytes': b'...', 'path': '...'}
                if isinstance(image_data, dict):
                    img_bytes = image_data.get("bytes")
                elif isinstance(image_data, bytes):
                    img_bytes = image_data
                else:
                    ignoradas += 1
                    continue

                if img_bytes is None:
                    ignoradas += 1
                    continue

                # Guardar imagen
                stats[clase_ecosort] += 1
                idx = stats[clase_ecosort]
                filename = f"trashnet_{clase_ecosort}_{idx:04d}.jpg"
                filepath = os.path.join(DATASET_DIR, clase_ecosort, filename)

                try:
                    img = Image.open(io.BytesIO(img_bytes))
                    if img.mode != "RGB":
                        img = img.convert("RGB")
                    img.save(filepath, "JPEG", quality=95)
                except Exception as e:
                    stats[clase_ecosort] -= 1
                    print(f"    Error guardando imagen: {e}")
                    continue

            total_hasta_ahora = sum(stats.values())
            print(f"    Total acumulado: {total_hasta_ahora} imagenes")

        finally:
            # Limpiar archivo temporal
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

    # Resumen final
    total_guardadas = sum(stats.values())
    print(f"\n{'='*60}")
    print(f"  DESCARGA COMPLETADA")
    print(f"{'='*60}")
    print(f"\n  Imagenes por categoria:")
    for clase in CLASES:
        clase_dir = os.path.join(DATASET_DIR, clase)
        total_en_carpeta = len([f for f in os.listdir(clase_dir)
                               if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
        suficiente = "OK (200+)" if total_en_carpeta >= 200 else "POCAS (<200)"
        print(f"    {clase:12s} → {total_en_carpeta:4d} imagenes  [{suficiente}]")
    print(f"\n  Total guardadas:         {total_guardadas}")
    print(f"  Ignoradas (glass/trash): {ignoradas}")
    print(f"  Dataset en: {DATASET_DIR}/")
    print(f"\n  Siguiente paso:")
    print(f"    python src/training/train_model.py")


if __name__ == "__main__":
    main()
