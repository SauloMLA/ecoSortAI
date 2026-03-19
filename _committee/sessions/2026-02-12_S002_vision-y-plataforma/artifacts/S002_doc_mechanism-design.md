# Diseño del Mecanismo — EcoSort IA

**Sesion:** S002  
**Autores:** CAD Architect, Mechanical Engineer, Anti-Jam Specialist  
**Fecha:** 2026-02-12

---

## Concepto general

El mecanismo funciona por **gravedad + desvio con flaps servo-accionados**.

```
              ┌──────────────┐
              │   TOLVA DE   │  ← Objeto entra por arriba
              │   ENTRADA    │
              └──────┬───────┘
                     │
              ┌──────▼───────┐
              │   CAMARA DE  │  ← Camara RPi + LEDs laterales
              │  INSPECCION  │     Fondo plano para foto estable
              │  (iluminada) │     Sensor IR detecta presencia
              └──────┬───────┘
                     │
              ┌──────▼───────┐
              │  MECANISMO   │  ← 4 flaps con servos SG90
              │  DE DESVIO   │     Solo 1 se abre a la vez
              │              │     Los demas quedan cerrados
              └──┬──┬──┬──┬──┘
                 │  │  │  │
              ┌──▼──▼──▼──▼──┐
              │ 4 CONTENEDORES│
              │ P  Pa Ca Al  │  ← Plastico, Papel, Carton, Aluminio
              └──────────────┘
```

## Dimensiones propuestas

| Componente | Ancho | Profundo | Alto | Material |
|-----------|-------|----------|------|----------|
| Estructura total | 60 cm | 40 cm | 50 cm | MDF / Acrilico |
| Tolva de entrada | 20 cm | 20 cm | 15 cm | Impresion 3D / Carton grueso |
| Camara de inspeccion | 30 cm | 30 cm | 15 cm | Acrilico transparente |
| Contenedores | 15 cm c/u | 30 cm | 20 cm | Plastico / Carton |

## Mecanismo de desvio: Flaps con servos

### Como funciona

1. El objeto cae por la tolva hacia la camara de inspeccion
2. Un sensor IR detecta que hay un objeto presente
3. La camara toma la foto, la RPi clasifica
4. Se abre el flap correspondiente (servo gira 90°)
5. El objeto cae por gravedad al contenedor correcto
6. El flap se cierra (servo vuelve a 0°)

### Disposicion de flaps

```
    Vista frontal del area de desvio:

    ┌────────────────────────────────────────┐
    │            Placa de caida              │
    │                                        │
    │  [Flap 1]  [Flap 2]  [Flap 3]  [Flap 4]
    │  Plastico   Papel    Carton   Aluminio │
    │     ↓         ↓        ↓         ↓    │
    │  ┌─────┐  ┌─────┐  ┌─────┐  ┌─────┐  │
    │  │ BIN │  │ BIN │  │ BIN │  │ BIN │  │
    │  │  1  │  │  2  │  │  3  │  │  4  │  │
    │  └─────┘  └─────┘  └─────┘  └─────┘  │
    └────────────────────────────────────────┘
```

### Alternativa: Rampa con compuerta unica

Si los 4 flaps resultan complejos, se puede simplificar a:
- Una **rampa inclinada** con una sola compuerta rotativa
- La compuerta gira a 4 posiciones diferentes (0°, 45°, 90°, 135°)
- Usa un solo servo MG996R (mas torque)

## Anti-atasco

| Riesgo | Solucion |
|--------|----------|
| Objeto muy grande | Tolva con limitador de tamaño (15cm max) |
| Objeto pegajoso/mojado | Superficies lisas, angulo > 45° |
| Dos objetos a la vez | Sensor IR con delay — procesar uno a la vez |
| Flap no cierra bien | Spring return + verificacion de posicion |

## Iluminacion controlada

La camara de inspeccion tiene iluminacion LED controlada para que las fotos
siempre tengan la misma luz, independientemente del ambiente externo.

```
    ┌─────────────────────┐
    │  [LED]    CAM   [LED]│  ← Tiras LED blancas laterales
    │         ┌───┐        │
    │         │ ◉ │        │  ← Camara mirando hacia abajo
    │         └───┘        │
    │                      │
    │  ==================  │  ← Placa de inspeccion (fondo blanco)
    │  [  OBJETO AQUI   ]  │
    └─────────────────────┘
```
