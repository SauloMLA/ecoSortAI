# FICHA TÉCNICA — EcoSort IA — Bowl con 2 Motores a Pasos

**Proyecto:** EcoSort IA  
**Documento:** Especificación para diseñador CAD  
**Revisión:** 1.0  
**Fecha:** 2026-02-13  
**Unidades:** mm (milímetros)  
**Tolerancias generales:** ±0.5 mm salvo indicación contraria

---

## 1. MOTOR NEMA 17 — DIMENSIONES DE REFERENCIA

*Fuente: Estándar NEMA. Verificar con ficha del proveedor antes de fabricar soportes.*

### 1.1 Vista frontal (cara de montaje)

```
                              ┌─────────────────────────────────────────┐
                              │           NEMA 17 — VISTA FRONTAL         │
                              │                                         │
        31.00                 │     ●─────────────────────────●         │
    ◄──────────────►          │    ╱ │                       │ ╲         │
                              │   ╱  │                       │  ╲        │
                              │  ●   │         Ø5.00         │   ●       │
                              │  │   │      (eje salida)     │   │       │
        31.00                  │  │   │           ●           │   │       │
    ◄──────────────►          │  │   │         centro         │   │       │
                              │  ●   │                       │   ●       │
                              │   ╲  │                       │  ╱        │
                              │    ╲ │                       │ ╱         │
                              │     ●─────────────────────────●          │
                              │                                         │
                              │  ◄────────── 42.00 ──────────►          │
                              │  ◄────────── 42.00 ──────────►          │
                              └─────────────────────────────────────────┘

    Patrón de agujeros: cuadrado 31×31 mm (centro a centro)
    Diámetro agujeros: Ø3.2 mm (para M3)
    Diámetro piloto (rebaje): Ø22 mm
```

### 1.2 Tabla de dimensiones — NEMA 17

| Ref | Parámetro | Valor (mm) | Tolerancia | Notas |
|-----|-----------|------------|------------|-------|
| A | Cara frontal (ancho) | 42.00 | ±0.2 | Cuadrado |
| B | Cara frontal (alto) | 42.00 | ±0.2 | Cuadrado |
| C | Distancia entre agujeros (centro a centro) | 31.00 | ±0.1 | Patrón cuadrado |
| D | Diámetro agujeros montaje | 3.20 | +0.2 | Para tornillo M3 |
| E | Diámetro eje de salida | 5.00 | -0.02 / +0.02 | Eje estándar |
| F | Diámetro piloto (rebaje) | 22.00 | ±0.2 | Centrado |
| G | Longitud cuerpo (34 mm stack) | 34.00 | ±1 | Modelo ligero |
| G | Longitud cuerpo (40 mm stack) | 40.00 | ±1 | **Recomendado** |
| G | Longitud cuerpo (48 mm stack) | 48.00 | ±1 | Alto torque |
| H | Longitud eje (típica) | 20.00 a 25.00 | — | Varía por fabricante |
| — | Roscas montaje | M3 | — | 4 agujeros |
| — | Peso (40 mm) | ~220 g | — | Referencia |

### 1.3 Vista lateral — NEMA 17

```
    VISTA LATERAL (corte)

         ┌─────────────────────┐
         │                     │
         │   NEMA 17           │
         │   cuerpo            │
         │                     │
    40   │                     │  ← Longitud 40 mm (recomendado)
    mm   │                     │
         │                     │
         └──────────┬──────────┘
                    │
                    │ Ø5 eje
                    │ 20-25 mm
                    ▼
```

---

## 2. BOWL (RECIPIENTE CENTRAL)

### 2.1 Vista superior

```
                              BOWL — VISTA SUPERIOR

                              ┌─────────────────────────────────────┐
                              │                                     │
                              │            Ø180.00                  │
                              │         ◄──────────►                │
                              │                                     │
                              │              ●                      │
                              │           centro                    │
                              │                                     │
                              │     ┌───┐         ┌───┐             │
                              │     │ A │         │ B │             │
                              │     │   │         │   │  Ejes de    │
                              │     └───┘    ●   └───┘  pivote     │
                              │              │   (M1, M2)           │
                              │     ┌───┐    │   ┌───┐             │
                              │     │ D │    │   │ C │             │
                              │     │   │    │   │   │             │
                              │     └───┘         └───┘             │
                              │                                     │
                              └─────────────────────────────────────┘
```

### 2.2 Vista lateral — Bowl (corte por eje de pivote)

```
    BOWL — VISTA LATERAL (corte)

    Origen de cotas: plano superior del borde

        0
        │
        │  ┌─────────────────────────────────────┐
        │ ╱                                       ╲
        │╱     R5.00 (borde redondeado)             ╲
      5 │───────────────────────────────────────────│  ← Espesor pared
        │╲                                         ╱
        │ ╲                                       ╱
        │  ╲                                     ╱
      60│   ╲         profundidad 60.00         ╱
        │    ╲                                 ╱
        │     ╲                               ╱
        │      ╲_____________________________╱
        │       │
        │       │  Eje pivote: Ø6.00
        │       │  Centrado en bowl
        │       │  Distancia desde borde superior: 30.00
        │       ●
        │
        └───────────────────────────────────────────
             0    90.00 (radio)    180.00 (diám)
```

### 2.3 Tabla de dimensiones — Bowl

| Ref | Parámetro | Valor (mm) | Tolerancia | Notas |
|-----|-----------|------------|------------|-------|
| — | Diámetro exterior | 180.00 | ±0.5 | Borde superior |
| — | Diámetro interior | 170.00 | ±0.5 | = 180 - 2×5 |
| — | Profundidad (desde borde) | 60.00 | ±1 | Hasta fondo |
| — | Espesor pared | 5.00 | ±0.3 | Uniforme |
| — | Radio borde (redondeo) | 5.00 | ±0.5 | Para deslizamiento |
| — | Diámetro eje pivote | 6.00 | +0.1 / -0.0 | Ajuste con rodamiento o buje |
| — | Altura eje desde borde | 30.00 | ±0.5 | Centro geométrico del bowl |
| — | Material | PLA o PETG | — | Impresión 3D, relleno 20% |
| — | Acabado interior | Lisa | — | Sin texturas para deslizamiento |

### 2.4 Forma del bowl

- **Opción A (recomendada):** Cono truncado — paredes rectas con ángulo ~15° desde vertical. Fondo plano Ø80 mm.
- **Opción B:** Semiesfera — más compleja de imprimir, mejor estética.
- **Requisito:** Los ejes de pivote M1 y M2 deben cruzar en el centro de masa del bowl (aprox. a 30 mm del borde superior, en el eje central).

---

## 3. SOPORTE DE MOTOR — NEMA 17

### 3.1 Vista frontal del soporte

```
    SOPORTE MOTOR — VISTA FRONTAL (contra la cara del motor)

    ┌─────────────────────────────────────────────────────────┐
    │                                                         │
    │     ●─────────────────────────────────────────●         │
    │    ╱ │                                     │ ╲           │
    │   ╱  │                                     │  ╲          │
    │  ●   │            Ø5.00                    │   ●        │
    │  │   │         (paso eje)                   │   │        │
    │  │   │             ●                        │   │        │
    │  ●   │                                     │   ●        │
    │   ╲  │                                     │  ╱         │
    │    ╲ │                                     │ ╱           │
    │     ●─────────────────────────────────────────●         │
    │                                                         │
    │  ◄──────────── 60.00 ────────────►                      │
    │                                                         │
    └─────────────────────────────────────────────────────────┘
    ◄──────────────── 60.00 ────────────────►

    Agujeros: 4× Ø3.2, patrón 31×31 mm (centro a centro)
    Espesor placa: 4.00 mm mínimo
    Material: PLA, PETG o MDF 6 mm
```

### 3.2 Vista lateral del soporte

```
    SOPORTE — VISTA LATERAL

         ┌─────────────────┐
         │   NEMA 17       │
         │   (motor)       │
         └────────┬────────┘
                  │
                  │ eje Ø5
                  │
    ┌─────────────┴─────────────┐
    │                            │
    │  Espesor: 4.00 mm          │  50.00 mm
    │  (o 6.00 si MDF)          │  (altura total
    │                            │   soporte)
    └────────────────────────────┘
```

### 3.3 Tabla de dimensiones — Soporte

| Ref | Parámetro | Valor (mm) | Tolerancia | Notas |
|-----|-----------|------------|------------|-------|
| — | Ancho placa | 60.00 | ±0.5 | Mínimo para NEMA 17 |
| — | Alto placa | 60.00 | ±0.5 | |
| — | Espesor | 4.00 (PLA) / 6.00 (MDF) | ±0.3 | |
| — | Agujeros M3 | 4× Ø3.2 | +0.2 | Patrón 31×31 mm |
| — | Paso eje (centro) | 21.00 desde cada borde | ±0.2 | Centrado en 42×42 |
| — | Altura total soporte | 50.00 | ±1 | Incluye espacio para motor |
| — | Cantidad | 2 | — | Uno por motor |

---

## 4. EJE DE PIVOTE

| Ref | Parámetro | Valor (mm) | Tolerancia | Notas |
|-----|-----------|------------|------------|-------|
| — | Diámetro | 6.00 | -0.05 / +0.05 | Varilla M6 o eje maquinado |
| — | Longitud | 100.00 | ±2 | Suficiente para cruzar bowl |
| — | Material | Acero inoxidable o acero | — | Varilla roscada M6 o lisa |
| — | Cantidad | 2 | — | Uno por eje (M1, M2) |

---

## 5. MARCO BASE — ESTRUCTURA

### 5.1 Vista superior — Distribución

```
    MARCO BASE — VISTA SUPERIOR (cotas en mm)

    0                   250                  500
    0 ┌──────────────────┬──────────────────┐
      │                  │                  │
      │    PLÁSTICO      │      PAPEL       │
      │   (cuadrante 1)  │  (cuadrante 2)   │
      │                  │                  │
 250 ├──────────────────┼──────────────────┤
      │         ●        │                  │
      │      BOWL        │   Centro 250,250 │
      │    (centro)      │                  │
      │    CARTÓN        │    ALUMINIO      │
      │  (cuadrante 3)   │  (cuadrante 4)   │
 500 └──────────────────┴──────────────────┘

    Marco exterior: 500 × 500 mm
    Divisores: 2 piezas, cruzan en centro
    Cada cuadrante: 250 × 250 mm (interior)
```

### 5.2 Tabla de dimensiones — Marco

| Pieza | Cantidad | Ancho (mm) | Alto (mm) | Espesor (mm) | Material |
|-------|----------|------------|-----------|--------------|----------|
| Base | 1 | 500 | 500 | 6 | MDF |
| Divisor longitudinal | 1 | 500 | 250 | 6 | MDF |
| Divisor transversal | 1 | 500 | 250 | 6 | MDF |
| Pared lateral (cada cuadrante) | 4 | 250 | 400 | 6 | MDF |
| Soporte cámara (arco) | 1 | 300 | 50 | 6 | MDF o tubo |

### 5.3 Posición del bowl respecto al marco

| Parámetro | Valor (mm) | Notas |
|-----------|------------|-------|
| Centro bowl X | 250.00 | Centro del marco |
| Centro bowl Y | 250.00 | Centro del marco |
| Altura borde bowl sobre base | 400.00 | Ajustar según contenedores |
| Altura cámara sobre bowl | 150.00 | Ver campo de visión |

---

## 6. ENSAMBLE GIMBAL — RELACIÓN ENTRE PIEZAS

```
    ESQUEMA DE ENSAMBLE (vista isométrica simplificada)

              Cámara
                 │
    ┌────────────┴────────────┐
    │                         │
    │      ╭─────────╮        │
    │      │  BOWL   │        │
    │      ╰────┬────╯        │
    │           │             │
    │    ════╪══╪═══         │  ← Eje M1 (eje X) ──┐
    │         ╪               │  ← Eje M2 (eje Y)   │
    │    ┌────┴────┐          │                      │
    │    │  M1     │  ┌───┐   │  Los ejes se cruzan  │
    │    └─────────┘  │M2 │   │  en el centro de     │
    │                 └───┘   │  masa del bowl        │
    └─────────────────────────┘  ──────────────────┘
```

**Orden de montaje sugerido:**
1. Marco base + divisores
2. Soportes de motor M1 y M2 fijados al marco (o a estructura elevada)
3. Ejes de pivote insertados en soportes
4. Bowl montado sobre ejes (con bujes o rodamientos si aplica)
5. Motores acoplados a ejes (cuando se defina acoplamiento)

---

## 7. ÁNGULOS DE INCLINACIÓN

| Clase | Eje | Ángulo desde horizontal | Sentido |
|-------|-----|-------------------------|---------|
| Plástico | M1 | 35° | Positivo (hacia frente) |
| Papel | M2 | 35° | Positivo (hacia derecha) |
| Cartón | M1 | 35° | Negativo (hacia atrás) |
| Aluminio | M2 | 35° | Negativo (hacia izquierda) |

*Ángulo mínimo para que objeto de 50 g deslice: ~30°. Se recomienda 35° con margen.*

---

## 8. RESUMEN — LISTA DE PIEZAS PARA DISEÑO CAD

| # | Pieza | Archivo sugerido | Prioridad |
|---|-------|-----------------|-----------|
| 1 | Bowl | `bowl_ecosort.stl` / `.step` | ALTA |
| 2 | Soporte motor NEMA 17 | `soporte_nema17.stl` / `.step` | ALTA |
| 3 | Marco base (cortes) | `marco_base.dxf` | ALTA |
| 4 | Buje eje-bowl (si aplica) | `buje_eje.stl` | MEDIA |
| 5 | Soporte cámara/arco | `soporte_camara.stl` | MEDIA |

---

## 9. REFERENCIAS

- Motor: NEMA 17, 40 mm stack, 28–40 N·cm, 1.3–1.7 A
- Driver: A4988 o TMC2209
- Fuente: 12 V, 3 A mínimo
- RPi 5 GPIO: M1 → STEP 17, DIR 27, EN 22; M2 → STEP 23, DIR 24, EN 25

---

*Documento generado para el equipo EcoSort IA — Sesión S004*
