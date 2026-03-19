# Plan — Pruebas en Raspberry Pi con LEDs

**Objetivo:** Ejecutar EcoSort IA en la Raspberry Pi y encender un LED distinto según la clase clasificada (plástico, papel, cartón, aluminio).

---

## Qué tienes

- [x] Raspberry Pi
- [x] Modelo TFLite entrenado
- [x] Código de clasificación

---

## Qué necesitas comprar / tener

| Item | Cantidad | Uso | Precio aprox. |
|------|----------|-----|---------------|
| **LED** (cualquier color) | 4 | Uno por clase | $5–20 MXN |
| **Resistencia 220–330 Ω** | 4 | Limitar corriente del LED | $10–20 MXN |
| **Cables jumper** (macho-hembra) | 8–12 | Conectar RPi ↔ LEDs | $30–50 MXN |
| **Cámara USB** o **Pi Camera** | 1 | Capturar imagen para clasificar | $150–400 MXN |
| **Sensor IR** o **botón** (opcional) | 1 | Detectar objeto; si no, modificar código para ENTER | — |

**Total estimado:** $200–500 MXN (sin cámara ya la tienes).

---

## Esquema de conexión — 4 LEDs

```
                    Raspberry Pi 5 (vista GPIO)

    ┌─────────────────────────────────────────┐
    │  3V3  (1) (2)  5V                      │
    │  GPIO2 (3) (4)  5V                      │
    │  GPIO3 (5) (6)  GND                     │
    │  GPIO4 (7) (8)  GPIO14                  │
    │  GND   (9)(10)  GPIO15                  │
    │  GPIO17(11)(12) GPIO18   ← PLÁSTICO    │
    │  GPIO27(13)(14) GND      ← PAPEL       │
    │  GPIO22(15)(16) GPIO23   ← CARTÓN      │
    │  3V3  (17)(18) GPIO24   ← ALUMINIO    │
    │  ...                                    │
    └─────────────────────────────────────────┘

    Cada LED:
    ┌─────────┐         ┌─────────┐
    │  GPIO   │───┬─────│  R220Ω  │─────┬─────│ LED +  │
    │  (17,27,│   │     └─────────┘     │     │ LED -  │
    │  22,23) │   │                     │     └────┬───┘
    └─────────┘   │                     │          │
                  │                     └──────────┼─── GND
                  └────────────────────────────────┘
```

**Pines GPIO por clase:**

| Clase | GPIO | Color LED sugerido |
|-------|------|--------------------|
| Plástico | 17 | Azul |
| Papel | 27 | Verde |
| Cartón | 22 | Naranja |
| Aluminio | 23 | Gris/Blanco |

---

## Paso a paso — Cómo hacerlo

### 1. Preparar la Raspberry Pi

```bash
# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar Python 3 y pip
sudo apt install -y python3 python3-pip python3-venv

# Instalar dependencias del sistema para OpenCV
sudo apt install -y libopencv-dev python3-opencv

# O si usas tflite-runtime (más ligero que tensorflow):
sudo apt install -y python3-pip
pip3 install tflite-runtime opencv-python-headless numpy RPi.GPIO
```

### 2. Clonar o copiar el proyecto

**Opción A — Desde GitHub (después de subir):**
```bash
cd ~
git clone https://github.com/TU_USUARIO/trash-bot.git
cd trash-bot
```

**Opción B — Copiar desde tu Mac (USB, SCP, etc.):**
```bash
# Desde tu Mac:
scp -r "/Users/salaniz/practice folder/trash-bot" pi@IP_DE_LA_RPI:~/
```

### 3. Crear entorno virtual e instalar dependencias

```bash
cd ~/trash-bot

python3 -m venv venv
source venv/bin/activate

# En RPi: usar tflite-runtime (no tensorflow completo)
pip install tflite-runtime opencv-python-headless numpy RPi.GPIO
```

### 4. Copiar el modelo a la RPi

El modelo TFLite debe estar en `models/`:

```bash
# Si lo copias desde tu Mac:
scp -r "/Users/salaniz/practice folder/trash-bot/models" pi@IP_DE_LA_RPI:~/trash-bot/
```

O descargarlo desde tu repo si lo subiste.

### 5. Conectar los LEDs

| GPIO | Cable | Resistencia | LED |
|------|-------|-------------|-----|
| 17 | jumper → GPIO 17 | 220Ω → patilla + LED | patilla - LED → GND |
| 27 | jumper → GPIO 27 | 220Ω → patilla + LED | patilla - LED → GND |
| 22 | jumper → GPIO 22 | 220Ω → patilla + LED | patilla - LED → GND |
| 23 | jumper → GPIO 23 | 220Ω → patilla + LED | patilla - LED → GND |

**Cuidado:** La patilla larga del LED es el ánodo (+). Conecta siempre la resistencia en serie con el LED.

### 6. Ejecutar el programa

```bash
cd ~/trash-bot
source venv/bin/activate

# Con cámara (modo automático con sensor IR si está conectado)
python src/inference/classify.py

# O el script de prueba con webcam (si prefieres)
python src/test_with_webcam.py
```

### 7. Probar

1. Mostrar un objeto a la cámara.
2. Activar detección: **sensor IR** (si está conectado) o **botón en GPIO 24 → GND**.
3. El modelo clasifica.
4. Si confianza ≥ 70%, se enciende el LED correspondiente 2 segundos.

**Sin sensor IR:** Conecta un botón entre GPIO 24 y GND. Al presionar simula detección. O modifica `classify.py` para usar `input()` en RPi (modo debug).

---

## Modificaciones necesarias en el código

El método `activar_mecanismo()` en `classify.py` actualmente solo imprime. Hay que cambiarlo para que:

1. Encienda el LED de la clase correcta.
2. Apague los demás.
3. Mantenga el LED encendido unos segundos.
4. Apague todos los LEDs.

Las configuraciones de pines ya están en `config.py` con `SERVO_PINS` — podemos reutilizarlos como `LED_PINS` para esta prueba.

---

## Checklist antes de probar

- [ ] RPi instalada y con acceso (SSH o pantalla)
- [ ] 4 LEDs + 4 resistencias conectados a GPIO 17, 27, 22, 23
- [ ] Cámara conectada (USB o CSI)
- [ ] Proyecto copiado en la RPi
- [ ] `venv` creado y dependencias instaladas
- [ ] Modelo `ecosort_model.tflite` o `ecosort_model_int8.tflite` en `models/`
- [ ] Código actualizado para controlar LEDs

---

## Próximos pasos (después de LEDs)

1. Validar clasificación con objetos reales.
2. Ajustar umbral de confianza si hace falta.
3. Integrar sensor IR si está disponible.
4. Pasar al mecanismo con bowl + motores a pasos (cuando tengas el hardware).
