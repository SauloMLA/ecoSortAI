# Raspberry Pi — Guía para empezar desde cero (EcoSort IA)

> **¿Solo quieres conectar 4 LEDs y verlos sin cámara?** Guía corta paso a paso: [**`TUTORIAL_LEDS_SIN_CAMARA.md`**](TUTORIAL_LEDS_SIN_CAMARA.md)

Este documento amplía conceptos (SSH, venv, GPIO) y explica **cámara + IA** cuando ya las tengas.

> **Subir el código a GitHub:** [`MANUAL_GITHUB.md`](MANUAL_GITHUB.md)

---

## 1. Conceptos rápidos (si nunca programaste en la Pi)

| Término | Qué es |
|--------|--------|
| **Raspberry Pi** | Una computadora pequeña. Tiene Linux (Raspberry Pi OS), puertos USB, GPIO (pines para LEDs, sensores). |
| **Terminal / consola** | Ventana de texto donde escribes comandos. En la Pi: aplicación **Terminal**. En tu Mac: **Terminal.app**. |
| **SSH** | Conectarte a la Pi **desde el Mac por red**, sin monitor: ves el Terminal de la Pi en tu Mac. |
| **GPIO** | Pines de la Pi que mandan encendido/apagado (3.3 V o 0 V). Los usamos para los LEDs. |
| **Protoboard (breadboard)** | Tablero con agujeros para armar circuitos sin soldar. Los cables **dupont** van de la Pi a la proto. |
| **Entorno virtual (`venv`)** | Carpeta aislada con sus propias librerías Python, para no mezclar con el sistema. |

---

## 2. Qué necesitas

- Raspberry Pi 4 o 5 con Raspberry Pi OS instalado y **WiFi o cable Ethernet**.
- **Monitor + teclado** la primera vez, **o** haber activado SSH antes (imagen preconfigurada).
- Mac o PC en la **misma red WiFi**.
- Cables **dupont** (macho-hembra), **protoboard**, 4 **LEDs**, 4 **resistencias 220 Ω**, cable negro a **GND**.
- (Más adelante) Cámara USB o Pi Camera.
- (Opcional) Botón entre **GPIO 24** y **GND** para disparar en `classify.py`.

---

## 3. Primera configuración de la Pi (una vez)

1. Enciende la Pi y termina el asistente (idioma, WiFi, usuario y contraseña).
2. Abre **Terminal** en la Pi y ejecuta:
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```
3. Activa **SSH** (para trabajar desde el Mac):
   ```bash
   sudo raspi-config
   ```
   - **Interface Options** → **SSH** → **Enable** → Finish.
4. Anota la **IP** de la Pi:
   ```bash
   hostname -I
   ```
   Ejemplo: `192.168.1.45`

---

## 4. Conectar desde tu Mac (SSH)

En el **Terminal del Mac**:

```bash
ssh TU_USUARIO@192.168.1.45
```

Sustituye `TU_USUARIO` (ej. `pi`) y la IP. Escribe la contraseña de la Pi.

A partir de aquí, los comandos largos son **en la Pi** (por SSH o Terminal en la Pi).

---

## 5. Instalar herramientas básicas en la Pi

```bash
sudo apt install -y python3 python3-pip python3-venv git
```

---

## 6. Pasar el proyecto a la Pi

### Opción A — Clonar desde GitHub

```bash
cd ~
git clone https://github.com/SauloMLA/ecoSortAI.git
cd ecoSortAI
```

*(Cambia la URL si tu repo tiene otro nombre.)*

### Opción B — Copiar carpeta desde el Mac

En el **Mac** (ajusta ruta, usuario e IP):

```bash
scp -r "/Users/salaniz/practice folder/trash-bot" pi@192.168.1.45:~/
```

En la **Pi**: `cd ~/trash-bot`

---

## 7. Entorno Python y librerías

Dentro de la carpeta del proyecto en la Pi:

```bash
cd ~/ecoSortAI    # o ~/trash-bot

python3 -m venv venv
source venv/bin/activate
```

Verás `(venv)` al inicio de la línea. Luego:

```bash
pip install --upgrade pip
pip install RPi.GPIO numpy
```

**Para cuando tengas cámara y quieras clasificar con IA**, además:

```bash
pip install tflite-runtime opencv-python-headless
```

`opencv-python-headless` sirve para `classify.py` (sin ventana). Si quieres **ver el video en una ventana** (`preview_webcam_leds.py` o `test_with_webcam.py`), instala el paquete con GUI:

```bash
pip uninstall -y opencv-python-headless
pip install opencv-python
```

---

## 8. Modelo TFLite (solo cuando vayas a usar `classify.py`)

Si en GitHub **no** subes la carpeta `models/`, cópiala desde el **Mac**:

```bash
# En el Mac
scp ~/ruta/a/tu/proyecto/models/ecosort_model_int8.tflite pi@192.168.1.45:~/ecoSortAI/models/
```

En la Pi:

```bash
mkdir -p ~/ecoSortAI/models
ls ~/ecoSortAI/models/
```

---

## 9. Esquema: Pi + protoboard + LEDs

**Pines BCM** (los que usa el código en `config.py`):

| Clase     | GPIO |
|-----------|------|
| Plástico  | 17   |
| Papel     | 27   |
| Cartón    | 22   |
| Aluminio  | 23   |

**Cada LED** (repite 4 veces):

```
GPIO (17, 27, 22 o 23) ──► resistencia 220 Ω ──► patilla larga del LED (+)
patilla corta del LED (−) ──► GND de la Pi (cualquier pin GND)
```

Une todos los **GND** de los LEDs al mismo **rail negro** de la protoboard y de ahí **un** cable a un pin **GND** de la Pi.

**No pongas el LED directo al GPIO sin resistencia.**

**Trigger opcional** (para `classify.py`): un cable de **GPIO 24** y otro a **GND** con un **botón** en medio (al pulsar, 24 toca GND).

---

## 10. Sin cámara todavía — probar solo los LEDs

Con el `venv` activado:

```bash
cd ~/ecoSortAI
source venv/bin/activate
python src/rpi_test_leds.py
```

- Pulsa **1**, **2**, **3**, **4** para encender el LED de cada clase.
- Pulsa **a** para una secuencia automática.
- **q** para salir.

Así confirmas cableado y que Python habla con la Pi **sin cámara ni modelo**.

---

## 11. Con cámara — clasificación real + LEDs

1. Conecta la **cámara USB** (o activa Pi Camera en `raspi-config`).
2. Instala dependencias extra:
   ```bash
   pip install tflite-runtime opencv-python-headless
   ```
   Para **preview en ventana** + LEDs automáticos:
   ```bash
   pip uninstall -y opencv-python-headless
   pip install opencv-python
   pip install tflite-runtime
   ```
3. Asegúrate de tener al menos un archivo `.tflite` en `models/`.
4. Ejecuta:
   ```bash
   cd ~/ecoSortAI
   source venv/bin/activate
   python src/inference/classify.py
   ```
   O, con ventana de cámara y LEDs según la IA:
   ```bash
   python src/preview_webcam_leds.py
   ```
5. Coloca el objeto frente a la cámara y **dispara** con el botón en GPIO 24 (o sensor IR). Si la confianza es ≥ 70%, se enciende el LED de esa clase.

Si la cámara no abre, en la Pi prueba:
```bash
python3 -c "import cv2; c=cv2.VideoCapture(0); print('OK' if c.isOpened() else 'FAIL'); c.release()"
```
Si falla con `0`, prueba cambiar a `1` en código o en otra ranura USB.

---

## 12. Resumen de comandos (orden típico)

| Paso | Dónde | Qué |
|------|--------|-----|
| 1 | Pi | `sudo apt update`, activar SSH, anotar IP |
| 2 | Mac | `ssh usuario@IP` |
| 3 | Pi | `git clone` o recibir carpeta por `scp` |
| 4 | Pi | `python3 -m venv venv` → `source venv/bin/activate` |
| 5 | Pi | `pip install RPi.GPIO numpy` |
| 6 | Pi | Montar LEDs en protoboard |
| 7 | Pi | `python src/rpi_test_leds.py` |
| 8 | (después) | `pip install tflite-runtime opencv-python-headless` + copiar `models/*.tflite` |
| 9 | (después) | `python src/inference/classify.py` |

---

## 13. Problemas frecuentes

| Síntoma | Qué revisar |
|---------|-------------|
| Python 3.13 en la Pi | tflite-runtime y TensorFlow no tienen wheels. Usar Pi con Python 3.11 (Raspberry Pi OS Bookworm) o instalar Python 3.11 con pyenv. |
| `ssh: Connection refused` | SSH desactivado o IP incorrecta |
| LED no enciende | Polaridad del LED, resistencia, GND común, pin GPIO correcto |
| `No module named RPi` | `source venv/bin/activate` y `pip install RPi.GPIO` |
| `rpi_test_leds` dice que no es Pi | Debe ejecutarse en la Pi, no en el Mac |
| Sin modelo al correr `classify.py` | Copiar `.tflite` a `models/` |
| `cv2.imshow` / «The function is not implemented» | Quita `opencv-python-headless` e instala `opencv-python`; hace falta escritorio o VNC, no solo SSH sin DISPLAY |

---

*EcoSort IA — una sola guía para la Raspberry Pi*
