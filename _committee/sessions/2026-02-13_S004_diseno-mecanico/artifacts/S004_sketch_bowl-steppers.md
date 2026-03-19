# Sketch — Bowl Central con 2 Motores a Pasos

**Sesión:** S004  
**Fecha:** 2026-02-13  
**Estado:** Concepto — sustituye diseño v4 (pirámide con servos)

---

## CONCEPTO GENERAL

Bowl (recipiente) en el centro que recibe el objeto. Dos motores a pasos controlan la inclinación en dos ejes (X e Y), formando un sistema tipo gimbal. Al inclinar el bowl hacia uno de los 4 cuadrantes, el objeto cae al contenedor correspondiente.

```
                    ┌─ CÁMARA + SENSOR IR
                    │  (arco sobre el bowl)
                ┌───┴───┐
                │  ◉ IR │
            ┌───┘       └───┐
            │               │
    ┌───────┴───────────────┴───────┐
    │                               │
    │         ┌─────────┐            │
    │         │  BOWL   │            │  ← Bowl semiesférico o cónico
    │         │  (U)    │            │     en el centro
    │         │ objeto  │            │
    │         └────┬────┘            │
    │              │                 │
    │     M1 ←─────┼─────→ M2        │  ← Eje X (M1) y Eje Y (M2)
    │              │                 │     cruzan bajo el bowl
    │   ┌──────────┼──────────┐      │
    │   │  PLÁST   │   PAPEL   │      │
    │   │  (azul)  │  (verde)  │      │
    │   ├──────────┼──────────┤      │
    │   │  CARTÓN  │ ALUMINIO  │      │
    │   │ (naranja)│  (gris)   │      │
    │   └──────────┴──────────┘      │
    └───────────────────────────────┘
```

---

## VISTA LATERAL — Ejes de inclinación

```
    Vista lateral (corte por eje de M1):

              CÁMARA
                 │
    ┌────────────┴────────────┐
    │      ╭─────────╮        │
    │      │  BOWL   │        │  ← Bowl en posición neutra (horizontal)
    │      │   (U)   │        │
    │      ╰────┬────╯        │
    │           │             │
    │    ═══════╪═══════      │  ← Eje de M1 (perpendicular al papel)
    │           │             │
    │    ┌──────┴──────┐      │
    │    │   MOTOR 1   │      │  ← NEMA 17, montado en marco
    │    │  (stepper)  │      │
    │    └─────────────┘      │
    └─────────────────────────┘

    Vista lateral (corte por eje de M2):

              CÁMARA
                 │
    ┌────────────┴────────────┐
    │      ╭─────────╮        │
    │      │  BOWL   │        │
    │      ╰────┬────╯        │
    │           │             │
    │    ═══════╪═══════      │  ← Eje de M2 (perpendicular al de M1)
    │           │             │
    │    ┌──────┴──────┐      │
    │    │   MOTOR 2   │      │
    │    └─────────────┘      │
    └─────────────────────────┘
```

---

## VISTA SUPERIOR — Mapeo bowl → contenedores

```
                    FRENTE
                       ▲
                       │
    ┌──────────────────┼──────────────────┐
    │                  │                  │
    │     PLÁSTICO     │      PAPEL       │
    │      (azul)      │     (verde)      │
    │                  │                  │
    │   M1 inclina     │   M1 inclina     │
    │   hacia FRENTE   │   hacia FRENTE   │
    │   + M2 neutro    │   + M2 neutro    │
    │                  │                  │
    ├──────────────────┼──────────────────┤
    │         ╭───╮    │    ╭───╮         │
    │         │ U │    │    │ U │         │  ← Bowl inclinado
    │         ╰───╯    │    ╰───╯         │     hacia cada cuadrante
    │                  │                  │
    │     CARTÓN       │   ALUMINIO       │
    │   (naranja)      │    (gris)        │
    │                  │                  │
    │   M1 inclina     │   M1 inclina     │
    │   hacia ATRÁS    │   hacia ATRÁS    │
    │   + M2 neutro    │   + M2 neutro    │
    │                  │                  │
    └──────────────────┴──────────────────┘
         IZQUIERDA ◄───┼───► DERECHA
                       │
                    M2
```

**Lógica de inclinación:**

| Clase     | M1 (eje X) | M2 (eje Y) | Dirección del bowl |
|-----------|------------|------------|--------------------|
| Plástico  | +α°        | 0°         | Frente             |
| Papel     | 0°         | +β°        | Derecha            |
| Cartón    | -α°        | 0°         | Atrás              |
| Aluminio  | 0°         | -β°        | Izquierda          |

(α y β = ángulo de inclinación para que el objeto caiga, típicamente 30–45°)

---

## DIMENSIONES PROPUESTAS

| Componente        | Medida      | Notas                          |
|------------------|-------------|--------------------------------|
| Bowl diámetro    | 15–20 cm    | Suficiente para botella 1L     |
| Bowl profundidad | 5–8 cm      | Evitar que el objeto salte      |
| Marco base       | 50×50 cm    | Contenedores 4× ~25×25 cm       |
| Altura total     | ~60–70 cm   | Incluye marco + contenedores   |
| Distancia eje a centro bowl | ~8–10 cm | Brazo de palanca para torque   |

---

## MOTORES A PASOS — ESPECIFICACIONES

### Opción recomendada: NEMA 17

| Parámetro           | Valor                    |
|---------------------|--------------------------|
| **Frame (cara frontal)** | 42.3 × 42.3 mm      |
| **Longitud cuerpo** | 34 mm (single) / 40 mm (double) / 48 mm (triple) |
| **Diámetro eje**    | 5 mm                     |
| **Agujeros montaje**| 4× M3, patrón 31 mm      |
| **Paso**            | 1.8° (200 pasos/vuelta)  |
| **Torque holding**  | 23 N·cm (single) / 42 N·cm (double) / 53 N·cm (triple) |
| **Voltaje**         | 12 V típico              |
| **Corriente/fase**  | 1.0–1.5 A                |

**Recomendación:** NEMA 17 **40 mm** (double stack) — torque ~0.42 N·m suficiente para bowl + objeto ~500 g.

### Alternativa compacta: NEMA 14

| Parámetro           | Valor                    |
|---------------------|--------------------------|
| **Frame**           | 35.2 × 35.2 mm           |
| **Longitud**        | 27–40 mm                 |
| **Diámetro eje**    | 5 mm                     |
| **Torque holding**  | 12–18 N·cm               |
| **Paso**            | 1.8°                     |

**Uso:** Solo si el bowl es muy ligero (<200 g total). Para bowl de 15–20 cm, preferir NEMA 17.

### Drivers necesarios

| Componente   | Cantidad | Opciones              | Conexión RPi      |
|-------------|----------|------------------------|-------------------|
| Driver      | 2        | A4988, DRV8825, TMC2209| GPIO: STEP, DIR, ENABLE |
| Fuente 12V  | 1        | 2–3 A mínimo           | Alimentación drivers |

**Pines GPIO sugeridos (RPi 5):**

| Motor | STEP | DIR  | ENABLE |
|-------|------|------|--------|
| M1    | 17   | 27   | 22     |
| M2    | 23   | 24   | 25     |

---

## SECUENCIA DE OPERACIÓN

```
1. Usuario deposita objeto en el bowl (posición neutra, horizontal)
2. Sensor IR detecta objeto → cámara captura imagen
3. Modelo clasifica → ej. "plástico" 92%
4. Si confianza ≥ 70%:
   - M1 y M2 inclinan bowl hacia el cuadrante PLÁSTICO (frente)
   - Objeto desliza y cae al contenedor
5. M1 y M2 regresan a posición neutra
6. Listo para siguiente objeto
```

---

## DISEÑO CAD — Bowl y soportes

### Bowl — geometría

```
    Vista lateral del bowl (corte):

              ╭─────────────────╮
             ╱                   ╲
            ╱                     ╲
           │    Ø 180 mm          │  ← Diámetro interior
           │   profundidad 60mm  │
            ╲                     ╱
             ╲                   ╱
              ╰────────┬────────╯
                       │
              ┌────────┴────────┐
              │  Eje pivote Ø6  │  ← Varilla M6 o eje impreso
              └────────────────┘
```

| Parámetro | Valor | Notas |
|-----------|-------|-------|
| Diámetro exterior | 180 mm | Para botella 1L (~30 cm) |
| Diámetro interior | 170 mm | Espesor pared 5 mm |
| Profundidad | 60 mm | Evita que objetos salten |
| Espesor pared | 5 mm | PLA/PETG impreso |
| Radio borde | 5 mm | Redondeado para deslizamiento |

**Forma:** Semiesférica o cono truncado (más fácil de imprimir). El fondo plano ayuda a que objetos no rueden antes de inclinar.

### Soportes de motor — dimensiones

```
    Soporte NEMA 17 (vista frontal):

    ┌─────────────────────────┐
    │  ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄  │
    │  █  NEMA 17  42×42  █  │  ← Motor
    │  ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀  │
    │         │              │
    │    ┌────┴────┐         │
    │    │ 31×31  │         │  ← Patrón M3
    │    │ 4 aguj │         │
    │    └────────┘         │
    └─────────────────────────┘

    Dimensiones del soporte:
    - Alto: 50 mm (espacio para motor + eje)
    - Ancho: 60 mm (para 42 mm motor + tornillos)
    - Agujeros M3: patrón 31×31 mm (estándar NEMA 17)
    - Eje de salida: centrado, Ø5 mm
```

**Montaje gimbal:** El soporte del motor M1 se fija al marco. El eje de M1 atraviesa el bowl. El soporte de M2 se monta sobre el eje de M1 (o en marco perpendicular). Los ejes deben cruzarse en el centro de masa del bowl.

### Planos de corte (MDF marco)

| Pieza | Cantidad | Dimensiones | Notas |
|-------|----------|-------------|-------|
| Base | 1 | 500×500 mm | Marco inferior |
| Divisores | 2 | 500×250 mm | Forman 4 cuadrantes |
| Paredes laterales | 4 | 250×400 mm | Cada contenedor |
| Soporte cámara | 1 | 300×50 mm | Arco o brazo |

---

## DÓNDE COMPRAR — Motores y drivers

### Motores NEMA 17

| Tienda | Producto | Precio | Ficha técnica / Enlace |
|--------|----------|--------|------------------------|
| **Maquinaria y Control** | NEMA 17, 12V 1.3A | $185 MXN | [maquinariaycontrol.com.mx/tienda/nema17](https://maquinariaycontrol.com.mx/tienda/nema17) — 28 N·cm, 1.8°, 4 cables |
| **Amazon México** | NEMA 17 varios | $200–400 MXN | [amazon.com.mx](https://www.amazon.com.mx/s?k=nema+17) — buscar "NEMA 17 stepper" |
| **Mercado Libre** | NEMA 17 impresora 3D | $150–300 MXN | [mercadolibre.com.mx](https://listado.mercadolibre.com.mx/nema-17) |
| **HTA3D** (internacional) | 17HS3401, 17HS4401 | ~$15–25 USD | [hta3d.com](https://www.hta3d.com) — datasheets en página |

**Especificaciones Maquinaria y Control (NEMA 17 @ $185):**

| Parámetro | Valor |
|-----------|-------|
| Corriente nominal | 1.3 A |
| Voltaje | 12 VCD |
| Resistencia de fase | 2.4 Ω |
| Inductancia de fase | 2.8 mH |
| Par de sujeción | 28 N·cm (min) |
| Ángulo de paso | 1.8° (200 pasos/vuelta) |
| Cables | 4 |
| Peso | 220 g |

**Fichas técnicas (PDF):**

| Modelo | Datasheet | Especificaciones clave |
|--------|-----------|------------------------|
| 17HS4401 | [alldatasheet.com](https://www.alldatasheet.com/datasheet-pdf/pdf/1245671/NINGBO/17HS4401.html) | 40 mm, 40 N·cm, 1.7A, 12V |
| 17HS3401 | [hta3d.com](https://www.hta3d.com/en/nema-17-stepper-motor-17hs3401-42hs34-42-34-5mm-d-shaft) | 34 mm, 28 N·cm, 1.3A |
| NEMA 17 genérico | [datasheetspdf.com](https://datasheetspdf.com/datasheet/NEMA17.html) | Referencia estándar |

### Drivers

| Tienda | Producto | Precio | Especificaciones |
|--------|----------|--------|------------------|
| **117 MX Electrónica** | A4988 | $33 MXN | [117mx.com.mx](https://117mx.com.mx/producto/a4988-driver-controlador-de-motor-a-pasos/) — 8–35V, 2A máx, STEP/DIR |
| **Inky.mx** | TMC2209 V2.0 | $150 MXN | [inky.mx](https://www.inky.mx) — silencioso, UART, 1.7A RMS |
| **Patzitec** | TMC2209 V3.0 | ~$150 MXN | [patzitec.com](https://patzitec.com/producto/driver-tmc2209-v3-0/) |
| **Mercado Libre** | TMC2209 V4.0 | $100–200 MXN | [mercadolibre.com.mx](https://www.mercadolibre.com.mx) — buscar "TMC2209" |

### Fuente 12V

| Tienda | Producto | Precio | Notas |
|--------|----------|--------|-------|
| Amazon México | Fuente 12V 3A | $80–120 MXN | 2× NEMA 17 @ 1.3A = 2.6A mínimo |
| Mercado Libre | Adaptador 12V 5A | $100–150 MXN | Margen para RPi si se usa misma fuente |

---

## PIEZAS A FABRICAR

| Pieza           | Material      | Fabricación        |
|-----------------|---------------|--------------------|
| Bowl            | PLA/PETG 3D   | Impresión 3D — Ø180×60 mm |
| Marco base      | MDF 6 mm      | Corte láser o manual |
| Soportes motores| PLA o MDF     | Impresión 3D — 60×50×20 mm c/u |
| Ejes de pivote  | Varilla M6 × 100 mm | Ferretería        |
| Contenedores    | Plástico o MDF | Comercial o fabricado |

---

## COSTO ESTIMADO (motores)

| Item                    | Cantidad | Rango MXN   | Fuente ejemplo |
|-------------------------|----------|-------------|----------------|
| NEMA 17                 | 2        | $370        | Maquinaria y Control @ $185 c/u |
| Drivers A4988            | 2        | $66         | 117 MX @ $33 c/u |
| Fuente 12V 3A           | 1        | $80–120     | Amazon / ML |
| **Subtotal motores**    |          | **$516–556**| |

*(Estructura, bowl y contenedores aparte)*

**Alternativa con TMC2209 (más silencioso):** +$234 (2× $117) → total ~$750

---

## NOTAS PARA PRÓXIMOS PASOS

1. Definir geometría exacta del bowl (diámetro, profundidad, forma)
2. Diseñar soportes de motor y ejes de pivote en CAD
3. Calcular ángulos α y β mínimos para que el objeto caiga de forma fiable
4. Actualizar `config.py` con pines GPIO para steppers
5. Implementar control de motores en `classify.py` (reemplazar lógica de servos)
