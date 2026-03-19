# Diseño del Mecanismo v4 — Bote Cuadrado con Pirámide Invertida

**Sesión:** S002  
**Autores:** Chair (diseño de referencia), Mechanical Lead  
**Fecha:** 2026-02-13  
**Revisión:** 4.1 — Corregido con referencia directa del Chair  
**Renders:** `S002_render_design-v4-final.png`

---

## RESUMEN EJECUTIVO

| Aspecto | Valor |
|---------|-------|
| **Forma** | Cuadrada — 40×40×70 cm |
| **Compuertas** | 4 solapas triangulares (pirámide invertida) — son la superficie superior del bote |
| **Espesor de solapa** | ~3-5 mm (MDF o acrílico delgado) |
| **Servos** | 4× SG90, montados por FUERA de la pared |
| **EL SERVO ES LA BISAGRA** | Sin bisagras separadas, sin varillaje, sin soportes L |
| **Ángulo cerrado** | ~20° — solapas inclinadas formando pirámide |
| **Ángulo abierto** | ~75° — solapa se abre, objeto cae al bote |
| **Cámara** | Montada en arco metálico sobre el bote (~15 cm de alto), mirando al centro |
| **Contenedores** | 4 botes internos cuadrados (20×20 cm), extraíbles |
| **Piezas por compuerta** | 1 servo + 1 horn + 2 tornillos + 1 agujero en pared |
| **Total piezas mecanismo** | 4 servos, 4 horns, 8 tornillos, 4 agujeros |

---

## CONCEPTO GENERAL

```
                    ┌─ CÁMARA + SENSOR IR
                    │  (mira hacia abajo al centro)
                ┌───┴───┐
                │  ◉ IR │
            ┌───┘       └───┐  ← ARCO metálico (~15 cm alto)
            │               │
    ┌───────┴───────────────┴───────┐
    │╲    PAPEL (green)          ╱│
    │  ╲                      ╱   │  ← 4 SOLAPAS = superficie superior
    │    ╲                  ╱     │     del bote, formando pirámide
    │      ╲    OBJETO   ╱       │     invertida. El objeto reposa
    │ PLÁST ╲   aquí  ╱  CARTÓN │     sobre ellas.
    │ (blue)  ╲     ╱  (orange)  │
    │           ╲ ╱               │
    │            ╳ ← vértice      │
    │     ALUMINIO (gray)         │
    ├─────────┬───────────────────┤
    │ ┌─────┐ │ ┌─────┐           │
    │ │BOTE │ │ │BOTE │           │  ← 4 CONTENEDORES internos
    │ │  1  │ │ │  2  │           │     (extraíbles)
    │ └─────┘ │ └─────┘           │
    │ ┌─────┐ │ ┌─────┐           │
    │ │BOTE │ │ │BOTE │           │
    │ │  3  │ │ │  4  │           │
    │ └─────┘ │ └─────┘           │
    └─────────┴───────────────────┘
```

**NO hay "zona de inspección" separada.** Las compuertas cerradas SON la superficie donde reposa el objeto. La cámara en el arco toma la foto desde arriba.

---

## DIMENSIONES

| Componente | Medida |
|-----------|--------|
| **Ancho del bote** | 40 cm |
| **Profundidad del bote** | 40 cm |
| **Altura del bote** | 70 cm |
| **Altura del arco (cámara)** | ~15 cm sobre el bote |
| **Altura total con arco** | ~85 cm |
| **Espesor de solapas** | 3-5 mm |
| **Contenedores internos** | 4× cuadrados de ~20×20 cm |

---

## ARCO DE CÁMARA

```
    Vista frontal:

        ┌─────────────┐
        │ ◉ CÁMARA    │  ← Cámara RPi mirando hacia ABAJO
        │ [IR] sensor  │     al centro de las 4 solapas
        └──────┬───────┘
          ╱    │    ╲
        ╱      │      ╲     ← Arco de tubo metálico o impreso 3D
      ╱        │        ╲      ~15 cm de alto
    ┌──────────┴──────────┐
    │    BOTE (40×40)     │
```

- Tubo metálico o varilla de aluminio doblada en arco
- Se fija a la pared trasera del bote
- La cámara y el sensor IR van montados en el centro del arco
- La cámara mira directo hacia ABAJO, al centro de la pirámide
- Los LEDs de iluminación pueden ir en el arco también

---

## LAS 4 SOLAPAS (COMPUERTAS)

### Vista superior — la X que forma la pirámide:

```
    ┌────────────────────────────────────┐
    │╲              S1               ╱│
    │  ╲                            ╱  │
    │    ╲     PAPEL (green)     ╱    │
    │      ╲                  ╱       │
    │        ╲              ╱         │
    │ S4      ╲           ╱      S2  │
    │ PLÁSTICO  ╲       ╱  CARTÓN    │
    │  (blue)     ╲   ╱   (orange)   │
    │               ╳                 │
    │  ALUMINIO   ╱   ╲              │
    │   (gray)  ╱       ╲            │
    │ S3      ╱           ╲      S4  │
    │        ╱              ╲         │
    │      ╱    ALUMINIO      ╲      │
    │    ╱       (gray)         ╲    │
    │  ╱                          ╲  │
    │╱              S3               ╲│
    └────────────────────────────────────┘

    S1, S2, S3, S4 = posición de cada servo
    (montado por FUERA de la pared correspondiente)
```

### Colores de cada solapa:

| Solapa | Servo | Color | Tipo de basura | Pared |
|--------|-------|-------|----------------|-------|
| Frente | S1 | Azul (blue) | Plástico | Pared frontal |
| Atrás | S2 | Verde (green) | Papel | Pared trasera |
| Derecha | S3 | Naranja (orange) | Cartón | Pared derecha |
| Izquierda | S4 | Gris (gray) | Aluminio | Pared izquierda |

---

## MECÁNICA DEL SERVO — EL SERVO ES LA BISAGRA

### Principio fundamental:

> **EL SERVO ES LA BISAGRA.**  
> No hay bisagras separadas. No hay soportes L. No hay brazos de varillaje.  
> El eje de rotación del servo ES el eje de rotación de la compuerta.

### Montaje: Servo por FUERA de la pared

```
    EXTERIOR          │PARED│          INTERIOR
    del bote          │     │          del bote
                      │     │
    ┌──────────┐      │     │
    │  SERVO   │      │     │
    │  SG90    ├─eje──┤AGUJ.├──horn──► SOLAPA (3-5mm)
    │          │      │     │
    └──────────┘      │     │
    (2 tornillos)     │     │
                      │     │

    El servo queda PROTEGIDO de la basura.
    Solo el horn y eje pasan al interior.
```

### Funcionamiento de la compuerta:

```
    CERRADO (~20°)                     ABIERTO (~75°)
    PWM = 1.0 ms                       PWM = 1.8 ms

    ───[SERVO]───                      ───[SERVO]───
          │                                  │
          eje                                eje
           ╲                                      ╱
             ╲                                  ╱
               ╲ ← solapa                     ╱ ← solapa
                 ╲  inclinada               ╱    abierta
                   ╲  ~20°               ╱      a ~75°
                     ╲                ╱
                       ╲           ╱
                                ╱
    ▲ objeto reposa            │  objeto cae ▼▼▼
      sobre la solapa          │  al contenedor
                               ▼
```

**El servo gira ~55° (de 20° a 75°).** Bien dentro del rango del SG90 (0°-180°).

---

## SECUENCIA DE OPERACIÓN

```
PASO 1 — DEPÓSITO
  El usuario coloca el objeto sobre las solapas cerradas.
  Las 4 solapas forman la pirámide → el objeto reposa en el centro.
  S1=20°  S2=20°  S3=20°  S4=20°
                    │
                    ▼
PASO 2 — DETECCIÓN
  El sensor IR (en el arco) detecta que hay un objeto.
  Los LEDs se encienden.
  La cámara (en el arco) toma la foto mirando hacia abajo.
                    │
                    ▼
PASO 3 — CLASIFICACIÓN
  RPi 5 ejecuta MobileNetV2 TFLite INT8.
  Resultado: "PLÁSTICO" — 92% confianza.
  (Si < 70%, no actúa)
                    │
                    ▼
PASO 4 — APERTURA
  Se envía PWM al S1 (Plástico, pared frontal):
    S1: 20° → 75°  (PWM 1.0ms → 1.8ms)
  La solapa azul se abre hacia afuera/abajo.
  El objeto desliza y cae al contenedor de Plástico.
  S1=75°  S2=20°  S3=20°  S4=20°
                    │
                    ▼
PASO 5 — CIERRE
  Después de 1.5 segundos:
    S1: 75° → 20°  (PWM 1.8ms → 1.0ms)
  S1=20°  S2=20°  S3=20°  S4=20°
  Listo para el siguiente objeto.
```

---

## ASIGNACIÓN DE SERVOS

| Servo | GPIO Pin | Compuerta | Basura | Color | PWM cerrado | PWM abierto |
|-------|----------|-----------|--------|-------|-------------|-------------|
| S1 | GPIO 17 | Frente | Plástico | Azul | 1.0 ms (20°) | 1.8 ms (75°) |
| S2 | GPIO 27 | Atrás | Papel | Verde | 1.0 ms (20°) | 1.8 ms (75°) |
| S3 | GPIO 22 | Derecha | Cartón | Naranja | 1.0 ms (20°) | 1.8 ms (75°) |
| S4 | GPIO 23 | Izquierda | Aluminio | Gris | 1.0 ms (20°) | 1.8 ms (75°) |

---

## CÓDIGO PWM — CONTROL DEL SERVO SG90

```python
import RPi.GPIO as GPIO
import time

# Pines de los 4 servos
SERVO_PINS = {
    "plastico": 17,   # S1 — Frente (azul)
    "papel": 27,      # S2 — Atrás (verde)
    "carton": 22,     # S3 — Derecha (naranja)
    "aluminio": 23,   # S4 — Izquierda (gris)
}

CERRADO = 20   # 20° — solapa formando pirámide
ABIERTO = 75   # 75° — solapa abierta

GPIO.setmode(GPIO.BCM)

def setup_servos():
    """Inicializa los 4 servos en posición cerrada."""
    servos = {}
    for clase, pin in SERVO_PINS.items():
        GPIO.setup(pin, GPIO.OUT)
        pwm = GPIO.PWM(pin, 50)  # 50 Hz
        pwm.start(0)
        set_angle(pwm, CERRADO)
        servos[clase] = pwm
    return servos

def set_angle(pwm, angle):
    """Mueve el servo al ángulo indicado."""
    duty = 2.5 + (angle / 180.0) * 10.0
    pwm.ChangeDutyCycle(duty)
    time.sleep(0.5)
    pwm.ChangeDutyCycle(0)

def abrir_compuerta(servos, clase):
    """Abre la compuerta de la clase indicada, espera, y cierra."""
    pwm = servos[clase]
    set_angle(pwm, ABIERTO)   # Abrir a 75°
    time.sleep(1.5)            # Esperar caída del objeto
    set_angle(pwm, CERRADO)   # Cerrar a 20°
```

---

## CONTENEDORES INTERNOS

```
    Vista superior (sin solapas):

    ┌──────────────────┬──────────────────┐
    │                  │                  │
    │   PLÁSTICO       │     PAPEL        │
    │    (azul)        │    (verde)       │
    │   ~20×20 cm      │   ~20×20 cm      │
    │                  │                  │
    ├──────────────────┼──────────────────┤
    │                  │                  │
    │    CARTÓN        │   ALUMINIO       │
    │   (naranja)      │    (gris)        │
    │   ~20×20 cm      │   ~20×20 cm      │
    │                  │                  │
    └──────────────────┴──────────────────┘
```

| Propiedad | Medida |
|-----------|--------|
| Forma | Cuadrada (~20×20 cm cada uno) |
| Alto | ~55 cm (espacio bajo las solapas hasta la base) |
| Capacidad | ~8-10 litros cada uno |
| Total | ~32-40 litros |
| Material | Contenedores plásticos o fabricados en MDF |
| Extracción | Puerta lateral o deslizables desde abajo |

---

## ANTI-ATASCO

| Riesgo | Solución |
|--------|----------|
| Objeto grande | Las solapas limitan el tamaño (~20 cm máx diagonal) |
| Objeto en el vértice | Ángulo + superficie lisa → desliza al abrir |
| Objeto pegajoso | Acabado liso en solapas (barniz o acrílico) |
| Dos objetos | Sensor IR → procesar uno a la vez |
| Servo no cierra | Spring return del SG90 + retry por software |

---

## LISTA DE MATERIALES — ESTRUCTURA

| Material | Uso | Costo MXN estimado |
|---------|-----|-------------------|
| MDF 6mm (hoja 120×60) | Paredes del bote | $150-250 |
| MDF 3mm o acrílico 3mm | 4 solapas (3-5mm espesor) | $80-150 |
| Servo SG90 × 4 | Control de solapas | $200-320 |
| Tornillos M2 × 8 | Montaje servos | $20-40 |
| Tubo metálico/varilla | Arco de cámara | $50-100 |
| Pintura acrílica | Acabado (gris + 4 colores solapas) | $100-200 |
| Contenedores plásticos × 4 | Botes internos | $100-200 |
| Pegamento/bisagras | Ensamblaje + puerta acceso | $50-80 |
| **Total estructura** | | **$750 - $1,340 MXN** |

---

## COSTO TOTAL DEL PROYECTO

| Concepto | Rango MXN |
|----------|-----------|
| Electrónica (RPi 5 + cámara + servos + sensor + fuente) | $2,190 – $3,070 |
| Estructura y mecanismo | $750 – $1,340 |
| **TOTAL** | **$2,940 – $4,410 MXN** |
| **Equivalente USD** | **~$147 – $220 USD** |

---

## NOTAS PARA EL EQUIPO MECÁNICO

1. **EL SERVO ES LA BISAGRA.** No necesitas bisagras, soportes L, ni varillaje.
2. **El servo va por FUERA.** 2 tornillos a la pared exterior. Solo el eje/horn pasan adentro.
3. **Solapa de 3-5 mm.** MDF delgado o acrílico. Superficie lisa para que deslice.
4. **Cerrado = 20°.** Solapa inclinada formando la pirámide.
5. **Abierto = 75°.** Solapa se abre hacia afuera/abajo, objeto cae.
6. **Solo UNA se abre a la vez.** Las otras 3 sostienen la pirámide.
7. **La cámara va en el ARCO.** No dentro del bote. Mira hacia abajo al centro.
8. **Piezas por compuerta:** 1 servo + 1 horn + 2 tornillos + 1 agujero. **Eso es todo.**
9. **40×40×70 cm.** Cortes rectos en MDF. Nada curvo, nada cilíndrico.
10. **4 colores:** Azul (plástico), Verde (papel), Naranja (cartón), Gris (aluminio).
