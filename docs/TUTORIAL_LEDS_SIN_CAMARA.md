# Tutorial fácil — 4 LEDs en Raspberry Pi (sin cámara)

Hasta que tengas la webcam, puedes **ver los 4 LEDs encenderse** con un programa de prueba. No hace falta cámara ni modelo de IA.

---

## Si nunca usaste una Raspberry Pi — ¿cómo “hago algo en la Pi”?

La Pi es una **computadora aparte**. No es que el Mac “controle” la Pi con un solo cable USB como un disco.

### Lo que sí necesitas en la Pi

- **Alimentación** (cargador USB-C correcto para Pi 4/5).
- **Tarjeta microSD** con **Raspberry Pi OS** ya instalado.
- **WiFi** configurado (en el primer arranque te pide red y contraseña).

### Dos formas de escribir comandos “en la Pi”

**Forma A — Con monitor en la Pi (la más visual la primera vez)**  
1. Conecta **monitor + teclado + ratón** a la Pi.  
2. Enciende la Pi.  
3. Abre el menú y busca **Terminal** (consola negra).  
4. Todo lo que decimos “en la Pi” lo escribes **ahí**. Eso ya es “estar en la Pi”.

**Forma B — Desde tu Mac, por la red (WiFi)**  
1. Mac y Pi en la **misma WiFi de tu casa** (no hace falta cable entre Mac y Pi).  
2. En la Pi (con monitor o la primera vez que la configuras) activa **SSH** y anota la **IP** (en Terminal de la Pi: `hostname -I`).  
3. En el **Terminal del Mac** escribes:
   ```bash
   ssh pi@192.168.1.XX
   ```
   (cambia `pi` por tu usuario de la Pi y la IP por la tuya).  
4. Te pide contraseña de la Pi. Después la ventana del Mac **es** la consola de la Pi: aquí también haces `git clone`, `python`, etc.

> **No** hace falta enchufar la Pi al Mac con USB solo para esto. Lo normal es **WiFi + SSH**.  
> (Conectar Pi al Mac por USB con trucos avanzados existe, pero no lo necesitas al inicio.)

### Qué es `git clone` en la Pi

Es un comando que escribes **en el Terminal de la Pi** (Forma A o B). Descarga una copia de tu repo de GitHub **dentro de la Pi**, por internet:

```bash
cd ~
git clone https://github.com/SauloMLA/ecoSortAI.git
cd ecoSortAI
```

Necesitas que la Pi **tenga internet** (WiFi). Tu Mac no tiene que estar conectado por cable a la Pi; solo hace falta que ambos estén en la misma red si usas SSH desde el Mac.

---

## Qué necesitas

| Cosas | Cantidad |
|-------|----------|
| Raspberry Pi encendida y con WiFi | 1 |
| Protoboard | 1 |
| LED | 4 |
| Resistencia **220 Ω** | 4 |
| Cable dupont (hembra ↔ macho o como te sirva) | Varios |
| Mac o PC en la misma WiFi | 1 |

**En la Pi:** SSH activo (menú `raspi-config` → Interface Options → SSH → Enable).

---

## Parte 1 — Cómo conectar los 4 LEDs

### Regla de oro

**GPIO → resistencia 220 Ω → patilla larga del LED (+) → patilla corta del LED (−) → GND**

Nunca conectes el LED directo al GPIO sin resistencia.

### Patilla del LED

- **Larga** = positivo (+), va hacia la resistencia (hacia el GPIO).
- **Corta** = negativo (−), va a **GND**.

### Pines de la Pi que usamos (números **GPIO**, no posición física)

| LED | Clase (para después) | Pin GPIO |
|-----|----------------------|----------|
| 1 | Plástico | **17** |
| 2 | Papel | **27** |
| 3 | Cartón | **22** |
| 4 | Aluminio | **23** |

### Dónde están en la Pi 40 pines (referencia)

Busca en una imagen “Raspberry Pi GPIO pinout”. Los BCM son:

- **GPIO 17** = pin físico **11**
- **GPIO 27** = pin físico **13**
- **GPIO 22** = pin físico **15**
- **GPIO 23** = pin físico **16**
- **GND** = varios; usa por ejemplo pin **6**, **9**, **14**, **20**, **25**, **39** (todos son GND)

### Montaje en protoboard (repite 4 veces)

```
   Pi                          Protoboard
   ───                         ──────────

   Pin GPIO 17 ────►  [220 Ω] ───► LED+  LED- ───► cable a rail GND
   Pin GPIO 27 ────►  [220 Ω] ───► LED+  LED- ───► mismo rail GND
   Pin GPIO 22 ────►  [220 Ω] ───► LED+  LED- ───► mismo rail GND
   Pin GPIO 23 ────►  [220 Ω] ───► LED+  LED- ───► mismo rail GND

   Pin GND de la Pi ────► mismo rail negro (GND) de la protoboard
```

Los **cuatro** LED− deben llegar al **mismo GND** (y ese GND a un pin GND de la Pi).

### Checklist visual antes de encender

- [ ] Cada GPIO tiene su resistencia **antes** del LED.
- [ ] Los 4 negativos de los LED van a GND.
- [ ] Nada une **5V** con **GND** directo (corto).

---

## Parte 2 — Pasar los archivos a la Raspberry

Necesitas la **IP** de la Pi (en la Pi: `hostname -I`) y tu **usuario** (ej. `pi`).

### Opción A — Copiar toda la carpeta del proyecto (más fácil)

En tu **Mac**, Terminal (cambia la ruta si tu proyecto está en otro sitio):

```bash
scp -r "/Users/salaniz/practice folder/trash-bot" pi@192.168.1.XX:~/
```

Cambia `pi` por tu usuario y `192.168.1.XX` por la IP real.

En la **Pi** tendrás: `~/trash-bot/`

### Opción B — Si ya clonaste desde GitHub en la Pi

En la **Pi**:

```bash
cd ~
git clone https://github.com/SauloMLA/ecoSortAI.git
cd ecoSortAI
```

*(Usa la URL de tu repo si es distinta.)*

### Archivos imprescindibles para la prueba de LEDs

- `src/rpi_test_leds.py`
- `src/config.py`

Si copiaste la carpeta completa o hiciste `git clone`, ya los tienes.

---

## Parte 3 — Instalar Python y correr la prueba (en la Pi)

Conéctate por SSH desde el Mac:

```bash
ssh pi@192.168.1.XX
```

Luego en la **Pi**:

```bash
cd ~/trash-bot
# o: cd ~/ecoSortAI

sudo apt update
sudo apt install -y python3 python3-pip python3-venv

python3 -m venv venv
source venv/bin/activate

pip install RPi.GPIO
```

Ejecuta la prueba de LEDs:

```bash
python src/rpi_test_leds.py
```

### Qué hacer en el programa

| Tecla | Efecto |
|-------|--------|
| **1** | Enciende LED de plástico (GPIO 17) |
| **2** | Enciende LED de papel (GPIO 27) |
| **3** | Enciende LED de cartón (GPIO 22) |
| **4** | Enciende LED de aluminio (GPIO 23) |
| **a** | Secuencia: los 4 uno tras otro |
| **q** | Salir |

Si ves los LEDs cambiar, **el cableado y el programa están bien**. Cuando tengas la C270, seguirás con la guía grande y `classify.py`.

---

## Si algo falla

| Problema | Qué revisar |
|----------|-------------|
| `ssh` no conecta | Misma WiFi, IP correcta, SSH activado en la Pi |
| LED no prende | Polaridad, resistencia en serie, GND común |
| `No module named RPi` | `source venv/bin/activate` y `pip install RPi.GPIO` |
| Script dice “solo en Raspberry Pi” | Lo ejecutaste en el Mac; debe ser **en la Pi** |

---

## Siguiente paso (cuando tengas cámara)

Lee [`RASPBERRY_PI_PRIMERA_VEZ.md`](RASPBERRY_PI_PRIMERA_VEZ.md) — sección de cámara y modelo TFLite.
