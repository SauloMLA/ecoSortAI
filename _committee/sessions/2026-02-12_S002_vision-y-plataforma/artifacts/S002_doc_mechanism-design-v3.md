# Diseño del Mecanismo v3 — Estilo Ameru con 4 botes de cuarto de circulo

**Sesion:** S002  
**Autores:** CAD Architect, Mechanical Engineer, Anti-Jam Specialist  
**Fecha:** 2026-02-12  
**Revision:** 3.0 — Rediseño basado en referencia Ameru + requerimiento del equipo  
**Plano:** S002_sketch_design-v3-ameru.png

---

## Concepto

Bote de basura cilindrico con acabado elegante (estilo Ameru). El interior
contiene **4 botes independientes en forma de cuarto de circulo** que juntos
forman el cilindro completo. La **bandeja receptora en la parte superior rota**
para alinear su abertura con el bote correcto.

---

## DIMENSIONES GENERALES

| Componente | Medida |
|-----------|--------|
| Altura total del bote | 90 cm |
| Diametro exterior | 50 cm |
| Altura de la pantalla (con poste) | 100 cm desde el piso |
| Altura zona superior (camara + mecanismo) | 45 cm (desde la bandeja hasta mitad del bote) |
| Altura zona de botes | 45 cm |
| Diametro de abertura de bandeja | 15 cm |
| Pantalla | 7 pulgadas |

---

## ESTRUCTURA DE ARRIBA A ABAJO

### 1. PANTALLA (poste exterior)

```
    ┌─────────┐
    │ PANTALLA│  ← 7 pulgadas, muestra: clase detectada,
    │ 7"      │     confianza, estadisticas
    └────┬────┘
         │        ← Poste delgado desde la parte trasera
         │
```

- Pantalla LCD de 7" conectada por HDMI a la RPi 5
- Montada en un poste metalico o impreso en 3D
- Muestra en tiempo real: clase detectada, porcentaje, contador

### 2. BANDEJA RECEPTORA GIRATORIA (la parte superior del bote)

```
    Vista lateral (corte):

    ╔══════════════════════╗
    ║   BANDEJA RECEPTORA  ║  ← Superficie donde depositas el objeto
    ║  ┌──────┐            ║
    ║  │HUECO │            ║  ← Abertura descentrada (cae al bote de abajo)
    ║  └──────┘            ║
    ║      ↕ MOTOR         ║  ← Motor/servo rota toda la bandeja
    ╚══════════════════════╝
```

```
    Vista superior de la bandeja:

         ┌───────────────┐
        ╱    ┌──────┐     ╲
       ╱     │ HUECO│      ╲      La abertura esta en una posicion
      │      └──────┘       │     fija respecto a la bandeja.
      │         ●           │     Al ROTAR la bandeja, el hueco
       ╲      (eje)        ╱      se alinea con cada cuadrante.
        ╲                 ╱
         └───────────────┘
```

**Funcionamiento:**
1. El objeto se deposita en la bandeja (superficie plana)
2. La camara (dentro, mirando arriba) toma la foto
3. La IA clasifica
4. El servo/motor rota la bandeja para que el HUECO quede sobre el bote correcto
5. El objeto cae por gravedad a traves del hueco

### 3. ZONA INTERMEDIA (camara + electronica)

```
    ┌──────────────────────────┐
    │                          │
    │    ◉ CAMARA              │  ← Camara mirando ARRIBA hacia la bandeja
    │                          │     (ve el objeto desde abajo a traves
    │    ○ LED  ○ LED  ○ LED   │      de una ventana transparente)
    │                          │
    │    RPi 5 montada aqui    │  ← Electronica protegida
    │                          │
    │    [SERVO/MOTOR]         │  ← Motor que rota la bandeja
    │                          │
    └──────────────────────────┘
```

**Alternativa de posicion de camara:**
- **Opcion A:** Camara ARRIBA mirando abajo (dentro de la bandeja, protegida)
- **Opcion B:** Camara ABAJO mirando arriba a traves de ventana transparente
- **Recomendacion:** Opcion A es mas simple — la camara se monta dentro del
  borde superior del cilindro, mirando hacia la bandeja

### 4. ZONA DE BOTES (la mitad inferior)

```
    Vista frontal (puertas abiertas):

    ┌─── puerta ───┐ ┌─── puerta ───┐
    │               │ │               │
    │  ┌─────────┐  │ │  ┌─────────┐ │
    │  │ PLASTICO│  │ │  │  PAPEL  │ │
    │  │  (azul) │  │ │  │(amarillo)│ │
    │  │         │  │ │  │         │ │
    │  └─────────┘  │ │  └─────────┘ │
    │  ┌─────────┐  │ │  ┌─────────┐ │
    │  │ALUMINIO │  │ │  │ CARTON  │ │
    │  │  (gris) │  │ │  │ (cafe)  │ │
    │  │         │  │ │  │         │ │
    │  └─────────┘  │ │  └─────────┘ │
    └───────────────┘ └───────────────┘
```

```
    Vista superior (los 4 botes):

         ┌─────────────────────┐
        ╱  PLASTICO │  PAPEL    ╲
       ╱    (azul)  │ (amarillo) ╲
      │─────────────┼─────────────│
       ╲  ALUMINIO  │  CARTON   ╱
        ╲  (gris)   │  (cafe)  ╱
         └─────────────────────┘

    Cada bote es 1/4 de circulo.
    Los 4 juntos forman el circulo completo.
    Cada uno es extraible individualmente.
```

---

## MEDIDAS DE CADA BOTE

| Propiedad | Medida |
|-----------|--------|
| Forma | Cuarto de circulo (90° de arco) |
| Alto | 45 cm |
| Radio exterior | ~23 cm (dejando espacio para paredes) |
| Capacidad estimada | ~10-12 litros cada uno |
| Total 4 botes | ~40-48 litros |
| Material | Plastico rigido o lamina metalica |
| Bolsa interior | Si — bolsa de color diferente por tipo |

### Colores de bolsa por tipo

| Tipo | Color del bote/bolsa | Angulo |
|------|---------------------|--------|
| Plastico | Azul | 45° (centro del cuadrante) |
| Papel | Amarillo | 135° |
| Carton | Cafe/marron | 225° |
| Aluminio | Gris | 315° |

---

## MECANISMO DE SEPARACION — Bandeja giratoria

### Como funciona (paso a paso)

```
ESTADO INICIAL:
  Bandeja en posicion neutral (hueco tapado o en posicion segura)

PASO 1 — DEPOSITO:
  Usuario coloca objeto en la bandeja
  ↓
PASO 2 — DETECCION:
  Sensor IR detecta presencia del objeto
  ↓
PASO 3 — CLASIFICACION:
  Camara toma foto → RPi clasifica → resultado: "PAPEL" (135°)
  ↓
PASO 4 — ROTACION:
  Motor/servo rota la bandeja para que el HUECO quede sobre
  el cuadrante de PAPEL (135°)
  ↓
PASO 5 — CAIDA:
  El objeto cae por gravedad a traves del hueco al bote de PAPEL
  ↓
PASO 6 — RESET:
  La bandeja puede quedar en esa posicion o volver a neutral
  Pantalla muestra: "PAPEL ✓ — 94% confianza"
  ↓
PASO 7 — LISTO:
  Sistema espera siguiente objeto
```

### Motor/servo necesario

| Opcion | Modelo | Torque | Rotacion | Precio MXN |
|--------|--------|--------|----------|-----------|
| **A (recomendada)** | Motor paso a paso NEMA 17 + driver | Alto | 360° preciso | ~$150-250 |
| B | Servo de rotacion continua | Medio | 360° | ~$100-150 |
| C | MG996R modificado | Medio-alto | 0-270° | ~$50-80 |

> **Recomendacion:** Motor paso a paso NEMA 17 con driver A4988.
> Da rotacion precisa a cualquier angulo, tiene buen torque, y es
> estandar en impresoras 3D (facil de conseguir en Mexico).

---

## ACCESO A LOS BOTES

Dos puertas frontales con bisagras (como el Ameru):
- **Puerta izquierda:** Acceso a botes de Plastico y Aluminio
- **Puerta derecha:** Acceso a botes de Papel y Carton
- Cierre con iman o pestillo simple
- Los botes se extraen deslizandolos hacia afuera

---

## CARCASA EXTERIOR

| Propiedad | Especificacion |
|-----------|---------------|
| Material | Lamina metalica pintada en negro (ideal) o tubo PVC negro |
| Acabado | Mate o semi-brillante |
| Puertas | 2 puertas frontales con bisagras |
| Ventilacion | Rejillas discretas en la base (para la RPi) |
| Estetica | Limpio, moderno, minimalista — estilo Ameru |

---

## LISTA DE MATERIALES ACTUALIZADA (estructura)

| Material | Uso | Costo MXN estimado |
|---------|-----|-------------------|
| Tubo PVC negro 50cm diam o lamina metalica | Carcasa exterior | $300-500 |
| 4 contenedores plasticos cuarto-circulo | Botes internos | $200-400 (o fabricar) |
| Motor NEMA 17 + driver A4988 | Rotacion de bandeja | $150-250 |
| Rodamiento de bolas | Base giratoria de bandeja | $50-100 |
| Filamento PLA/PETG | Bandeja, soportes, tolva | $150-250 |
| Bisagras + pestillos | Puertas | $50-100 |
| Pantalla 7" HDMI | Display de estado | $500-800 |
| Poste metalico/impreso | Soporte de pantalla | $50-100 |
| Pintura negra mate | Acabado | $100-150 |
| **Total estructura** | | **$1,550 - $2,650 MXN** |

### Total del proyecto (hardware + estructura)

| Concepto | Rango MXN |
|----------|-----------|
| Electronica (RPi + camara + motor + fuente + sensor) | $2,500 – $3,500 |
| Estructura y mecanismo | $1,550 – $2,650 |
| **TOTAL PROYECTO** | **$4,050 – $6,150 MXN** |
| **Equivalente USD** | **~$200 – $310 USD** |
